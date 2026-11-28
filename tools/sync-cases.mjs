#!/usr/bin/env node
// Nạp đáp án của mọi hồ sơ "available" vào bảng case_questions, để server chấm khi chơi nhóm.
// Chạy lại sau mỗi lần sửa câu hỏi:  npm run sync-cases
// Dùng SUPABASE_SECRET_KEY trong .env.local (khoá này bỏ qua RLS, chỉ chạy trên máy của bạn).
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { normalizeLine } from '../src/lib/checks.js';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

function readEnv() {
  const env = { ...process.env };
  for (const f of ['.env', '.env.local']) {
    const p = join(ROOT, f);
    if (!existsSync(p)) continue;
    for (const line of readFileSync(p, 'utf8').split('\n')) {
      const m = /^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/.exec(line);
      if (m && !line.trim().startsWith('#')) env[m[1]] = m[2];
    }
  }
  return env;
}

const env = readEnv();
const url = env.VITE_SUPABASE_URL;
const key = env.SUPABASE_SECRET_KEY;
if (!url || !key) {
  console.error('Thiếu VITE_SUPABASE_URL hoặc SUPABASE_SECRET_KEY trong .env.local');
  process.exit(1);
}
const headers = { apikey: key, 'Content-Type': 'application/json' };

function rowsFor(c) {
  return c.questions.map((q, i) => {
    let answer = q.answer || [];
    if (q.type === 'evidence') answer = [...new Set(answer.map(String))].sort();
    if (q.type === 'line') answer = answer.map(normalizeLine).filter(Boolean);
    if (q.type === 'choice') answer = [...new Set(answer.map(Number))].sort((a, b) => a - b);
    return {
      case_id: c.id,
      question_id: q.id,
      ord: i + 1,
      stage: q.stage ?? 1,
      type: q.type,
      answer,
      has_options: q.type !== 'choice' || (q.options || []).length > 0,
      hint_count: (q.hints || []).length,
      updated_at: new Date().toISOString(),
    };
  });
}

const casesDir = join(ROOT, 'public', 'cases');
const ids = readdirSync(casesDir).filter((n) => existsSync(join(casesDir, n, 'case.json')));
let failed = false;
for (const id of ids) {
  const c = JSON.parse(readFileSync(join(casesDir, id, 'case.json'), 'utf8'));
  if (c.status !== 'available') { console.log(`- ${id}: bỏ qua (${c.status})`); continue; }
  const rows = rowsFor(c);
  const up = await fetch(`${url}/rest/v1/case_questions?on_conflict=case_id,question_id`, {
    method: 'POST',
    headers: { ...headers, Prefer: 'resolution=merge-duplicates,return=minimal' },
    body: JSON.stringify(rows),
  });
  if (!up.ok) {
    failed = true;
    console.error(`✗ ${id}: ${up.status} ${await up.text()}`);
    continue;
  }
  // drop questions that no longer exist in the case file
  const keep = rows.map((r) => `"${r.question_id}"`).join(',');
  const del = await fetch(`${url}/rest/v1/case_questions?case_id=eq.${encodeURIComponent(id)}&question_id=not.in.(${encodeURIComponent(keep)})`, {
    method: 'DELETE', headers,
  });
  if (!del.ok) { failed = true; console.error(`✗ ${id}: xoá câu cũ lỗi ${del.status} ${await del.text()}`); continue; }
  // AI interrogation profiles (contain the solution): authoring/<id>/interrogation.json → case_ai, service role only
  const aiPath = join(ROOT, 'authoring', id, 'interrogation.json');
  const examPath = join(ROOT, 'authoring', id, 'conclusion.json');
  let aiNote = '';
  if (existsSync(aiPath) || existsSync(examPath)) {
    const ai = existsSync(aiPath) ? JSON.parse(readFileSync(aiPath, 'utf8')) : { world: c.setting || '', style: '', suspects: {} };
    delete ai._ghi_chu;
    // conclusion report to the AI prosecutor: rubric per question id (the question carries "exam" in case.json)
    if (existsSync(examPath)) {
      const exams = JSON.parse(readFileSync(examPath, 'utf8'));
      delete exams._ghi_chu;
      const qids = new Set(c.questions.filter((q) => q.exam).map((q) => q.id));
      const badQ = Object.keys(exams).filter((k) => !qids.has(k));
      if (badQ.length) { failed = true; console.error(`✗ ${id}: conclusion.json có câu không mang "exam" trong case.json: ${badQ.join(', ')}`); continue; }
      ai.exams = exams;
    }
    ai.docTitles = Object.fromEntries(c.documents.map((d) => [d.id, d.title]));
    ai.docStages = Object.fromEntries(c.documents.map((d) => [d.id, d.stage ?? 1]));
    const known = new Set(c.documents.map((d) => d.id));
    const bad = Object.values(ai.suspects).flatMap((sp) => [...sp.lies.flatMap((l) => l.breaksWith.flat()), ...Object.keys(sp.reactions || {})]).filter((d) => !known.has(d));
    if (bad.length) { failed = true; console.error(`✗ ${id}: interrogation.json nhắc tài liệu không có: ${[...new Set(bad)].join(', ')}`); continue; }
    const r = await fetch(`${url}/rest/v1/case_ai?on_conflict=case_id`, {
      method: 'POST',
      headers: { ...headers, Prefer: 'resolution=merge-duplicates,return=minimal' },
      body: JSON.stringify([{ case_id: id, data: ai, updated_at: new Date().toISOString() }]),
    });
    if (!r.ok) { failed = true; console.error(`✗ ${id}: case_ai ${r.status} ${await r.text()}`); continue; }
    aiNote = `, thẩm vấn AI: ${Object.keys(ai.suspects).length} nghi phạm${ai.exams ? `, báo cáo kết luận: ${Object.keys(ai.exams).join(', ')}` : ''}`;
  }
  console.log(`✓ ${id}: ${rows.length} câu hỏi${aiNote}`);
}
process.exit(failed ? 1 : 0);
