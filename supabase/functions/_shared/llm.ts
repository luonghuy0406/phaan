// Free-tier language models behind OpenAI-compatible chat endpoints, tried in order.
// On a rate limit, overload, timeout or empty reply the next model is tried, and the failing one rests for a while.
// No runtime-specific APIs: works in Deno (Edge Function) and Node (tests).

export type Provider = 'gemini' | 'groq' | 'openrouter';
export interface ModelRef { provider: Provider; model: string }
export interface ChatMessage { role: string; content: string }

const ENDPOINTS: Record<Provider, string> = {
  gemini: 'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions',
  groq: 'https://api.groq.com/openai/v1/chat/completions',
  openrouter: 'https://openrouter.ai/api/v1/chat/completions',
};

/** Role-play order, measured on 2026-11-27: quality first, then speed. */
export const ROLEPLAY_MODELS: ModelRef[] = [
  { provider: 'gemini', model: 'gemini-3.5-flash-lite' },
  { provider: 'groq', model: 'qwen/qwen3.8-27b' },
  { provider: 'groq', model: 'openai/gpt-oss-120b' },
  { provider: 'openrouter', model: 'baidu/ernie-5.5-flash-preview:free' },
  { provider: 'groq', model: 'openai/gpt-oss-20b' },
];

const restingUntil = new Map<string, number>();
const keyOf = (m: ModelRef) => `${m.provider}/${m.model}`;

export class AllModelsFailed extends Error {
  attempts: string[];
  constructor(attempts: string[]) { super(`AI_UNAVAILABLE: ${attempts.join('; ')}`); this.attempts = attempts; }
}

export async function chat(
  messages: ChatMessage[],
  keys: Partial<Record<Provider, string>>,
  opts: { models?: ModelRef[]; maxTokens?: number; temperature?: number; timeoutMs?: number; fetchFn?: typeof fetch; now?: () => number } = {},
): Promise<{ text: string; model: string }> {
  const models = opts.models ?? ROLEPLAY_MODELS;
  const doFetch = opts.fetchFn ?? fetch;
  const now = opts.now ?? Date.now;
  const attempts: string[] = [];
  // models that are resting go last rather than being skipped, so a burst never leaves the player with nothing
  const order = [...models].sort((a, b) => Number((restingUntil.get(keyOf(a)) ?? 0) > now()) - Number((restingUntil.get(keyOf(b)) ?? 0) > now()));
  for (const m of order) {
    const key = keys[m.provider];
    if (!key) { attempts.push(`${keyOf(m)}: no key`); continue; }
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), opts.timeoutMs ?? 20000);
    try {
      const res = await doFetch(ENDPOINTS[m.provider], {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${key}` },
        body: JSON.stringify({ model: m.model, messages, max_tokens: opts.maxTokens ?? 400, temperature: opts.temperature ?? 0.7 }),
        signal: ctrl.signal,
      });
      if (!res.ok) {
        attempts.push(`${keyOf(m)}: HTTP ${res.status}`);
        // rate limited / overloaded / gone: rest it (longer when the quota is spent)
        if ([408, 409, 425, 429, 500, 502, 503, 504, 404].includes(res.status)) restingUntil.set(keyOf(m), now() + (res.status === 429 ? 60_000 : res.status === 404 ? 3_600_000 : 30_000));
        continue;
      }
      const j = await res.json();
      const text = String(j?.choices?.[0]?.message?.content ?? '').trim();
      if (!text) { attempts.push(`${keyOf(m)}: empty`); continue; }
      return { text, model: keyOf(m) };
    } catch (e) {
      attempts.push(`${keyOf(m)}: ${(e as Error).name === 'AbortError' ? 'timeout' : (e as Error).message}`);
      restingUntil.set(keyOf(m), now() + 30_000);
    } finally {
      clearTimeout(timer);
    }
  }
  throw new AllModelsFailed(attempts);
}

/** test helper */
export function _resetRests() { restingUntil.clear(); }
