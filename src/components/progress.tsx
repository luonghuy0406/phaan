import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import { listMyRooms, listSavedCases, type MyRoom, type SavedCase } from '../lib/account';
import { loadCatalog, caseBase, caseNo } from '../lib/data';
import type { CaseSummary } from '../lib/types';

export interface Activity { saved: SavedCase[]; rooms: MyRoom[]; catalog: CaseSummary[]; loading: boolean; reload: () => void }

// Saved solo progress + rooms the player belongs to (signed-in players only).
export function useMyActivity(): Activity {
  const me = useAuth((s) => s.session?.user.id);
  const [state, setState] = useState<Omit<Activity, 'reload'>>({ saved: [], rooms: [], catalog: [], loading: true });
  const [tick, setTick] = useState(0);
  const reload = useCallback(() => setTick((t) => t + 1), []);
  useEffect(() => {
    if (!me) { setState({ saved: [], rooms: [], catalog: [], loading: false }); return undefined; }
    let live = true;
    Promise.all([listSavedCases(), listMyRooms(), loadCatalog().catch(() => [])])
      .then(([saved, rooms, catalog]) => { if (live) setState({ saved, rooms, catalog, loading: false }); })
      .catch(() => { if (live) setState((s) => ({ ...s, loading: false })); });
    return () => { live = false; };
  }, [me, tick]);
  return { ...state, reload };
}

export const roomLink = (r: MyRoom) => (r.status === 'lobby' ? `/phong/${r.id}` : `/phong/${r.id}/choi`);
export const ROOM_STATUS: Record<MyRoom['status'], string> = { lobby: 'Đang chờ', playing: 'Đang điều tra', finished: 'Đã phá án' };

const ago = (iso: string) => {
  const m = Math.round((Date.now() - new Date(iso).getTime()) / 60000);
  if (m < 1) return 'vừa xong';
  if (m < 60) return `${m} phút trước`;
  if (m < 60 * 24) return `${Math.round(m / 60)} giờ trước`;
  return new Date(iso).toLocaleDateString('vi-VN');
};

function Thumb({ entry }: { entry?: CaseSummary }) {
  return entry?.cover
    ? <img className="cont__thumb" src={caseBase(entry.id) + entry.cover} alt="" loading="lazy" />
    : <span className="cont__thumb cont__thumb--blank" />;
}

function Bar({ solved, total }: { solved: number; total: number }) {
  return <span className="cont__bar" aria-label={`${solved}/${total} trọng điểm`}><i style={{ width: `${total ? (solved / total) * 100 : 0}%` }} /></span>;
}

export function SavedCaseItem({ s, entry }: { s: SavedCase; entry?: CaseSummary }) {
  const done = s.total > 0 && s.solved >= s.total;
  return (
    <li className="cont__item">
      <Thumb entry={entry} />
      <div className="cont__body">
        <span className="cont__meta">{entry ? caseNo(entry) : s.case_id} · Chơi một mình · {ago(s.saved_at)}</span>
        <strong>{entry?.title || s.case_id}</strong>
        <span className="cont__progress"><Bar solved={s.solved} total={s.total} />{s.solved}/{s.total} trọng điểm{done ? ' · đã phá án' : ''}</span>
      </div>
      <Link className="btn btn--small btn--ghost" to={`/choi/${s.case_id}`}>{done ? 'Xem lại' : 'Tiếp tục'}</Link>
    </li>
  );
}

export function RoomItem({ r, entry, actions }: { r: MyRoom; entry?: CaseSummary; actions?: React.ReactNode }) {
  return (
    <li className="cont__item">
      <Thumb entry={entry} />
      <div className="cont__body">
        <span className="cont__meta">
          Phòng {r.role === 'host' ? 'của bạn' : 'đã tham gia'} · {r.members} người · <span className={`cont__status cont__status--${r.status}`}>{ROOM_STATUS[r.status]}</span>
        </span>
        <strong>{entry?.title || r.case_id}</strong>
        <span className="cont__progress"><Bar solved={r.solved} total={r.total} />{r.solved}/{r.total} trọng điểm</span>
      </div>
      <div className="cont__actions">
        <Link className="btn btn--small btn--primary" to={roomLink(r)}>{r.status === 'finished' ? 'Xem lại' : 'Vào phòng'}</Link>
        {actions}
      </div>
    </li>
  );
}

// Home page strip: the few most recent unfinished things.
export function ContinueStrip() {
  const me = useAuth((s) => s.session?.user.id);
  const { saved, rooms, catalog, loading } = useMyActivity();
  if (!me || loading) return null;
  const openRooms = rooms.filter((r) => r.status !== 'finished').slice(0, 3);
  const openCases = saved.filter((s) => s.solved < s.total).slice(0, 3 - Math.min(3, openRooms.length));
  if (!openRooms.length && !openCases.length) return null;
  const find = (id: string) => catalog.find((c) => c.id === id);
  return (
    <section className="section cont">
      <div className="wrap">
        <div className="section__head">
          <div><p className="eyebrow">Của bạn</p><h2>Tiếp tục điều tra</h2></div>
          <Link className="link-btn" to="/tai-khoan">Xem tất cả</Link>
        </div>
        <ul className="cont__list">
          {openRooms.map((r) => <RoomItem key={r.id} r={r} entry={find(r.case_id)} />)}
          {openCases.map((s) => <SavedCaseItem key={s.case_id} s={s} entry={find(s.case_id)} />)}
        </ul>
      </div>
    </section>
  );
}
