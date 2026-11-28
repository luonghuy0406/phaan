// Suspect ID cards: the gallery (intro, "Nghi phạm" dialog) and the card picker used by choice questions with `cards`.
import type { CasePerson } from '../lib/types';
import { useBoard } from './context';
import { caseBase } from '../lib/data';
import { Txt } from '../lib/text';
import { Icon } from './icons';

export function SuspectCard({ p, no, tag, picked, compact = false }: { p: CasePerson; no?: number; tag?: string; picked?: boolean; compact?: boolean }) {
  const { c } = useBoard();
  return (
    <span className={`sus${picked ? ' is-on' : ''}${compact ? ' sus--compact' : ''}`}>
      <span className="sus__photo">
        {p.image ? <img src={caseBase(c.id) + p.image} alt={`Ảnh thẻ ${p.name}`} loading="lazy" draggable={false} /> : <span className="sus__blank" aria-hidden="true" />}
        {(tag || no != null) && <span className={`sus__no${tag ? ' sus__no--tag' : ''}`}>{tag || String(no).padStart(2, '0')}</span>}
      </span>
      <span className="sus__name">{p.alias || p.name}</span>
      <span className="sus__role">{p.role}{p.age ? ` · ${p.age} tuổi` : ''}</span>
    </span>
  );
}

/** Hồ sơ nhân thân: one card per person, the reason for suspicion inside the card, and a clear "Thẩm vấn" action. */
export function SuspectGallery({ onInterrogate }: { withReasons?: boolean; onInterrogate?: (id: string) => void }) {
  const { c } = useBoard();
  if (!c.suspects?.length) return null;
  const base = caseBase(c.id);
  const photo = (p: CasePerson, tag: string, victim = false) => (
    <div className="dossier__photo">
      {p.image ? <img src={base + p.image} alt={`Ảnh thẻ ${p.name}`} loading="lazy" draggable={false} /> : <span className="sus__blank" aria-hidden="true" />}
      <span className={`dossier__tag${victim ? ' dossier__tag--victim' : ''}`}>{tag}</span>
    </div>
  );
  const meta = (p: CasePerson) => [p.alias ? p.name : '', p.age ? `${p.age} tuổi` : '', p.role].filter(Boolean).join(' · ');
  return (
    <div className="dossier-grid">
      {c.victim && (
        <article className="dossier dossier--victim">
          {photo(c.victim, 'Nạn nhân', true)}
          <div className="dossier__body">
            <h3>{c.victim.alias || c.victim.name}</h3>
            <p className="dossier__meta">{meta(c.victim)}</p>
            {c.victim.note && <div className="dossier__why"><b>Hồ sơ</b><Txt>{c.victim.note}</Txt></div>}
          </div>
        </article>
      )}
      {c.suspects.map((p, i) => (
        <article key={p.id} className="dossier">
          {photo(p, `Nghi phạm ${String(i + 1).padStart(2, '0')}`)}
          <div className="dossier__body">
            <h3>{p.alias || p.name}</h3>
            <p className="dossier__meta">{meta(p)}</p>
            {p.suspicion && <div className="dossier__why"><b>Lý do nghi vấn</b><Txt>{p.suspicion}</Txt></div>}
          </div>
          {onInterrogate && (
            <button type="button" className="dossier__ask" onClick={() => onInterrogate(p.id)}>
              <Icon name="chat" /><span>Thẩm vấn</span>
            </button>
          )}
        </article>
      ))}
    </div>
  );
}
