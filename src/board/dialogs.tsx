import { useEffect, useRef, useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { useBoard, useBoardState } from './context';
import { useUi, saveSettings, reopenAfterRemount } from './ui';
import { resetBoard } from './store';
import { deleteCloud } from '../lib/cloud';
import { caseNo } from '../lib/data';
import { useNavigate } from 'react-router-dom';
import { leaveRoom } from '../multiplayer/room';
import { ttsEngine, isDeviceVoiceCached, removeDeviceVoice, MODEL_MB } from '../lib/tts';
import { Txt, Paras } from '../lib/text';
import { useAudio, playVoice, stopVoice } from '../lib/sfx';
import { caseBase } from '../lib/data';
import { Icon } from './icons';
import { SuspectGallery } from './suspects';
import { Interrogation } from './interrogate';
import { interrogationEnabled, resetInterrogation } from '../lib/interrogate';

function Modal({ open, onClose, className = '', children }: { open: boolean; onClose: () => void; className?: string; children: ReactNode }) {
  const ref = useRef<HTMLDialogElement>(null);
  const openRef = useRef(open);
  openRef.current = open;
  useEffect(() => {
    const d = ref.current;
    if (!d) return;
    if (open && !d.open) d.showModal();
    if (!open && d.open) d.close();
  }, [open]);
  // the native close event also fires when another dialog takes over (open turned false): only a close by the player counts
  return (
    <dialog ref={ref} className={`dlg ${className}`} onClose={() => { if (openRef.current) onClose(); }} onClick={(e) => { if (e.target === ref.current) onClose(); }} data-ui>
      {open && <div className="dlg__body">{children}</div>}
    </dialog>
  );
}

export function Dialogs() {
  const dialog = useUi((s) => s.dialog);
  const set = useUi((s) => s.set);
  const { store } = useBoard();
  const close = () => {
    stopVoice();
    if (dialog === 'interrogate') reopenAfterRemount(null); // the player closed the room: never bring it back
    const first = dialog === 'intro' && !store.getState().seenIntro;
    if (dialog === 'intro') store.getState().setSeenIntro();
    set({ dialog: null, ...(first ? { tourStep: 0 } : {}) }); // first visit: walk through the board
  };
  return (
    <>
      <Modal open={dialog === 'intro'} onClose={close}><Intro onClose={close} /></Modal>
      <Modal open={dialog === 'finale'} onClose={close} className="dlg--finale"><Finale onClose={close} /></Modal>
      <Modal open={dialog === 'settings'} onClose={close}><Settings onClose={close} /></Modal>
      <Modal open={dialog === 'beat'} onClose={close} className="dlg--beat"><Beat onClose={close} /></Modal>
      <Modal open={dialog === 'suspects'} onClose={close} className="dlg--wide dlg--dossier"><Suspects onClose={close} /></Modal>
      <Modal open={dialog === 'interrogate'} onClose={close} className="dlg--itg"><Interrogation onClose={close} /></Modal>
    </>
  );
}

function Intro({ onClose }: { onClose: () => void }) {
  const { c } = useBoard();
  const seen = useBoardState((s) => s.seenIntro);
  // intro may be written as an object, a plain string, or be missing (then fall back to the synopsis)
  const raw = c.intro as unknown;
  const intro = typeof raw === 'string'
    ? { title: undefined, paragraphs: raw.split(/\n\s*\n/).filter(Boolean), objective: undefined }
    : (c.intro || {});
  const paras = intro.paragraphs?.length ? intro.paragraphs
    : Array.isArray(c.synopsis) ? c.synopsis : typeof c.synopsis === 'string' ? [c.synopsis as string] : [];
  const objective = intro.objective || 'Đọc kỹ tài liệu, đối chiếu lời khai và trả lời từng trọng điểm để tìm ra sự thật.';
  return (
    <>
      <p className="eyebrow">{caseNo(c)}</p>
      <h2><Txt>{intro.title || c.title}</Txt></h2>
      {c.audio?.intro && <VoiceButton src={caseBase(c.id) + c.audio.intro} label="Nghe lời dẫn" />}
      <div className="dlg__text"><Paras list={paras} /></div>
      <p className="dlg__objective"><span>Nhiệm vụ</span><Txt>{objective}</Txt></p>
      <ul className="guide">
        <li><b>Di chuyển</b>Kéo ở bất kỳ đâu (cả trên tài liệu) để lướt bàn, chụm hai ngón để phóng to. Tài liệu đứng yên; muốn xếp lại thì kéo thanh tiêu đề có dấu ⠿.</li>
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
  // finale may be { title, paragraphs[] }, { culprit, text } or a plain string
  const rawFin = c.finale as unknown as { title?: string; paragraphs?: string[]; text?: string; culprit?: string } | string | undefined;
  const fin = typeof rawFin === 'string' ? { paragraphs: rawFin.split(/\n\s*\n/) }
    : { ...(rawFin || {}), paragraphs: rawFin?.paragraphs?.length ? rawFin.paragraphs : rawFin?.text ? String(rawFin.text).split(/\n\s*\n/) : [] };
  const hints = c.questions.reduce((n, x) => n + (q[x.id]?.hints || 0), 0);
  const tries = c.questions.reduce((n, x) => n + (q[x.id]?.tries || 0), 0);
  const minutes = Math.max(1, Math.round((Date.now() - startedAt) / 60000));
  // each question needs one correct submission; everything above that was a wrong guess
  const wrongs = Math.max(0, tries - c.questions.length);
  const score = Math.max(0, 100 - wrongs * 12 - hints * 8);
  const rank = score >= 85 ? { stars: 3, name: 'Thám tử lừng danh', note: 'Gần như không cần gợi ý, rất ít lần kết luận sai.' }
    : score >= 60 ? { stars: 2, name: 'Điều tra viên vững nghề', note: 'Suy luận chắc tay, đôi lúc cần thêm gợi ý.' }
      : score >= 30 ? { stars: 1, name: 'Điều tra viên', note: 'Đã phá được án, nhưng còn nhiều lần đoán thử.' }
        : { stars: 0, name: 'Điều tra viên tập sự', note: 'Hãy thử lại hồ sơ khác và dựa nhiều hơn vào tài liệu.' };
  return (
    <>
      <span className="stamp dlg__stamp">Đã phá án</span>
      <p className="eyebrow">{caseNo(c)} · Hồ sơ khép lại</p>
      <h2><Txt>{fin.title || 'Sự thật đã sáng tỏ'}</Txt></h2>
      {c.audio?.finale && <VoiceButton src={caseBase(c.id) + c.audio.finale} label="Nghe kết thúc" />}
      <div className="dlg__text"><Paras list={fin.paragraphs} /></div>
      {!!c.epilogue?.length && (
        <div className="epilogue">
          <p className="eyebrow">Sau khi hồ sơ khép lại</p>
          {c.epilogue.map((e) => <div key={e.title} className="epilogue__item"><b>{e.title}</b><span><Txt>{e.text}</Txt></span></div>)}
        </div>
      )}
      <div className="rank" aria-label={`Xếp hạng: ${rank.name}, ${rank.stars} trên 3 sao`}>
        <span className="rank__stars" aria-hidden="true">{[0, 1, 2].map((i) => <i key={i} className={i < rank.stars ? 'on' : ''}>★</i>)}</span>
        <span className="rank__body"><b>{rank.name}</b><small>{rank.note} Điểm điều tra: {score}/100.</small></span>
      </div>
      <dl className="dlg__stats">
        <div><dt>Kết luận sai</dt><dd>{wrongs}</dd></div>
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
          Kể cả khi đang ở chế độ Di chuyển, bút viết còn ngón tay di chuyển bàn (giống GoodNotes). Tắt nếu bạn muốn dùng bút để lướt bàn hoặc kéo thanh tiêu đề tài liệu.
          {penSeen ? ' Đã nhận Apple Pencil trên thiết bị này.' : ''}
        </span>
      </label>
      <AudioSetting />
      <VoiceSetting />
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
          await Promise.all([resetBoard(c, room?.id), deleteCloud(c, room?.id ?? '').catch(() => {}), room ? Promise.resolve() : resetInterrogation(c.id).catch(() => {})]);
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
  { title: 'Di chuyển bàn', text: 'Kéo ở bất kỳ đâu, kể cả trên tài liệu, để lướt bàn; chụm hai ngón (hoặc cuộn chuột) để phóng to. Muốn xếp lại tài liệu, kéo thanh tiêu đề có dấu ⠿. Nút “Tài liệu” mở danh sách để tìm nhanh.' },
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

// On-device voice: show whether it is downloaded and let the player free the space.
function VoiceSetting() {
  const [cached, setCached] = useState<boolean | null>(null);
  const [busy, setBusy] = useState(false);
  useEffect(() => { if (ttsEngine() === 'device') void isDeviceVoiceCached().then(setCached); }, []);
  if (ttsEngine() !== 'device' || cached === null) return null;
  return (
    <div className="setting">
      <span>
        <b>Giọng đọc AI</b>
        {cached
          ? `Đã tải về máy (khoảng ${MODEL_MB} MB). Đọc được cả khi không có mạng.`
          : `Chưa tải. Bấm nút loa trên một tài liệu để tải (khoảng ${MODEL_MB} MB, sẽ hỏi trước).`}
        {cached && (
          <button type="button" className="link-btn" style={{ display: 'block' }} disabled={busy} onClick={async () => {
            setBusy(true);
            await removeDeviceVoice();
            setCached(false);
            setBusy(false);
          }}>{busy ? 'Đang xoá…' : 'Xoá giọng đọc khỏi máy'}</button>
        )}
      </span>
    </div>
  );
}

/* ── narration: pre-generated clips (tools/gen-voice.mjs) ── */
function VoiceButton({ src, label, auto = false }: { src: string; label: string; auto?: boolean }) {
  const playing = useAudio((s) => s.voice === src);
  useEffect(() => {
    if (auto) void playVoice(src);
    return () => { if (useAudio.getState().voice === src) stopVoice(); };
  }, [src, auto]);
  return (
    <button type="button" className={`voice-btn${playing ? ' is-on' : ''}`} onClick={() => (playing ? stopVoice() : void playVoice(src))} aria-pressed={playing}>
      <Icon name="speaker" />
      <span>{playing ? 'Dừng đọc' : label}</span>
      {playing && <i className="voice-btn__wave" aria-hidden="true"><b /><b /><b /></i>}
    </button>
  );
}

/* ── the scene that opens a new round ── */
function Beat({ onClose }: { onClose: () => void }) {
  const { c } = useBoard();
  const stage = useUi((s) => s.beatStage);
  const effects = useAudio((s) => s.effects);
  const beat = c.beats?.find((b) => b.stage === stage);
  if (!beat) return null;
  return (
    <>
      <p className="eyebrow">Trọng điểm {beat.stage}{beat.kicker ? ` · ${beat.kicker}` : ''}</p>
      <h2><Txt>{beat.title || 'Hồ sơ mở rộng'}</Txt></h2>
      {/* the round was opened by a tap on "Kết luận", so the clip may start on its own when sound is on */}
      {beat.voice && <VoiceButton src={caseBase(c.id) + beat.voice} label="Nghe lời dẫn" auto={effects} />}
      <div className="dlg__text dlg__text--beat"><Paras list={beat.paragraphs} /></div>
      <div className="dlg__actions"><button type="button" className="btn btn--primary" onClick={onClose}>Mở hồ sơ mới</button></div>
    </>
  );
}

function AudioSetting() {
  const { c } = useBoard();
  const { effects, ambient, volume, setPrefs } = useAudio();
  return (
    <div className="setting setting--audio">
      <span>
        <b>Âm thanh</b>
        Tiếng giấy, con dấu, gợi ý{c.audio?.ambient ? ' và tiếng nền của hồ sơ' : ''}. Lời dẫn chuyện nghe bằng nút loa ở màn mở đầu, đầu mỗi trọng điểm và màn kết thúc.
        <span className="setting__row">
          <label><input type="checkbox" checked={effects} onChange={(e) => setPrefs({ effects: e.target.checked })} /> Hiệu ứng</label>
          {c.audio?.ambient && <label><input type="checkbox" checked={ambient} onChange={(e) => setPrefs({ ambient: e.target.checked })} /> Tiếng nền</label>}
          <label className="setting__vol">Âm lượng <input type="range" min={0} max={1} step={0.05} value={volume} onChange={(e) => setPrefs({ volume: Number(e.target.value) })} /></label>
        </span>
      </span>
    </div>
  );
}

function Suspects({ onClose }: { onClose: () => void }) {
  const { c } = useBoard();
  const set = useUi((s) => s.set);
  return (
    <>
      <p className="eyebrow">{caseNo(c)} · Hồ sơ nhân thân</p>
      <h2>Nghi phạm</h2>
      <p className="dlg__lead">Lý do mỗi người bị đưa vào diện nghi vấn lúc mở hồ sơ. Đối chiếu với tài liệu để loại trừ hoặc buộc tội.</p>
      <SuspectGallery onInterrogate={interrogationEnabled() && !!c.aiInterrogation ? (id) => set({ dialog: 'interrogate', interrogateId: id }) : undefined} />
      <div className="dlg__actions"><button type="button" className="btn btn--primary" onClick={onClose}>Quay lại bàn điều tra</button></div>
    </>
  );
}
