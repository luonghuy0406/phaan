import { describe, it, expect, beforeEach } from 'vitest';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { presentEvidence, presentMany, buildMessages, buildOfficerTurn, buildSystemPrompt, sanitizeMessage, tidyReply, clampStage, lockedDocs, type CaseAi, type InterrogationState } from './interrogation.ts';
import { chat, _resetRests, AllModelsFailed } from './llm.ts';

const ROOT = join(__dirname, '..', '..', '..');
const loadAi = (id: string): CaseAi => {
  const ai = JSON.parse(readFileSync(join(ROOT, 'authoring', id, 'interrogation.json'), 'utf8'));
  const c = JSON.parse(readFileSync(join(ROOT, 'public', 'cases', id, 'case.json'), 'utf8'));
  return {
    ...ai,
    docTitles: Object.fromEntries(c.documents.map((d: { id: string; title: string }) => [d.id, d.title])),
    docStages: Object.fromEntries(c.documents.map((d: { id: string; stage?: number }) => [d.id, d.stage ?? 1])),
  };
};
const fresh = (): InterrogationState => ({ presented: [], admitted: [], turns: 0 });

describe('interrogation profiles', () => {
  const ids = readdirSync(join(ROOT, 'authoring')).filter((n) => existsSync(join(ROOT, 'authoring', n, 'interrogation.json')));
  it.each(ids)('%s: every document, lie and secret reference is valid', (id) => {
    const ai = loadAi(id);
    const c = JSON.parse(readFileSync(join(ROOT, 'public', 'cases', id, 'case.json'), 'utf8'));
    const suspects = new Set((c.suspects || []).map((s: { id: string }) => s.id));
    for (const [sid, p] of Object.entries(ai.suspects)) {
      expect(suspects.has(sid), `${sid} có trong case.json suspects`).toBe(true);
      const lieIds = p.lies.map((l) => l.id);
      expect(new Set(lieIds).size).toBe(lieIds.length);
      for (const l of p.lies) for (const d of l.breaksWith.flat()) expect(ai.docTitles[d], `${sid}/${l.id}: ${d}`).toBeTruthy();
      for (const d of Object.keys(p.reactions || {})) expect(ai.docTitles[d], `${sid} reaction ${d}`).toBeTruthy();
      for (const s of p.secrets || []) expect(lieIds).toContain(s.after);
      // a lie must be raised no later than the round that opens the documents breaking it
      for (const l of p.lies) for (const g of l.breaksWith) {
        expect(Math.max(...g.map((d) => ai.docStages![d])), `${sid}/${l.id}: stage`).toBeGreaterThanOrEqual(l.stage ?? 1);
      }
    }
  });
});

describe('round gating', () => {
  const ai = loadAi('con-nuoc-ram-thang-gieng');
  it('keeps Ba Thuyền quiet about diving, the wine and the debt in early rounds', () => {
    const early = buildSystemPrompt(ai, 'thuyen', fresh(), 2);
    expect(early).not.toMatch(/thuê lặn|ve rượu sang biếu|thế chấp|lặn sông giỏi|rễ nhàu/);
    expect(early).not.toMatch(/thợ lặn/);
    const r4 = buildSystemPrompt(ai, 'thuyen', fresh(), 4);
    expect(r4).toMatch(/thuê lặn tháo van lù/);
    expect(r4).toMatch(/rễ nhàu/);
    expect(r4).not.toMatch(/thế chấp/);
    expect(buildSystemPrompt(ai, 'thuyen', fresh(), 5)).toMatch(/thế chấp/);
  });
  it('Tư Lợi hides his ear injury until the medical record is shown', () => {
    const p = buildSystemPrompt(ai, 'loi', fresh(), 4);
    expect(p).not.toMatch(/Những điều bạn ĐÃ khai nhận/);
    const { state, broke } = presentEvidence(ai.suspects.loi, fresh(), 'd37');
    expect(broke.map((l) => l.id)).toEqual(['tai']);
    expect(buildSystemPrompt(ai, 'loi', state, 4)).toMatch(/thủng màng nhĩ/);
  });
  it('clamps the round and locks documents from later rounds', () => {
    expect(clampStage(ai, 3)).toBe(3);
    expect(clampStage(ai, 99)).toBe(5);
    expect(clampStage(ai, undefined)).toBe(5);
    expect(clampStage(ai, 0)).toBe(5);
    expect(lockedDocs(ai, ['d20', 'd33'], 3)).toEqual(['d33']);
    expect(lockedDocs(ai, ['d20'], 3)).toEqual([]);
  });
});

