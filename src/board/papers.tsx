// One renderer per document type. Every readable block is a <B> with a stable key (used by highlights,
// red strings and notebook quotes), so keys survive content edits elsewhere in the paper.
import { createContext, useContext, useState, useSyncExternalStore, type ElementType, type ReactNode } from 'react';
import { Ctx } from './context';
import type { CaseDoc, DocType, Field } from '../lib/types';
import { Txt, plain } from '../lib/text';
import { pad3 } from '../lib/data';

export const TYPE_LABEL: Record<DocType, string> = {
  newspaper: 'Bài báo', report: 'Biên bản', testimony: 'Lời khai', photo: 'Ảnh',
  letter: 'Thư tay', receipt: 'Hoá đơn', evidence: 'Tang vật', note: 'Ghi chép', scan: 'Bản chụp',
};
export const typeLabel = (t: string) => TYPE_LABEL[t as DocType] || 'Tài liệu';

export const DEFAULT_WIDTH: Record<DocType, number> = {
  newspaper: 640, report: 600, testimony: 580, photo: 420, letter: 500, receipt: 330, evidence: 470, note: 420, scan: 620,
};

export const PaperCtx = createContext<{ hl: Set<string>; picked: string; nation: boolean }>({ hl: new Set(), picked: '', nation: true });

function B({ k, as: As = 'p', line, className = '', children }: { k: string; as?: ElementType; line?: string; className?: string; children: ReactNode }) {
  const { hl, picked } = useContext(PaperCtx);
  const cls = ['blk', className, hl.has(k) && 'is-hl', line && line === picked && 'is-picked'].filter(Boolean).join(' ');
  return <As className={cls} data-key={k} data-line={line}>{children}</As>;
}

const noop = () => () => {};
// true once the desk is zoomed in enough to need the sharp file
function useZoomedIn(threshold = 0.85) {
  const ctx = useContext(Ctx);
  return useSyncExternalStore(ctx ? (cb) => ctx.cam.subscribe(cb) : noop, () => (ctx ? ctx.cam.z >= threshold : false));
}

function Figure({ src, hi, caption, base, className = '', capKey = 'cap' }: { src?: string | null; hi?: string; caption?: string; base: string; className?: string; capKey?: string }) {
  const [broken, setBroken] = useState(false);
  const zoomed = useZoomedIn();
  const [sharp, setSharp] = useState(false);
  if (hi && zoomed && !sharp) setSharp(true); // once loaded, keep the sharp file
  const missing = !src || broken;
  return (
    <figure className={`pf ${className}`}>
      <div className={`pf__img${missing ? ' is-missing' : ''}`}>
        {!missing && (
          <img src={base + (sharp && hi ? hi : src)} alt={plain(caption) || 'Ảnh tư liệu'} draggable={false} decoding="async" onError={() => setBroken(true)} />
        )}
      </div>
      {caption && <B k={capKey} as="figcaption"><Txt>{caption}</Txt></B>}
    </figure>
  );
}

function Fields({ list, className = 'fields' }: { list?: Field[]; className?: string }) {
  if (!list?.length) return null;
  return (
    <dl className={className}>
      {list.map((f, i) => (
        <B key={i} k={`f${i}`} as="div" className="fld"><dt>{f.label}</dt><dd><Txt>{f.value}</Txt></dd></B>
      ))}
    </dl>
  );
}

const ParaBlocks = ({ list, prefix = 'p' }: { list?: string[]; prefix?: string }) => (
  <>{(list || []).map((p, i) => <B key={i} k={`${prefix}${i}`}><Txt>{p}</Txt></B>)}</>
);

const Sign = ({ text, className = 'sign' }: { text?: string; className?: string }) => (text ? <B k="sig" className={className}><Txt>{text}</Txt></B> : null);

type Opts = { nation: boolean };
type R = (d: CaseDoc, base: string, extra: ReactNode, o: Opts) => ReactNode;

/* ── Vietnamese official paperwork: agency block + national motto, dotted fill-in lines, signature blocks ── */

