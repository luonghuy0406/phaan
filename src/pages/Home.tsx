import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';
import { CaseCard, Footer, Nav } from '../components/site';
import { ContinueStrip } from '../components/progress';
import { loadCatalog, useAsync, caseKind } from '../lib/data';
import type { CaseKind } from '../lib/types';
import { SITE } from '../lib/config';
import '../styles/home.css';

gsap.registerPlugin(ScrollTrigger, useGSAP);

type Filter = 'all' | CaseKind;
const FILTERS: { id: Filter; label: string }[] = [
  { id: 'all', label: 'Tất cả' },
  { id: 'fiction', label: 'Hư cấu' },
  { id: 'true-crime', label: 'Vụ án có thật' },
];
const GROUPS: { kind: CaseKind; title: string; note: string }[] = [
  { kind: 'fiction', title: 'Hồ sơ hư cấu', note: 'Nhân vật, địa danh và tình tiết đều do chúng tôi dựng nên. Phù hợp để chơi cùng bạn bè, gia đình.' },
  { kind: 'true-crime', title: 'Dựa trên vụ án có thật', note: 'Tái hiện từ thông tin công khai về những vụ án đã xảy ra. Có chi tiết dễ gây ám ảnh, không dành cho trẻ em.' },
];

const TICKER = ['Biên bản khám nghiệm', 'Lời khai nhân chứng', 'Ảnh hiện trường', 'Tang vật', 'Dây đỏ', 'Sổ tay điều tra', 'Hồ sơ niêm phong', 'Apple Pencil'];

const STEPS = [
  { no: '01', title: 'Đọc hồ sơ', text: 'Bài báo, biên bản, lời khai, ảnh chụp, hoá đơn… Mọi tài liệu trải trên một bàn điều tra rộng, kéo thả và phóng to tuỳ ý.', art: 'read' },
  { no: '02', title: 'Ghi chép như thật', text: 'Khoanh tròn bằng Apple Pencil, tô dạ quang, căng dây đỏ giữa hai lời khai mâu thuẫn, dán giấy ghi chú suy luận.', art: 'ink' },
  { no: '03', title: 'Mở niêm phong', text: 'Ghim bằng chứng, chỉ ra dòng khai man. Mỗi trọng điểm giải đúng sẽ mở phong bì hồ sơ tiếp theo.', art: 'seal' },
  { no: '04', title: 'Gọi tên hung thủ', text: 'Kết luận cuối cùng cùng lời giải chi tiết. Bị kẹt thì có gợi ý mở dần từng nấc, không lộ đáp án.', art: 'stamp' },
] as const;

const FAQ = [
  ['Một vụ án chơi được bao nhiêu người?', 'Từ 1 đến 6 người. Chơi một mình như đọc một cuốn trinh thám tương tác; chơi nhóm thì mỗi người vào cùng một phòng bằng mã 6 số hoặc mã QR.'],
  ['Chơi trên iPad có tốt không?', 'Bàn điều tra được thiết kế cho iPad: viết tay bằng Apple Pencil thẳng lên tài liệu, ngón tay để di chuyển và phóng to, chạm lòng bàn tay khi viết được bỏ qua. Cài lên màn hình chính để chơi toàn màn hình.'],
  ['Tiến độ có được lưu không?', 'Có. Tiến độ, nét vẽ và sổ tay tự lưu trên máy; khi đăng nhập thì lưu cả lên cloud để mở tiếp trên thiết bị khác.'],
  ['Nếu bị kẹt thì sao?', 'Mỗi câu hỏi có gợi ý mở dần từng nấc: nấc đầu chỉ hướng tới tài liệu cần đọc lại, nấc cuối gần như chỉ thẳng vào chi tiết.'],
  ['Các vụ án có phải chuyện có thật?', 'Không. Mọi nhân vật, địa danh cụ thể và sự kiện đều là hư cấu, được viết riêng cho trò chơi.'],
];

