// Main-thread side of the on-device Supertonic voice: picks the model variant for this device, owns the worker,
// reports download progress, and tells whether the model is already on this device.
import { MODEL_REPO, MODEL_REVISION, VOICES, encodeWav, variantFiles, variantBytes, type Variant } from './core';
import type { InMsg, OutMsg } from './worker';

export { VOICES };
export const CACHE_NAME = `hsm-tts-supertonic3-${MODEL_REVISION.slice(0, 8)}`;
// VITE_TTS_MODEL_BASE can point at a mirror of the official files (e.g. a local folder while developing)
export const modelBase = () =>
  ((import.meta.env.VITE_TTS_MODEL_BASE as string | undefined) || `https://huggingface.co/${MODEL_REPO}/resolve/${MODEL_REVISION}/`).replace(/\/?$/, '/');
// Optimized fp16 / int8 graphs (folders fp16/ and int8/). Without it every device downloads the official fp32 graphs.
export const optimizedBase = () => ((import.meta.env.VITE_TTS_MODEL_OPT_BASE as string | undefined) || '').replace(/\/?$/, (m) => (m ? '/' : ''));

export const onDeviceSupported = () =>
  typeof WebAssembly === 'object' && typeof Worker === 'function' && typeof caches === 'object';

/* ── which graphs suit this device ── */
export interface Plan { variant: Variant; backend: 'webgpu' | 'wasm' }
let planP: Promise<Plan> | null = null;
export function devicePlan(): Promise<Plan> {
  if (!planP) {
    planP = (async () => {
      const opt = Boolean(optimizedBase());
      let adapter: { features: { has(f: string): boolean } } | null = null;
      try {
        const gpu = (navigator as Navigator & { gpu?: { requestAdapter(): Promise<typeof adapter> } }).gpu;
        adapter = gpu ? await gpu.requestAdapter() : null;
      } catch { adapter = null; }
      if (adapter) return { variant: opt && adapter.features.has('shader-f16') ? 'fp16' : 'fp32', backend: 'webgpu' };
      return { variant: opt ? 'int8' : 'fp32', backend: 'wasm' };
    })();
  }
  return planP;
}
/** Download size for this device (bytes). */
export async function modelBytes(): Promise<number> { return variantBytes((await devicePlan()).variant); }

let worker: Worker | null = null;
let ready: Promise<string> | null = null;
let nextId = 1;
const pending = new Map<number, { resolve: (b: Blob) => void; reject: (e: Error) => void }>();

function getWorker(): Worker {
  if (!worker) {
    worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' });
    worker.addEventListener('message', (e: MessageEvent<OutMsg>) => {
      const m = e.data;
      if (m.type === 'audio') {
        const p = pending.get(m.id);
        pending.delete(m.id);
        p?.resolve(new Blob([encodeWav(m.pcm, m.sampleRate)], { type: 'audio/wav' }));
      } else if (m.type === 'error' && m.id != null) {
        const p = pending.get(m.id);
        pending.delete(m.id);
        p?.reject(new Error(m.message));
      }
    });
  }
  return worker;
}

const fileUrl = (plan: Plan, f: { path: string; opt: boolean }) => (f.opt ? `${optimizedBase()}${plan.variant}/` : modelBase()) + f.path;

/** True when every model file for this device is already in this browser (no download needed). */
export async function isModelCached(voice: string): Promise<boolean> {
  if (!onDeviceSupported()) return false;
  try {
    if (!(await caches.has(CACHE_NAME))) return false; // don't create an empty cache just by checking
    const cache = await caches.open(CACHE_NAME);
    const plan = await devicePlan();
    const urls = [...variantFiles(plan.variant).map((f) => fileUrl(plan, f)), `${modelBase()}voice_styles/${voice}.json`];
    const hits = await Promise.all(urls.map((u) => cache.match(u)));
    return hits.every(Boolean);
  } catch { return false; }
}

export type Progress = { phase: 'download' | 'load'; loaded: number; total: number };

/** Download (if needed) and load the model. Resolves with the backend in use, e.g. "webgpu · fp16". */
export function ensureModel(voice: string, onProgress: (p: Progress) => void): Promise<string> {
  if (ready) return ready;
  const w = getWorker();
  ready = devicePlan().then((plan) => new Promise<string>((resolve, reject) => {
    const onMsg = (e: MessageEvent<OutMsg>) => {
      const m = e.data;
      if (m.type === 'progress') onProgress(m);
      else if (m.type === 'ready') { w.removeEventListener('message', onMsg); resolve(m.backend); }
      else if (m.type === 'error' && m.id == null) { w.removeEventListener('message', onMsg); ready = null; reject(new Error(m.message)); }
    };
    w.addEventListener('message', onMsg);
    // keep the model even when the device runs low on space (best effort)
    void navigator.storage?.persist?.().catch(() => false);
    w.postMessage({ type: 'init', officialBase: modelBase(), optBase: optimizedBase(), variant: plan.variant, backend: plan.backend, cacheName: CACHE_NAME, voice } satisfies InMsg);
  }));
  return ready;
}

/** Compile kernels / pipelines with a tiny utterance so the first real line is not slow. */
export function warmUp() { if (ready) void ready.then(() => getWorker().postMessage({ type: 'warm' } satisfies InMsg)).catch(() => {}); }

/** Text → WAV blob, synthesized in the worker. */
export function synthesize(text: string, opts: { lang: string; steps: number; speed: number; voice?: string }): Promise<Blob> {
  const id = nextId++;
  return new Promise<Blob>((resolve, reject) => {
    pending.set(id, { resolve, reject });
    getWorker().postMessage({ type: 'synth', id, text, ...opts } satisfies InMsg);
  });
}

/** Remove the downloaded model from this device. */
export async function deleteModel() {
  worker?.terminate();
  worker = null;
  ready = null;
  pending.forEach((p) => p.reject(new Error('Đã xoá giọng đọc')));
  pending.clear();
  try { await caches.delete(CACHE_NAME); } catch { /* ignore */ }
}

export async function storageInfo(): Promise<{ free: number | null }> {
  try {
    const e = await navigator.storage?.estimate?.();
    return { free: e?.quota != null && e.usage != null ? e.quota - e.usage : null };
  } catch { return { free: null }; }
}
