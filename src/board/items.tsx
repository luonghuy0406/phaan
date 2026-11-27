import { memo, useLayoutEffect, useMemo, useRef } from 'react';
import { useShallow } from 'zustand/react/shallow';
import type { CaseDoc } from '../lib/types';
import { pad2, caseNo } from '../lib/data';
import { Paper, PaperCtx, DEFAULT_WIDTH, Seal, TYPE_LABEL } from './papers';
import { useBoard, useBoardState, type BoardCtx } from './context';
import { currentQ, evidenceNeed, stageOpen, NOTE_COLORS, type End } from './store';
import { strokePath, type Stroke } from './ink';
import { useUi } from './ui';
import { localToWorld } from './geometry';
import { Icon } from './icons';
import { useTts, speakDoc, stop } from '../lib/tts';

/* ── ink ── */
const InkPath = memo(function InkPath({ s }: { s: Stroke }) {
  const d = useMemo(() => strokePath(s), [s]);
  return <path d={d} fill={s.c} className={s.m ? 'ink-marker' : undefined} />;
});

export function SurfaceInk({ target, className = 'ink' }: { target: string; className?: string }) {
  const strokes = useBoardState(useShallow((s) => s.ink.filter((k) => k.t === target)));
  if (!strokes.length) return null;
  // markers under pen strokes so writing stays readable
  const sorted = [...strokes.filter((s) => s.m), ...strokes.filter((s) => !s.m)];
  return <svg className={className} aria-hidden="true">{sorted.map((s) => <InkPath key={s.id} s={s} />)}</svg>;
}

/* ── size tracking ── */
function useTrackSize(key: string, ref: React.RefObject<HTMLElement>, register: (el: HTMLElement | null) => void) {
  const { reg } = useBoard();
  const bump = useUi((s) => s.bumpLayout);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return undefined;
    register(el);
    const measure = () => {
      const prev = reg.sizes.get(key);
      const next = { w: el.offsetWidth, h: el.offsetHeight };
      if (!prev || prev.w !== next.w || prev.h !== next.h) {
        reg.sizes.set(key, next);
        reg.anchorCache.clear();
        bump();
      }
    };
    measure();
    const ro = new ResizeObserver(measure);
    ro.observe(el);
    return () => { ro.disconnect(); register(null); reg.sizes.delete(key); };
  }, [key, reg, ref, register, bump]);
}

