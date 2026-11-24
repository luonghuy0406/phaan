// TTS integration: Supertonic 3 (https://huggingface.co/supertone-oss-archive/supertonic-3) with Vietnamese ('vi')
// Compatible with OpenAI-style endpoint: POST /v1/audio/speech
// Also works with VieNeu-TTS or any standard OpenAI speech server.

import { create } from 'zustand';

/* ── config ── */
const API_URL = () =>
  (import.meta.env.VITE_TTS_API_URL as string | undefined) ||
  (import.meta.env.VITE_VIENEU_API_URL as string | undefined) ||
  'http://localhost:8000/v1/audio/speech';

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

const isLocal = () => /localhost|127\.0\.0\.1|192\.168\.|10\./.test(API_URL());
const MAX_CHUNK_CHARS = 400; // max characters per TTS request
const CACHE_DB = 'hsm-tts-cache';
const CACHE_STORE = 'audio';
const CACHE_VERSION = 1;

export const ttsEnabled = () => Boolean(API_KEY() || isLocal());

/* ── state ── */
export type TtsStatus = 'idle' | 'loading' | 'playing' | 'paused' | 'error';

interface TtsState {
  status: TtsStatus;
  /** Which document + key is currently being read */
  activeId: string | null;
  /** Progress: index of the chunk currently playing */
  chunkIndex: number;
  chunkCount: number;
  error: string | null;
}

export const useTts = create<TtsState>(() => ({
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
let currentAudio: HTMLAudioElement | null = null;

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

function cacheKey(text: string): string {
  // Hash: model + voice + lang + text → deterministic key
  const voice = DEFAULT_VOICE();
  const model = DEFAULT_MODEL();
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
export function chunkText(text: string): string[] {
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
async function synthesizeChunk(text: string, signal: AbortSignal): Promise<Blob> {
  const key = cacheKey(text);
  const cached = await getCached(key);
  if (cached) return cached;

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
function playBlob(blob: Blob, signal: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    currentAudio = audio;
    audio.onended = () => { URL.revokeObjectURL(url); currentAudio = null; resolve(); };
    audio.onerror = () => { URL.revokeObjectURL(url); currentAudio = null; reject(new Error('Lỗi phát audio')); };

    const onAbort = () => {
      audio.pause();
      audio.src = '';
      URL.revokeObjectURL(url);
      currentAudio = null;
      reject(new DOMException('Aborted', 'AbortError'));
    };
    if (signal.aborted) { onAbort(); return; }
    signal.addEventListener('abort', onAbort, { once: true });

    // Ensure AudioContext is active (iOS Safari requires user-initiated)
    getAudioCtx();
    void audio.play().catch(reject);
  });
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
}): string {
  const strip = (s?: string | null) => (s || '').replace(/\*\*|__|~~/g, '');
  const parts: string[] = [];

  // Title / heading
  const title = doc.headline || doc.heading || doc.title;
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

  // Signature
  if (doc.signature) parts.push(strip(doc.signature));

  return parts.join('. ').replace(/\.\./g, '.');
}

/** Start reading text aloud. Chunks the text, synthesizes each, plays sequentially. */
export async function speak(id: string, text: string) {
  // Stop any current playback
  stop();

  if (!ttsEnabled()) {
    useTts.setState({ status: 'error', error: 'Chưa cấu hình API key TTS (VITE_VIENEU_API_KEY).', activeId: null });
    return;
  }

  const chunks = chunkText(text);
  if (!chunks.length) return;

  abortController = new AbortController();
  const { signal } = abortController;

  useTts.setState({ status: 'loading', activeId: id, chunkIndex: 0, chunkCount: chunks.length, error: null });

  // Pipeline: prefetch next chunk while current one is playing
  try {
    let nextBlobPromise: Promise<Blob> | null = null;

    for (let i = 0; i < chunks.length; i++) {
      if (signal.aborted) break;

      useTts.setState({ chunkIndex: i, status: i === 0 ? 'loading' : 'playing' });

      // Get current chunk audio (from prefetch or fresh)
      const blob = nextBlobPromise ? await nextBlobPromise : await synthesizeChunk(chunks[i], signal);

      // Start prefetching next chunk
      nextBlobPromise = i + 1 < chunks.length ? synthesizeChunk(chunks[i + 1], signal) : null;

      useTts.setState({ status: 'playing' });
      await playBlob(blob, signal);
    }

    if (!signal.aborted) {
      useTts.setState({ status: 'idle', activeId: null, chunkIndex: 0, chunkCount: 0 });
    }
  } catch (err) {
    if ((err as DOMException).name === 'AbortError') return; // user stopped
    useTts.setState({ status: 'error', error: `Lỗi đọc: ${(err as Error).message}`, activeId: null });
  }
}

/** Pause current playback. */
export function pause() {
  if (currentAudio && !currentAudio.paused) {
    currentAudio.pause();
    useTts.setState({ status: 'paused' });
  }
}

/** Resume paused playback. */
export function resume() {
  if (currentAudio && currentAudio.paused) {
    void currentAudio.play();
    useTts.setState({ status: 'playing' });
  }
}

/** Stop and cancel all playback. */
export function stop() {
  abortController?.abort();
  abortController = null;
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.src = '';
    currentAudio = null;
  }
  useTts.setState({ status: 'idle', activeId: null, chunkIndex: 0, chunkCount: 0, error: null });
}
