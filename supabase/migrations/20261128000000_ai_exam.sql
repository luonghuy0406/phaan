-- Báo cáo kết luận trước kiểm sát viên (AI): trạng thái từng người chơi cho mỗi câu kết luận.
-- Chỉ Edge Function `conclude` (service role) đọc/ghi; trình duyệt không truy cập trực tiếp (state chứa tiến độ chấm).
create table public.exam_state (
  user_id uuid not null references auth.users (id) on delete cascade,
  case_id text not null check (case_id ~ '^[a-z0-9-]{1,60}$'),
  question_id text not null check (question_id ~ '^[a-z0-9-]{1,60}$'),
  state jsonb not null check (jsonb_typeof(state) = 'object' and pg_column_size(state) < 200000),
  updated_at timestamptz not null default now(),
  primary key (user_id, case_id, question_id)
);
alter table public.exam_state enable row level security;
revoke all on public.exam_state from anon, authenticated;
