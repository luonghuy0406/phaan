import { createClient } from '@supabase/supabase-js';

// Only the publishable key ever reaches the browser. The secret key stays in .env.local for tools/ scripts.
const url = import.meta.env.VITE_SUPABASE_URL as string | undefined;
const key = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY as string | undefined;

export const supabaseReady = Boolean(url && key);

export const supabase = createClient(url || 'http://localhost:54321', key || 'missing-key', {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
});

// Invite links / QR codes point here. Set VITE_PUBLIC_URL when the host plays on localhost but guests join from phones.
export const publicUrl = ((import.meta.env.VITE_PUBLIC_URL as string | undefined) || window.location.origin).replace(/\/$/, '');

const ERRORS: Record<string, string> = {
  AUTH_REQUIRED: 'Bạn cần đăng nhập.',
  CASE_NOT_SYNCED: 'Hồ sơ này chưa được nạp lên máy chủ (chạy npm run sync-cases).',
  TOO_MANY_ROOMS: 'Bạn đã tạo quá nhiều phòng hôm nay.',
  HOST_ONLY: 'Chỉ chủ phòng mới làm được việc này.',
  ROOM_FINISHED: 'Phòng này đã kết thúc.',
  INVALID_CODE: 'Mã không đúng hoặc đã hết hạn. Hỏi chủ phòng mã mới.',
  TOO_MANY_ATTEMPTS: 'Bạn nhập sai quá nhiều lần. Thử lại sau 10 phút.',
  ROOM_FULL: 'Phòng đã đủ người.',
  NOT_MEMBER: 'Bạn không còn ở trong phòng này.',
  NOT_CURRENT: 'Đồng đội vừa giải câu này rồi.',
  FINISHED: 'Vụ án đã được phá.',
  CANNOT_KICK_SELF: 'Không thể tự mời mình ra.',
};

export function errorText(e: unknown): string {
  const raw = typeof e === 'string' ? e : (e as { message?: string })?.message || '';
  const code = Object.keys(ERRORS).find((k) => raw.includes(k));
  if (code) return ERRORS[code];
  if (/rate limit/i.test(raw)) return 'Gửi email quá nhiều lần. Đợi một lúc rồi thử lại.';
  if (/expired|invalid/i.test(raw) && /otp|token/i.test(raw)) return 'Mã đăng nhập sai hoặc đã hết hạn.';
  if (/fetch|network/i.test(raw)) return 'Mất kết nối. Kiểm tra mạng rồi thử lại.';
  return raw || 'Có lỗi xảy ra.';
}
