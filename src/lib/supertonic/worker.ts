/// <reference lib="webworker" />
// Supertonic in a Web Worker: downloads the model once into Cache Storage (with progress),
// loads it into onnxruntime-web (WebGPU when it works, else WebAssembly), and synthesizes speech
// off the main thread so the investigation board never stutters.
import * as ort from 'onnxruntime-web/webgpu';
import { MODEL_FILES, VOICE_BYTES, makeStyle, synthesizeOne, type Models, type Style, type OrtModule, type OrtSession } from './core';

declare const self: DedicatedWorkerGlobalScope;

// the .wasm runtime is bundled by Vite next to this worker (served from our own domain)
// only real errors in the console (the "some nodes were not assigned to the preferred EP" notice is expected with WebGPU)
ort.env.logLevel = 'error';
ort.env.wasm.numThreads = self.crossOriginIsolated ? Math.min(4, navigator.hardwareConcurrency || 2) : 1;

export type InMsg =
  | { type: 'init'; base: string; cacheName: string; voice: string }
  | { type: 'synth'; id: number; text: string; lang: string; steps: number; speed: number };
export type OutMsg =
  | { type: 'progress'; phase: 'download' | 'load'; loaded: number; total: number }
  | { type: 'ready'; backend: string }
  | { type: 'audio'; id: number; pcm: Float32Array; sampleRate: number; duration: number }
  | { type: 'error'; id?: number; message: string };

const post = (m: OutMsg, transfer: Transferable[] = []) => self.postMessage(m, transfer);

let models: Models | null = null;
let style: Style | null = null;
let backend = 'wasm';

async function fetchToCache(cache: Cache, url: string, onBytes: (n: number) => void): Promise<void> {
  if (await cache.match(url)) return;
  const res = await fetch(url, { mode: 'cors' });
  if (!res.ok || !res.body) throw new Error(`Tải ${url.split('/').pop()} thất bại (${res.status})`);
  // count bytes on one branch while the other streams straight into the cache
  const [a, b] = res.body.tee();
  const counting = (async () => {
    const reader = a.getReader();
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      onBytes(value.byteLength);
    }
  })();
  await Promise.all([cache.put(url, new Response(b, { headers: res.headers })), counting]);
}

async function readBytes(cache: Cache, url: string): Promise<Uint8Array> {
  const hit = await cache.match(url);
  if (!hit) throw new Error('Thiếu file mô hình trong bộ nhớ đệm');
  return new Uint8Array(await hit.arrayBuffer());
}

async function session(bytes: Uint8Array, providers: string[]): Promise<OrtSession> {
  return ort.InferenceSession.create(bytes, { executionProviders: providers, graphOptimizationLevel: 'all', logSeverityLevel: 3 }) as unknown as Promise<OrtSession>;
}

async function init(base: string, cacheName: string, voice: string) {
  const cache = await caches.open(cacheName);
  const files = [...MODEL_FILES.map((f) => f.path), `voice_styles/${voice}.json`];
  const total = MODEL_FILES.reduce((n, f) => n + f.bytes, 0) + VOICE_BYTES;
  let loaded = 0;
  // count what is already cached, then download the rest
  for (const f of MODEL_FILES) if (await cache.match(base + f.path)) loaded += f.bytes;
  let last = 0;
  const tick = (n: number) => {
    loaded += n;
    const now = performance.now();
    if (now - last > 150) { last = now; post({ type: 'progress', phase: 'download', loaded, total }); }
  };
  for (const path of files) await fetchToCache(cache, base + path, tick);
  post({ type: 'progress', phase: 'download', loaded: total, total });

  if (!models) {
    post({ type: 'progress', phase: 'load', loaded: 0, total: 4 });
    const [cfg, indexer] = await Promise.all([
      cache.match(base + 'onnx/tts.json').then((r) => r!.json()),
      cache.match(base + 'onnx/unicode_indexer.json').then((r) => r!.json()),
    ]);
    const names = ['duration_predictor', 'text_encoder', 'vector_estimator', 'vocoder'] as const;
    const create = async (providers: string[]) => {
      const out: OrtSession[] = [];
      for (let i = 0; i < names.length; i++) {
        out.push(await session(await readBytes(cache, `${base}onnx/${names[i]}.onnx`), providers));
        post({ type: 'progress', phase: 'load', loaded: i + 1, total: 4 });
      }
      return out;
    };
    let sessions: OrtSession[];
    const gpu = 'gpu' in navigator && Boolean(await (navigator as Navigator & { gpu: { requestAdapter(): Promise<unknown> } }).gpu.requestAdapter().catch(() => null));
    try {
      if (!gpu) throw new Error('no webgpu');
      sessions = await create(['webgpu', 'wasm']);
      backend = 'webgpu';
    } catch {
      sessions = await create(['wasm']);
      backend = 'wasm';
    }
    const [dp, te, ve, voc] = sessions;
    models = { dp, te, ve, voc, cfg, indexer };
  }
  style = makeStyle(ort as unknown as OrtModule, await (await cache.match(`${base}voice_styles/${voice}.json`))!.json());
  post({ type: 'ready', backend });
}

let queue = Promise.resolve();
self.onmessage = (e: MessageEvent<InMsg>) => {
  const msg = e.data;
  // one job at a time: ONNX sessions are not re-entrant
  queue = queue.then(async () => {
    try {
      if (msg.type === 'init') await init(msg.base, msg.cacheName, msg.voice);
      else {
        if (!models || !style) throw new Error('Mô hình chưa sẵn sàng');
        const r = await synthesizeOne(ort as unknown as OrtModule, models, style, msg.text, { lang: msg.lang, steps: msg.steps, speed: msg.speed });
        post({ type: 'audio', id: msg.id, pcm: r.pcm, sampleRate: r.sampleRate, duration: r.duration }, [r.pcm.buffer]);
      }
    } catch (err) {
      post({ type: 'error', id: msg.type === 'synth' ? msg.id : undefined, message: (err as Error).message || String(err) });
    }
  });
};
