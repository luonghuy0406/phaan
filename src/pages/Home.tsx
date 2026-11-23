import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { CaseCard, Footer, Nav } from '../components/site';
import { loadCatalog, useAsync } from '../lib/data';
import { SITE } from '../lib/config';

type Filter = 'all' | 'available' | 'coming-soon';
const FILTERS: { id: Filter; label: string }[] = [
  { id: 'all', label: 'Tất cả' },
  { id: 'available', label: 'Đang mở' },
  { id: 'coming-soon', label: 'Sắp ra mắt' },
];

const FAQ = [
  ['Một vụ án chơi được bao nhiêu người?', 'Từ 1 đến 6 người. Chơi một mình như đọc một cuốn trinh thám tương tác, chơi nhóm thì mỗi người cầm một phần hồ sơ rồi đối chiếu.'],
  ['Chơi trên iPad có tốt không?', 'Bàn điều tra được thiết kế cho iPad: viết tay bằng Apple Pencil thẳng lên tài liệu, ngón tay để di chuyển và phóng to, lòng bàn tay chạm màn hình khi đang viết sẽ được bỏ qua. Thêm trang vào màn hình chính để chơi toàn màn hình.'],
  ['Có cần cài đặt hay tạo tài khoản không?', 'Không. Bàn điều tra chạy trực tiếp trên trình duyệt. Tiến trình, nét vẽ và sổ tay được lưu tự động trên thiết bị bạn đang dùng.'],
  ['Nếu bị kẹt thì sao?', 'Mỗi câu hỏi có gợi ý mở dần từng nấc: nấc đầu chỉ hướng bạn tới tài liệu cần đọc lại, nấc cuối gần như chỉ thẳng vào chi tiết.'],
  ['Các vụ án có phải chuyện có thật?', 'Không. Mọi nhân vật, địa danh cụ thể và sự kiện đều là hư cấu, được viết riêng cho trò chơi.'],
];

