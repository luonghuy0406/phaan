import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { Difficulty, Footer, Nav, ReleasedCard, SoonCard, scrollToSection } from '../components/site';
import { ContinueStrip } from '../components/progress';
import { loadCatalog, useAsync, caseKind, caseBase, caseNo } from '../lib/data';
import type { CaseKind, CaseSummary } from '../lib/types';
import { SITE } from '../lib/config';
import '../styles/home.css';

gsap.registerPlugin(ScrollTrigger, useGSAP);

type Filter = 'all' | CaseKind;
type DeskLayer = 'all' | 'paper' | 'ai' | 'board';

interface DeskCardMeta {
  id: string;
  layer: Exclude<DeskLayer, 'all'>;
  label: string;
  note: string;
}

const FILTERS: { id: Filter; label: string }[] = [
  { id: 'all', label: 'Tất cả' },
  { id: 'fiction', label: 'Hư cấu' },
  { id: 'true-crime', label: 'Vụ án có thật' },
];

const FLOW_STEPS = [
  {
    no: '01',
    title: 'Mở tệp hồ sơ',
    text: 'Biên bản khám nghiệm, sơ đồ nhà, ảnh hiện trường và lời khai bản gốc tự động mở ra theo từng vòng niêm phong.',
    tag: 'Tài liệu nền giấy',
  },
  {
    no: '02',
    title: 'Khoanh & nối dây',
    text: 'Khoanh chi tiết khả nghi trực tiếp bằng Apple Pencil, ghim thẻ và kéo dây đỏ xuyên suốt các chứng cứ khớp nhau.',
    tag: 'Bàn vô hạn & iPad',
  },
  {
    no: '03',
    title: 'Thẩm vấn AI',
    text: 'Chất vấn nghi phạm theo thời gian thực hoặc bật giọng đọc ba miền Bắc – Trung – Nam để nghe nguyên văn lời khai.',
    tag: 'Phản xạ có chứng cứ',
  },
  {
    no: '04',
    title: 'Trình Kiểm sát',
    text: 'Chọn dòng khai man, đưa ra tang vật chốt hạ và đối đáp trước Kiểm sát viên AI để chính thức khép lại hồ sơ.',
    tag: 'Kết luận điều tra',
  },
] as const;

const DESK_LAYERS: { id: DeskLayer; label: string; hint: string }[] = [
  { id: 'all', label: 'Toàn bàn điều tra', hint: 'Nhấp vào từng món trên bàn để xem công cụ tương ứng khi phá án.' },
  { id: 'paper', label: 'Bút lục & Apple Pencil', hint: 'Viết tay thẳng lên biên bản, tô vàng chi tiết ẩn và xoay sơ đồ hiện trường bất kỳ góc nào.' },
  { id: 'ai', label: 'Thẩm vấn AI & Giọng đọc', hint: 'Đưa chứng cứ ra trước mặt nghi phạm AI để ép đổi lời khai; hỗ trợ đọc lời khai ba miền ngay trên máy.' },
  { id: 'board', label: 'Nối dây đỏ & Kết án', hint: 'Ghim đầu mối, kéo dây đỏ nối hai tờ tài liệu và ghim dòng nói dối trình Kiểm sát viên.' },
];

const DESK_ITEMS: Record<string, DeskCardMeta> = {
  report: {
    id: 'report',
    layer: 'paper',
    label: 'Biên bản khám nghiệm & Bút đỏ Apple Pencil',
    note: 'Nét mực đỏ khoanh tay trực tiếp bằng Apple Pencil giúp đánh dấu giờ giấc mâu thuẫn trên biên bản.',
  },
  blueprint: {
    id: 'blueprint',
    layer: 'paper',
    label: 'Sơ đồ hiện trường ngõ Gác Chuông',
    note: 'Zoom sâu để kiểm tra vị trí cửa sổ vỡ, hướng gió, khóa trong và đường thoát thân trên mặt bằng thật.',
  },
  interrogation: {
    id: 'interrogation',
    layer: 'ai',
    label: 'Bảng thẩm vấn AI & Giọng đọc 3 miền',
    note: 'Hỏi nghi phạm bất kỳ câu nào hoặc nhấn phát giọng đọc Bắc – Trung – Nam để cảm nhận sắc thái nhân vật.',
  },
  suspects: {
    id: 'suspects',
    layer: 'ai',
    label: 'Hồ sơ nhân thân & Nạn nhân',
    note: 'Đối chiếu danh sách người có mặt tại hiện trường và theo dõi thái độ thay đổi qua từng vòng điều tra.',
  },
  scene: {
    id: 'scene',
    layer: 'board',
    label: 'Ảnh chụp hiện trường & Dây đỏ suy luận',
    note: 'Kéo dây đỏ từ ảnh chụp hiện trường nối thẳng tới tang vật để không bị lạc giữa hàng chục tờ hồ sơ.',
  },
  evidence: {
    id: 'evidence',
    layer: 'board',
    label: 'Tang vật & Phiếu trình Kiểm sát viên',
    note: 'Chỉ rõ chứng cứ vật chất kết hợp lập luận logic để vượt qua vòng xét hỏi của Kiểm sát viên AI.',
  },
};

