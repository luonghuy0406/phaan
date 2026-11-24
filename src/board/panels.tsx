import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { useShallow } from 'zustand/react/shallow';
import { useBoard, useBoardState } from './context';
import { useUi } from './ui';
import { Icon } from './icons';
import { allSolved, currentQ, evidenceNeed, isSolved, stageOpen, type Entry } from './store';
import { Txt, Paras } from '../lib/text';
import { normalizeLine } from '../lib/checks.js';
import { pad2 } from '../lib/data';
import type { Question } from '../lib/types';
import { typeLabel } from './papers';
import { Avatar } from '../components/auth';
import { useRoom, memberName, addRoomNote, updateRoomNote, deleteRoomNote, type RoomEvent } from '../multiplayer/room';

export function SidePanel() {
  const { room } = useBoard();
  const panel = useUi((s) => s.panel);
  const set = useUi((s) => s.set);
  return (
    <aside className={`panel${panel ? ' is-open' : ''}`} aria-hidden={!panel} data-ui>
      <div className="panel__tabs" role="tablist">
        <button type="button" role="tab" aria-selected={panel === 'questions'} className={panel === 'questions' ? 'is-on' : ''} onClick={() => set({ panel: 'questions' })}>
          <Icon name="check" />Kết luận
        </button>
        <button type="button" role="tab" aria-selected={panel === 'notebook'} className={panel === 'notebook' ? 'is-on' : ''} onClick={() => set({ panel: 'notebook' })}>
          <Icon name="book" />Sổ tay
        </button>
        {room && (
          <button type="button" role="tab" aria-selected={panel === 'team'} className={panel === 'team' ? 'is-on' : ''} onClick={() => set({ panel: 'team' })}>
            <Icon name="link" />Nhóm
          </button>
        )}
        <button type="button" className="icon-btn panel__close" aria-label="Đóng" onClick={() => set({ panel: null })}><Icon name="close" /></button>
      </div>
      {panel === 'notebook' ? <Notebook /> : panel === 'team' && room ? <Team /> : <Questions />}
    </aside>
  );
}

/* ── conclusions ── */
function useDocLabel() {
  const { c } = useBoard();
  return {
    doc: (id: string) => {
      const d = c.documents.find((x) => x.id === id);
      return d ? `${pad2(d.no ?? 0)} · ${d.title}` : id;
    },
    line: (ref: string) => {
      const [id, n] = ref.split(':');
      const d = c.documents.find((x) => x.id === id);
      return d ? `Tài liệu ${pad2(d.no ?? 0)} · dòng ${n}` : ref;
    },
  };
}

function Questions() {
  const { c, store } = useBoard();
  const st = useBoardState(useShallow((s) => ({ q: s.q, pins: s.pins, feedback: s.feedback })));
  const s = store.getState();
  const cur = currentQ(c, s);
  const done = c.questions.filter((q) => isSolved(s, q)).length;
  const set = useUi((x) => x.set);
  const curRef = useRef<HTMLElement>(null);
  const curId = cur?.id;
  useEffect(() => { curRef.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }, [curId]);

  let lockedShown = false;
  return (
    <div className="panel__body">
      <div className="progress" aria-label={`Đã giải ${done}/${c.questions.length}`}><span style={{ width: `${(done / Math.max(1, c.questions.length)) * 100}%` }} /></div>
      {c.questions.map((q, i) => {
        const qs = st.q[q.id];
        const head = <><p className="q__no">Câu {i + 1} · Trọng điểm {q.stage}</p><h3 className="q__title"><Txt>{q.title}</Txt></h3></>;
        if (qs?.solved) return <SolvedQ key={q.id} q={q} head={head} />;
        if (q !== cur) {
          if (lockedShown) return null;
          lockedShown = true;
          const rest = c.questions.length - i;
          return (
            <article key={q.id} className="q is-locked">
              <p className="q__no">Câu {i + 1}{rest > 1 ? `–${c.questions.length}` : ''}</p>
              <p className="q__lock">Còn {rest} câu hỏi đang khoá. Giải câu hiện tại để mở tiếp.</p>
            </article>
          );
        }
        return <CurrentQ key={q.id} q={q} head={head} innerRef={curRef} />;
      })}
      {allSolved(c, s) && (
        <article className="q q--final">
          <p className="q__no">Hồ sơ đã khép lại</p>
          <h3 className="q__title">Bạn đã phá được vụ án.</h3>
          <button type="button" className="btn btn--primary btn--small" onClick={() => set({ dialog: 'finale' })}>Đọc kết luận vụ án</button>
        </article>
      )}
    </div>
  );
}

