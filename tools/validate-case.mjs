#!/usr/bin/env node
// Kiểm định hồ sơ vụ án.  node tools/validate-case.mjs demo-01   |   node tools/validate-case.mjs --all
// Exit code 1 if any error. Warnings do not fail.
import { readFileSync, existsSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { check, normalizeLine } from '../src/lib/checks.js';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const TYPES = ['newspaper', 'report', 'testimony', 'photo', 'letter', 'receipt', 'evidence', 'note', 'scan'];
const QTYPES = ['evidence', 'line', 'choice'];
const ID = /^[a-z0-9-]{1,60}$/;
const DOC_ID = /^[a-z0-9-]{1,40}$/;
const IMG_EXT = /\.(webp|jpe?g|png|avif)$/i;

function validate(id) {
  const errors = [];
  const warns = [];
  const err = (m) => errors.push(m);
  const warn = (m) => warns.push(m);
  const dir = join(ROOT, 'public', 'cases', id);
  const file = join(dir, 'case.json');
  if (!existsSync(file)) return { errors: [`Không có ${file}`], warns };
  let c;
  try { c = JSON.parse(readFileSync(file, 'utf8')); } catch (e) { return { errors: [`JSON lỗi: ${e.message}`], warns }; }

  if (c.id !== id) err(`"id" phải là "${id}" (đang là "${c.id}")`);
  for (const k of ['title', 'status', 'synopsis', 'intro', 'documents', 'questions', 'finale']) if (c[k] == null) err(`Thiếu trường "${k}"`);
  if (!['available', 'coming-soon'].includes(c.status)) err('"status" phải là "available" hoặc "coming-soon"');
  if (!Number.isInteger(c.difficulty) || c.difficulty < 1 || c.difficulty > 5) warn('"difficulty" nên là số nguyên 1–5');

  const imageRef = (where, src) => {
    if (src == null) { warn(`${where}: chưa có ảnh (đang hiển thị khung chờ)`); return; }
    if (typeof src !== 'string' || src.startsWith('/') || src.includes('..') || /^https?:/i.test(src)) { err(`${where}: đường dẫn ảnh phải là tương đối trong thư mục hồ sơ, ví dụ "images/x.webp"`); return; }
    if (!IMG_EXT.test(src)) warn(`${where}: nên dùng .webp`);
    const p = join(dir, src);
    if (!existsSync(p)) err(`${where}: không tìm thấy file ${src}`);
    else if (statSync(p).size > 600 * 1024) warn(`${where}: ${src} nặng ${(statSync(p).size / 1024).toFixed(0)} KB (nên < 400 KB)`);
  };
  if (c.cover !== undefined) imageRef('cover', c.cover);

  const docs = Array.isArray(c.documents) ? c.documents : [];
  const docIds = new Set();
  const lines = new Set();
  const stageOf = new Map();
  docs.forEach((d, i) => {
    const w = `documents[${i}]${d && d.id ? ` (${d.id})` : ''}`;
    if (!d || !DOC_ID.test(d.id || '')) { err(`${w}: "id" thiếu hoặc sai dạng (a-z, 0-9, -)`); return; }
    if (docIds.has(d.id)) err(`${w}: trùng id`);
    docIds.add(d.id);
    if (!TYPES.includes(d.type)) err(`${w}: "type" phải là một trong ${TYPES.join(', ')}`);
    if (!d.title) err(`${w}: thiếu "title"`);
    const stage = d.stage ?? 1;
    if (!Number.isInteger(stage) || stage < 1) err(`${w}: "stage" phải là số nguyên ≥ 1`);
    stageOf.set(d.id, stage);
    if (d.type === 'testimony') {
      const seen = new Set();
      (d.lines || []).forEach((l) => {
        if (!Number.isInteger(l.n) || l.n < 1 || l.n > 999) err(`${w}: dòng có "n" không hợp lệ`);
        if (seen.has(l.n)) err(`${w}: trùng số dòng ${l.n}`);
        seen.add(l.n);
        if (!l.text) err(`${w}: dòng ${l.n} không có nội dung`);
        lines.add(normalizeLine(`${d.id}:${l.n}`));
      });
      if (!seen.size) err(`${w}: lời khai cần có "lines"`);
    }
    // something the player can actually read on the paper
    const hasBody = (typeof d.content === 'string' && d.content.trim()) || d.paragraphs?.length || d.lines?.length
      || d.sections?.length || d.fields?.length || d.items?.length || d.caption || d.imageCaption || d.image || d.headline || d.deck;
    if (!hasBody) err(`${w}: tài liệu không có nội dung hiển thị (cần "content", "paragraphs", "lines", "sections"… xem docs/case-schema.md)`);
    if (d.content !== undefined && typeof d.content !== 'string') err(`${w}: "content" phải là chuỗi`);
    if (['photo', 'scan'].includes(d.type) || d.image !== undefined) imageRef(`${w}.image`, d.image);
    if (d.imageHi !== undefined) imageRef(`${w}.imageHi`, d.imageHi);
    if (d.file !== undefined) {
      if (typeof d.file !== 'string' || d.file.startsWith('/') || d.file.includes('..')) err(`${w}: "file" phải là đường dẫn tương đối trong thư mục hồ sơ`);
      else if (!existsSync(join(dir, d.file))) err(`${w}: không tìm thấy file ${d.file}`);
    }
    const text = JSON.stringify(d);
    if (/<[a-z/][^>]*>/i.test(text)) err(`${w}: không được dùng thẻ HTML, chỉ dùng **đậm**, __gạch chân__, ~~gạch xoá~~`);
  });

  const stages = [...new Set(docs.map((d) => d.stage ?? 1))].sort((a, b) => a - b);
  stages.forEach((s, i) => { if (s !== i + 1) err(`Các trọng điểm phải liên tục 1, 2, 3… (đang có ${stages.join(', ')})`); });

  const qs = Array.isArray(c.questions) ? c.questions : [];
  const qIds = new Set();
  let lastStage = 1;
  qs.forEach((q, i) => {
    const w = `questions[${i}]${q && q.id ? ` (${q.id})` : ''}`;
    if (!q || !/^[a-z0-9-]{1,30}$/.test(q.id || '')) { err(`${w}: "id" thiếu hoặc sai dạng`); return; }
    if (qIds.has(q.id)) err(`${w}: trùng id`);
    qIds.add(q.id);
    if (!QTYPES.includes(q.type)) err(`${w}: "type" phải là ${QTYPES.join(' | ')}`);
    if (!q.title) err(`${w}: thiếu "title"`);
    const st = q.stage ?? 1;
    if (st < lastStage) err(`${w}: câu hỏi phải xếp theo trọng điểm tăng dần`);
    lastStage = st;
    if (!stages.includes(st)) err(`${w}: stage ${st} không có tài liệu nào`);
    const visible = (docId) => (stageOf.get(docId) ?? 99) <= st;
    if (!Array.isArray(q.hints) || q.hints.length < 2) warn(`${w}: nên có 2–3 gợi ý tăng dần`);
    if (!Array.isArray(q.explanation) || !q.explanation.length) warn(`${w}: nên có "explanation"`);

    if (q.type === 'evidence') {
      const ans = q.answer || [];
      if (!ans.length) err(`${w}: thiếu "answer"`);
      ans.forEach((a) => { if (!docIds.has(a)) err(`${w}: answer "${a}" không phải id tài liệu`); else if (!visible(a)) err(`${w}: answer "${a}" chưa hiện ở trọng điểm ${st}`); });
      if (q.need && q.need !== ans.length) err(`${w}: "need" (${q.need}) phải bằng số đáp án (${ans.length})`);
      (q.nudges || []).forEach((n, k) => {
        const ids = n.picks || n.any || [];
        if (!ids.length) err(`${w}: nudges[${k}] cần "picks" hoặc "any"`);
        ids.forEach((x) => { if (!docIds.has(x)) err(`${w}: nudges[${k}] tham chiếu "${x}" không tồn tại`); });
        if (n.picks && check(q, n.picks).status === 'correct') err(`${w}: nudges[${k}] trùng với đáp án đúng`);
        if (!n.message) err(`${w}: nudges[${k}] thiếu "message"`);
      });
      if (check(q, ans).status !== 'correct') err(`${w}: đáp án không vượt qua chính hàm kiểm tra`);
    }
    if (q.type === 'line') {
      const ans = (q.answer || []).map(normalizeLine);
      if (!ans.length) err(`${w}: thiếu "answer" dạng "dXX:NNN"`);
      ans.forEach((a, k) => {
        if (!a || !lines.has(a)) err(`${w}: answer "${(q.answer || [])[k]}" không trỏ tới dòng lời khai có thật`);
        else if (!visible(a.split(':')[0])) err(`${w}: dòng ${a} chưa hiện ở trọng điểm ${st}`);
      });
      Object.keys(q.nudges || {}).forEach((k) => { if (!lines.has(normalizeLine(k))) err(`${w}: nudge "${k}" không trỏ tới dòng có thật`); });
    }
    if (q.type === 'choice') {
      const n = (q.options || []).length;
      if (n && n < 2) err(`${w}: cần ít nhất 2 lựa chọn`);
      (q.answer || []).forEach((a) => { if (!Number.isInteger(a) || a < 0 || a >= n) err(`${w}: answer ${a} ngoài phạm vi options`); });
      if (n && !(q.answer || []).length) err(`${w}: thiếu "answer"`);
      if (!q.multiple && (q.answer || []).length > 1) err(`${w}: nhiều đáp án thì phải đặt "multiple": true`);
      if (n && check(q, q.answer).status !== 'correct') err(`${w}: đáp án không vượt qua chính hàm kiểm tra`);
    }
  });
  if (!qs.length) err('Cần ít nhất 1 câu hỏi');
  const maxDocStage = Math.max(1, ...stages);
  const maxQStage = Math.max(1, ...qs.map((q) => q.stage ?? 1));
  if (maxQStage < maxDocStage) err(`Tài liệu ở trọng điểm ${maxDocStage} không bao giờ được dùng: câu hỏi cuối chỉ ở trọng điểm ${maxQStage}`);
  for (let s = 1; s < maxDocStage; s++) if (!qs.some((q) => (q.stage ?? 1) === s)) err(`Trọng điểm ${s} không có câu hỏi nào, nên trọng điểm ${s + 1} sẽ tự mở`);

  // catalog consistency
  try {
    const cat = JSON.parse(readFileSync(join(ROOT, 'public', 'cases', 'index.json'), 'utf8')).cases || [];
    const entry = cat.find((e) => e.id === id);
    if (!entry) err('Chưa có trong cases/index.json');
    else for (const k of ['title', 'status', 'no']) if (entry[k] !== c[k]) warn(`index.json: "${k}" khác case.json (${JSON.stringify(entry[k])} ≠ ${JSON.stringify(c[k])})`);
  } catch { err('cases/index.json lỗi'); }

  // images in the case folder that nothing points to: they still ship to the website
  const used = new Set([c.cover, ...docs.flatMap((d) => [d && d.image, d && d.imageHi, d && d.file])].filter((x) => typeof x === 'string'));
  const walk = (rel) => readdirSync(join(dir, rel), { withFileTypes: true }).flatMap((e) => (e.isDirectory() ? walk(`${rel}/${e.name}`) : [`${rel}/${e.name}`]));
  if (existsSync(join(dir, 'images'))) {
    for (const f of walk('images')) if (!used.has(f) && !f.endsWith('.DS_Store')) warn(`${f}: không tài liệu nào dùng ảnh này (vẫn bị đưa lên web, ${(statSync(join(dir, f)).size / 1024).toFixed(0)} KB)`);
  }
  return { errors, warns, stats: { docs: docs.length, stages: stages.length, questions: qs.length } };
}

const arg = process.argv[2];
if (!arg) { console.log('Dùng: node tools/validate-case.mjs <case-id> | --all'); process.exit(2); }
const ids = arg === '--all'
  ? readdirSync(join(ROOT, 'public', 'cases')).filter((n) => ID.test(n) && existsSync(join(ROOT, 'public', 'cases', n, 'case.json')))
  : [arg];
let failed = false;
for (const id of ids) {
  const { errors, warns, stats } = validate(id);
  console.log(`\n■ ${id}${stats ? `  (${stats.docs} tài liệu · ${stats.stages} trọng điểm · ${stats.questions} câu hỏi)` : ''}`);
  errors.forEach((m) => console.log(`  ✗ ${m}`));
  warns.forEach((m) => console.log(`  ! ${m}`));
  if (!errors.length) console.log(`  ✓ Hợp lệ${warns.length ? ` (${warns.length} cảnh báo)` : ''}`);
  if (errors.length) failed = true;
}
process.exit(failed ? 1 : 0);
