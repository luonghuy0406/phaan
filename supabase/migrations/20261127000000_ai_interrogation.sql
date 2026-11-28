-- Thẩm vấn nghi phạm bằng AI (Edge Function `interrogate`).
-- case_ai chứa hồ sơ thẩm vấn có lời giải: chỉ service role đọc được (như case_questions).

create table public.case_ai (
  case_id text primary key check (case_id ~ '^[a-z0-9-]{1,60}$'),
  data jsonb not null,
  updated_at timestamptz not null default now()
);

-- lượt hỏi mỗi người, mỗi hồ sơ, mỗi ngày (bảo vệ khoá AI miễn phí dùng chung)
create table public.ai_usage (
  user_id uuid not null references auth.users (id) on delete cascade,
  case_id text not null,
  day date not null default current_date,
  turns int not null default 0,
  primary key (user_id, case_id, day)
);

create table public.interrogation_state (
  user_id uuid not null references auth.users (id) on delete cascade,
  case_id text not null,
  suspect_id text not null,
  presented text[] not null default '{}',
  admitted text[] not null default '{}',
  turns int not null default 0,
  updated_at timestamptz not null default now(),
  primary key (user_id, case_id, suspect_id)
);

create table public.interrogation_log (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users (id) on delete cascade,
  case_id text not null,
  suspect_id text not null,
  question text not null default '',
  evidence text,
  reply text not null,
  admitted text[] not null default '{}',
  model text not null default '',
  created_at timestamptz not null default now()
);
create index interrogation_log_lookup on public.interrogation_log (user_id, case_id, suspect_id, id);

alter table public.case_ai enable row level security;            -- no policies: invisible to clients
alter table public.ai_usage enable row level security;           -- no policies
alter table public.interrogation_state enable row level security;
alter table public.interrogation_log enable row level security;

create policy "read own interrogation state" on public.interrogation_state
  for select to authenticated using (user_id = (select auth.uid()));
create policy "read own interrogation log" on public.interrogation_log
  for select to authenticated using (user_id = (select auth.uid()));

revoke all on public.case_ai, public.ai_usage, public.interrogation_state, public.interrogation_log from anon, authenticated;
grant select on public.interrogation_state, public.interrogation_log to authenticated;
grant all on public.case_ai, public.ai_usage, public.interrogation_state, public.interrogation_log to service_role;

-- take one turn of the daily allowance; returns turns left, or -1 when spent
create function public.ai_take_turn(p_user uuid, p_case text, p_limit int)
returns int
language plpgsql
security definer
set search_path = ''
as $$
declare
  used int;
begin
  insert into public.ai_usage as u (user_id, case_id, day, turns)
  values (p_user, p_case, current_date, 1)
  on conflict (user_id, case_id, day) do update set turns = u.turns + 1
    where u.turns < p_limit
  returning u.turns into used;
  if used is null then return -1; end if;
  return p_limit - used;
end;
$$;
revoke execute on function public.ai_take_turn(uuid, text, int) from public, anon, authenticated;
grant execute on function public.ai_take_turn(uuid, text, int) to service_role;

-- "Chơi lại từ đầu": the player clears their own interrogations of one case
create function public.reset_interrogation(p_case text)
returns void
language plpgsql
security definer
set search_path = ''
as $$
begin
  if auth.uid() is null then raise exception 'AUTH_REQUIRED'; end if;
  delete from public.interrogation_state where user_id = auth.uid() and case_id = p_case;
  delete from public.interrogation_log where user_id = auth.uid() and case_id = p_case;
end;
$$;
revoke execute on function public.reset_interrogation(text) from public, anon;
grant execute on function public.reset_interrogation(text) to authenticated;
