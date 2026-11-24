import { Link } from 'react-router-dom';
import { SITE } from '../lib/config';
import { caseBase, caseNo, caseKind } from '../lib/data';
import type { CaseSummary } from '../lib/types';
import { AccountChip } from './auth';
import { useCanInstall, openInstall } from './install';

export function Brand() {
  return <Link className="brand" to="/"><span className="brand__mark" aria-hidden="true" /><span>{SITE.name}</span></Link>;
}

export function Nav({ cta = { to: '/#catalog', label: 'Chơi ngay' } }: { cta?: { to: string; label: string } }) {
  return (
    <header className="nav">
      <div className="wrap nav__inner">
        <Brand />
        <nav className="nav__links" aria-label="Điều hướng chính">
          <Link to="/#catalog">Kho hồ sơ</Link>
          <Link to="/#how">Cách chơi</Link>
          <Link to="/#faq">Hỏi đáp</Link>
          <Link to="/tham-gia">Tham gia phòng</Link>
        </nav>
        <AccountChip />
        <Link className="btn btn--primary btn--small" to={cta.to}>{cta.label}</Link>
      </div>
    </header>
  );
}

export function Footer() {
  const canInstall = useCanInstall();
  return (
    <footer className="footer">
      <div className="wrap footer__inner">
        <Brand />
        <p>Mọi nhân vật và sự kiện trong các hồ sơ đều là hư cấu.</p>
        {canInstall && <button type="button" className="link-btn" onClick={openInstall}>Cài ứng dụng lên màn hình chính</button>}
        <p>© {new Date().getFullYear()} {SITE.name}</p>
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
              {entry.draft && <span className="badge badge--draft" title="Hồ sơ chơi được nhưng hình ảnh tư liệu đang được bổ sung">Chưa hoàn thiện</span>}
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