function SolvedQ({ q, head }: { q: Question; head: React.ReactNode }) {
  const label = useDocLabel();
  const answer = q.type === 'evidence'
    ? (q.answer || []).map((a) => label.doc(String(a)))
    : q.type === 'line'
      ? (q.answer || []).map((a) => label.line(normalizeLine(a)))
      : (q.answer || []).map((a) => (q.options || [])[Number(a)] || '');
  return (
    <article className="q is-solved">
      {head}
      {(q.type !== 'choice' || (q.options || []).length > 0) && (
        <div className="q__answer"><span>Đáp án</span>{answer.map((a, i) => <div key={i}><Txt>{a}</Txt></div>)}</div>
      )}
      {q.solved && <p className="q__msg"><Txt>{q.solved}</Txt></p>}
      {!!q.explanation?.length && (
        <details className="q__explain">
          <summary>Lời giải</summary>
          {q.explanation.map((e, i) => <div key={i}><h4><Txt>{e.title}</Txt></h4><Paras list={e.body} /></div>)}
        </details>
      )}
    </article>
  );
}

/* Guessing guard: the first wrong answer is free; after that each wrong answer locks the button for a while
   (15 s, 30 s, 45 s, max 60 s) so trying every combination costs more than reading the papers. */
const lockedUntil = new Map<string, number>();
const COOLDOWN = (wrongs: number) => (wrongs < 2 ? 0 : Math.min(60, 15 * (wrongs - 1))) * 1000;

function useCountdown(until: number) {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (until <= Date.now()) return undefined;
    const t = window.setInterval(() => setNow(Date.now()), 500);
    return () => window.clearInterval(t);
  }, [until]);
  return Math.max(0, Math.ceil((until - now) / 1000));
}

