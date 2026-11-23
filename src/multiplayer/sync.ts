// Bridges the board store and the room: the conclusions (answers, pins, chosen lines, picks, hints) are shared
// and decided by the server; papers, ink, sticky notes and the personal notebook stay on each player's own desk.
import { useEffect } from 'react';
import type { CaseData } from '../lib/types';
import { check, normalizeLine } from '../lib/checks.js';
import { supabase } from '../lib/supabase';
import { currentQ, type BoardState, type BoardStore, type QState } from '../board/store';
import { useUi } from '../board/ui';
import { useRoom, memberName, submitAnswer, useHintRemote, type RoomEvent } from './room';

type Actions = Pick<BoardState, 'togglePin' | 'setPin' | 'setLine' | 'setPick' | 'useHint' | 'submit'>;

export function useRoomBoardSync(store: BoardStore, c: CaseData, roomId: string | undefined, me: string | undefined) {
  // remote → board
  useEffect(() => {
    if (!roomId || !me) return undefined;
    let first = true;
    const apply = () => {
      const rs = useRoom.getState();
      if (!rs.room) return;
      const s = store.getState();
      const shared = rs.shared;
      const takeShared = Boolean(shared) && (first || shared!.updated_by !== me);
      const q: Record<string, QState> = {};
      c.questions.forEach((x) => {
        const cur = s.q[x.id] || { solved: false, hints: 0, tries: 0, line: '', pick: [] };
        const p = rs.progress[x.id];
        q[x.id] = {
          solved: Boolean(p?.solved),
          hints: p?.hints ?? 0,
          tries: p?.tries ?? 0,
          line: takeShared ? normalizeLine(shared!.lines?.[x.id] ?? '') : cur.line,
          pick: takeShared ? (shared!.picks?.[x.id] ?? []) : cur.pick,
        };
      });
      store.setState({ q, ...(takeShared ? { pins: (shared!.pins || []).map((p) => (typeof p === 'string' ? p : null)) } : {}) });
      first = false;
    };
    apply();
    return useRoom.subscribe((rs, prev) => {
      if (rs.progress !== prev.progress || rs.shared !== prev.shared || rs.room !== prev.room) apply();
    });
  }, [store, c, roomId, me]);

  // board actions → room
  useEffect(() => {
    if (!roomId || !me) return undefined;
    const s0 = store.getState();
    const original: Actions = { togglePin: s0.togglePin, setPin: s0.setPin, setLine: s0.setLine, setPick: s0.setPick, useHint: s0.useHint, submit: s0.submit };
    let timer = 0;
    const pushShared = () => {
      window.clearTimeout(timer);
      timer = window.setTimeout(() => {
        const s = store.getState();
        const lines: Record<string, string> = {};
        const picks: Record<string, number[]> = {};
        c.questions.forEach((x) => {
          if (s.q[x.id]?.line) lines[x.id] = s.q[x.id].line;
          if (s.q[x.id]?.pick?.length) picks[x.id] = s.q[x.id].pick;
        });
        void supabase.from('room_state')
          .update({ pins: s.pins.slice(0, 6), lines, picks, updated_by: me, updated_at: new Date().toISOString() })
          .eq('room_id', roomId);
      }, 200);
    };
    const log = (kind: 'pin' | 'line' | 'pick', payload: Record<string, unknown>) => {
      void supabase.from('room_events').insert({ room_id: roomId, user_id: me, kind, payload });
    };
    store.setState({
      togglePin: (doc, need) => {
        const r = original.togglePin(doc, need);
        if (r !== 'full') { pushShared(); log('pin', { doc, on: r === 'pinned' }); }
        return r;
      },
      setPin: (slot, doc, need) => {
        original.setPin(slot, doc, need);
        pushShared();
        if (doc) log('pin', { doc, on: true });
      },
      setLine: (qid, ref) => {
        original.setLine(qid, ref);
        pushShared();
        log('line', { question: qid, line: normalizeLine(ref) });
      },
      setPick: (qid, pick) => { original.setPick(qid, pick); pushShared(); },
      useHint: (qid) => {
        original.useHint(qid); // shows at once; the server count arrives right after
        void useHintRemote(roomId, qid).catch(() => {});
      },
      submit: (qid) => {
        const s = store.getState();
        const q = c.questions.find((x) => x.id === qid);
        if (!q || q !== currentQ(c, s)) return null;
        const st = s.q[qid];
        const input = q.type === 'evidence' ? s.pins.filter((p): p is string => Boolean(p)) : q.type === 'line' ? st.line : st.pick;
        const result = check(q, input);
        store.setState({ feedback: { ...s.feedback, [qid]: result } });
        if (result.status === 'incomplete') return result;
        // the server records the attempt and, if right, unseals the next round for everyone
        submitAnswer(roomId, qid, input).then((r) => {
          if (!r.ok && r.error) useUi.getState().showToast(r.error === 'NOT_CURRENT' ? 'Đồng đội vừa giải câu này rồi.' : 'Vụ án đã được phá.');
          else if (r.correct !== (result.status === 'correct')) {
            useUi.getState().showToast('Đáp án trên máy chủ khác với bản hồ sơ này. Chủ dự án cần chạy npm run sync-cases.');
          }
        }).catch((e) => useUi.getState().showToast(String(e.message || e)));
        return result;
      },
    });
    return () => { window.clearTimeout(timer); store.setState(original); };
  }, [store, c, roomId, me]);

  // teammates' actions → toasts
  useEffect(() => {
    if (!roomId || !me) return undefined;
    const label = (id: unknown) => {
      const d = c.documents.find((x) => x.id === id);
      return d ? `Tài liệu ${String(d.no ?? 0).padStart(2, '0')}` : 'một tài liệu';
    };
    const qNo = (id: unknown) => c.questions.findIndex((x) => x.id === id) + 1;
    const text = (e: RoomEvent): string | null => {
      const who = memberName(e.user_id);
      const p = e.payload || {};
      switch (e.kind) {
        case 'join': return `${who} đã vào phòng.`;
        case 'leave': return `${who} đã rời phòng.`;
        case 'pin': return p.on ? `${who} ghim ${label(p.doc)} làm bằng chứng.` : null;
        case 'line': return `${who} chọn dòng ${String(p.line || '').split(':')[1] || ''} trong ${label(String(p.line || '').split(':')[0])}.`;
        case 'hint': return `${who} mở gợi ý ${p.hint ?? ''} của câu ${qNo(p.question)}.`;
        case 'submit': return p.correct ? `${who} đã giải câu ${qNo(p.question)}!` : `${who} gửi kết luận câu ${qNo(p.question)}: chưa đúng.`;
        case 'finish': return 'Cả nhóm đã phá được vụ án!';
        default: return null;
      }
    };
    return useRoom.subscribe((rs, prev) => {
      const e = rs.lastEvent;
      if (!e || e === prev.lastEvent || e.user_id === me) return;
      const t = text(e);
      if (t) useUi.getState().showToast(t);
    });
  }, [c, roomId, me]);
}
