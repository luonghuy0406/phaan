// Báo cáo kết luận trước kiểm sát viên (AI): hỏi lần lượt từng ý, điều tra viên gõ câu trả lời.
// Xong mọi ý thì câu hỏi được tính là đã giải (số lần trả lời trái hồ sơ và gợi ý tính vào xếp hạng).
import { useEffect, useRef, useState } from 'react';
import type { Question } from '../lib/types';
import { useAuth, signInAnonymous } from '../lib/auth';
import { openExam, answerExam, type ExamView } from '../lib/exam';
import { Txt } from '../lib/text';
import { useBoard } from './context';

export function ExamPanel({ q, onSolved, onUseChoice }: { q: Question; onSolved: (misses: number, hints: number) => void; onUseChoice: () => void }) {
  const { c } = useBoard();
  const session = useAuth((s) => s.session);
  const [view, setView] = useState<ExamView | null>(null);
  const [msg, setMsg] = useState('');
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const logRef = useRef<HTMLOListElement>(null);
  const examiner = q.exam?.examiner || 'Kiểm sát viên';

  useEffect(() => {
    if (!session) return undefined;
    let live = true;
    setErr('');
    openExam(c.id, q.id).then((v) => { if (live) setView(v); }).catch((e) => { if (live) setErr((e as Error).message); });
    return () => { live = false; };
  }, [session?.user.id, c.id, q.id]);

  useEffect(() => { const el = logRef.current; if (el) el.scrollTop = el.scrollHeight; }, [view?.log.length, busy]);

  const send = async () => {
    const text = msg.trim();
    if (!text || busy || !view || view.done) return;
    setBusy(true); setErr('');
    setView({ ...view, log: [...view.log, { who: 'officer', text }] });
    setMsg('');
    try {
      const v = await answerExam(c.id, q.id, text);
      setView(v);
      if (v.done) onSolved(v.misses, v.hints);
    } catch (e) {
      setErr((e as Error).message);
      setView(view);
      setMsg(text);
    } finally { setBusy(false); }
  };

  const restart = async () => {
    setBusy(true); setErr('');
    try { setView(await openExam(c.id, q.id, true)); } catch (e) { setErr((e as Error).message); } finally { setBusy(false); }
  };

  if (!session) {
    return (
      <div className="exam">
        <p className="exam__note">Phần báo cáo do AI đóng vai kiểm sát viên, cần một tài khoản (ẩn danh cũng được) để lưu tiến độ.</p>
        <div className="q__actions">
          <button type="button" className="btn btn--primary btn--small" disabled={busy}
            onClick={async () => { setBusy(true); try { await signInAnonymous(); } catch (e) { setErr((e as Error).message); } finally { setBusy(false); } }}>
            Bắt đầu báo cáo (đăng nhập ẩn danh)
          </button>
          <button type="button" className="link-btn" onClick={onUseChoice}>Trả lời bằng trắc nghiệm</button>
        </div>
        {err && <p className="q__feedback is-wrong" role="alert">{err}</p>}
      </div>
    );
  }

  return (
    <div className="exam">
      <div className="exam__head">
        <strong>{view?.examiner || examiner}</strong>
        {view && <span className="exam__step">{view.done ? 'Đã xong' : `Câu ${view.point}/${view.total}`}</span>}
      </div>
      <ol className="exam__log" ref={logRef} aria-live="polite">
        {!view && !err && <li className="exam__line is-wait">Đang mở buổi báo cáo…</li>}
        {view?.log.map((l, i) => (
          <li key={i} className={`exam__line is-${l.who}`}>
            {l.who === 'examiner' && <span className="exam__who">{view.examiner}</span>}
            {l.who === 'officer' && <span className="exam__who">Điều tra viên</span>}
            <Txt>{l.text}</Txt>
          </li>
        ))}
        {busy && view && !view.done && <li className="exam__line is-wait">Kiểm sát viên đang đọc báo cáo…</li>}
      </ol>
      {view && !view.done && (
        <>
          <textarea className="exam__input" value={msg} rows={3} maxLength={800} placeholder="Trả lời bằng lời của bạn, có nêu căn cứ…"
            onChange={(e) => setMsg(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); void send(); } }} />
          <div className="q__actions">
            <button type="button" className="btn btn--primary btn--small" onClick={send} disabled={busy || !msg.trim()}>Trình bày</button>
            <button type="button" className="link-btn" onClick={onUseChoice}>Trả lời bằng trắc nghiệm</button>
          </div>
        </>
      )}
      {view?.done && (
        <div className="q__actions">
          <button type="button" className="btn btn--primary btn--small" onClick={() => onSolved(view.misses, view.hints)}>Ghi nhận kết luận</button>
          <button type="button" className="link-btn" onClick={restart} disabled={busy}>Báo cáo lại từ đầu</button>
        </div>
      )}
      {err && <p className="q__feedback is-wrong" role="alert">{err}</p>}
    </div>
  );
}