function NationalMotto() {
  return (
    <div className="qh">
      <b>Cộng hòa xã hội chủ nghĩa Việt Nam</b>
      <span>Độc lập - Tự do - Hạnh phúc</span>
    </div>
  );
}

function OfficialHead({ d, nation }: { d: CaseDoc; nation: boolean }) {
  const agency = d.header?.length ? d.header : null;
  if (!agency && !nation && !d.form) return null;
  return (
    <div className="oh">
      {d.form && <p className="oh__form">{d.form}</p>}
      <div className={`oh__row${agency && nation ? '' : ' oh__row--one'}`}>
        {agency && (
          <div className="oh__agency">
            {agency.map((l, i) => <span key={i}>{l}</span>)}
            {d.code && <em className="oh__code">Số: {d.code}</em>}
          </div>
        )}
        {nation && <NationalMotto />}
      </div>
    </div>
  );
}

/** "Label: ……value……" with the value filled in by hand, like a printed form. */
function FillLines({ list }: { list?: Field[] }) {
  if (!list?.length) return null;
  return (
    <div className="fl-list">
      {list.map((f, i) => (
        <B key={i} k={`f${i}`} as="div" className="fl">
          <span className="fl__label">{f.label}:</span>
          <span className="fl__val"><Txt>{f.value}</Txt></span>
        </B>
      ))}
    </div>
  );
}

// "08 giờ 30, ngày 15/3/2024" → "Vào hồi 08 giờ 30, ngày 15/3/2024"; anything else is shown as is
function When({ date }: { date?: string }) {
  if (!date) return null;
  const isTime = /^\s*\d/.test(date);
  return <p className="off__when">{isTime && 'Vào hồi '}<span className="hand">{date}</span></p>;
}

type Signer = { role: string; name: string };

// "Người khai ký tên: Hoà" → { role: "Người khai", name: "Hoà" }
function parseSignature(text?: string): Signer | null {
  if (!text) return null;
  const t = plain(text).trim();
  const m = /^(.+?)\s*(?:\(?ký(?: tên)?(?:, ghi rõ họ tên)?\)?)?\s*[:：]\s*(.+)$/i.exec(t);
  return m ? { role: m[1].trim(), name: m[2].trim() } : { role: '', name: t };
}

function Seal({ text }: { text: string }) {
  const id = `seal-${text.length}-${text.charCodeAt(0)}`;
  return (
    <svg className="doc-seal" viewBox="0 0 120 120" aria-hidden="true">
      <defs><path id={id} d="M60 60 m-44 0 a44 44 0 1 1 88 0 a44 44 0 1 1 -88 0" /></defs>
      <circle cx="60" cy="60" r="56" /><circle cx="60" cy="60" r="34" />
      <text><textPath href={`#${id}`} startOffset="2%">{`★ ${text.toUpperCase()} ★ `}</textPath></text>
      <path className="doc-seal__star" d="M60 42l5.3 11 12 1.6-8.8 8.3 2.2 11.9L60 69l-10.7 5.8 2.2-11.9-8.8-8.3 12-1.6z" />
    </svg>
  );
}

function Signatures({ signers, seal }: { signers: Signer[]; seal?: string }) {
  if (!signers.length) return null;
  return (
    <B k="sig" as="div" className={`sg sg--${signers.length > 1 ? 'two' : 'one'}`}>
      {signers.map((s, i) => {
        const given = s.name.replace(/\(.*?\)/g, '').trim().split(/\s+/).pop() || s.name;
        return (
          <div key={i} className="sg__col">
            {s.role && <b className="sg__role">{s.role}</b>}
            <i className="sg__hint">(ký, ghi rõ họ tên)</i>
            <span className="sg__mark">
              {seal && i === signers.length - 1 && <Seal text={seal} />}
              {given}
            </span>
            <b className="sg__name">{s.name}</b>
          </div>
        );
      })}
    </B>
  );
}

