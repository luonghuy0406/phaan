import { useEffect, useRef, type ReactNode } from 'react';
import { Link, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import { supabaseReady } from '../lib/supabase';

export function RequireAuth({ children }: { children: ReactNode }) {
  const { ready, session } = useAuth();
  const loc = useLocation();
  if (!supabaseReady) return <div className="board-loading">Chưa cấu hình Supabase (xem .env.example).</div>;
  if (!ready) return <div className="board-loading">Đang kiểm tra đăng nhập…</div>;
  if (!session) return <Navigate to={`/dang-nhap?next=${encodeURIComponent(loc.pathname + loc.search)}`} replace />;
  return <>{children}</>;
}

export function AccountChip() {
  const { session, profile } = useAuth();
  if (!supabaseReady) return null;
  if (!session) return <Link className="nav__account" to="/dang-nhap">Đăng nhập</Link>;
  const name = profile?.display_name || session.user.email || 'Tài khoản';
  return (
    <Link className="nav__account" to="/tai-khoan" title="Tài khoản">
      <span className="avatar" style={{ background: profile?.color || '#d9452f' }}>{name.slice(0, 1).toUpperCase()}</span>
      <span className="nav__account-name">{name}</span>
    </Link>
  );
}

export function Avatar({ name, color, online, size = 30 }: { name: string; color: string; online?: boolean; size?: number }) {
  return (
    <span className={`avatar${online === false ? ' is-away' : ''}`} style={{ background: color, width: size, height: size, fontSize: size * 0.45 }} title={name}>
      {name.slice(0, 1).toUpperCase()}
    </span>
  );
}

// Digit boxes for 6-digit codes: typing, deleting, pasting and iOS one-time-code autofill all work.
export function OtpInput({ value, onChange, length = 6, autoFocus, disabled }: { value: string; onChange: (v: string) => void; length?: number; autoFocus?: boolean; disabled?: boolean }) {
  const refs = useRef<(HTMLInputElement | null)[]>([]);
  useEffect(() => { if (autoFocus) refs.current[Math.min(value.length, length - 1)]?.focus(); }, [autoFocus]); // eslint-disable-line react-hooks/exhaustive-deps
  const set = (v: string) => onChange(v.replace(/\D/g, '').slice(0, length));
  return (
    <div className="otp" role="group" aria-label={`Mã ${length} số`}>
      {Array.from({ length }, (_, i) => (
        <input
          key={i}
          ref={(el) => { refs.current[i] = el; }}
          className="otp__box"
          inputMode="numeric"
          autoComplete={i === 0 ? 'one-time-code' : 'off'}
          maxLength={length}
          disabled={disabled}
          value={value[i] || ''}
          aria-label={`Chữ số ${i + 1}`}
          onChange={(e) => {
            const typed = e.target.value.replace(/\D/g, '');
            if (!typed) return;
            if (typed.length > 1) { set(value.slice(0, i) + typed); refs.current[Math.min(i + typed.length, length - 1)]?.focus(); return; }
            set(value.slice(0, i) + typed + value.slice(i + 1));
            refs.current[i + 1]?.focus();
          }}
          onKeyDown={(e) => {
            if (e.key === 'Backspace') {
              e.preventDefault();
              if (value[i]) set(value.slice(0, i) + value.slice(i + 1));
              else if (i > 0) { set(value.slice(0, i - 1) + value.slice(i)); refs.current[i - 1]?.focus(); }
            } else if (e.key === 'ArrowLeft') refs.current[i - 1]?.focus();
            else if (e.key === 'ArrowRight') refs.current[i + 1]?.focus();
          }}
          onPaste={(e) => { e.preventDefault(); set(e.clipboardData.getData('text')); }}
        />
      ))}
    </div>
  );
}
