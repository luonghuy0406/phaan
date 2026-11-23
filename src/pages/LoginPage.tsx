import { useEffect, useState } from 'react';
import { Navigate, useSearchParams } from 'react-router-dom';
import { Footer, Nav } from '../components/site';
import { useAuth, sendLoginCode, verifyLoginCode, enabledProviders, signInWithProvider, OAUTH_PROVIDERS, type OAuthProvider } from '../lib/auth';
import { errorText, supabaseReady } from '../lib/supabase';
import { SITE } from '../lib/config';

const safeNext = (n: string | null) => (n && n.startsWith('/') && !n.startsWith('//') ? n : '/');

function ProviderIcon({ id }: { id: OAuthProvider }) {
  const paths: Record<OAuthProvider, React.ReactNode> = {
    google: <><path fill="#EA4335" d="M12 10.2v3.9h5.5c-.2 1.3-1.6 3.8-5.5 3.8-3.3 0-6-2.7-6-6.1s2.7-6.1 6-6.1c1.9 0 3.2.8 3.9 1.5l2.7-2.6C16.9 3 14.7 2 12 2 6.5 2 2 6.5 2 12s4.5 10 10 10c5.8 0 9.6-4.1 9.6-9.8 0-.7-.1-1.2-.2-1.7H12z" /></>,
    apple: <path fill="currentColor" d="M16.4 12.6c0-2.6 2.1-3.8 2.2-3.9-1.2-1.8-3.1-2-3.7-2-1.6-.2-3.1.9-3.9.9-.8 0-2-.9-3.4-.9-1.7 0-3.3 1-4.2 2.6-1.8 3.1-.5 7.7 1.3 10.2.8 1.2 1.8 2.6 3.1 2.5 1.2 0 1.7-.8 3.2-.8s1.9.8 3.2.8c1.3 0 2.2-1.2 3-2.5.9-1.4 1.3-2.7 1.3-2.8-.1 0-2.6-1-2.6-4.1zM13.9 5c.7-.8 1.1-1.9 1-3-1 0-2.2.7-2.9 1.5-.6.7-1.2 1.8-1 2.9 1.1.1 2.2-.6 2.9-1.4z" />,
    facebook: <path fill="#1877F2" d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z" />,
    azure: <><path fill="#F25022" d="M3 3h8.5v8.5H3z" /><path fill="#7FBA00" d="M12.5 3H21v8.5h-8.5z" /><path fill="#00A4EF" d="M3 12.5h8.5V21H3z" /><path fill="#FFB900" d="M12.5 12.5H21V21h-8.5z" /></>,
    github: <path fill="currentColor" d="M12 2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.3-3.4-1.3-.4-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.6-1.4-2.2-.3-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.8 1a9.6 9.6 0 0 1 5 0c1.9-1.3 2.8-1 2.8-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.3 4.7-4.6 5 .4.3.7.9.7 1.9V21c0 .3.2.6.7.5A10 10 0 0 0 12 2z" />,
    discord: <path fill="#5865F2" d="M19.5 5.3A16.5 16.5 0 0 0 15.4 4l-.5 1a15.3 15.3 0 0 0-5.8 0L8.6 4a16.4 16.4 0 0 0-4.1 1.3C1.9 9.2 1.2 13 1.6 16.7a16.6 16.6 0 0 0 5 2.5l1.1-1.7c-.6-.2-1.2-.5-1.7-.9l.4-.3a11.8 11.8 0 0 0 11.2 0l.4.3c-.5.4-1.1.7-1.7.9l1.1 1.7a16.5 16.5 0 0 0 5-2.5c.5-4.3-.8-8.1-2.9-11.4zM8.7 14.4c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2zm6.6 0c-1 0-1.8-.9-1.8-2s.8-2 1.8-2 1.8.9 1.8 2-.8 2-1.8 2z" />,
  };
  return <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">{paths[id]}</svg>;
}