function signersOf(d: CaseDoc, fallbackRole?: string): Signer[] {
  if (d.signers?.length) return d.signers;
  const one = parseSignature(d.signature);
  if (one) return [{ role: one.role || fallbackRole || '', name: one.name }];
  return [];
}

// who asks the questions in a testimony
const ASKER = /^(hỏi|câu hỏi|đtv|điều tra viên|cán bộ|thanh tra|kiểm sát viên|công an|trinh sát|cảnh sát|thẩm phán)/i;
const ANSWER = /^(đáp|trả lời)/i;

const RENDER: Record<DocType, R> = {
  newspaper: (d, base, extra) => (
    <div className="np">
      {(() => {
        const name = d.masthead || 'Báo Thành Phố';
        // long names shrink so the masthead stays on one or two tidy lines
        const size = name.length <= 12 ? 46 : name.length <= 18 ? 38 : name.length <= 26 ? 30 : 24;
        return <div className="np__mast" style={{ fontSize: size }}>{name}</div>;
      })()}
      {(d.issue || d.date) && <div className="np__bar"><span className="np__issue">{d.issue}</span><span>{d.date}</span></div>}
      <B k="hd" as="h2" className="np__head"><Txt>{d.headline || d.title}</Txt></B>
      {d.deck && <B k="dk" className="np__deck"><Txt>{d.deck}</Txt></B>}
      {d.image !== undefined && <Figure src={d.image} hi={d.imageHi} caption={d.imageCaption} base={base} className="np__fig" />}
      {d.paragraphs?.length ? <div className="np__cols"><ParaBlocks list={d.paragraphs} /></div> : null}
      {extra}
      <div className="np__foot" />
    </div>
  ),
  report: (d, base, extra, o) => (
    <div className="rp off">
      <OfficialHead d={d} nation={o.nation} />
      <h2 className="off__title"><Txt>{d.heading || d.title}</Txt></h2>
      {d.code && !d.header?.length && <p className="off__code">Số: {d.code}</p>}
      <When date={d.date} />
      <FillLines list={d.fields} />
      {d.image !== undefined && <Figure src={d.image} hi={d.imageHi} caption={d.imageCaption} base={base} />}
      {(d.sections || []).map((sec, i) => (
        <section key={i}>
          <B k={`s${i}`} as="h3"><Txt>{sec.heading}</Txt></B>
          <ParaBlocks list={sec.paragraphs} prefix={`s${i}p`} />
        </section>
      ))}
      {extra}
      <Signatures signers={signersOf(d, 'Người lập biên bản')} seal={d.header?.[0]} />
    </div>
  ),
  testimony: (d, base, extra, o) => {
    const lines = d.lines || [];
    const qa = lines.some((l) => l.speaker && ASKER.test(l.speaker));
    const others = new Set(lines.filter((l) => l.speaker && !ASKER.test(l.speaker)).map((l) => l.speaker));
    const label = (sp?: string) => {
      if (!sp) return null;
      if (ASKER.test(sp)) return 'Câu hỏi';
      if (ANSWER.test(sp) || (qa && others.size <= 1)) return 'Trả lời';
      return sp;
    };
    const deponent = d.fields?.find((f) => /người khai|họ (và )?tên|người làm chứng|nghi can/i.test(f.label))?.value.split(',')[0];
    const signers = d.signers?.length ? d.signers : (() => {
      const one = parseSignature(d.signature);
      let name = one && one.name && !/^(đã ký|ký)$/i.test(one.name) ? one.name : deponent;
      // "ký tên: Tư" + "Người khai: Phạm Thị Tư" → print the full name under the signature
      if (name && deponent && !/\s/.test(name.trim()) && deponent.trim().endsWith(name.trim())) name = deponent.trim();
      return name ? [{ role: one?.role && !/ký/i.test(one.role) ? one.role : 'Người khai', name }] : [];
    })();
    return (
      <div className="ts off">
        <OfficialHead d={d} nation={o.nation} />
        <h2 className="off__title"><Txt>{d.heading || 'Biên bản ghi lời khai'}</Txt></h2>
        <When date={d.date} />
        <FillLines list={d.fields} />
        {d.image !== undefined && <Figure src={d.image} hi={d.imageHi} caption={d.imageCaption} base={base} />}
        {lines.length > 0 && <p className="off__legal">Người khai đã được giải thích quyền và nghĩa vụ, cam đoan chịu trách nhiệm về lời khai của mình.</p>}
        {lines.length > 0 && <h3 className="off__sub">{qa ? 'Hỏi và trả lời' : 'Nội dung lời khai'}</h3>}
        <ol className="ts__lines">
          {lines.map((l) => {
            const lb = label(l.speaker);
            const aside = /^\(.*\)$/.test(l.text.trim());
            return (
              <B key={l.n} k={`l${l.n}`} as="li" className={`tl${lb === 'Câu hỏi' ? ' tl--q' : ''}${aside ? ' tl--aside' : ''}`} line={`${d.id}:${pad3(l.n)}`}>
                <span className="tl__n">{pad3(l.n)}</span>
                <span className="tl__t">{lb && <b>{lb}: </b>}<Txt>{l.text}</Txt></span>
              </B>
            );
          })}
        </ol>
        {extra}
        <Signatures signers={signers} />
      </div>
    );
  },
  photo: (d, base, extra) => (
    <div className="ph">
      <Figure src={d.image} hi={d.imageHi} base={base} />
      {d.caption && <B k="cap" className="ph__cap"><Txt>{d.caption}</Txt></B>}
      {d.label && <p className="ph__label">{d.label}</p>}
      {extra}
    </div>
  ),
  letter: (d, _base, extra) => (
    <div className="lt">
      {d.date && <B k="date" className="lt__date">{d.date}</B>}
      {d.greeting && <B k="gr"><Txt>{d.greeting}</Txt></B>}
      <ParaBlocks list={d.paragraphs} />
      {extra}
      <Sign text={d.signature} className="lt__sign" />
    </div>
  ),
  receipt: (d, base, extra) => (
    <div className="rc">
      <p className="rc__shop">{d.shop}</p>
      {d.address && <p className="rc__addr">{d.address}</p>}
      {d.image !== undefined && <Figure src={d.image} hi={d.imageHi} caption={d.imageCaption} base={base} />}
      <Fields list={d.fields} className="rc__fields" />
      {d.items?.length ? (
        <table>
          <thead><tr><th>Món</th><th>SL</th><th>Tiền</th></tr></thead>
          <tbody>
            {d.items.map((it, i) => (
              <B key={i} k={`it${i}`} as="tr"><td><Txt>{it.name}</Txt></td><td>{it.qty}</td><td>{it.price}</td></B>
            ))}
          </tbody>
        </table>
      ) : null}
      {d.total && <B k="tot" className="rc__total"><span>Tổng</span><span>{d.total}</span></B>}
      {extra}
      <ParaBlocks list={d.footer} prefix="ft" />
    </div>
  ),
  evidence: (d, base, extra) => (
    <div className="ev">
      <div className="ev__title">Tang vật vụ án</div>
      <div className="ev__frame">
        <div className="ev__inner">
          {d.image !== undefined && <Figure src={d.image} hi={d.imageHi} caption={d.imageCaption} base={base} />}
          <Fields list={d.fields} />
          <ParaBlocks list={d.paragraphs} />
          {extra}
        </div>
      </div>
      <div className="ev__foot">
        {d.code && <div className="ev__line"><span>Số thứ tự:</span><b className="ev__no">{d.code}</b></div>}
        <div className="ev__line"><span>Mô tả chung:</span><b className="ev__desc"><Txt>{d.title}</Txt></b></div>
      </div>
    </div>
  ),
  scan: (d, base) => (
    <div className="scan">
      <Figure src={d.image} hi={d.imageHi} base={base} caption={d.caption} />
    </div>
  ),
  note: (d, base, extra) => (
    <div className="nt">
      {d.image !== undefined && <Figure src={d.image} hi={d.imageHi} caption={d.imageCaption} base={base} />}
      <ParaBlocks list={d.paragraphs} />
      {extra}
      <Sign text={d.signature} className="lt__sign" />
    </div>
  ),
};

