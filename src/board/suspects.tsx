// Suspect ID cards: the gallery (intro, "Nghi phạm" dialog) and the card picker used by choice questions with `cards`.
import type { CasePerson } from '../lib/types';
import { useBoard } from './context';
import { caseBase } from '../lib/data';
import { Txt } from '../lib/text';

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

/** Victim + suspects with why each is suspected (surface reasons only, never the solution). */
export function SuspectGallery({ withReasons = true }: { withReasons?: boolean }) {
  const { c } = useBoard();
  if (!c.suspects?.length) return null;
  return (
    <div className="sus-gallery">
      <div className="sus-grid">
        {/* the victim sits first, same size as the suspects */}
        {c.victim && (
          <div className="sus-item sus-item--victim">
            <SuspectCard p={c.victim} tag="Nạn nhân" />
            {withReasons && c.victim.note && <p className="sus-item__why"><Txt>{c.victim.note}</Txt></p>}
          </div>
        )}
        {c.suspects.map((p, i) => (
          <div key={p.id} className="sus-item">
            <SuspectCard p={p} no={i + 1} />
            {withReasons && p.suspicion && <p className="sus-item__why"><Txt>{p.suspicion}</Txt></p>}
          </div>
        ))}
      </div>
    </div>
  );
}
