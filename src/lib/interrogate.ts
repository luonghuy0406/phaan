// Thẩm vấn nghi phạm bằng AI: gọi Edge Function `interrogate` (Supabase). Hồ sơ thẩm vấn và lời giải chỉ nằm trên máy chủ;
// trình duyệt chỉ gửi câu hỏi và mã tài liệu đưa ra, rồi đọc lại lịch sử của chính người chơi.
import { supabase, supabaseReady } from './supabase';

export const interrogationEnabled = () => supabaseReady && import.meta.env.VITE_AI_INTERROGATION !== 'off';

export interface Exchange { id: number; question: string; evidence: string | null; reply: string; admitted: string[] }
export interface Admission { id: string; admission: string }
export interface AskResult { id: number | null; reply: string; broke: Admission[]; admitted: Admission[]; presented: string[]; remaining: number }

const ERRORS: Record<string, string> = {
  AUTH_REQUIRED: 'Cần đăng nhập để thẩm vấn nghi phạm.',
  AI_QUOTA: 'Hôm nay bạn đã hỏi hết lượt cho hồ sơ này. Mai quay lại nhé.',
  AI_UNAVAILABLE: 'Nghi phạm chưa trả lời được (máy chủ AI đang bận). Thử lại sau ít phút.',
  CASE_NOT_SYNCED: 'Hồ sơ này chưa mở thẩm vấn trên máy chủ.',
  BAD_REQUEST: 'Câu hỏi không hợp lệ.',
  DOC_LOCKED: 'Tài liệu này chưa mở ở vòng hiện tại.',
};

async function errorCode(e: unknown): Promise<string> {
  // FunctionsHttpError carries the Response in `context`
  const res = (e as { context?: Response })?.context;
  if (res && typeof res.json === 'function') {
    try { const j = await res.clone().json(); if (j?.error) return String(j.error); } catch { /* not json */ }
  }
  return /fetch|network/i.test(String((e as Error)?.message)) ? 'NETWORK' : 'SERVER';
}

/** `stage` = the latest round open on the board: the suspect only talks about what that round has revealed. */
export async function askSuspect(caseId: string, suspectId: string, message: string, evidence: string[], stage: number): Promise<AskResult> {
  const { data, error } = await supabase.functions.invoke('interrogate', { body: { caseId, suspectId, message, evidence, stage } });
  if (error) {
    const code = await errorCode(error);
    throw new Error(ERRORS[code] || (code === 'NETWORK' ? 'Mất kết nối. Kiểm tra mạng rồi thử lại.' : 'Có lỗi khi thẩm vấn. Thử lại sau.'));
  }
  return data as AskResult;
}

/** The player's own past exchanges with one suspect (RLS: only their rows). */
export async function loadInterrogation(caseId: string, suspectId: string): Promise<{ log: Exchange[]; presented: string[] }> {
  const [log, st] = await Promise.all([
    supabase.from('interrogation_log').select('id, question, evidence, reply, admitted').eq('case_id', caseId).eq('suspect_id', suspectId).order('id').limit(200),
    supabase.from('interrogation_state').select('presented').eq('case_id', caseId).eq('suspect_id', suspectId).maybeSingle(),
  ]);
  return { log: (log.data as Exchange[] | null) ?? [], presented: (st.data?.presented as string[] | undefined) ?? [] };
}

export async function resetInterrogation(caseId: string) {
  if (!interrogationEnabled()) return;
  await supabase.rpc('reset_interrogation', { p_case: caseId });
}

const AUTO_KEY = 'hsm:itg-voice';
export const autoVoice = () => { try { return localStorage.getItem(AUTO_KEY) !== 'off'; } catch { return true; } };
export const setAutoVoice = (on: boolean) => { try { localStorage.setItem(AUTO_KEY, on ? 'on' : 'off'); } catch { /* private mode */ } };
