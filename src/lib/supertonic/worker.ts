/// <reference lib="webworker" />
// Supertonic in a Web Worker: downloads the chosen model variant once into Cache Storage (with progress),
// loads it into onnxruntime-web and synthesizes speech off the main thread so the board never stutters.
// Speed (see https://onnxruntime.ai/docs/performance/): fp16 graphs on WebGPU with the latent kept on the GPU between
// denoising steps, or int8 graphs on multi-threaded WebAssembly (needs cross-origin isolation for threads).
import * as ort from 'onnxruntime-web/webgpu';
import { ONNX_NAMES, VOICE_BYTES, makeStyle, synthesizeOne, tightenSilence, variantFiles, type Models, type Style, type OrtModule, type OrtSession, type Variant } from './core';

declare const self: DedicatedWorkerGlobalScope;

// only real errors in the console (the "some nodes were not assigned to the preferred EP" notice is expected with WebGPU)
ort.env.logLevel = 'error';
ort.env.wasm.numThreads = self.crossOriginIsolated ? Math.max(1, Math.min(4, (navigator.hardwareConcurrency || 2) - 1)) : 1;

export type InMsg =
  | { type: 'init'; officialBase: string; optBase: string; variant: Variant; backend: 'webgpu' | 'wasm'; cacheName: string; voice: string }
  | { type: 'synth'; id: number; text: string; lang: string; steps: number; speed: number; voice?: string }
  | { type: 'warm' };
export type OutMsg =
  | { type: 'progress'; phase: 'download' | 'load'; loaded: number; total: number }
  | { type: 'ready'; backend: string }
  | { type: 'audio'; id: number; pcm: Float32Array; sampleRate: number; duration: number }
  | { type: 'error'; id?: number; message: string };

const post = (m: OutMsg, transfer: Transferable[] = []) => self.postMessage(m, transfer);

let models: Models | null = null;
let backend = 'wasm';
let officialBase = '';
let cacheName = '';
const styles = new Map<string, Style>();

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

function session(bytes: Uint8Array, providers: string[], keepOnGpu: boolean): Promise<OrtSession> {
  return ort.InferenceSession.create(bytes, {
    executionProviders: providers,
    graphOptimizationLevel: 'all',
    enableMemPattern: true,
    executionMode: 'sequential',
    logSeverityLevel: 3,
    // outputs that only feed the next graph stay in GPU memory (no copy back to the CPU)
    ...(keepOnGpu ? { preferredOutputLocation: 'gpu-buffer' as const } : {}),
  }) as unknown as Promise<OrtSession>;
}

async function style(voice: string): Promise<Style> {
  const hit = styles.get(voice);
  if (hit) return hit;
  const cache = await caches.open(cacheName);
  const url = `${officialBase}voice_styles/${voice}.json`;
  await fetchToCache(cache, url, () => {});
  const s = makeStyle(ort as unknown as OrtModule, await (await cache.match(url))!.json());
  styles.set(voice, s);
  return s;
}

async function init(msg: Extract<InMsg, { type: 'init' }>) {
  officialBase = msg.officialBase;
  cacheName = msg.cacheName;
  const cache = await caches.open(cacheName);
  const files = variantFiles(msg.variant).map((f) => ({ ...f, url: (f.opt ? `${msg.optBase}${msg.variant}/` : officialBase) + f.path }));
  const total = files.reduce((n, f) => n + f.bytes, 0) + VOICE_BYTES;
  let loaded = 0;
  for (const f of files) if (await cache.match(f.url)) loaded += f.bytes;
  let last = 0;
  const tick = (n: number) => {
    loaded += n;
    const now = performance.now();
    if (now - last > 150) { last = now; post({ type: 'progress', phase: 'download', loaded, total }); }
  };
  for (const f of files) await fetchToCache(cache, f.url, tick);
  await fetchToCache(cache, `${officialBase}voice_styles/${msg.voice}.json`, tick);
  post({ type: 'progress', phase: 'download', loaded: total, total });

  if (!models) {
    post({ type: 'progress', phase: 'load', loaded: 0, total: 4 });
    const url = (p: string) => files.find((f) => f.path === p)!.url;
    const [cfg, indexer] = await Promise.all([
      cache.match(url('onnx/tts.json')).then((r) => r!.json()),
      cache.match(url('onnx/unicode_indexer.json')).then((r) => r!.json()),
    ]);
    const create = async (providers: string[], gpu: boolean) => {
      const out: OrtSession[] = [];
      for (let i = 0; i < ONNX_NAMES.length; i++) {
        const name = ONNX_NAMES[i];
        // text_encoder and vector_estimator outputs are consumed on the GPU; durations and audio are read on the CPU
        const keep = gpu && (name === 'text_encoder' || name === 'vector_estimator');
        out.push(await session(await readBytes(cache, url(`onnx/${name}.onnx`)), providers, keep));
        post({ type: 'progress', phase: 'load', loaded: i + 1, total: 4 });
      }
      return out;
    };
    let sessions: OrtSession[];
    try {
      if (msg.backend !== 'webgpu') throw new Error('wasm requested');
      sessions = await create(['webgpu', 'wasm'], true);
      backend = 'webgpu';
    } catch {
      sessions = await create(['wasm'], false);
      backend = `wasm×${ort.env.wasm.numThreads}`;
    }
    const [dp, te, ve, voc] = sessions;
    models = { dp, te, ve, voc, cfg, indexer };
  }
  await style(msg.voice);
  post({ type: 'ready', backend: `${backend} · ${msg.variant}` });
}

let queue = Promise.resolve();
self.onmessage = (e: MessageEvent<InMsg>) => {
  const msg = e.data;
  // one job at a time: ONNX sessions are not re-entrant
  queue = queue.then(async () => {
    try {
      if (msg.type === 'init') await init(msg);
      else if (msg.type === 'warm') {
        // first run compiles WebGPU pipelines / allocates buffers: do it before the player is waiting
        if (models) await synthesizeOne(ort as unknown as OrtModule, models, styles.values().next().value!, 'Dạ.', { lang: 'vi', steps: 2, speed: 1 });
      } else {
        if (!models) throw new Error('Mô hình chưa sẵn sàng');
        const s = await style(msg.voice || styles.keys().next().value || 'M1');
        const r = await synthesizeOne(ort as unknown as OrtModule, models, s, msg.text, { lang: msg.lang, steps: msg.steps, speed: msg.speed });
        const pcm = tightenSilence(r.pcm, r.sampleRate).slice();
        post({ type: 'audio', id: msg.id, pcm, sampleRate: r.sampleRate, duration: pcm.length / r.sampleRate }, [pcm.buffer]);
      }
    } catch (err) {
      post({ type: 'error', id: msg.type === 'synth' ? msg.id : undefined, message: (err as Error).message || String(err) });
    }
  });
};
