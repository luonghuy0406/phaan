// Phòng thẩm vấn: hỏi một nghi phạm bằng lời, đặt tài liệu đang mở lên bàn để bác lời khai,
// ghi lại đoạn khai vào sổ tay, nghe giọng nghi phạm. Máy chủ quyết định nghi phạm khai nhận điều gì; AI chỉ đóng vai.
import { useCallback, useEffect, useRef, useState } from 'react';
import { useShallow } from 'zustand/react/shallow';
import { Link, useLocation } from 'react-router-dom';
import { useBoard, useBoardState } from './context';
import { useUi, reopenAfterRemount } from './ui';
import { stageOpen } from './store';
import { MyNotebook } from './panels';
import { useAuth, signInAnonymous } from '../lib/auth';
import { askSuspect, loadInterrogation, autoVoice, setAutoVoice, type Exchange } from '../lib/interrogate';
import { speak as ttsSpeak, stop as ttsStop, useTts, acceptTtsDownload, declineTtsDownload, prepareDeviceVoice, isDeviceVoiceCached, ttsEnabled, MODEL_MB } from '../lib/tts';
import { caseBase } from '../lib/data';
import { playSfx } from '../lib/sfx';
import { Icon } from './icons';

const MAX_EVIDENCE = 3;
type Line = { who: 'officer' | 'suspect' | 'note'; text: string; docs?: string[]; id?: number };

const toLines = (log: Exchange[]): Line[] => log.flatMap((e) => [
  { who: 'officer' as const, text: e.question, docs: e.evidence ? e.evidence.split(',') : [] },
  { who: 'suspect' as const, text: e.reply, id: e.id },
  ...(e.admitted?.length ? [{ who: 'note' as const, text: 'Lời khai đã thay đổi sau khi xem tài liệu.' }] : []),
]);

