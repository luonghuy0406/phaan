#!/usr/bin/env node
// Tạo sẵn giọng đọc cho TÀI LIỆU của một hồ sơ bằng VieNeu-TTS (cùng engine với lời dẫn chuyện).
//
//   node tools/gen-doc-voice.mjs <case-id> [doc-id …] [--force] [--dry]
//
// Mỗi khối chữ trên tờ giấy (khoá giống papers.tsx: hd, dk, f0, p0, s0, s0p1, l3, it0, tot, ft0, cap, date, gr, sig)
// thành một file `public/cases/<id>/audio/read/<doc>/<khoá>.mp3`, cộng vài phần chỉ dùng khi đọc cả tài liệu
// (_t tiêu đề, _d dòng "Vào hồi…"). Danh sách theo thứ tự đọc ghi trong `audio/read/index.json`.
// Bàn điều tra phát các file này khi bấm "Đọc toàn bộ tài liệu" / "Đọc đoạn này"; không có file thì quay về đọc trực tiếp.
//
// Cấu hình trong `authoring/<id>/voice.json`, mục "docs":
//   "docs": { "narrator": "dan", "asker": "danh", "speakers": { "Trần Văn Thuyền": "thuyen", "Nguyễn Thị Lành": "Thục Đoan" } }
// (tên vai lấy từ "voices", hoặc ghi thẳng tên giọng VieNeu). Cài VieNeu: xem đầu tools/gen-voice.mjs.
// Tài liệu viết bằng `content` (Markdown) chưa được hỗ trợ: vẫn đọc trực tiếp như cũ.
import { readFileSync, writeFileSync, existsSync, mkdirSync, rmSync, mkdtempSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { tmpdir, homedir } from 'node:os';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const force = args.includes('--force');
const dry = args.includes('--dry');
const [caseId, ...only] = args.filter((a) => !a.startsWith('--'));
if (!caseId) { console.log('Dùng: node tools/gen-doc-voice.mjs <case-id> [doc-id …] [--force] [--dry]'); process.exit(2); }

const caseDir = join(ROOT, 'public', 'cases', caseId);
const c = JSON.parse(readFileSync(join(caseDir, 'case.json'), 'utf8'));
const vPath = join(ROOT, 'authoring', caseId, 'voice.json');
const vcfg = existsSync(vPath) ? JSON.parse(readFileSync(vPath, 'utf8')) : {};
const dcfg = vcfg.docs || {};
const voiceOf = (v) => vcfg.voices?.[v] || v;
const NARRATOR = voiceOf(dcfg.narrator || 'dan');
const ASKER_VOICE = voiceOf(dcfg.asker || dcfg.narrator || 'dan');
const speakerVoice = (name) => voiceOf(dcfg.speakers?.[name] || dcfg.narrator || 'dan');
const { normalizeVi } = await import('../src/lib/vi-normalize.ts');

/* ── what the paper shows (mirror of src/board/papers.tsx) ── */
const docNo = new Map(c.documents.map((d, i) => [d.id, d.no ?? i + 1]));
const show = (s) => String(s ?? '')
  .replace(/\*\*|__|~~/g, '')
  .replace(/\bd\d{2,3}[a-z]?\b/g, (id) => (docNo.has(id) ? `Tài liệu ${String(docNo.get(id)).padStart(2, '0')}` : id))
  .replace(/\s+/g, ' ').trim();
const ASKER = /^(hỏi|câu hỏi|đtv|điều tra viên|cán bộ|thanh tra|kiểm sát viên|công an|trinh sát|cảnh sát|thẩm phán)/i;
const parseSig = (t) => { if (!t) return null; const m = /^([^:]+):\s*(.+)$/.exec(t); return m ? { role: m[1].trim(), name: m[2].trim() } : { role: '', name: t.trim() }; };
const signText = (d) => {
  const list = d.signers?.length ? d.signers : d.signature ? [parseSig(d.signature)] : [];
  return list.map((s) => (s.role ? `${s.role}: ${s.name}` : s.name)).join('. ');
};

/** Ordered pieces to read for one document: { k, text, voice, pause }. Keys starting with "_" are not paper blocks. */
function pieces(d) {
  if (typeof d.content === 'string' && d.content.trim()) return null;
  const out = [];
  const add = (k, text, voice = NARRATOR, pause = 0.5) => { const t = show(text); if (t) out.push({ k, text: t, voice, pause }); };
  const fields = (d.fields || []).forEach.bind(d.fields || []);
  const when = () => { if (d.date) add('_d', /^\s*\d/.test(d.date) ? `Vào hồi ${d.date}` : d.date); };
  switch (d.type) {
    case 'newspaper':
      add('hd', d.headline || d.title, NARRATOR, 0.7); add('dk', d.deck);
      if (d.imageCaption) add('cap', d.imageCaption);
      (d.paragraphs || []).forEach((p, i) => add(`p${i}`, p));
      break;
    case 'report':
      add('_t', d.heading || d.title, NARRATOR, 0.7); when();
      fields((f, i) => add(`f${i}`, `${f.label}: ${f.value}`, NARRATOR, 0.35));
      if (d.imageCaption) add('cap', d.imageCaption);
      (d.sections || []).forEach((s, i) => { add(`s${i}`, s.heading, NARRATOR, 0.45); (s.paragraphs || []).forEach((p, j) => add(`s${i}p${j}`, p)); });
      add('sig', signText(d));
      break;
    case 'testimony': {
      add('_t', d.title, NARRATOR, 0.7); when();
      fields((f, i) => add(`f${i}`, `${f.label}: ${f.value}`, NARRATOR, 0.35));
      if (d.imageCaption) add('cap', d.imageCaption);
      (d.lines || []).forEach((l) => {
        const aside = /^\(.*\)$/.test(l.text.trim());
        const voice = aside ? NARRATOR : l.speaker && ASKER.test(l.speaker) ? ASKER_VOICE : speakerVoice(l.speaker);
        add(`l${l.n}`, aside ? l.text.trim().slice(1, -1) : l.text, voice, 0.45);
      });
      break;
    }
    case 'photo':
      add('_t', d.title, NARRATOR, 0.6); add('cap', d.caption);
      break;
    case 'letter':
      add('_t', d.title, NARRATOR, 0.7); add('date', d.date); add('gr', d.greeting);
      (d.paragraphs || []).forEach((p, i) => add(`p${i}`, p)); add('sig', d.signature);
      break;
    case 'receipt':
      add('_t', d.title, NARRATOR, 0.7);
      fields((f, i) => add(`f${i}`, `${f.label}: ${f.value}`, NARRATOR, 0.35));
      (d.items || []).forEach((it, i) => add(`it${i}`, `${it.name}, số lượng ${it.qty ?? 1}, ${it.price || ''}`, NARRATOR, 0.35));
      if (d.total) add('tot', `Tổng: ${d.total}`);
      (d.footer || []).forEach((f, i) => add(`ft${i}`, f));
      break;
    case 'evidence':
      add('_t', d.title, NARRATOR, 0.7);
      if (d.imageCaption) add('cap', d.imageCaption);
      fields((f, i) => add(`f${i}`, `${f.label}: ${f.value}`, NARRATOR, 0.35));
      (d.paragraphs || []).forEach((p, i) => add(`p${i}`, p));
      break;
    case 'scan':
      add('_t', d.title, NARRATOR, 0.6); add('cap', d.caption);
      break;
    case 'people': {
      add('_t', d.title, NARRATOR, 0.7);
      (d.paragraphs || []).forEach((p, i) => add(`p${i}`, p));
      const persons = [...(c.victim ? [{ ...c.victim, victim: true }] : []), ...(c.suspects || [])];
      let n = 0;
      persons.forEach((p, i) => {
        const head = p.victim ? 'Nạn nhân' : `Nghi phạm số ${++n}`;
        const who = [p.name + (p.alias ? `, thường gọi ${p.alias}` : ''), p.age ? `${p.age} tuổi` : '', p.role].filter(Boolean).join(', ');
        add(`pp${i}`, `${head}: ${who}. ${(p.victim ? p.note : p.suspicion) || ''}`, NARRATOR, 0.6);
      });
      break;
    }
    default: // note
      add('_t', d.title, NARRATOR, 0.7);
      if (d.imageCaption) add('cap', d.imageCaption);
      (d.paragraphs || []).forEach((p, i) => add(`p${i}`, p)); add('sig', d.signature);
  }
  return out;
}

const docs = c.documents.filter((d) => !only.length || only.includes(d.id));
if (dry) {
  for (const d of docs) {
    const list = pieces(d);
    console.log(`\n■ ${d.id} · ${d.title}${list ? '' : '  (content: đọc trực tiếp)'}`);
    (list || []).forEach((p) => console.log(`  ${p.k.padEnd(6)} [${p.voice}] ${p.text}`));
  }
  process.exit(0);
}

/* ── synthesis (VieNeu, batched in one process) ── */
const readDir = join(caseDir, 'audio', 'read');
mkdirSync(readDir, { recursive: true });
const lockPath = join(ROOT, 'authoring', caseId, 'doc-voice.lock.json');
const lock = existsSync(lockPath) ? JSON.parse(readFileSync(lockPath, 'utf8')) : {};
const indexPath = join(readDir, 'index.json');
const index = existsSync(indexPath) ? JSON.parse(readFileSync(indexPath, 'utf8')) : { v: 1, docs: {} };

const prep = (t) => normalizeVi(t);
const hashOf = (p) => createHash('sha256').update(JSON.stringify([p.text, p.voice, vcfg.temperature ?? 0.8])).digest('hex').slice(0, 12);
const jobs = [];
for (const d of docs) {
  const list = pieces(d);
  if (!list) { delete index.docs[d.id]; continue; }
  index.docs[d.id] = list.map((p) => ({ k: p.k, p: p.pause }));
  for (const p of list) {
    const file = join(readDir, d.id, `${p.k}.mp3`);
    const h = hashOf(p);
    if (!force && lock[`${d.id}/${p.k}`] === h && existsSync(file)) continue;
    jobs.push({ doc: d.id, k: p.k, file, h, voice: p.voice, text: prep(p.text) });
  }
  // drop files of blocks that no longer exist
  const keep = new Set(list.map((p) => `${p.k}.mp3`));
  if (existsSync(join(readDir, d.id))) for (const f of readdirSync(join(readDir, d.id))) if (!keep.has(f)) rmSync(join(readDir, d.id, f));
}
console.log(`${jobs.length} khối cần tạo (${docs.length} tài liệu).`);

if (jobs.length) {
  const py = process.env.VIENEU_PYTHON || join(homedir(), '.venvs/vieneu/bin/python');
  if (!existsSync(py)) { console.error(`Không thấy Python có gói vieneu ở ${py}. Cài: python3 -m venv ~/.venvs/vieneu && ~/.venvs/vieneu/bin/pip install vieneu`); process.exit(1); }
  const work = mkdtempSync(join(tmpdir(), 'gen-doc-voice-'));
  const t0 = Date.now();
  const out = execFileSync(py, ['-I', join(ROOT, 'tools', 'vieneu-synth.py')], {
    input: JSON.stringify({ out_dir: work, segments: jobs.map((j) => ({ voice: j.voice, text: j.text, temperature: vcfg.temperature ?? 0.8 })) }),
    stdio: ['pipe', 'pipe', 'inherit'], maxBuffer: 1 << 26,
  });
  const { files } = JSON.parse(String(out).trim().split('\n').pop());
  jobs.forEach((j, i) => {
    mkdirSync(dirname(j.file), { recursive: true });
    // trim edge silence, loudness-normalise like the narration, mono 48 kbps
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', files[i], '-af',
      'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.12,areverse,highpass=f=70,loudnorm=I=-17:TP=-1.5:LRA=9',
      '-ac', '1', '-ar', '44100', '-b:a', '48k', j.file]);
    lock[`${j.doc}/${j.k}`] = j.h;
  });
  rmSync(work, { recursive: true, force: true });
  console.log(`Đã tạo ${jobs.length} file trong ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
writeFileSync(lockPath, JSON.stringify(lock, null, 2) + '\n');
writeFileSync(indexPath, JSON.stringify(index) + '\n');
console.log(`Ghi ${indexPath.replace(ROOT + '/', '')}`);