export default function LoginPage() {
  const [params] = useSearchParams();
  const next = safeNext(params.get('next'));
  const { ready, session } = useAuth();
  const [step, setStep] = useState<'email' | 'code'>('email');
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [busy, setBusy] = useState('');
  const [msg, setMsg] = useState<{ kind: 'error' | 'info'; text: string } | null>(null);
  const [providers, setProviders] = useState<OAuthProvider[]>([]);

  useEffect(() => { document.title = `Đăng nhập – ${SITE.name}`; }, []);
  useEffect(() => { if (supabaseReady) void enabledProviders().then(setProviders); }, []);
  // OAuth errors come back in the URL (e.g. the player cancelled on Google's page)
  useEffect(() => {
    const err = params.get('error_description') || new URLSearchParams(window.location.hash.slice(1)).get('error_description');
    if (err) setMsg({ kind: 'error', text: 'Đăng nhập chưa thành công. Hãy thử lại.' });
  }, [params]);

  if (ready && session) {
    // signed in (code, magic link or SSO): go where the player was heading, or to the account page
    return <Navigate to={next === '/' ? '/tai-khoan' : next} replace />;
  }

  const send = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!/^\S+@\S+\.\S+$/.test(email)) { setMsg({ kind: 'error', text: 'Email chưa đúng.' }); return; }
    setBusy('email'); setMsg(null);
    try {
      await sendLoginCode(email.trim(), name.trim(), next);
      setStep('code');
      setMsg({ kind: 'info', text: `Đã gửi mã đăng nhập tới ${email.trim()}. Nhập mã, hoặc bấm liên kết trong email.` });
    } catch (err) { setMsg({ kind: 'error', text: errorText(err) }); }
    setBusy('');
  };

  const verify = async (e?: React.FormEvent) => {
    e?.preventDefault();
    const token = code.replace(/\D/g, '');
    if (token.length < 6) return;
    setBusy('code'); setMsg(null);
    try { await verifyLoginCode(email.trim(), token); } catch (err) { setMsg({ kind: 'error', text: errorText(err) }); }
    setBusy('');
  };

  const sso = async (p: OAuthProvider) => {
    setBusy(p); setMsg(null);
    try { await signInWithProvider(p, next); } catch (err) { setMsg({ kind: 'error', text: errorText(err) }); setBusy(''); }
  };

  if (!supabaseReady) {
    return <><Nav /><main className="wrap auth"><h1>Chưa cấu hình đăng nhập</h1><p>Thêm VITE_SUPABASE_URL và VITE_SUPABASE_PUBLISHABLE_KEY vào .env.local.</p></main></>;
  }

  return (
    <>
      <Nav />
      <main className="wrap auth">
        <div className="auth__card">
          {step === 'email' ? (
            <div className="auth__form">
              <p className="eyebrow">Đăng nhập</p>
              <h1>Vào phòng điều tra</h1>
              <p className="auth__muted">Đăng nhập để chơi nhóm và lưu tiến độ lên cloud, mở lại trên iPad hay máy tính đều được.</p>
              {providers.length > 0 && (
                <>
                  <div className="sso">
                    {OAUTH_PROVIDERS.filter((p) => providers.includes(p.id)).map((p) => (
                      <button key={p.id} type="button" className={`btn sso__btn sso__btn--${p.id}`} disabled={Boolean(busy)} onClick={() => sso(p.id)}>
                        <ProviderIcon id={p.id} />
                        <span>{busy === p.id ? 'Đang chuyển…' : `Tiếp tục với ${p.label}`}</span>
                      </button>
                    ))}
                  </div>
                  <p className="auth__or"><span>hoặc dùng email</span></p>
                </>
              )}
              <form className="auth__form" onSubmit={send}>
                <label className="field"><span>Email</span>
                  <input type="email" inputMode="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="ban@email.com" />
                </label>
                <label className="field"><span>Tên hiển thị (tuỳ chọn)</span>
                  <input value={name} maxLength={40} autoComplete="nickname" onChange={(e) => setName(e.target.value)} placeholder="Thám tử Lan" />
                </label>
                {msg && <p className={`auth__msg is-${msg.kind}`}>{msg.text}</p>}
                <button className="btn btn--primary" disabled={Boolean(busy)}>{busy === 'email' ? 'Đang gửi…' : 'Gửi mã đăng nhập'}</button>
              </form>
            </div>
          ) : (
            <form className="auth__form" onSubmit={verify}>
              <p className="eyebrow">Đăng nhập</p>
              <h1>Nhập mã trong email</h1>
              {msg && <p className={`auth__msg is-${msg.kind}`}>{msg.text}</p>}
              <label className="field"><span>Mã đăng nhập</span>
                <input className="auth__code" inputMode="numeric" autoComplete="one-time-code" autoFocus maxLength={10}
                  value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))} placeholder="••••••" />
              </label>
              <button className="btn btn--primary" disabled={Boolean(busy) || code.length < 6}>{busy === 'code' ? 'Đang kiểm tra…' : 'Đăng nhập'}</button>
              <div className="auth__row">
                <button type="button" className="link-btn" onClick={() => { setStep('email'); setCode(''); setMsg(null); }}>Đổi email</button>
                <button type="button" className="link-btn" disabled={Boolean(busy)} onClick={() => send()}>Gửi lại mã</button>
              </div>
            </form>
          )}
        </div>
      </main>
      <Footer />
    </>
  );
}
