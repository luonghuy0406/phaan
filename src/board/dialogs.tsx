import { useEffect, useRef, useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { useBoard, useBoardState } from './context';
import { useUi, saveSettings } from './ui';
import { resetBoard } from './store';
import { deleteCloud } from '../lib/cloud';
import { caseNo } from '../lib/data';
import { useNavigate } from 'react-router-dom';
import { leaveRoom } from '../multiplayer/room';
import { Txt, Paras } from '../lib/text';

function Modal({ open, onClose, className = '', children }: { open: boolean; onClose: () => void; className?: string; children: ReactNode }) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const d = ref.current;
    if (!d) return;
    if (open && !d.open) d.showModal();
    if (!open && d.open) d.close();
  }, [open]);
  return (
    <dialog ref={ref} className={`dlg ${className}`} onClose={onClose} onClick={(e) => { if (e.target === ref.current) onClose(); }} data-ui>
      {open && <div className="dlg__body">{children}</div>}
    </dialog>
  );
}

export function Dialogs() {
  const dialog = useUi((s) => s.dialog);
  const set = useUi((s) => s.set);
  const { store } = useBoard();
  const close = () => {
    const first = dialog === 'intro' && !store.getState().seenIntro;
    if (dialog === 'intro') store.getState().setSeenIntro();
    set({ dialog: null, ...(first ? { tourStep: 0 } : {}) }); // first visit: walk through the board
  };
  return (
    <>
      <Modal open={dialog === 'intro'} onClose={close}><Intro onClose={close} /></Modal>
      <Modal open={dialog === 'finale'} onClose={close} className="dlg--finale"><Finale onClose={close} /></Modal>
      <Modal open={dialog === 'settings'} onClose={close}><Settings onClose={close} /></Modal>
    </>
  );
}

function Intro({ onClose }: { onClose: () => void }) {
  const { c } = useBoard();
  const seen = useBoardState((s) => s.seenIntro);
  const intro = c.intro || {};
  return (
    <>
      <p className="eyebrow">{caseNo(c)}</p>
      <h2><Txt>{intro.title || c.title}</Txt></h2>
      <div className="dlg__text"><Paras list={intro.paragraphs} /></div>
      {intro.objective && <p className="dlg__objective"><span>Nhiệm vụ</span><Txt>{intro.objective}</Txt></p>}
      <ul className="guide">
        <li><b>Di chuyển</b>Kéo nền để di chuyển bàn, kéo tài liệu để sắp xếp, chụm hai ngón để phóng to.</li>
        <li><b>Chạm vào đoạn văn</b>để tô dạ quang, trích vào sổ tay, nối dây đỏ, ghim bằng chứng hoặc chọn dòng khai.</li>
        <li><b>Apple Pencil</b>viết thẳng lên tài liệu và mặt bàn; ngón tay vẫn dùng để di chuyển. Nét vẽ đi theo tài liệu khi bạn kéo hay xoay.</li>
        <li><b>Bút · Dạ quang · Tẩy</b>trên thanh công cụ; chạm lại vào Bút để đổi màu và cỡ nét.</li>
        <li><b>Kết luận</b>Trả lời từng trọng điểm để mở niêm phong hồ sơ tiếp theo.</li>
      </ul>
      <div className="dlg__actions"><button type="button" className="btn btn--primary" onClick={onClose}>{seen ? 'Tiếp tục điều tra' : 'Bắt đầu điều tra'}</button></div>
    </>
  );
}

function Finale({ onClose }: { onClose: () => void }) {
  const { c } = useBoard();
  const q = useBoardState((s) => s.q);
  const startedAt = useBoardState((s) => s.startedAt);
  const fin = c.finale || {};
  const hints = c.questions.reduce((n, x) => n + (q[x.id]?.hints || 0), 0);
  const tries = c.questions.reduce((n, x) => n + (q[x.id]?.tries || 0), 0);
  const minutes = Math.max(1, Math.round((Date.now() - startedAt) / 60000));
  return (
    <>
      <span className="stamp dlg__stamp">Đã phá án</span>
      <p className="eyebrow">{caseNo(c)} · Hồ sơ khép lại</p>
      <h2><Txt>{fin.title || 'Sự thật đã sáng tỏ'}</Txt></h2>
      <div className="dlg__text"><Paras list={fin.paragraphs} /></div>
      {!!c.epilogue?.length && (
        <div className="epilogue">
          <p className="eyebrow">Sau khi hồ sơ khép lại</p>
          {c.epilogue.map((e) => <div key={e.title} className="epilogue__item"><b>{e.title}</b><span><Txt>{e.text}</Txt></span></div>)}
        </div>
      )}
      <dl className="dlg__stats">
        <div><dt>Lần gửi kết luận</dt><dd>{tries}</dd></div>
        <div><dt>Gợi ý đã dùng</dt><dd>{hints}</dd></div>
        <div><dt>Thời gian</dt><dd>{minutes >= 60 ? `${Math.floor(minutes / 60)} giờ ${minutes % 60} phút` : `${minutes} phút`}</dd></div>
      </dl>
      <div className="dlg__actions">
        <button type="button" className="btn btn--ghost" onClick={onClose}>Xem lại bàn điều tra</button>
        <Link className="btn btn--primary" to="/#catalog">Mở hồ sơ khác</Link>
      </div>
    </>
  );
}

