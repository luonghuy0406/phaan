// Turns written Vietnamese case text into what a narrator would actually say, before it reaches the TTS model:
// numbers, dates, times, money, units, abbreviations, acronyms and ALL-CAPS headings.
// Then splits it into short, sentence-aligned segments with natural pauses.

const DIGITS = ['không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín'];

/** 0–999, `full` = inside a larger number (keeps "không trăm", "lẻ"). */
function readTriple(n: number, full: boolean): string {
  const h = Math.floor(n / 100), t = Math.floor((n % 100) / 10), u = n % 10;
  const out: string[] = [];
  if (h > 0 || full) out.push(DIGITS[h], 'trăm');
  if (t === 0) {
    if (u > 0 && (h > 0 || full)) out.push('lẻ');
    if (u > 0 || out.length === 0) out.push(DIGITS[u]);
  } else if (t === 1) {
    out.push('mười');
    if (u === 5) out.push('lăm');
    else if (u > 0) out.push(DIGITS[u]);
  } else {
    out.push(DIGITS[t], 'mươi');
    if (u === 1) out.push('mốt');
    else if (u === 4) out.push('tư');
    else if (u === 5) out.push('lăm');
    else if (u > 0) out.push(DIGITS[u]);
  }
  return out.join(' ');
}

const UNITS = ['', 'nghìn', 'triệu', 'tỷ', 'nghìn tỷ', 'triệu tỷ'];

/** Integer written with digits only (no separators) → words. */
export function readNumber(digits: string): string {
  const s = digits.replace(/^0+(?=\d)/, '');
  if (s.length > 18) return readDigits(s);
  const groups: number[] = [];
  for (let i = s.length; i > 0; i -= 3) groups.unshift(Number(s.slice(Math.max(0, i - 3), i)));
  if (groups.every((g) => g === 0)) return 'không';
  const out: string[] = [];
  groups.forEach((g, i) => {
    const unit = UNITS[groups.length - 1 - i];
    if (g === 0) return;
    out.push(readTriple(g, out.length > 0));
    if (unit) out.push(unit);
  });
  return out.join(' ');
}

export const readDigits = (s: string) => [...s].map((d) => DIGITS[Number(d)] ?? d).join(' ');

const MONTH = (m: number) => (m === 4 ? 'tư' : readNumber(String(m)));
const DAY = (d: number) => (d <= 10 ? `mùng ${readNumber(String(d))}` : readNumber(String(d)));

const ROMAN: Record<string, number> = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };
function roman(s: string): number | null {
  let total = 0;
  for (let i = 0; i < s.length; i++) {
    const v = ROMAN[s[i]], next = ROMAN[s[i + 1]] ?? 0;
    if (!v) return null;
    total += v < next ? -v : v;
  }
  return total > 0 && total < 4000 ? total : null;
}

// unit symbols after a number (longest first)
const UNIT_WORDS: [string, string][] = [
  ['km/h', 'ki-lô-mét một giờ'], ['m²', 'mét vuông'], ['m2', 'mét vuông'], ['m³', 'mét khối'], ['m3', 'mét khối'],
  ['kVA', 'ki-lô vôn ampe'], ['kW', 'ki-lô oát'], ['mcg', 'mi-crô-gam'], ['km', 'ki-lô-mét'], ['cm', 'xăng-ti-mét'], ['mm', 'mi-li-mét'], ['kg', 'ki-lô-gam'], ['mg', 'mi-li-gam'], ['ml', 'mi-li-lít'],
  ['ha', 'héc-ta'], ['m', 'mét'], ['g', 'gam'], ['l', 'lít'], ['%', 'phần trăm'], ['°C', 'độ C'], ['°', 'độ'], ['V', 'vôn'], ['A', 'ampe'], ['W', 'oát'], ['K', 'ca-ra'], ['G', 'gờ'],
  ['USD', 'đô la Mỹ'], ['VNĐ', 'đồng'], ['VND', 'đồng'], ['đ', 'đồng'], ['tr', 'triệu'],
];

