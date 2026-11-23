-- ════════════════════════════════════════════════════════════════════════════
-- Hồ Sơ Mật · chơi nhiều người
--
--   profiles        tên hiển thị + màu của mỗi người chơi (tạo tự động khi đăng ký)
--   case_questions  đáp án từng câu hỏi (chỉ server đọc; nạp bằng tools/sync-cases.mjs)
--   rooms           phòng chơi của một hồ sơ, có mã mời 6 số hết hạn sau 30 phút
--   room_members    thành viên phòng (host | player)
--   room_state      lựa chọn chung đang soạn: ghim bằng chứng, dòng khai, phương án
--   room_progress   tiến trình từng câu: đã giải, số lần thử, số gợi ý
--   room_notes      sổ tay nhóm
--   room_events     nhật ký hoạt động (ai ghim gì, ai gửi kết luận…)
--   join_attempts   chống dò mã mời
--
-- Mọi thao tác quan trọng đi qua hàm security definer (create_room, join_room, submit_answer…),
-- bảng chỉ cho thành viên phòng đọc (RLS). Kênh realtime "room:<id>" là kênh private, chỉ thành viên vào được.
-- ════════════════════════════════════════════════════════════════════════════

-- ── profiles ──────────────────────────────────────────────────────────────
create table public.profiles (
  id uuid primary key references auth.users (id) on delete cascade,
  display_name text not null default 'Điều tra viên' check (char_length(display_name) between 1 and 40),
  color text not null default '#d9452f' check (color ~ '^#[0-9a-fA-F]{6}$'),
  created_at timestamptz not null default now()
);

