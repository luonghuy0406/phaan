import { useEffect, useState } from 'react';
import { Link, Navigate, useParams } from 'react-router-dom';
import { loadCase } from '../lib/data';
import { useAuth } from '../lib/auth';
import { SITE } from '../lib/config';
import type { CaseData } from '../lib/types';
import { getBoardStore, type BoardStore } from '../board/store';
import { Board } from '../board/Board';
import { useRoom, useRoomConnection } from '../multiplayer/room';
import '../styles/board.css';

export default function RoomPlayPage() {
  const { roomId = '' } = useParams();
  useRoomConnection(roomId);
  const me = useAuth((s) => s.session?.user.id);
  const status = useRoom((s) => s.status);
  const error = useRoom((s) => s.error);
  const room = useRoom((s) => s.room);
  const [c, setC] = useState<CaseData | null>(null);
  const [store, setStore] = useState<BoardStore | null>(null);
  const [hydrated, setHydrated] = useState(false);
  const caseId = room?.case_id;

  useEffect(() => {
    document.body.classList.add('is-board');
    return () => document.body.classList.remove('is-board');
  }, []);
  useEffect(() => {
    if (!caseId) return;
    let live = true;
    loadCase(caseId).then((data) => {
      if (!live) return;
      const s = getBoardStore(data, roomId); // personal desk (layout, ink, notes) per room
      setC(data);
      setStore(s);
      document.title = `${data.title} – Phòng chơi – ${SITE.name}`;
      if (s.persist.hasHydrated()) setHydrated(true);
      else s.persist.onFinishHydration(() => live && setHydrated(true));
    });
    return () => { live = false; };
  }, [caseId, roomId]);

  if (status === 'error') {
    return (
      <div className="board-error">
        <h1>Không vào được phòng</h1>
        <p>{error}</p>
        <Link className="btn btn--primary" to="/#catalog">Về kho hồ sơ</Link>
      </div>
    );
  }
  if (room?.status === 'lobby') return <Navigate to={`/phong/${roomId}`} replace />;
  if (!c || !store || !hydrated || !me || !room) return <div className="board-loading">Đang vào phòng điều tra…</div>;
  return <Board key={`${c.id}:${roomId}`} c={c} store={store} room={{ id: roomId, me }} />;
}
