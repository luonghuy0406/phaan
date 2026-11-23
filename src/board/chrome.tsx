import { useEffect, useLayoutEffect, useRef, useState, useSyncExternalStore } from 'react';
import { Link } from 'react-router-dom';
import { useShallow } from 'zustand/react/shallow';
import { useBoard, useBoardState } from './context';
import { useUi, type Tool } from './ui';
import { Icon } from './icons';
import { MARKER_COLORS, MARKER_SIZES, PEN_COLORS, PEN_SIZES } from './ink';
import { currentQ, evidenceNeed, isSolved, stageOpen, NOTE_COLORS, type End } from './store';
import { caseNo, pad2 } from '../lib/data';
import { typeLabel } from './papers';
import { Avatar } from '../components/auth';
import { useRoom, addRoomNote } from '../multiplayer/room';

/* ── top bar ── */
function RoomPeople() {
  const members = useRoom((s) => s.members);
  const online = useRoom((s) => s.online);
  const set = useUi((s) => s.set);
  const here = members.filter((m) => online.includes(m.user_id));
  if (!members.length) return null;
  return (
    <button type="button" className="people" onClick={() => set({ panel: 'team' })} aria-label={`${here.length} người đang online`}>
      {here.slice(0, 4).map((m) => <Avatar key={m.user_id} name={m.name} color={m.color} size={30} />)}
      {here.length > 4 && <span className="people__more">+{here.length - 4}</span>}
    </button>
  );
}

export function Topbar() {
  const { c, room } = useBoard();
  const done = useBoardState((s) => c.questions.filter((q) => isSolved(s, q)).length);
  const panel = useUi((s) => s.panel);
  const indexOpen = useUi((s) => s.indexOpen);
  const set = useUi((s) => s.set);
  const toggle = (p: 'questions' | 'notebook') => set({ panel: panel === p ? null : p });
  return (
    <header className="topbar" data-ui>
      <Link className="topbar__back" to={`/ho-so/${c.id}`} aria-label="Về trang hồ sơ"><Icon name="back" /><span>Hồ sơ</span></Link>
      <div className="topbar__title">
        <span className="topbar__no">{caseNo(c)}</span>
        <strong>{c.title}</strong>
      </div>
      <div className="topbar__actions">
        {room && <RoomPeople />}
        <span className="topbar__progress">{done}/{c.questions.length} trọng điểm</span>
        <button type="button" className={`tb-btn${indexOpen ? ' is-on' : ''}`} onClick={() => set({ indexOpen: !indexOpen })}><Icon name="list" /><span>Tài liệu</span></button>
        <button type="button" className={`tb-btn${panel === 'notebook' ? ' is-on' : ''}`} onClick={() => toggle('notebook')}><Icon name="book" /><span>Sổ tay</span></button>
        <button type="button" className={`tb-btn tb-btn--accent${panel === 'questions' ? ' is-on' : ''}`} onClick={() => toggle('questions')}><Icon name="check" /><span>Kết luận</span></button>
        <button type="button" className="tb-btn tb-btn--icon" aria-label="Hướng dẫn" onClick={() => set({ dialog: 'intro' })}><Icon name="help" /></button>
        <button type="button" className="tb-btn tb-btn--icon" aria-label="Cài đặt" onClick={() => set({ dialog: 'settings' })}><Icon name="gear" /></button>
      </div>
    </header>
  );
}

/* ── toolbar ── */
const TOOLS: { id: Tool; icon: string; label: string; key: string }[] = [
  { id: 'move', icon: 'hand', label: 'Di chuyển', key: 'V' },
  { id: 'pen', icon: 'pen', label: 'Bút', key: 'P' },
  { id: 'marker', icon: 'marker', label: 'Dạ quang', key: 'H' },
  { id: 'eraser', icon: 'eraser', label: 'Tẩy', key: 'E' },
  { id: 'note', icon: 'note', label: 'Ghi chú', key: 'N' },
];

function useZoom() {
  const { cam } = useBoard();
  return useSyncExternalStore((cb) => cam.subscribe(cb), () => Math.round(cam.z * 100));
}

