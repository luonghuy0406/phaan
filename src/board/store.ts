// Board progress for one case, persisted to IndexedDB (ink can be large; localStorage caps at ~5 MB on iPad).
import { createStore, type StoreApi } from 'zustand/vanilla';
import { persist, createJSONStorage, type StateStorage } from 'zustand/middleware';
import { get as idbGet, set as idbSet, del as idbDel } from 'idb-keyval';
import type { CaseData, CheckResult, Question } from '../lib/types';
import { check, normalizeLine } from '../lib/checks.js';
import { pad3 } from '../lib/data';
import type { Stroke } from './ink';
import type { Cam } from './camera';

export interface DocPos { x: number; y: number; z: number; r: number }
export interface Note { id: string; x: number; y: number; z: number; text: string; c?: number }
export type End = { doc: string; key?: string } | { note: string };
export interface Str { id: string; a: End; b: End }
export interface QState { solved: boolean; hints: number; tries: number; line: string; pick: number[] }
export interface Entry { id: string; kind: 'text' | 'quote'; text: string; ref?: { doc: string; key: string }; at: number }

export interface BoardData {
  docs: Record<string, DocPos>;
  notes: Note[];
  strings: Str[];
  hl: string[];
  ink: Stroke[];
  pins: (string | null)[];
  q: Record<string, QState>;
  notebook: Entry[];
  cam: (Cam & { w: number; h: number }) | null;
  seenIntro: boolean;
  startedAt: number;
  savedAt: number; // last real change (not camera moves); newer side wins when syncing with the cloud
}

type InkOp = { add?: Stroke[]; remove?: Stroke[] };

export interface BoardState extends BoardData {
  past: InkOp[];
  future: InkOp[];
  feedback: Record<string, CheckResult>;
  // layout
  initLayout: (defaults: Record<string, { x: number; y: number; r: number }>) => void;
  placeItem: (kind: 'doc' | 'note', id: string, x: number, y: number) => void;
  raise: (kind: 'doc' | 'note', id: string) => void;
  rotateDoc: (id: string, back?: boolean) => void;
  relayout: (defaults: Record<string, { x: number; y: number; r: number }>) => void;
  // notes
  addNote: (x: number, y: number) => string;
  setNote: (id: string, patch: Partial<Pick<Note, 'text' | 'c'>>) => void;
  deleteNote: (id: string) => void;
  // strings + highlights
  addString: (a: End, b: End) => boolean;
  removeString: (id: string) => void;
  toggleHl: (key: string) => void;
  // ink
  addStroke: (s: Stroke) => void;
  eraseStrokes: (ids: string[]) => void;
  undo: () => void;
  redo: () => void;
  // questions
  togglePin: (doc: string, need: number) => 'pinned' | 'unpinned' | 'full';
  setPin: (slot: number, doc: string | null, need: number) => void;
  setLine: (qid: string, ref: string) => void;
  setPick: (qid: string, pick: number[]) => void;
  useHint: (qid: string) => void;
  submit: (qid: string) => CheckResult | null;
  // notebook
  addEntry: (e: Omit<Entry, 'id' | 'at'>) => string;
  setEntry: (id: string, text: string) => void;
  deleteEntry: (id: string) => void;
  // misc
  saveCam: (cam: Cam, w: number, h: number) => void;
  setSeenIntro: () => void;
}

export const LIMITS = { notes: 80, noteText: 1000, strings: 150, hl: 800, strokes: 4000, strokePts: 9000, entries: 300, entryText: 4000 };
export const NOTE_COLORS = ['#f3d76b', '#f6b7c6', '#b9e2c4'];
export const uid = (p: string) => p + Math.random().toString(36).slice(2, 10);

const num = (v: unknown, d = 0) => (Number.isFinite(Number(v)) ? Number(v) : d);
const clampN = (v: unknown, a: number, b: number, d = 0) => Math.min(b, Math.max(a, num(v, d)));

/* ── storage: IndexedDB with a debounced writer (persist fires on every drag frame) ── */
const pending = new Map<string, string>();
let flushTimer = 0;
async function writeOut() {
  window.clearTimeout(flushTimer);
  flushTimer = 0;
  const items = [...pending.entries()];
  pending.clear();
  for (const [k, v] of items) {
    try { await idbSet(k, v); } catch { try { localStorage.setItem(k, v); } catch { /* storage full or blocked */ } }
  }
}
export const flushStorage = () => { if (pending.size) void writeOut(); };
if (typeof window !== 'undefined') {
  window.addEventListener('pagehide', flushStorage);
  document.addEventListener('visibilitychange', () => { if (document.hidden) flushStorage(); });
}
const idbStorage: StateStorage = {
  getItem: async (name) => {
    try {
      const v = await idbGet<string>(name);
      if (v != null) return v;
    } catch { /* IndexedDB blocked: fall back */ }
    try { return localStorage.getItem(name); } catch { return null; }
  },
  setItem: (name, value) => {
    pending.set(name, value);
    if (!flushTimer) flushTimer = window.setTimeout(() => { void writeOut(); }, 400);
  },
  removeItem: async (name) => {
    pending.delete(name);
    try { await idbDel(name); } catch { /* ignore */ }
    try { localStorage.removeItem(name); } catch { /* ignore */ }
  },
};

