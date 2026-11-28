// Supertonic 3 text-to-speech, ported from the official Python package (supertonic 1.3.1, core.py).
// Runtime-agnostic: pass in onnxruntime-web (browser worker) or onnxruntime-node (tests) as `ort`.
// Only type annotations here (no enums / parameter properties), so Node can import this file directly.

/* ── minimal shapes of the onnxruntime API we use ── */
export interface OrtTensor { data: unknown; dims: readonly number[]; location?: string; dispose?: () => void; getData?: () => Promise<unknown> }
export interface OrtSession {
  readonly outputNames: readonly string[];
  run(feeds: Record<string, OrtTensor>): Promise<Record<string, OrtTensor>>;
}
export interface OrtModule {
  Tensor: new (type: string, data: unknown, dims: readonly number[]) => OrtTensor;
}

export interface SupertonicConfig { ae: { sample_rate: number; base_chunk_size: number }; ttl: { chunk_compress_factor: number; latent_dim: number } }
export interface StyleJson { style_ttl: { dims: number[]; data: unknown }; style_dp: { dims: number[]; data: unknown } }
export interface Models { dp: OrtSession; te: OrtSession; ve: OrtSession; voc: OrtSession; cfg: SupertonicConfig; indexer: number[] }
export interface Style { ttl: OrtTensor; dp: OrtTensor }

export const MODEL_REVISION = '724fb5abbf5502583fb520898d45929e62f02c0b'; // pinned like the Python package
export const MODEL_REPO = 'Supertone/supertonic-3';
export const VOICES = ['F1', 'F2', 'F3', 'F4', 'F5', 'M1', 'M2', 'M3', 'M4', 'M5'] as const;
export const MODEL_FILES: { path: string; bytes: number }[] = [
  { path: 'onnx/tts.json', bytes: 8253 },
  { path: 'onnx/unicode_indexer.json', bytes: 277676 },
  { path: 'onnx/duration_predictor.onnx', bytes: 3700147 },
  { path: 'onnx/text_encoder.onnx', bytes: 36416150 },
  { path: 'onnx/vector_estimator.onnx', bytes: 256534781 },
  { path: 'onnx/vocoder.onnx', bytes: 101424195 },
];
export const VOICE_BYTES = 292000;
export const MODEL_BYTES = MODEL_FILES.reduce((n, f) => n + f.bytes, 0) + VOICE_BYTES;

/* ── optimized variants (tools/optimize-supertonic.py), built from the official fp32 files above ──
   fp16: every graph in half precision (keep fp32 inputs/outputs) for WebGPU with shader-f16 — spectral distance to fp32 0.7 dB.
   int8: vector_estimator + text_encoder dynamic int8 (MatMul/Gemm/Conv), vocoder + duration_predictor fp32, for WebAssembly
         on the CPU — about 2x faster than fp32. Both transcribe identically to fp32 at 6 steps. */
export type Variant = 'fp32' | 'fp16' | 'int8';
export const ONNX_NAMES = ['duration_predictor', 'text_encoder', 'vector_estimator', 'vocoder'] as const;
const OPT_BYTES: Record<'fp16' | 'int8', Record<(typeof ONNX_NAMES)[number], number>> = {
  fp16: { duration_predictor: 1972038, text_encoder: 18426612, vector_estimator: 128374932, vocoder: 50747682 },
  int8: { duration_predictor: 3700147, text_encoder: 16195891, vector_estimator: 65360966, vocoder: 101424195 },
};
/** Files of one variant: `opt` files live under `<optimizedBase>/<variant>/`, the rest come from the official repository. */
export function variantFiles(v: Variant): { path: string; bytes: number; opt: boolean }[] {
  const common = MODEL_FILES.filter((f) => f.path.endsWith('.json')).map((f) => ({ ...f, opt: false }));
  if (v === 'fp32') return MODEL_FILES.map((f) => ({ ...f, opt: false }));
  return [...common, ...ONNX_NAMES.map((n) => ({ path: `onnx/${n}.onnx`, bytes: OPT_BYTES[v][n], opt: true }))];
}
export const variantBytes = (v: Variant) => variantFiles(v).reduce((n, f) => n + f.bytes, 0) + VOICE_BYTES;