const ABBREVIATIONS: [RegExp, string][] = [
  [/\bTP\.\s?HCM\b/g, 'Thành phố Hồ Chí Minh'], [/\bTP\.?(?=\s)/g, 'thành phố'], [/\bTp\.(?=\s)/g, 'thành phố'], [/\bTX\.(?=\s)/g, 'thị xã'],
  [/\bUBND\b/g, 'Ủy ban nhân dân'], [/\bHĐND\b/g, 'Hội đồng nhân dân'], [/\bCSGT\b/g, 'cảnh sát giao thông'],
  [/\bCSĐT\b/g, 'cảnh sát điều tra'], [/\bTHPT\b/g, 'trung học phổ thông'], [/\bTHCS\b/g, 'trung học cơ sở'],
  [/\bSĐT\b/g, 'số điện thoại'], [/\bĐT\b(?=\s*:)/g, 'điện thoại'], [/\bv\.v\.?/g, 'vân vân'], [/\bvv\./g, 'vân vân'],
  [/\bBS\.(?=\s)/g, 'bác sĩ'], [/\bThS\.(?=\s)/g, 'thạc sĩ'], [/\bTS\.(?=\s)/g, 'tiến sĩ'], [/\bPGS\.(?=\s)/g, 'phó giáo sư'], [/\bGS\.(?=\s)/g, 'giáo sư'],
  [/\bQ\.\s?(?=\d)/g, 'quận '], [/\bP\.\s?(?=\d)/g, 'phường '], [/\bNo\.\s?(?=\d)/g, 'số '], [/\bTr\.\s?(?=\d)/g, 'trang '],
  [/\bk\/g\b/g, 'kính gửi'], [/\bCty\b/gi, 'công ty'], [/\bTNHH\b/g, 'trách nhiệm hữu hạn'],
];

const LETTER: Record<string, string> = {
  A: 'a', B: 'bê', C: 'xê', D: 'dê', Đ: 'đê', E: 'e', F: 'ép', G: 'gờ', H: 'hát', I: 'i', J: 'gi', K: 'ca', L: 'lờ', M: 'mờ',
  N: 'nờ', O: 'o', P: 'pê', Q: 'quy', R: 'rờ', S: 'ét', T: 'tê', U: 'u', V: 'vê', W: 'vê kép', X: 'ích', Y: 'i', Z: 'dét',
};

const UPPER = 'A-ZĐÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ';
const LOWER = 'a-zđàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ';
const CAPS_WORD = new RegExp(`^[${UPPER}]{2,}$`);
const HAS_TONE_OR_HAT = /[ĐÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ]/;
const KNOWN_ACRONYMS: Record<string, string> = { USD: 'đô la Mỹ', VND: 'đồng', VNĐ: 'đồng', OK: 'ô kê', TV: 'ti vi', ID: 'ai đi', SOS: 'ét o ét' };

/** ALL-CAPS headings → normal case; short isolated acronyms (PVC, ADN) → spelled out. */
function fixCaps(line: string): string {
  const tokens = line.split(/(\s+)/);
  const isCaps = (t: string) => CAPS_WORD.test(t.replace(/[^\p{L}]/gu, ''));
  return tokens.map((tok, i) => {
    const word = tok.replace(/[^\p{L}]/gu, '');
    if (!word || !isCaps(tok)) return tok;
    if (KNOWN_ACRONYMS[word]) return tok.replace(word, KNOWN_ACRONYMS[word]);
    const neighbours = [tokens[i - 2], tokens[i + 2]].filter((t) => t && /\p{L}/u.test(t));
    const inHeading = neighbours.some((t) => isCaps(t!));
    if (!inHeading && word.length <= 4 && !HAS_TONE_OR_HAT.test(word)) {
      return tok.replace(word, [...word].map((c) => LETTER[c] ?? c).join(' '));
    }
    return tok.toLocaleLowerCase('vi');
  }).join('');
}

const NUM = String.raw`\d{1,3}(?:\.\d{3})+|\d+`; // 30.000 or 2005
const unitAlt = UNIT_WORDS.map(([u]) => u.replace(/[.*+?^${}()|[\]\\/]/g, '\\$&')).join('|');
const AFTER_UNIT = `(?![${LOWER}${UPPER}\\d])`;

