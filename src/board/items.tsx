import { memo, useEffect, useLayoutEffect, useMemo, useRef } from 'react';
import { useShallow } from 'zustand/react/shallow';
import type { CaseDoc } from '../lib/types';
import { pad2, caseNo } from '../lib/data';
import { Paper, PaperCtx, DEFAULT_WIDTH, Seal, TYPE_LABEL } from './papers';
import { useBoard, useBoardState, type BoardCtx } from './context';
import { currentQ, evidenceNeed, stageOpen, NOTE_COLORS, type End, type Str } from './store';
import { strokePath, type Stroke } from './ink';
import { useUi } from './ui';
import { localToWorld, type Pt } from './geometry';
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
    if (!n || !size) return null;
    return end.x != null && end.y != null ? { x: n.x + end.x, y: n.y + end.y } : { x: n.x + size.w / 2, y: n.y + 10 };
  }
  const d = s.docs[end.doc];
  const el = ctx.reg.docEls.get(end.doc);
  const size = ctx.reg.sizes.get(`doc:${end.doc}`);
  const meta = ctx.c.documents.find((x) => x.id === end.doc);
  if (!d || !el || !size || !meta || !stageOpen(ctx.c, s, meta.stage ?? 1)) return null;
  const box = { x: d.x, y: d.y, w: size.w, h: size.h, r: d.r };
  if (end.x != null && end.y != null) return localToWorld(end.x, end.y, box);
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

function hashSeed(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return ((h >>> 0) % 2000) / 1000 - 1; // [-1, 1)
}

function endKey(e: End): string {
  const base = 'note' in e ? `note:${e.note}` : `doc:${e.doc}:${e.key || ''}`;
  return e.x != null && e.y != null ? `${base}@${Math.round(e.x / 6)},${Math.round(e.y / 6)}` : base;
}

// Offset from the steel needle puncture point (0, 0) up-left to the wrapped yarn collar on the exposed needle shaft.
const PIN_NECK_X = -1.2;
const PIN_NECK_Y = -3.6;

function stringGeom(a: Pt, b: Pt, seedStr: string, endOnPin = true) {
  const ax = a.x + PIN_NECK_X;
  const ay = a.y + PIN_NECK_Y;
  const bx = b.x + (endOnPin ? PIN_NECK_X : 0);
  const by = b.y + (endOnPin ? PIN_NECK_Y : 0);
  const dx = bx - ax;
  const dy = by - ay;
  const dist = Math.hypot(dx, dy);
  if (dist < 1) {
    const p = `M${ax.toFixed(1)} ${ay.toFixed(1)} a4 4 0 1 0 0.1 0`;
    return { path: p, shadow: p };
  }
  const h = hashSeed(seedStr);
  const horiz = Math.abs(dx) / dist;
  const sag = Math.min(185, dist * (0.14 + 0.09 * horiz) + 12) * (1 + h * 0.12);
  const sway = Math.abs(dx) < 90
    ? (1 - Math.abs(dx) / 90) * Math.min(34, dist * 0.1 + 10) * (h >= 0 ? 1 : -1)
    : h * 6;
  const c1x = ax + dx * 0.28 + sway;
  const c1y = ay + dy * 0.28 + sag;
  const c2x = ax + dx * 0.72 + sway;
  const c2y = ay + dy * 0.72 + sag;
  const path = `M${ax.toFixed(1)} ${ay.toFixed(1)} C${c1x.toFixed(1)} ${c1y.toFixed(1)} ${c2x.toFixed(1)} ${c2y.toFixed(1)} ${bx.toFixed(1)} ${by.toFixed(1)}`;
  const dropY = 4.5 + Math.min(16, sag * 0.11);
  const dropX = 3.5 + Math.min(7, sag * 0.045);
  const shadow = `M${(a.x + 1.3).toFixed(1)} ${(a.y + 1.6).toFixed(1)} C${(c1x + dropX).toFixed(1)} ${(c1y + dropY).toFixed(1)} ${(c2x + dropX).toFixed(1)} ${(c2y + dropY).toFixed(1)} ${(b.x + (endOnPin ? 1.3 : 2.2)).toFixed(1)} ${(b.y + (endOnPin ? 1.6 : 3.2)).toFixed(1)}`;
  return { path, shadow };
}

