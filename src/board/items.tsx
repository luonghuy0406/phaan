import { memo, useLayoutEffect, useMemo, useRef } from 'react';
import { useShallow } from 'zustand/react/shallow';
import type { CaseDoc } from '../lib/types';
import { pad2 } from '../lib/data';
import { Paper, PaperCtx, DEFAULT_WIDTH } from './papers';
import { useBoard, useBoardState, type BoardCtx } from './context';
import { currentQ, evidenceNeed, stageOpen, NOTE_COLORS, type End } from './store';
import { strokePath, type Stroke } from './ink';
import { useUi } from './ui';
import { localToWorld } from './geometry';
import { Icon } from './icons';

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
  const showToast = useUi((s) => s.showToast);
  const { focusDoc } = useBoard();
  const hl = useMemo(() => new Set(hlKey ? hlKey.split('|').map((k) => k.slice(id.length + 1)) : []), [hlKey, id]);
  const paperCtx = useMemo(() => ({ hl, picked }), [hl, picked]);
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
      <header className="doc__bar" data-bar>
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
        return (
          <section key={st} className="seal" style={{ transform: `translate(${x}px, ${y}px)` }} data-seal data-x={x} data-y={y}>
            <p className="seal__no">Trọng điểm {st} · {range}</p>
            <p className="seal__title">Hồ sơ niêm phong</p>
            <p className="seal__text">{docs.length} tài liệu. Mở khi bạn giải xong {st === 2 ? 'trọng điểm 1' : `các trọng điểm 1–${st - 1}`}.</p>
            <span className="stamp">Niêm phong</span>
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
