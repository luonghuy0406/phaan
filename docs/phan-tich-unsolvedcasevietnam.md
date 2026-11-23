# Phân tích kỹ thuật: unsolvedcasevietnam.com

Ngày phân tích: 2026-11-23. Nguồn: HTML/JS/CSS công khai tải từ trang (không gọi các API thanh toán).

> Lưu ý pháp lý: tài liệu này chỉ mô tả **cơ chế và kiến trúc** để tham khảo. Cốt truyện, nhân vật,
> hình ảnh, tên thương hiệu và mã nguồn của họ là tài sản của họ: đừng sao chép vào game của bạn.
> Hãy tự viết vụ án, tự vẽ tài liệu và tự viết code.

## 1. Tổng quan

| Hạng mục | Thực tế quan sát được |
|---|---|
| Kiểu site | Site tĩnh, HTML + JavaScript thuần (không framework, không bundler, không minify) |
| Animation | GSAP + ScrollTrigger (landing page) |
| Font | Be Vietnam Pro (chữ thường), Old Standard TT (kiểu giấy tờ cũ) |
| Ảnh | `.webp`, có 2 mức: ảnh preview và ảnh nét (`data-hi`), ảnh nét chỉ tải khi zoom đủ gần |
| Backend | Serverless dạng `/api/*` (có thể là Vercel vì có `api/_lib/...`): mở khoá, thanh toán payOS, đổi mã |
| Analytics | `track.js` gom sự kiện chuẩn GA4 rồi phát cho GA4, PostHog, Meta Pixel (+ CAPI phía server) |
| A/B test | PostHog feature flag cho giá paywall (`control` / `after-2`) |
| Lưu tiến trình | `localStorage`, có `sanitizeState()` lọc dữ liệu vì coi localStorage là input không tin cậy |

### Các trang
- `index.html`: landing (hero, showcase vụ án 4 chương, trải nghiệm, cách chơi, đánh giá, mua hàng, FAQ).
- `case-01.html?format=box|online`, `case-02.html`: trang sản phẩm / ưu đãi.
- `casefile-tap01.html`: **bản chơi online**, bàn điều tra (phần quan trọng nhất).
- `files.html`: tải hồ sơ để in. `blog/`: bài SEO.

## 2. Lõi game: "Bàn điều tra" (`case-canvas.js`, ~2.800 dòng)

### 2.1 Mô hình trang (khai báo bằng `data-*`)
```html
<main data-case-canvas data-config="#case-json">
  <div data-cc-viewport>              <!-- mặt bàn kéo/zoom được -->
    <div data-cc-world>
      <article class="cc-doc" data-doc="d01" data-stage="1" data-title="…"
               data-x="0" data-y="0" data-evidence="nhom" data-foldable> … </article>
      <svg data-cc-strings></svg>     <!-- dây đỏ nối manh mối -->
      <div data-cc-notes></div>       <!-- giấy nhớ -->
    </div>
  </div>
  <nav data-cc-index></nav>           <!-- danh sách tài liệu -->
  <aside data-cc-panel><div data-cc-questions></div></aside>
  <div data-cc-toolbar>…</div>
</main>
```
Trong tài liệu: `data-key` (điểm neo dây / tô sáng), `data-hl` (tô sáng được), `data-line="038"`
(dòng lời khai chọn được), `data-box`/`data-code` (giải mã bằng cách gập giấy chồng lên nhau).

Ý hay: **nội dung vụ án là HTML thuần, engine đọc thuộc tính**. Người viết vụ án không cần sửa code.

### 2.2 Cơ chế chơi
| Cơ chế | Cách làm |
|---|---|
| Mặt bàn vô hạn | camera `{x, y, zoom}` từ 0.12 đến 2.5, zoom quanh con trỏ (`zoomAt`), `fitAll`, `flyTo` có easing |
| Tài liệu | kéo thả, đưa lên trên (z-index), xoay 90° (phím R), gập/mở |
| Dây đỏ | SVG path có độ võng giữa 2 neo (tài liệu, một `data-key` cụ thể, hoặc giấy nhớ), tối đa 80 dây |
| Bút dạ quang | tô `data-hl` hoặc kéo khung, lưu theo **tỉ lệ 0..1** của tờ giấy nên không lệch khi đổi màn hình |
| Giấy nhớ | tối đa 40 tờ, 600 ký tự |
| Ghim bằng chứng | ghim N tài liệu vào ô (slot) để trả lời |
| Gập & khớp (dock) | gập tờ "dải mã" rồi đặt khớp lên tờ đích thì các ô số được giải mã |
| Tour hướng dẫn | `config.tour`: các bước gắn với tài liệu, có chữ riêng cho chuột/cảm ứng |
| Tải ZIP | tự tạo file ZIP ngay trên trình duyệt (tự viết CRC32), chia thư mục theo "Trọng điểm" |

