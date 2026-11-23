import { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { Footer, Nav } from '../components/site';
import { useAuth, sendLoginCode, verifyLoginCode, saveDisplayName, signOut } from '../lib/auth';
import { errorText, supabaseReady } from '../lib/supabase';
import { SITE } from '../lib/config';

const safeNext = (n: string | null) => (n && n.startsWith('/') && !n.startsWith('//') ? n : '/');

export default function LoginPage() {
  const [params] = useSearchParams();
  const next = safeNext(params.get('next'));
  const navigate = useNavigate();
  const { ready, session, profile } = useAuth();
  const [step, setStep] = useState<'email' | 'code'>('email');
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState<{ kind: 'error' | 'info'; text: string } | null>(null);
  const [cameFromLogin, setCameFromLogin] = useState(params.get('tu-email') === '1');

  useEffect(() => { document.title = `Đăng nhập – ${SITE.name}`; }, []);
  // Signed in here (code or magic link in this browser): continue where the player was going.
  useEffect(() => { if (session && cameFromLogin) navigate(next, { replace: true }); }, [session, cameFromLogin, next, navigate]);
  useEffect(() => { if (profile) setName(profile.display_name); }, [profile]);

  const send = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!/^\S+@\S+\.\S+$/.test(email)) { setMsg({ kind: 'error', text: 'Email chưa đúng.' }); return; }
    setBusy(true); setMsg(null);
    try {
      await sendLoginCode(email.trim(), name.trim(), next);
      setStep('code');
      setMsg({ kind: 'info', text: `Đã gửi mã đăng nhập tới ${email.trim()}. Nhập mã, hoặc bấm liên kết trong email.` });
    } catch (err) { setMsg({ kind: 'error', text: errorText(err) }); }
    setBusy(false);
  };

  const verify = async (e?: React.FormEvent) => {
    e?.preventDefault();
    const token = code.replace(/\D/g, '');
    if (token.length < 6) return;
    setBusy(true); setMsg(null);
    try {
      await verifyLoginCode(email.trim(), token);
      setCameFromLogin(true);
    } catch (err) { setMsg({ kind: 'error', text: errorText(err) }); }
    setBusy(false);
  };

  if (!supabaseReady) {
    return <><Nav /><main className="wrap auth"><h1>Chưa cấu hình đăng nhập</h1><p>Thêm VITE_SUPABASE_URL và VITE_SUPABASE_PUBLISHABLE_KEY vào .env.local.</p></main></>;
  }

  return (
    <>
      <Nav />
      <main className="wrap auth">
        <div className="auth__card">
          {ready && session && !cameFromLogin ? (
            <>
              <p className="eyebrow">Tài khoản</p>
              <h1>Xin chào, {profile?.display_name || 'điều tra viên'}</h1>
              <p className="auth__muted">{session.user.email}</p>
              <form className="auth__form" onSubmit={async (e) => { e.preventDefault(); setBusy(true); try { await saveDisplayName(name); setMsg({ kind: 'info', text: 'Đã lưu tên.' }); } catch (err) { setMsg({ kind: 'error', text: errorText(err) }); } setBusy(false); }}>
                <label className="field"><span>Tên hiển thị trong phòng chơi</span>
                  <input value={name} maxLength={40} onChange={(e) => setName(e.target.value)} />
                </label>
                <button className="btn btn--ghost" disabled={busy}>Lưu tên</button>
              </form>
              {msg && <p className={`auth__msg is-${msg.kind}`}>{msg.text}</p>}
              <div className="auth__actions">
                <Link className="btn btn--primary" to={next}>{next === '/' ? 'Về trang chủ' : 'Tiếp tục'}</Link>
                <Link className="btn btn--ghost" to="/tham-gia">Tham gia phòng</Link>
                <button className="btn btn--danger" type="button" onClick={() => signOut()}>Đăng xuất</button>
              </div>
            </>
          ) : step === 'email' ? (
            <form className="auth__form" onSubmit={send}>
              <p className="eyebrow">Đăng nhập</p>
              <h1>Vào phòng điều tra</h1>
              <p className="auth__muted">Chơi nhóm cần đăng nhập để đồng đội nhận ra bạn. Không cần mật khẩu: chúng tôi gửi mã một lần qua email.</p>
              <label className="field"><span>Email</span>
                <input type="email" inputMode="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="ban@email.com" />
              </label>
              <label className="field"><span>Tên hiển thị (tuỳ chọn)</span>
                <input value={name} maxLength={40} autoComplete="nickname" onChange={(e) => setName(e.target.value)} placeholder="Thám tử Lan" />
              </label>
              {msg && <p className={`auth__msg is-${msg.kind}`}>{msg.text}</p>}
              <button className="btn btn--primary" disabled={busy}>{busy ? 'Đang gửi…' : 'Gửi mã đăng nhập'}</button>
            </form>
          ) : (
            <form className="auth__form" onSubmit={verify}>
              <p className="eyebrow">Đăng nhập</p>
              <h1>Nhập mã trong email</h1>
              {msg && <p className={`auth__msg is-${msg.kind}`}>{msg.text}</p>}
              <label className="field"><span>Mã đăng nhập</span>
                <input className="auth__code" inputMode="numeric" autoComplete="one-time-code" autoFocus maxLength={10}
                  value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))} placeholder="••••••" />
              </label>
              <button className="btn btn--primary" disabled={busy || code.length < 6}>{busy ? 'Đang kiểm tra…' : 'Đăng nhập'}</button>
              <div className="auth__row">
                <button type="button" className="link-btn" onClick={() => { setStep('email'); setCode(''); setMsg(null); }}>Đổi email</button>
                <button type="button" className="link-btn" disabled={busy} onClick={() => send()}>Gửi lại mã</button>
              </div>
            </form>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
