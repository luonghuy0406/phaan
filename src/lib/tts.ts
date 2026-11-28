// Đọc hồ sơ bằng giọng AI tiếng Việt (Supertonic 3, https://huggingface.co/Supertone/supertonic-3).
//   Mặc định: chạy NGAY TRÊN THIẾT BỊ bằng ONNX Runtime Web (src/lib/supertonic/). Mô hình ~400 MB chỉ được tải
//   sau khi người chơi đồng ý, rồi nằm trong bộ nhớ đệm trình duyệt (dùng được cả khi không có mạng).
//   Tuỳ chọn: đặt VITE_TTS_API_URL để dùng server tương thích OpenAI /v1/audio/speech (vd. npm run tts-server).

import { create } from 'zustand';
import * as onDevice from './supertonic/client';
import { normalizeVi, splitSpeech } from './vi-normalize';

/* ── config ── */
const API_URL = () =>
  (import.meta.env.VITE_TTS_API_URL as string | undefined) ||
  (import.meta.env.VITE_VIENEU_API_URL as string | undefined) ||
  '';
/** 'server' when a speech server is configured, otherwise the on-device model. */
export const ttsEngine = (): 'server' | 'device' => (API_URL() ? 'server' : 'device');

const API_KEY = () =>
  (import.meta.env.VITE_TTS_API_KEY as string | undefined) ||
  (import.meta.env.VITE_VIENEU_API_KEY as string | undefined) ||
  '';

const DEFAULT_VOICE = () =>
  (import.meta.env.VITE_TTS_VOICE as string | undefined) ||
  (import.meta.env.VITE_VIENEU_VOICE as string | undefined) ||
  'F1'; // Supertonic: F1-F5 (nữ), M1-M5 (nam)

const DEFAULT_MODEL = () =>
  (import.meta.env.VITE_TTS_MODEL as string | undefined) ||
  (import.meta.env.VITE_VIENEU_MODEL as string | undefined) ||
  'supertonic-3';

const DEFAULT_LANG = () =>
  (import.meta.env.VITE_TTS_LANG as string | undefined) ||
  'vi'; // Tiếng Việt

const STEPS = () => Number(import.meta.env.VITE_TTS_STEPS as string | undefined) || 8;
const SPEED = () => Number(import.meta.env.VITE_TTS_SPEED as string | undefined) || 1;
const voiceName = () => (onDevice.VOICES as readonly string[]).includes(DEFAULT_VOICE().toUpperCase()) ? DEFAULT_VOICE().toUpperCase() : 'M1';
const MAX_CHUNK_CHARS = 400; // max characters per TTS request
const CACHE_DB = 'hsm-tts-cache';
const CACHE_STORE = 'audio';
const CACHE_VERSION = 1;

export const ttsEnabled = () => (ttsEngine() === 'server' ? true : onDevice.onDeviceSupported());

/* ── consent to download the on-device voice ── */
const CONSENT_KEY = 'hsm:tts-consent';
const hasConsent = () => { try { return localStorage.getItem(CONSENT_KEY) === 'yes'; } catch { return false; } };
const setConsent = (v: 'yes' | 'no') => { try { localStorage.setItem(CONSENT_KEY, v); } catch { /* private mode */ } };
// download size for this device (fp16 on WebGPU, int8 on the CPU, fp32 without optimized files): known after the GPU check
export let MODEL_MB = 200;
if (typeof window !== 'undefined') void onDevice.modelBytes().then((b) => { MODEL_MB = Math.round(b / 1e6); }).catch(() => {});
let deviceReady = false;

/* ── state ── */
export type TtsStatus = 'idle' | 'consent' | 'downloading' | 'loading' | 'playing' | 'paused' | 'error';

interface TtsState {
  status: TtsStatus;
  /** Which document + key is currently being read */
  activeId: string | null;
  /** Progress: index of the chunk currently playing */
  chunkIndex: number;
  chunkCount: number;
  error: string | null;
  /** download of the on-device voice: bytes so far / total, or model loading steps */
  download: onDevice.Progress | null;
  /** what to read once the player agrees to download the voice */
  pending: { id: string; text: string; opts?: SpeakOpts } | null;
  backend: string | null;
}

export const useTts = create<TtsState>(() => ({
  download: null,
  pending: null,
  backend: null,
  status: 'idle',
  activeId: null,
  chunkIndex: 0,
  chunkCount: 0,
  error: null,
}));