/* ── text preprocessing (same steps and order as UnicodeProcessor._preprocess_text) ── */
const EMOJI = /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F1E6}-\u{1F1FF}]+/gu;
const SYMBOLS: [string, string][] = [
  ['–', '-'], ['‑', '-'], ['—', '-'], ['¯', ' '], ['_', ' '],
  ['“', '"'], ['”', '"'], ['‘', "'"], ['’', "'"], ['´', "'"], ['`', "'"],
  ['[', ' '], [']', ' '], ['|', ' '], ['/', ' '], ['#', ' '], ['→', ' '], ['←', ' '],
];
const SPECIAL = /[♥☆♡©\\]/g;
const ABBREV: [string, string][] = [['@', ' at '], ['e.g.,', 'for example, '], ['i.e.,', 'that is, ']];
const PUNCT_SPACING: [RegExp, string][] = [[/ ,/g, ','], [/ \./g, '.'], [/ !/g, '!'], [/ \?/g, '?'], [/ ;/g, ';'], [/ :/g, ':'], [/ '/g, "'"]];
const DUP_QUOTES = /(["'`])\1+/g;
const ENDING = /[.!?;:,'"')\]}…。」』】〉》›»]$/;

export function preprocess(text: string, lang: string | null): string {
  let t = text.normalize('NFKD');
  t = t.replace(EMOJI, '');
  for (const [a, b] of SYMBOLS) t = t.split(a).join(b);
  t = t.replace(SPECIAL, '');
  for (const [a, b] of ABBREV) t = t.split(a).join(b);
  for (const [re, b] of PUNCT_SPACING) t = t.replace(re, b);
  t = t.replace(DUP_QUOTES, '$1');
  t = t.replace(/\s+/g, ' ').trim();
  if (!ENDING.test(t)) t += '.';
  return lang ? `<${lang}>${t}</${lang}>` : t;
}

// Unicode code points → model ids. Characters the model does not know (-1) are dropped
// (the Python package refuses the whole text instead).
export function toIds(text: string, indexer: number[]): number[] {
  const ids: number[] = [];
  for (const ch of text) {
    const cp = ch.codePointAt(0) ?? 0;
    const id = cp < indexer.length ? indexer[cp] : -1;
    if (id >= 0) ids.push(id);
  }
  return ids;
}

// Split long text at sentence ends, ≤ maxLen characters per chunk (utils.chunk_text).
export function chunkForModel(text: string, maxLen = 300): string[] {
  const chunks: string[] = [];
  for (const para of text.split(/\n\s*\n+/).map((p) => p.trim()).filter(Boolean)) {
    let cur = '';
    for (const s of para.split(/(?<=[.!?])\s+/).map((x) => x.trim()).filter(Boolean)) {
      if (cur.length + s.length + 1 <= maxLen) cur += (cur ? ' ' : '') + s;
      else {
        if (cur) chunks.push(cur);
        // a single sentence longer than maxLen: cut at commas / spaces
        let rest = s;
        while (rest.length > maxLen) {
          let cut = Math.max(rest.lastIndexOf(', ', maxLen), rest.lastIndexOf(' ', maxLen));
          if (cut < maxLen * 0.3) cut = maxLen;
          chunks.push(rest.slice(0, cut).trim());
          rest = rest.slice(cut).trim();
        }
        cur = rest;
      }
    }
    if (cur) chunks.push(cur);
  }
  return chunks;
}

const flatten = (data: unknown): number[] => (Array.isArray(data) ? (data as unknown[]).flat(Infinity as 1) as number[] : []);

export function makeStyle(ort: OrtModule, json: StyleJson): Style {
  return {
    ttl: new ort.Tensor('float32', Float32Array.from(flatten(json.style_ttl.data)), json.style_ttl.dims),
    dp: new ort.Tensor('float32', Float32Array.from(flatten(json.style_dp.data)), json.style_dp.dims),
  };
}

function gaussian(n: number): Float32Array {
  const out = new Float32Array(n);
  for (let i = 0; i < n; i += 2) {
    const u = Math.max(Number.EPSILON, Math.random());
    const v = Math.random();
    const r = Math.sqrt(-2 * Math.log(u));
    out[i] = r * Math.cos(2 * Math.PI * v);
    if (i + 1 < n) out[i + 1] = r * Math.sin(2 * Math.PI * v);
  }
  return out;
}

const first = async (s: OrtSession, feeds: Record<string, OrtTensor>) => (await s.run(feeds))[s.outputNames[0]];
// WebGPU sessions can keep outputs on the GPU (preferredOutputLocation): free those as soon as they are used
const release = (t: OrtTensor | null | undefined) => { if (t && t.location === 'gpu-buffer') t.dispose?.(); };

/** One chunk of text → mono PCM float32 at cfg.ae.sample_rate (Supertonic.__call__ with batch size 1). */
export async function synthesizeOne(
  ort: OrtModule, m: Models, style: Style, text: string,
  opts: { lang?: string | null; steps?: number; speed?: number } = {},
): Promise<{ pcm: Float32Array; duration: number; sampleRate: number }> {
  const lang = opts.lang === undefined ? 'vi' : opts.lang;
  const steps = Math.max(1, Math.min(32, Math.round(opts.steps ?? 8)));
  const speed = Math.max(0.7, Math.min(2, opts.speed ?? 1.05));
  const ids = toIds(preprocess(text, lang), m.indexer);
  if (!ids.length) return { pcm: new Float32Array(0), duration: 0, sampleRate: m.cfg.ae.sample_rate };
  const L = ids.length;
  const textIds = new ort.Tensor('int64', BigInt64Array.from(ids, (x) => BigInt(x)), [1, L]);
  const textMask = new ort.Tensor('float32', new Float32Array(L).fill(1), [1, 1, L]);

  const durT = await first(m.dp, { text_ids: textIds, style_dp: style.dp, text_mask: textMask });
  const duration = Number((durT.data as Float32Array)[0]) / speed;
  const textEmb = await first(m.te, { text_ids: textIds, style_ttl: style.ttl, text_mask: textMask });

  // noisy latent + mask (sample_noisy_latent / get_latent_mask)
  const sr = m.cfg.ae.sample_rate;
  const chunk = m.cfg.ae.base_chunk_size * m.cfg.ttl.chunk_compress_factor;
  const latentDim = m.cfg.ttl.latent_dim * m.cfg.ttl.chunk_compress_factor;
  const wavLen = duration * sr;
  const latentLen = Math.max(1, Math.floor((wavLen + chunk - 1) / chunk));
  const validLen = Math.min(latentLen, Math.floor((Math.trunc(wavLen) + chunk - 1) / chunk));
  const mask = new Float32Array(latentLen);
  for (let i = 0; i < validLen; i++) mask[i] = 1;
  const noise = gaussian(latentDim * latentLen);
  for (let d = 0; d < latentDim; d++) for (let t = 0; t < latentLen; t++) noise[d * latentLen + t] *= mask[t];
  let xt: OrtTensor = new ort.Tensor('float32', noise, [1, latentDim, latentLen]);
  const latentMask = new ort.Tensor('float32', mask, [1, 1, latentLen]);
  const totalStep = new ort.Tensor('float32', Float32Array.of(steps), [1]);

  // the latent stays on the GPU between steps when the session allows it: no round trip through the CPU
  for (let step = 0; step < steps; step++) {
    const next = await first(m.ve, {
      noisy_latent: xt, text_emb: textEmb, style_ttl: style.ttl, text_mask: textMask,
      latent_mask: latentMask, current_step: new ort.Tensor('float32', Float32Array.of(step), [1]), total_step: totalStep,
    });
    release(xt);
    xt = next;
  }
  release(textEmb);
  const wav = await first(m.voc, { latent: xt });
  release(xt);
  return { pcm: wav.data as Float32Array, duration, sampleRate: sr };
}

/** Mono float32 PCM → 16-bit WAV bytes. */
export function encodeWav(pcm: Float32Array, sampleRate: number): ArrayBuffer {
  const buf = new ArrayBuffer(44 + pcm.length * 2);
  const v = new DataView(buf);
  const str = (o: number, s: string) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  str(0, 'RIFF'); v.setUint32(4, 36 + pcm.length * 2, true); str(8, 'WAVE');
  str(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
  v.setUint32(24, sampleRate, true); v.setUint32(28, sampleRate * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true);
  str(36, 'data'); v.setUint32(40, pcm.length * 2, true);
  for (let i = 0; i < pcm.length; i++) {
    const s = Math.max(-1, Math.min(1, pcm[i]));
    v.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true);
  }
  return buf;
}

/** Trim the model's leading/trailing near-silence and shorten long pauses inside a chunk to at most `maxGap` seconds. */
export function tightenSilence(pcm: Float32Array, sr: number, maxGap = 0.32): Float32Array {
  const w = Math.max(1, Math.round(sr * 0.02));
  const rms = (i: number) => { let s = 0; const end = Math.min(i + w, pcm.length); for (let j = i; j < end; j++) s += pcm[j] * pcm[j]; return Math.sqrt(s / Math.max(1, end - i)); };
  let a = 0; while (a < pcm.length && rms(a) < 0.012) a += w;
  let b = pcm.length - w; while (b > a && rms(b) < 0.012) b -= w;
  if (a >= b) return pcm;
  a = Math.max(0, a - Math.round(sr * 0.04));
  b = Math.min(pcm.length, b + w + Math.round(sr * 0.1));
  const keep = Math.round((maxGap * sr) / w);
  const parts: Float32Array[] = [];
  let quiet = 0;
  for (let i = a; i < b; i += w) {
    quiet = rms(i) > 0.008 ? 0 : quiet + 1;
    if (quiet <= keep) parts.push(pcm.subarray(i, Math.min(i + w, b)));
  }
  const out = new Float32Array(parts.reduce((n, x) => n + x.length, 0));
  let o = 0; for (const x of parts) { out.set(x, o); o += x.length; }
  return out;
}
