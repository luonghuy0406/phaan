// Âm thanh của bàn điều tra: hiệu ứng thao tác, tiếng nền theo hồ sơ và giọng dẫn chuyện đã tạo sẵn.
// Mọi thứ đi qua một AudioContext dùng chung. iPad chỉ cho phát tiếng sau một lần chạm, nên context được
// mở khoá ở lần chạm đầu tiên (unlockAudio) và sau đó phát được ở bất kỳ lúc nào, kể cả sau hiệu ứng React.
import { create } from 'zustand';

export type Sfx = 'paper' | 'pin' | 'correct' | 'wrong' | 'hint' | 'unseal' | 'finale' | 'tick';

/** Shared effects in public/sfx/ (Kenney CC0, BigSoundBank CC0: see public/sfx/CREDITS.md). */
const B = import.meta.env.BASE_URL;
const FILES: Record<Sfx, { src: string; gain: number }> = {
  paper: { src: `${B}sfx/paper.mp3`, gain: 0.55 },
  pin: { src: `${B}sfx/pin.mp3`, gain: 0.6 },
  correct: { src: `${B}sfx/stamp.mp3`, gain: 0.9 },
  wrong: { src: `${B}sfx/wrong.mp3`, gain: 0.55 },
  hint: { src: `${B}sfx/pencil.mp3`, gain: 0.6 },
  unseal: { src: `${B}sfx/unseal.mp3`, gain: 0.75 },
  finale: { src: `${B}sfx/gong.mp3`, gain: 0.6 },
  tick: { src: `${B}sfx/tick.mp3`, gain: 0.4 },
};

interface AudioPrefs { effects: boolean; ambient: boolean; volume: number }
const PREFS_KEY = 'hsm:audio';
function readPrefs(): AudioPrefs {
  try {
    const p = JSON.parse(localStorage.getItem(PREFS_KEY) || '{}');
    return { effects: p.effects ?? true, ambient: p.ambient ?? true, volume: typeof p.volume === 'number' ? p.volume : 0.8 };
  } catch { return { effects: true, ambient: true, volume: 0.8 }; }
}

interface AudioState extends AudioPrefs {
  /** voice clip being played: its src, or null */
  voice: string | null;
  setPrefs: (p: Partial<AudioPrefs>) => void;
}

export const useAudio = create<AudioState>((set, get) => ({
  ...readPrefs(),
  voice: null,
  setPrefs: (p) => {
    set(p);
    const { effects, ambient, volume } = get();
    try { localStorage.setItem(PREFS_KEY, JSON.stringify({ effects, ambient, volume })); } catch { /* private mode */ }
    applyLevels();
  },
}));

/* ── context, buses ── */
let ctx: AudioContext | null = null;
let master: GainNode | null = null;
let ambientBus: GainNode | null = null;
let voiceBus: GainNode | null = null;

