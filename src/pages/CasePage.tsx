import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import { supabaseReady } from '../lib/supabase';
import { createRoom } from '../multiplayer/room';
import { CaseCard, Cover, Difficulty, Footer, Nav } from '../components/site';
import { caseNo, loadCase, loadCatalog, useAsync } from '../lib/data';
import { Paras } from '../lib/text';
import { SITE } from '../lib/config';
import { typeLabel } from '../board/papers';
import type { CaseData, CaseSummary } from '../lib/types';

async function loadBoth(id: string): Promise<{ entry?: CaseSummary; full?: CaseData; catalog: CaseSummary[] }> {
  const catalog = await loadCatalog().catch(() => [] as CaseSummary[]);
  const full = await loadCase(id).catch(() => undefined);
  return { entry: catalog.find((c) => c.id === id), full, catalog };
}

export default function CasePage() {
  const { id = '' } = useParams();
  const { data, loading } = useAsync(() => loadBoth(id), [id]);
  const c: (CaseSummary & Partial<CaseData>) | undefined = data?.full ? { ...data.entry, ...data.full } : data?.entry;
  useEffect(() => { if (c) document.title = `${c.title} – ${SITE.name}`; }, [c]);
  useEffect(() => { window.scrollTo(0, 0); }, [id]);

  const open = c?.status === 'available' && Boolean(data?.full);
  const navigate = useNavigate();
  const session = useAuth((s) => s.session);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState('');
  const playTogether = async () => {
    if (!session) { navigate(`/dang-nhap?next=${encodeURIComponent(`/ho-so/${id}`)}`); return; }
    setBusy(true); setErr('');
    try { const r = await createRoom(id); navigate(`/phong/${r.id}`); } catch (e) { setErr((e as Error).message); setBusy(false); }
  };
  const counts: Record<string, number> = {};
  (data?.full?.documents || []).forEach((d) => { counts[d.type] = (counts[d.type] || 0) + 1; });
  const stages = new Set((data?.full?.documents || []).map((d) => d.stage ?? 1)).size;
  const others = (data?.catalog || []).filter((x) => x.id !== id).slice(0, 4);

  return (
    <>
      <Nav cta={{ to: '/#catalog', label: 'Kho hồ sơ' }} />
      <main>
        <div className="wrap crumbs"><Link to="/#catalog">Kho hồ sơ</Link> / <span>{c?.title || '…'}</span></div>
        <section className="case-hero">
          <div className="wrap case-hero__inner">
            {loading ? <p>Đang tải hồ sơ…</p> : !c ? (
              <div>
                <h1>Không tìm thấy hồ sơ</h1>
                <p className="case-synopsis">Hồ sơ này không tồn tại hoặc đã bị gỡ.</p>
                <Link className="btn btn--primary" to="/#catalog">Về kho hồ sơ</Link>
              </div>
            ) : (
              <>
                <div className="case-hero__cover"><Cover entry={c} /></div>
                <div>
                  <p className="eyebrow">{caseNo(c)} · {open ? 'Đang mở' : 'Sắp ra mắt'}</p>
                  <h1>{c.title}</h1>
                  {c.subtitle && <p className="case-hero__sub">{c.subtitle}</p>}
                  <div className="case-synopsis"><Paras list={c.synopsis || (c.tagline ? [c.tagline] : [])} /></div>
                  <dl className="case-facts">
                    <div><dt>Độ khó</dt><dd><Difficulty level={c.difficulty} /></dd></div>
                    <div><dt>Người chơi</dt><dd>{c.players || '1–6'}</dd></div>
                    <div><dt>Thời lượng</dt><dd>{c.duration || '—'}</dd></div>
                    <div><dt>Bối cảnh</dt><dd>{c.setting || '—'}</dd></div>
                    {c.era && <div><dt>Thời điểm</dt><dd>{c.era}</dd></div>}
                  </dl>
                  <div className="case-actions">
                    {open ? (
                      <>
                        <Link className="btn btn--primary" to={`/choi/${c.id}`}>Chơi một mình</Link>
                        {supabaseReady && <button type="button" className="btn btn--primary btn--alt" disabled={busy} onClick={playTogether}>{busy ? 'Đang tạo phòng…' : 'Chơi nhóm'}</button>}
                        {supabaseReady && <Link className="btn btn--ghost" to="/tham-gia">Có mã phòng?</Link>}
                      </>
                    ) : <span className="btn btn--primary" aria-disabled="true">Sắp ra mắt</span>}
                  </div>
                  {open && supabaseReady && <p className="case-hint">Chơi nhóm: bạn làm chủ phòng, mời đồng đội bằng mã 6 số hoặc mã QR. Mọi người cùng xem kết luận, ghim bằng chứng và sổ tay nhóm theo thời gian thực.{session ? '' : ' Cần đăng nhập.'}</p>}
                  {err && <p className="case-warning">{err}</p>}
                  {data?.full && (
                    <div className="case-contents">
                      <h2>Trong hồ sơ có</h2>
                      <ul>
                        {Object.entries(counts).map(([t, n]) => <li key={t}><b>{n}</b>{typeLabel(t)}</li>)}
                        <li><b>{stages}</b>trọng điểm điều tra</li>
                        <li><b>{data.full.questions.length}</b>câu hỏi kết luận</li>
                      </ul>
                    </div>
                  )}
                  {c.contentWarning && <p className="case-warning">{c.contentWarning}</p>}
                </div>
              </>
            )}
          </div>
        </section>
        <section className="more">
          <div className="wrap">
            <h2>Hồ sơ khác</h2>
            <div className="catalog">
              {others.length ? others.map((x) => <CaseCard key={x.id} entry={x} compact />) : <p className="catalog__empty">Các hồ sơ mới đang được biên soạn.</p>}
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