const CRAFT_SPECS = [
  {
    code: 'A-01',
    title: 'Tối ưu bàn tay & Apple Pencil',
    text: 'Vẽ, gạch chân và viết ghi chú lề trực tiếp lên biên bản với độ trễ thấp. Ngón tay để kéo bàn vô hạn, lòng bàn tay tự động được bỏ qua.',
  },
  {
    code: 'A-02',
    title: 'Giọng đọc ba miền chạy ngoại tuyến',
    text: 'Lời khai, bài báo và thư tay có thể phát thành tiếng với giọng Bắc, Trung hoặc Nam ngay trên trình duyệt — riêng tư, không gửi dữ liệu ra ngoài.',
  },
  {
    code: 'A-03',
    title: 'Nghi phạm & Kiểm sát viên AI',
    text: 'Nghi phạm phản ứng theo đúng các chứng cứ đã mở ở vòng hiện tại; muốn qua màn phải thuyết phục được Kiểm sát viên bằng chứng cứ xác thực.',
  },
  {
    code: 'A-04',
    title: 'Chơi một mình hoặc đồng bộ phòng 6 số',
    text: 'Tạo phòng trong một chạm, chia sẻ mã 6 số hoặc quét QR cho tối đa 6 thành viên để cùng kéo dây đỏ và hội ý theo thời gian thực.',
  },
] as const;

const FAQ = [
  ['Một vụ án chơi được bao nhiêu người?', 'Từ 1 đến 6 người. Chơi một mình như đọc một cuốn tiểu thuyết trinh thám tương tác; chơi nhóm thì mọi người cùng vào một phòng bằng mã 6 số hoặc mã QR.'],
  ['Chơi trên iPad và Apple Pencil có tốt không?', 'Bàn điều tra được thiết kế ưu tiên cho iPad: viết tay bằng Apple Pencil thẳng lên giấy, hai ngón phóng to/kéo bàn, chạm lòng bàn tay được bỏ qua. Có thể cài lên màn hình chính như ứng dụng độc lập.'],
  ['Tiến độ và nét vẽ có tự lưu không?', 'Có. Toàn bộ nét bút, dây đỏ, ghim chứng cứ và sổ tay được lưu tự động trên thiết bị (IndexedDB). Nếu đăng nhập, tiến độ còn đồng bộ lên cloud giữa nhiều máy.'],
  ['Nếu bị bí manh mối giữa chừng thì sao?', 'Mỗi câu hỏi đều có hệ thống gợi ý mở dần từng nấc: nấc đầu chỉ định tài liệu cần xem lại, nấc cuối chỉ rõ chi tiết chốt hạ để bạn không bao giờ bị kẹt cứng.'],
  ['Vụ án có thật và vụ án hư cấu khác nhau thế nào?', 'Hồ sơ hư cấu lấy bối cảnh Việt Nam quen thuộc nhưng toàn bộ nhân vật, cơ quan đều do tác giả dựng nên. Riêng mục "Vụ án có thật" tái hiện từ tư liệu công khai và luôn gắn nhãn cảnh báo riêng.'],
] as const;

