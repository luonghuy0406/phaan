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
  console.log(`✓ ${id}: ${rows.length} câu hỏi`);
}
process.exit(failed ? 1 : 0);
