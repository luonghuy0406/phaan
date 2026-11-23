// One live room connection at a time: rows from Postgres (RLS: members only) kept fresh by Realtime,
// plus Presence on the private channel "room:<id>" for who is online.
import { useEffect } from 'react';
import { create } from 'zustand';
import type { RealtimeChannel } from '@supabase/supabase-js';
import { supabase, errorText } from '../lib/supabase';
import { useAuth } from '../lib/auth';

export interface RoomRow {
  id: string; case_id: string; host_id: string; name: string;
  status: 'lobby' | 'playing' | 'finished';
  join_code: string | null; join_code_expires_at: string | null;
  max_players: number; created_at: string; started_at: string | null; finished_at: string | null;
}
export interface Member { user_id: string; role: 'host' | 'player'; joined_at: string; name: string; color: string }
export interface ProgressRow { question_id: string; solved: boolean; solved_by: string | null; tries: number; hints: number }
export interface SharedRow { pins: (string | null)[]; lines: Record<string, string>; picks: Record<string, number[]>; updated_by: string | null; updated_at: string }
export interface RoomNote { id: string; room_id: string; user_id: string; kind: 'text' | 'quote'; body: string; ref: { doc: string; key: string } | null; created_at: string; updated_at: string }
export interface RoomEvent { id: number; user_id: string | null; kind: string; payload: Record<string, unknown>; created_at: string }

interface RoomStore {
  roomId: string | null;
  status: 'idle' | 'loading' | 'ready' | 'error';
  error: string | null;
  room: RoomRow | null;
  members: Member[];
  online: string[];
  progress: Record<string, ProgressRow>;
  shared: SharedRow | null;
  notes: RoomNote[];
  events: RoomEvent[];
  lastEvent: RoomEvent | null;
}

const EMPTY: RoomStore = {
  roomId: null, status: 'idle', error: null, room: null, members: [], online: [], progress: {}, shared: null, notes: [], events: [], lastEvent: null,
};
export const useRoom = create<RoomStore>(() => EMPTY);

export const memberName = (id: string | null | undefined) => useRoom.getState().members.find((m) => m.user_id === id)?.name || 'Một thành viên';

type MemberRow = { user_id: string; role: 'host' | 'player'; joined_at: string; profiles: { display_name: string; color: string } | null };

async function loadMembers(roomId: string) {
  const { data } = await supabase.from('room_members').select('user_id, role, joined_at, profiles(display_name, color)').eq('room_id', roomId).order('joined_at');
  const members = ((data || []) as unknown as MemberRow[]).map((m) => ({
    user_id: m.user_id, role: m.role, joined_at: m.joined_at, name: m.profiles?.display_name || 'Điều tra viên', color: m.profiles?.color || '#d9452f',
  }));
  if (useRoom.getState().roomId === roomId) useRoom.setState({ members });
  return members;
}

async function loadAll(roomId: string) {
  const [room, progress, shared, notes, events] = await Promise.all([
    supabase.from('rooms').select('*').eq('id', roomId).maybeSingle(),
    supabase.from('room_progress').select('question_id, solved, solved_by, tries, hints').eq('room_id', roomId),
    supabase.from('room_state').select('pins, lines, picks, updated_by, updated_at').eq('room_id', roomId).maybeSingle(),
    supabase.from('room_notes').select('*').eq('room_id', roomId).order('created_at'),
    supabase.from('room_events').select('id, user_id, kind, payload, created_at').eq('room_id', roomId).order('id', { ascending: false }).limit(30),
  ]);
  if (room.error) throw room.error;
  if (!room.data) throw new Error('NOT_MEMBER');
  await loadMembers(roomId);
  const map: Record<string, ProgressRow> = {};
  (progress.data || []).forEach((p) => { map[p.question_id] = p as ProgressRow; });
  useRoom.setState({
    room: room.data as RoomRow,
    progress: map,
    shared: (shared.data as SharedRow | null) ?? null,
    notes: (notes.data || []) as RoomNote[],
    events: ((events.data || []) as RoomEvent[]).reverse(),
  });
}