function Settings({ onClose }: { onClose: () => void }) {
  const { c, store, reg, fitAll, room } = useBoard();
  const navigate = useNavigate();
  const pencilDraws = useUi((s) => s.pencilDraws);
  const penSeen = useUi((s) => s.penSeen);
  const set = useUi((s) => s.set);
  const [armed, setArmed] = useState(false);
  return (
    <>
      <p className="eyebrow">Cài đặt</p>
      <h2>Bàn điều tra</h2>
      <label className="setting">
        <input type="checkbox" checked={pencilDraws} onChange={(e) => { set({ pencilDraws: e.target.checked }); saveSettings({ pencilDraws: e.target.checked }); }} />
        <span>
          <b>Apple Pencil luôn viết</b>
          Kể cả khi đang ở chế độ Di chuyển, bút viết còn ngón tay di chuyển bàn (giống GoodNotes). Tắt nếu bạn muốn dùng bút để kéo tài liệu.
          {penSeen ? ' Đã nhận Apple Pencil trên thiết bị này.' : ''}
        </span>
      </label>
      <div className="setting">
        <span>
          <b>Chơi toàn màn hình trên iPad</b>
          Trong Safari, bấm nút Chia sẻ rồi chọn “Thêm vào màn hình chính”. Mở từ biểu tượng đó để có toàn bộ màn hình cho bàn điều tra.
        </span>
      </div>
      <div className="dlg__actions dlg__actions--split">
        <button type="button" className="btn btn--ghost" onClick={() => { store.getState().relayout(reg.defaults); setTimeout(() => fitAll(), 50); onClose(); }}>Xếp lại bàn</button>
        <button type="button" className="btn btn--danger" onClick={async () => {
          if (!armed) { setArmed(true); return; }
          await Promise.all([resetBoard(c, room?.id), deleteCloud(c, room?.id ?? '').catch(() => {})]);
          window.location.reload();
        }}>{armed ? 'Bấm lần nữa để xoá' : room ? 'Xoá ghi chép cá nhân' : 'Chơi lại từ đầu'}</button>
        {room && (
          <button type="button" className="btn btn--danger" onClick={async () => { await leaveRoom(room.id).catch(() => {}); navigate('/#catalog'); }}>Rời phòng</button>
        )}
      </div>
    </>
  );
}

/* ── first-visit walkthrough (4 short steps) ── */
const DEFAULT_TOUR = [
  { title: 'Đọc hồ sơ', text: 'Mỗi tờ giấy trên bàn là một tài liệu trong hồ sơ. Chạm vào một đoạn văn để tô dạ quang, trích vào sổ tay hoặc nối dây đỏ.' },
  { title: 'Di chuyển bàn', text: 'Kéo nền để di chuyển, chụm hai ngón (hoặc cuộn chuột) để phóng to. Nút “Tài liệu” mở danh sách để tìm nhanh.' },
  { title: 'Ghi chép', text: 'Dùng Bút, Dạ quang và Tẩy trên thanh công cụ. Trên iPad, Apple Pencil luôn viết, còn ngón tay để di chuyển.' },
  { title: 'Trả lời', text: 'Mở “Kết luận” để trả lời từng trọng điểm. Trả lời đúng, hồ sơ của trọng điểm tiếp theo sẽ được mở niêm phong.' },
];

export function Tour() {
  const { c } = useBoard();
  const step = useUi((s) => s.tourStep);
  const set = useUi((s) => s.set);
  if (step == null) return null;
  const steps = c.tour?.length ? c.tour : DEFAULT_TOUR;
  const cur = steps[step];
  if (!cur) return null;
  const last = step === steps.length - 1;
  return (
    <div className="tour" role="dialog" aria-label="Hướng dẫn nhanh" data-ui>
      <p className="tour__step">Bước {step + 1}/{steps.length}</p>
      <h3>{cur.title}</h3>
      <p><Txt>{cur.text}</Txt></p>
      <div className="tour__actions">
        <button type="button" className="link-btn" onClick={() => set({ tourStep: null })}>Bỏ qua</button>
        <button type="button" className="btn btn--primary btn--small" onClick={() => set(last ? { tourStep: null, panel: 'questions' } : { tourStep: step + 1 })}>
          {last ? 'Mở Kết luận' : 'Tiếp'}
        </button>
      </div>
    </div>
  );
}
