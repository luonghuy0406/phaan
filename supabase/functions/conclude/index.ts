// Báo cáo kết luận trước kiểm sát viên (AI).  POST { caseId, questionId, answer?, reset? }  (Authorization: Bearer <access token>)
// Không có answer: trả lại buổi báo cáo đang dở (hoặc mở buổi mới). Có answer: chấm một câu trả lời.
// Đáp án (rubric) đọc từ case_ai.data.exams bằng service role; trình duyệt chỉ thấy lời của kiểm sát viên.
import { createClient } from 'npm:@supabase/supabase-js@2';
import { type Exam, type ExamState, startExam, sanitizeAnswer, buildJudgeMessages, parseJudgement, applyAnswer, publicLog } from '../_shared/exam.ts';
import { chat, AllModelsFailed } from '../_shared/llm.ts';

const DAILY_TURNS_PER_CASE = Number(Deno.env.get('AI_DAILY_TURNS') || 120);
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { ...CORS, 'Content-Type': 'application/json' } });
const ID = /^[a-z0-9-]{1,60}$/;

const admin = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!, { auth: { persistSession: false } });
const keys = { gemini: Deno.env.get('GEMINI_API_KEY'), groq: Deno.env.get('GROQ_API_KEY'), openrouter: Deno.env.get('OPENROUTER_API_KEY') };

const view = (exam: Exam, s: ExamState, extra: Record<string, unknown> = {}) => ({
  examiner: exam.examiner, log: publicLog(s.log), point: Math.min(s.point + 1, exam.points.length), total: exam.points.length,
  done: s.done, misses: s.misses, hints: s.hints, ...extra,
});

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  if (req.method !== 'POST') return json({ error: 'METHOD' }, 405);

  const token = (req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');
  const { data: auth } = token ? await admin.auth.getUser(token) : { data: { user: null } };
  const user = auth?.user;
  if (!user) return json({ error: 'AUTH_REQUIRED' }, 401);

  let body: { caseId?: string; questionId?: string; answer?: string; reset?: boolean };
  try { body = await req.json(); } catch { return json({ error: 'BAD_REQUEST' }, 400); }
  const caseId = String(body.caseId || '');
  const questionId = String(body.questionId || '');
  const answer = sanitizeAnswer(body.answer);
  if (!ID.test(caseId) || !ID.test(questionId)) return json({ error: 'BAD_REQUEST' }, 400);

  const { data: row } = await admin.from('case_ai').select('data').eq('case_id', caseId).maybeSingle();
  const exam = (row?.data as { exams?: Record<string, Exam> } | undefined)?.exams?.[questionId];
  const world = String((row?.data as { world?: string } | undefined)?.world || '');
  if (!exam?.points?.length) return json({ error: 'CASE_NOT_SYNCED' }, 404);

  const where = { user_id: user.id, case_id: caseId, question_id: questionId };
  const save = (s: ExamState) => admin.from('exam_state').upsert({ ...where, state: s, updated_at: new Date().toISOString() });
  const { data: st } = await admin.from('exam_state').select('state').match(where).maybeSingle();
  let state = (st?.state as ExamState | undefined) ?? null;
  if (!state || body.reset) { state = startExam(exam); await save(state); }
  if (!answer || state.done) return json(view(exam, state));

  const { data: left, error: qErr } = await admin.rpc('ai_take_turn', { p_user: user.id, p_case: caseId, p_limit: DAILY_TURNS_PER_CASE });
  if (qErr) return json({ error: 'SERVER' }, 500);
  if ((left as number) < 0) return json({ error: 'AI_QUOTA' }, 429);

  let judged = null;
  try {
    const r = await chat(buildJudgeMessages(exam, world, state, answer), keys, { temperature: 0.2, maxTokens: 600 });
    judged = parseJudgement(r.text);
    if (!judged) console.error(`exam: unparsable reply from ${r.model}`);
  } catch (e) {
    if (e instanceof AllModelsFailed) console.error(e.message);
  }
  if (!judged) return json({ error: 'AI_UNAVAILABLE' }, 503);

  const r = applyAnswer(exam, state, answer, judged);
  await save(r.state);
  return json(view(exam, r.state, { passed: r.passed, remaining: left }));
});