/* ── audio context ── */
let audioCtx: AudioContext | null = null;
function getAudioCtx() {
  if (!audioCtx) audioCtx = new AudioContext();
  if (audioCtx.state === 'suspended') void audioCtx.resume();
  return audioCtx;
}

/* ── abort handling ── */
let abortController: AbortController | null = null;

// iOS Safari only lets an <audio> element play if it first played inside a user gesture.
// speak() is called from a tap, so we play a tiny silent clip on one shared element right away
// and reuse that element for every chunk later (even after a long model download).
const SILENT_WAV = 'data:audio/wav;base64,UklGRrQBAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YZABAACAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA'; // 50 ms of silence
let sharedAudio: HTMLAudioElement | null = null;
function unlockAudio() {
  // iOS: play through the ringer/silent switch like a media app, not like a notification sound
  try { const s = (navigator as Navigator & { audioSession?: { type: string } }).audioSession; if (s) s.type = 'playback'; } catch { /* older Safari */ }
  if (!sharedAudio) sharedAudio = new Audio();
  sharedAudio.src = SILENT_WAV;
  void sharedAudio.play().catch(() => {});
  getAudioCtx();
}

/* ── IndexedDB cache ── */
function openCacheDb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(CACHE_DB, CACHE_VERSION);
    req.onupgradeneeded = () => { req.result.createObjectStore(CACHE_STORE); };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function getCached(key: string): Promise<Blob | null> {
  try {
    const db = await openCacheDb();
    return new Promise((resolve) => {
      const tx = db.transaction(CACHE_STORE, 'readonly');
      const req = tx.objectStore(CACHE_STORE).get(key);
      req.onsuccess = () => resolve(req.result instanceof Blob ? req.result : null);
      req.onerror = () => resolve(null);
    });
  } catch { return null; }
}

async function putCache(key: string, blob: Blob) {
  try {
    const db = await openCacheDb();
    const tx = db.transaction(CACHE_STORE, 'readwrite');
    tx.objectStore(CACHE_STORE).put(blob, key);
  } catch { /* non-critical */ }
}

export interface SpeakOpts { voice?: string; steps?: number; fastStart?: boolean }

function cacheKey(text: string, o: SpeakOpts = {}): string {
  // Hash: model + voice + lang + text → deterministic key
  const voice = ttsEngine() === 'device' ? (o.voice || voiceName()) : DEFAULT_VOICE();
  const model = ttsEngine() === 'device' ? `device-supertonic3-s${o.steps ?? STEPS()}-x${SPEED()}` : DEFAULT_MODEL();
  const lang = DEFAULT_LANG();
  const raw = `${model}|${voice}|${lang}|${text}`;
  let h = 0;
  for (let i = 0; i < raw.length; i++) {
    h = ((h << 5) - h + raw.charCodeAt(i)) | 0;
  }
  return `tts:${(h >>> 0).toString(36)}`;
}

/* ── chunking ── */

/** Split text into speakable chunks at sentence boundaries (. ! ? ;) or at MAX_CHUNK_CHARS. */
export function chunkText(text: string, maxChars = MAX_CHUNK_CHARS): string[] {
  const MAX_CHUNK_CHARS = maxChars;
  if (!text.trim()) return [];
  // Normalize whitespace
  const clean = text.replace(/\s+/g, ' ').trim();
  if (clean.length <= MAX_CHUNK_CHARS) return [clean];

  const chunks: string[] = [];
  let remaining = clean;

  while (remaining.length > 0) {
    if (remaining.length <= MAX_CHUNK_CHARS) {
      chunks.push(remaining.trim());
      break;
    }
    // Try to break at sentence boundary
    let cut = -1;
    const search = remaining.slice(0, MAX_CHUNK_CHARS);
    // Look for the last sentence-ending punctuation followed by a space
    for (let i = search.length - 1; i >= MAX_CHUNK_CHARS * 0.3; i--) {
      if (/[.!?;:。]/.test(search[i]) && (i + 1 >= search.length || search[i + 1] === ' ')) {
        cut = i + 1;
        break;
      }
    }
    // Fall back to comma or space
    if (cut < 0) {
      for (let i = search.length - 1; i >= MAX_CHUNK_CHARS * 0.3; i--) {
        if (search[i] === ',' || search[i] === ' ') { cut = i + 1; break; }
      }
    }
    if (cut < 0) cut = MAX_CHUNK_CHARS;

    chunks.push(remaining.slice(0, cut).trim());
    remaining = remaining.slice(cut).trim();
  }

  return chunks.filter(Boolean);
}

