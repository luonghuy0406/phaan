import { create } from 'zustand';
import type { Session } from '@supabase/supabase-js';
import { supabase, supabaseReady } from './supabase';

export interface Profile { id: string; display_name: string; color: string }

interface AuthState { ready: boolean; session: Session | null; profile: Profile | null }

export const useAuth = create<AuthState>(() => ({ ready: !supabaseReady, session: null, profile: null }));

async function loadProfile(id: string) {
  const { data } = await supabase.from('profiles').select('id, display_name, color').eq('id', id).maybeSingle();
  if (useAuth.getState().session?.user.id === id) useAuth.setState({ profile: data as Profile | null });
}

let started = false;
export function initAuth() {
  if (started || !supabaseReady) return;
  started = true;
  supabase.auth.getSession().then(({ data }) => {
    useAuth.setState({ session: data.session, ready: true });
    if (data.session) void loadProfile(data.session.user.id);
  });
  supabase.auth.onAuthStateChange((_event, session) => {
    useAuth.setState({ session, ready: true, ...(session ? {} : { profile: null }) });
    // never await Supabase calls inside this callback (it can deadlock the auth client)
    if (session) setTimeout(() => { void loadProfile(session.user.id); }, 0);
  });
}

export async function sendLoginCode(email: string, displayName: string, next: string) {
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      shouldCreateUser: true,
      emailRedirectTo: `${window.location.origin}/dang-nhap?tu-email=1&next=${encodeURIComponent(next)}`,
      data: displayName ? { display_name: displayName } : undefined,
    },
  });
  if (error) throw error;
}

export async function verifyLoginCode(email: string, token: string) {
  const { error } = await supabase.auth.verifyOtp({ email, token, type: 'email' });
  if (error) throw error;
}

export async function saveDisplayName(name: string) {
  const id = useAuth.getState().session?.user.id;
  if (!id) return;
  const display_name = name.trim().slice(0, 40);
  if (!display_name) return;
  const { error } = await supabase.from('profiles').update({ display_name }).eq('id', id);
  if (error) throw error;
  await loadProfile(id);
}

export async function signOut() {
  await supabase.auth.signOut();
}
