/*
 * The desk: camera, gestures and pen input.
 *
 *  finger / mouse drag   pan the desk, also when it starts on a paper (papers stay put while browsing zoomed in);
 *                        a paper moves only when dragged by its title bar, a sticky note by its grip ([data-grip])
 *  two fingers / ⌘-wheel pinch zoom (use-gesture)
 *  Apple Pencil          always writes (unless turned off in settings); fingers keep panning,
 *                        and touches while the pencil is down are ignored (palm rejection)
 *  tap                   opens the action menu for the block / paper / note under the finger
 */
import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import { useGesture } from '@use-gesture/react';
import { useBoard, surfaceBox } from './context';
import { useUi } from './ui';
import { MIN_Z, MAX_Z } from './camera';
import { clamp, worldToLocal, type Box } from './geometry';
import { hitStroke, strokeLength, strokePath } from './ink';
import { uid, type End } from './store';
import { DocItem, NotesLayer, StageMarks, Strings, SurfaceInk } from './items';
import { DEFAULT_WIDTH } from './papers';

const UI_SEL = 'button, textarea, input, select, a, label, [data-ui]';

type Drag = { kind: 'pan' | 'item'; itemKind?: 'doc' | 'note'; id?: string; ox: number; oy: number; cancelled?: boolean; el?: HTMLElement };
type Ink = {
  pointerId: number; mode: 'pen' | 'marker' | 'eraser'; target: string; box: Box | null;
  pts: number[]; wpts: number[]; pen: boolean; t0: number; color: string; size: number;
};

async function waitForAssets(root: HTMLElement | null) {
  const imgs = root ? [...root.querySelectorAll('img')] : [];
  const ready = Promise.all([
    document.fonts?.ready,
    ...imgs.map((img) => (img.complete ? null : img.decode().catch(() => null))),
  ]);
  await Promise.race([ready, new Promise((r) => setTimeout(r, 2500))]);
}