/* ── synthesize one chunk ── */
async function synthesizeChunk(text: string, signal: AbortSignal, o: SpeakOpts = {}): Promise<Blob> {
  const key = cacheKey(text, o);
  const cached = await getCached(key);
  if (cached) return cached;

  if (ttsEngine() === 'device') {
    const blob = await onDevice.synthesize(text, { lang: DEFAULT_LANG(), steps: o.steps ?? STEPS(), speed: SPEED(), voice: o.voice || voiceName() });
    if (signal.aborted) throw new DOMException('Aborted', 'AbortError');
    void putCache(key, blob);
    return blob;
  }

  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (API_KEY()) headers.Authorization = `Bearer ${API_KEY()}`;

  const res = await fetch(API_URL(), {
    method: 'POST',
    headers,
    body: JSON.stringify({
      model: DEFAULT_MODEL(),
      input: text,
      voice: DEFAULT_VOICE(),
      lang: DEFAULT_LANG(),
      speed: 1,
    }),
    signal,
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`TTS API ${res.status}: ${body.slice(0, 200)}`);
  }

  const blob = await res.blob();
  void putCache(key, blob);
  return blob;
}

/* ── play a blob ── */
/* ── gapless playback with Web Audio ── */
let sources: AudioBufferSourceNode[] = [];

async function decode(blob: Blob): Promise<AudioBuffer> {
  return getAudioCtx().decodeAudioData(await blob.arrayBuffer());
}

/** Drop the model's leading/trailing near-silence so our own pauses are what the listener hears. */
function trimSilence(buf: AudioBuffer): AudioBuffer {
  const ch = buf.getChannelData(0);
  const thr = 0.004;
  let a = 0, b = ch.length - 1;
  while (a < b && Math.abs(ch[a]) < thr) a++;
  while (b > a && Math.abs(ch[b]) < thr) b--;
  const pad = Math.round(buf.sampleRate * 0.03);
  a = Math.max(0, a - pad); b = Math.min(ch.length, b + pad * 2);
  if (b - a <= 0 || (a === 0 && b === ch.length)) return buf;
  const out = getAudioCtx().createBuffer(buf.numberOfChannels, b - a, buf.sampleRate);
  for (let c = 0; c < buf.numberOfChannels; c++) out.copyToChannel(buf.getChannelData(c).subarray(a, b), c);
  return out;
}

/** Schedule a buffer at `at` (AudioContext time) with tiny fades (no clicks). Resolves when it ends. */
function schedule(buf: AudioBuffer, at: number): Promise<void> {
  const ctx = getAudioCtx();
  const src = ctx.createBufferSource();
  const gain = ctx.createGain();
  src.buffer = buf;
  const f = Math.min(0.012, buf.duration / 4);
  gain.gain.setValueAtTime(0, at);
  gain.gain.linearRampToValueAtTime(1, at + f);
  gain.gain.setValueAtTime(1, at + buf.duration - f);
  gain.gain.linearRampToValueAtTime(0, at + buf.duration);
  src.connect(gain).connect(ctx.destination);
  sources.push(src);
  src.start(at);
  return new Promise((resolve) => {
    src.onended = () => { sources = sources.filter((x) => x !== src); resolve(); };
  });
}

function stopSources() {
  for (const s of sources) { try { s.stop(); } catch { /* not started */ } }
  sources = [];
}

/* ── public API ── */

