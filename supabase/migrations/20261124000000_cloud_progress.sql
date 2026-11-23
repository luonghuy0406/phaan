-- ════════════════════════════════════════════════════════════════════════════
-- Lưu tiến độ lên cloud + tên hiển thị cho tài khoản đăng nhập bằng Google/Apple/Facebook…
--
--   user_progress   một bản lưu cho mỗi (người chơi, hồ sơ, phạm vi)
--                   scope = ''        → chơi một mình
--                   scope = <room id> → bàn riêng của người đó trong một phòng
--                   fingerprint       → cấu trúc hồ sơ lúc lưu; khác cấu trúc hiện tại thì bỏ qua bản lưu
-- ════════════════════════════════════════════════════════════════════════════

create table public.user_progress (
  user_id uuid not null default auth.uid() references public.profiles (id) on delete cascade,
  case_id text not null check (case_id ~ '^[a-z0-9-]{1,60}$'),
  scope text not null default '' check (scope = '' or scope ~ '^[0-9a-f-]{36}$'),
  fingerprint text not null check (char_length(fingerprint) between 1 and 32),
  data jsonb not null check (jsonb_typeof(data) = 'object' and pg_column_size(data) < 3000000),
  solved int not null default 0 check (solved >= 0),
  total int not null default 0 check (total >= 0),
  saved_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, case_id, scope)
);
create index user_progress_recent_idx on public.user_progress (user_id, saved_at desc);

alter table public.user_progress enable row level security;

create policy "read own progress" on public.user_progress
  for select to authenticated using (user_id = (select auth.uid()));
create policy "insert own progress" on public.user_progress
  for insert to authenticated with check (user_id = (select auth.uid()));
create policy "update own progress" on public.user_progress
  for update to authenticated using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
create policy "delete own progress" on public.user_progress
  for delete to authenticated using (user_id = (select auth.uid()));

revoke all on public.user_progress from anon;
grant select, insert, update, delete on public.user_progress to authenticated;

-- OAuth providers put the name in full_name / name (email sign-ups use display_name)
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  insert into public.profiles (id, display_name, color)
  values (
    new.id,
    left(coalesce(
      nullif(trim(new.raw_user_meta_data ->> 'display_name'), ''),
      nullif(trim(new.raw_user_meta_data ->> 'full_name'), ''),
      nullif(trim(new.raw_user_meta_data ->> 'name'), ''),
      nullif(split_part(new.email, '@', 1), ''),
      'Điều tra viên'), 40),
    (array['#d9452f', '#1f4fa8', '#2f8f5b', '#b7791f', '#7b4bb7', '#c2417a'])[1 + floor(random() * 6)::int]
  )
  on conflict (id) do nothing;
  return new;
end;
$$;
revoke execute on function public.handle_new_user() from public, anon, authenticated;