/* ── papers ── */
export const DocItem = memo(function DocItem({ doc }: { doc: CaseDoc }) {
  const { c, reg, store } = useBoard();
  const ref = useRef<HTMLElement>(null);
  const id = doc.id;
  const pos = useBoardState((s) => s.docs[id]);
  const locked = useBoardState((s) => !stageOpen(c, s, doc.stage ?? 1));
  const hlKey = useBoardState((s) => s.hl.filter((k) => k.startsWith(`${id}:`)).join('|'));
  const picked = useBoardState((s) => { const q = currentQ(c, s); return q?.type === 'line' ? s.q[q.id].line : ''; });
  const evidence = useBoardState((s) => { const q = currentQ(c, s); return q?.type === 'evidence' ? q : null; });
  const pinSlot = useBoardState((s) => (evidence ? s.pins.indexOf(id) : -1));
  const isSpeaking = useTts((s) => s.activeId === `doc:${id}` && (s.status === 'playing' || s.status === 'loading' || s.status === 'downloading'));
  const showToast = useUi((s) => s.showToast);
  const { focusDoc } = useBoard();
  const hl = useMemo(() => new Set(hlKey ? hlKey.split('|').map((k) => k.slice(id.length + 1)) : []), [hlKey, id]);
  const nation = c.nationalHeader !== false;
  const paperCtx = useMemo(() => ({ hl, picked, nation }), [hl, picked, nation]);
  useTrackSize(`doc:${id}`, ref, (el) => { if (el) reg.docEls.set(id, el); else reg.docEls.delete(id); });

  const placed = Boolean(pos);
  const style: React.CSSProperties = {
    width: doc.width || DEFAULT_WIDTH[doc.type] || 520,
    transform: pos ? `translate(${pos.x}px, ${pos.y}px)${pos.r ? ` rotate(${pos.r * 90}deg)` : ''}` : undefined,
    zIndex: pos?.z ?? 1,
  };
  const classes = ['doc', `doc--${doc.type}`, locked && 'is-locked', !placed && 'is-unplaced', pinSlot >= 0 && 'is-pinned'].filter(Boolean).join(' ');

  return (
    <article
      ref={ref}
      className={classes}
      style={style}
      data-item={`doc:${id}`}
      data-surface={`doc:${id}`}
      data-doc={id}
      aria-hidden={locked || undefined}
      aria-label={`Tài liệu ${pad2(doc.no ?? 0)}: ${doc.title}`}
    >
      {/* the title bar is the paper's handle: drag it to move the paper; dragging the paper itself pans the desk */}
      <header className="doc__bar" data-bar data-grip title="Kéo thanh này để di chuyển tài liệu">
        <span className="doc__handle" aria-hidden="true"><Icon name="grip" /></span>
        <span className="doc__no">{pad2(doc.no ?? 0)}</span>
        <span className="doc__title">{doc.title}</span>
        <span className="doc__tools">
          {evidence && (
            <button type="button" className={`doc__btn doc__btn--pin${pinSlot >= 0 ? ' is-on' : ''}`} aria-label={pinSlot >= 0 ? 'Bỏ ghim' : 'Ghim làm bằng chứng'}
              onClick={() => {
                const r = store.getState().togglePin(id, evidenceNeed(evidence));
                showToast(r === 'full' ? `Đã ghim đủ ${evidenceNeed(evidence)} tài liệu. Bỏ bớt một ghim trước.` : r === 'pinned' ? 'Đã ghim làm bằng chứng.' : 'Đã bỏ ghim.');
              }}>
              <Icon name="pin" />
            </button>
          )}
          {doc.file && (
            <a className="doc__btn" href={`${import.meta.env.BASE_URL}cases/${c.id}/${doc.file}`} download aria-label="Tải bản gốc" title="Tải bản gốc" data-ui>
              <Icon name="download" />
            </a>
          )}
          {doc.type !== 'scan' && (
            <button
              type="button"
              className={`doc__btn doc__btn--tts${isSpeaking ? ' is-on' : ''}`}
              aria-label={isSpeaking ? 'Dừng đọc' : 'Đọc tài liệu'}
              title={isSpeaking ? 'Dừng đọc' : 'Đọc tài liệu'}
              onClick={() => {
                if (isSpeaking) stop();
                else void speakDoc(c.id, doc);
              }}
            >
              <Icon name={isSpeaking ? 'pause' : 'speaker'} />
            </button>
          )}
          <button type="button" className="doc__btn" aria-label="Đọc gần" title="Đọc gần" onClick={() => focusDoc(id)}>
            <Icon name="search" />
          </button>
          <button type="button" className="doc__btn" aria-label="Xoay tài liệu" onClick={(e) => store.getState().rotateDoc(id, e.shiftKey)}>
            <Icon name="rotate" />
          </button>
        </span>
      </header>
      <div className="doc__paper">
        <PaperCtx.Provider value={paperCtx}>
          <Paper doc={doc} base={`${import.meta.env.BASE_URL}cases/${c.id}/`} />
        </PaperCtx.Provider>
      </div>
      <SurfaceInk target={`doc:${id}`} />
      {pinSlot >= 0 && <span className="doc__pinned">Bằng chứng {pinSlot + 1}</span>}
    </article>
  );
});