describe('presentEvidence (con-nuoc-ram-thang-gieng)', () => {
  const ai = loadAi('con-nuoc-ram-thang-gieng');
  const thuyen = ai.suspects.thuyen;

  it('breaks a lie only with the right document', () => {
    expect(presentEvidence(thuyen, fresh(), 'd05').broke).toEqual([]);
    const r = presentEvidence(thuyen, fresh(), 'd20');
    expect(r.broke.map((l) => l.id)).toEqual(['tren-do']);
    expect(r.state.presented).toEqual(['d20']);
  });

  it('the final confession needs two other admissions first', () => {
    let s = presentEvidence(thuyen, fresh(), 'd33').state;
    expect(s.admitted).toEqual([]);
    s = presentEvidence(thuyen, s, 'd20').state;
    s = presentEvidence(thuyen, s, 'd27').state;
    expect(s.admitted).toEqual(['tren-do', 'day-curoa']);
    // d33 was shown before: only showing it again (now) can trigger the confession
    expect(presentEvidence(thuyen, s, null).broke).toEqual([]);
    const r = presentEvidence(thuyen, s, 'd33');
    expect(r.broke.map((l) => l.id)).toEqual(['vo-can']);
  });

  it('an admitted lie does not break twice', () => {
    const s = presentEvidence(thuyen, fresh(), 'd20').state;
    expect(presentEvidence(thuyen, s, 'd21').broke).toEqual([]);
  });

  it('several documents at once break every lie they cover', () => {
    const r = presentMany(thuyen, fresh(), ['d20', 'd27', 'd05']);
    expect(r.broke.map((l) => l.id)).toEqual(['tren-do', 'day-curoa']);
    expect(r.state.presented).toEqual(['d20', 'd27', 'd05']);
    const t = buildOfficerTurn(ai, 'thuyen', '', ['d20', 'd27'], r.broke);
    expect(t).toContain('2 tài liệu');
  });

  it('lies with no documents can never break', () => {
    expect(presentEvidence(ai.suspects.sau, fresh(), 'd17').broke).toEqual([]);
  });

  it('prompt keeps the truth hidden and lists admissions once made', () => {
    const before = buildSystemPrompt(ai, 'thuyen', fresh());
    expect(before).toContain('KHÔNG BAO GIỜ tự nói ra');
    expect(before).not.toContain('ĐÃ khai nhận');
    const after = buildSystemPrompt(ai, 'thuyen', presentEvidence(thuyen, fresh(), 'd20').state);
    expect(after).toContain('ĐÃ khai nhận');
    expect(after).toContain(thuyen.lies[0].admission);
  });

  it('secrets unlock only after their lie is admitted', () => {
    const lanh = ai.suspects.lanh;
    expect(buildSystemPrompt(ai, 'lanh', fresh())).not.toContain('Mai kêu thằng Ba qua');
    const s = presentEvidence(lanh, fresh(), 'd23').state;
    expect(buildSystemPrompt(ai, 'lanh', s)).toContain('Mai kêu thằng Ba qua');
  });

  it('officer turn names the document and the verdict', () => {
    const r = presentEvidence(thuyen, fresh(), 'd20');
    const t = buildOfficerTurn(ai, 'thuyen', 'Giải thích đi.', 'd20', r.broke);
    expect(t).toContain(ai.docTitles.d20);
    expect(t).toContain('khai nhận');
    const msgs = buildMessages(ai, 'thuyen', r.state, [{ role: 'officer', text: 'a' }, { role: 'suspect', text: 'b' }], t);
    expect(msgs.map((m) => m.role)).toEqual(['system', 'user', 'assistant', 'user']);
  });
});

describe('text helpers', () => {
  it('sanitizes and caps officer input', () => {
    expect(sanitizeMessage('  a\n\nb  ')).toBe('a b');
    expect(sanitizeMessage('x'.repeat(1000)).length).toBe(400);
  });
  it('strips role labels and quotes from replies', () => {
    expect(tidyReply('Trần Văn Thuyền: "Tui ở trên đò."', 'Trần Văn Thuyền (Ba Thuyền)')).toBe('Tui ở trên đò.');
    expect(tidyReply('*(Cúi đầu)* Dạ, tui **hổng** biết.', 'X')).toBe('(Cúi đầu) Dạ, tui hổng biết.');
  });
});

describe('chat rotation', () => {
  beforeEach(() => _resetRests());
  const ok = (text: string) => new Response(JSON.stringify({ choices: [{ message: { content: text } }] }), { status: 200 });
  const models = [{ provider: 'gemini' as const, model: 'a' }, { provider: 'groq' as const, model: 'b' }];

  it('falls through to the next model on 429 and rests the failed one', async () => {
    const calls: string[] = [];
    const fetchFn = (async (_u: string, init: RequestInit) => {
      const m = JSON.parse(String(init.body)).model;
      calls.push(m);
      return m === 'a' ? new Response('{}', { status: 429 }) : ok('xin chào');
    }) as unknown as typeof fetch;
    const r = await chat([{ role: 'user', content: 'hi' }], { gemini: 'k', groq: 'k' }, { models, fetchFn });
    expect(r).toEqual({ text: 'xin chào', model: 'groq/b' });
    await chat([{ role: 'user', content: 'hi' }], { gemini: 'k', groq: 'k' }, { models, fetchFn });
    expect(calls).toEqual(['a', 'b', 'b']); // 'a' is resting, tried last only if needed
  });

  it('skips providers without a key and reports when everything fails', async () => {
    const fetchFn = (async () => new Response('{}', { status: 503 })) as unknown as typeof fetch;
    await expect(chat([{ role: 'user', content: 'hi' }], { groq: 'k' }, { models, fetchFn })).rejects.toBeInstanceOf(AllModelsFailed);
  });
});