### 2.3 Hệ thống câu hỏi (thuần, có unit test)
- `evidence`: ghim đúng tập tài liệu. Có `nudges` (`picks` khớp chính xác, `any` chứa một trong) và `near` = "gần đúng".
- `line`: chọn đúng số dòng trong biên bản, chuẩn hoá về 3 chữ số, có nudge riêng cho từng dòng sai.
- `choice`: trắc nghiệm một hoặc nhiều đáp án; không có option thì là bước "xem đáp án".
- Mỗi câu có `hints[]` (gợi ý dần, đếm số lần dùng), `tries`, `explanation[]` (lời giải theo mục).

### 2.4 Mở khoá theo giai đoạn ("Trọng điểm")
- Tài liệu có `data-stage="N"` và chỉ hiện khi câu N-1 đã giải. Giai đoạn đóng hiện "phong bì niêm phong" (`data-cc-seal`).
- Câu hỏi phải giải **theo thứ tự**: `sanitizeState` không cho câu sau "solved" nếu câu trước chưa giải.
- Giai đoạn trả phí: **đáp án không nằm trong HTML**, lấy từ `GET /api/case/<id>-premium`
  (200 = có dữ liệu, 402 = chưa trả). Cách này chống xem trộm đáp án trong source. Nên học theo.

### 2.5 Kiếm tiền
Freemium: chơi miễn phí vài trọng điểm, sau đó paywall. `POST /api/pay/create` trả `checkoutUrl` (payOS);
hoặc `POST /api/pay/redeem {code}` (mã in trong hộp boardgame, giới hạn số thiết bị, lỗi `CODE_LIMIT_REACHED`).
Kèm upsell sang vụ tiếp theo (`case-upsell.js`) và bán hộp vật lý qua Shopee/TikTok.

### 2.6 State lưu (localStorage, version 1)
```js
{ v: 1,
  docs:   { d01: { x, y, z, folded, turn: 0..3, docked } },
  notes:  [{ id, x, y, z, text }],
  strings:[{ id, a: {doc,key?}|{note}, b: … }],
  hl: ["key", …],  marks: [{ id, doc, x, y, w, h }],   // tỉ lệ 0..1
  pins: ["nhom", null],
  q: { s1: { solved, hints, tries, line, pick: [] } },
  cam: { x, y, z, w, h }, seenIntro }
```

## 3. Gợi ý kiến trúc cho game của bạn

Giữ lại các **ý tưởng kỹ thuật** đã chứng minh hiệu quả, và tạo khác biệt ở nội dung và gameplay:

1. **Tách engine và dữ liệu vụ án**: mỗi vụ là một thư mục `cases/<id>/` gồm `case.json` (meta, câu hỏi
   free, tour) và tài liệu (HTML/Markdown/ảnh). Engine chung đọc vào và dựng bàn điều tra.
2. **Stack đề xuất**: Vite + TypeScript. Bàn điều tra có thể dùng DOM + CSS transform như họ (đơn giản, chữ
   sắc nét, dễ truy cập), hoặc PixiJS/Konva nếu cần hiệu ứng nặng. Backend: Supabase hoặc Cloudflare Workers.
3. **Đáp án trả phí kiểm tra ở server**, không gửi đáp án xuống client trước khi mở khoá.
4. **Logic kiểm tra đáp án là hàm thuần** + unit test (Vitest), như `checkEvidence/checkLine/checkChoice`.
5. **Lưu state có version + sanitize**, sau thêm đồng bộ tài khoản (cloud save).
6. **Hướng khác biệt có thể làm**:
   - Chơi nhóm realtime (nhiều người cùng một bàn, con trỏ và dây đỏ đồng bộ), phù hợp "chơi cùng bạn bè".
   - Thẩm vấn nhân chứng dạng hội thoại phân nhánh, hoặc thẩm vấn bằng AI có giới hạn theo hồ sơ.
   - Dòng thời gian (timeline) kéo thả sự kiện, bản đồ hiện trường, đối chiếu dấu vân tay / camera.
   - Trình soạn vụ án (case editor) để bạn hoặc cộng đồng tự tạo vụ.
   - Bảng xếp hạng theo thời gian / số gợi ý đã dùng.

## 4. Hạn chế của lần phân tích này
- Không chạy được REA CLI: `rea-agents@6.10.1` cần Node ≥ 22.23.4 / 24.22.1 / 26.12.1, máy đang có 22.19.0.
  Code của trang không minify nên đã đọc trực tiếp.
- Không xem được mã backend (`/api/*`): chỉ suy ra hợp đồng API từ code phía client.
- Không gọi thử API thanh toán / mở khoá.