export function Viewport() {
  const ctx = useBoard();
  const { c, store, cam, reg } = ctx;
  const vpRef = useRef<HTMLDivElement>(null);
  const worldRef = useRef<HTMLDivElement>(null);
  const liveRef = useRef<SVGPathElement>(null);
  const drag = useRef<Drag | null>(null);
  const pinching = useRef(false);
  const ink = useRef<Ink | null>(null);
  const lastPenUp = useRef(0);
  const liveFrame = useRef(0);
  const [ready, setReady] = useState(false);

  useLayoutEffect(() => {
    cam.attach(vpRef.current, worldRef.current);
    return () => cam.attach(null, null);
  }, [cam]);

  // First layout: measure every paper (fonts + images loaded), compute the default desk, place the camera.
  useEffect(() => {
    let live = true;
    (async () => {
      await waitForAssets(worldRef.current);
      if (!live) return;
      const stages = [...new Set(c.documents.map((d) => d.stage ?? 1))].sort((a, b) => a - b);
      const defaults: Record<string, { x: number; y: number; r: number }> = {};
      let y = 0;
      stages.forEach((st) => {
        let x = 0;
        let rowH = 0;
        c.documents.filter((d) => (d.stage ?? 1) === st).forEach((d) => {
          const el = reg.docEls.get(d.id);
          const w = el?.offsetWidth || d.width || DEFAULT_WIDTH[d.type] || 520;
          const h = el?.offsetHeight || 600;
          defaults[d.id] = Number.isFinite(d.x) && Number.isFinite(d.y) ? { x: d.x!, y: d.y!, r: (d.rotate ?? 0) % 4 } : { x, y, r: (d.rotate ?? 0) % 4 };
          x += w + 90;
          rowH = Math.max(rowH, h);
        });
        y += rowH + 200;
      });
      reg.defaults = defaults;
      store.getState().initLayout(defaults);
      useUi.getState().bumpLayout();
      const saved = store.getState().cam;
      const { w, h } = cam.size();
      requestAnimationFrame(() => {
        if (saved && Math.abs(saved.w - w) < 120 && Math.abs(saved.h - h) < 120) cam.set(saved);
        else ctx.fitAll(false);
        setReady(true);
      });
    })();
    return () => { live = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Persist the camera a moment after it stops moving; close menus when it moves.
  useEffect(() => {
    let t = 0;
    return cam.subscribe(() => {
      if (useUi.getState().menu) useUi.getState().set({ menu: null });
      window.clearTimeout(t);
      t = window.setTimeout(() => { const { w, h } = cam.size(); store.getState().saveCam(cam, w, h); }, 500);
    });
  }, [cam, store]);

  /* ── finger / mouse gestures ── */
  useGesture({
    onDrag: ({ first, last, movement: [mx, my], event, cancel, tap }) => {
      if (tap) return;
      if (first) {
        const t = event.target as HTMLElement;
        if (pinching.current || ink.current || t.closest(UI_SEL)) { cancel(); drag.current = null; return; }
        cam.stop();
        const item = t.closest<HTMLElement>('[data-item]');
        if (item && t.closest('[data-grip]')) {
          const [kind, id] = (item.dataset.item || '').split(':') as ['doc' | 'note', string];
          const st = store.getState();
          const p = kind === 'doc' ? st.docs[id] : st.notes.find((n) => n.id === id);
          if (!p) { cancel(); return; }
          st.raise(kind, id);
          drag.current = { kind: 'item', itemKind: kind, id, ox: p.x, oy: p.y, el: item };
          item.classList.add('is-lifted');
        } else {
          drag.current = { kind: 'pan', ox: cam.x, oy: cam.y };
        }
      }
      const d = drag.current;
      if (d && !d.cancelled) {
        if (d.kind === 'pan') cam.set({ x: d.ox + mx, y: d.oy + my });
        else store.getState().placeItem(d.itemKind!, d.id!, d.ox + mx / cam.z, d.oy + my / cam.z);
      }
      if (last) {
        reg.lastDragEnd = performance.now();
        d?.el?.classList.remove('is-lifted');
        drag.current = null;
      }
    },
    onPinchStart: () => {
      pinching.current = true;
      cancelFingerGesture(); // the first finger may have started dragging something
    },
    onPinch: ({ origin: [ox, oy], offset: [z], first, memo }) => {
      const r = vpRef.current!.getBoundingClientRect();
      const m = first || !memo ? { wx: (ox - r.left - cam.x) / cam.z, wy: (oy - r.top - cam.y) / cam.z } : memo;
      cam.set({ z, x: ox - r.left - m.wx * z, y: oy - r.top - m.wy * z });
      return m;
    },
    onPinchEnd: () => {
      pinching.current = false;
      reg.lastDragEnd = performance.now();
    },
    onWheel: ({ event }) => {
      const e = event as WheelEvent;
      e.preventDefault();
      if (e.ctrlKey || (e.target as HTMLElement).closest('textarea, [data-ui]')) return; // ctrl + wheel = trackpad pinch, handled above
      const r = vpRef.current!.getBoundingClientRect();
      const mouseWheel = e.deltaMode !== 0 || (e.deltaX === 0 && Math.abs(e.deltaY) >= 40 && Number.isInteger(e.deltaY));
      if (mouseWheel) cam.zoomAt(cam.z * Math.exp(-e.deltaY * (e.deltaMode === 1 ? 0.03 : 0.0018)), e.clientX - r.left, e.clientY - r.top);
      else cam.set({ x: cam.x - e.deltaX, y: cam.y - e.deltaY });
    },
  }, {
    target: vpRef,
    eventOptions: { passive: false },
    drag: { threshold: 4, filterTaps: true },
    pinch: { scaleBounds: { min: MIN_Z, max: MAX_Z }, from: () => [cam.z, 0], rubberband: false },
  });

  // Safari's own pinch-zoom of the page fights ours.
  useEffect(() => {
    const stop = (e: Event) => e.preventDefault();
    document.addEventListener('gesturestart', stop);
    document.addEventListener('gesturechange', stop);
    return () => {
      document.removeEventListener('gesturestart', stop);
      document.removeEventListener('gesturechange', stop);
    };
  }, []);

  function cancelFingerGesture() {
    const d = drag.current;
    if (!d || d.cancelled) return;
    if (d.kind === 'pan') cam.set({ x: d.ox, y: d.oy });
    else if (d.id && d.itemKind) store.getState().placeItem(d.itemKind, d.id, d.ox, d.oy);
    d.el?.classList.remove('is-lifted');
    d.cancelled = true;
  }

  /* ── pen input ── */
  function drawLive() {
    liveFrame.current = 0;
    const k = ink.current;
    const path = liveRef.current;
    if (!path) return;
    if (!k || k.mode === 'eraser' || k.wpts.length < 3) { path.setAttribute('d', ''); return; }
    path.setAttribute('d', strokePath({ pts: k.wpts, s: k.size, m: k.mode === 'marker' ? 1 : undefined, p: k.pen ? 1 : undefined }, false));
    path.setAttribute('fill', k.color);
    path.setAttribute('class', k.mode === 'marker' ? 'ink-marker' : '');
  }

  function eraseAt(wx: number, wy: number) {
    const st = store.getState();
    const radius = 12 / cam.z;
    const hits: string[] = [];
    for (const s of st.ink) {
      let x = wx;
      let y = wy;
      if (s.t !== 'world') {
        const box = surfaceBox(ctx, s.t);
        if (!box) continue;
        const p = worldToLocal(wx, wy, box);
        x = p.x; y = p.y;
      }
      if (hitStroke(s, x, y, radius)) hits.push(s.id);
    }
    if (hits.length) st.eraseStrokes(hits);
  }

  function addPoints(e: React.PointerEvent) {
    const k = ink.current;
    if (!k) return;
    const native = e.nativeEvent as PointerEvent;
    const events = native.getCoalescedEvents?.() ?? [];
    for (const ev of events.length ? events : [native]) {
      const w = cam.toWorld(ev.clientX, ev.clientY);
      if (k.mode === 'eraser') { eraseAt(w.x, w.y); continue; }
      if (k.pts.length >= 8997) break;
      const l = k.box ? worldToLocal(w.x, w.y, k.box) : w;
      const p = k.pen ? Math.max(0.05, ev.pressure || 0.5) : 0.5;
      k.pts.push(Math.round(l.x * 10) / 10, Math.round(l.y * 10) / 10, Math.round(p * 100) / 100);
      k.wpts.push(w.x, w.y, p);
    }
    if (!liveFrame.current) liveFrame.current = requestAnimationFrame(drawLive);
  }

  function onPointerDownCapture(e: React.PointerEvent) {
    const t = e.target as HTMLElement;
    const isPen = e.pointerType === 'pen';
    const ui = useUi.getState();
    if (isPen && !ui.penSeen) {
      ui.set({ penSeen: true });
      ui.showToast('Đã nhận Apple Pencil: viết bằng bút, di chuyển bằng ngón tay.');
    }
    // Palm rejection: while the pencil is down (or was just lifted) other touches are ignored.
    if (e.pointerType === 'touch' && (ink.current?.pen || performance.now() - lastPenUp.current < 350)) {
      e.stopPropagation();
      return;
    }
    if (ink.current || ui.pendingString) return;
    if (t.closest(UI_SEL)) return; // includes text boxes, so iPadOS Scribble keeps working there
    const tool = ui.tool;
    const inkTool = tool === 'pen' || tool === 'marker' || tool === 'eraser';
    let mode: Ink['mode'] | null = null;
    if (inkTool && (isPen || e.pointerType === 'mouse' || !ui.penSeen)) mode = tool as Ink['mode'];
    else if (isPen && tool === 'move' && ui.pencilDraws && !t.closest('[data-bar], [data-grip]')) mode = 'pen';
    if (!mode || (e.pointerType === 'mouse' && e.button !== 0)) return;

    e.stopPropagation(); // keep use-gesture from also panning
    vpRef.current?.setPointerCapture(e.pointerId);
    if (isPen) cancelFingerGesture();
    ui.set({ menu: null });
    cam.stop();

    const surf = t.closest<HTMLElement>('[data-surface]')?.dataset.surface ?? 'world';
    const box = surf === 'world' ? null : surfaceBox(ctx, surf);
    const style = mode === 'marker' ? ui.marker : ui.pen;
    ink.current = {
      pointerId: e.pointerId, mode, target: box ? surf : 'world', box,
      pts: [], wpts: [], pen: isPen, t0: performance.now(),
      color: style.color, size: Math.min(80, style.size / Math.max(cam.z, 0.15)),
    };
    addPoints(e);
  }

  function onPointerMove(e: React.PointerEvent) {
    if (ink.current && e.pointerId === ink.current.pointerId) addPoints(e);
  }

  function finishInk(e: React.PointerEvent, cancelled = false) {
    const k = ink.current;
    if (!k || e.pointerId !== k.pointerId) return;
    ink.current = null;
    if (k.pen) lastPenUp.current = performance.now();
    if (liveFrame.current) cancelAnimationFrame(liveFrame.current);
    drawLive();
    if (cancelled || k.mode === 'eraser') return;
    const len = strokeLength(k.wpts) * cam.z; // on-screen length
    if (len < 4 && performance.now() - k.t0 < 350) {
      // a tap with the pencil: treat it like a finger tap (open the menu, place a note…)
      reg.lastSyntheticTap = performance.now();
      handleTap(document.elementFromPoint(e.clientX, e.clientY), e.clientX, e.clientY);
      return;
    }
    store.getState().addStroke({
      id: uid('k'), t: k.target, pts: k.pts, c: k.color, s: Math.round(k.size * 10) / 10,
      ...(k.mode === 'marker' ? { m: 1 as const } : {}), ...(k.pen ? { p: 1 as const } : {}),
    });
  }

  /* ── taps ── */
  function pointEnd(doc: string | undefined, note: string | undefined, key: string | undefined, clientX: number, clientY: number): End | null {
    const w = cam.toWorld(clientX, clientY);
    if (doc) {
      const box = surfaceBox(ctx, `doc:${doc}`);
      if (!box) return key ? { doc, key } : { doc };
      const l = worldToLocal(w.x, w.y, box);
      return {
        doc,
        ...(key ? { key } : {}),
        x: Math.round(clamp(l.x, 8, Math.max(8, box.w - 8))),
        y: Math.round(clamp(l.y, 10, Math.max(10, box.h - 8))),
      };
    }
    if (note) {
      const box = surfaceBox(ctx, `note:${note}`);
      if (!box) return { note };
      return {
        note,
        x: Math.round(clamp(w.x - box.x, 8, Math.max(8, box.w - 8))),
        y: Math.round(clamp(w.y - box.y, 10, Math.max(10, box.h - 8))),
      };
    }
    return null;
  }

  function handleTap(target: Element | null, x: number, y: number) {
    if (!target) return;
    const ui = useUi.getState();
    const st = store.getState();
    const blk = target.closest<HTMLElement>('[data-key]');
    const docEl = target.closest<HTMLElement>('[data-doc]');
    const noteEl = target.closest<HTMLElement>('[data-note]');
    const strEl = target.closest<HTMLElement>('[data-str]');
    const doc = docEl?.dataset.doc;
    const note = noteEl?.dataset.note;

    if (ui.pendingString) {
      if (target.closest('[data-ui]')) return;
      const end = pointEnd(doc, note, blk?.dataset.key, x, y);
      if (end) ui.showToast(st.addString(ui.pendingString, end) ? 'Đã nối dây đỏ.' : 'Không nối được: chọn một điểm khác.');
      ui.set({ pendingString: null });
      return;
    }
    if (target.closest(UI_SEL)) return;
    if (strEl && ui.tool === 'move') {
      ui.set({ menu: { target: { kind: 'string', id: strEl.dataset.str! }, x, y } });
      return;
    }
    if (ui.tool === 'note' && !docEl && !noteEl && !target.closest('[data-seal]')) {
      const w = cam.toWorld(x, y);
      const id = st.addNote(w.x - 120, w.y - 24);
      if (!id) { ui.showToast('Đã đạt số ghi chú tối đa.'); return; }
      ui.setTool('move');
      setTimeout(() => document.getElementById(`note-${id}`)?.focus({ preventScroll: true }), 60);
      return;
    }
    if (blk && doc) {
      ui.set({ menu: { target: { kind: 'block', doc, key: blk.dataset.key!, line: blk.dataset.line, text: ((blk.querySelector('.tl__t') ?? blk).textContent || '').replace(/\s+/g, ' ').trim() }, x, y } });
    } else if (doc) {
      ui.set({ menu: { target: { kind: 'doc', doc }, x, y } });
    } else if (noteEl && target.closest('[data-grip]')) {
      ui.set({ menu: { target: { kind: 'note', note: noteEl.dataset.note! }, x, y } });
    } else {
      ui.set({ menu: null });
    }
  }

  function onClick(e: React.MouseEvent) {
    const now = performance.now();
    if (now - reg.lastDragEnd < 90 || now - reg.lastSyntheticTap < 600) return;
    if (ink.current || (e.nativeEvent as PointerEvent).pointerType === 'touch' && now - lastPenUp.current < 600) return; // palm
    handleTap(e.target as Element, e.clientX, e.clientY);
  }

  const docs = c.documents;
  return (
    <div
      ref={vpRef}
      className={`viewport${ready ? ' is-ready' : ''}`}
      onPointerDownCapture={onPointerDownCapture}
      onPointerMove={onPointerMove}
      onPointerUp={(e) => finishInk(e)}
      onPointerCancel={(e) => finishInk(e, true)}
      onClick={onClick}
      aria-label="Bàn điều tra"
    >
      <div ref={worldRef} className="world">
        <StageMarks />
        {docs.map((d) => <DocItem key={d.id} doc={d} />)}
        <NotesLayer />
        <Strings />
        <SurfaceInk target="world" className="ink ink--world" />
        <svg className="ink ink--live" aria-hidden="true"><path ref={liveRef} /></svg>
      </div>
      {!ready && <div className="viewport__loading">Đang trải hồ sơ lên bàn…</div>}
    </div>
  );
}