/** Written text → spoken Vietnamese (still punctuated, one paragraph per line). */
export function normalizeVi(input: string): string {
  let t = input.replace(/\r\n/g, '\n');
  // markdown leftovers and typography
  t = t.replace(/\*\*|__|~~/g, '').replace(/[“”«»„]/g, '"').replace(/[‘’]/g, "'").replace(/…/g, '...');
  t = t.replace(/["']/g, '');
  for (const [re, rep] of ABBREVIATIONS) t = t.replace(re, rep);

  // dates: 19/08/2005, 19-08-2005, 19/08, 08/2005
  t = t.replace(/(ngày\s+)?\b(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})\b/gi, (_, _pre, d, m, y) =>
    `ngày ${DAY(Number(d))} tháng ${MONTH(Number(m))} năm ${readNumber(y)}`);
  t = t.replace(/(ngày\s+)?\b(\d{1,2})\/(\d{1,2})\b/gi, (all, _pre, d, m) =>
    Number(m) >= 1 && Number(m) <= 12 && Number(d) >= 1 && Number(d) <= 31 ? `ngày ${DAY(Number(d))} tháng ${MONTH(Number(m))}` : all);
  t = t.replace(/(tháng\s+)?\b(\d{1,2})\/(\d{4})\b/gi, (_, _pre, m, y) => `tháng ${MONTH(Number(m))} năm ${readNumber(y)}`);
  // ranges between numbers/times: 1990-1995, 11h45 - 13h00 (dates above already consumed their dashes)
  t = t.replace(/(\d[hg]?\d*)\s*[–—-]\s*(?=\d)/g, '$1 đến ');
  // times: 14h00, 11h45, 8g30, 20:00, 9h
  t = t.replace(/\b(\d{1,2})\s?[hg:](\d{2})\b(?!\s*\/)/g, (_, h, m) => `${readNumber(h)} giờ${Number(m) ? ` ${readNumber(m)} phút` : ''}`);
  t = t.replace(/\b(\d{1,2})\s?h\b/g, (_, h) => `${readNumber(h)} giờ`);
  // "ngày 5" / "tháng 4" spoken forms
  t = t.replace(/\bngày\s+(\d{1,2})\b/gi, (_, d) => `ngày ${DAY(Number(d))}`);
  t = t.replace(/\btháng\s+(\d{1,2})\b/gi, (_, m) => `tháng ${MONTH(Number(m))}`);
  // references to other papers: d07 → "tài liệu số bảy"
  t = t.replace(/\b[dD](\d{2,3})\b/g, (_, n) => `tài liệu số ${readNumber(n)}`);
  // codes mixing capitals and digits: SE3, K54, A6, QN-9288-TS, PUR-82, CO2 → spelled letters, short numbers read
  t = t.replace(/\b[A-ZĐ][A-ZĐ0-9]*(?:-[A-ZĐ0-9]+)*\b/g, (code) => {
    if (!/\d/.test(code) || !/[A-ZĐ]/.test(code) || roman(code)) return code;
    return code.split('-').flatMap((part) => part.match(/[A-ZĐ]+|\d+/g) || []).map((run) => (
      /\d/.test(run) ? (run.length <= 2 ? readNumber(run) : readDigits(run)) : [...run].map((c) => LETTER[c] ?? c).join(' ')
    )).join(' ');
  });
  // heights 1m75 → một mét bảy mươi lăm
  t = t.replace(/\b(\d)m(\d{2})\b/g, (_, a, b) => `${readNumber(a)} mét ${readNumber(b)}`);
  // decimals written with a dot (+0.45m, 1.10 m): a dot followed by 1–2 digits, or 4+ digits, is not a thousands separator
  t = t.replace(/(\d+)\.(\d{1,2}|\d{4,})(?!\d)/g, (_, a, b) => `${a},${b}`);
  t = t.replace(/(^|\s)\+(?=\d)/g, '$1cộng ').replace(/(^|\s)-(?=\d)/g, '$1âm ');
  // Roman numerals after the words that use them
  t = t.replace(/\b(thế kỷ|thế kỉ|chương|phần|khoản|khóa|khoá|đợt)\s+([IVXLCDM]+)\b/g, (all, w, r) => {
    const n = roman(r);
    return n ? `${w} ${readNumber(String(n))}` : all;
  });
  // ranges and dimensions between numbers: 1990-1995, 40 x 120
  t = t.replace(/(\d)\s*(?:[a-zA-Z²³%]*)\s*[x×]\s*(?=\d)/g, (all) => all.replace(/\s*[x×]\s*$/, ' nhân '));
  // phone numbers / codes with a leading zero, long digit strings: digit by digit
  t = t.replace(/\b0\d{6,}\b|\b\d{10,}\b/g, (s) => readDigits(s));
  t = t.replace(/\b(\d{2,4})[ .](\d{3})[ .](\d{3,4})\b(?=\D|$)/g, (all, a, b, c) => (a.startsWith('0') ? readDigits(a + b + c) : all));
  // money / units directly after a number: 30.000 USD, 40cm, 80m, 15%
  t = t.replace(new RegExp(`(${NUM})(?:,(\\d+))?\\s?(${unitAlt})${AFTER_UNIT}`, 'g'), (_, n, dec, u) => {
    const words = UNIT_WORDS.find(([k]) => k === u)![1];
    return `${readNumber(n.replace(/\./g, ''))}${dec ? ` phẩy ${readDecimal(dec)}` : ''} ${words}`;
  });
  t = t.replace(/\$\s?(\d[\d.,]*)/g, (_, n) => `${n} đô la`);
  // decimals 3,5 and plain numbers (with thousand dots)
  t = t.replace(new RegExp(`\\b(${NUM}),(\\d+)\\b`, 'g'), (_, a, b) => `${readNumber(a.replace(/\./g, ''))} phẩy ${readDecimal(b)}`);
  t = t.replace(new RegExp(`\\b(${NUM})\\b`, 'g'), (n) => readNumber(n.replace(/\./g, '')));
  // symbols
  t = t.replace(/&/g, ' và ').replace(/\s\+\s/g, ' cộng ').replace(/\s=\s/g, ' bằng ').replace(/№/g, 'số ');
  t = t.replace(/\s*[(]\s*/g, ', ').replace(/\s*[)]\s*/g, ', ').replace(/\s*[[\]{}]\s*/g, ' ');
  t = t.replace(/\s[–—-]\s/g, ', ').replace(/(\p{L})\s*\/\s*(?=\p{L})/gu, '$1 hoặc ').replace(/\//g, ' trên ').replace(/[#*_|~^<>]/g, ' ');

  return t.split('\n').map((line) => {
    let l = fixCaps(line).replace(/\s+/g, ' ').replace(/\s+([,.;:!?])/g, '$1').replace(/,(\s*[,.;:!?])+/g, '$1').replace(/^[,;:\s]+/, '').trim();
    l = l.replace(/,\s*$/, '');
    return l;
  }).join('\n');
}

function readDecimal(d: string): string {
  // 3,5 → "ba phẩy năm"; 3,25 → "ba phẩy hai lăm"; long tails digit by digit
  if (d.length <= 2 && !d.startsWith('0')) return readNumber(d).replace(/^hai mươi /, 'hai ').replace(/ mươi /, ' ');
  return readDigits(d);
}

export type SpeechSegment = { text: string; pause: number };

/**
 * Spoken text → short segments the model reads with natural prosody.
 * Sentences are grouped up to `max` characters, never cut mid-sentence unless one is longer than `max`
 * (then at a comma/semicolon). `pause` is the silence (s) after the segment: longer at paragraph ends and headings.
 */
export function splitSpeech(text: string, max = 180): SpeechSegment[] {
  const segs: SpeechSegment[] = [];
  const paras = text.split(/\n+/).map((p) => p.trim()).filter(Boolean);
  for (const para of paras) {
    const isHeading = !/[.!?…:;]$/.test(para) && para.length < 90;
    const sentence = /[^.!?…]+(?:[.!?…]+|$)/g;
    const sentences = (para.match(sentence) || [para]).map((s) => s.trim()).filter(Boolean);
    const pieces: string[] = [];
    for (const s of sentences) {
      if (s.length <= max) { pieces.push(s); continue; }
      // long sentence: cut at clause boundaries
      let cur = '';
      for (const clause of s.split(/(?<=[,;:])\s+/)) {
        if (cur && cur.length + clause.length + 1 > max) { pieces.push(cur); cur = clause; }
        else cur = cur ? `${cur} ${clause}` : clause;
        while (cur.length > max) {
          const cut = cur.lastIndexOf(' ', max);
          pieces.push(cur.slice(0, cut > max * 0.4 ? cut : max));
          cur = cur.slice(cut > max * 0.4 ? cut + 1 : max);
        }
      }
      if (cur) pieces.push(cur);
    }
    // group short sentences so the model keeps the flow across them
    let group = '';
    const flush = (pause: number) => { if (group) segs.push({ text: group, pause }); group = ''; };
    for (const p of pieces) {
      if (group && group.length + p.length + 1 > max) flush(/[,;:]$/.test(group) ? 0.12 : 0.22);
      group = group ? `${group} ${p}` : p;
    }
    flush(isHeading ? 0.55 : 0.45);
  }
  return segs.map((s) => ({ ...s, text: /[.!?…,;:]$/.test(s.text) ? s.text : `${s.text}.` }));
}