const FALLBACK_HERO_DECK: CaseSummary[] = [
  {
    id: 'demo-01',
    no: 0,
    status: 'available',
    kind: 'fiction',
    title: 'Chiếc đồng hồ ở ngõ Gác Chuông',
    tagline: 'Cửa sổ vỡ, két sắt mở đúng mã, con chó becgie không sủa một tiếng.',
    difficulty: 2,
    players: '1–4',
    duration: '45–60 phút',
    setting: 'Phố cổ, Hà Nội (hư cấu)',
    cover: 'images/cover.webp',
    art: 'images/d01-window.webp',
    features: ['ai', 'exam', 'voice', 'starter'],
  },
  {
    id: 'con-nuoc-ram-thang-gieng',
    no: 1,
    status: 'available',
    kind: 'fiction',
    title: 'Con nước Rằm tháng Giêng',
    tagline: 'Cửa khoang then cài từ bên trong, nhưng nước sông Hàm Luông đã dâng ngập mặt người nằm mộng.',
    difficulty: 5,
    players: '2–6',
    duration: '150–180 phút',
    setting: 'Xã Tân Mỹ, Bến Tre (hư cấu)',
    cover: 'images/cover.webp',
    art: 'images/d04-boat.webp',
    features: ['ai', 'exam', 'voice'],
  },
  {
    id: 'chuyen-tau-dem-muong-man',
    no: 5,
    status: 'available',
    kind: 'fiction',
    title: 'Chuyến tàu đêm Mường Mán',
    tagline: 'Khoang giường nằm số 4 khoá từ bên trong khi đoàn tàu SE3 vượt đèo Cà Ná lúc nửa đêm.',
    difficulty: 5,
    players: '2–6',
    duration: '120–150 phút',
    setting: 'Toa 6 tàu Thống Nhất SE3, Bình Thuận (hư cấu)',
    cover: 'images/cover.webp',
    art: 'images/d01-bao-chi.webp',
    features: ['ai', 'exam', 'voice', 'accomplice'],
  },
];

const FEATURE_LABELS: Record<string, string> = {
  ai: 'Thẩm vấn nghi phạm AI',
  exam: 'Đối chất Kiểm sát viên',
  voice: 'Giọng đọc ba miền',
  accomplice: 'Có nghi phạm đồng phạm',
  starter: 'Hồ sơ nhập môn 15 phút làm quen',
};

