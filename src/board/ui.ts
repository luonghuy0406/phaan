// Non-persisted UI state of the board (tool, panels, menus). One board is open at a time.
import { create } from 'zustand';
import type { End } from './store';
import { MARKER_COLORS, MARKER_SIZES, PEN_COLORS, PEN_SIZES } from './ink';

export type Tool = 'move' | 'pen' | 'marker' | 'eraser' | 'note';
export type Panel = 'questions' | 'notebook' | 'team' | null;

export type MenuTarget =
  | { kind: 'block'; doc: string; key: string; line?: string; text: string }
  | { kind: 'doc'; doc: string }
  | { kind: 'note'; note: string }
  | { kind: 'string'; id: string };

export interface UiState {
  tool: Tool;
  pen: { color: string; size: number };
  marker: { color: string; size: number };
  palette: boolean;
  panel: Panel;
  indexOpen: boolean;
  menu: { target: MenuTarget; x: number; y: number } | null;
  pendingString: End | null;
  dialog: 'intro' | 'finale' | 'settings' | 'beat' | 'suspects' | 'interrogate' | null;
  /** suspect shown in the interrogation room */
  interrogateId: string | null;
  /** stage whose opening scene the 'beat' dialog shows */
  beatStage: number | null;
  tourStep: number | null;
  layoutVersion: number;
  penSeen: boolean;
  pencilDraws: boolean;
  toast: { text: string; id: number } | null;
  setTool: (t: Tool) => void;
  set: (patch: Partial<UiState>) => void;
  bumpLayout: () => void;
  showToast: (text: string) => void;
}

const SETTINGS_KEY = 'hsm:settings';
function readSettings(): { pencilDraws?: boolean } {
  try { return JSON.parse(localStorage.getItem(SETTINGS_KEY) || '{}'); } catch { return {}; }
}
export function saveSettings(s: { pencilDraws: boolean }) {
  try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(s)); } catch { /* ignore */ }
}

let layoutFrame = 0;
let toastId = 0;

export const useUi = create<UiState>((set, get) => ({
  tool: 'move',
  pen: { color: PEN_COLORS[0].v, size: PEN_SIZES[0] },
  marker: { color: MARKER_COLORS[0].v, size: MARKER_SIZES[1] },
  palette: false,
  panel: null,
  indexOpen: false,
  menu: null,
  pendingString: null,
  dialog: null,
  beatStage: null,
  interrogateId: null,
  tourStep: null,
  layoutVersion: 0,
  penSeen: false,
  pencilDraws: readSettings().pencilDraws ?? true,
  toast: null,
  // Tapping the active pen / marker again toggles its colour palette.
  setTool: (tool) => {
    const ink = tool === 'pen' || tool === 'marker';
    const palette = ink ? (get().tool === tool ? !get().palette : true) : false;
    set({ tool, palette, menu: null, pendingString: null });
  },
  set: (patch) => set(patch),
  bumpLayout: () => {
    if (layoutFrame) return;
    layoutFrame = requestAnimationFrame(() => { layoutFrame = 0; set({ layoutVersion: get().layoutVersion + 1 }); });
  },
  showToast: (text) => set({ toast: { text, id: ++toastId } }),
}));

/** a dialog to reopen after the board remounts (signing in reloads progress from the cloud and rebuilds the board) */
// the board may be rebuilt more than once while the new account's progress loads: keep the request for a short while
let reopen: { patch: Partial<UiState>; until: number } | null = null;
export const reopenAfterRemount = (patch: Partial<UiState> | null) => { reopen = patch ? { patch, until: Date.now() + 15000 } : null; };
export const takeReopen = () => (reopen && reopen.until > Date.now() ? reopen.patch : null);

export const resetUi = () => useUi.setState({
  tool: 'move', palette: false, panel: null, indexOpen: false, menu: null, pendingString: null, dialog: null, beatStage: null, tourStep: null, toast: null,
});