function CurrentQ({ q, head, innerRef }: { q: Question; head: React.ReactNode; innerRef: React.RefObject<HTMLElement> }) {
  const { c, store, focusDoc } = useBoard();
  const label = useDocLabel();
  const qs = useBoardState((s) => s.q[q.id]);
  const pins = useBoardState((s) => s.pins);
  const fb = useBoardState((s) => s.feedback[q.id]);
  const openDocs = useBoardState(useShallow((s) => c.documents.filter((d) => stageOpen(c, s, d.stage ?? 1)).map((d) => d.id)));
  const showToast = useUi((s) => s.showToast);
  const set = useUi((s) => s.set);
  const api = store.getState();
  const hints = q.hints || [];
  const isReveal = q.type === 'choice' && !(q.options || []).length;
  const lockKey = `${c.id}:${q.id}`;
  const [lockUntil, setLockUntil] = useState(() => lockedUntil.get(lockKey) || 0);
  const wait = useCountdown(lockUntil);

  const submit = () => {
    if (wait > 0) return;
    const r = api.submit(q.id);
    if (r?.status === 'wrong') {
      const wrongs = store.getState().q[q.id]?.tries || 0;
      const until = Date.now() + COOLDOWN(wrongs);
      if (until > Date.now()) { lockedUntil.set(lockKey, until); setLockUntil(until); }
    }
    if (r?.status === 'correct') {
      showToast('Chính xác!');
      const s = store.getState();
      if (allSolved(c, s)) setTimeout(() => set({ dialog: 'finale' }), 900);
    }
  };

  let form: React.ReactNode = null;
  if (q.type === 'evidence') {
    const need = evidenceNeed(q);
    form = (
      <>
        <div className="slots">
          {Array.from({ length: need }, (_, i) => {
            const v = pins[i] || '';
            const d = v ? c.documents.find((x) => x.id === v) : null;
            return (
              <div key={i} className={`slot${v ? ' is-filled' : ''}`}>
                <span className="slot__n">{i + 1}</span>
                <span className="slot__body">
                  {d ? (
                    <>
                      <span className="slot__meta">Tài liệu {pad2(d.no ?? 0)} · {typeLabel(d.type)}</span>
                      <span className="slot__title">{d.title}</span>
                    </>
                  ) : <span className="slot__empty">Chọn tài liệu…</span>}
                </span>
                {/* the native picker covers the whole card: one tap opens the iPad / browser list */}
                <select value={v} aria-label={`Bằng chứng ${i + 1}`} onChange={(e) => api.setPin(i, e.target.value || null, need)}>
                  <option value="">Chọn tài liệu…</option>
                  {openDocs.map((id) => <option key={id} value={id}>{label.doc(id)}</option>)}
                </select>
                {v && (
                  <span className="slot__actions">
                    <button type="button" className="icon-btn icon-btn--sm" aria-label="Xem tài liệu" onClick={() => focusDoc(v)}><Icon name="eye" /></button>
                    <button type="button" className="icon-btn icon-btn--sm" aria-label="Bỏ chọn" onClick={() => api.setPin(i, null, need)}><Icon name="close" /></button>
                  </span>
                )}
              </div>
            );
          })}
        </div>
        <p className="q__tip">Mẹo: chạm vào tài liệu rồi chọn “Ghim làm bằng chứng”, hoặc bấm biểu tượng ghim ở góc tài liệu.</p>
      </>
    );
  } else if (q.type === 'line') {
    form = (
      <div className={`line-pick${qs.line ? ' is-filled' : ''}`}>
        <span className="line-pick__label">Dòng đã chọn</span>
        <strong>{qs.line ? label.line(qs.line) : 'Chưa chọn'}</strong>
        {qs.line && <button type="button" className="link-btn" onClick={() => focusDoc(qs.line.split(':')[0], `l${Number(qs.line.split(':')[1])}`)}>Xem dòng này</button>}
        <span className="q__tip">Chạm vào một dòng có đánh số trong lời khai, rồi chọn “Chọn dòng này để trả lời”.</span>
      </div>
    );
  } else if (!isReveal) {
    const multi = Boolean(q.multiple);
    const toggle = (i: number) => api.setPick(q.id, multi ? (qs.pick.includes(i) ? qs.pick.filter((x) => x !== i) : [...qs.pick, i]) : [i]);
    form = (
      <>
        <div className="opts" role={multi ? 'group' : 'radiogroup'}>
          {(q.options || []).map((o, i) => (
            <label key={i} className={`opt${qs.pick.includes(i) ? ' is-on' : ''}`}>
              <input type={multi ? 'checkbox' : 'radio'} name={`opt-${q.id}`} checked={qs.pick.includes(i)} onChange={() => toggle(i)} />
              <span className="opt__k">{String.fromCharCode(65 + i)}</span><span><Txt>{o}</Txt></span>
            </label>
          ))}
        </div>
        {multi && <p className="q__tip">Có thể chọn nhiều đáp án.</p>}
      </>
    );
  }

  return (
    <article className="q is-current" ref={innerRef}>
      {head}
      {q.prompt && <div className="q__prompt"><Paras list={q.prompt} /></div>}
      {form}
      <div className="q__actions">
        <button type="button" className="btn btn--primary btn--small" onClick={submit} disabled={wait > 0} aria-disabled={wait > 0}>
          {wait > 0 ? `Đọc lại hồ sơ… (${wait} giây)` : isReveal ? 'Xem diễn biến' : q.submit || 'Gửi kết luận'}
        </button>
        {qs.tries > 0 && <span className="q__tries">{qs.tries} lần thử</span>}
      </div>
      {wait > 0 && <p className="q__cooldown">Kết luận sai liên tiếp sẽ bị tạm khoá. Hãy đối chiếu lại tài liệu trước khi gửi tiếp: mỗi lần sai đều tính vào xếp hạng cuối hồ sơ.</p>}
      {fb && <p className={`q__feedback is-${fb.status}`} role="status"><Txt>{fb.message}</Txt></p>}
      {qs.hints > 0 && (
        <ol className="q__hints">
          {hints.slice(0, qs.hints).map((h, i) => <li key={i}><b>Gợi ý {i + 1}</b><Txt>{h}</Txt></li>)}
        </ol>
      )}
      {qs.hints < hints.length && (
        <button type="button" className="link-btn" onClick={() => api.useHint(q.id)}>Xem gợi ý {qs.hints + 1}/{hints.length}</button>
      )}
    </article>
  );
}