/* ── sticky notes ── */
export const NoteItem = memo(function NoteItem({ id }: { id: string }) {
  const { reg, store } = useBoard();
  const ref = useRef<HTMLDivElement>(null);
  const note = useBoardState((s) => s.notes.find((n) => n.id === id));
  useTrackSize(`note:${id}`, ref, (el) => { if (el) reg.noteEls.set(id, el); else reg.noteEls.delete(id); });
  if (!note) return null;
  return (
    <div
      ref={ref}
      className="note"
      data-item={`note:${id}`}
      data-surface={`note:${id}`}
      data-note={id}
      style={{ transform: `translate(${note.x}px, ${note.y}px)`, zIndex: note.z, background: NOTE_COLORS[note.c ?? 0] }}
    >
      <div className="note__grip" data-grip><span>Ghi chú</span><Icon name="dots" /></div>
      <textarea
        id={`note-${id}`}
        value={note.text}
        maxLength={1000}
        placeholder="Viết hoặc dùng Apple Pencil…"
        aria-label="Nội dung ghi chú"
        onChange={(e) => store.getState().setNote(id, { text: e.target.value })}
      />
      <SurfaceInk target={`note:${id}`} />
    </div>
  );
});

export function NotesLayer() {
  const ids = useBoardState(useShallow((s) => s.notes.map((n) => n.id)));
  return <>{ids.map((id) => <NoteItem key={id} id={id} />)}</>;
}

/* ── round labels on the desk + a sealed envelope over every locked round ── */
export function StageMarks() {
  const { c, reg } = useBoard();
  useUi((s) => s.layoutVersion);
  const open = useBoardState(useShallow((s) => [...new Set(c.documents.map((d) => d.stage ?? 1))].map((n) => stageOpen(c, s, n))));
  const stages = [...new Set(c.documents.map((d) => d.stage ?? 1))].sort((a, b) => a - b);
  return (
    <>
      {stages.map((st, i) => {
        const docs = c.documents.filter((d) => (d.stage ?? 1) === st);
        const pts = docs.map((d) => reg.defaults[d.id]).filter(Boolean);
        if (!pts.length) return null;
        const x = Math.min(...pts.map((p) => p.x));
        const y = Math.min(...pts.map((p) => p.y));
        const nos = docs.map((d) => d.no ?? 0);
        const range = nos.length > 1 ? `Tài liệu ${pad2(Math.min(...nos))}–${pad2(Math.max(...nos))}` : `Tài liệu ${pad2(nos[0])}`;
        if (open[i]) {
          return <p key={st} className="zone" style={{ transform: `translate(${x}px, ${y - 92}px)` }}><b>Trọng điểm {st}</b> · {range}</p>;
        }
        // inventory by kind of paper only (never titles: nothing is revealed before the seal is broken)
        const kinds = Object.entries(docs.reduce<Record<string, number>>((m, d) => ({ ...m, [d.type]: (m[d.type] || 0) + 1 }), {}))
          .map(([t, n]) => `${n} ${(TYPE_LABEL[t as CaseDoc['type']] || 'tài liệu').toLowerCase()}`).join(' · ');
        const until = st === 2 ? 'trọng điểm 1' : `các trọng điểm 1–${st - 1}`;
        const sheets = Math.min(4, Math.max(2, Math.ceil(docs.length / 2)));
        return (
          <section key={st} className="seal env" style={{ transform: `translate(${x}px, ${y}px)` }} data-seal data-x={x} data-y={y} aria-label={`Hồ sơ trọng điểm ${st} đang niêm phong, mở khi giải xong ${until}`}>
            {/* papers peeking out behind the envelope */}
            {Array.from({ length: sheets }, (_, k) => <i key={k} className="env__sheet" style={{ '--k': k } as React.CSSProperties} />)}
            <div className="env__body">
              <div className="env__flap" />
              <span className="env__button env__button--flap" />
              <span className="env__button env__button--body" />
              <svg className="env__string" viewBox="0 0 120 120" aria-hidden="true"><path d="M60 22 C 30 40, 25 78, 60 92 C 92 104, 98 58, 74 46 C 60 40, 52 60, 64 64" /></svg>

              <div className="env__label">
                <p className="env__agency">Ban chuyên án · {caseNo(c)}</p>
                <p className="env__kind">Hồ sơ vụ án</p>
                <dl className="env__rows">
                  <div><dt>Vụ án</dt><dd>{c.title}</dd></div>
                  <div><dt>Trọng điểm</dt><dd>{String(st).padStart(2, '0')}</dd></div>
                  <div><dt>Tài liệu</dt><dd>{range.replace('Tài liệu ', 'Số ')} ({docs.length} tờ)</dd></div>
                  <div><dt>Bảng kê</dt><dd>{kinds}</dd></div>
                </dl>
              </div>
              <span className="env__mat">Mật</span>

              <div className="env__strip">
                <b>Niêm phong</b>
                <span>Chỉ mở khi đã giải {until}</span>
                <i className="env__sig">Đ.tra viên</i>
                <Seal text="Ban chuyên án" />
              </div>
            </div>
          </section>
        );
      })}
    </>
  );
}