create function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, display_name, color)
  values (
    new.id,
    left(coalesce(nullif(trim(new.raw_user_meta_data ->> 'display_name'), ''), nullif(split_part(new.email, '@', 1), ''), 'Điều tra viên'), 40),
    (array['#d9452f', '#1f4fa8', '#2f8f5b', '#b7791f', '#7b4bb7', '#c2417a'])[1 + floor(random() * 6)::int]
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ── answers (server only) ───────────────────────────────────────────────
create table public.case_questions (
  case_id text not null check (case_id ~ '^[a-z0-9-]{1,60}$'),
  question_id text not null,
  ord int not null,
  stage int not null default 1,
  type text not null check (type in ('evidence', 'line', 'choice')),
  answer jsonb not null default '[]'::jsonb check (jsonb_typeof(answer) = 'array'),
  has_options boolean not null default true,
  hint_count int not null default 0,
  updated_at timestamptz not null default now(),
  primary key (case_id, question_id)
);

-- ── rooms ─────────────────────────────────────────────────────────────────
create table public.rooms (
  id uuid primary key default gen_random_uuid(),
  case_id text not null check (case_id ~ '^[a-z0-9-]{1,60}$'),
  host_id uuid not null references public.profiles (id) on delete cascade,
  name text not null default '' check (char_length(name) <= 60),
  status text not null default 'lobby' check (status in ('lobby', 'playing', 'finished')),
  join_code text unique check (join_code ~ '^[0-9]{6}$'),
  join_code_expires_at timestamptz,
  max_players int not null default 6 check (max_players between 2 and 12),
  created_at timestamptz not null default now(),
  started_at timestamptz,
  finished_at timestamptz
);
create index rooms_host_idx on public.rooms (host_id);

create table public.room_members (
  room_id uuid not null references public.rooms (id) on delete cascade,
  user_id uuid not null references public.profiles (id) on delete cascade,
  role text not null default 'player' check (role in ('host', 'player')),
  joined_at timestamptz not null default now(),
  primary key (room_id, user_id)
);
create index room_members_user_idx on public.room_members (user_id);

create table public.room_state (
  room_id uuid primary key references public.rooms (id) on delete cascade,
  pins jsonb not null default '[]'::jsonb check (jsonb_typeof(pins) = 'array' and jsonb_array_length(pins) <= 6),
  lines jsonb not null default '{}'::jsonb check (jsonb_typeof(lines) = 'object'),
  picks jsonb not null default '{}'::jsonb check (jsonb_typeof(picks) = 'object'),
  updated_by uuid references public.profiles (id) on delete set null,
  updated_at timestamptz not null default now()
);

create table public.room_progress (
  room_id uuid not null references public.rooms (id) on delete cascade,
  question_id text not null,
  solved boolean not null default false,
  solved_by uuid references public.profiles (id) on delete set null,
  solved_at timestamptz,
  tries int not null default 0,
  hints int not null default 0,
  primary key (room_id, question_id)
);

create table public.room_notes (
  id uuid primary key default gen_random_uuid(),
  room_id uuid not null references public.rooms (id) on delete cascade,
  user_id uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  kind text not null default 'text' check (kind in ('text', 'quote')),
  body text not null default '' check (char_length(body) <= 4000),
  ref jsonb check (ref is null or jsonb_typeof(ref) = 'object'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index room_notes_room_idx on public.room_notes (room_id, created_at);

create table public.room_events (
  id bigint generated always as identity primary key,
  room_id uuid not null references public.rooms (id) on delete cascade,
  user_id uuid default auth.uid() references public.profiles (id) on delete set null,
  kind text not null check (kind in ('join', 'leave', 'kick', 'start', 'pin', 'line', 'pick', 'submit', 'hint', 'finish')),
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
create index room_events_room_idx on public.room_events (room_id, id desc);

create table public.join_attempts (
  user_id uuid not null references auth.users (id) on delete cascade,
  ok boolean not null,
  at timestamptz not null default now()
);
create index join_attempts_user_idx on public.join_attempts (user_id, at desc);

-- ── helpers ───────────────────────────────────────────────────────────────
create function public.is_room_member(p_room uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (select 1 from public.room_members m where m.room_id = p_room and m.user_id = (select auth.uid()));
$$;

create function public.is_room_host(p_room uuid)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (select 1 from public.rooms r where r.id = p_room and r.host_id = (select auth.uid()));
$$;

-- 6 random digits from a cryptographic source, unique among live codes
create function public.new_join_code()
returns text
language plpgsql
volatile
security definer
set search_path = ''
as $$
declare
  c text;
begin
  update public.rooms set join_code = null where join_code is not null and join_code_expires_at < now();
  loop
    c := lpad((('x' || encode(extensions.gen_random_bytes(4), 'hex'))::bit(32)::bigint % 1000000)::text, 6, '0');
    exit when not exists (select 1 from public.rooms r where r.join_code = c);
  end loop;
  return c;
end;
$$;

-- ── RLS ───────────────────────────────────────────────────────────────────
alter table public.profiles enable row level security;
alter table public.case_questions enable row level security;  -- no policies: invisible to clients
alter table public.rooms enable row level security;
alter table public.room_members enable row level security;
alter table public.room_state enable row level security;
alter table public.room_progress enable row level security;
alter table public.room_notes enable row level security;
alter table public.room_events enable row level security;
alter table public.join_attempts enable row level security;   -- no policies

create policy "profiles readable by signed-in users" on public.profiles
  for select to authenticated using (true);
create policy "update own profile" on public.profiles
  for update to authenticated using (id = (select auth.uid())) with check (id = (select auth.uid()));

create policy "members read room" on public.rooms
  for select to authenticated using (public.is_room_member(id));
create policy "host updates room settings" on public.rooms
  for update to authenticated using (host_id = (select auth.uid())) with check (host_id = (select auth.uid()));

create policy "members read members" on public.room_members
  for select to authenticated using (public.is_room_member(room_id));

create policy "members read state" on public.room_state
  for select to authenticated using (public.is_room_member(room_id));
create policy "members edit state" on public.room_state
  for update to authenticated using (public.is_room_member(room_id)) with check (public.is_room_member(room_id));

create policy "members read progress" on public.room_progress
  for select to authenticated using (public.is_room_member(room_id));

create policy "members read notes" on public.room_notes
  for select to authenticated using (public.is_room_member(room_id));
create policy "members add own notes" on public.room_notes
  for insert to authenticated with check (public.is_room_member(room_id) and user_id = (select auth.uid()));
create policy "edit own notes" on public.room_notes
  for update to authenticated using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()) and public.is_room_member(room_id));
create policy "delete own notes" on public.room_notes
  for delete to authenticated using (user_id = (select auth.uid()));

create policy "members read events" on public.room_events
  for select to authenticated using (public.is_room_member(room_id));
create policy "members log selection events" on public.room_events
  for insert to authenticated with check (public.is_room_member(room_id) and user_id = (select auth.uid()) and kind in ('pin', 'line', 'pick'));

-- explicit grants (newer projects do not grant table access to API roles by default); RLS still filters rows
grant select on public.profiles, public.rooms, public.room_members, public.room_state, public.room_progress,
  public.room_notes, public.room_events to authenticated;
grant insert, delete on public.room_notes to authenticated;
grant insert on public.room_events to authenticated;
grant all on public.case_questions to service_role;  -- tools/sync-cases.mjs (secret key)

-- column-level limits on what clients may write directly
revoke all on public.case_questions, public.join_attempts from anon, authenticated;
revoke all on public.rooms, public.room_members, public.room_state, public.room_progress, public.room_notes, public.room_events, public.profiles from anon;
revoke insert, update, delete on public.rooms, public.room_members, public.room_progress, public.room_state from authenticated;
grant update (name, max_players) on public.rooms to authenticated;
grant update (pins, lines, picks, updated_by, updated_at) on public.room_state to authenticated;
revoke update on public.profiles from authenticated;
grant update (display_name, color) on public.profiles to authenticated;
revoke update on public.room_notes from authenticated;
grant update (body, updated_at) on public.room_notes to authenticated;

-- ── RPC: rooms ────────────────────────────────────────────────────────────
create function public.create_room(p_case_id text, p_name text default '')
returns public.rooms
language plpgsql
security definer
set search_path = ''
as $$
declare
  uid uuid := auth.uid();
  r public.rooms;
begin
  if uid is null then raise exception 'AUTH_REQUIRED'; end if;
  if not exists (select 1 from public.case_questions q where q.case_id = p_case_id) then
    raise exception 'CASE_NOT_SYNCED';
  end if;
  if (select count(*) from public.rooms x where x.host_id = uid and x.created_at > now() - interval '1 day') >= 20 then
    raise exception 'TOO_MANY_ROOMS';
  end if;
  insert into public.profiles (id) values (uid) on conflict (id) do nothing;
  insert into public.rooms (case_id, host_id, name, join_code, join_code_expires_at)
    values (p_case_id, uid, left(coalesce(p_name, ''), 60), public.new_join_code(), now() + interval '30 minutes')
    returning * into r;
  insert into public.room_members (room_id, user_id, role) values (r.id, uid, 'host');
  insert into public.room_state (room_id) values (r.id);
  insert into public.room_progress (room_id, question_id)
    select r.id, q.question_id from public.case_questions q where q.case_id = p_case_id;
  insert into public.room_events (room_id, user_id, kind) values (r.id, uid, 'join');
  return r;
end;
$$;

create function public.refresh_join_code(p_room uuid)
returns public.rooms
language plpgsql
security definer
set search_path = ''
as $$
declare
  r public.rooms;
begin
  if not public.is_room_host(p_room) then raise exception 'HOST_ONLY'; end if;
  update public.rooms
    set join_code = null where id = p_room;
  update public.rooms
    set join_code = public.new_join_code(), join_code_expires_at = now() + interval '30 minutes'
    where id = p_room and status <> 'finished'
    returning * into r;
  if r.id is null then raise exception 'ROOM_FINISHED'; end if;
  return r;
end;
$$;

-- Returns {ok, room_id} or {ok:false, error}. Never raises for a bad code, so the failed attempt is recorded.
create function public.join_room(p_code text)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  uid uuid := auth.uid();
  r public.rooms;
  n int;
begin
  if uid is null then return jsonb_build_object('ok', false, 'error', 'AUTH_REQUIRED'); end if;
  if (select count(*) from public.join_attempts a where a.user_id = uid and not a.ok and a.at > now() - interval '10 minutes') >= 8 then
    return jsonb_build_object('ok', false, 'error', 'TOO_MANY_ATTEMPTS');
  end if;
  select * into r from public.rooms x
    where x.join_code = trim(p_code) and x.join_code_expires_at > now() and x.status <> 'finished'
    for update;
  if r.id is null then
    insert into public.join_attempts (user_id, ok) values (uid, false);
    return jsonb_build_object('ok', false, 'error', 'INVALID_CODE');
  end if;
  insert into public.profiles (id) values (uid) on conflict (id) do nothing;
  if exists (select 1 from public.room_members m where m.room_id = r.id and m.user_id = uid) then
    return jsonb_build_object('ok', true, 'room_id', r.id);
  end if;
  select count(*) into n from public.room_members m where m.room_id = r.id;
  if n >= r.max_players then return jsonb_build_object('ok', false, 'error', 'ROOM_FULL'); end if;
  insert into public.room_members (room_id, user_id, role) values (r.id, uid, 'player');
  insert into public.room_events (room_id, user_id, kind) values (r.id, uid, 'join');
  insert into public.join_attempts (user_id, ok) values (uid, true);
  return jsonb_build_object('ok', true, 'room_id', r.id);
end;
$$;

create function public.start_room(p_room uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  if not public.is_room_host(p_room) then raise exception 'HOST_ONLY'; end if;
  update public.rooms set status = 'playing', started_at = coalesce(started_at, now())
    where id = p_room and status = 'lobby';
  if found then insert into public.room_events (room_id, user_id, kind) values (p_room, auth.uid(), 'start'); end if;
end;
$$;

-- Leaving as host hands the room to the longest-standing member; the last one out closes it.
create function public.leave_room(p_room uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  uid uuid := auth.uid();
  heir uuid;
begin
  if not public.is_room_member(p_room) then return; end if;
  delete from public.room_members where room_id = p_room and user_id = uid;
  insert into public.room_events (room_id, user_id, kind) values (p_room, uid, 'leave');
  if public.is_room_host(p_room) then
    select m.user_id into heir from public.room_members m where m.room_id = p_room order by m.joined_at limit 1;
    if heir is null then
      delete from public.rooms where id = p_room;
    else
      update public.rooms set host_id = heir where id = p_room;
      update public.room_members set role = 'host' where room_id = p_room and user_id = heir;
    end if;
  end if;
end;
$$;

create function public.kick_member(p_room uuid, p_user uuid)
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  if not public.is_room_host(p_room) then raise exception 'HOST_ONLY'; end if;
  if p_user = auth.uid() then raise exception 'CANNOT_KICK_SELF'; end if;
  delete from public.room_members where room_id = p_room and user_id = p_user;
  if found then
    insert into public.room_events (room_id, user_id, kind, payload) values (p_room, auth.uid(), 'kick', jsonb_build_object('user', p_user));
  end if;
end;
$$;

-- ── RPC: play ─────────────────────────────────────────────────────────────
-- Input: evidence → ["d09","d10"] · line → "d16:007" · choice → [2]
create function public.submit_answer(p_room uuid, p_question text, p_input jsonb)
returns jsonb
language plpgsql
security definer
set search_path = ''
as $$
declare
  uid uuid := auth.uid();
  rm public.rooms;
  q public.case_questions;
  cur text;
  ok boolean;
  inp jsonb := coalesce(p_input, '[]'::jsonb);
begin
  if not public.is_room_member(p_room) then raise exception 'NOT_MEMBER'; end if;
  select * into rm from public.rooms where id = p_room for update;  -- one submission at a time per room
  if rm.status = 'finished' then return jsonb_build_object('ok', false, 'error', 'FINISHED'); end if;

  select cq.question_id into cur
    from public.case_questions cq
    join public.room_progress p on p.room_id = p_room and p.question_id = cq.question_id
    where cq.case_id = rm.case_id and not p.solved
    order by cq.ord
    limit 1;
  if cur is distinct from p_question then return jsonb_build_object('ok', false, 'error', 'NOT_CURRENT'); end if;
  select * into q from public.case_questions where case_id = rm.case_id and question_id = p_question;

  -- (type checks are separate IFs: SQL does not promise to short-circuit AND)
  ok := false;
  if q.type = 'line' then
    if jsonb_typeof(inp) = 'string' then
      ok := exists (select 1 from jsonb_array_elements_text(q.answer) a where a = inp #>> '{}');
    end if;
  elsif q.type = 'choice' and not q.has_options then
    ok := true;
  elsif jsonb_typeof(inp) = 'array' then
    if q.type = 'evidence' then
      ok := (select coalesce(array_agg(distinct v order by v), '{}') from jsonb_array_elements_text(inp) v)
          = (select coalesce(array_agg(distinct v order by v), '{}') from jsonb_array_elements_text(q.answer) v);
    else
      ok := (select coalesce(array_agg(distinct v::int order by v::int), '{}') from jsonb_array_elements_text(inp) v where v ~ '^[0-9]{1,2}$')
          = (select coalesce(array_agg(distinct v::int order by v::int), '{}') from jsonb_array_elements_text(q.answer) v where v ~ '^[0-9]{1,2}$');
    end if;
  end if;

  update public.room_progress
    set tries = tries + 1,
        solved = ok,
        solved_by = case when ok then uid end,
        solved_at = case when ok then now() end
    where room_id = p_room and question_id = p_question;
  insert into public.room_events (room_id, user_id, kind, payload)
    values (p_room, uid, 'submit', jsonb_build_object('question', p_question, 'correct', ok));

  if ok then
    if rm.status = 'lobby' then update public.rooms set status = 'playing', started_at = now() where id = p_room; end if;
    if q.type = 'evidence' then
      update public.room_state set pins = '[]'::jsonb, updated_by = uid, updated_at = now() where room_id = p_room;
    end if;
    if not exists (select 1 from public.room_progress p where p.room_id = p_room and not p.solved) then
      update public.rooms set status = 'finished', finished_at = now(), join_code = null where id = p_room;
      insert into public.room_events (room_id, user_id, kind) values (p_room, uid, 'finish');
    end if;
  end if;
  return jsonb_build_object('ok', true, 'correct', ok);
end;
$$;

create function public.use_hint(p_room uuid, p_question text)
returns int
language plpgsql
security definer
set search_path = ''
as $$
declare
  n int;
begin
  if not public.is_room_member(p_room) then raise exception 'NOT_MEMBER'; end if;
  update public.room_progress p
    set hints = least(p.hints + 1, (select cq.hint_count from public.case_questions cq join public.rooms r on r.case_id = cq.case_id
                                    where r.id = p_room and cq.question_id = p_question))
    where p.room_id = p_room and p.question_id = p_question
    returning p.hints into n;
  insert into public.room_events (room_id, user_id, kind, payload)
    values (p_room, auth.uid(), 'hint', jsonb_build_object('question', p_question, 'hint', n));
  return n;
end;
$$;

-- functions: callable by signed-in users only; internal helpers by nobody
revoke execute on all functions in schema public from public, anon;
revoke execute on function public.new_join_code() from authenticated;
revoke execute on function public.handle_new_user() from authenticated;
grant execute on function public.is_room_member(uuid), public.is_room_host(uuid),
  public.create_room(text, text), public.refresh_join_code(uuid), public.join_room(text),
  public.start_room(uuid), public.leave_room(uuid), public.kick_member(uuid, uuid),
  public.submit_answer(uuid, text, jsonb), public.use_hint(uuid, text)
  to authenticated;

-- ── realtime ──────────────────────────────────────────────────────────────
alter table public.room_members replica identity full;  -- deletes carry room_id for filtered subscriptions
alter table public.room_notes replica identity full;
alter publication supabase_realtime add table
  public.rooms, public.room_members, public.room_state, public.room_progress, public.room_notes, public.room_events;

-- private channel "room:<uuid>" (presence): members only
create policy "room members receive on room channel" on realtime.messages
  for select to authenticated
  using (realtime.topic() like 'room:%' and public.is_room_member(nullif(split_part(realtime.topic(), ':', 2), '')::uuid));
create policy "room members send on room channel" on realtime.messages
  for insert to authenticated
  with check (realtime.topic() like 'room:%' and public.is_room_member(nullif(split_part(realtime.topic(), ':', 2), '')::uuid));