/* ── stage helpers ── */
export const isSolved = (s: BoardData, q: Question) => Boolean(s.q[q.id]?.solved);
export const stageOpen = (c: CaseData, s: BoardData, n: number) => c.questions.every((q) => (q.stage ?? 1) >= n || isSolved(s, q));
export const currentQ = (c: CaseData, s: BoardData) => c.questions.find((q) => !isSolved(s, q) && stageOpen(c, s, q.stage ?? 1)) ?? null;
export const allSolved = (c: CaseData, s: BoardData) => c.questions.length > 0 && c.questions.every((q) => isSolved(s, q));
export const evidenceNeed = (q: Question) => q.need || (q.answer || []).length || 2;

function emptyData(c: CaseData): BoardData {
  const q: Record<string, QState> = {};
  c.questions.forEach((x) => { q[x.id] = { solved: false, hints: 0, tries: 0, line: '', pick: [] }; });
  return { docs: {}, notes: [], strings: [], hl: [], ink: [], pins: [], q, notebook: [], cam: null, seenIntro: false, startedAt: Date.now(), savedAt: 0 };
}

// Saved boards come from storage, so treat them as untrusted input.
export function sanitize(raw: unknown, c: CaseData): BoardData {
  const src = (raw && typeof raw === 'object' ? raw : {}) as Partial<Record<keyof BoardData, unknown>>;
  const out = emptyData(c);
  const docIds = new Set(c.documents.map((d) => d.id));
  const lineIds = new Set<string>();
  c.documents.forEach((d) => (d.lines || []).forEach((l) => lineIds.add(`${d.id}:${pad3(l.n)}`)));

  Object.entries((src.docs as Record<string, DocPos>) || {}).forEach(([id, d]) => {
    if (!docIds.has(id) || !d || typeof d !== 'object') return;
    out.docs[id] = { x: clampN(d.x, -1e5, 1e5), y: clampN(d.y, -1e5, 1e5), z: Math.round(clampN(d.z, 1, 1e6, 1)), r: Math.round(clampN(d.r, 0, 3)) };
  });
  out.notes = (Array.isArray(src.notes) ? src.notes : []).slice(0, LIMITS.notes)
    .filter((n): n is Note => n && /^n[a-z0-9]{1,16}$/.test(n.id))
    .map((n) => ({ id: n.id, x: clampN(n.x, -1e5, 1e5), y: clampN(n.y, -1e5, 1e5), z: Math.round(clampN(n.z, 1, 1e6, 1)), text: String(n.text || '').slice(0, LIMITS.noteText), c: Math.round(clampN(n.c, 0, NOTE_COLORS.length - 1)) }));
  const noteIds = new Set(out.notes.map((n) => n.id));
  const okEnd = (e: unknown): e is End => {
    if (!e || typeof e !== 'object') return false;
    const x = e as { doc?: string; note?: string; key?: unknown };
    return (docIds.has(x.doc ?? '') || noteIds.has(x.note ?? '')) && (x.key == null || /^[a-z0-9-]{1,24}$/.test(String(x.key)));
  };
  const cleanEnd = (e: End): End => ('note' in e ? { note: e.note } : { doc: e.doc, ...(e.key ? { key: e.key } : {}) });
  out.strings = (Array.isArray(src.strings) ? src.strings : []).slice(0, LIMITS.strings)
    .filter((s): s is Str => s && /^s[a-z0-9]{1,16}$/.test(s.id) && okEnd(s.a) && okEnd(s.b))
    .map((s) => ({ id: s.id, a: cleanEnd(s.a), b: cleanEnd(s.b) }));
  out.hl = [...new Set((Array.isArray(src.hl) ? src.hl : []).filter((k): k is string => typeof k === 'string' && /^[a-z0-9-]+:[a-z0-9-]{1,24}$/.test(k) && docIds.has(k.split(':')[0])))].slice(0, LIMITS.hl);
  const okTarget = (t: unknown) => t === 'world' || (typeof t === 'string' && ((t.startsWith('doc:') && docIds.has(t.slice(4))) || (t.startsWith('note:') && noteIds.has(t.slice(5)))));
  out.ink = (Array.isArray(src.ink) ? src.ink : []).slice(-LIMITS.strokes)
    .filter((s): s is Stroke => s && /^k[a-z0-9]{1,16}$/.test(s.id) && okTarget(s.t) && Array.isArray(s.pts) && s.pts.length >= 3 && s.pts.length % 3 === 0
      && s.pts.length <= LIMITS.strokePts && s.pts.every((v: unknown) => Number.isFinite(v)) && /^#[0-9a-f]{6}$/i.test(s.c))
    .map((s) => ({ id: s.id, t: s.t, pts: s.pts, c: s.c, s: clampN(s.s, 0.5, 120, 3), ...(s.m ? { m: 1 as const } : {}), ...(s.p ? { p: 1 as const } : {}) }));
  out.pins = (Array.isArray(src.pins) ? src.pins : []).slice(0, 6).map((p) => (typeof p === 'string' && docIds.has(p) ? p : null));
  let reachable = true; // questions are solved in order
  const srcQ = (src.q && typeof src.q === 'object' ? src.q : {}) as Record<string, Partial<QState>>;
  c.questions.forEach((question) => {
    const s = srcQ[question.id] || {};
    const line = normalizeLine(s.line);
    out.q[question.id] = {
      solved: reachable && Boolean(s.solved),
      hints: Math.round(clampN(s.hints, 0, (question.hints || []).length)),
      tries: Math.round(clampN(s.tries, 0, 9999)),
      line: lineIds.has(line) ? line : '',
      pick: (Array.isArray(s.pick) ? s.pick : []).map(Number).filter((n) => Number.isInteger(n) && n >= 0 && n < 20),
    };
    if (!out.q[question.id].solved) reachable = false;
  });
  out.notebook = (Array.isArray(src.notebook) ? src.notebook : []).slice(0, LIMITS.entries)
    .filter((e): e is Entry => e && /^e[a-z0-9]{1,16}$/.test(e.id) && (e.kind === 'text' || e.kind === 'quote'))
    .map((e) => ({
      id: e.id, kind: e.kind, text: String(e.text || '').slice(0, LIMITS.entryText), at: num(e.at, Date.now()),
      ...(e.ref && docIds.has(e.ref.doc) && /^[a-z0-9-]{1,24}$/.test(e.ref.key) ? { ref: { doc: e.ref.doc, key: e.ref.key } } : {}),
    }));
  const cam = src.cam as BoardData['cam'];
  out.cam = cam && typeof cam === 'object'
    ? { x: num(cam.x), y: num(cam.y), z: clampN(cam.z, 0.05, 5, 0.5), w: num(cam.w), h: num(cam.h) }
    : null;
  out.seenIntro = Boolean(src.seenIntro);
  out.startedAt = num(src.startedAt) || Date.now();
  out.savedAt = Math.max(0, num(src.savedAt));
  return out;
}

const DATA_KEYS: (keyof BoardData)[] = ['docs', 'notes', 'strings', 'hl', 'ink', 'pins', 'q', 'notebook', 'cam', 'seenIntro', 'startedAt', 'savedAt'];
// changes that count as progress (camera moves do not)
const PROGRESS_KEYS: (keyof BoardData)[] = ['docs', 'notes', 'strings', 'hl', 'ink', 'pins', 'q', 'notebook', 'seenIntro'];

export const snapshot = (s: BoardData): BoardData => Object.fromEntries(DATA_KEYS.map((k) => [k, s[k]])) as unknown as BoardData;
export const solvedCount = (c: CaseData, s: BoardData) => c.questions.filter((q) => isSolved(s, q)).length;

export type BoardStore = StoreApi<BoardState> & { persist: { hasHydrated: () => boolean; onFinishHydration: (fn: () => void) => () => void; clearStorage: () => void } };

const stores = new Map<string, BoardStore>();

// Progress is tied to the case's structure (ids, rounds, answers), not its wording: restructuring a case
// starts fresh instead of mapping old answers onto new questions, while typo fixes keep progress.
export function fingerprint(c: CaseData): string {
  const shape = JSON.stringify([
    c.documents.map((d) => [d.id, d.stage ?? 1, d.type]),
    c.questions.map((q) => [q.id, q.stage ?? 1, q.type, q.answer]),
  ]);
  let h = 2166136261;
  for (let i = 0; i < shape.length; i++) { h ^= shape.charCodeAt(i); h = Math.imul(h, 16777619); }
  return (h >>> 0).toString(36);
}
// scope: a room id gives each room its own desk (layout, ink, notes), separate from solo play
const keyFor = (c: CaseData, scope = '') => `hsm:board:${c.id}:${fingerprint(c)}${scope ? `:${scope}` : ''}`;

export function getBoardStore(c: CaseData, scope = ''): BoardStore {
  const cacheKey = `${c.id}|${scope}`;
  const hit = stores.get(cacheKey);
  if (hit) return hit;
  const store = createStore<BoardState>()(persist((set, get) => {
    const maxZ = () => Math.max(1, ...Object.values(get().docs).map((d) => d.z), ...get().notes.map((n) => n.z));
    const qOf = (qid: string) => c.questions.find((q) => q.id === qid);
    const touchQ = (qid: string, patch: Partial<QState>) => {
      const { [qid]: _gone, ...feedback } = get().feedback;
      set({ q: { ...get().q, [qid]: { ...get().q[qid], ...patch } }, feedback });
    };
    const fitPins = (need: number) => {
      const pins = get().pins.slice(0, need);
      while (pins.length < need) pins.push(null);
      return pins;
    };
    const clearPinFeedback = () => {
      const cur = currentQ(c, get());
      if (cur) { const { [cur.id]: _gone, ...feedback } = get().feedback; set({ feedback }); }
    };

    return {
      ...emptyData(c),
      past: [],
      future: [],
      feedback: {},

      initLayout: (defaults) => {
        const docs = { ...get().docs };
        let changed = false;
        Object.entries(defaults).forEach(([id, p]) => {
          if (!docs[id]) { docs[id] = { x: p.x, y: p.y, z: 1, r: p.r }; changed = true; }
        });
        if (changed) set({ docs });
      },
      placeItem: (kind, id, x, y) => {
        if (kind === 'doc') {
          const d = get().docs[id];
          if (d) set({ docs: { ...get().docs, [id]: { ...d, x: Math.round(x), y: Math.round(y) } } });
        } else {
          set({ notes: get().notes.map((n) => (n.id === id ? { ...n, x: Math.round(x), y: Math.round(y) } : n)) });
        }
      },
      raise: (kind, id) => {
        const top = maxZ();
        if (kind === 'doc') {
          const d = get().docs[id];
          if (d && d.z < top) set({ docs: { ...get().docs, [id]: { ...d, z: top + 1 } } });
        } else {
          const n = get().notes.find((x) => x.id === id);
          if (n && n.z < top) set({ notes: get().notes.map((x) => (x.id === id ? { ...x, z: top + 1 } : x)) });
        }
      },
      rotateDoc: (id, back) => {
        const d = get().docs[id];
        if (d) set({ docs: { ...get().docs, [id]: { ...d, r: (d.r + (back ? 3 : 1)) % 4 } } });
      },
      relayout: (defaults) => {
        const docs = { ...get().docs };
        Object.entries(defaults).forEach(([id, p]) => { docs[id] = { ...(docs[id] || { z: 1 }), x: p.x, y: p.y, r: p.r }; });
        set({ docs });
      },

      addNote: (x, y) => {
        const id = uid('n');
        if (get().notes.length >= LIMITS.notes) return '';
        set({ notes: [...get().notes, { id, x: Math.round(x), y: Math.round(y), z: maxZ() + 1, text: '', c: 0 }] });
        return id;
      },
      setNote: (id, patch) => set({ notes: get().notes.map((n) => (n.id === id ? { ...n, ...patch, text: String(patch.text ?? n.text).slice(0, LIMITS.noteText) } : n)) }),
      deleteNote: (id) => set({
        notes: get().notes.filter((n) => n.id !== id),
        strings: get().strings.filter((s) => !('note' in s.a && s.a.note === id) && !('note' in s.b && s.b.note === id)),
        ink: get().ink.filter((k) => k.t !== `note:${id}`),
      }),

      addString: (a, b) => {
        const same = JSON.stringify(a) === JSON.stringify(b);
        if (same || get().strings.length >= LIMITS.strings) return false;
        set({ strings: [...get().strings, { id: uid('s'), a, b }] });
        return true;
      },
      removeString: (id) => set({ strings: get().strings.filter((s) => s.id !== id) }),
      toggleHl: (key) => {
        const hl = get().hl;
        set({ hl: hl.includes(key) ? hl.filter((k) => k !== key) : [...hl, key].slice(-LIMITS.hl) });
      },

      addStroke: (s) => set({ ink: [...get().ink, s].slice(-LIMITS.strokes), past: [...get().past, { add: [s] }].slice(-200), future: [] }),
      eraseStrokes: (ids) => {
        if (!ids.length) return;
        const gone = get().ink.filter((s) => ids.includes(s.id));
        set({ ink: get().ink.filter((s) => !ids.includes(s.id)), past: [...get().past, { remove: gone }].slice(-200), future: [] });
      },
      undo: () => {
        const op = get().past[get().past.length - 1];
        if (!op) return;
        const addIds = new Set((op.add || []).map((s) => s.id));
        set({ ink: [...get().ink.filter((s) => !addIds.has(s.id)), ...(op.remove || [])], past: get().past.slice(0, -1), future: [...get().future, op] });
      },
      redo: () => {
        const op = get().future[get().future.length - 1];
        if (!op) return;
        const removeIds = new Set((op.remove || []).map((s) => s.id));
        set({ ink: [...get().ink.filter((s) => !removeIds.has(s.id)), ...(op.add || [])], future: get().future.slice(0, -1), past: [...get().past, op] });
      },

      togglePin: (doc, need) => {
        const pins = fitPins(need);
        const at = pins.indexOf(doc);
        if (at >= 0) { pins[at] = null; set({ pins }); clearPinFeedback(); return 'unpinned'; }
        const free = pins.indexOf(null);
        if (free < 0) return 'full';
        pins[free] = doc;
        set({ pins });
        clearPinFeedback();
        return 'pinned';
      },
      setPin: (slot, doc, need) => {
        let pins = fitPins(need);
        if (doc) pins = pins.map((p, i) => (p === doc && i !== slot ? null : p));
        pins[slot] = doc;
        set({ pins });
        clearPinFeedback();
      },
      setLine: (qid, ref) => touchQ(qid, { line: normalizeLine(ref) }),
      setPick: (qid, pick) => touchQ(qid, { pick }),
      useHint: (qid) => {
        const q = qOf(qid);
        const s = get().q[qid];
        if (q && s) set({ q: { ...get().q, [qid]: { ...s, hints: Math.min((q.hints || []).length, s.hints + 1) } } });
      },
      submit: (qid) => {
        const q = qOf(qid);
        const s = get().q[qid];
        if (!q || !s || q !== currentQ(c, get())) return null;
        const input = q.type === 'evidence' ? get().pins.filter((p): p is string => Boolean(p)) : q.type === 'line' ? s.line : s.pick;
        const result = check(q, input);
        const next: QState = { ...s, tries: s.tries + (result.status === 'incomplete' ? 0 : 1), solved: result.status === 'correct' };
        set({
          q: { ...get().q, [qid]: next },
          feedback: { ...get().feedback, [qid]: result },
          ...(result.status === 'correct' && q.type === 'evidence' ? { pins: [] } : {}),
        });
        return result;
      },

      addEntry: (e) => {
        const id = uid('e');
        set({ notebook: [...get().notebook, { ...e, id, at: Date.now(), text: e.text.slice(0, LIMITS.entryText) }].slice(-LIMITS.entries) });
        return id;
      },
      setEntry: (id, text) => set({ notebook: get().notebook.map((e) => (e.id === id ? { ...e, text: text.slice(0, LIMITS.entryText) } : e)) }),
      deleteEntry: (id) => set({ notebook: get().notebook.filter((e) => e.id !== id) }),

      saveCam: (cam, w, h) => set({ cam: { x: cam.x, y: cam.y, z: cam.z, w, h } }),
      setSeenIntro: () => set({ seenIntro: true }),
    };
  }, {
    name: keyFor(c, scope),
    version: 2,
    storage: createJSONStorage(() => idbStorage),
    partialize: (s) => Object.fromEntries(DATA_KEYS.map((k) => [k, s[k]])) as unknown as BoardState,
    merge: (persisted, current) => ({ ...current, ...sanitize(persisted, c) }),
  })) as BoardStore;
  store.subscribe((s, prev) => {
    if (s.savedAt !== prev.savedAt) return; // hydration or a cloud copy being applied
    if (PROGRESS_KEYS.some((k) => s[k] !== prev[k])) store.setState({ savedAt: Date.now() });
  });
  stores.set(cacheKey, store);
  return store;
}

export async function resetBoard(c: CaseData, scope = '') {
  const store = stores.get(`${c.id}|${scope}`);
  pending.delete(keyFor(c, scope));
  await idbStorage.removeItem(keyFor(c, scope));
  if (store) {
    store.setState({ ...emptyData(c), past: [], future: [], feedback: {} });
    pending.delete(keyFor(c, scope)); // the reset itself triggered a write
    await idbStorage.removeItem(keyFor(c, scope));
  }
}
