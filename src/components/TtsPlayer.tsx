// Floating TTS player: asks before downloading the on-device voice, shows download progress,
// then playback status with pause / resume / stop.
import { useEffect, useState } from 'react';
import { useTts, pause, resume, stop, acceptTtsDownload, declineTtsDownload, MODEL_MB, type TtsStatus } from '../lib/tts';
import { storageInfo } from '../lib/supertonic/client';
import { Icon } from '../board/icons';

function statusLabel(s: TtsStatus, idx: number, total: number): string {
  switch (s) {
    case 'downloading': return 'Đang tải giọng đọc…';
    case 'loading': return 'Đang chuẩn bị giọng đọc…';
    case 'playing': return total > 1 ? `Đang đọc (${idx + 1}/${total})` : 'Đang đọc…';
    case 'paused': return 'Đã tạm dừng';
    case 'error': return 'Lỗi';
    default: return '';
  }
}

const mb = (bytes: number) => `${Math.round(bytes / 1e6)} MB`;

function Consent() {
  const [warn, setWarn] = useState<string[]>([]);
  useEffect(() => {
    const notes: string[] = [];
    const conn = (navigator as Navigator & { connection?: { saveData?: boolean; type?: string; effectiveType?: string } }).connection;
    if (conn?.saveData) notes.push('Máy đang bật chế độ tiết kiệm dữ liệu.');
    if (conn?.type === 'cellular') notes.push('Bạn đang dùng dữ liệu di động.');
    void storageInfo().then(({ free }) => {
      if (free != null && free < MODEL_MB * 1.3e6) notes.push(`Bộ nhớ trình duyệt còn khoảng ${mb(free)}, có thể không đủ.`);
      setWarn([...notes]);
    });
    setWarn([...notes]);
  }, []);
  return (
    <div className="tts-consent" role="dialog" aria-modal="false" aria-labelledby="tts-consent-title" data-ui>
      <div className="tts-consent__head">
        <Icon name="speaker" />
        <strong id="tts-consent-title">Nghe đọc hồ sơ bằng giọng AI?</strong>
      </div>
      <p>
        Để đọc tiếng Việt ngay trên máy (không gửi nội dung đi đâu), cần tải mô hình giọng đọc
        khoảng <b>{MODEL_MB} MB</b> về thiết bị. Chỉ tải <b>một lần</b>; sau đó đọc được cả khi không có mạng.
      </p>
      <p className="tts-consent__muted">Nên dùng Wi-Fi. Có thể xoá giọng đọc bất kỳ lúc nào trong Cài đặt.</p>
      {warn.map((w) => <p key={w} className="tts-consent__warn">{w}</p>)}
      <div className="tts-consent__actions">
        <button type="button" className="btn btn--primary btn--small" onClick={acceptTtsDownload}>Tải và đọc</button>
        <button type="button" className="btn btn--ghost btn--small" onClick={declineTtsDownload}>Để sau</button>
      </div>
    </div>
  );
}

export function TtsPlayer() {
  const { status, chunkIndex, chunkCount, error, activeId, download } = useTts();
  if (status === 'consent') return <Consent />;
  if (status === 'idle' || !activeId) return null;

  const downloading = status === 'downloading' && download?.phase === 'download';
  const pct = download ? Math.min(100, (download.loaded / Math.max(1, download.total)) * 100) : 0;
  const progress = downloading || status === 'loading'
    ? pct
    : chunkCount > 0 ? ((chunkIndex + (status === 'playing' ? 0.5 : 0)) / chunkCount) * 100 : 0;
  const label = error
    || (downloading && download ? `Đang tải giọng đọc ${Math.floor(pct)}% (${mb(download.loaded)}/${mb(download.total)})` : statusLabel(status, chunkIndex, chunkCount));

  return (
    <div className={`tts-player tts-player--${status}`} role="status" data-ui>
      <div className="tts-player__bar">
        <span className="tts-player__icon">
          {status === 'loading' || status === 'downloading' ? <span className="tts-player__spinner" /> : <Icon name="speaker" />}
        </span>
        <span className="tts-player__label">{label}</span>
        <span className="tts-player__actions">
          {(status === 'playing' || status === 'paused') && (
            <button type="button" className="icon-btn icon-btn--sm" aria-label={status === 'playing' ? 'Tạm dừng' : 'Tiếp tục'} onClick={status === 'playing' ? pause : resume}>
              <Icon name={status === 'playing' ? 'pause' : 'play'} />
            </button>
          )}
          <button type="button" className="icon-btn icon-btn--sm" aria-label={status === 'downloading' ? 'Dừng tải' : 'Dừng đọc'} onClick={stop}>
            <Icon name="close" />
          </button>
        </span>
      </div>
      {(chunkCount > 1 || status === 'downloading' || status === 'loading') && (
        <div className="tts-player__progress">
          <div className="tts-player__fill" style={{ width: `${progress}%` }} />
        </div>
      )}
      {status === 'downloading' && <p className="tts-player__note">Chỉ tải một lần. Có thể tiếp tục chơi trong lúc chờ.</p>}
    </div>
  );
}
