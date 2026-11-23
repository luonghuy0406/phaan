import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import QRCode from 'qrcode';
import { Footer, Nav, Cover } from '../components/site';
import { Avatar } from '../components/auth';
import { useAuth } from '../lib/auth';
import { publicUrl } from '../lib/supabase';
import { loadCatalog, useAsync, caseNo } from '../lib/data';
import { SITE } from '../lib/config';
import { useRoom, useRoomConnection, refreshJoinCode, startRoom, leaveRoom, kickMember } from '../multiplayer/room';

function useCountdown(until: string | null) {
  const [now, setNow] = useState(Date.now());
  useEffect(() => { const t = setInterval(() => setNow(Date.now()), 1000); return () => clearInterval(t); }, []);
  if (!until) return null;
  const left = Math.max(0, Math.floor((new Date(until).getTime() - now) / 1000));
  return left;
}

function useQr(text: string | null) {
  const [src, setSrc] = useState('');
  useEffect(() => {
    if (!text) { setSrc(''); return; }
    QRCode.toString(text, { type: 'svg', margin: 1, errorCorrectionLevel: 'M', color: { dark: '#1a1712', light: '#f1e8d4' } })
      .then((svg) => setSrc(`data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`))
      .catch(() => setSrc(''));
  }, [text]);
  return src;
}

export default function LobbyPage() {
  const { roomId = '' } = useParams();
  const navigate = useNavigate();
  useRoomConnection(roomId);
  const me = useAuth((s) => s.session?.user.id);
  const { status, error, room, members, online } = useRoom();
  const { data: catalog } = useAsync(loadCatalog, []);
  const entry = catalog?.find((c) => c.id === room?.case_id);
  const isHost = room?.host_id === me;
  const left = useCountdown(room?.join_code_expires_at ?? null);
  const expired = left === 0 || !room?.join_code;
  const link = room?.join_code && !expired ? `${publicUrl}/tham-gia?ma=${room.join_code}` : null;
  const qr = useQr(link);
  const [busy, setBusy] = useState('');
  const [msg, setMsg] = useState('');

  useEffect(() => { document.title = `Phòng chơi – ${SITE.name}`; }, []);
  // everyone moves to the desk when the host starts
  useEffect(() => { if (room?.status === 'playing' || room?.status === 'finished') navigate(`/phong/${roomId}/choi`, { replace: true }); }, [room?.status, roomId, navigate]);

  const act = async (name: string, fn: () => Promise<unknown>) => {
    setBusy(name); setMsg('');
    try { await fn(); } catch (e) { setMsg((e as Error).message); }
    setBusy('');
  };

  if (status === 'error') {
    return (
      <><Nav /><main className="wrap auth"><div className="auth__card">
        <h1>Không vào được phòng</h1><p className="auth__muted">{error}</p>
        <div className="auth__actions"><Link className="btn btn--primary" to="/tham-gia">Nhập mã khác</Link><Link className="btn btn--ghost" to="/#catalog">Kho hồ sơ</Link></div>
      </div></main></>
    );
  }
  if (!room) return <div className="board-loading">Đang mở phòng…</div>;

  const mm = left != null ? `${String(Math.floor(left / 60)).padStart(2, '0')}:${String(left % 60).padStart(2, '0')}` : '';
  return (
    <>
      <Nav cta={{ to: '/#catalog', label: 'Kho hồ sơ' }} />
      <main className="wrap lobby">
        <section className="lobby__case">
          {entry && <div className="lobby__cover"><Cover entry={entry} /></div>}
          <div>
            <p className="eyebrow">Phòng điều tra · {entry ? caseNo(entry) : ''}</p>
            <h1>{entry?.title || room.case_id}</h1>
            <p className="auth__muted">{isHost ? 'Mời đồng đội bằng mã 6 số hoặc mã QR, rồi bấm bắt đầu khi mọi người đã vào.' : 'Chờ chủ phòng bắt đầu cuộc điều tra…'}</p>
          </div>
        </section>

        <section className="lobby__grid">
          <div className="lobby__invite">
            <p className="eyebrow">Mã mời</p>
            {expired ? (
              <p className="lobby__expired">Mã đã hết hạn.</p>
            ) : (
              <>
                <p className="lobby__code" aria-label={`Mã mời ${room.join_code?.split('').join(' ')}`}>{room.join_code?.slice(0, 3)} {room.join_code?.slice(3)}</p>
                <p className="auth__muted">Còn hiệu lực {mm}</p>
                {qr && <img className="lobby__qr" src={qr} alt="Mã QR để tham gia phòng" width={220} height={220} />}
                <div className="auth__row">
                  <button type="button" className="link-btn" onClick={() => { if (link) void navigator.clipboard?.writeText(link).then(() => setMsg('Đã sao chép liên kết mời.')); }}>Sao chép liên kết</button>
                  {typeof navigator.share === 'function' && link && (
                    <button type="button" className="link-btn" onClick={() => { void navigator.share({ title: SITE.name, text: `Vào phòng điều tra với mã ${room.join_code}`, url: link }).catch(() => {}); }}>Chia sẻ</button>
                  )}
                </div>
              </>
            )}
            {isHost && room.status !== 'finished' && (
              <button type="button" className="btn btn--ghost btn--small" disabled={busy === 'code'} onClick={() => act('code', () => refreshJoinCode(roomId))}>Tạo mã mới</button>
            )}
          </div>

          <div className="lobby__members">
            <p className="eyebrow">Thành viên ({members.length}/{room.max_players})</p>
            <ul>
              {members.map((m) => {
                const on = online.includes(m.user_id);
                return (
                  <li key={m.user_id}>
                    <Avatar name={m.name} color={m.color} online={on} size={38} />
                    <span className="lobby__name">{m.name}{m.user_id === me ? ' (bạn)' : ''}</span>
                    {m.role === 'host' && <span className="badge">Chủ phòng</span>}
                    <span className={`lobby__dot${on ? ' is-on' : ''}`}>{on ? 'Đang online' : 'Vắng'}</span>
                    {isHost && m.user_id !== me && (
                      <button type="button" className="link-btn" onClick={() => act('kick', () => kickMember(roomId, m.user_id))}>Mời ra</button>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>
        </section>

        {msg && <p className="auth__msg is-info">{msg}</p>}
        <div className="auth__actions">
          {isHost
            ? <button type="button" className="btn btn--primary" disabled={busy === 'start'} onClick={() => act('start', () => startRoom(roomId))}>Bắt đầu điều tra</button>
            : <span className="auth__muted">Bạn sẽ được chuyển vào bàn điều tra khi chủ phòng bắt đầu.</span>}
          <button type="button" className="btn btn--danger" disabled={busy === 'leave'} onClick={() => act('leave', async () => { await leaveRoom(roomId); navigate('/#catalog'); })}>Rời phòng</button>
        </div>
      </main>
      <Footer />
    </>
  );
}