/* ── red strings ── */
function localOffset(el: HTMLElement, root: HTMLElement) {
  let x = 0;
  let y = 0;
  let n: HTMLElement | null = el;
  while (n && n !== root) {
    x += n.offsetLeft;
    y += n.offsetTop;
    n = n.offsetParent as HTMLElement | null;
  }
  return { x, y };
}

export function anchorPoint(ctx: Pick<BoardCtx, 'store' | 'reg' | 'c'>, end: End) {
  const s = ctx.store.getState();
  if ('note' in end) {
    const n = s.notes.find((x) => x.id === end.note);
    const size = ctx.reg.sizes.get(`note:${end.note}`);
    return n && size ? { x: n.x + size.w / 2, y: n.y + 10 } : null;
  }
  const d = s.docs[end.doc];
  const el = ctx.reg.docEls.get(end.doc);
  const size = ctx.reg.sizes.get(`doc:${end.doc}`);
  const meta = ctx.c.documents.find((x) => x.id === end.doc);
  if (!d || !el || !size || !meta || !stageOpen(ctx.c, s, meta.stage ?? 1)) return null;
  const box = { x: d.x, y: d.y, w: size.w, h: size.h, r: d.r };
  if (!end.key) return localToWorld(size.w / 2, 14, box);
  const cacheKey = `${end.doc}:${end.key}`;
  let local = ctx.reg.anchorCache.get(cacheKey);
  if (!local) {
    const blk = el.querySelector<HTMLElement>(`[data-key="${end.key}"]`);
    if (!blk) return localToWorld(size.w / 2, 14, box);
    const o = localOffset(blk, el);
    local = { x: o.x + 6, y: o.y + blk.offsetHeight / 2 };
    ctx.reg.anchorCache.set(cacheKey, local);
  }
  return localToWorld(local.x, local.y, box);
}

function sagPath(a: { x: number; y: number }, b: { x: number; y: number }) {
  const sag = Math.min(160, Math.hypot(b.x - a.x, b.y - a.y) * 0.18);
  return `M${a.x.toFixed(1)} ${a.y.toFixed(1)} Q${((a.x + b.x) / 2).toFixed(1)} ${((a.y + b.y) / 2 + sag).toFixed(1)} ${b.x.toFixed(1)} ${b.y.toFixed(1)}`;
}

export function Strings() {
  const ctx = useBoard();
  const strings = useBoardState((s) => s.strings);
  useBoardState((s) => s.docs);
  useBoardState((s) => s.notes);
  useBoardState((s) => s.q);
  useUi((s) => s.layoutVersion);
  const pending = useUi((s) => s.pendingString);
  const pendingPt = pending ? anchorPoint(ctx, pending) : null;
  return (
    <svg className="strings" aria-hidden="true">
      {strings.map((s) => {
        const a = anchorPoint(ctx, s.a);
        const b = anchorPoint(ctx, s.b);
        if (!a || !b) return null;
        return (
          <g key={s.id}>
            <path className="str" d={sagPath(a, b)} />
            <circle className="str__pin" cx={a.x} cy={a.y} r={7} />
            <circle className="str__pin" cx={b.x} cy={b.y} r={7} />
          </g>
        );
      })}
      {pendingPt && <circle className="str__pin str__pin--pending" cx={pendingPt.x} cy={pendingPt.y} r={11} />}
    </svg>
  );
}
