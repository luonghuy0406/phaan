// Báo cáo kết luận trước kiểm sát viên (AI): gọi Edge Function `conclude`. Đáp án chỉ nằm trên máy chủ;
// trình duyệt gửi câu trả lời và nhận lời của kiểm sát viên cùng tiến độ.
import { supabase } from './supabase';
import { interrogationEnabled } from './interrogate';

export const examEnabled = interrogationEnabled;

export interface ExamLine { who: 'examiner' | 'officer' | 'hint'; text: string }
export interface ExamView {
  examiner: string;
  log: ExamLine[];
  /** 1-based point being asked */
  point: number;
  total: number;
  done: boolean;
  misses: number;
  hints: number;
  passed?: boolean;
  remaining?: number;
}

const ERRORS: Record<string, string> = {
  AUTH_REQUIRED: 'Cần đăng nhập để báo cáo với kiểm sát viên.',
  AI_QUOTA: 'Hôm nay bạn đã dùng hết lượt AI cho hồ sơ này. Có thể chọn bản kết luận bằng trắc nghiệm.',
  AI_UNAVAILABLE: 'Kiểm sát viên chưa nghe được (máy chủ AI đang bận). Thử lại sau ít phút, hoặc trả lời bằng trắc nghiệm.',
  CASE_NOT_SYNCED: 'Hồ sơ này chưa mở phần báo cáo trên máy chủ.',
  BAD_REQUEST: 'Câu trả lời không hợp lệ.',
};

async function call(body: Record<string, unknown>): Promise<ExamView> {
  const { data, error } = await supabase.functions.invoke('conclude', { body });
  if (error) {
    const res = (error as { context?: Response }).context;
    let code = /fetch|network/i.test(String(error.message)) ? 'NETWORK' : 'SERVER';
    if (res && typeof res.json === 'function') { try { const j = await res.clone().json(); if (j?.error) code = String(j.error); } catch { /* not json */ } }
    throw new Error(ERRORS[code] || (code === 'NETWORK' ? 'Mất kết nối. Kiểm tra mạng rồi thử lại.' : 'Có lỗi khi báo cáo. Thử lại sau.'));
  }
  return data as ExamView;
}

/** Open (or resume) the report; `reset` starts over. */
export const openExam = (caseId: string, questionId: string, reset = false) => call({ caseId, questionId, reset });
/** Give one answer to the current question of the examiner. */
export const answerExam = (caseId: string, questionId: string, answer: string) => call({ caseId, questionId, answer });
