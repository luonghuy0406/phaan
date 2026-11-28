// Thẩm vấn nghi phạm bằng AI.  POST { caseId, suspectId, message?, evidence?, stage? }  (stage = vòng người chơi đang mở)  (Authorization: Bearer <access token>)
// Hồ sơ thẩm vấn (có lời giải) đọc từ bảng case_ai bằng service role; trạng thái và lịch sử lưu theo từng người chơi.
// Khoá AI: Edge Function secrets GEMINI_API_KEY, GROQ_API_KEY, OPENROUTER_API_KEY.
import { createClient } from 'npm:@supabase/supabase-js@2';
import {
  type CaseAi, type InterrogationState, type Turn,
  presentMany, sanitizeMessage, clampStage, lockedDocs, buildMessages, buildOfficerTurn, tidyReply, MAX_HISTORY_TURNS, MAX_EVIDENCE,
} from '../_shared/interrogation.ts';
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

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  if (req.method !== 'POST') return json({ error: 'METHOD' }, 405);

  // who is asking (the function checks the token itself)
  const token = (req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');
  const { data: auth } = token ? await admin.auth.getUser(token) : { data: { user: null } };
  const user = auth?.user;
  if (!user) return json({ error: 'AUTH_REQUIRED' }, 401);

  let body: { caseId?: string; suspectId?: string; message?: string; evidence?: string | string[] | null; stage?: number };
  try { body = await req.json(); } catch { return json({ error: 'BAD_REQUEST' }, 400); }
  const caseId = String(body.caseId || '');
  const suspectId = String(body.suspectId || '');
  const message = sanitizeMessage(body.message);
  const rawEv = body.evidence == null ? [] : Array.isArray(body.evidence) ? body.evidence : [body.evidence];
  const evidence = [...new Set(rawEv.map(String))].filter((d) => /^[a-z0-9-]{1,40}$/.test(d)).slice(0, MAX_EVIDENCE);
  if (!ID.test(caseId) || !ID.test(suspectId) || (!message && !evidence.length)) return json({ error: 'BAD_REQUEST' }, 400);

  const { data: row } = await admin.from('case_ai').select('data').eq('case_id', caseId).maybeSingle();
  const c = row?.data as CaseAi | undefined;
  if (!c?.suspects?.[suspectId]) return json({ error: 'CASE_NOT_SYNCED' }, 404);
  if (evidence.some((d) => !c.docTitles[d])) return json({ error: 'BAD_REQUEST' }, 400);
  // the suspect only talks about what this round has opened, and documents from later rounds cannot be shown yet
  const stage = clampStage(c, body.stage);
  if (lockedDocs(c, evidence, stage).length) return json({ error: 'DOC_LOCKED' }, 400);

  // per-player daily allowance protects the shared free-tier keys
  const { data: left, error: qErr } = await admin.rpc('ai_take_turn', { p_user: user.id, p_case: caseId, p_limit: DAILY_TURNS_PER_CASE });
  if (qErr) return json({ error: 'SERVER' }, 500);
  if ((left as number) < 0) return json({ error: 'AI_QUOTA' }, 429);

  const { data: st } = await admin.from('interrogation_state').select('presented, admitted, turns')
    .eq('user_id', user.id).eq('case_id', caseId).eq('suspect_id', suspectId).maybeSingle();
  const before: InterrogationState = { presented: st?.presented ?? [], admitted: st?.admitted ?? [], turns: st?.turns ?? 0 };
  const { state, broke } = presentMany(c.suspects[suspectId], before, evidence);

  const { data: logs } = await admin.from('interrogation_log').select('question, evidence, reply')
    .eq('user_id', user.id).eq('case_id', caseId).eq('suspect_id', suspectId)
    .order('id', { ascending: false }).limit(MAX_HISTORY_TURNS / 2);
  const history: Turn[] = (logs ?? []).reverse().flatMap((l) => [
    { role: 'officer' as const, text: `${l.evidence ? `[Đưa ra: ${String(l.evidence).split(',').map((d) => c.docTitles[d] || d).join(', ')}] ` : ''}${l.question || ''}`.trim() },
    { role: 'suspect' as const, text: l.reply },
  ]);

  let reply: string;
  let model = '';
  try {
    const r = await chat(buildMessages(c, suspectId, state, history, buildOfficerTurn(c, suspectId, message, evidence, broke), stage), keys);
    reply = tidyReply(r.text, c.suspects[suspectId].name);
    model = r.model;
  } catch (e) {
    if (e instanceof AllModelsFailed) console.error(e.message);
    return json({ error: 'AI_UNAVAILABLE' }, 503);
  }

  state.turns = before.turns + 1;
  await admin.from('interrogation_state').upsert({
    user_id: user.id, case_id: caseId, suspect_id: suspectId,
    presented: state.presented, admitted: state.admitted, turns: state.turns, updated_at: new Date().toISOString(),
  });
  const { data: logged } = await admin.from('interrogation_log').insert({
    user_id: user.id, case_id: caseId, suspect_id: suspectId, question: message, evidence: evidence.join(',') || null, reply,
    admitted: broke.map((l) => l.id), model,
  }).select('id').single();

  const lies = c.suspects[suspectId].lies;
  return json({
    id: logged?.id ?? null,
    reply,
    broke: broke.map((l) => ({ id: l.id, admission: l.admission })),
    admitted: lies.filter((l) => state.admitted.includes(l.id)).map((l) => ({ id: l.id, admission: l.admission })),
    presented: state.presented,
    remaining: left,
  });
});
