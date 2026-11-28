import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Footer, Nav } from '../components/site';
import { Avatar } from '../components/auth';
import { useMyActivity, SavedCaseItem, RoomItem } from '../components/progress';
import { useAuth, saveDisplayName, signOut } from '../lib/auth';
import { errorText } from '../lib/supabase';
import { SITE } from '../lib/config';
import { leaveRoom } from '../multiplayer/room';

const PROVIDER_LABEL: Record<string, string> = { email: 'Email', google: 'Google', apple: 'Apple', facebook: 'Facebook', azure: 'Microsoft', github: 'GitHub', discord: 'Discord' };

export default function AccountPage() {
  const navigate = useNavigate();
  const { session, profile } = useAuth();
  const { saved, rooms, catalog, loading, reload } = useMyActivity();
  const [name, setName] = useState('');
  const [msg, setMsg] = useState<{ kind: 'error' | 'info'; text: string } | null>(null);
  const [busy, setBusy] = useState('');
  useEffect(() => { document.title = `Tài khoản – ${SITE.name}`; }, []);
  useEffect(() => { if (profile) setName(profile.display_name); }, [profile]);

  const find = (id: string) => catalog.find((c) => c.id === id);
  const providers = (session?.user.app_metadata?.providers as string[] | undefined) || [session?.user.app_metadata?.provider as string].filter(Boolean);
  const activeRooms = rooms.filter((r) => r.status !== 'finished');
  const pastRooms = rooms.filter((r) => r.status === 'finished');

  return (
    <>
      <Nav cta={{ to: '/#catalog', label: 'Kho hồ sơ' }} />
      <main className="wrap account">
        <section className="account__head">
          <Avatar name={profile?.display_name || session?.user.email || '?'} color={profile?.color || '#d9452f'} size={64} />
          <div>
            <p className="eyebrow">Tài khoản</p>
            <h1>{profile?.display_name || 'Điều tra viên'}</h1>
            <p className="auth__muted">{session?.user.is_anonymous ? 'Tài khoản ẩn danh, chỉ có trên trình duyệt này' : session?.user.email}{providers.length ? ` · đăng nhập bằng ${providers.map((p) => PROVIDER_LABEL[p] || p).join(', ')}` : ''}</p>
          </div>
        </section>

        <section className="account__grid">
          <div className="account__col">
            <h2>Phòng chơi nhóm</h2>
            {loading ? <p className="auth__muted">Đang tải…</p> : !rooms.length ? (
              <p className="auth__muted">Bạn chưa tham gia phòng nào. Mở một hồ sơ và chọn “Chơi nhóm”, hoặc <Link to="/tham-gia">nhập mã phòng</Link>.</p>
            ) : (
              <>
                {!!activeRooms.length && (
                  <ul className="cont__list">
                    {activeRooms.map((r) => (
                      <RoomItem key={r.id} r={r} entry={find(r.case_id)} actions={
                        <button type="button" className="link-btn" disabled={busy === r.id} onClick={async () => {
                          setBusy(r.id);
                          try { await leaveRoom(r.id); reload(); } catch (e) { setMsg({ kind: 'error', text: errorText(e) }); }
                          setBusy('');
                        }}>Rời phòng</button>
                      } />
                    ))}
                  </ul>
                )}
                {!!pastRooms.length && (
                  <details className="account__past">
                    <summary>Phòng đã phá án ({pastRooms.length})</summary>
                    <ul className="cont__list">{pastRooms.map((r) => <RoomItem key={r.id} r={r} entry={find(r.case_id)} />)}</ul>
                  </details>
                )}
              </>
            )}

            <h2>Hồ sơ chơi một mình</h2>
            {loading ? <p className="auth__muted">Đang tải…</p> : !saved.length ? (
              <p className="auth__muted">Chưa có tiến độ nào được lưu. Tiến độ tự lưu lên cloud khi bạn chơi trong lúc đã đăng nhập.</p>
            ) : (
              <ul className="cont__list">{saved.map((s) => <SavedCaseItem key={s.case_id} s={s} entry={find(s.case_id)} />)}</ul>
            )}
          </div>

          <aside className="account__side">
            <form className="auth__form" onSubmit={async (e) => {
              e.preventDefault(); setBusy('name');
              try { await saveDisplayName(name); setMsg({ kind: 'info', text: 'Đã lưu tên.' }); } catch (err) { setMsg({ kind: 'error', text: errorText(err) }); }
              setBusy('');
            }}>
              <label className="field"><span>Tên hiển thị trong phòng chơi</span>
                <input value={name} maxLength={40} onChange={(e) => setName(e.target.value)} />
              </label>
              <button className="btn btn--ghost" disabled={busy === 'name'}>Lưu tên</button>
            </form>
            {msg && <p className={`auth__msg is-${msg.kind}`}>{msg.text}</p>}
            <div className="auth__actions">
              <Link className="btn btn--ghost" to="/tham-gia">Tham gia phòng</Link>
              <button className="btn btn--danger" type="button" onClick={async () => { await signOut(); navigate('/'); }}>Đăng xuất</button>
            </div>
            <p className="auth__muted account__note">Tiến độ trên thiết bị này vẫn được giữ khi đăng xuất. Đăng nhập lại ở bất kỳ thiết bị nào để tiếp tục từ bản mới nhất.</p>
          </aside>
        </section>
      </main>
      <Footer />
    </>
  );
}
