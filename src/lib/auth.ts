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
      emailRedirectTo: `${window.location.origin}/dang-nhap?xong=1&next=${encodeURIComponent(next)}`,
      data: displayName ? { display_name: displayName } : undefined,
    },
  });
  if (error) throw error;
}

/** Play without email (Supabase anonymous sign-in): the account lives in this browser only. */
export async function signInAnonymous() {
  const { error } = await supabase.auth.signInAnonymously({ options: { data: { display_name: 'Điều tra viên' } } });
  if (error) throw new Error(/anonymous/i.test(error.message) ? 'Máy chủ chưa bật đăng nhập ẩn danh (Supabase → Authentication → Allow anonymous sign-ins).' : error.message);
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

export type OAuthProvider = 'google' | 'apple' | 'facebook' | 'azure' | 'github' | 'discord';
export const OAUTH_PROVIDERS: { id: OAuthProvider; label: string }[] = [
  { id: 'google', label: 'Google' },
  { id: 'apple', label: 'Apple' },
  { id: 'facebook', label: 'Facebook' },
  { id: 'azure', label: 'Microsoft' },
  { id: 'github', label: 'GitHub' },
  { id: 'discord', label: 'Discord' },
];

// Which SSO buttons to show: whatever is switched on in Supabase → Authentication → Sign In / Providers.
let providersCache: Promise<OAuthProvider[]> | null = null;
export function enabledProviders(): Promise<OAuthProvider[]> {
  if (!providersCache) {
    const url = import.meta.env.VITE_SUPABASE_URL as string;
    const key = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY as string;
    providersCache = fetch(`${url}/auth/v1/settings`, { headers: { apikey: key } })
      .then((r) => r.json())
      .then((j: { external?: Record<string, boolean> }) => OAUTH_PROVIDERS.map((p) => p.id).filter((id) => j.external?.[id]))
      .catch(() => { providersCache = null; return []; });
  }
  return providersCache;
}

export async function signInWithProvider(provider: OAuthProvider, next: string) {
  const { error } = await supabase.auth.signInWithOAuth({
    provider,
    options: { redirectTo: `${window.location.origin}/dang-nhap?xong=1&next=${encodeURIComponent(next)}` },
  });
  if (error) throw error;
}

export async function signOut() {
  await supabase.auth.signOut();
}
