import { createContext, useContext } from 'react';
import { useStore } from 'zustand';
import type { CaseData } from '../lib/types';
import type { BoardState, BoardStore } from './store';
import type { Camera } from './camera';
import type { Box } from './geometry';

// Live DOM registry, outside React state: element + size of each paper / note, and the default layout.
export interface Registry {
  docEls: Map<string, HTMLElement>;
  noteEls: Map<string, HTMLElement>;
  sizes: Map<string, { w: number; h: number }>; // key "doc:<id>" | "note:<id>"
  defaults: Record<string, { x: number; y: number; r: number }>;
  anchorCache: Map<string, { x: number; y: number }>;
  lastDragEnd: number;
  lastSyntheticTap: number;
}

export interface BoardCtx {
  c: CaseData;
  store: BoardStore;
  cam: Camera;
  reg: Registry;
  focusDoc: (id: string, key?: string) => void;
  fitAll: (animate?: boolean) => void;
  room?: { id: string; me: string }; // set when playing in a multiplayer room
}

export const Ctx = createContext<BoardCtx | null>(null);

export function useBoard(): BoardCtx {
  const v = useContext(Ctx);
  if (!v) throw new Error('useBoard outside board');
  return v;
}

export function useBoardState<T>(selector: (s: BoardState) => T): T {
  const { store } = useBoard();
  return useStore(store, selector);
}

// Current box (position + size + rotation) of a surface, or null if unknown.
export function surfaceBox(ctx: Pick<BoardCtx, 'store' | 'reg'>, target: string): Box | null {
  const s = ctx.store.getState();
  if (target.startsWith('doc:')) {
    const id = target.slice(4);
    const d = s.docs[id];
    const size = ctx.reg.sizes.get(target);
    return d && size ? { x: d.x, y: d.y, w: size.w, h: size.h, r: d.r } : null;
  }
  if (target.startsWith('note:')) {
    const id = target.slice(5);
    const n = s.notes.find((x) => x.id === id);
    const size = ctx.reg.sizes.get(target);
    return n && size ? { x: n.x, y: n.y, w: size.w, h: size.h, r: 0 } : null;
  }
  return null;
}
