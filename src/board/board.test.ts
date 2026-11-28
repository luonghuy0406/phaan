import { describe, expect, it } from 'vitest';
import { boundsOf, localToWorld, worldToLocal, type Box } from './geometry';
import { hitStroke, strokePath, type Stroke } from './ink';
import { sanitize, stageOpen, currentQ } from './store';
import { check, normalizeLine } from '../lib/checks.js';
import type { CaseData } from '../lib/types';
import { chunkText, extractDocText } from '../lib/tts';

describe('geometry', () => {
  const box: Box = { x: 100, y: 50, w: 200, h: 100, r: 0 };
  it('round-trips local ↔ world for every quarter turn', () => {
    for (let r = 0; r < 4; r++) {
      const b = { ...box, r };
      for (const [lx, ly] of [[0, 0], [200, 0], [37, 81], [200, 100]]) {
        const w = localToWorld(lx, ly, b);
        const l = worldToLocal(w.x, w.y, b);
        expect(l.x).toBeCloseTo(lx);
        expect(l.y).toBeCloseTo(ly);
      }
    }
  });
  it('matches CSS rotate(90deg) around the centre (clockwise)', () => {
    // top-left corner of a 200×100 paper turned 90° clockwise ends at the top-right of the turned box
    const w = localToWorld(0, 0, { ...box, r: 1 });
    expect(w).toEqual({ x: 250, y: 0 });
    expect(boundsOf({ ...box, r: 1 })).toEqual({ x: 150, y: 0, w: 100, h: 200 });
  });
});

describe('ink', () => {
  const s: Stroke = { id: 'k1', t: 'world', pts: [0, 0, 0.5, 100, 0, 0.5], c: '#000000', s: 4 };
  it('hit-tests along the stroke', () => {
    expect(hitStroke(s, 50, 3, 2)).toBe(true);
    expect(hitStroke(s, 50, 20, 2)).toBe(false);
  });
  it('builds a closed svg path', () => {
    expect(strokePath(s)).toMatch(/^M.*Z$/);
  });
});

const CASE: CaseData = {
  id: 't', no: 1, status: 'available', title: 'T',
  documents: [
    { id: 'd1', stage: 1, type: 'report', title: 'a' },
    { id: 'd2', stage: 1, type: 'testimony', title: 'b', lines: [{ n: 4, text: 'x' }] },
    { id: 'd3', stage: 2, type: 'note', title: 'c' },
  ],
  questions: [
    { id: 'q1', stage: 1, type: 'evidence', title: '', answer: ['d1', 'd2'], need: 2, nudges: [{ any: ['d3'], message: 'no' }] },
    { id: 'q2', stage: 2, type: 'line', title: '', answer: ['d2:004'] },
  ],
};

describe('answer checks', () => {
  it('evidence: order does not matter, nudges apply', () => {
    expect(check(CASE.questions[0], ['d2', 'd1']).status).toBe('correct');
    expect(check(CASE.questions[0], ['d1']).status).toBe('incomplete');
    expect(check(CASE.questions[0], ['d1', 'd3']).message).toBe('no');
  });
  it('line: normalises numbers', () => {
    expect(normalizeLine('d2:4')).toBe('d2:004');
    expect(check(CASE.questions[1], 'd2:4').status).toBe('correct');
  });
});

describe('saved state', () => {
  it('drops unknown ids, bad strokes and out-of-order solves', () => {
    const s = sanitize({
      docs: { d1: { x: 1, y: 2, z: 3, r: 9 }, nope: { x: 0, y: 0, z: 1, r: 0 } },
      notes: [{ id: 'n1', x: 10, y: 20, z: 2, text: 'hi' }],
      strings: [
        { id: 's1', a: { doc: 'd1', key: 'p0', x: 120.4, y: 240.6 }, b: { note: 'n1', x: 45, y: 80 } },
        { id: 's2', a: { doc: 'd1' }, b: { doc: 'nope' } },
      ],
      ink: [
        { id: 'kok', t: 'doc:d1', pts: [1, 2, 0.5], c: '#112233', s: 3 },
        { id: 'kbad', t: 'doc:zz', pts: [1, 2, 0.5], c: '#112233', s: 3 },
        { id: 'kxss', t: 'world', pts: [1, 2, 0.5], c: 'red;}', s: 3 },
      ],
      q: { q1: { solved: false }, q2: { solved: true, line: 'd2:4' } },
    }, CASE);
    expect(Object.keys(s.docs)).toEqual(['d1']);
    expect(s.docs.d1.r).toBe(3);
    expect(s.strings).toEqual([{ id: 's1', a: { doc: 'd1', key: 'p0', x: 120, y: 241 }, b: { note: 'n1', x: 45, y: 80 } }]);
    expect(s.ink.map((k) => k.id)).toEqual(['kok']);
    expect(s.q.q2.solved).toBe(false);
    expect(s.q.q2.line).toBe('d2:004');
  });
  it('opens stages in order', () => {
    const s = sanitize({ q: { q1: { solved: true } } }, CASE);
    expect(stageOpen(CASE, s, 2)).toBe(true);
    expect(currentQ(CASE, s)?.id).toBe('q2');
  });
});

describe('TTS (text-to-speech)', () => {
  it('chunks text by sentence boundaries without exceeding max chunk size', () => {
    const short = 'Chào bạn. Đây là đoạn ngắn.';
    expect(chunkText(short)).toEqual([short]);

    const longSentence = 'Câu thứ nhất rất dài và có nhiều thông tin chi tiết cần phải truyền đạt đến người nghe một cách mạch lạc. '.repeat(6);
    const chunks = chunkText(longSentence);
    expect(chunks.length).toBeGreaterThan(1);
    chunks.forEach((c) => {
      expect(c.length).toBeLessThanOrEqual(400);
      expect(c.length).toBeGreaterThan(0);
    });
  });

  it('extracts plain text from complex documents', () => {
    const doc = {
      type: 'testimony',
      title: 'Biên bản lấy lời khai',
      fields: [{ label: 'Nhân chứng', value: 'Nguyễn Văn A' }],
      lines: [
        { n: 1, speaker: 'Điều tra viên', text: 'Ông ở đâu vào lúc **20:00**?' },
        { n: 2, speaker: 'Nguyễn Văn A', text: 'Tôi ở nhà đọc sách.' },
      ],
      signature: 'Ký tên A',
    };
    const extracted = extractDocText(doc);
    expect(extracted).toContain('Biên bản lấy lời khai');
    expect(extracted).toContain('Nhân chứng: Nguyễn Văn A');
    expect(extracted).toContain('Điều tra viên: Ông ở đâu vào lúc 20:00?');
    expect(extracted).not.toContain('**');
  });
});