export function Toolbar() {
  const { store, cam, fitAll } = useBoard();
  const tool = useUi((s) => s.tool);
  const palette = useUi((s) => s.palette);
  const pen = useUi((s) => s.pen);
  const marker = useUi((s) => s.marker);
  const set = useUi((s) => s.set);
  const setTool = useUi((s) => s.setTool);
  const canUndo = useBoardState((s) => s.past.length > 0);
  const canRedo = useBoardState((s) => s.future.length > 0);
  const zoom = useZoom();
  const panel = useUi((s) => s.panel);
  const indexOpen = useUi((s) => s.indexOpen);
  const isMarker = tool === 'marker';
  const style = isMarker ? marker : pen;
  const colors = isMarker ? MARKER_COLORS : PEN_COLORS;
  const sizes = isMarker ? MARKER_SIZES : PEN_SIZES;
  return (
    <div className="toolbar-wrap" data-ui>
      {palette && (tool === 'pen' || tool === 'marker') && (
        <div className="palette" role="group" aria-label={isMarker ? 'Màu dạ quang' : 'Màu bút'}>
          {colors.map((col) => (
            <button key={col.id} type="button" className={`swatch${style.color === col.v ? ' is-on' : ''}`} style={{ '--sw': col.v } as React.CSSProperties}
              aria-label={col.label} onClick={() => set(isMarker ? { marker: { ...marker, color: col.v } } : { pen: { ...pen, color: col.v } })} />
          ))}
          <span className="palette__sep" />
          {sizes.map((sz, i) => (
            <button key={sz} type="button" className={`size${style.size === sz ? ' is-on' : ''}`} aria-label={['Nét mảnh', 'Nét vừa', 'Nét đậm'][i]}
              onClick={() => set(isMarker ? { marker: { ...marker, size: sz } } : { pen: { ...pen, size: sz } })}>
              <i style={{ width: 6 + i * 6, height: 6 + i * 6, background: style.color }} />
            </button>
          ))}
        </div>
      )}
      <div className="toolbar" role="toolbar" aria-label="Công cụ">
        <button type="button" className={`tool tool--label${indexOpen ? ' is-on' : ''}`} onClick={() => set({ indexOpen: !indexOpen })}><Icon name="list" /><span>Tài liệu</span></button>
        <span className="toolbar__sep" />
        {TOOLS.map((t) => (
          <button key={t.id} type="button" className={`tool${tool === t.id ? ' is-on' : ''}`} aria-pressed={tool === t.id} title={`${t.label} (${t.key})`} onClick={() => setTool(t.id)}>
            <Icon name={t.icon} />
            <span>{t.label}</span>
            {(t.id === 'pen' || t.id === 'marker') && <i className="tool__dot" style={{ background: t.id === 'pen' ? pen.color : marker.color }} />}
          </button>
        ))}
        <span className="toolbar__sep" />
        <button type="button" className="tool tool--sq" aria-label="Hoàn tác nét vẽ" title="Hoàn tác (⌘Z)" disabled={!canUndo} onClick={() => store.getState().undo()}><Icon name="undo" /></button>
        <button type="button" className="tool tool--sq" aria-label="Làm lại" title="Làm lại (⇧⌘Z)" disabled={!canRedo} onClick={() => store.getState().redo()}><Icon name="redo" /></button>
        <span className="toolbar__sep" />
        <button type="button" className="tool tool--sq" aria-label="Thu nhỏ" onClick={() => cam.zoomBy(0.8)}><Icon name="minus" /></button>
        <span className="toolbar__zoom">{zoom}%</span>
        <button type="button" className="tool tool--sq" aria-label="Phóng to" onClick={() => cam.zoomBy(1.25)}><Icon name="plus" /></button>
        <button type="button" className="tool tool--sq" aria-label="Xem toàn bộ bàn" title="Xem toàn bộ (0)" onClick={() => fitAll()}><Icon name="fit" /></button>
        <span className="toolbar__sep" />
        <button type="button" className={`tool tool--label tool--accent${panel === 'questions' ? ' is-on' : ''}`} onClick={() => set({ panel: panel === 'questions' ? null : 'questions' })}><Icon name="check" /><span>Kết luận</span></button>
      </div>
    </div>
  );
}

/* ── action menu (tap on a block / paper / note) ── */
const sameEnd = (a: End, b: End) => JSON.stringify(a) === JSON.stringify(b);