export function Interrogation({ onClose }: { onClose: () => void }) {
  const { c, store } = useBoard();
  const id = useUi((s) => s.interrogateId);
  const { session } = useAuth();
  const loc = useLocation();
  const p = c.suspects?.find((x) => x.id === id);
  const who = p ? (p.alias || p.name) : '';
  const openDocs = useBoardState(useShallow((s) => c.documents.filter((d) => stageOpen(c, s, d.stage ?? 1)).map((d) => d.id)));
  const stage = useBoardState((s) => Math.max(1, ...c.documents.filter((d) => stageOpen(c, s, d.stage ?? 1)).map((d) => d.stage ?? 1)));
  const titleOf = useCallback((docId: string) => {
    const d = c.documents.find((x) => x.id === docId);
    return d ? `Tài liệu ${String(d.no ?? 0).padStart(2, '0')} · ${d.title}` : docId;
  }, [c]);

  const [lines, setLines] = useState<Line[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const [msg, setMsg] = useState('');
  const [docs, setDocs] = useState<string[]>([]);
  const [left, setLeft] = useState<number | null>(null);
  const [notes, setNotes] = useState(false);
  const [auto, setAuto] = useState(autoVoice);
  const [picked, setPicked] = useState('');
  const [saved, setSaved] = useState('');
  const tts = useTts();
  const lineOf = (aid: string | null) => (aid && aid.startsWith('itg:') ? Number(aid.slice(4)) : null);
  const playingId = tts.status === 'playing' || tts.status === 'paused' ? lineOf(tts.activeId) : null;
  const voiceBusy = tts.status === 'loading' || tts.status === 'downloading' ? lineOf(tts.activeId) : null;
  const askedConsent = useRef(false);
  const logRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!p || !session) { setLoading(false); return; }
    let alive = true;
    setLoading(true);
    loadInterrogation(c.id, p.id)
      .then(({ log }) => { if (alive) setLines(toLines(log)); })
      .catch(() => {})
      .finally(() => { if (alive) setLoading(false); });
    return () => { alive = false; };
  }, [c.id, p?.id, session]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => { const el = logRef.current; if (el) el.scrollTop = el.scrollHeight; }, [lines, busy]);
  // load the voice model in the background (only if already on this device) and compile it before the first reply
  useEffect(() => { if (session && p) void prepareDeviceVoice(p.voice); }, [session, p?.id]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => () => { if (lineOf(useTts.getState().activeId) != null) ttsStop(); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // a passage selected inside one of the suspect's replies can go to the notebook
  useEffect(() => {
    const onSel = () => {
      const sel = document.getSelection();
      const node = sel?.anchorNode;
      const el = node && (node.nodeType === 1 ? node as Element : node.parentElement);
      const inReply = el?.closest('.itg__msg--suspect') && logRef.current?.contains(el);
      setPicked(inReply ? (sel?.toString() || '').replace(/\s+/g, ' ').trim().slice(0, 400) : '');
    };
    document.addEventListener('selectionchange', onSel);
    return () => document.removeEventListener('selectionchange', onSel);
  }, []);

  const flash = (t: string) => { setSaved(t); setTimeout(() => setSaved(''), 1800); };
  const toNotebook = (text: string) => {
    const t = text.replace(/^\(([^)]*)\)\s*/, '').trim();
    if (!t) return;
    store.getState().addEntry({ kind: 'text', text: `${who} khai (thẩm vấn): “${t}”` });
    document.getSelection()?.removeAllRanges();
    setPicked('');
    playSfx('hint');
    flash('Đã ghi vào sổ tay');
  };

  // on-device Supertonic: stage directions in brackets are acted, not read; a short first piece starts the voice sooner
  const speak = (logId: number, text: string) => {
    if (playingId === logId || voiceBusy === logId) { ttsStop(); return; }
    const spoken = text.replace(/\([^)]*\)/g, ' ').replace(/\s+/g, ' ').trim();
    if (spoken) void ttsSpeak(`itg:${logId}`, spoken, { voice: p?.voice, steps: 6, fastStart: true });
  };
  const autoSpeak = async (logId: number, text: string) => {
    // ask for the one-time download at most once per room visit; afterwards only the "Nghe" button asks
    if (!(await isDeviceVoiceCached(p?.voice)) && askedConsent.current) return;
    askedConsent.current = true;
    speak(logId, text);
  };

  if (!p) return null;

  const send = async () => {
    const text = msg.trim();
    if ((!text && !docs.length) || busy) return;
    setBusy(true); setErr('');
    const sent: Line = { who: 'officer', text, docs };
    setLines((l) => [...l, sent]);
    setMsg(''); setDocs([]);
    try {
      const r = await askSuspect(c.id, p.id, text, sent.docs || [], stage);
      setLines((l) => [...l, { who: 'suspect', text: r.reply, id: r.id ?? undefined }, ...(r.broke.length ? [{ who: 'note' as const, text: 'Lời khai đã thay đổi sau khi xem tài liệu.' }] : [])]);
      setLeft(r.remaining);
      if (r.broke.length) playSfx('correct');
      if (r.id && auto && ttsEnabled()) void autoSpeak(r.id, r.reply);
    } catch (e) {
      setErr((e as Error).message);
      setLines((l) => l.filter((x) => x !== sent));
      setMsg(text); setDocs(sent.docs || []);
    } finally {
      setBusy(false);
    }
  };

  const addDoc = (d: string) => { if (d && !docs.includes(d) && docs.length < MAX_EVIDENCE) setDocs([...docs, d]); };

  return (
    <div className={`itg${notes ? ' has-notes' : ''}`}>
      <header className="itg__head">
        {p.image && <img src={caseBase(c.id) + p.image} alt="" className="itg__photo" />}
        <div className="itg__who">
          <p className="eyebrow">Phòng thẩm vấn</p>
          <h2>{who}</h2>
          <p className="itg__role">{[p.alias ? p.name : '', p.age ? `${p.age} tuổi` : '', p.role].filter(Boolean).join(' · ')}</p>
        </div>
        {session && (
          <div className="itg__tools">
            <button type="button" className={`itg__tool${auto ? ' is-on' : ''}`} aria-pressed={auto} onClick={() => { setAuto(!auto); setAutoVoice(!auto); if (auto && lineOf(useTts.getState().activeId) != null) ttsStop(); }}
              title="Tự đọc câu trả lời mới bằng giọng nghi phạm">
              <Icon name="speaker" /><span>{auto ? 'Tự đọc: bật' : 'Tự đọc: tắt'}</span>
            </button>
            <button type="button" className={`itg__tool${notes ? ' is-on' : ''}`} aria-pressed={notes} onClick={() => setNotes(!notes)}>
              <Icon name="book" /><span>Sổ tay</span>
            </button>
          </div>
        )}
        <button type="button" className="icon-btn itg__close" aria-label="Đóng" onClick={() => { reopenAfterRemount(null); onClose(); }}><Icon name="close" /></button>
      </header>

      {!session ? (
        <div className="itg__login">
          <p>Thẩm vấn dùng AI trên máy chủ nên cần một tài khoản để giữ lượt hỏi riêng cho bạn. Không có email cũng được: tài khoản sẽ gắn với trình duyệt này.</p>
          <div className="itg__login-actions">
            <button type="button" className="btn btn--primary" disabled={busy} onClick={async () => {
              setBusy(true); setErr('');
              // the board is rebuilt once the new account's progress loads: come back to this room afterwards
              reopenAfterRemount({ dialog: 'interrogate', interrogateId: p.id });
              try { await signInAnonymous(); } catch (e) { reopenAfterRemount(null); setErr((e as Error).message); } finally { setBusy(false); }
            }}>{busy ? 'Đang mở phòng…' : 'Thẩm vấn ngay (không cần email)'}</button>
            <Link className="btn btn--ghost" to={`/dang-nhap?next=${encodeURIComponent(loc.pathname)}`} onClick={onClose}>Đăng nhập bằng email</Link>
          </div>
          {err && <p className="itg__err" role="alert">{err}</p>}
        </div>
      ) : (
        <>
          <div className="itg__main">
            <div className="itg__log" ref={logRef} aria-live="polite">
              {loading && <p className="itg__hint">Đang mở biên bản…</p>}
              {!loading && !lines.length && (
                <p className="itg__hint">Đặt câu hỏi như một điều tra viên. Lời khai có thể sai sự thật: muốn bác bỏ, hãy đặt tài liệu lên bàn. Bôi chọn một đoạn câu trả lời để ghi vào sổ tay.</p>
              )}
              {lines.map((l, i) => (
                <div key={i} className={`itg__msg itg__msg--${l.who}${l.id && l.id === playingId ? ' is-speaking' : ''}`}>
                  {!!l.docs?.length && (
                    <span className="itg__docs">{l.docs.map((d) => <span key={d} className="itg__doc"><Icon name="pin" />{titleOf(d)}</span>)}</span>
                  )}
                  {l.text && <span className="itg__text">{l.text}</span>}
                  {l.who === 'suspect' && (
                    <span className="itg__msg-actions">
                      {l.id && (
                        <button type="button" className="itg__mini" onClick={() => speak(l.id!, l.text)} aria-label={l.id === playingId ? 'Dừng đọc' : 'Nghe câu này'}>
                          <Icon name={l.id === playingId ? 'pause' : 'speaker'} />{voiceBusy === l.id ? 'Đang chuẩn bị…' : l.id === playingId ? 'Dừng' : 'Nghe'}
                        </button>
                      )}
                      <button type="button" className="itg__mini" onClick={() => toNotebook(l.text)}><Icon name="note" />Ghi cả câu</button>
                    </span>
                  )}
                </div>
              ))}
              {busy && <div className="itg__msg itg__msg--suspect itg__typing" aria-label="Đang trả lời"><i /><i /><i /></div>}
            </div>
            {notes && <aside className="itg__notes" aria-label="Sổ tay"><MyNotebook embedded /></aside>}
          </div>

          <footer className="itg__foot">
            {lineOf(tts.activeId) != null && tts.status === 'consent' && (
              <div className="itg__voice">
                <span>Nghe giọng nghi phạm: tải giọng đọc về máy một lần (khoảng {MODEL_MB} MB), sau đó đọc ngay trên thiết bị, không cần mạng.</span>
                <button type="button" className="btn btn--small btn--primary" onClick={() => acceptTtsDownload()}>Tải giọng đọc</button>
                <button type="button" className="btn btn--small btn--ghost" onClick={() => declineTtsDownload()}>Để sau</button>
              </div>
            )}
            {lineOf(tts.activeId) != null && tts.status === 'downloading' && tts.download && (
              <div className="itg__voice">
                <span>Đang tải giọng đọc… {Math.round((tts.download.loaded / Math.max(1, tts.download.total)) * 100)}%</span>
                <progress max={tts.download.total} value={tts.download.loaded} />
              </div>
            )}
            {lineOf(tts.activeId) != null && tts.status === 'error' && tts.error && <div className="itg__voice"><span className="itg__err">{tts.error}</span></div>}
            {(picked || saved) && (
              <div className="itg__picked">
                {saved ? <span className="itg__saved">{saved}</span> : (
                  <>
                    <span className="itg__quote">“{picked.length > 90 ? `${picked.slice(0, 90)}…` : picked}”</span>
                    {/* onPointerDown keeps the selection alive on iPad until the tap lands */}
                    <button type="button" className="btn btn--small btn--primary" onPointerDown={(e) => e.preventDefault()} onClick={() => toNotebook(picked)}>Ghi đoạn này vào sổ</button>
                  </>
                )}
              </div>
            )}
            <div className="itg__evidence">
              {docs.map((d) => (
                <span key={d} className="itg__chip"><Icon name="pin" />{titleOf(d)}
                  <button type="button" aria-label="Bỏ tài liệu này" onClick={() => setDocs(docs.filter((x) => x !== d))}><Icon name="close" /></button>
                </span>
              ))}
              {docs.length < MAX_EVIDENCE && (
                <label className="itg__add">
                  <Icon name="plus" />
                  <select value="" onChange={(e) => addDoc(e.target.value)} aria-label="Đặt tài liệu lên bàn">
                    <option value="">{docs.length ? 'Thêm tài liệu…' : `Đặt tài liệu lên bàn (tối đa ${MAX_EVIDENCE})…`}</option>
                    {openDocs.filter((d) => !docs.includes(d)).map((d) => <option key={d} value={d}>{titleOf(d)}</option>)}
                  </select>
                </label>
              )}
            </div>
            <div className="itg__compose">
              <textarea value={msg} onChange={(e) => setMsg(e.target.value.slice(0, 400))} rows={2} placeholder={`Hỏi ${who}…`}
                onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); void send(); } }} />
              <button type="button" className="btn btn--primary itg__send" onClick={() => void send()} disabled={busy || (!msg.trim() && !docs.length)}>{busy ? 'Đang chờ…' : 'Hỏi'}</button>
            </div>
            <div className="itg__status">
              {err ? <span className="itg__err" role="alert">{err}</span> : <span>{left != null ? `Còn ${left} lượt hỏi hôm nay` : 'Enter để gửi, Shift+Enter xuống dòng'}</span>}
            </div>
          </footer>
        </>
      )}
    </div>
  );
}
