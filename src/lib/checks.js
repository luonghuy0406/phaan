// Pure answer checks (no DOM). Plain JS so tools/validate-case.mjs can import it with plain Node.
// Each returns { status: 'correct' | 'near' | 'wrong' | 'incomplete', message }.

const uniqSorted = (list) => [...new Set((Array.isArray(list) ? list : []).filter(Boolean).map(String))].sort();
const sameList = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);

// evidence: the player pins `need` documents. Nudges are checked in order, first match wins:
//   { "picks": ["d01","d02"] } exact set     { "any": ["d05"] } contains at least one of
export function checkEvidence(picks, q) {
  const chosen = uniqSorted(picks);
  const need = q.need || (q.answer || []).length;
  if (chosen.length < need) {
    return { status: 'incomplete', message: q.incomplete || `Hãy ghim đủ ${need} tài liệu.` };
  }
  if (sameList(chosen, uniqSorted(q.answer))) return { status: 'correct', message: q.solved || 'Chính xác.' };
  for (const rule of Array.isArray(q.nudges) ? q.nudges : []) {
    const hit = Array.isArray(rule.picks)
      ? sameList(chosen, uniqSorted(rule.picks))
      : Array.isArray(rule.any) && chosen.some((p) => rule.any.includes(p));
    if (hit) return { status: rule.near ? 'near' : 'wrong', message: rule.message };
  }
  return { status: 'wrong', message: q.wrong || 'Chưa đúng. Đối chiếu lại các tài liệu.' };
}

// line: a numbered line of a testimony, written "docId:NNN" (e.g. "d04:007").
export function normalizeLine(value) {
  const m = /^([a-z0-9-]+):(\d{1,3})$/.exec(String(value ?? '').trim());
  return m ? `${m[1]}:${m[2].padStart(3, '0')}` : '';
}

export function checkLine(value, q) {
  const line = normalizeLine(value);
  if (!line) return { status: 'incomplete', message: q.incomplete || 'Hãy chạm vào một dòng có đánh số trong lời khai rồi chọn "Chọn dòng này".' };
  if ((q.answer || []).map(normalizeLine).includes(line)) return { status: 'correct', message: q.solved || 'Chính xác.' };
  const nudges = {};
  if (q.nudges && !Array.isArray(q.nudges)) {
    Object.entries(q.nudges).forEach(([k, v]) => { nudges[normalizeLine(k)] = v; });
  }
  const nudge = nudges[line];
  if (nudge) return { status: nudge.near ? 'near' : 'wrong', message: nudge.message };
  return { status: 'wrong', message: q.wrong || 'Chưa đúng. Dòng này không mâu thuẫn với bằng chứng.' };
}

// choice: exact set of option indexes (any order). No options = a "reveal" step.
export function checkChoice(picks, q) {
  const count = (q.options || []).length;
  if (!count) return { status: 'correct', message: q.solved || '' };
  const norm = (list) => [...new Set((Array.isArray(list) ? list : []).map(Number))]
    .filter((n) => Number.isInteger(n) && n >= 0 && n < count).sort((a, b) => a - b);
  const chosen = norm(picks);
  if (!chosen.length) return { status: 'incomplete', message: q.incomplete || 'Hãy chọn đáp án.' };
  if (sameList(chosen.map(String), norm(q.answer).map(String))) return { status: 'correct', message: q.solved || 'Chính xác.' };
  const nudge = q.nudges && !Array.isArray(q.nudges) ? q.nudges[String(chosen[0])] : null;
  if (chosen.length === 1 && nudge) return { status: nudge.near ? 'near' : 'wrong', message: nudge.message };
  return { status: 'wrong', message: q.wrong || 'Chưa đúng. Đối chiếu lại các tài liệu rồi thử lại.' };
}

export function check(q, input) {
  if (q.type === 'evidence') return checkEvidence(input, q);
  if (q.type === 'line') return checkLine(input, q);
  return checkChoice(input, q);
}