/** Extract plain text from a document for reading aloud. Strips markup. */
export function extractDocText(doc: {
  type: string;
  title?: string;
  headline?: string;
  heading?: string;
  paragraphs?: string[];
  sections?: { heading?: string; paragraphs?: string[] }[];
  lines?: { n: number; speaker?: string; text: string }[];
  greeting?: string;
  signature?: string;
  caption?: string;
  imageCaption?: string;
  deck?: string;
  items?: { name: string; qty?: number | string; price?: string }[];
  fields?: { label: string; value: string }[];
  footer?: string[];
  content?: string;
  persons?: { name: string; age?: number; role?: string; note?: string; suspicion?: string; victim?: boolean }[];
}): string {
  const strip = (s?: string | null) => (s || '').replace(/\*\*|__|~~/g, '');
  const parts: string[] = [];

  // Title / heading
  // the paper shows a bold first line of `content` as its heading: read that instead of the board title
  const contentLead = typeof doc.content === 'string' && /^\s*\*\*[^*]+\*\*\s*(\n|$)/.test(doc.content);
  const title = doc.headline || doc.heading || (contentLead ? '' : doc.title);
  if (title) parts.push(strip(title));

  // Deck (newspaper)
  if (doc.deck) parts.push(strip(doc.deck));

  // Fields
  if (doc.fields?.length) {
    for (const f of doc.fields) parts.push(`${strip(f.label)}: ${strip(f.value)}`);
  }

  // Greeting (letter)
  if (doc.greeting) parts.push(strip(doc.greeting));

  // Paragraphs
  if (doc.paragraphs?.length) {
    for (const p of doc.paragraphs) parts.push(strip(p));
  }

  // Sections (report)
  if (doc.sections?.length) {
    for (const s of doc.sections) {
      if (s.heading) parts.push(strip(s.heading));
      if (s.paragraphs?.length) for (const p of s.paragraphs) parts.push(strip(p));
    }
  }

  // Testimony lines
  if (doc.lines?.length) {
    for (const l of doc.lines) {
      parts.push(l.speaker ? `${l.speaker}: ${strip(l.text)}` : strip(l.text));
    }
  }

  // Caption
  if (doc.imageCaption) parts.push(strip(doc.imageCaption));
  if (doc.caption) parts.push(strip(doc.caption));

  // Receipt items
  if (doc.items?.length) {
    for (const it of doc.items) parts.push(`${strip(it.name)}, số lượng ${it.qty ?? 1}, ${it.price || ''}`);
  }
  if (doc.footer?.length) for (const f of doc.footer) parts.push(strip(f));

  // Free-text body (light Markdown): drop list markers, keep the words
  if (typeof doc.content === 'string') {
    for (const line of doc.content.split('\n')) {
      const t = strip(line.replace(/^\s*([-*•]|\d+[.)])\s+/, '')).trim();
      if (t) parts.push(t);
    }
  }

  // ID sheet ("people"): one entry per person
  for (const p of doc.persons || []) {
    parts.push(strip(`${p.victim ? 'Nạn nhân' : 'Nghi phạm'}: ${p.name}${p.age ? `, ${p.age} tuổi` : ''}${p.role ? `, ${p.role}` : ''}. ${(p.victim ? p.note : p.suspicion) || ''}`));
  }

  // Signature
  if (doc.signature) parts.push(strip(doc.signature));

  // one part per line: the reader pauses longer between them (headings, paragraphs, list items)
  return parts.map((p) => p.trim()).filter(Boolean).join('\n');
}

