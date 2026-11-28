import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { SITE } from '../lib/config';
import { caseBase, caseNo, caseKind } from '../lib/data';
import type { CaseSummary } from '../lib/types';
import { AccountChip } from './auth';
import { useCanInstall, openInstall } from './install';

export function scrollToSection(id: string): boolean {
  const el = document.getElementById(id);
  if (!el) return false;
  const anchor = el.parentElement?.classList.contains('pin-spacer') ? el.parentElement : el;
  const navH = document.querySelector<HTMLElement>('.nav')?.offsetHeight ?? 65;
  const isPinnedHow = id === 'how' && anchor !== el;
  const pad = isPinnedHow ? 0 : navH + 10;
  const top = Math.max(0, anchor.getBoundingClientRect().top + window.scrollY - pad);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.scrollTo({ top, behavior: reduced ? 'auto' : 'smooth' });
  return true;
}

export function Brand() {
  return (
    <Link
      className="brand"
      to="/#top"
      onClick={(e) => {
        if (window.location.pathname === '/') {
          e.preventDefault();
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }}
    >
      <span className="brand__mark" aria-hidden="true">
        <svg viewBox="0 0 20 20" fill="none">
          <path d="M2.5 4.5h6l1.8 2H17.5v9.5h-15V4.5z" stroke="currentColor" strokeWidth="1.5" />
          <circle cx="10" cy="11.2" r="2.2" fill="var(--red-2)" />
        </svg>
      </span>
      <span className="brand__text">
        <b>{SITE.name}</b>
        <small>Kho lưu trữ vụ án</small>
      </span>
    </Link>
  );
}

export function Nav({ cta = { to: '/#catalog', label: 'Mở kho hồ sơ' } }: { cta?: { to: string; label: string } }) {
  const { pathname, hash } = useLocation();
  const [scrolled, setScrolled] = useState(false);
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  const handleHashLink = (to: string) => (e: React.MouseEvent) => {
    const idx = to.indexOf('#');
    if (idx < 0 || pathname !== '/') return;
    const targetHash = to.slice(idx);
    if (hash === targetHash) {
      e.preventDefault();
      scrollToSection(targetHash.slice(1));
    }
  };
  return (
    <header className={`nav${scrolled ? ' is-scrolled' : ''}`}>
      <div className="wrap nav__inner">
        <Brand />
        <nav className="nav__links" aria-label="Điều hướng chính">
          <Link to="/#how" onClick={handleHashLink('/#how')}>Quy trình</Link>
          <Link to="/#inside" onClick={handleHashLink('/#inside')}>Bàn điều tra</Link>
          <Link to="/#catalog" onClick={handleHashLink('/#catalog')}>Kho hồ sơ</Link>
          <Link to="/#faq" onClick={handleHashLink('/#faq')}>Hỏi đáp</Link>
          <Link to="/tham-gia">Phòng 6 số</Link>
        </nav>
        <AccountChip />
        <Link className="btn btn--primary btn--small" to={cta.to} onClick={handleHashLink(cta.to)}>{cta.label}</Link>
      </div>
    </header>
  );
}

export function Footer() {
  const canInstall = useCanInstall();
  const { pathname, hash } = useLocation();
  const goHash = (to: string) => (e: React.MouseEvent) => {
    const idx = to.indexOf('#');
    if (idx >= 0 && pathname === '/' && hash === to.slice(idx)) {
      e.preventDefault();
      scrollToSection(to.slice(idx + 1));
    }
  };
  return (
    <footer className="footer">
      <div className="wrap">
        <div className="foot-cols">
          <div className="foot-brand">
            <Brand />
            <p className="foot-note">{SITE.tagline}. Trải nghiệm bàn điều tra trực quan trên trình duyệt, viết tay bằng Apple Pencil và thẩm vấn nghi phạm AI.</p>
            {canInstall && (
              <button type="button" className="link-btn" onClick={openInstall}>Cài ứng dụng lên màn hình chính →</button>
            )}
          </div>
          <div>
            <h4>Điều hướng</h4>
            <Link to="/#how" onClick={goHash('/#how')}>Quy trình 4 bước</Link>
            <Link to="/#inside" onClick={goHash('/#inside')}>Bàn điều tra mẫu</Link>
            <Link to="/#catalog" onClick={goHash('/#catalog')}>Kho hồ sơ</Link>
            <Link to="/#faq" onClick={goHash('/#faq')}>Câu hỏi thường gặp</Link>
          </div>
          <div>
            <h4>Hồ sơ nổi bật</h4>
            <Link to="/ho-so/demo-01">00 · Ngõ Gác Chuông</Link>
            <Link to="/ho-so/con-nuoc-ram-thang-gieng">01 · Con nước Rằm tháng Giêng</Link>
            <Link to="/ho-so/chuyen-tau-dem-muong-man">05 · Chuyến tàu đêm Mường Mán</Link>
            <Link to="/ho-so/vet-muc-lang-dong-ho">12 · Vết mực làng Đông Hồ</Link>
          </div>
          <div>
            <h4>Chế độ chơi</h4>
            <Link to="/#featured" onClick={goHash('/#featured')}>Chơi một mình</Link>
            <Link to="/tham-gia">Nhập mã phòng 6 số</Link>
            <Link to="/dang-nhap">Đồng bộ tiến độ cloud</Link>
          </div>
        </div>
        <div className="foot-fine">
          <span>© {new Date().getFullYear()} {SITE.name} · Phiên bản web &amp; iPad PWA</span>
          <span>Nhân vật, địa danh và cơ quan trong trò chơi hư cấu đều do tác giả xây dựng.</span>
        </div>
      </div>
    </footer>
  );
}

export function Difficulty({ level, max = 5 }: { level?: number; max?: number }) {
  const n = Math.max(0, Math.min(max, Number(level) || 0));
  return (
    <span className="diff" role="img" aria-label={`Độ khó ${n}/${max}`}>
      {Array.from({ length: max }, (_, i) => <i key={i} className={i < n ? 'on' : ''} />)}
    </span>
  );
}

export function Cover({ entry }: { entry: CaseSummary }) {
  if (entry.cover) {
    return (
      <div className="folder folder--image">
        <img src={caseBase(entry.id) + entry.cover} alt={`Bìa ${entry.title}`} loading="lazy" />
        <span className="folder__overlay">
          <span className="folder__no">{caseNo(entry)}</span>
          <span className="folder__title">{entry.title}</span>
        </span>
      </div>
    );
  }
  const soon = entry.status !== 'available';
  return (
    <div className="folder">
      <span className="folder__no">{caseNo(entry)}</span>
      <span className="stamp">{soon ? 'Đang lập' : 'Mật'}</span>
      <span className="folder__title">{entry.title}</span>
      {entry.tagline && <span className="folder__tag">{entry.tagline}</span>}
      <span className="folder__label">{entry.setting || 'Hồ sơ hình sự'}</span>
    </div>
  );
}

export function CaseCard({ entry, compact = false }: { entry: CaseSummary; compact?: boolean }) {
  const open = entry.status === 'available';
  const real = caseKind(entry) === 'true-crime';
  const tags = (entry.tags || []).filter((t) => !/vụ án có thật/i.test(t));
  return (
    <Link className={`case-card${open ? '' : ' is-soon'}${real ? ' case-card--real' : ''}`} to={`/ho-so/${entry.id}`}>
      <div className="case-card__cover">
        <Cover entry={entry} />
        {real && <span className="kind-ribbon">Vụ án có thật</span>}
      </div>
      <div className="case-card__body">
        <div className="case-card__top">
          <span className="case-card__no">{caseNo(entry)}</span>
          {!compact && (
            <span className="case-card__badges">
              {open && entry.draft && <span className="badge badge--draft" title="Hồ sơ chơi được nhưng hình ảnh tư liệu đang được bổ sung">Chưa hoàn thiện</span>}
              <span className={`badge${open ? '' : ' badge--soon'}`}>{open ? 'Đang mở' : 'Sắp ra mắt'}</span>
            </span>
          )}
        </div>
        <h3>{entry.title}</h3>
        {!compact && entry.tagline && <p>{entry.tagline}</p>}
        {!compact && (
          <dl className="case-card__meta">
            <div><dt>Độ khó</dt><dd><Difficulty level={entry.difficulty} /></dd></div>
            <div><dt>Người chơi</dt><dd>{entry.players || '1–6'}</dd></div>
            <div><dt>Thời lượng</dt><dd>{entry.duration || '—'}</dd></div>
          </dl>
        )}
        {!compact && !!tags.length && <ul className="case-card__tags">{tags.slice(0, 3).map((t) => <li key={t}>{t}</li>)}</ul>}
      </div>
    </Link>
  );
}

const FEATURE_SHORT: Record<string, string> = { ai: 'Thẩm vấn AI', exam: 'Kiểm sát AI', voice: 'Giọng đọc', accomplice: 'Đồng phạm', starter: 'Nhập môn' };
const DIFF_WORD = ['', 'Rất dễ', 'Dễ', 'Vừa', 'Khó', 'Rất khó'];

/** Archival folder card for an available case on the home shelf. */
export function ReleasedCard({ entry, lead = false }: { entry: CaseSummary; lead?: boolean }) {
  const real = caseKind(entry) === 'true-crime';
  const img = entry.art || entry.cover;
  const feats = (entry.features || []).filter((f) => FEATURE_SHORT[f]);
  const starter = feats.includes('starter');
  const modList = feats.filter((f) => f !== 'starter');
  const place = entry.setting ? entry.setting.replace(/\s*\(hư cấu\)/gi, '') : '';
  return (
    <Link className={`file${lead ? ' file--lead' : ''}${starter ? ' file--starter' : ''}${real ? ' file--real' : ''}`} to={`/ho-so/${entry.id}`}>
      <div className="file__tab">
        <span className="file__tab-no">{caseNo(entry)}</span>
        <span className="file__tab-tag">
          {starter ? 'Nhập môn' : real ? 'Vụ án có thật' : 'Đang mở'}
        </span>
      </div>
      <div className="file__art">
        {img ? <img src={caseBase(entry.id) + img} alt="" loading="lazy" style={entry.artPos ? { objectPosition: entry.artPos } : undefined} /> : <span className="file__blank" />}
        <div className="file__cap">
          {entry.tagline && <p>{entry.tagline}</p>}
          <span>Mở tệp hồ sơ →</span>
        </div>
      </div>
      <div className="file__meta">
        {place && <span className="file__place">{place}</span>}
        <h3>{entry.title}</h3>
        {!!modList.length && (
          <ul className="file__feats" aria-label="Tính năng hồ sơ">
            {modList.slice(0, 3).map((f) => <li key={f}>{FEATURE_SHORT[f]}</li>)}
          </ul>
        )}
        <dl className="file__specs">
          <div><dt>Độ khó</dt><dd><Difficulty level={entry.difficulty} /> <span>{DIFF_WORD[entry.difficulty || 0]}</span></dd></div>
          <div><dt>Người chơi</dt><dd>{entry.players || '1–6'}</dd></div>
          <div><dt>Thời lượng</dt><dd>{entry.duration || '—'}</dd></div>
        </dl>
      </div>
    </Link>
  );
}

/** Small locked card for a case still being written. */
export function SoonCard({ entry }: { entry: CaseSummary }) {
  const real = caseKind(entry) === 'true-crime';
  return (
    <Link className={`soon-card${real ? ' soon-card--real' : ''}`} to={`/ho-so/${entry.id}`} aria-label={`${entry.title}: sắp ra mắt`}>
      <span className="soon-card__art">
        {entry.cover && <img src={caseBase(entry.id) + entry.cover} alt="" loading="lazy" />}
        <svg className="soon-card__lock" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2" /><path d="M8 11V8a4 4 0 0 1 8 0v3" /></svg>
      </span>
      <span className="soon-card__body">
        <span className="soon-card__no">{caseNo(entry)}{real ? ' · Có thật' : ''}</span>
        <span className="soon-card__title">{entry.title}</span>
        <span className="soon-card__meta"><Difficulty level={entry.difficulty} />{entry.duration ? <span>{entry.duration}</span> : null}</span>
      </span>
    </Link>
  );
}
