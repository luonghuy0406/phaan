// Cloud save for signed-in players: the local IndexedDB copy stays the working copy (works offline, instant),
// and a copy is pushed to Supabase a few seconds after each change. Opening a case on another device pulls
// the newer of the two (last change wins).
import { useEffect, useState } from 'react';
import { create } from 'zustand';
import { supabase } from './supabase';
import { useAuth } from './auth';
import type { CaseData } from './types';
import { fingerprint, sanitize, snapshot, solvedCount, type BoardStore } from '../board/store';

export type CloudStatus = 'off' | 'saving' | 'saved' | 'error';
export const useCloud = create<{ status: CloudStatus; at: number }>(() => ({ status: 'off', at: 0 }));

const uid = () => useAuth.getState().session?.user.id;
const MAX_BYTES = 2_500_000;

async function pull(store: BoardStore, c: CaseData, scope: string): Promise<'remote' | 'local' | 'same' | 'none'> {
  const me = uid();
  if (!me) return 'none';
  const { data, error } = await supabase.from('user_progress')
    .select('fingerprint, data, saved_at').eq('user_id', me).eq('case_id', c.id).eq('scope', scope).maybeSingle();
  if (error || !data || data.fingerprint !== fingerprint(c)) return 'none';
  const remoteAt = new Date(data.saved_at as string).getTime();
  const localAt = store.getState().savedAt || 0;
  if (remoteAt > localAt) {
    store.setState({ ...sanitize(data.data, c), savedAt: remoteAt });
    return 'remote';
  }
  return remoteAt === localAt ? 'same' : 'local';
}

let warnedSize = false;
async function push(store: BoardStore, c: CaseData, scope: string) {
  const me = uid();
  if (!me) return;
  const s = store.getState();
  if (!s.savedAt) return;
  const data = snapshot(s);
  if (JSON.stringify(data).length > MAX_BYTES) {
    if (!warnedSize) { warnedSize = true; console.warn('Bản lưu quá lớn để đồng bộ (quá nhiều nét vẽ).'); }
    useCloud.setState({ status: 'error' });
    return;
  }
  useCloud.setState({ status: 'saving' });
  const { error } = await supabase.from('user_progress').upsert({
    user_id: me, case_id: c.id, scope, fingerprint: fingerprint(c), data,
    solved: solvedCount(c, s), total: c.questions.length,
    saved_at: new Date(s.savedAt).toISOString(), updated_at: new Date().toISOString(),
  }, { onConflict: 'user_id,case_id,scope' });
  useCloud.setState({ status: error ? 'error' : 'saved', at: Date.now() });
}

export async function deleteCloud(c: CaseData, scope = '') {
  const me = uid();
  if (me) await supabase.from('user_progress').delete().eq('user_id', me).eq('case_id', c.id).eq('scope', scope);
}

// Before the board opens: wait for sign-in state, then take the cloud copy if it is newer (max ~3 s, then go local).
export function useCloudReady(store: BoardStore | null, c: CaseData | null, scope: string, hydrated: boolean) {
  const ready = useAuth((s) => s.ready);
  const me = useAuth((s) => s.session?.user.id);
  const [done, setDone] = useState(false);
  useEffect(() => {
    setDone(false);
    if (!store || !c || !hydrated || !ready) return undefined;
    if (!me) { setDone(true); return undefined; }
    let live = true;
    const timeout = setTimeout(() => live && setDone(true), 3000);
    pull(store, c, scope).catch(() => 'none').finally(() => { clearTimeout(timeout); if (live) setDone(true); });
    return () => { live = false; clearTimeout(timeout); };
  }, [store, c, scope, hydrated, ready, me]);
  return done;
}

// While the board is open: push a few seconds after each change, and right away when the page is hidden.
export function useCloudSave(store: BoardStore, c: CaseData, scope: string) {
  const me = useAuth((s) => s.session?.user.id);
  useEffect(() => {
    if (!me) { useCloud.setState({ status: 'off' }); return undefined; }
    useCloud.setState({ status: 'saved' });
    let timer = 0;
    let pushed = -1;
    const flush = () => {
      window.clearTimeout(timer);
      const at = store.getState().savedAt;
      if (at && at !== pushed) { pushed = at; void push(store, c, scope); }
    };
    const later = () => { window.clearTimeout(timer); timer = window.setTimeout(flush, 2500); };
    // a local copy newer than the cloud one (e.g. played offline): upload it now
    void pull(store, c, scope).then((r) => {
      if (r === 'local' || r === 'none') flush();
      else pushed = store.getState().savedAt; // already in sync
    });
    const unsub = store.subscribe((s, prev) => { if (s.savedAt !== prev.savedAt) later(); });
    const onHide = () => { if (document.visibilityState === 'hidden') flush(); };
    document.addEventListener('visibilitychange', onHide);
    window.addEventListener('pagehide', flush);
    return () => {
      flush();
      unsub();
      document.removeEventListener('visibilitychange', onHide);
      window.removeEventListener('pagehide', flush);
    };
  }, [store, c, scope, me]);
}

