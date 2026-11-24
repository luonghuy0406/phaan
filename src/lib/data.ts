import { useEffect, useState } from 'react';
import type { CaseData, CaseSummary, CaseKind } from './types';

const BASE = import.meta.env.BASE_URL;
const ID_RE = /^[a-z0-9-]{1,60}$/;

export const caseBase = (id: string) => `${BASE}cases/${id}/`;
export const caseNo = (c: { no?: number }) => `Hồ sơ ${String(c.no ?? '').padStart(2, '0')}`;
export const pad2 = (n: number | string) => String(n).padStart(2, '0');
export const pad3 = (n: number | string) => String(n).padStart(3, '0');

const cache = new Map<string, Promise<unknown>>();
function getJson<T>(url: string): Promise<T> {
  if (!cache.has(url)) {
    cache.set(url, fetch(url, { cache: 'no-cache' }).then((r) => {
      if (!r.ok) throw new Error(`${r.status} ${url}`);
      return r.json();
    }).catch((e) => { cache.delete(url); throw e; }));
  }
  return cache.get(url) as Promise<T>;
}

export async function loadCatalog(): Promise<CaseSummary[]> {
  const json = await getJson<{ cases?: CaseSummary[] }>(`${BASE}cases/index.json`);
  return (json.cases || []).slice().sort((a, b) => (a.no ?? 0) - (b.no ?? 0));
}

export async function loadCase(id: string): Promise<CaseData> {
  if (!ID_RE.test(id)) throw new Error('bad-id');
  const data = await getJson<CaseData>(`${caseBase(id)}case.json`);
  return {
    ...data,
    documents: (data.documents || []).map((d, i) => ({ ...d, stage: Math.max(1, Math.floor(Number(d.stage) || 1)), no: d.no ?? i + 1 })),
    questions: (data.questions || []).map((q) => ({ ...q, stage: Math.max(1, Math.floor(Number(q.stage) || 1)) })),
  };
}

type Async<T> = { data?: T; error?: unknown; loading: boolean };
export function useAsync<T>(fn: () => Promise<T>, deps: unknown[]): Async<T> {
  const [state, setState] = useState<Async<T>>({ loading: true });
  useEffect(() => {
    let live = true;
    setState({ loading: true });
    fn().then((data) => live && setState({ data, loading: false }), (error) => live && setState({ error, loading: false }));
    return () => { live = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return state;
}

/** Fiction or reconstructed from a real case. Older catalogs only mark real cases with the tag "Vụ án có thật". */
export const caseKind = (c: { kind?: CaseKind; tags?: string[] }): CaseKind =>
  c.kind ?? (c.tags?.some((t) => /vụ án có thật/i.test(t)) ? 'true-crime' : 'fiction');
export const KIND_LABEL: Record<CaseKind, string> = { fiction: 'Hư cấu', 'true-crime': 'Vụ án có thật' };