function StepArt({ kind }: { kind: (typeof STEPS)[number]['art'] }) {
  if (kind === 'read') {
    return (
      <div className="h-art h-art--read">
        <div className="h-mini-paper"><b>Biên bản</b><i /><i /><i className="w60" /><i /><i className="w40" /></div>
        <div className="h-mini-paper h-mini-paper--b"><b>Lời khai</b><i /><i className="w70" /><i /><i className="w50" /></div>
      </div>
    );
  }
  if (kind === 'ink') {
    return (
      <div className="h-art h-art--ink">
        <div className="h-mini-paper"><b>Lời khai · dòng 007</b><i /><i className="w70" /><i className="h-hl" /><i /><i className="w50" /></div>
        <svg viewBox="0 0 200 120" className="h-ink"><path pathLength={1} d="M30 66 C 40 40, 150 38, 168 62 S 60 98, 34 72" /></svg>
      </div>
    );
  }
  if (kind === 'seal') {
    return (
      <div className="h-art h-art--seal">
        <div className="h-envelope"><span className="stamp">Niêm phong</span><b>Trọng điểm 3</b><small>3 tài liệu</small></div>
      </div>
    );
  }
  return (
    <div className="h-art h-art--stamp">
      <div className="h-mini-paper h-mini-paper--wide"><b>Kết luận điều tra</b><i /><i className="w70" /><i /><i className="w60" /></div>
      <span className="stamp h-stamp-final">Đã phá án</span>
    </div>
  );
}