/** 3D detective pushpin anchored by its needle tip at (0, 0), with wrapped yarn collar and loose thread tails. */
const PinMark = memo(function PinMark({ x, y, seed, multi, pending }: { x: number; y: number; seed: string; multi?: boolean; pending?: boolean }) {
  const h = hashSeed(seed);
  const tilt = (h * 4.5).toFixed(2);
  const t1 = (9.0 + h * 2.2).toFixed(1);
  const t2 = (10.8 - h * 2.2).toFixed(1);
  const s1 = (-4.2 + h * 2.0).toFixed(1);
  const s2 = (3.6 + h * 1.8).toFixed(1);
  return (
    <g className={`str__pin${pending ? ' str__pin--pending' : ''}`} transform={`translate(${x.toFixed(1)} ${y.toFixed(1)})`}>
      {/* cast shadow on paper/desk */}
      <ellipse cx="6.2" cy="5.0" rx="7.6" ry="4.1" transform="rotate(24 6.2 5.0)" fill="rgba(8, 5, 2, 0.16)" />
      <ellipse cx="5.4" cy="4.4" rx="5.4" ry="2.9" transform="rotate(24 5.4 4.4)" fill="rgba(8, 5, 2, 0.34)" />
      <path d="M0.3 0.2 L4.8 3.8" stroke="rgba(8, 5, 2, 0.45)" strokeWidth="1.5" strokeLinecap="round" />

      {/* dangling loose red thread tails + cast shadows */}
      <g transform={`translate(${PIN_NECK_X} ${PIN_NECK_Y})`}>
        <path d={`M-0.4 0.7 Q${s1} 4.5 ${(Number(s1) * 1.15).toFixed(1)} ${t1}`} fill="none" stroke="rgba(8, 5, 2, 0.3)" strokeWidth="2.0" strokeLinecap="round" transform="translate(1.8 2.2)" />
        <path d={`M0.5 0.7 Q${s2} 5.2 ${(Number(s2) * 1.1).toFixed(1)} ${t2}`} fill="none" stroke="rgba(8, 5, 2, 0.3)" strokeWidth="1.9" strokeLinecap="round" transform="translate(1.8 2.2)" />
        <path d={`M-0.4 0.7 Q${s1} 4.5 ${(Number(s1) * 1.15).toFixed(1)} ${t1}`} fill="none" stroke="#991a14" strokeWidth="1.75" strokeLinecap="round" />
        <path d={`M-0.4 0.7 Q${s1} 4.5 ${(Number(s1) * 1.15).toFixed(1)} ${t1}`} fill="none" stroke="#e24334" strokeWidth="0.9" strokeDasharray="2.5 2.2" strokeLinecap="round" />
        <path d={`M0.5 0.7 Q${s2} 5.2 ${(Number(s2) * 1.1).toFixed(1)} ${t2}`} fill="none" stroke="#8c1610" strokeWidth="1.65" strokeLinecap="round" />
        <path d={`M0.5 0.7 Q${s2} 5.2 ${(Number(s2) * 1.1).toFixed(1)} ${t2}`} fill="none" stroke="#d83829" strokeWidth="0.85" strokeDasharray="2.2 2.4" strokeLinecap="round" />
      </g>

      {/* pinhole + exposed steel needle shaft */}
      <circle cx="0" cy="0" r="1.35" fill="rgba(20, 10, 6, 0.75)" />
      <path d="M0 0 L-2.4 -7.4" stroke="#575e69" strokeWidth="1.9" strokeLinecap="round" />
      <path d="M-0.3 -0.4 L-2.5 -7.2" stroke="#edf1f7" strokeWidth="0.8" strokeLinecap="round" />

      {/* yarn collar wrapped cleanly around the exposed needle shaft */}
      <g transform={`translate(${PIN_NECK_X} ${PIN_NECK_Y})`}>
        <ellipse cx="0" cy="0" rx={multi ? 3.3 : 2.8} ry={multi ? 1.85 : 1.5} fill="none" stroke="#7d120c" strokeWidth={multi ? 2.8 : 2.3} />
        <path d="M-2.7 0.2 A2.7 1.5 0 0 0 2.7 0.1" fill="none" stroke="#e34535" strokeWidth="1.35" strokeLinecap="round" />
        {multi && <path d="M-3.0 -0.4 A3.0 1.65 0 0 1 2.9 -0.3" fill="none" stroke="#b92118" strokeWidth="1.2" strokeLinecap="round" />}
      </g>

      {/* 3D plastic pushpin body seated above the collar (skirt, waist barrel, glossy top cap) */}
      <g transform={`rotate(${tilt})`}>
        <ellipse cx="-2.8" cy="-9.2" rx="7.6" ry="4.6" fill="url(#str-pin-skirt)" stroke="#4c0906" strokeWidth="0.85" />
        <ellipse cx="-2.8" cy="-9.5" rx="6.2" ry="3.5" fill="none" stroke="rgba(255, 198, 186, 0.26)" strokeWidth="0.75" />
        <path d="M-7.0 -9.4 A4.2 2.1 0 0 0 1.4 -9.4 L0.2 -13.4 L-7.4 -13.4 Z" fill="url(#str-pin-barrel)" stroke="#4e0906" strokeWidth="0.7" />
        <ellipse cx="-3.6" cy="-13.6" rx="6.4" ry="4.3" fill="url(#str-pin-cap-edge)" stroke="#470805" strokeWidth="0.8" />
        <ellipse cx="-3.6" cy="-14.4" rx="6.1" ry="4.0" fill="url(#str-pin-head)" />
        <path d="M-7.7 -15.3 A4.5 2.8 0 0 1 -2.3 -17.3" fill="none" stroke="rgba(255, 245, 240, 0.78)" strokeWidth="1.35" strokeLinecap="round" />
        <ellipse cx="-5.8" cy="-16.0" rx="1.5" ry="0.8" transform="rotate(-18 -5.8 -16.0)" fill="rgba(255, 249, 245, 0.6)" />
      </g>
    </g>
  );
});