/* ── `content`: light Markdown body used by many cases ──
   blank line = new paragraph · "- " / "* " / "1. " lines = list items (indent ≥ 2 spaces = sub-item) · **bold** */
const LIST_ITEM = /^(\s*)([-*•]|\d+[.)])\s+(.*)$/;
const BOLD_ONLY = /^\*\*([^*]+)\*\*$/;

type ContentPart = { kind: 'p'; key: string; text: string } | { kind: 'ul'; key: string; items: { key: string; text: string; num: string | null; sub: boolean }[] };

export function parseContent(text: string): ContentPart[] {
  const parts: ContentPart[] = [];
  let n = 0;
  for (const block of text.replace(/\r\n/g, '\n').split(/\n\s*\n/)) {
    let list: Extract<ContentPart, { kind: 'ul' }> | null = null;
    for (const raw of block.split('\n')) {
      if (!raw.trim()) continue;
      const m = LIST_ITEM.exec(raw);
      if (m) {
        if (!list) { list = { kind: 'ul', key: `u${n}`, items: [] }; parts.push(list); }
        list.items.push({ key: `c${n++}`, text: m[3], num: /\d/.test(m[2]) ? m[2] : null, sub: m[1].length >= 2 });
      } else {
        list = null;
        parts.push({ kind: 'p', key: `c${n++}`, text: raw.trim() });
      }
    }
  }
  return parts;
}