function ac(): AudioContext | null {
  if (ctx) return ctx;
  const Ctor = typeof window !== 'undefined' ? (window.AudioContext || (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext) : undefined;
  if (!Ctor) return null;
  ctx = new Ctor();
  master = ctx.createGain();
  master.connect(ctx.destination);
  ambientBus = ctx.createGain();
  ambientBus.connect(master);
  voiceBus = ctx.createGain();
  voiceBus.connect(master);
  applyLevels();
  return ctx;
}

const AMBIENT_LEVEL = 0.32;
const DUCKED = 0.08; // ambient while a voice clip plays

function applyLevels() {
  if (!ctx || !master || !ambientBus) return;
  const { volume, ambient, voice } = useAudio.getState();
  const t = ctx.currentTime;
  master.gain.setTargetAtTime(volume, t, 0.05);
  const target = !ambient ? 0 : voice ? DUCKED : AMBIENT_LEVEL;
  ambientBus.gain.setTargetAtTime(target, t, voice ? 0.25 : 0.8);
}

/** Call from a pointer / key handler: iOS keeps audio silent until a context is resumed inside a gesture. */
export function unlockAudio() {
  const c = ac();
  if (c && c.state !== 'running') void c.resume().catch(() => {});
}
if (typeof window !== 'undefined') {
  const once = () => { unlockAudio(); if (ctx?.state === 'running') { window.removeEventListener('pointerdown', once, true); window.removeEventListener('keydown', once, true); } };
  window.addEventListener('pointerdown', once, true);
  window.addEventListener('keydown', once, true);
}

/* ── buffers ── */
const buffers = new Map<string, Promise<AudioBuffer | null>>();
function load(src: string): Promise<AudioBuffer | null> {
  const c = ac();
  if (!c) return Promise.resolve(null);
  let p = buffers.get(src);
  if (!p) {
    p = fetch(src)
      .then((r) => (r.ok ? r.arrayBuffer() : Promise.reject(new Error(String(r.status)))))
      .then((b) => new Promise<AudioBuffer>((res, rej) => { c.decodeAudioData(b, res, rej); }))
      .catch(() => { buffers.delete(src); return null; });
    buffers.set(src, p);
  }
  return p;
}

/** Fetch and decode the effects ahead of time so the first stamp is not late. */
export function preloadSfx() { (Object.keys(FILES) as Sfx[]).forEach((k) => void load(FILES[k].src)); }

let lastAt: Partial<Record<Sfx, number>> = {};
export function playSfx(name: Sfx) {
  if (!useAudio.getState().effects) return;
  const c = ac();
  if (!c || !master || c.state !== 'running') return;
  const now = performance.now();
  if ((lastAt[name] ?? 0) > now - 120) return; // the same sound fired twice by one action
  lastAt = { ...lastAt, [name]: now };
  const f = FILES[name];
  void load(f.src).then((buf) => {
    if (!buf || !master) return;
    const src = c.createBufferSource();
    src.buffer = buf;
    src.playbackRate.value = name === 'paper' || name === 'pin' ? 0.94 + Math.random() * 0.12 : 1;
    const g = c.createGain();
    g.gain.value = f.gain;
    src.connect(g).connect(master);
    src.start();
  });
}

/* ── ambient loop (one per case) ── */
let ambientSrc: AudioBufferSourceNode | null = null;
let ambientUrl: string | null = null;
let ambientWanted: string | null = null;

export function setAmbient(url: string | null) {
  ambientWanted = url;
  if (url === ambientUrl && ambientSrc) return;
  stopAmbientNode();
  if (!url) return;
  const c = ac();
  if (!c) return;
  const start = () => {
    if (ambientWanted !== url || ambientSrc) return;
    void load(url).then((buf) => {
      if (!buf || ambientWanted !== url || !ambientBus || ambientSrc) return;
      const src = c.createBufferSource();
      src.buffer = buf;
      src.loop = true;
      src.connect(ambientBus);
      ambientBus.gain.setValueAtTime(0, c.currentTime);
      src.start();
      ambientSrc = src;
      ambientUrl = url;
      applyLevels(); // fades in
    });
  };
  if (c.state === 'running') start();
  else {
    // wait for the first tap
    const onState = () => { if (c.state === 'running') { c.removeEventListener('statechange', onState); start(); } };
    c.addEventListener('statechange', onState);
  }
}

function stopAmbientNode() {
  if (ambientSrc) { try { ambientSrc.stop(); } catch { /* already stopped */ } ambientSrc.disconnect(); }
  ambientSrc = null;
  ambientUrl = null;
}

/* ── narration clips ── */
let voiceSrc: AudioBufferSourceNode | null = null;

export function stopVoice() {
  if (voiceSrc) { try { voiceSrc.stop(); } catch { /* already stopped */ } voiceSrc.disconnect(); }
  voiceSrc = null;
  if (useAudio.getState().voice) { useAudio.setState({ voice: null }); applyLevels(); }
}

/** Play a pre-generated narration clip (replaces any clip already playing). Resolves when it ends or is stopped. */
export async function playVoice(url: string): Promise<void> {
  stopVoice();
  unlockAudio();
  const c = ac();
  if (!c || !voiceBus) return;
  useAudio.setState({ voice: url });
  applyLevels();
  const buf = await load(url);
  if (!buf || useAudio.getState().voice !== url) { if (useAudio.getState().voice === url) stopVoice(); return; }
  const src = c.createBufferSource();
  src.buffer = buf;
  src.connect(voiceBus);
  voiceSrc = src;
  await new Promise<void>((res) => {
    src.onended = () => res();
    src.start();
  });
  if (voiceSrc === src) stopVoice();
}

/** Stop everything when the board closes. */
export function stopAllAudio() {
  stopVoice();
  ambientWanted = null;
  stopAmbientNode();
}