export function Strings() {
  const ctx = useBoard();
  const { cam } = ctx;
  const strings = useBoardState((s) => s.strings);
  useBoardState((s) => s.docs);
  useBoardState((s) => s.notes);
  useBoardState((s) => s.q);
  useUi((s) => s.layoutVersion);
  const pending = useUi((s) => s.pendingString);
  const pendingPt = pending ? anchorPoint(ctx, pending) : null;

  const liveShadowRef = useRef<SVGPathElement>(null);
  const liveBaseRef = useRef<SVGPathElement>(null);
  const liveTwistRef = useRef<SVGPathElement>(null);
  const liveEndRef = useRef<SVGCircleElement>(null);

  // Live taut/sagging preview string following the mouse or Apple Pencil hover while picking the second endpoint.
  useEffect(() => {
    const clear = () => {
      liveShadowRef.current?.setAttribute('d', '');
      liveBaseRef.current?.setAttribute('d', '');
      liveTwistRef.current?.setAttribute('d', '');
      liveEndRef.current?.setAttribute('opacity', '0');
    };
    if (!pending || !pendingPt) { clear(); return undefined; }
    let hasCursor = false;
    let lx = 0;
    let ly = 0;
    const draw = () => {
      if (!hasCursor) return;
      const cur = cam.toWorld(lx, ly);
      const g = stringGeom(pendingPt, cur, 'pending', false);
      liveShadowRef.current?.setAttribute('d', g.shadow);
      liveBaseRef.current?.setAttribute('d', g.path);
      liveTwistRef.current?.setAttribute('d', g.path);
      if (liveEndRef.current) {
        liveEndRef.current.setAttribute('cx', cur.x.toFixed(1));
        liveEndRef.current.setAttribute('cy', cur.y.toFixed(1));
        liveEndRef.current.setAttribute('opacity', '1');
      }
    };
    const onMove = (e: PointerEvent) => {
      if (e.pointerType === 'touch') return;
      hasCursor = true;
      lx = e.clientX;
      ly = e.clientY;
      draw();
    };
    window.addEventListener('pointermove', onMove, { passive: true });
    const unsub = cam.subscribe(draw);
    return () => { window.removeEventListener('pointermove', onMove); unsub(); clear(); };
  }, [cam, pending, pendingPt]);

  const resolved: { s: Str; a: Pt; b: Pt; g: { path: string; shadow: string } }[] = [];
  const pins = new Map<string, { x: number; y: number; key: string; count: number }>();
  const addPin = (end: End, pt: Pt) => {
    const k = endKey(end);
    const cur = pins.get(k);
    if (cur) cur.count += 1;
    else pins.set(k, { x: pt.x, y: pt.y, key: k, count: 1 });
  };
  strings.forEach((s) => {
    const a = anchorPoint(ctx, s.a);
    const b = anchorPoint(ctx, s.b);
    if (!a || !b) return;
    resolved.push({ s, a, b, g: stringGeom(a, b, s.id) });
    addPin(s.a, a);
    addPin(s.b, b);
  });

  const pendingKey = pending ? endKey(pending) : '';
  const pendingAlreadyPinned = pendingPt ? pins.has(pendingKey) : false;

  return (
    <svg className="strings" aria-hidden="true">
      <defs>
        <radialGradient id="str-pin-skirt" cx="38%" cy="32%" r="68%">
          <stop offset="0%" stopColor="#e64133" />
          <stop offset="58%" stopColor="#b41e15" />
          <stop offset="100%" stopColor="#580a06" />
        </radialGradient>
        <linearGradient id="str-pin-barrel" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#7e100b" />
          <stop offset="32%" stopColor="#d83729" />
          <stop offset="70%" stopColor="#9a1610" />
          <stop offset="100%" stopColor="#4b0805" />
        </linearGradient>
        <linearGradient id="str-pin-cap-edge" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#d63628" />
          <stop offset="55%" stopColor="#9e1710" />
          <stop offset="100%" stopColor="#4a0805" />
        </linearGradient>
        <radialGradient id="str-pin-head" cx="34%" cy="28%" r="72%">
          <stop offset="0%" stopColor="#ff9c8a" />
          <stop offset="24%" stopColor="#e53c2c" />
          <stop offset="68%" stopColor="#b51b13" />
          <stop offset="100%" stopColor="#690c08" />
        </radialGradient>
      </defs>

      {/* 1. cast shadows beneath every yarn */}
      <g className="str-shadows">
        {resolved.map(({ s, g }) => (
          <g key={s.id}>
            <path className="str__shadow-outer" d={g.shadow} />
            <path className="str__shadow-inner" d={g.shadow} />
          </g>
        ))}
      </g>

      {/* 2. braided red yarn cords */}
      {resolved.map(({ s, g }) => (
        <g key={s.id} className="str-group" data-str={s.id}>
          <path className="str__base" d={g.path} />
          <path className="str__twist" d={g.path} />
          <path className="str__shine" d={g.path} />
          <path className="str__hit" d={g.path} />
        </g>
      ))}

      {/* 3. live preview thread while connecting */}
      {pendingPt && (
        <g className="str-live">
          <path ref={liveShadowRef} className="str__shadow-inner" />
          <path ref={liveBaseRef} className="str__base str__base--live" />
          <path ref={liveTwistRef} className="str__twist" />
          <circle ref={liveEndRef} className="str__live-tip" r={4} opacity={0} />
        </g>
      )}

      {/* 4. 3D pushpins sitting over tied yarn ends */}
      {[...pins.values()].map((p) => (
        <PinMark key={p.key} x={p.x} y={p.y} seed={p.key} multi={p.count > 1} />
      ))}

      {/* 5. pending pin pulse ring (+ unseated pin if not already pinned here) */}
      {pendingPt && (
        <>
          <circle className="str__pulse" cx={pendingPt.x} cy={pendingPt.y} r={14} />
          {!pendingAlreadyPinned && <PinMark x={pendingPt.x} y={pendingPt.y} seed={pendingKey || 'pending'} pending />}
        </>
      )}
    </svg>
  );
}
