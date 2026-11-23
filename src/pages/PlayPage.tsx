import { useEffect, useState } from 'react';
import { Link, Navigate, useParams } from 'react-router-dom';
import { loadCase, useAsync } from '../lib/data';
import { SITE } from '../lib/config';
import { getBoardStore, type BoardStore } from '../board/store';
import { Board } from '../board/Board';
import { useCloudReady } from '../lib/cloud';
import '../styles/board.css';

function useHydrated(store: BoardStore | null) {
  const [ok, setOk] = useState(() => Boolean(store?.persist.hasHydrated()));
  useEffect(() => {
    if (!store) return undefined;
    if (store.persist.hasHydrated()) { setOk(true); return undefined; }
    setOk(false);
    return store.persist.onFinishHydration(() => setOk(true));
  }, [store]);
  return ok;
}

export default function PlayPage() {
  const { id = '' } = useParams();
  const { data: c, error } = useAsync(() => loadCase(id), [id]);
  const store = c ? getBoardStore(c) : null;
  const hydrated = useHydrated(store);
  const cloudReady = useCloudReady(store, c ?? null, '', hydrated);

  useEffect(() => {
    document.body.classList.add('is-board');
    return () => document.body.classList.remove('is-board');
  }, []);
  useEffect(() => { if (c) document.title = `${c.title} – Bàn điều tra – ${SITE.name}`; }, [c]);

  if (error) {
    return (
      <div className="board-error">
        <h1>Không mở được hồ sơ</h1>
        <p>Hồ sơ không tồn tại hoặc đã bị gỡ.</p>
        <Link className="btn btn--primary" to="/#catalog">Về kho hồ sơ</Link>
      </div>
    );
  }
  if (c && c.status !== 'available') return <Navigate to={`/ho-so/${c.id}`} replace />;
  if (!c || !store || !hydrated || !cloudReady) return <div className="board-loading">Đang mở hồ sơ…</div>;
  return <Board key={c.id} c={c} store={store} />;
}