export default function Home() {
  const { data: cases, error } = useAsync(loadCatalog, []);
  const [filter, setFilter] = useState<Filter>('all');
  const { hash } = useLocation();
  const root = useRef<HTMLDivElement>(null);
  useEffect(() => { document.title = `${SITE.name} – Game phá án trên web`; }, []);
  // jump to #catalog etc.; again after images load, since they push sections down
  useEffect(() => {
    if (!hash || !cases) return undefined;
    const go = () => { document.getElementById(hash.slice(1))?.scrollIntoView(); ScrollTrigger.refresh(); };
    const t = window.setTimeout(go, 120);
    window.addEventListener('load', go, { once: true });
    return () => { window.clearTimeout(t); window.removeEventListener('load', go); };
  }, [hash, cases]);

  const open = (cases || []).filter((c) => c.status === 'available');
  const featured = open[0];
  const ofKind = (k: CaseKind) => (cases || []).filter((c) => caseKind(c) === k);
  const groups = GROUPS.filter((g) => filter === 'all' || g.kind === filter).map((g) => ({ ...g, list: ofKind(g.kind) })).filter((g) => g.list.length);
  const featuredTo = featured ? `/ho-so/${featured.id}` : '/#catalog';

  /* ── animations: everything degrades to the static layout with prefers-reduced-motion ── */
  useGSAP(() => {
    const mm = gsap.matchMedia();
    mm.add({ motion: '(prefers-reduced-motion: no-preference)', desktop: '(min-width: 900px)', fine: '(pointer: fine)' }, (ctx) => {
      const { motion, desktop, fine } = ctx.conditions as { motion: boolean; desktop: boolean; fine: boolean };
      if (!motion) return undefined;

      // hero entrance
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
      tl.from('.h-word > span', { yPercent: 115, rotate: 6, duration: 0.9, stagger: 0.06 })
        .from('.h-hero .h-reveal', { y: 24, opacity: 0, duration: 0.7, stagger: 0.08 }, '-=0.5')
        .from('.h-photo, .h-file, .h-note', {
          y: -80, opacity: 0, scale: 1.12, rotate: (i: number) => [-14, 12, -10, 8, -6][i % 5],
          duration: 0.9, stagger: 0.12, ease: 'back.out(1.4)',
        }, 0.25)
        .fromTo('.h-string path', { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut' }, '-=0.3')
        .from('.h-pin', { scale: 0, duration: 0.35, stagger: 0.12, ease: 'back.out(3)' }, '<0.2');


      // hero parallax on scroll
      const depth: [string, number][] = [['.h-photo--a', -90], ['.h-photo--b', -40], ['.h-photo--c', -130], ['.h-file', -20], ['.h-note', -160]];
      depth.forEach(([sel, y]) => {
        gsap.to(sel, { y, ease: 'none', scrollTrigger: { trigger: '.h-hero', start: 'top top', end: 'bottom top', scrub: true } });
      });
      gsap.to('.h-hero__copy', { y: 80, opacity: 0.2, ease: 'none', scrollTrigger: { trigger: '.h-hero', start: 'top top', end: 'bottom top', scrub: true } });

      // the desk leans toward the pointer; a lamp follows it
      let unbind = () => {};
      if (fine) {
        const board = document.querySelector<HTMLElement>('.h-board');
        const hero = document.querySelector<HTMLElement>('.h-hero');
        if (board && hero) {
          const rx = gsap.quickTo(board, 'rotationX', { duration: 0.6, ease: 'power3' });
          const ry = gsap.quickTo(board, 'rotationY', { duration: 0.6, ease: 'power3' });
          const onMove = (e: PointerEvent) => {
            const r = hero.getBoundingClientRect();
            const px = (e.clientX - r.left) / r.width - 0.5;
            const py = (e.clientY - r.top) / r.height - 0.5;
            rx(-py * 8); ry(px * 10);
            hero.style.setProperty('--mx', `${e.clientX - r.left}px`);
            hero.style.setProperty('--my', `${e.clientY - r.top}px`);
          };
          hero.addEventListener('pointermove', onMove);
          unbind = () => hero.removeEventListener('pointermove', onMove);
        }
      }

      // ticker
      gsap.to('.h-ticker__track', { xPercent: -50, ease: 'none', duration: 40, repeat: -1 });

      // section headings
      gsap.utils.toArray<HTMLElement>('.h-rise').forEach((el) => {
        gsap.from(el, { y: 40, opacity: 0, duration: 0.8, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 85%' } });
      });

      // how to play: pinned and scrubbed on large screens, simple reveals on phones
      if (desktop) {
        const steps = gsap.utils.toArray<HTMLElement>('.h-step');
        gsap.set(steps.slice(1), { yPercent: 40, opacity: 0 });
        gsap.set('.h-how__bar i', { scaleX: 1 / steps.length });
        gsap.set('.h-how__dots span', { opacity: (j: number) => (j === 0 ? 1 : 0.25) });
        const how = gsap.timeline({
          scrollTrigger: { trigger: '.h-how', start: 'top top', end: `+=${steps.length * 70}%`, scrub: 0.6, pin: true, anticipatePin: 1 },
        });
        steps.forEach((step, i) => {
          if (i === 0) return;
          how.to(steps[i - 1], { yPercent: -30, opacity: 0, duration: 1 }, i)
            .to(step, { yPercent: 0, opacity: 1, duration: 1 }, i)
            .to('.h-how__bar i', { scaleX: (i + 1) / steps.length, duration: 1 }, i)
            .to('.h-how__dots span', { opacity: (j: number) => (j === i ? 1 : 0.25), duration: 0.3 }, i + 0.4);
        });
        how.fromTo('.h-step .h-ink path', { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.8 }, 1.3);
      } else {
        gsap.utils.toArray<HTMLElement>('.h-step').forEach((step) => {
          gsap.from(step, { y: 50, opacity: 0, duration: 0.7, scrollTrigger: { trigger: step, start: 'top 85%' } });
        });
      }

      // features
      gsap.utils.toArray<HTMLElement>('.h-feat').forEach((feat) => {
        const media = feat.querySelector('.h-feat__media');
        gsap.from(media, { clipPath: 'inset(18% 18% 18% 18% round 22px)', duration: 1.1, ease: 'power3.out', scrollTrigger: { trigger: feat, start: 'top 75%' } });
        gsap.from(feat.querySelectorAll('.h-feat__copy > *'), { y: 30, opacity: 0, stagger: 0.08, duration: 0.7, scrollTrigger: { trigger: feat, start: 'top 70%' } });
      });
      gsap.fromTo('.h-feat--ink .h-ink path', { strokeDashoffset: 1 }, { strokeDashoffset: 0, ease: 'none', scrollTrigger: { trigger: '.h-feat--ink', start: 'top 70%', end: 'center 40%', scrub: true } });
      gsap.from('.h-toast', { x: 60, opacity: 0, stagger: 0.35, duration: 0.6, ease: 'back.out(1.6)', scrollTrigger: { trigger: '.h-feat--team', start: 'top 60%' } });
      gsap.fromTo('.h-feat--place img', { yPercent: -8, scale: 1.15 }, { yPercent: 8, scale: 1.15, ease: 'none', scrollTrigger: { trigger: '.h-feat--place', start: 'top bottom', end: 'bottom top', scrub: true } });
      gsap.fromTo('.h-cta__bg', { yPercent: -12 }, { yPercent: 12, ease: 'none', scrollTrigger: { trigger: '.h-cta', start: 'top bottom', end: 'bottom top', scrub: true } });
      return () => unbind();
    });
  }, { scope: root });

  // case cards appear as they enter (re-run when the list first arrives)
  useGSAP(() => {
    if (!cases || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const cards = gsap.utils.toArray<HTMLElement>('.catalog .case-card');
    gsap.set(cards, { y: 50, opacity: 0 });
    ScrollTrigger.batch(cards, {
      start: 'top 90%',
      once: true,
      onEnter: (els) => gsap.to(els, { y: 0, opacity: 1, duration: 0.7, stagger: 0.08, ease: 'power3.out', overwrite: true }),
    });
    ScrollTrigger.refresh();
  }, { scope: root, dependencies: [Boolean(cases)] });

  // count up once the catalog has arrived (the span has no React children, so GSAP owns its text)
  const countRef = useRef<HTMLSpanElement>(null);
  const openCount = open.length;
  useEffect(() => {
    const el = countRef.current;
    if (!el || !cases) return undefined;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = String(openCount); return undefined; }
    const o = { v: 0 };
    const tw = gsap.to(o, { v: openCount, duration: 1.2, ease: 'power1.out', onUpdate: () => { el.textContent = String(Math.round(o.v)); } });
    return () => { tw.kill(); };
  }, [cases, openCount]);

  const words = ['Mọi', 'vụ', 'án', 'đều', 'để', 'lại'];
  return (
    <div ref={root}>
      <Nav />
      <main>
        <section className="h-hero">
          <div className="h-hero__lamp" aria-hidden="true" />
          <div className="wrap h-hero__inner">
            <div className="h-hero__copy">
              <p className="eyebrow h-reveal">Boardgame phá án · Chơi trên trình duyệt</p>
              <h1 className="h-title">
                {words.map((w) => <span key={w} className="h-word"><span>{w}</span></span>)}{' '}
                <span className="h-word"><span><em>dấu vết.</em></span></span>
              </h1>
              <p className="lead h-reveal">Mở hồ sơ, đọc biên bản, đối chiếu từng lời khai và nối manh mối bằng dây đỏ. Không người dẫn chuyện, không đáp án dọn sẵn: chỉ có bạn và sự thật bị giấu trong giấy tờ.</p>
              <div className="hero__cta h-reveal">
                <Link className="btn btn--primary" to={featuredTo}>Mở hồ sơ đầu tiên</Link>
                <a className="btn btn--ghost" href="#how">Xem cách chơi</a>
              </div>
              <dl className="h-stats h-reveal">
                <div><dt>Hồ sơ đang mở</dt><dd><span ref={countRef}>–</span></dd></div>
                <div><dt>Người chơi</dt><dd>1–6</dd></div>
                <div><dt>Tối ưu cho</dt><dd>iPad & Pencil</dd></div>
              </dl>
            </div>

            <div className="h-board-wrap" aria-hidden="true">
              <div className="h-board">
                <figure className="h-photo h-photo--a"><img src="/site/photo-watch.webp" alt="" /><figcaption>Tang vật · TV-03</figcaption></figure>
                <figure className="h-photo h-photo--b"><img src="/site/photo-cctv.webp" alt="" /><figcaption>Camera đầu ngõ · 22:53</figcaption></figure>
                <figure className="h-photo h-photo--c"><img src="/site/photo-river.webp" alt="" /><figcaption>Bến sông · 06:15</figcaption></figure>
                <div className="h-file"><span className="h-file__tab" /><span className="stamp">Mật</span><b>Hồ sơ 01</b><small>Lời khai · Biên bản · Tang vật</small></div>
                <div className="h-note">Ai biết mã két?</div>
                <svg className="h-string" viewBox="0 0 100 100" preserveAspectRatio="none">
                  <path pathLength={1} d="M24 9 Q 52 34 77 26 Q 58 52 36 58 Q 62 84 82 72" />
                </svg>
                <span className="h-pin" style={{ left: '24%', top: '9%' }} />
                <span className="h-pin" style={{ left: '77%', top: '26%' }} />
                <span className="h-pin" style={{ left: '36%', top: '58%' }} />
                <span className="h-pin" style={{ left: '82%', top: '72%' }} />
              </div>
            </div>
          </div>
          <a className="h-scroll" href="#catalog" aria-label="Cuộn xuống kho hồ sơ"><span /></a>
        </section>

        <div className="h-ticker" aria-hidden="true">
          <div className="h-ticker__track">
            {[...TICKER, ...TICKER].map((t, i) => <span key={i}>{t}<i>✦</i></span>)}
          </div>
        </div>

        <ContinueStrip />

        <section id="catalog" className="section">
          <div className="wrap">
            <div className="section__head h-rise">
              <div>
                <p className="eyebrow">Kho hồ sơ</p>
                <h2>Chọn vụ án để điều tra</h2>
              </div>
              <div className="chips" role="tablist" aria-label="Lọc hồ sơ">
                {FILTERS.map((f) => (
                  <button key={f.id} type="button" role="tab" aria-selected={filter === f.id} className={`chip${filter === f.id ? ' is-on' : ''}${f.id === 'true-crime' ? ' chip--real' : ''}`} onClick={() => setFilter(f.id)}>
                    {f.label}{cases && <span className="chip__n">{f.id === 'all' ? cases.length : ofKind(f.id).length}</span>}
                  </button>
                ))}
              </div>
            </div>
            {error ? <p className="catalog__empty">Không tải được kho hồ sơ.</p>
              : !cases ? <p className="catalog__empty">Đang tải hồ sơ…</p>
                : groups.length ? groups.map((g) => (
                  <div key={g.kind} className={`catalog-group catalog-group--${g.kind}`}>
                    <div className="catalog-group__head">
                      <h3>{g.title}<span>{g.list.length} hồ sơ</span></h3>
                      <p>{g.note}</p>
                    </div>
                    <div className="catalog">{g.list.map((c) => <CaseCard key={c.id} entry={c} />)}</div>
                  </div>
                ))
                  : <p className="catalog__empty">Chưa có hồ sơ nào trong mục này.</p>}
          </div>
        </section>

        <section id="how" className="h-how">
          <div className="wrap h-how__inner">
            <div className="h-how__left">
              <p className="eyebrow">Cách chơi</p>
              <h2>Bốn bước từ hồ sơ đến hung thủ</h2>
              <p className="lead">Không cần luật dài dòng. Đọc kỹ, ghi chép, và để giấy tờ tự lên tiếng.</p>
              <div className="h-how__bar"><i /></div>
              <div className="h-how__dots">{STEPS.map((s) => <span key={s.no}>{s.no}</span>)}</div>
            </div>
            <div className="h-how__stage">
              {STEPS.map((s) => (
                <article key={s.no} className="h-step">
                  <StepArt kind={s.art} />
                  <div className="h-step__copy">
                    <span className="h-step__no">{s.no}</span>
                    <h3>{s.title}</h3>
                    <p>{s.text}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="section h-feats">
          <div className="wrap">
            <article className="h-feat h-feat--ink">
              <div className="h-feat__media">
                <div className="h-tablet">
                  <div className="h-tablet__screen">
                    <div className="h-mini-paper h-mini-paper--wide"><b>Biên bản ghi lời khai</b><i /><i className="w70" /><i /><i className="h-hl" /><i className="w60" /><i /><i className="w50" /></div>
                    <svg viewBox="0 0 200 120" className="h-ink"><path pathLength={1} d="M24 74 C 34 46, 162 44, 176 70 S 56 104, 28 78" /></svg>
                  </div>
                  <span className="h-pencil" />
                </div>
              </div>
              <div className="h-feat__copy">
                <p className="eyebrow">iPad &amp; Apple Pencil</p>
                <h3>Viết thẳng lên hồ sơ</h3>
                <p>Nét bút cảm ứng lực nhấn, bám theo tài liệu khi bạn kéo hay xoay. Bút để viết, ngón tay để di chuyển; lòng bàn tay chạm màn hình khi viết được bỏ qua.</p>
              </div>
            </article>

            <article className="h-feat h-feat--team">
              <div className="h-feat__media">
                <div className="h-team">
                  <div className="h-team__people">
                    {[['L', '#1f4fa8'], ['M', '#2f8f5b'], ['H', '#b7791f'], ['T', '#c2417a']].map(([n, c]) => <span key={n} className="avatar" style={{ background: c, width: 48, height: 48, fontSize: 20 }}>{n}</span>)}
                  </div>
                  <p className="h-toast"><b>Lan</b> ghim Tài liệu 09 làm bằng chứng</p>
                  <p className="h-toast"><b>Minh</b> chọn dòng 007 trong Tài liệu 16</p>
                  <p className="h-toast h-toast--ok"><b>Hà</b> đã giải câu 3!</p>
                  <div className="h-code"><span>Mã phòng</span><b>482 915</b></div>
                </div>
              </div>
              <div className="h-feat__copy">
                <p className="eyebrow">Chơi nhóm</p>
                <h3>Cùng một bàn, nhiều đôi mắt</h3>
                <p>Chủ phòng mời bằng mã 6 số hoặc mã QR. Cả nhóm thấy ngay ai ghim gì, ai chọn dòng khai nào, cùng ghi sổ tay nhóm và cùng mở niêm phong.</p>
              </div>
            </article>

            <article className="h-feat h-feat--place">
              <div className="h-feat__media"><img src="/site/photo-river.webp" alt="Bến sông miền Tây lúc sáng sớm" loading="lazy" /></div>
              <div className="h-feat__copy">
                <p className="eyebrow">Bối cảnh Việt Nam</p>
                <h3>Những vụ án rất gần</h3>
                <p>Bến sông miền Tây, khu tập thể thời bao cấp, phố cổ đêm Rằm. Mỗi hồ sơ là một câu chuyện độc lập, công bằng với người chơi: mọi manh mối đều nằm trên giấy.</p>
              </div>
            </article>
          </div>
        </section>

        <section id="faq" className="section faq">
          <div className="wrap faq__inner">
            <div className="h-rise"><p className="eyebrow">Hỏi đáp</p><h2>Trước khi mở hồ sơ</h2></div>
            <div className="faq__list">
              {FAQ.map(([q, a]) => <details key={q}><summary>{q}</summary><p>{a}</p></details>)}
            </div>
          </div>
        </section>

        <section className="h-cta">
          <img className="h-cta__bg" src="/site/bg-window.webp" alt="" aria-hidden="true" loading="lazy" />
          <div className="wrap h-cta__inner h-rise">
            <p className="eyebrow">Hồ sơ đang chờ trên bàn</p>
            <h2>Sự thật nằm đâu đó<br />trong tập giấy này.</h2>
            <Link className="btn btn--primary" to={featuredTo}>Bắt đầu điều tra</Link>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}
