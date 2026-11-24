// Main-thread side of the on-device Supertonic voice: owns the worker, reports download progress,
// and tells whether the model is already on this device.
import { MODEL_FILES, MODEL_REPO, MODEL_REVISION, MODEL_BYTES, VOICES, encodeWav } from './core';
import type { InMsg, OutMsg } from './worker';

export { MODEL_BYTES, VOICES };
export const CACHE_NAME = `hsm-tts-supertonic3-${MODEL_REVISION.slice(0, 8)}`;
// VITE_TTS_MODEL_BASE can point at a mirror (e.g. a local folder while developing)
export const modelBase = () =>
  ((import.meta.env.VITE_TTS_MODEL_BASE as string | undefined) || `https://huggingface.co/${MODEL_REPO}/resolve/${MODEL_REVISION}/`).replace(/\/?$/, '/');

export const onDeviceSupported = () =>
  typeof WebAssembly === 'object' && typeof Worker === 'function' && typeof caches === 'object';

let worker: Worker | null = null;
let ready: Promise<string> | null = null;
let readyVoice = '';
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

/** True when every model file is already in this browser (no download needed). */
export async function isModelCached(voice: string): Promise<boolean> {
  if (!onDeviceSupported()) return false;
  try {
    if (!(await caches.has(CACHE_NAME))) return false; // don't create an empty cache just by checking
    const cache = await caches.open(CACHE_NAME);
    const base = modelBase();
    const paths = [...MODEL_FILES.map((f) => f.path), `voice_styles/${voice}.json`];
    const hits = await Promise.all(paths.map((p) => cache.match(base + p)));
    return hits.every(Boolean);
  } catch { return false; }
}

export type Progress = { phase: 'download' | 'load'; loaded: number; total: number };

/** Download (if needed) and load the model. Resolves with the backend in use ("webgpu" | "wasm"). */
export function ensureModel(voice: string, onProgress: (p: Progress) => void): Promise<string> {
  if (ready && readyVoice === voice) return ready;
  readyVoice = voice;
  const w = getWorker();
  ready = new Promise<string>((resolve, reject) => {
    const onMsg = (e: MessageEvent<OutMsg>) => {
      const m = e.data;
      if (m.type === 'progress') onProgress(m);
      else if (m.type === 'ready') { w.removeEventListener('message', onMsg); resolve(m.backend); }
      else if (m.type === 'error' && m.id == null) { w.removeEventListener('message', onMsg); ready = null; reject(new Error(m.message)); }
    };
    w.addEventListener('message', onMsg);
    // keep the model even when the device runs low on space (best effort)
    void navigator.storage?.persist?.().catch(() => false);
    w.postMessage({ type: 'init', base: modelBase(), cacheName: CACHE_NAME, voice } satisfies InMsg);
  });
  return ready;
}

/** Text → WAV blob, synthesized in the worker. */
export function synthesize(text: string, opts: { lang: string; steps: number; speed: number }): Promise<Blob> {
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
  readyVoice = '';
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
