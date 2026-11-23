// Lists for the account page and the home page (kept apart from the board code so those pages stay light).
import { supabase } from './supabase';
import { useAuth } from './auth';

const uid = () => useAuth.getState().session?.user.id;

export interface SavedCase { case_id: string; solved: number; total: number; saved_at: string }
export interface MyRoom {
  id: string; case_id: string; status: 'lobby' | 'playing' | 'finished'; name: string;
  join_code: string | null; join_code_expires_at: string | null; role: 'host' | 'player';
  joined_at: string; solved: number; total: number; members: number;
}

export async function listSavedCases(): Promise<SavedCase[]> {
  const me = uid();
  if (!me) return [];
  const { data } = await supabase.from('user_progress').select('case_id, solved, total, saved_at')
    .eq('user_id', me).eq('scope', '').order('saved_at', { ascending: false });
  return (data || []) as SavedCase[];
}

type MemberRow = { role: 'host' | 'player'; joined_at: string; rooms: Omit<MyRoom, 'role' | 'joined_at' | 'solved' | 'total' | 'members'> | null };

export async function listMyRooms(): Promise<MyRoom[]> {
  const me = uid();
  if (!me) return [];
  const { data } = await supabase.from('room_members')
    .select('role, joined_at, rooms(id, case_id, status, name, join_code, join_code_expires_at)')
    .eq('user_id', me).order('joined_at', { ascending: false }).limit(50);
  const rows = ((data || []) as unknown as MemberRow[]).filter((r) => r.rooms);
  const ids = rows.map((r) => r.rooms!.id);
  if (!ids.length) return [];
  const [progress, members] = await Promise.all([
    supabase.from('room_progress').select('room_id, solved').in('room_id', ids),
    supabase.from('room_members').select('room_id').in('room_id', ids),
  ]);
  return rows.map((r) => {
    const p = (progress.data || []).filter((x) => x.room_id === r.rooms!.id);
    return {
      ...r.rooms!, role: r.role, joined_at: r.joined_at,
      solved: p.filter((x) => x.solved).length, total: p.length,
      members: (members.data || []).filter((x) => x.room_id === r.rooms!.id).length,
    };
  });
}
