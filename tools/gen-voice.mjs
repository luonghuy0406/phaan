#!/usr/bin/env node
// Tạo sẵn giọng đọc (lời dẫn, chuyển cảnh, kết thúc) cho một hồ sơ, chạy trên máy.
//
//   node tools/gen-voice.mjs <case-id> [clip-id …] [--force] [--dry]
//   --dry: chỉ in ra các câu sẽ đọc (để đối chiếu với chữ hiển thị), không tạo âm thanh.
//
// Đọc kịch bản `authoring/<case-id>/voice.json`, ghi file vào `public/cases/<case-id>/audio/<clip>.mp3`.
// Clip đã có file và kịch bản không đổi thì bỏ qua (băm nội dung lưu trong `authoring/<case-id>/voice.lock.json`).
//
// Hai bộ máy đọc, chọn bằng "engine" trong voice.json:
//   - "vieneu" (khuyên dùng): VieNeu-TTS v3 Turbo (https://github.com/pnnbao97/VieNeu-TTS), 25 giọng Bắc/Trung/Nam.
//       Cài một lần:  python3 -m venv ~/.venvs/vieneu && ~/.venvs/vieneu/bin/pip install vieneu
//       Chạy với:     VIENEU_PYTHON=~/.venvs/vieneu/bin/python npm run gen-voice -- <case-id>
//       (mặc định tìm ~/.venvs/vieneu/bin/python). Giọng: tên dựng sẵn, ví dụ "Thái Sơn", "Thiện Minh".
//   - "supertonic": Supertonic 3 qua onnxruntime-node (cài tạm: npm i --no-save onnxruntime-node@1.22.0),
//       mô hình trong ~/.cache/supertonic3. Giọng: F1–F5, M1–M5.
// Cần ffmpeg để chuyển sang MP3.
//
// voice.json:
// {
//   "engine": "vieneu",
//   "voices": { "dan": "Thiện Minh", "thuyen": "Đức Trí" },   // tên vai → giọng
//   "clips": [
//     { "id": "intro", "segments": [ { "voice": "dan", "text": "…", "pause": 0.6 }, … ] }
//   ]
// }
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync, mkdtempSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { tmpdir, homedir } from 'node:os';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const force = args.includes('--force');
const [caseId, ...only] = args.filter((a) => !a.startsWith('--'));
if (!caseId) { console.log('Dùng: node tools/gen-voice.mjs <case-id> [clip-id …] [--force]'); process.exit(2); }

const scriptPath = join(ROOT, 'authoring', caseId, 'voice.json');
if (!existsSync(scriptPath)) { console.error(`Không có ${scriptPath}`); process.exit(1); }
const script = JSON.parse(readFileSync(scriptPath, 'utf8'));
const engine = script.engine || 'supertonic';
const lockPath = join(ROOT, 'authoring', caseId, 'voice.lock.json');
const lock = existsSync(lockPath) ? JSON.parse(readFileSync(lockPath, 'utf8')) : {};
const outDir = join(ROOT, 'public', 'cases', caseId, 'audio');
mkdirSync(outDir, { recursive: true });
const { normalizeVi } = await import('../src/lib/vi-normalize.ts');
const voiceOf = (v) => script.voices?.[v] || v;
// VieNeu reads tags like [thở dài], [cười]: keep them out of the number / symbol normaliser
const prepText = (t) => (engine === 'vieneu'
  ? String(t).split(/(\[[^\]]+\])/).map((p) => (/^\[[^\]]+\]$/.test(p) ? p : normalizeVi(p))).join(' ').replace(/\s+/g, ' ').trim()
  : normalizeVi(String(t).replace(/\[[^\]]+\]/g, ' ')));

/* ── which clips need (re)making ── */
/* ── clips read straight from case.json, so the voice always matches what the player sees ──
   { "id": "beat-3", "source": "beat:3", "quotes": ["thuyen", { "voice": "thuyen", "before": "[thở dài]" }] }
   source: "intro" (title, paragraphs, objective) · "beat:N" (round label, kicker, title, paragraphs) · "finale" (title, paragraphs).
   Every "…" quote in the text is read by the next voice in `quotes` (narrator: `narrator`, default "dan"). */