/** Start reading text aloud. Chunks the text, synthesizes each, plays sequentially. */
export async function speak(id: string, text: string, opts: SpeakOpts = {}) {
  // Stop any current playback
  stop();
  unlockAudio(); // must happen synchronously inside the tap

  if (!ttsEnabled()) {
    useTts.setState({ status: 'error', error: 'Trình duyệt này chưa hỗ trợ đọc bằng giọng AI.', activeId: null });
    return;
  }

  const device = ttsEngine() === 'device';
  // what a narrator would say (numbers, dates, units…), cut at sentence boundaries with natural pauses
  const segs = splitSpeech(normalizeVi(text), device ? 180 : MAX_CHUNK_CHARS);
  if (!segs.length) return;
  // a short first piece starts the voice sooner; the rest is synthesized while it plays
  if (opts.fastStart && device && segs[0].text.length > 70) {
    const t = segs[0].text;
    const cut = (() => { for (let i = 55; i < Math.min(t.length - 15, 110); i++) if (/[,;:]/.test(t[i]) || (i > 70 && t[i] === ' ')) return i + 1; return -1; })();
    if (cut > 0) segs.splice(0, 1, { ...segs[0], text: t.slice(0, cut).trim(), pause: 0.12 }, { ...segs[0], text: t.slice(cut).trim() });
  }

  abortController = new AbortController();
  const { signal } = abortController;

  if (device && !deviceReady) {
    const voice = opts.voice || voiceName();
    const cached = await onDevice.isModelCached(voice);
    if (signal.aborted) return;
    if (!cached && !hasConsent()) {
      // ask before downloading ~400 MB; acceptTtsDownload() resumes from here
      useTts.setState({ status: 'consent', activeId: id, pending: { id, text, opts }, error: null });
      return;
    }
    useTts.setState({ status: cached ? 'loading' : 'downloading', activeId: id, error: null, download: null });
    try {
      const backend = await onDevice.ensureModel(voice, (p) => {
        if (!signal.aborted) useTts.setState({ download: p, status: p.phase === 'download' && !cached ? 'downloading' : 'loading' });
      });
      deviceReady = true;
      useTts.setState({ backend, download: null });
    } catch (err) {
      if (!signal.aborted) useTts.setState({ status: 'error', error: `Không tải được giọng đọc: ${(err as Error).message}`, activeId: null, download: null });
      return;
    }
    if (signal.aborted) return; // stopped while downloading: the model stays cached for next time
  }

  useTts.setState({ status: 'loading', activeId: id, chunkIndex: 0, chunkCount: segs.length, error: null });

  // synthesize up to LOOKAHEAD segments ahead (the worker runs them one by one) and schedule them back to back
  const LOOKAHEAD = 3;
  const jobs: Promise<AudioBuffer>[] = [];
  const job = (i: number) => {
    if (i < segs.length && !jobs[i]) {
      jobs[i] = synthesizeChunk(segs[i].text, signal, opts).then(decode).then(trimSilence);
      jobs[i].catch(() => {}); // handled when awaited
    }
    return jobs[i];
  };
  try {
    const ctx = getAudioCtx();
    let end = 0; // when the last scheduled segment finishes (AudioContext time)
    let last: Promise<void> = Promise.resolve();
    for (let i = 0; i < segs.length; i++) {
      for (let k = i; k <= i + LOOKAHEAD; k++) job(k);
      if (signal.aborted) return;
      if (ctx.currentTime >= end && useTts.getState().status !== 'paused') useTts.setState({ status: 'loading' }); // waiting on the model
      const buf = await job(i);
      if (signal.aborted) return;
      const at = Math.max(ctx.currentTime + 0.06, end + (i > 0 ? segs[i - 1].pause : 0));
      const idx = i;
      last = schedule(buf, at);
      void last.then(() => { if (!signal.aborted) useTts.setState({ chunkIndex: Math.min(idx + 1, segs.length - 1) }); });
      end = at + buf.duration;
      if (useTts.getState().status !== 'paused') useTts.setState({ status: 'playing' });
      // don't run more than ~LOOKAHEAD segments ahead of what is audible
      while (!signal.aborted && i + 1 < segs.length && end - ctx.currentTime > 20) await new Promise((r) => setTimeout(r, 250));
    }
    await last;
    if (!signal.aborted) useTts.setState({ status: 'idle', activeId: null, chunkIndex: 0, chunkCount: 0 });
  } catch (err) {
    if ((err as DOMException).name === 'AbortError' || signal.aborted) return; // user stopped
    stopSources();
    useTts.setState({ status: 'error', error: `Lỗi đọc: ${(err as Error).message}`, activeId: null });
  }
}

/* ── pre-recorded reading of case documents (tools/gen-doc-voice.mjs, VieNeu) ──
   public/cases/<id>/audio/read/index.json lists, per document, its blocks in reading order;
   each block is <doc>/<key>.mp3 with the same key as the paper block (f0, p1, l7…). Played back to back,
   with the next few files fetched ahead, so reading is smooth and uses the same voices as the narration.
   Documents or blocks without a file fall back to the live voice above. */
type ReadIndex = { v: number; docs: Record<string, { k: string; p: number }[]> };
const readIndexes = new Map<string, Promise<ReadIndex | null>>();
const readBase = (caseId: string) => `${import.meta.env.BASE_URL}cases/${caseId}/audio/read/`;
function loadReadIndex(caseId: string): Promise<ReadIndex | null> {
  let p = readIndexes.get(caseId);
  if (!p) {
    p = fetch(readBase(caseId) + 'index.json')
      .then((r) => (r.ok ? (r.json() as Promise<ReadIndex>) : null))
      .catch(() => null);
    readIndexes.set(caseId, p);
  }
  return p;
}

