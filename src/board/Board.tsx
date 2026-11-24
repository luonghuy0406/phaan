import { useCallback, useEffect, useMemo } from 'react';
import type { CaseData } from '../lib/types';
import { Ctx, surfaceBox, type BoardCtx, type Registry } from './context';
import { Camera } from './camera';
import { boundsOf, union, type Rect } from './geometry';
import { stageOpen, type BoardStore } from './store';
import { useUi, resetUi, type Tool } from './ui';
import { Viewport } from './Viewport';
import { Topbar, Toolbar, ActionMenu, PendingBanner, DocIndex, Toast } from './chrome';
import { SidePanel } from './panels';
import { Dialogs, Tour } from './dialogs';
import { TtsPlayer } from '../components/TtsPlayer';
import { setDocNumbers } from '../lib/text';
import { allSolved } from './store';
import { useRoomBoardSync } from '../multiplayer/sync';
import { useCloudSave } from '../lib/cloud';

export function Board({ c, store, room }: { c: CaseData; store: BoardStore; room?: { id: string; me: string } }) {
  const cam = useMemo(() => new Camera(), []);
  useMemo(() => setDocNumbers(new Map(c.documents.map((d) => [d.id, d.no ?? 0]))), [c]);
  const reg = useMemo<Registry>(() => ({
    docEls: new Map(), noteEls: new Map(), sizes: new Map(), defaults: {}, anchorCache: new Map(), lastDragEnd: 0, lastSyntheticTap: 0,
  }), []);

  const focusDoc = useCallback((id: string, key?: string) => {
    const box = surfaceBox({ store, reg }, `doc:${id}`);
    const el = reg.docEls.get(id);
    if (!box || !el || el.classList.contains('is-locked')) return;
    store.getState().raise('doc', id);
    cam.flyTo(cam.forRect(boundsOf(box), 1.1));
    el.classList.remove('is-flash');
    void el.offsetWidth; // restart the animation
    el.classList.add('is-flash');
    if (key) {
      const blk = el.querySelector<HTMLElement>(`[data-key="${key}"]`);
      if (blk) {
        blk.classList.add('is-flash-blk');
        setTimeout(() => blk.classList.remove('is-flash-blk'), 1800);
      }
    }
  }, [cam, reg, store]);

  const fitAll = useCallback((animate = true) => {
    const s = store.getState();
    const rects: Rect[] = [];
    c.documents.forEach((d) => {
      if (!stageOpen(c, s, d.stage ?? 1)) return;
      const b = surfaceBox({ store, reg }, `doc:${d.id}`);
      if (b) rects.push(boundsOf(b));
    });
    s.notes.forEach((n) => {
      const b = surfaceBox({ store, reg }, `note:${n.id}`);
      if (b) rects.push(boundsOf(b));
    });
    // only the next sealed round: later envelopes are further down the desk for players who explore
    const seal = document.querySelector<HTMLElement>('[data-seal]');
    if (seal) rects.push({ x: Number(seal.dataset.x), y: Number(seal.dataset.y), w: seal.offsetWidth, h: seal.offsetHeight });
    const all = union(rects);
    if (!all) return;
    const target = cam.forRect(all, 1);
    if (animate) cam.flyTo(target); else cam.set(target);
  }, [c, cam, reg, store]);

  const ctx = useMemo<BoardCtx>(() => ({ c, store, cam, reg, focusDoc, fitAll, room }), [c, store, cam, reg, focusDoc, fitAll, room?.id, room?.me]); // eslint-disable-line react-hooks/exhaustive-deps
  useRoomBoardSync(store, c, room?.id, room?.me);
  useCloudSave(store, c, room?.id ?? '');

  // fresh UI for each case; panel open by default on wide screens
  useEffect(() => {
    resetUi();
    if (window.innerWidth >= 1200) useUi.setState({ panel: 'questions' });
    if (!store.getState().seenIntro) useUi.setState({ dialog: 'intro' });
  }, [c.id, store]);

  // Newly unsealed papers: announce and fly to them.
  useEffect(() => store.subscribe((s, prev) => {
    if (s.q === prev.q) return;
    // the last round can be solved by a teammate too
    if (allSolved(c, s) && !allSolved(c, prev)) setTimeout(() => useUi.getState().set({ dialog: 'finale' }), 900);
    const open = c.documents.filter((d) => stageOpen(c, s, d.stage ?? 1));
    const before = c.documents.filter((d) => stageOpen(c, prev, d.stage ?? 1));
    if (open.length > before.length) {
      const fresh = open.filter((d) => !before.includes(d));
      useUi.getState().showToast(`Mở niêm phong: ${fresh.length} tài liệu mới đã được đặt lên bàn.`);
      setTimeout(() => {
        const rects = fresh.map((d) => surfaceBox({ store, reg }, `doc:${d.id}`)).filter((b): b is NonNullable<typeof b> => Boolean(b)).map(boundsOf);
        const u = union(rects);
        if (u) cam.flyTo(cam.forRect(u, 1));
        fresh.forEach((d) => {
          const el = reg.docEls.get(d.id);
          el?.classList.add('is-new');
          setTimeout(() => el?.classList.remove('is-new'), 2600);
        });
      }, 400);
    }
  }), [c, cam, reg, store]);

  // keyboard
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement;
      if (t.closest?.('textarea, input, select') || document.querySelector('dialog[open]')) return;
      const ui = useUi.getState();
      const mod = e.metaKey || e.ctrlKey;
      const k = e.key.toLowerCase();
      if (mod && k === 'z') { e.preventDefault(); if (e.shiftKey) store.getState().redo(); else store.getState().undo(); return; }
      if (mod || e.altKey) return;
      const tools: Record<string, Tool> = { v: 'move', p: 'pen', h: 'marker', e: 'eraser', n: 'note' };
      if (tools[k]) ui.setTool(tools[k]);
      else if (k === '+' || k === '=') cam.zoomBy(1.25);
      else if (k === '-' || k === '_') cam.zoomBy(0.8);
      else if (k === '0') fitAll();
      else if (k === 'escape') ui.set({ menu: null, pendingString: null, palette: false, indexOpen: false });
      else return;
      e.preventDefault();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [cam, fitAll, store]);

  const tool = useUi((s) => s.tool);
  const panel = useUi((s) => s.panel);
  const pending = useUi((s) => s.pendingString);

  return (
    <Ctx.Provider value={ctx}>
      <div className={`board tool-${tool}${panel ? ' has-panel' : ''}${pending ? ' has-pending' : ''}`}>
        <Topbar />
        <div className="board__body">
          <DocIndex />
          <div className="board__stage">
            <Viewport />
            <Toolbar />
            <PendingBanner />
            <Tour />
          </div>
          <SidePanel />
        </div>
        <ActionMenu />
        <Dialogs />
        <Toast />
        <TtsPlayer />
      </div>
    </Ctx.Provider>
  );
}