// Mount in every room page. Keeps useRoom in sync while mounted.
export function useRoomConnection(roomId: string | undefined) {
  const userId = useAuth((s) => s.session?.user.id);
  const profile = useAuth((s) => s.profile);
  useEffect(() => {
    if (!roomId || !userId) return undefined;
    let channel: RealtimeChannel | null = null;
    let live = true;
    useRoom.setState({ ...EMPTY, roomId, status: 'loading' });
    const filter = `room_id=eq.${roomId}`;
    (async () => {
      try {
        await loadAll(roomId);
      } catch (e) {
        if (live) useRoom.setState({ status: 'error', error: errorText(e) });
        return;
      }
      if (!live) return;
      await supabase.realtime.setAuth();
      channel = supabase.channel(`room:${roomId}`, { config: { private: true, presence: { key: userId } } })
        .on('postgres_changes', { event: '*', schema: 'public', table: 'rooms', filter: `id=eq.${roomId}` }, (p) => {
          if (p.eventType === 'DELETE') useRoom.setState({ status: 'error', error: 'Phòng đã đóng.' });
          else useRoom.setState({ room: p.new as RoomRow });
        })
        .on('postgres_changes', { event: '*', schema: 'public', table: 'room_members', filter }, (p) => {
          const gone = p.eventType === 'DELETE' && (p.old as { user_id?: string }).user_id === userId;
          if (gone) useRoom.setState({ status: 'error', error: 'Bạn đã rời phòng hoặc bị mời ra khỏi phòng.' });
          else void loadMembers(roomId);
        })
        .on('postgres_changes', { event: '*', schema: 'public', table: 'room_progress', filter }, (p) => {
          const row = p.new as ProgressRow;
          if (row?.question_id) useRoom.setState({ progress: { ...useRoom.getState().progress, [row.question_id]: row } });
        })
        .on('postgres_changes', { event: '*', schema: 'public', table: 'room_state', filter }, (p) => {
          useRoom.setState({ shared: p.new as SharedRow });
        })
        .on('postgres_changes', { event: '*', schema: 'public', table: 'room_notes', filter }, (p) => {
          const notes = useRoom.getState().notes;
          if (p.eventType === 'DELETE') useRoom.setState({ notes: notes.filter((n) => n.id !== (p.old as RoomNote).id) });
          else {
            const n = p.new as RoomNote;
            useRoom.setState({ notes: notes.some((x) => x.id === n.id) ? notes.map((x) => (x.id === n.id ? n : x)) : [...notes, n] });
          }
        })
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'room_events', filter }, (p) => {
          const ev = p.new as RoomEvent;
          useRoom.setState({ events: [...useRoom.getState().events, ev].slice(-30), lastEvent: ev });
        })
        .on('presence', { event: 'sync' }, () => {
          useRoom.setState({ online: Object.keys(channel?.presenceState() || {}) });
        })
        .subscribe((status) => {
          if (status === 'SUBSCRIBED') {
            void channel?.track({ at: Date.now() });
            void loadAll(roomId).catch(() => {}); // catch anything that changed while connecting
          }
        });
      useRoom.setState({ status: 'ready' });
    })();
    return () => {
      live = false;
      if (channel) void supabase.removeChannel(channel);
      useRoom.setState(EMPTY);
    };
  }, [roomId, userId]);
  // display name changed: reload members so teammates' labels stay right
  useEffect(() => { if (roomId && profile) void loadMembers(roomId); }, [roomId, profile]);
}

/* ── calls ── */
async function rpc<T>(fn: string, args: Record<string, unknown>): Promise<T> {
  const { data, error } = await supabase.rpc(fn, args);
  if (error) throw new Error(errorText(error));
  return data as T;
}

export const createRoom = (caseId: string, name = '') => rpc<RoomRow>('create_room', { p_case_id: caseId, p_name: name });
export const refreshJoinCode = (roomId: string) => rpc<RoomRow>('refresh_join_code', { p_room: roomId });
export const startRoom = (roomId: string) => rpc<void>('start_room', { p_room: roomId });
export const leaveRoom = (roomId: string) => rpc<void>('leave_room', { p_room: roomId });
export const kickMember = (roomId: string, userId: string) => rpc<void>('kick_member', { p_room: roomId, p_user: userId });
export async function joinRoom(code: string): Promise<string> {
  const r = await rpc<{ ok: boolean; room_id?: string; error?: string }>('join_room', { p_code: code });
  if (!r.ok || !r.room_id) throw new Error(errorText(r.error || 'INVALID_CODE'));
  return r.room_id;
}
export const submitAnswer = (roomId: string, questionId: string, input: unknown) =>
  rpc<{ ok: boolean; correct?: boolean; error?: string }>('submit_answer', { p_room: roomId, p_question: questionId, p_input: input });
export const useHintRemote = (roomId: string, questionId: string) => rpc<number>('use_hint', { p_room: roomId, p_question: questionId });

export async function addRoomNote(roomId: string, note: { kind: 'text' | 'quote'; body: string; ref?: { doc: string; key: string } }) {
  const { error } = await supabase.from('room_notes').insert({ room_id: roomId, kind: note.kind, body: note.body.slice(0, 4000), ref: note.ref ?? null });
  if (error) throw new Error(errorText(error));
}
export async function updateRoomNote(id: string, body: string) {
  await supabase.from('room_notes').update({ body: body.slice(0, 4000), updated_at: new Date().toISOString() }).eq('id', id);
}
export async function deleteRoomNote(id: string) {
  await supabase.from('room_notes').delete().eq('id', id);
}