async function playRecorded(id: string, list: { url: string; pause: number }[]) {
  const ctrl = new AbortController();
  abortController = ctrl;
  const { signal } = ctrl;
  useTts.setState({ status: 'loading', activeId: id, chunkIndex: 0, chunkCount: list.length, error: null });
  const ctx = getAudioCtx();
  const bufs: Promise<AudioBuffer>[] = [];
  const get = (i: number) => {
    if (i < list.length && !bufs[i]) {
      bufs[i] = fetch(list[i].url, { signal })
        .then((r) => (r.ok ? r.arrayBuffer() : Promise.reject(new Error(`HTTP ${r.status}`))))
        .then((b) => ctx.decodeAudioData(b));
      bufs[i].catch(() => {}); // handled when awaited
    }
    return bufs[i];
  };
  try {
    let end = 0;
    let last: Promise<void> = Promise.resolve();
    for (let i = 0; i < list.length; i++) {
      for (let k = i; k <= i + 3; k++) void get(k);
      const buf = await get(i);
      if (signal.aborted) return;
      const at = Math.max(ctx.currentTime + 0.05, end + (i > 0 ? list[i - 1].pause : 0));
      const idx = i;
      last = schedule(buf, at);
      void last.then(() => { if (!signal.aborted) useTts.setState({ chunkIndex: Math.min(idx + 1, list.length - 1) }); });
      end = at + buf.duration;
      if (useTts.getState().status !== 'paused') useTts.setState({ status: 'playing' });
      while (!signal.aborted && i + 1 < list.length && end - ctx.currentTime > 15) await new Promise((r) => setTimeout(r, 250));
    }
    await last;
    if (!signal.aborted) useTts.setState({ status: 'idle', activeId: null, chunkIndex: 0, chunkCount: 0 });
  } catch (err) {
    if ((err as DOMException).name === 'AbortError' || signal.aborted) return;
    stopSources();
    useTts.setState({ status: 'error', error: `Lỗi đọc: ${(err as Error).message}`, activeId: null });
  }
}

/** Read a whole document: pre-recorded voice when the case has it, otherwise the live voice. */
export async function speakDoc(caseId: string, doc: Parameters<typeof extractDocText>[0] & { id: string }) {
  stop();
  unlockAudio(); // inside the tap, before any await
  const entry = (await loadReadIndex(caseId))?.docs[doc.id];
  if (!entry?.length) return speak(`doc:${doc.id}`, extractDocText(doc));
  const base = readBase(caseId);
  return playRecorded(`doc:${doc.id}`, entry.map((e) => ({ url: `${base}${doc.id}/${e.k}.mp3`, pause: e.p })));
}

/** Read one block of a document ("Đọc đoạn này"). */
export async function speakBlock(caseId: string, docId: string, key: string, text: string) {
  stop();
  unlockAudio();
  const entry = (await loadReadIndex(caseId))?.docs[docId]?.find((e) => e.k === key);
  if (!entry) return speak(`${docId}:${key}`, text);
  return playRecorded(`${docId}:${key}`, [{ url: `${readBase(caseId)}${docId}/${key}.mp3`, pause: 0 }]);
}

/** The player agreed to download the on-device voice: remember it and read what they asked for. */
export function acceptTtsDownload() {
  setConsent('yes');
  const p = useTts.getState().pending;
  useTts.setState({ pending: null });
  if (p) void speak(p.id, p.text, p.opts);
}

/** "Để sau": nothing is downloaded; we ask again next time they tap a read button. */
export function declineTtsDownload() {
  setConsent('no');
  useTts.setState({ status: 'idle', activeId: null, pending: null });
}

/** Remove the downloaded voice from this device (settings). */
export async function removeDeviceVoice() {
  stop();
  deviceReady = false;
  setConsent('no');
  await onDevice.deleteModel();
}
export const isDeviceVoiceCached = (voice?: string) => onDevice.isModelCached(voice || voiceName());

/** Load the on-device voice ahead of time (only when it is already downloaded) and compile its kernels. */
export async function prepareDeviceVoice(voice?: string) {
  if (ttsEngine() !== 'device' || !onDevice.onDeviceSupported()) return;
  if (!deviceReady && !(await onDevice.isModelCached(voice || voiceName()))) return;
  try {
    const backend = await onDevice.ensureModel(voice || voiceName(), () => {});
    deviceReady = true;
    useTts.setState({ backend });
    onDevice.warmUp();
  } catch { /* the next speak() reports it */ }
}

/** Pause current playback (freezes the audio clock, so scheduled segments wait too). */
export function pause() {
  const st = useTts.getState().status;
  if ((st === 'playing' || st === 'loading') && audioCtx) {
    void audioCtx.suspend();
    useTts.setState({ status: 'paused' });
  }
}

/** Resume after pause. */
export function resume() {
  if (useTts.getState().status === 'paused' && audioCtx) {
    void audioCtx.resume();
    useTts.setState({ status: 'playing' });
  }
}

/** Stop and reset everything. */
export function stop() {
  abortController?.abort();
  abortController = null;
  stopSources();
  if (audioCtx?.state === 'suspended') void audioCtx.resume();
  useTts.setState({ status: 'idle', activeId: null, chunkIndex: 0, chunkCount: 0, error: null, download: null, pending: null });
}
