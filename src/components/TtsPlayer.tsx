// Floating TTS player: shows current status, progress bar, pause/resume/stop.
import { useTts, pause, resume, stop, type TtsStatus } from '../lib/tts';
import { Icon } from '../board/icons';

function statusLabel(s: TtsStatus, idx: number, total: number): string {
  switch (s) {
    case 'loading': return 'Đang tải giọng đọc…';
    case 'playing': return total > 1 ? `Đang đọc (${idx + 1}/${total})` : 'Đang đọc…';
    case 'paused': return 'Đã tạm dừng';
    case 'error': return 'Lỗi';
    default: return '';
  }
}

export function TtsPlayer() {
  const { status, chunkIndex, chunkCount, error, activeId } = useTts();
  if (status === 'idle' || !activeId) return null;

  const progress = chunkCount > 0 ? ((chunkIndex + (status === 'playing' ? 0.5 : 0)) / chunkCount) * 100 : 0;

  return (
    <div className={`tts-player tts-player--${status}`} role="status" data-ui>
      <div className="tts-player__bar">
        <span className="tts-player__icon">
          {status === 'loading' ? <span className="tts-player__spinner" /> : <Icon name="speaker" />}
        </span>
        <span className="tts-player__label">{error || statusLabel(status, chunkIndex, chunkCount)}</span>
        <span className="tts-player__actions">
          {(status === 'playing' || status === 'paused') && (
            <button type="button" className="icon-btn icon-btn--sm" aria-label={status === 'playing' ? 'Tạm dừng' : 'Tiếp tục'} onClick={status === 'playing' ? pause : resume}>
              <Icon name={status === 'playing' ? 'pause' : 'play'} />
            </button>
          )}
          <button type="button" className="icon-btn icon-btn--sm" aria-label="Dừng đọc" onClick={stop}>
            <Icon name="close" />
          </button>
        </span>
      </div>
      {chunkCount > 1 && (
        <div className="tts-player__progress">
          <div className="tts-player__fill" style={{ width: `${progress}%` }} />
        </div>
      )}
    </div>
  );
}
