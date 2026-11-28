// Đọc to một câu trả lời của nghi phạm (Gemini TTS).  POST { logId }  (Authorization: Bearer <access token>) → audio/wav
// Chỉ đọc câu có trong interrogation_log của chính người gọi, nên không dùng được như dịch vụ đọc chữ tuỳ ý.
// Giọng và cách đọc lấy từ case_ai.suspects[id].voice. Khoá: Edge Function secret GEMINI_API_KEY.
import { createClient } from 'npm:@supabase/supabase-js@2';

const MODELS = ['gemini-3.8-flash-lite-tts', 'gemini-3.8-flash-tts', 'gemini-3.1-flash-tts-preview'];
const DAILY_LINES_PER_CASE = Number(Deno.env.get('AI_DAILY_VOICE') || 150);
const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { ...CORS, 'Content-Type': 'application/json' } });
const admin = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!, { auth: { persistSession: false } });
const KEY = Deno.env.get('GEMINI_API_KEY');

/** Gemini returns 16-bit mono PCM (sometimes already a WAV): wrap raw PCM in a WAV header. */
function toWav(bytes: Uint8Array, mime: string): Uint8Array {
  if (bytes[0] === 0x52 && bytes[1] === 0x49 && bytes[2] === 0x46 && bytes[3] === 0x46) return bytes; // "RIFF"
  const rate = Number(/rate=(\d+)/i.exec(mime)?.[1] || 24000);
  const out = new Uint8Array(44 + bytes.length);
  const v = new DataView(out.buffer);
  const str = (o: number, s: string) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  str(0, 'RIFF'); v.setUint32(4, 36 + bytes.length, true); str(8, 'WAVE'); str(12, 'fmt ');
  v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true); v.setUint32(24, rate, true);
  v.setUint32(28, rate * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); str(36, 'data'); v.setUint32(40, bytes.length, true);
  out.set(bytes, 44);
  return out;
}

const b64 = (s: string) => Uint8Array.from(atob(s), (ch) => ch.charCodeAt(0));

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  if (req.method !== 'POST') return json({ error: 'METHOD' }, 405);
  if (!KEY) return json({ error: 'AI_UNAVAILABLE' }, 503);

  const token = (req.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '');
  const { data: auth } = token ? await admin.auth.getUser(token) : { data: { user: null } };
  const user = auth?.user;
  if (!user) return json({ error: 'AUTH_REQUIRED' }, 401);

  let body: { logId?: number };
  try { body = await req.json(); } catch { return json({ error: 'BAD_REQUEST' }, 400); }
  const logId = Number(body.logId);
  if (!Number.isSafeInteger(logId) || logId < 1) return json({ error: 'BAD_REQUEST' }, 400);

  const { data: line } = await admin.from('interrogation_log').select('case_id, suspect_id, reply').eq('id', logId).eq('user_id', user.id).maybeSingle();
  if (!line?.reply) return json({ error: 'NOT_FOUND' }, 404);

  const { data: left } = await admin.rpc('ai_take_turn', { p_user: user.id, p_case: `${line.case_id}#voice`, p_limit: DAILY_LINES_PER_CASE });
  if (typeof left !== 'number' || left < 0) return json({ error: 'AI_QUOTA' }, 429);

  const { data: row } = await admin.from('case_ai').select('data').eq('case_id', line.case_id).maybeSingle();
  const v = row?.data?.suspects?.[line.suspect_id]?.voice as { name: string; style: string } | undefined;
  // stage directions in brackets are acted, not read aloud
  const spoken = String(line.reply).replace(/\([^)]*\)/g, ' ').replace(/\s+/g, ' ').trim();
  if (!spoken) return json({ error: 'NOTHING_TO_SAY' }, 422);
  const prompt = `Đọc bằng giọng ${v?.style || 'người miền Tây Nam Bộ, tự nhiên'}, như đang bị hỏi cung: ${spoken}`;

  for (const model of MODELS) {
    try {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'x-goog-api-key': KEY },
        body: JSON.stringify({
          contents: [{ parts: [{ text: prompt }] }],
          generationConfig: { responseModalities: ['AUDIO'], speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: v?.name || 'Charon' } } } },
        }),
        signal: AbortSignal.timeout(25000),
      });
      if (!r.ok) { console.error(`${model}: HTTP ${r.status}`); continue; }
      const j = await r.json();
      const part = j?.candidates?.[0]?.content?.parts?.find((p: { inlineData?: unknown }) => p.inlineData);
      if (!part) { console.error(`${model}: no audio`); continue; }
      const wav = toWav(b64(part.inlineData.data), String(part.inlineData.mimeType || ''));
      return new Response(wav, { headers: { ...CORS, 'Content-Type': 'audio/wav', 'Cache-Control': 'private, max-age=86400' } });
    } catch (e) {
      console.error(`${model}: ${(e as Error).message}`);
    }
  }
  return json({ error: 'AI_UNAVAILABLE' }, 503);
});
