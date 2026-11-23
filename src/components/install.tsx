// "Add to Home Screen" suggestion for phones and tablets.
//   Android / Chromium: the browser's own install dialog (beforeinstallprompt)
//   iPhone / iPad Safari: step-by-step via the Share button (iOS has no install API)
//   In-app browsers (Zalo, Facebook, Instagram…): ask to open in Safari / Chrome first
// Never shown when already installed, while playing a case, or for 14 days after "Để sau".
import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { create } from 'zustand';
import { SITE } from '../lib/config';

interface BeforeInstallPromptEvent extends Event { prompt: () => Promise<void>; userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }> }

const DISMISS_KEY = 'hsm:install-dismissed';
const SNOOZE_MS = 14 * 24 * 60 * 60 * 1000;

export type Platform = 'ios' | 'android' | 'inapp' | 'desktop';

export function detectPlatform(): Platform {
  const ua = navigator.userAgent;
  if (/FBAN|FBAV|Instagram|Zalo|Line\/|MicroMessenger|TikTok/i.test(ua)) return 'inapp';
  const iPadOS = navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1; // iPad reports itself as a Mac
  if (/iPad|iPhone|iPod/.test(ua) || iPadOS) return 'ios';
  if (/Android/i.test(ua)) return 'android';
  return 'desktop';
}

export const isStandalone = () =>
  window.matchMedia('(display-mode: standalone)').matches
  || window.matchMedia('(display-mode: fullscreen)').matches
  || (navigator as Navigator & { standalone?: boolean }).standalone === true;

const useInstall = create<{ deferred: BeforeInstallPromptEvent | null; open: boolean; installed: boolean }>(() => ({
  deferred: null, open: false, installed: false,
}));

// Register early: Chrome fires this once, shortly after load.
if (typeof window !== 'undefined') {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault(); // keep it for our own button
    useInstall.setState({ deferred: e as BeforeInstallPromptEvent });
  });
  window.addEventListener('appinstalled', () => useInstall.setState({ installed: true, open: false, deferred: null }));
}

const snoozed = () => {
  try { return Date.now() - Number(localStorage.getItem(DISMISS_KEY) || 0) < SNOOZE_MS; } catch { return false; }
};
const snooze = () => { try { localStorage.setItem(DISMISS_KEY, String(Date.now())); } catch { /* private mode */ } };

// For a menu item ("Cài ứng dụng"): true when it makes sense to offer it.
export function useCanInstall() {
  const deferred = useInstall((s) => s.deferred);
  const installed = useInstall((s) => s.installed);
  const [p] = useState(detectPlatform);
  return !installed && !isStandalone() && (Boolean(deferred) || p === 'ios' || p === 'inapp');
}
export const openInstall = () => useInstall.setState({ open: true });

function ShareIcon() {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" className="inst__ico">
      <path d="M12 3v12M7.5 7.5 12 3l4.5 4.5M5 11v8.5A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V11" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
function AddIcon() {
  return (
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" className="inst__ico">
      <rect x="3.5" y="3.5" width="17" height="17" rx="4" fill="none" stroke="currentColor" strokeWidth="1.8" />
      <path d="M12 8v8M8 12h8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

export function InstallPrompt() {
  const { pathname } = useLocation();
  const { deferred, open, installed } = useInstall();
  const [platform] = useState(detectPlatform);
  const playing = /^\/choi\/|^\/phong\/[^/]+\/choi/.test(pathname); // never interrupt a game

  // auto-suggest on phones/tablets after the visitor has looked around a little
  useEffect(() => {
    if (installed || isStandalone() || snoozed() || playing || platform === 'desktop') return undefined;
    if (platform === 'android' && !deferred) return undefined; // wait for the browser to allow installing
    let fired = false;
    const show = () => { if (!fired) { fired = true; useInstall.setState({ open: true }); } };
    const t = window.setTimeout(show, 12000);
    const onScroll = () => { if (window.scrollY > window.innerHeight * 1.2) show(); };
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => { window.clearTimeout(t); window.removeEventListener('scroll', onScroll); };
  }, [platform, deferred, installed, playing]);

  if (!open || installed || isStandalone() || playing) return null;
  const close = () => { snooze(); useInstall.setState({ open: false }); };
  const install = async () => {
    if (!deferred) return;
    await deferred.prompt();
    const { outcome } = await deferred.userChoice;
    useInstall.setState({ deferred: null, open: false });
    if (outcome === 'dismissed') snooze();
  };
  const isIPad = platform === 'ios' && (/iPad/.test(navigator.userAgent) || navigator.maxTouchPoints > 1 && navigator.platform === 'MacIntel');

  return (
    <div className="inst" role="dialog" aria-label="Cài ứng dụng lên màn hình chính">
      <div className="inst__card">
        <button type="button" className="inst__close" aria-label="Đóng" onClick={close}>×</button>
        <div className="inst__head">
          <img src="/icon-192.png" alt="" width={52} height={52} />
          <div>
            <strong>Cài {SITE.name} lên màn hình chính</strong>
            <span>Mở như một ứng dụng: toàn màn hình, vào nhanh, chơi được cả khi mạng yếu.</span>
          </div>
        </div>

        {platform === 'inapp' ? (
          <p className="inst__text">Bạn đang mở trang trong ứng dụng khác. Bấm <b>⋯</b> rồi chọn <b>Mở bằng trình duyệt</b> (Safari hoặc Chrome) để cài.</p>
        ) : platform === 'ios' ? (
          <ol className="inst__steps">
            <li><span className="inst__n">1</span>Bấm nút <b>Chia sẻ</b> <ShareIcon /> {isIPad ? 'ở góc trên bên phải thanh địa chỉ' : 'ở thanh dưới cùng của Safari'}.</li>
            <li><span className="inst__n">2</span>Kéo xuống, chọn <b>Thêm vào MH chính</b> <AddIcon />.</li>
            <li><span className="inst__n">3</span>Bấm <b>Thêm</b>. Mở trò chơi từ biểu tượng mới trên màn hình chính.</li>
          </ol>
        ) : deferred ? (
          <div className="inst__actions">
            <button type="button" className="btn btn--primary" onClick={install}>Cài đặt</button>
            <button type="button" className="btn btn--ghost" onClick={close}>Để sau</button>
          </div>
        ) : (
          <p className="inst__text">Mở menu <b>⋮</b> của trình duyệt rồi chọn <b>Cài đặt ứng dụng</b> hoặc <b>Thêm vào màn hình chính</b>.</p>
        )}
        {(platform === 'ios' || platform === 'inapp' || !deferred) && (
          <button type="button" className="link-btn inst__later" onClick={close}>Để sau</button>
        )}
      </div>
    </div>
  );
}
