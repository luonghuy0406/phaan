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

export const PaperCtx = createContext<{ hl: Set<string>; picked: string }>({ hl: new Set(), picked: '' });

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

function Header({ lines }: { lines?: string[] }) {
  if (!lines?.length) return null;
  return <div className="doc-head">{lines.map((l, i) => <span key={i}>{l}</span>)}</div>;
}

const ParaBlocks = ({ list, prefix = 'p' }: { list?: string[]; prefix?: string }) => (
  <>{(list || []).map((p, i) => <B key={i} k={`${prefix}${i}`}><Txt>{p}</Txt></B>)}</>
);

const Sign = ({ text, className = 'sign' }: { text?: string; className?: string }) => (text ? <B k="sig" className={className}><Txt>{text}</Txt></B> : null);

type R = (d: CaseDoc, base: string) => ReactNode;

const RENDER: Record<DocType, R> = {
  newspaper: (d, base) => (
    <div className="np">
      <div className="np__mast">{d.masthead || 'Báo Thành Phố'}</div>
      <div className="np__meta"><span>{d.issue}</span><span>{d.date}</span></div>
      <B k="hd" as="h2" className="np__head"><Txt>{d.headline || d.title}</Txt></B>
      {d.deck && <B k="dk" className="np__deck"><Txt>{d.deck}</Txt></B>}
      {d.image !== undefined && <Figure src={d.image} hi={d.imageHi} caption={d.imageCaption} base={base} className="np__fig" />}
      <div className="np__cols"><ParaBlocks list={d.paragraphs} /></div>
    </div>
  ),
  report: (d) => (
    <div className="rp">
      <Header lines={d.header} />
      <h2 className="rp__title"><Txt>{d.heading || d.title}</Txt></h2>
      {(d.code || d.date) && <p className="rp__code">{[d.code && `Số: ${d.code}`, d.date].filter(Boolean).join(' · ')}</p>}
      <Fields list={d.fields} />
      {(d.sections || []).map((s, i) => (
        <section key={i}>
          <B k={`s${i}`} as="h3"><Txt>{s.heading}</Txt></B>
          <ParaBlocks list={s.paragraphs} prefix={`s${i}p`} />
        </section>
      ))}
      <Sign text={d.signature} />
    </div>
  ),
  testimony: (d) => (
    <div className="ts">
      <Header lines={d.header} />
      <h2 className="rp__title"><Txt>{d.heading || 'Biên bản ghi lời khai'}</Txt></h2>
      {d.date && <p className="rp__code">{d.date}</p>}
      <Fields list={d.fields} />
      <ol className="ts__lines">
        {(d.lines || []).map((l) => (
          <B key={l.n} k={`l${l.n}`} as="li" className="tl" line={`${d.id}:${pad3(l.n)}`}>
            <span className="tl__n">{pad3(l.n)}</span>
            <span className="tl__t">{l.speaker && <b>{l.speaker}: </b>}<Txt>{l.text}</Txt></span>
          </B>
        ))}
      </ol>
      <Sign text={d.signature} />
    </div>
  ),
  photo: (d, base) => (
    <div className="ph">
      <Figure src={d.image} hi={d.imageHi} base={base} />
      {d.caption && <B k="cap" className="ph__cap"><Txt>{d.caption}</Txt></B>}
      {d.label && <p className="ph__label">{d.label}</p>}
    </div>
  ),
  letter: (d) => (
    <div className="lt">
      {d.date && <B k="date" className="lt__date">{d.date}</B>}
      {d.greeting && <B k="gr"><Txt>{d.greeting}</Txt></B>}
      <ParaBlocks list={d.paragraphs} />
      <Sign text={d.signature} className="lt__sign" />
    </div>
  ),
  receipt: (d) => (
    <div className="rc">
      <p className="rc__shop">{d.shop}</p>
      {d.address && <p className="rc__addr">{d.address}</p>}
      <Fields list={d.fields} className="rc__fields" />
      <table>
        <thead><tr><th>Món</th><th>SL</th><th>Tiền</th></tr></thead>
        <tbody>
          {(d.items || []).map((it, i) => (
            <B key={i} k={`it${i}`} as="tr"><td><Txt>{it.name}</Txt></td><td>{it.qty}</td><td>{it.price}</td></B>
          ))}
        </tbody>
      </table>
      {d.total && <B k="tot" className="rc__total"><span>Tổng</span><span>{d.total}</span></B>}
      <ParaBlocks list={d.footer} prefix="ft" />
    </div>
  ),
  evidence: (d, base) => (
    <div className="ev">
      <div className="ev__tag"><span>Tang vật</span><strong>{d.code}</strong></div>
      {d.image !== undefined && <Figure src={d.image} hi={d.imageHi} caption={d.imageCaption} base={base} />}
      <Fields list={d.fields} />
      <ParaBlocks list={d.paragraphs} />
    </div>
  ),
  scan: (d, base) => (
    <div className="scan">
      <Figure src={d.image} hi={d.imageHi} base={base} caption={d.caption} />
    </div>
  ),
  note: (d) => (
    <div className="nt">
      <ParaBlocks list={d.paragraphs} />
      <Sign text={d.signature} className="lt__sign" />
    </div>
  ),
};

export function Paper({ doc, base }: { doc: CaseDoc; base: string }) {
  return <>{(RENDER[doc.type] || RENDER.note)(doc, base)}</>;
}