export default function Home() {
  const { data: cases, error } = useAsync(loadCatalog, []);
  const [filter, setFilter] = useState<Filter>('all');
  const [deckIdx, setDeckIdx] = useState(0);
  const [deskLayer, setDeskLayer] = useState<DeskLayer>('all');
  const [selectedItem, setSelectedItem] = useState<string | null>(null);
  const { hash, key } = useLocation();
  const root = useRef<HTMLDivElement>(null);
  const initialScrollDone = useRef(false);

  useEffect(() => {
    document.title = `${SITE.name} – Bàn điều tra phá án tương tác`;
  }, []);

  useEffect(() => {
    if (!hash || (!cases && !error)) return undefined;
    const id = hash.slice(1);
    const delay = initialScrollDone.current ? 20 : 120;
    initialScrollDone.current = true;
    const go = () => { scrollToSection(id); };
    const t = window.setTimeout(go, delay);
    if (document.readyState !== 'complete') window.addEventListener('load', go, { once: true });
    return () => {
      window.clearTimeout(t);
      window.removeEventListener('load', go);
    };
  }, [hash, key, cases, error]);

  const open = (cases || []).filter((c) => c.status === 'available');
  const featured = open.find((c) => c.features?.includes('starter')) || open[0] || FALLBACK_HERO_DECK[0];
  const heroDeck = open.length >= 3
    ? [
        open.find((c) => c.id === 'demo-01') || open[0],
        open.find((c) => c.id === 'con-nuoc-ram-thang-gieng') || open[1],
        open.find((c) => c.id === 'chuyen-tau-dem-muong-man') || open[2],
      ]
    : FALLBACK_HERO_DECK;
  const activeDeckCase = heroDeck[deckIdx % heroDeck.length] || heroDeck[0];

  const ofKind = (k: CaseKind) => (cases || []).filter((c) => caseKind(c) === k);
  const shown = (cases || []).filter((c) => filter === 'all' || caseKind(c) === filter).slice().sort((a, b) => (a.no ?? 0) - (b.no ?? 0));
  const released = shown.filter((c) => c.status === 'available');
  const soon = shown.filter((c) => c.status !== 'available');

  const featuredTo = `/ho-so/${featured.id}`;
  const featuredImg = caseBase(featured.id) + (featured.art || featured.cover || 'images/cover.webp');
  const featuredMods = (featured.features || []).map((f) => FEATURE_LABELS[f]).filter(Boolean);

  const activeLayerMeta = DESK_LAYERS.find((l) => l.id === deskLayer) || DESK_LAYERS[0];
  const activeCardMeta = selectedItem ? DESK_ITEMS[selectedItem] : null;
  const itemStateClass = (id: string) => {
    const meta = DESK_ITEMS[id];
    if (!meta) return '';
    const isSel = selectedItem === id;
    if (selectedItem) return isSel ? ' is-focus' : ' is-dim';
    if (deskLayer === 'all') return '';
    return meta.layer === deskLayer ? ' is-focus' : ' is-dim';
  };

  useGSAP(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    gsap.from('.h-hero__copy > *', {
      y: 22, opacity: 0, duration: 0.7, stagger: 0.08, ease: 'power3.out', clearProps: 'transform,opacity',
    });
    gsap.from('.h-hero__deck', {
      y: 26, opacity: 0, duration: 0.8, delay: 0.14, ease: 'power3.out', clearProps: 'transform,opacity',
    });
    gsap.utils.toArray<HTMLElement>('.h-rv').forEach((el) => {
      gsap.from(el, {
        y: 24, opacity: 0, duration: 0.7, ease: 'power3.out', clearProps: 'transform,opacity',
        scrollTrigger: { trigger: el, start: 'top 88%', once: true },
      });
    });
    gsap.from('.desk-lab__wires path.desk-wire', {
      strokeDashoffset: 1, duration: 1.05, stagger: 0.1, ease: 'power2.inOut',
      scrollTrigger: { trigger: '.desk-lab', start: 'top 78%', once: true },
    });
  }, { scope: root });

  useGSAP(() => {
    if (!cases || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const cards = gsap.utils.toArray<HTMLElement>('.files .file, .soon-grid .soon-card');
    if (!cards.length) return;
    gsap.fromTo(
      cards,
      { y: 24, opacity: 0 },
      {
        y: 0, opacity: 1, duration: 0.55, stagger: 0.05, ease: 'power3.out', clearProps: 'transform,opacity',
        scrollTrigger: { trigger: '#catalog', start: 'top 95%', once: true },
      },
    );
    ScrollTrigger.refresh();
  }, { scope: root, dependencies: [Boolean(cases)] });

  return (
    <div id="top" ref={root}>
      <Nav cta={{ to: featuredTo, label: 'Mở hồ sơ' }} />

      <main>
        {/* ── 1. Split Asymmetric Editorial Hero + Live Case Deck ── */}
        <section className="h-hero">
          <div className="h-hero__grid-bg" aria-hidden="true" />
          <div className="wrap h-hero__inner">
            <div className="h-hero__copy">
              <p className="h-status">
                <span className="h-status__dot" aria-hidden="true" />
                Phòng lưu trữ trực tuyến · {open.length || 13} hồ sơ đang mở
              </p>
              <h1 className="h-title">
                Mọi dấu vết<br />
                đều chờ<br />
                <em>chân tướng.</em>
              </h1>
              <p className="lead">
                Mở tập hồ sơ điều tra ngay trên trình duyệt: soi biên bản, khoanh mực đỏ bằng Apple Pencil,
                căng dây đỏ nối manh mối và trực tiếp thẩm vấn nghi phạm AI.
              </p>
              <div className="h-hero__cta">
                <Link className="btn btn--primary" to={featuredTo}>Bắt đầu vụ nhập môn</Link>
                <a
                  className="btn btn--ghost"
                  href="#catalog"
                  onClick={(e) => {
                    e.preventDefault();
                    window.history.replaceState(null, '', '#catalog');
                    scrollToSection('catalog');
                  }}
                >
                  Duyệt kho hồ sơ
                </a>
              </div>
              <dl className="h-hero__specs">
                <div><dt>Hình thức</dt><dd>Chơi trên web · Miễn phí</dd></div>
                <div><dt>Số người</dt><dd>1–6 người · Phòng 6 số</dd></div>
                <div><dt>Thiết bị</dt><dd>iPad &amp; Apple Pencil</dd></div>
                <div><dt>Âm thanh</dt><dd>Giọng đọc 3 miền</dd></div>
              </dl>
            </div>

            <div className="h-hero__deck" aria-label="Xem nhanh các hồ sơ nổi bật">
              <div className="deck-stack">
                <div className="deck-folder-back" aria-hidden="true" />
                <div className="deck-folder-mid" aria-hidden="true" />
                <Link className="deck-card" to={`/ho-so/${activeDeckCase.id}`}>
                  <div className="deck-card__head">
                    <span className="deck-card__no">{caseNo(activeDeckCase)}</span>
                    <span className="deck-card__state">Đang mở</span>
                  </div>
                  <div className="deck-card__art">
                    <img
                      src={caseBase(activeDeckCase.id) + (activeDeckCase.art || activeDeckCase.cover || 'images/cover.webp')}
                      alt={activeDeckCase.title}
                      style={activeDeckCase.artPos ? { objectPosition: activeDeckCase.artPos } : undefined}
                    />
                    <div className="deck-card__corner" aria-hidden="true" />
                  </div>
                  <div className="deck-card__body">
                    {activeDeckCase.setting && (
                      <p className="deck-card__place">{activeDeckCase.setting.replace(/\s*\(hư cấu\)/gi, '')}</p>
                    )}
                    <h2>{activeDeckCase.title}</h2>
                    {activeDeckCase.tagline && <p className="deck-card__tag">{activeDeckCase.tagline}</p>}
                    <div className="deck-card__foot">
                      <span><Difficulty level={activeDeckCase.difficulty} /></span>
                      <span>{activeDeckCase.duration || '60 phút'}</span>
                      <span className="deck-card__go">Nhận hồ sơ →</span>
                    </div>
                  </div>
                </Link>
              </div>

              <div className="deck-tabs" role="tablist" aria-label="Chọn hồ sơ xem trước">
                {heroDeck.map((c, idx) => (
                  <button
                    key={c.id}
                    type="button"
                    role="tab"
                    aria-selected={idx === deckIdx % heroDeck.length}
                    className={`deck-tab${idx === deckIdx % heroDeck.length ? ' is-on' : ''}`}
                    onClick={() => setDeckIdx(idx)}
                  >
                    <small>{caseNo(c)}</small>
                    <span>{c.title}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* ── 2. Connected 4-Stage Investigation Rail ── */}
        <section id="how" className="h-sec h-flow">
          <div className="wrap">
            <div className="h-flow__head h-rv">
              <div>
                <p className="eyebrow">Quy trình phá án</p>
                <h2 className="h-disp">Bốn chặng khép lại một hồ sơ.</h2>
              </div>
              <p className="h-flow__sub">Tự do suy luận trên bàn vô hạn: không ép chọn đáp án trước khi mọi chứng cứ trong tay đã khớp.</p>
            </div>
            <ol className="h-rail">
              {FLOW_STEPS.map((s) => (
                <li key={s.no} className="h-rail__step h-rv">
                  <div className="h-rail__top">
                    <span className="h-rail__no">{s.no}</span>
                    <span className="h-rail__tag">{s.tag}</span>
                  </div>
                  <h3>{s.title}</h3>
                  <p>{s.text}</p>
                </li>
              ))}
            </ol>
          </div>
        </section>

        {/* ── 3. Split Editorial Featured Case ── */}
        <section id="featured" className="h-sec h-feat">
          <div className="wrap">
            <div className="h-feat__frame">
              <Link className="h-feat__media h-rv" to={featuredTo} aria-label={featured.title}>
                <img
                  src={featuredImg}
                  alt={featured.title}
                  style={featured.artPos ? { objectPosition: featured.artPos } : undefined}
                />
                <span className="vf vf--tl" aria-hidden="true" />
                <span className="vf vf--tr" aria-hidden="true" />
                <span className="vf vf--bl" aria-hidden="true" />
                <span className="vf vf--br" aria-hidden="true" />
                <span className="h-feat__coord">{featured.setting || 'Hồ sơ nhập môn'}</span>
              </Link>

              <div className="h-feat__info h-rv">
                <p className="eyebrow">Đề xuất cho lượt chơi đầu · {caseNo(featured)}</p>
                <h2 className="h-disp">{featured.title}</h2>
                {featured.tagline && <p className="h-feat__lead">{featured.tagline}</p>}
                <div className="h-feat__meta">
                  <span>Độ khó <Difficulty level={featured.difficulty} /></span>
                  <span>{featured.players || '1–4'} người</span>
                  <span>{featured.duration || '45–60 phút'}</span>
                </div>
                {!!featuredMods.length && (
                  <ul className="h-feat__mods">
                    {featuredMods.map((m) => <li key={m}>{m}</li>)}
                  </ul>
                )}
                <div className="h-feat__actions">
                  <Link className="btn btn--primary" to={`/choi/${featured.id}`}>Vào thẳng bàn điều tra</Link>
                  <Link className="btn btn--ghost" to={featuredTo}>Xem chi tiết hồ sơ</Link>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ── 4. Interactive Evidence Desk Showcase ── */}
        <section id="inside" className="h-sec h-desk">
          <div className="wrap">
            <div className="h-desk__head h-rv">
              <div>
                <p className="eyebrow">Bàn điều tra tương tác</p>
                <h2 className="h-disp">Không chỉ đọc hồ sơ — bạn tự tay dàn án.</h2>
              </div>
              <div className="desk-modes" role="tablist" aria-label="Lọc lớp công cụ trên bàn">
                {DESK_LAYERS.map((m) => (
                  <button
                    key={m.id}
                    type="button"
                    role="tab"
                    aria-selected={deskLayer === m.id}
                    className={`chip${deskLayer === m.id && !selectedItem ? ' is-on' : ''}`}
                    onClick={() => {
                      setDeskLayer(m.id);
                      setSelectedItem(null);
                    }}
                  >
                    {m.label}
                  </button>
                ))}
              </div>
            </div>

            <div className="desk-lab">
              <svg className="desk-lab__wires" viewBox="0 0 1000 540" preserveAspectRatio="none" aria-hidden="true">
                <path
                  className={`desk-wire${(deskLayer === 'board' || deskLayer === 'paper' || selectedItem === 'report' || selectedItem === 'blueprint') ? ' is-lit' : ''}`}
                  pathLength={1}
                  d="M 150 52 Q 265 110 395 62"
                />
                <path
                  className={`desk-wire${(deskLayer === 'board' || selectedItem === 'scene' || selectedItem === 'blueprint') ? ' is-lit' : ''}`}
                  pathLength={1}
                  d="M 395 62 Q 368 195 312 322"
                />
                <path
                  className={`desk-wire${(deskLayer === 'board' || deskLayer === 'ai' || selectedItem === 'suspects' || selectedItem === 'interrogation') ? ' is-lit' : ''}`}
                  pathLength={1}
                  d="M 622 46 Q 730 108 842 72"
                />
                <path
                  className={`desk-wire${(deskLayer === 'board' || selectedItem === 'scene' || selectedItem === 'evidence') ? ' is-lit' : ''}`}
                  pathLength={1}
                  d="M 312 322 Q 465 390 612 333"
                />
                <path
                  className={`desk-wire${(deskLayer === 'board' || deskLayer === 'ai' || selectedItem === 'suspects' || selectedItem === 'evidence') ? ' is-lit' : ''}`}
                  pathLength={1}
                  d="M 622 46 Q 570 190 612 333"
                />
              </svg>

              {/* Paper + Apple Pencil SVG circle */}
              <button
                type="button"
                className={`dl-card dl-report${itemStateClass('report')}`}
                onClick={() => setSelectedItem(selectedItem === 'report' ? null : 'report')}
              >
                <span className="dl-pin" aria-hidden="true" />
                <small>07/KNHT · BÚT LỤC GỐC</small>
                <b>BIÊN BẢN KHÁM NGHIỆM</b>
                <span className="dl-lines">
                  <i /><i className="w75" /><i className="hl">21:40 — Cửa khoá trong</i><i className="w65" />
                </span>
                <svg className="dl-pencil-mark" viewBox="0 0 180 56" aria-hidden="true">
                  <path d="M12 31C22 14 148 11 166 28C178 40 34 49 14 34C6 28 19 20 35 19" />
                </svg>
                <span className="dl-stamp">BÚT ĐỎ PENCIL</span>
              </button>

              {/* Blueprint */}
              <button
                type="button"
                className={`dl-card dl-map${itemStateClass('blueprint')}`}
                onClick={() => setSelectedItem(selectedItem === 'blueprint' ? null : 'blueprint')}
              >
                <span className="dl-pin" aria-hidden="true" />
                <img src="/cases/demo-01/images/d02-so-do-nha.webp" alt="" />
                <span>Sơ đồ ngõ Gác Chuông</span>
              </button>

              {/* Suspect IDs */}
              <button
                type="button"
                className={`dl-card dl-id${itemStateClass('suspects')}`}
                onClick={() => setSelectedItem(selectedItem === 'suspects' ? null : 'suspects')}
              >
                <span className="dl-pin" aria-hidden="true" />
                <div className="dl-id__pair">
                  <img src="/cases/chuyen-tau-dem-muong-man/images/id-long.webp" alt="" />
                  <img src="/cases/chuyen-tau-dem-muong-man/images/id-thao.webp" alt="" />
                </div>
                <div className="dl-id__cap">
                  <b>Hồ sơ nhân thân</b>
                  <small>5 nhân vật liên quan</small>
                </div>
              </button>

              {/* AI Interrogation & Voice panel */}
              <button
                type="button"
                className={`dl-card dl-ai${itemStateClass('interrogation')}`}
                onClick={() => setSelectedItem(selectedItem === 'interrogation' ? null : 'interrogation')}
              >
                <span className="dl-pin" aria-hidden="true" />
                <div className="dl-ai__top">
                  <span>Thẩm vấn AI</span>
                  <span className="dl-ai__voice">● Giọng miền Bắc</span>
                </div>
                <p className="dl-ai__q">“Lúc tàu qua ga Cà Ná, vé số 04 ở đâu?”</p>
                <p className="dl-ai__a">“Tôi… tôi để quên trong túi áo khoác từ tối.”</p>
                <div className="dl-ai__wave" aria-hidden="true">
                  <i /><i /><i /><i /><i /><i /><i />
                  <span>0:14 / Nghe lời khai</span>
                </div>
              </button>

              {/* Scene polaroid */}
              <button
                type="button"
                className={`dl-card dl-scene${itemStateClass('scene')}`}
                onClick={() => setSelectedItem(selectedItem === 'scene' ? null : 'scene')}
              >
                <span className="dl-pin" aria-hidden="true" />
                <img src="/cases/chuyen-tau-dem-muong-man/images/d01-bao-chi.webp" alt="" />
                <span>Toa SE3 · Hiện trường đèo Cà Ná</span>
              </button>

              {/* Tang vật / Kiểm sát viên */}
              <button
                type="button"
                className={`dl-card dl-evid${itemStateClass('evidence')}`}
                onClick={() => setSelectedItem(selectedItem === 'evidence' ? null : 'evidence')}
              >
                <span className="dl-pin" aria-hidden="true" />
                <img src="/cases/vet-muc-lang-dong-ho/images/d03-ban-khac.webp" alt="" />
                <div className="dl-evid__foot">
                  <small>TANG VẬT ĐỐI CHIẾU</small>
                  <b>Bản khắc gỗ vỡ đôi</b>
                </div>
              </button>
            </div>

            <div className="desk-caption" aria-live="polite">
              <span className="desk-caption__badge">
                {activeCardMeta ? activeCardMeta.label : activeLayerMeta.label}
              </span>
              <p>{activeCardMeta ? activeCardMeta.note : activeLayerMeta.hint}</p>
              {selectedItem && (
                <button type="button" className="link-btn" onClick={() => setSelectedItem(null)}>
                  Bỏ chọn
                </button>
              )}
            </div>
          </div>
        </section>

        {/* ── 5. Continue Strip + Case Archive Shelf ── */}
        <ContinueStrip />

        <section id="catalog" className="section h-shelf">
          <div className="wrap">
            <div className="section__head h-rv">
              <div>
                <p className="eyebrow">Kho hồ sơ lưu trữ</p>
                <h2>Chọn một vụ án để bắt đầu.</h2>
              </div>
              <div className="chips" role="tablist" aria-label="Lọc hồ sơ">
                {FILTERS.map((f) => (
                  <button
                    key={f.id}
                    type="button"
                    role="tab"
                    aria-selected={filter === f.id}
                    className={`chip${filter === f.id ? ' is-on' : ''}${f.id === 'true-crime' ? ' chip--real' : ''}`}
                    onClick={() => setFilter(f.id)}
                  >
                    {f.label}{cases && <span className="chip__n">{f.id === 'all' ? cases.length : ofKind(f.id).length}</span>}
                  </button>
                ))}
              </div>
            </div>

            {error ? <p className="catalog__empty">Không tải được kho hồ sơ.</p>
              : !cases ? <p className="catalog__empty">Đang tải hồ sơ…</p>
                : !shown.length ? <p className="catalog__empty">Chưa có hồ sơ nào trong mục này.</p>
                  : (
                    <>
                      {!!released.length && (
                        <div className="files">{released.map((c) => <ReleasedCard key={c.id} entry={c} />)}</div>
                      )}
                      {!!soon.length && (
                        <div className="cat-block cat-block--soon">
                          <div className="cat-block__head">
                            <h3>Đang biên tập<span className="cat-block__n">{soon.length} hồ sơ</span></h3>
                            <p>Đang hoàn thiện ảnh tư liệu và giọng đọc. Hồ sơ nào xong sẽ mở niêm phong ngay tại đây.</p>
                          </div>
                          <div className="soon-grid">{soon.map((c) => <SoonCard key={c.id} entry={c} />)}</div>
                        </div>
                      )}
                    </>
                  )}
          </div>
        </section>

        {/* ── 6. Asymmetric Archival Paper Spec Sheet ── */}
        <section id="craft" className="h-craft">
          <div className="wrap h-craft__grid">
            <div className="h-craft__lead h-rv">
              <p className="eyebrow">Thiết kế cho bàn điều tra</p>
              <h2>Tập hồ sơ Việt Nam.<br />Công cụ của thời đại số.</h2>
              <p>Không dừng ở đọc chữ và bấm chọn: mọi thao tác đều xoay quanh trải nghiệm lật giấy, khoanh bút mực và đối chất trực tiếp.</p>
              <div className="h-craft__seal">Cài được PWA · Hỗ trợ Apple Pencil · Giọng đọc on-device</div>
            </div>
            <dl className="h-craft__list">
              {CRAFT_SPECS.map((s) => (
                <div key={s.code} className="h-craft__row h-rv">
                  <dt>
                    <span>{s.code}</span>
                    <b>{s.title}</b>
                  </dt>
                  <dd>{s.text}</dd>
                </div>
              ))}
            </dl>
          </div>
        </section>

        {/* ── 7. FAQ & Quick Archive Index ── */}
        <section id="faq" className="h-sec faq">
          <div className="wrap faq__inner">
            <div className="faq__side h-rv">
              <p className="eyebrow">Hỏi đáp nhanh</p>
              <h2 className="h-disp">Trước khi mở tập giấy đầu tiên</h2>
              <dl className="faq__stats">
                <div><dt>Hồ sơ đang mở</dt><dd>{open.length || 13} vụ</dd></div>
                <div><dt>Đang dựng thêm</dt><dd>{soon.length || 3} vụ</dd></div>
                <div><dt>Chơi cùng lúc</dt><dd>1–6 người</dd></div>
              </dl>
            </div>
            <div className="faq__list">
              {FAQ.map(([q, a]) => <details key={q}><summary>{q}</summary><p>{a}</p></details>)}
            </div>
          </div>
        </section>

        {/* ── 8. Solo vs 6-Digit Room Closing Strip ── */}
        <section className="h-close">
          <div className="wrap h-close__inner">
            <div className="h-close__copy h-rv">
              <p className="eyebrow">Bắt đầu ngay lúc này</p>
              <h2>Chơi một mình, hoặc mở phòng cùng đồng đội.</h2>
              <p>Không cần tải file cài đặt nặng máy. Nhận ngay hồ sơ nhập môn chỉ trong một chạm hoặc gia nhập bàn điều tra chung.</p>
              <div className="h-close__actions">
                <Link className="btn btn--primary" to={featuredTo}>Mở vụ án đầu tiên</Link>
                <Link className="btn btn--ghost" to="/dang-nhap">Đăng nhập lưu tiến độ</Link>
              </div>
            </div>

            <div className="h-roombox h-rv">
              <span className="h-roombox__kicker">Chơi nhóm qua trình duyệt</span>
              <h3>Nhập mã phòng 6 số</h3>
              <p>Chủ phòng tạo mã 6 chữ số &amp; QR; mọi người cùng thấy dây đỏ và ghi chú trên bàn.</p>
              <div className="h-roombox__digits" aria-hidden="true">
                <span>4</span><span>8</span><span>2</span><i /><span>9</span><span>1</span><span>7</span>
              </div>
              <Link className="btn btn--ghost" to="/tham-gia">Nhập mã vào phòng →</Link>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