/* ── notebook ── */
function AutoText({ value, onChange, placeholder, autoFocus }: { value: string; onChange: (v: string) => void; placeholder?: string; autoFocus?: boolean }) {
  const ref = useRef<HTMLTextAreaElement>(null);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${el.scrollHeight + 2}px`;
  }, [value]);
  useEffect(() => { if (autoFocus) ref.current?.focus({ preventScroll: false }); }, [autoFocus]);
  return <textarea ref={ref} rows={2} value={value} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} />;
}

function Notebook() {
  const { room } = useBoard();
  const [mine, setMine] = useState(true);
  if (!room) return <MyNotebook />;
  return (
    <div className="panel__body notebook">
      <div className="seg" role="tablist">
        <button type="button" role="tab" aria-selected={mine} className={mine ? 'is-on' : ''} onClick={() => setMine(true)}>Sổ của tôi</button>
        <button type="button" role="tab" aria-selected={!mine} className={!mine ? 'is-on' : ''} onClick={() => setMine(false)}>Sổ nhóm</button>
      </div>
      {mine ? <MyNotebook embedded /> : <TeamNotebook roomId={room.id} me={room.me} />}
    </div>
  );
}

function MyNotebook({ embedded = false }: { embedded?: boolean }) {
  const { c, store, focusDoc } = useBoard();
  const entries = useBoardState((s) => s.notebook);
  const label = useDocLabel();
  const api = store.getState();
  const newest = useRef<string | null>(null);
  const endRef = useRef<HTMLDivElement>(null);

  const add = () => {
    newest.current = api.addEntry({ kind: 'text', text: '' });
    setTimeout(() => endRef.current?.scrollIntoView({ block: 'end', behavior: 'smooth' }), 30);
  };
  const count = entries.length;
  return (
    <div className={embedded ? '' : 'panel__body notebook'}>
      <p className="notebook__intro">
        Sổ tay điều tra của bạn. Chạm vào bất kỳ đoạn văn nào trên bàn rồi chọn “Trích vào sổ tay” để lưu lại kèm nguồn.
        Trên iPad có thể viết tay bằng Apple Pencil (Scribble) vào ô ghi chú.
      </p>
      {count === 0 && <p className="notebook__empty">Chưa có ghi chép nào.</p>}
      <ol className="entries">
        {entries.map((e: Entry) => (
          <li key={e.id} className={`entry entry--${e.kind}`}>
            {e.kind === 'quote' ? (
              <>
                <blockquote>“{e.text}”</blockquote>
                <div className="entry__meta">
                  <span>{e.ref ? label.doc(e.ref.doc) : ''}</span>
                  {e.ref && c.documents.some((d) => d.id === e.ref!.doc) && (
                    <button type="button" className="link-btn" onClick={() => focusDoc(e.ref!.doc, e.ref!.key)}>Xem</button>
                  )}
                  <button type="button" className="icon-btn icon-btn--sm" aria-label="Xoá trích dẫn" onClick={() => api.deleteEntry(e.id)}><Icon name="trash" /></button>
                </div>
              </>
            ) : (
              <>
                <AutoText value={e.text} onChange={(v) => api.setEntry(e.id, v)} placeholder="Suy luận, nghi vấn, việc cần kiểm tra…" autoFocus={newest.current === e.id} />
                <div className="entry__meta">
                  <span>{new Date(e.at).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}</span>
                  <button type="button" className="icon-btn icon-btn--sm" aria-label="Xoá ghi chép" onClick={() => api.deleteEntry(e.id)}><Icon name="trash" /></button>
                </div>
              </>
            )}
          </li>
        ))}
      </ol>
      <div ref={endRef} />
      <button type="button" className="btn btn--ghost btn--small notebook__add" onClick={add}><Icon name="plus" />Thêm ghi chép</button>
    </div>
  );
}

/* ── shared notebook (room) ── */
// Own note: edit locally, save after a pause, so realtime echoes never move the caret.
function OwnTeamNote({ id, body }: { id: string; body: string }) {
  const [text, setText] = useState(body);
  const timer = useRef(0);
  useEffect(() => () => window.clearTimeout(timer.current), []);
  return (
    <AutoText value={text} onChange={(v) => {
      setText(v);
      window.clearTimeout(timer.current);
      timer.current = window.setTimeout(() => { void updateRoomNote(id, v); }, 600);
    }} />
  );
}

function TeamNotebook({ roomId, me }: { roomId: string; me: string }) {
  const { c, focusDoc } = useBoard();
  const notes = useRoom((s) => s.notes);
  const members = useRoom((s) => s.members);
  const label = useDocLabel();
  const [draft, setDraft] = useState('');
  const [err, setErr] = useState('');
  const color = (id: string) => members.find((m) => m.user_id === id)?.color || '#888';
  const post = async () => {
    if (!draft.trim()) return;
    try { await addRoomNote(roomId, { kind: 'text', body: draft.trim() }); setDraft(''); setErr(''); } catch (e) { setErr((e as Error).message); }
  };
  return (
    <>
      <p className="notebook__intro">Mọi thành viên đều thấy sổ nhóm ngay lập tức. Chạm vào một đoạn văn trên bàn rồi chọn “Trích vào sổ nhóm” để chia sẻ kèm nguồn.</p>
      {!notes.length && <p className="notebook__empty">Nhóm chưa ghi gì.</p>}
      <ol className="entries">
        {notes.map((n) => (
          <li key={n.id} className={`entry entry--${n.kind} entry--team`} style={{ '--who': color(n.user_id) } as React.CSSProperties}>
            <p className="entry__who">{memberName(n.user_id)}</p>
            {n.kind === 'quote' ? <blockquote>“{n.body}”</blockquote>
              : n.user_id === me ? <OwnTeamNote id={n.id} body={n.body} />
                : <p className="entry__text">{n.body}</p>}
            <div className="entry__meta">
              <span>{n.ref ? label.doc(n.ref.doc) : new Date(n.created_at).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}</span>
              {n.ref && c.documents.some((d) => d.id === n.ref!.doc) && <button type="button" className="link-btn" onClick={() => focusDoc(n.ref!.doc, n.ref!.key)}>Xem</button>}
              {n.user_id === me && <button type="button" className="icon-btn icon-btn--sm" aria-label="Xoá" onClick={() => { void deleteRoomNote(n.id); }}><Icon name="trash" /></button>}
            </div>
          </li>
        ))}
      </ol>
      <div className="team-compose">
        <textarea rows={2} value={draft} placeholder="Chia sẻ một suy luận với cả nhóm…" onChange={(e) => setDraft(e.target.value)} />
        <button type="button" className="btn btn--primary btn--small" disabled={!draft.trim()} onClick={() => { void post(); }}>Gửi</button>
      </div>
      {err && <p className="q__feedback is-wrong">{err}</p>}
    </>
  );
}

/* ── team: who is here + recent activity ── */
function Team() {
  const { c } = useBoard();
  const members = useRoom((s) => s.members);
  const online = useRoom((s) => s.online);
  const events = useRoom((s) => s.events);
  const room = useRoom((s) => s.room);
  const label = (id: unknown) => {
    const d = c.documents.find((x) => x.id === id);
    return d ? `Tài liệu ${String(d.no ?? 0).padStart(2, '0')}` : 'tài liệu';
  };
  const qNo = (id: unknown) => c.questions.findIndex((x) => x.id === id) + 1;
  const line = (e: RoomEvent) => {
    const p = e.payload || {};
    switch (e.kind) {
      case 'join': return 'vào phòng';
      case 'leave': return 'rời phòng';
      case 'kick': return `mời ${memberName(String(p.user))} ra khỏi phòng`;
      case 'start': return 'bắt đầu cuộc điều tra';
      case 'pin': return p.on ? `ghim ${label(p.doc)}` : `bỏ ghim ${label(p.doc)}`;
      case 'line': return `chọn dòng ${String(p.line || '').split(':')[1] || ''} của ${label(String(p.line || '').split(':')[0])}`;
      case 'pick': return 'đổi lựa chọn';
      case 'hint': return `mở gợi ý ${p.hint ?? ''} câu ${qNo(p.question)}`;
      case 'submit': return p.correct ? `giải đúng câu ${qNo(p.question)}` : `gửi kết luận câu ${qNo(p.question)} (chưa đúng)`;
      case 'finish': return 'khép lại hồ sơ';
      default: return e.kind;
    }
  };
  return (
    <div className="panel__body">
      <p className="q__no">Thành viên</p>
      <ul className="team-list">
        {members.map((m) => {
          const on = online.includes(m.user_id);
          return (
            <li key={m.user_id}>
              <Avatar name={m.name} color={m.color} online={on} size={32} />
              <span>{m.name}{m.role === 'host' ? ' · chủ phòng' : ''}</span>
              <span className={`lobby__dot${on ? ' is-on' : ''}`}>{on ? 'online' : 'vắng'}</span>
            </li>
          );
        })}
      </ul>
      {room?.join_code && room.status !== 'finished' && (
        <p className="q__tip">Mời thêm người: mã <b>{room.join_code}</b> (đổi mã trong sảnh chờ).</p>
      )}
      <p className="q__no" style={{ marginTop: 22 }}>Hoạt động gần đây</p>
      <ol className="feed">
        {[...events].reverse().map((e) => (
          <li key={e.id}>
            <b>{memberName(e.user_id)}</b> {line(e)}
            <time>{new Date(e.created_at).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })}</time>
          </li>
        ))}
      </ol>
    </div>
  );
}
