import { useEffect, useRef, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Footer, Nav } from '../components/site';
import { OtpInput } from '../components/auth';
import { joinRoom } from '../multiplayer/room';
import { SITE } from '../lib/config';

export default function JoinPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [code, setCode] = useState((params.get('ma') || '').replace(/\D/g, '').slice(0, 6));
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const tried = useRef('');

  useEffect(() => { document.title = `Tham gia phòng – ${SITE.name}`; }, []);

  const join = async (value = code) => {
    if (value.length !== 6 || busy) return;
    tried.current = value;
    setBusy(true); setError('');
    try {
      const roomId = await joinRoom(value);
      navigate(`/phong/${roomId}`, { replace: true });
    } catch (e) {
      setError((e as Error).message);
      setBusy(false);
    }
  };

  // QR links carry the code: join straight away; typing the 6th digit joins too
  useEffect(() => {
    if (code.length === 6 && tried.current !== code) void join(code);
  }, [code]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <>
      <Nav />
      <main className="wrap auth">
        <form className="auth__card auth__form" onSubmit={(e) => { e.preventDefault(); void join(); }}>
          <p className="eyebrow">Chơi nhóm</p>
          <h1>Tham gia phòng điều tra</h1>
          <p className="auth__muted">Nhập mã 6 số chủ phòng đưa cho bạn, hoặc quét mã QR trên màn hình của chủ phòng. Mã đổi sau mỗi 30 phút.</p>
          <OtpInput value={code} onChange={(v) => { setCode(v); setError(''); }} autoFocus disabled={busy} />
          {error && <p className="auth__msg is-error">{error}</p>}
          <button className="btn btn--primary" disabled={busy || code.length !== 6}>{busy ? 'Đang vào phòng…' : 'Vào phòng'}</button>
        </form>
      </main>
      <Footer />
    </>
  );
}