const caseData = JSON.parse(readFileSync(join(ROOT, 'public', 'cases', caseId, 'case.json'), 'utf8'));
const VN_NUM = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín'];
function sourceLines(src) {
  if (src === 'intro') {
    const i = caseData.intro || {};
    return [i.title || caseData.title, ...(i.paragraphs || []), ...(i.objective ? [`Nhiệm vụ: ${i.objective}`] : [])];
  }
  if (src === 'finale') { const f = caseData.finale || {}; return [f.title || 'Sự thật đã sáng tỏ', ...(f.paragraphs || [])]; }
  const m = /^beat:(\d+)$/.exec(src || '');
  const b = m && (caseData.beats || []).find((x) => x.stage === Number(m[1]));
  if (!b) { console.error(`Clip nguồn "${src}" không có trong case.json`); process.exit(1); }
  const head = `Trọng điểm ${b.stage < 10 ? VN_NUM[b.stage] : b.stage}${b.kicker ? `. ${b.kicker.replace(/\s*·\s*/g, ', ')}` : ''}`;
  return [head, b.title || 'Hồ sơ mở rộng', ...b.paragraphs];
}
function expand(clip) {
  if (!clip.source) return clip.segments || [];
  const narrator = clip.narrator || 'dan';
  const quotes = [...(clip.quotes || [])];
  const segs = [];
  sourceLines(clip.source).forEach((line, li) => {
    const parts = String(line).replace(/\*\*|__|~~/g, '').split(/("[^"]+"|“[^”]+”)/).map((x) => x.trim()).filter(Boolean);
    parts.forEach((part, pi) => {
      const isQuote = /^["“]/.test(part);
      const q = isQuote ? quotes.shift() : null;
      if (isQuote && q === undefined) { console.error(`${clip.id}: thiếu vai cho lời thoại ${part}`); process.exit(1); }
      const voice = isQuote ? (typeof q === 'string' ? q : q.voice) : narrator;
      const text = (isQuote && typeof q === 'object' && q.before ? `${q.before} ` : '') + part.replace(/^["“]|["”]$/g, '');
      const last = pi === parts.length - 1;
      const prev = pi > 0 ? segs[segs.length - 1] : null;
      // same voice continues (e.g. a "quoted" word inside the narration): keep it one sentence
      if (prev && prev.voice === voice) { prev.text = `${prev.text} ${text}`; prev.pause = last ? (li === 0 ? 0.8 : 0.65) : 0.3; return; }
      segs.push({ voice, text, pause: last ? (li === 0 ? 0.8 : 0.65) : 0.3 });
    });
    segs.forEach((g) => { g.text = g.text.replace(/^[\s.,;:]+/, '').replace(/\s+([.,;:!?…])/g, '$1'); });
  });
  if (quotes.length) { console.error(`${clip.id}: thừa ${quotes.length} vai trong "quotes" (văn bản có ít lời thoại hơn)`); process.exit(1); }
  return segs;
}
for (const clip of script.clips || []) clip.segments = expand(clip);
if (args.includes('--dry')) {
  // print exactly what will be read, clip by clip, to compare with the screen
  for (const clip of script.clips || []) {
    if (only.length && !only.includes(clip.id)) continue;
    console.log(`\n■ ${clip.id}${clip.source ? `  (từ case.json: ${clip.source})` : ''}`);
    clip.segments.forEach((g) => console.log(`  [${voiceOf(g.voice)}] ${g.text}`));
  }
  process.exit(0);
}

const todo = (script.clips || []).filter((clip) => {
  if (only.length && !only.includes(clip.id)) return false;
  clip.hash = createHash('sha256').update(JSON.stringify({ engine, clip: { ...clip, hash: undefined }, voices: script.voices, steps: script.steps, speed: script.speed })).digest('hex').slice(0, 16);
  if (!force && lock[clip.id] === clip.hash && existsSync(join(outDir, `${clip.id}.mp3`))) { console.log(`= ${clip.id} (không đổi)`); return false; }
  return true;
});
if (!todo.length) { console.log('Không có clip nào cần tạo.'); process.exit(0); }

/* ── audio helpers ── */
// cut leading / trailing near-silence so our own pauses set the rhythm
function trim(pcm, sr, maxGap) {
  const w = Math.round(sr * 0.02);
  const loud = (i) => { let s = 0; for (let j = i; j < Math.min(i + w, pcm.length); j++) s += pcm[j] * pcm[j]; return Math.sqrt(s / w) > 0.012; };
  let a = 0; while (a < pcm.length && !loud(a)) a += w;
  let b = pcm.length - w; while (b > a && !loud(b)) b -= w;
  a = Math.max(0, a - Math.round(sr * 0.04)); b = Math.min(pcm.length, b + w + Math.round(sr * 0.12));
  return collapseGaps(pcm.subarray(a, b), sr, maxGap);
}
// shorten long holes between phrases inside one piece to at most `maxGap` seconds
function collapseGaps(pcm, sr, maxGap) {
  const w = Math.round(sr * 0.02);
  const keep = Math.round(maxGap * sr / w);
  const out = [];
  let quiet = 0;
  for (let i = 0; i < pcm.length; i += w) {
    const end = Math.min(i + w, pcm.length);
    let s = 0; for (let j = i; j < end; j++) s += pcm[j] * pcm[j];
    quiet = Math.sqrt(s / (end - i)) > 0.008 ? 0 : quiet + 1;
    if (quiet <= keep) out.push(pcm.subarray(i, end));
  }
  const res = new Float32Array(out.reduce((n, p) => n + p.length, 0));
  let o = 0; for (const p of out) { res.set(p, o); o += p.length; }
  return res;
}
function encodeWav(pcm, sampleRate) {
  const buf = Buffer.alloc(44 + pcm.length * 2);
  buf.write('RIFF', 0); buf.writeUInt32LE(36 + pcm.length * 2, 4); buf.write('WAVE', 8);
  buf.write('fmt ', 12); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(1, 22);
  buf.writeUInt32LE(sampleRate, 24); buf.writeUInt32LE(sampleRate * 2, 28); buf.writeUInt16LE(2, 32); buf.writeUInt16LE(16, 34);
  buf.write('data', 36); buf.writeUInt32LE(pcm.length * 2, 40);
  for (let i = 0; i < pcm.length; i++) { const s = Math.max(-1, Math.min(1, pcm[i])); buf.writeInt16LE(Math.round(s < 0 ? s * 0x8000 : s * 0x7fff), 44 + i * 2); }
  return buf;
}
const readPcm = (file, sr) => {
  const raw = execFileSync('ffmpeg', ['-loglevel', 'error', '-i', file, '-f', 'f32le', '-ac', '1', '-ar', String(sr), '-'], { maxBuffer: 1 << 30 });
  return new Float32Array(raw.buffer, raw.byteOffset, raw.byteLength / 4).slice();
};

/* ── engines: return, for each clip, a list of pieces { pcm, gapAfter } ── */
async function renderSupertonic(clips) {
  let ort;
  try { ort = (await import('onnxruntime-node')).default; } catch {
    console.error('Thiếu onnxruntime-node. Cài tạm (không ghi vào package.json):  npm i --no-save onnxruntime-node@1.22.0');
    process.exit(1);
  }
  const { makeStyle, synthesizeOne, chunkForModel } = await import('../src/lib/supertonic/core.ts');
  const MODEL = process.env.SUPERTONIC_DIR || join(homedir(), '.cache/supertonic3');
  if (!existsSync(join(MODEL, 'onnx/vocoder.onnx'))) { console.error(`Không thấy mô hình Supertonic trong ${MODEL}`); process.exit(1); }
  const load = (f) => ort.InferenceSession.create(join(MODEL, 'onnx', f));
  const m = {
    cfg: JSON.parse(readFileSync(join(MODEL, 'onnx/tts.json'), 'utf8')),
    indexer: JSON.parse(readFileSync(join(MODEL, 'onnx/unicode_indexer.json'), 'utf8')),
    dp: await load('duration_predictor.onnx'), te: await load('text_encoder.onnx'),
    ve: await load('vector_estimator.onnx'), voc: await load('vocoder.onnx'),
  };
  const styles = new Map();
  const styleOf = (v) => {
    const name = String(voiceOf(v) || 'M1').toUpperCase();
    if (!styles.has(name)) styles.set(name, makeStyle(ort, JSON.parse(readFileSync(join(MODEL, 'voice_styles', `${name}.json`), 'utf8'))));
    return styles.get(name);
  };
  const result = new Map();
  for (const clip of clips) {
    const pieces = [];
    let sr = 44100;
    for (const seg of clip.segments || []) {
      const chunks = chunkForModel(prepText(seg.text), 260);
      for (let k = 0; k < chunks.length; k++) {
        const r = await synthesizeOne(ort, m, styleOf(seg.voice), chunks[k], { lang: 'vi', steps: script.steps || 12, speed: seg.speed || script.speed || 1 });
        sr = r.sampleRate;
        // Supertonic leaves long holes between phrases: keep at most 0.32 s
        pieces.push({ pcm: trim(r.pcm, sr, 0.32), gapAfter: k < chunks.length - 1 ? 0.22 : (seg.pause ?? 0.45) });
      }
    }
    result.set(clip.id, { sr, pieces });
  }
  return result;
}

function renderVieneu(clips) {
  const py = process.env.VIENEU_PYTHON || join(homedir(), '.venvs/vieneu/bin/python');
  if (!existsSync(py)) {
    console.error(`Không thấy Python có gói vieneu ở ${py}.\nCài: python3 -m venv ~/.venvs/vieneu && ~/.venvs/vieneu/bin/pip install vieneu\nhoặc đặt VIENEU_PYTHON=/đường/dẫn/python`);
    process.exit(1);
  }
  const work = mkdtempSync(join(tmpdir(), 'gen-voice-'));
  const segments = clips.flatMap((clip) => (clip.segments || []).map((seg) => ({ voice: voiceOf(seg.voice), text: prepText(seg.text), temperature: seg.temperature ?? script.temperature ?? 0.8 })));
  console.log(`VieNeu: ${segments.length} đoạn, ${clips.length} clip…`);
  const out = execFileSync(py, ['-I', join(ROOT, 'tools', 'vieneu-synth.py')], {
    input: JSON.stringify({ out_dir: work, segments }), stdio: ['pipe', 'pipe', 'inherit'], maxBuffer: 1 << 26,
  });
  const { sample_rate: sr, files } = JSON.parse(String(out).trim().split('\n').pop());
  const result = new Map();
  let i = 0;
  for (const clip of clips) {
    const pieces = (clip.segments || []).map((seg) => ({ pcm: trim(readPcm(files[i++], sr), sr, 0.6), gapAfter: seg.pause ?? 0.45 }));
    result.set(clip.id, { sr, pieces });
  }
  rmSync(work, { recursive: true, force: true });
  return result;
}

const t0 = Date.now();
const rendered = engine === 'vieneu' ? renderVieneu(todo) : await renderSupertonic(todo);
for (const clip of todo) {
  const { sr, pieces } = rendered.get(clip.id);
  const parts = [new Float32Array(Math.round(sr * 0.25))];
  for (const p of pieces) parts.push(p.pcm, new Float32Array(Math.round(sr * p.gapAfter)));
  const total = parts.reduce((n, p) => n + p.length, 0);
  const pcm = new Float32Array(total);
  let o = 0; for (const p of parts) { pcm.set(p, o); o += p.length; }
  const wav = join(tmpdir(), `gen-voice-${caseId}-${clip.id}.wav`);
  writeFileSync(wav, encodeWav(pcm, sr));
  // loudness-normalise for speech; mono 64 kbps is plenty for a voice
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', wav, '-af', 'highpass=f=70,loudnorm=I=-17:TP=-1.5:LRA=9', '-ac', '1', '-ar', '44100', '-b:a', '64k', join(outDir, `${clip.id}.mp3`)]);
  rmSync(wav, { force: true });
  lock[clip.id] = clip.hash;
  console.log(`✓ ${clip.id}  ${(total / sr).toFixed(1)}s`);
}
writeFileSync(lockPath, JSON.stringify(lock, null, 2) + '\n');
console.log(`Đã tạo ${todo.length} clip (${engine}) trong public/cases/${caseId}/audio/ · ${((Date.now() - t0) / 1000).toFixed(0)}s`);