export default function Home() {
  const { data: cases, error } = useAsync(loadCatalog, []);
  const [filter, setFilter] = useState<Filter>('all');
  const { hash } = useLocation();
  useEffect(() => { document.title = `${SITE.name} – Game phá án trên web`; }, []);
  // jump to #catalog etc.; again after cover images load, since they push the section down
  useEffect(() => {
    if (!hash || !cases) return undefined;
    const go = () => document.getElementById(hash.slice(1))?.scrollIntoView();
    go();
    const t = window.setTimeout(go, 400);
    window.addEventListener('load', go, { once: true });
    return () => { window.clearTimeout(t); window.removeEventListener('load', go); };
  }, [hash, cases]);

  const featured = cases?.find((c) => c.status === 'available');
  const list = (cases || []).filter((c) => filter === 'all' || c.status === filter);
  const featuredTo = featured ? `/ho-so/${featured.id}` : '/#catalog';

  return (
    <>
      <Nav />
      <main>
        <section className="hero">
          <div className="wrap hero__inner">
            <div className="hero__copy">
              <p className="eyebrow">Boardgame phá án · Chơi trên trình duyệt</p>
              <h1>Mọi vụ án đều để lại <em>dấu vết</em>.</h1>
              <p className="lead">Mở hồ sơ, đọc biên bản, đối chiếu từng lời khai và nối manh mối bằng dây đỏ. Không có người dẫn chuyện, không có đáp án dọn sẵn: chỉ có bạn và sự thật bị giấu trong giấy tờ.</p>
              <div className="hero__cta">
                <Link className="btn btn--primary" to={featuredTo}>Mở hồ sơ đầu tiên</Link>
                <a className="btn btn--ghost" href="#how">Xem cách chơi</a>
              </div>
              <dl className="hero__stats">
                <div><dt>Người chơi</dt><dd>1–6</dd></div>
                <div><dt>Mỗi vụ án</dt><dd>60–120 phút</dd></div>
                <div><dt>Tối ưu cho</dt><dd>iPad &amp; Apple Pencil</dd></div>
              </dl>
            </div>
            <div className="desk" aria-hidden="true">
              <div className="desk__paper desk__paper--a">
                <p className="desk__kicker">Biên bản khám nghiệm</p>
                <span className="bar w90" /><span className="bar w70" /><span className="bar w80" />
                <span className="bar w60 hl" /><span className="bar w85" /><span className="bar w40" />
              </div>
              <div className="desk__paper desk__paper--b">
                <p className="desk__kicker">Lời khai nhân chứng</p>
                <ol className="desk__lines">
                  <li><b>011</b><span className="bar w80" /></li>
                  <li><b>012</b><span className="bar w65" /></li>
                  <li className="is-circled"><b>013</b><span className="bar w90" /></li>
                  <li><b>014</b><span className="bar w55" /></li>
                </ol>
              </div>
              <div className="desk__photo"><div className="desk__photo-img" /><p>Hiện trường · 23:15</p></div>
              <div className="desk__note">Ai biết mã két?</div>
              <span className="stamp desk__stamp">Mật</span>
              <svg className="desk__string" viewBox="0 0 400 300" preserveAspectRatio="none"><path d="M70 80 Q 200 190 330 120" /><path d="M330 120 Q 300 230 160 250" /></svg>
            </div>
          </div>
        </section>

        <section id="catalog" className="section">
          <div className="wrap">
            <div className="section__head">
              <div>
                <p className="eyebrow">Kho hồ sơ</p>
                <h2>Chọn vụ án để điều tra</h2>
              </div>
              <div className="chips" role="tablist" aria-label="Lọc hồ sơ">
                {FILTERS.map((f) => (
                  <button key={f.id} type="button" role="tab" aria-selected={filter === f.id} className={`chip${filter === f.id ? ' is-on' : ''}`} onClick={() => setFilter(f.id)}>{f.label}</button>
                ))}
              </div>
            </div>
            <div className="catalog">
              {error ? <p className="catalog__empty">Không tải được kho hồ sơ.</p>
                : !cases ? <p className="catalog__empty">Đang tải hồ sơ…</p>
                  : list.length ? list.map((c) => <CaseCard key={c.id} entry={c} />)
                    : <p className="catalog__empty">Chưa có hồ sơ nào trong mục này.</p>}
            </div>
          </div>
        </section>

        <section id="how" className="section how">
          <div className="wrap">
            <p className="eyebrow">Cách chơi</p>
            <h2>Bốn bước từ hồ sơ đến hung thủ</h2>
            <ol className="steps">
              <li><span className="steps__no">01</span><h3>Đọc hồ sơ</h3><p>Bài báo, biên bản hiện trường, lời khai, ảnh chụp, hoá đơn… Mọi tài liệu nằm trên bàn điều tra, kéo thả và phóng to tuỳ ý.</p></li>
              <li><span className="steps__no">02</span><h3>Ghi chép như thật</h3><p>Viết tay bằng Apple Pencil lên tài liệu, tô dạ quang, căng dây đỏ, dán giấy ghi chú và trích dẫn vào sổ tay điều tra.</p></li>
              <li><span className="steps__no">03</span><h3>Giải từng trọng điểm</h3><p>Ghim bằng chứng, chỉ ra dòng khai man, chọn kết luận. Giải xong mỗi trọng điểm, hồ sơ mới được mở niêm phong.</p></li>
              <li><span className="steps__no">04</span><h3>Gọi tên hung thủ</h3><p>Kết luận cuối cùng cùng lời giải chi tiết. Bị kẹt? Gợi ý được mở dần từng nấc, không lộ đáp án.</p></li>
            </ol>
          </div>
        </section>

        <section className="section features">
          <div className="wrap features__grid">
            <article className="feature"><h3>Viết tay trên iPad</h3><p>Nét bút cảm ứng lực nhấn của Apple Pencil, bám theo tài liệu khi kéo và xoay. Ngón tay để di chuyển, bỏ qua lòng bàn tay.</p></article>
            <article className="feature"><h3>Chơi cùng bạn bè</h3><p>Chia tài liệu cho từng người, tranh luận và cùng đi đến kết luận. Hợp cho buổi tối cuối tuần.</p></article>
            <article className="feature"><h3>Bối cảnh Việt Nam</h3><p>Phố cũ, khu tập thể, miền sông nước, những cái Tết. Mỗi hồ sơ là một câu chuyện độc lập, công bằng với người chơi.</p></article>
          </div>
        </section>

        <section id="faq" className="section faq">
          <div className="wrap faq__inner">
            <div><p className="eyebrow">Hỏi đáp</p><h2>Trước khi mở hồ sơ</h2></div>
            <div className="faq__list">
              {FAQ.map(([q, a]) => <details key={q}><summary>{q}</summary><p>{a}</p></details>)}
            </div>
          </div>
        </section>

        <section className="cta-band">
          <div className="wrap cta-band__inner">
            <h2>Hồ sơ đang chờ trên bàn.</h2>
            <Link className="btn btn--primary" to={featuredTo}>Bắt đầu điều tra</Link>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