export function ActionMenu() {
  const { c, store, focusDoc, room } = useBoard();
  const menu = useUi((s) => s.menu);
  const set = useUi((s) => s.set);
  const toast = useUi((s) => s.showToast);
  const ref = useRef<HTMLDivElement>(null);
  const [pos, setPos] = useState<{ left: number; top: number } | null>(null);
  const st = useBoardState(useShallow((s) => ({ hl: s.hl, strings: s.strings, pins: s.pins, q: s.q, notes: s.notes })));

  useLayoutEffect(() => {
    if (!menu || !ref.current) { setPos(null); return; }
    const r = ref.current.getBoundingClientRect();
    const left = Math.min(Math.max(8, menu.x - r.width / 2), window.innerWidth - r.width - 8);
    const below = menu.y + 16;
    const top = below + r.height > window.innerHeight - 90 ? Math.max(8, menu.y - r.height - 16) : below;
    setPos({ left, top });
  }, [menu]);

  useEffect(() => {
    if (!menu) return undefined;
    const close = (e: PointerEvent) => { if (!ref.current?.contains(e.target as Node)) set({ menu: null }); };
    const esc = (e: KeyboardEvent) => { if (e.key === 'Escape') set({ menu: null }); };
    document.addEventListener('pointerdown', close, true);
    document.addEventListener('keydown', esc);
    return () => { document.removeEventListener('pointerdown', close, true); document.removeEventListener('keydown', esc); };
  }, [menu, set]);

  if (!menu) return null;
  const t = menu.target;
  const s = store.getState();
  const q = currentQ(c, s);
  const close = () => set({ menu: null });
  const items: { icon: string; label: string; run: () => void; primary?: boolean; danger?: boolean }[] = [];
  let title = '';
  let snippet = '';

  const pinItem = (doc: string) => {
    if (q?.type !== 'evidence') return;
    const pinned = st.pins.includes(doc);
    items.push({
      icon: 'pin', label: pinned ? 'Bỏ ghim bằng chứng' : 'Ghim làm bằng chứng', primary: !pinned, run: () => {
        const r = s.togglePin(doc, evidenceNeed(q));
        toast(r === 'full' ? `Đã ghim đủ ${evidenceNeed(q)} tài liệu. Bỏ bớt một ghim trước.` : r === 'pinned' ? 'Đã ghim làm bằng chứng.' : 'Đã bỏ ghim.');
      },
    });
  };
  const unlinkItem = (match: (e: End) => boolean, label: string) => {
    const attached = st.strings.filter((x) => match(x.a) || match(x.b));
    if (attached.length) {
      items.push({ icon: 'unlink', label: `${label} (${attached.length})`, danger: true, run: () => attached.forEach((x) => s.removeString(x.id)) });
    }
  };

  if (t.kind === 'block') {
    const doc = c.documents.find((d) => d.id === t.doc);
    title = doc ? `${pad2(doc.no ?? 0)} · ${doc.title}` : '';
    snippet = t.text.length > 110 ? `${t.text.slice(0, 110)}…` : t.text;
    if (q?.type === 'line' && t.line) {
      items.push({ icon: 'target', label: 'Chọn dòng này để trả lời', primary: true, run: () => { s.setLine(q.id, t.line!); toast('Đã chọn dòng. Mở "Kết luận" để gửi.'); } });
    }
    const hk = `${t.doc}:${t.key}`;
    const isHl = st.hl.includes(hk);
    items.push({ icon: 'highlight', label: isHl ? 'Bỏ tô dạ quang' : 'Tô dạ quang', run: () => s.toggleHl(hk) });
    items.push({ icon: 'quote', label: room ? 'Trích vào sổ của tôi' : 'Trích vào sổ tay', run: () => { s.addEntry({ kind: 'quote', text: t.text, ref: { doc: t.doc, key: t.key } }); toast('Đã trích vào Sổ tay.'); } });
    if (room) {
      items.push({ icon: 'quote', label: 'Trích vào sổ nhóm', run: () => {
        addRoomNote(room.id, { kind: 'quote', body: t.text, ref: { doc: t.doc, key: t.key } })
          .then(() => toast('Đã chia sẻ vào sổ nhóm.'), (e) => toast(String(e.message || e)));
      } });
    }
    items.push({ icon: 'link', label: 'Nối dây đỏ từ đây', run: () => { set({ pendingString: { doc: t.doc, key: t.key } }); } });
    pinItem(t.doc);
    unlinkItem((e) => sameEnd(e, { doc: t.doc, key: t.key }), 'Gỡ dây ở đoạn này');
  } else if (t.kind === 'doc') {
    const doc = c.documents.find((d) => d.id === t.doc);
    title = doc ? `${pad2(doc.no ?? 0)} · ${doc.title}` : '';
    pinItem(t.doc);
    items.push({ icon: 'eye', label: 'Xem cận cảnh', run: () => focusDoc(t.doc) });
    items.push({ icon: 'link', label: 'Nối dây đỏ từ tài liệu', run: () => set({ pendingString: { doc: t.doc } }) });
    items.push({ icon: 'rotate', label: 'Xoay 90°', run: () => s.rotateDoc(t.doc) });
    unlinkItem((e) => 'doc' in e && e.doc === t.doc, 'Gỡ mọi dây của tài liệu');
  } else if (t.kind === 'note') {
    title = 'Giấy ghi chú';
    const note = st.notes.find((n) => n.id === t.note);
    items.push({ icon: 'link', label: 'Nối dây đỏ từ ghi chú', run: () => set({ pendingString: { note: t.note } }) });
    items.push({ icon: 'color', label: 'Đổi màu giấy', run: () => s.setNote(t.note, { c: ((note?.c ?? 0) + 1) % NOTE_COLORS.length }) });
    unlinkItem((e) => 'note' in e && e.note === t.note, 'Gỡ dây');
    items.push({ icon: 'trash', label: 'Xoá ghi chú', danger: true, run: () => s.deleteNote(t.note) });
  }

  return (
    <div ref={ref} className="amenu" role="menu" data-ui style={pos ? { left: pos.left, top: pos.top } : { left: -9999, top: -9999 }}>
      {title && <p className="amenu__title">{title}</p>}
      {snippet && <p className="amenu__snippet">“{snippet}”</p>}
      {items.map((it, i) => (
        <button key={i} type="button" role="menuitem" className={`amenu__item${it.primary ? ' is-primary' : ''}${it.danger ? ' is-danger' : ''}`}
          onClick={() => { close(); it.run(); }}>
          <Icon name={it.icon} /><span>{it.label}</span>
        </button>
      ))}
    </div>
  );
}

