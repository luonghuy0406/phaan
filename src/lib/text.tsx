import { Fragment, type ReactNode } from 'react';

// Inline markup allowed in case text: **đậm**, __gạch chân__, ~~gạch xoá~~.
// Parsed into React nodes, so case files can never inject HTML.
const TOKEN = /(\*\*(.+?)\*\*|__(.+?)__|~~(.+?)~~)/g;

// Authors sometimes cite documents by id, e.g. "(d12)"; players see document numbers instead.
const DOC_REF = /\b(d\d{2,3})\b/g;
let docNumbers = new Map<string, number>();
export function setDocNumbers(map: Map<string, number>) { docNumbers = map; }

export function Txt({ children }: { children?: string | null }): ReactNode {
  const text = String(children ?? '').replace(DOC_REF, (id: string) => (docNumbers.has(id) ? `Tài liệu ${String(docNumbers.get(id)).padStart(2, '0')}` : id));
  const out: ReactNode[] = [];
  let last = 0;
  let i = 0;
  for (const m of text.matchAll(TOKEN)) {
    const at = m.index ?? 0;
    if (at > last) out.push(text.slice(last, at));
    if (m[2] != null) out.push(<strong key={i++}>{m[2]}</strong>);
    else if (m[3] != null) out.push(<u key={i++}>{m[3]}</u>);
    else out.push(<s key={i++}>{m[4]}</s>);
    last = at + m[0].length;
  }
  if (last < text.length) out.push(text.slice(last));
  return <Fragment>{out}</Fragment>;
}

export const plain = (text?: string | null) => String(text ?? '').replace(/\*\*|__|~~/g, '');

export function Paras({ list }: { list?: string[] | string }) {
  const items = Array.isArray(list) ? list : list ? [list] : [];
  return <>{items.map((p, i) => <p key={i}><Txt>{p}</Txt></p>)}</>;
}