// A leading line that is entirely bold ("**BIÊN BẢN KHÁM NGHIỆM**") is the paper's own heading.
function splitLead(text: string): { lead: string | null; body: string } {
  const t = text.trim();
  const firstBreak = t.search(/\n/);
  const first = (firstBreak < 0 ? t : t.slice(0, firstBreak)).trim();
  const m = BOLD_ONLY.exec(first);
  return m ? { lead: m[1].trim(), body: firstBreak < 0 ? '' : t.slice(firstBreak + 1) } : { lead: null, body: t };
}

function Content({ text }: { text: string }) {
  return (
    <>
      {parseContent(text).map((part) => (part.kind === 'p' ? (
        <B key={part.key} k={part.key} className={BOLD_ONLY.test(part.text) ? 'ct__head' : undefined}><Txt>{part.text}</Txt></B>
      ) : (
        <ul key={part.key} className="ct__list">
          {part.items.map((it) => (
            <B key={it.key} k={it.key} as="li" className={it.sub ? 'ct__sub' : undefined}>
              {it.num && <span className="ct__num">{it.num} </span>}<Txt>{it.text}</Txt>
            </B>
          ))}
        </ul>
      )))}
    </>
  );
}

const LEAD_FIELD: Partial<Record<DocType, 'headline' | 'heading' | 'shop'>> = { newspaper: 'headline', report: 'heading', testimony: 'heading', receipt: 'shop' };

export function Paper({ doc, base }: { doc: CaseDoc; base: string }) {
  const { nation } = useContext(PaperCtx);
  const o: Opts = { nation };
  const render = RENDER[doc.type] || RENDER.note;
  if (typeof doc.content !== 'string' || !doc.content.trim()) return <>{render(doc, base, null, o)}</>;
  // use the content's bold first line as heading (when the case gives none) and render the rest in the body
  let body = doc.content;
  let d: CaseDoc = doc;
  const field = LEAD_FIELD[doc.type];
  if (field && !doc[field]) {
    const { lead, body: rest } = splitLead(doc.content);
    if (lead) { d = { ...doc, [field]: lead }; body = rest; }
  }
  if (doc.type === 'newspaper' && !doc.masthead) {
    const name = doc.title.split(/\s[-–:]\s/)[0].trim();
    d = { ...d, masthead: name && name !== doc.title ? name : 'Tin Nhanh' };
  }
  return <>{render(d, base, <div className={`ct ct--${doc.type}`}><Content text={body} /></div>, o)}</>;
}