export function PendingBanner() {
  const pending = useUi((s) => s.pendingString);
  const set = useUi((s) => s.set);
  if (!pending) return null;
  return (
    <div className="banner" role="status" data-ui>
      <Icon name="link" />
      <span>Chạm vào đoạn văn, tài liệu hoặc ghi chú thứ hai để nối dây đỏ.</span>
      <button type="button" onClick={() => set({ pendingString: null })}>Huỷ</button>
    </div>
  );
}

/* ── documents drawer ── */
export function DocIndex() {
  const { c, focusDoc } = useBoard();
  const open = useUi((s) => s.indexOpen);
  const set = useUi((s) => s.set);
  const openStages = useBoardState(useShallow((s) => [...new Set(c.documents.map((d) => d.stage ?? 1))].filter((n) => stageOpen(c, s, n))));
  const stages = [...new Set(c.documents.map((d) => d.stage ?? 1))].sort((a, b) => a - b);
  return (
    <nav className={`drawer${open ? ' is-open' : ''}`} aria-label="Danh sách tài liệu" aria-hidden={!open} data-ui>
      <div className="drawer__head">
        <h2>Tài liệu</h2>
        <button type="button" className="icon-btn" aria-label="Đóng" onClick={() => set({ indexOpen: false })}><Icon name="close" /></button>
      </div>
      <div className="drawer__list">
        {stages.map((st) => (
          <section className="idx" key={st}>
            <h3>Trọng điểm {st}{openStages.includes(st) ? '' : ' · niêm phong'}</h3>
            {openStages.includes(st) ? (
              <ul>
                {c.documents.filter((d) => (d.stage ?? 1) === st).map((d) => (
                  <li key={d.id}>
                    <button type="button" onClick={() => { if (window.innerWidth < 1100) set({ indexOpen: false }); focusDoc(d.id); }}>
                      <span className="idx__no">{pad2(d.no ?? 0)}</span>
                      <span className="idx__text"><span className="idx__type">{typeLabel(d.type)}</span>{d.title}</span>
                    </button>
                  </li>
                ))}
              </ul>
            ) : <p className="idx__locked">Giải xong trọng điểm trước để mở.</p>}
          </section>
        ))}
      </div>
    </nav>
  );
}

/* ── toast ── */
export function Toast() {
  const toast = useUi((s) => s.toast);
  const [shown, setShown] = useState(false);
  useEffect(() => {
    if (!toast) return undefined;
    setShown(true);
    const t = setTimeout(() => setShown(false), 3000);
    return () => clearTimeout(t);
  }, [toast]);
  return <div className={`toast${shown ? ' is-on' : ''}`} role="status" aria-live="polite">{toast?.text}</div>;
}
