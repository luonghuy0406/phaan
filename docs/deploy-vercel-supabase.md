# Triển khai Hồ Sơ Mật lên Vercel + Supabase

Danh sách việc cần làm, theo đúng thứ tự. Đánh dấu `[x]` khi xong.

- **Vercel** phục vụ trang web tĩnh (thư mục `dist/` sau khi build).
- **Supabase** lo đăng nhập, database, realtime.

Không cần Next.js, không cần server riêng.

> Trạng thái ngày 24/11/2026: **Phần A đã xong.** Đã tạo bảng qua MCP, nạp đáp án 8 hồ sơ (30 câu), và kiểm tra luồng
> chơi nhóm ngay trong database (25 bước, dữ liệu thử đã huỷ). Còn lại: Phần B (email, SMTP, đổi khoá), rồi C–F.

---

## Phần A. Tạo database trên Supabase

### A1. Phê duyệt và đăng nhập MCP Supabase (để Claude tạo bảng giúp bạn)
- [x] Mở Terminal, vào thư mục dự án: `cd ~/Documents/game_pha_an`
- [x] Chạy `claude`. Khi được hỏi, **chấp nhận** server `supabase` (khai báo trong `.mcp.json`).
- [x] Gõ `/mcp`, chọn `supabase`, chọn **Authenticate**, rồi đăng nhập tài khoản Supabase trên trình duyệt.
- [x] Nhắn Claude: *"MCP Supabase đã kết nối, hãy áp dụng migration và chạy thử chơi nhóm"*.

**Cách khác (không dùng MCP):** vào Supabase Dashboard → **SQL Editor** → New query, dán toàn bộ nội dung file
`supabase/migrations/20261123000000_multiplayer.sql`, rồi bấm **Run**.

### A2. Nạp đáp án các hồ sơ lên server
- [x] Trong thư mục dự án: `npm run sync-cases`
- [ ] Kết quả mong đợi: mỗi hồ sơ một dòng `✓ <tên-hồ-sơ>: N câu hỏi`.
- [ ] **Chạy lại lệnh này mỗi khi sửa câu hỏi hoặc đáp án** của bất kỳ hồ sơ nào. Nếu không, server sẽ chấm theo đáp án cũ.

> Lệnh này dùng `SUPABASE_SECRET_KEY` trong `.env.local`. Chỉ chạy trên máy của bạn, không đưa lên Vercel.

---

## Phần B. Cấu hình Supabase Dashboard

### B1. Email đăng nhập có mã số
Authentication → **Email Templates** → **Magic Link**: thêm dòng có `{{ .Token }}`, ví dụ:

```html
<h2>Mã đăng nhập Hồ Sơ Mật</h2>
<p>Mã của bạn: <strong style="font-size:24px;letter-spacing:4px">{{ .Token }}</strong></p>
<p>Hoặc bấm vào đây để đăng nhập: <a href="{{ .ConfirmationURL }}">Đăng nhập</a></p>
<p>Mã có hiệu lực trong 1 giờ. Nếu bạn không yêu cầu, hãy bỏ qua email này.</p>
```

- [ ] Làm tương tự cho template **Confirm signup** (người đăng nhập lần đầu sẽ nhận email này).

### B2. Gửi email bằng SMTP riêng (bắt buộc khi có người chơi thật)
Email mặc định của Supabase chỉ gửi được vài thư mỗi giờ.
- [ ] Tạo tài khoản ở một dịch vụ gửi email (Resend, Brevo, SendGrid…), rồi xác minh tên miền gửi thư.
- [ ] Authentication → **SMTP Settings** → bật Custom SMTP, điền host, cổng, tài khoản, mật khẩu do dịch vụ đó cấp.
- [ ] Authentication → **Rate Limits**: nâng giới hạn gửi email cho phù hợp.

### B3. Đổi khoá secret
Khoá secret hiện tại đã bị dán vào khung chat, cần thay.
- [ ] Settings → **API Keys** → tạo secret key mới, rồi xoá khoá cũ (`sb_secret_oZ9S…`).
- [ ] Mở `.env.local`, thay giá trị `SUPABASE_SECRET_KEY` bằng khoá mới.
- [ ] Chạy lại `npm run sync-cases` để kiểm tra khoá mới hoạt động.

---

## Phần C. Đưa code lên GitHub

- [ ] Tạo repo **private** trên GitHub, ví dụ `ho-so-mat`.
- [ ] Trong thư mục dự án:
  ```bash
  git init
  git add .
  git status          # kiểm tra: KHÔNG được có .env.local trong danh sách
  git commit -m "Hồ Sơ Mật: bản đầu tiên"
  git branch -M main
  git remote add origin https://github.com/<tài-khoản>/ho-so-mat.git
  git push -u origin main
  ```
- [ ] Nếu `git status` có hiện `.env.local`: **dừng lại**, kiểm tra file `.gitignore` có dòng `.env*.local`.

> Thư mục `authoring/` (kịch bản có lời giải) và `prompts/` nằm trong repo private, nhưng **không** bị đưa lên web,
> vì Vercel chỉ phục vụ thư mục `dist/`.

---

## Phần D. Deploy lên Vercel

### D1. Tạo project
- [ ] vercel.com → **Add New… → Project** → chọn repo `ho-so-mat`.
- [ ] Framework Preset: **Vite**
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] Install Command: `npm install`

### D2. Biến môi trường
Vào Settings → **Environment Variables**, thêm cho cả Production và Preview:

| Tên | Giá trị |
|---|---|
| `VITE_SUPABASE_URL` | `https://ridpypfdsqgxnswrzfrf.supabase.co` |
| `VITE_SUPABASE_PUBLISHABLE_KEY` | `sb_publishable_…` (khoá publishable, công khai được) |
| `VITE_PUBLIC_URL` | tên miền thật, ví dụ `https://hosomat.vercel.app` (để mã QR và link mời trỏ đúng) |

- [ ] **KHÔNG** thêm `SUPABASE_SECRET_KEY` vào Vercel. Trang web không cần khoá này.
- [ ] Sau khi đổi biến môi trường: Deployments → **Redeploy** (biến `VITE_` được gắn vào lúc build).

### D3. Tên miền riêng (tuỳ chọn)
- [ ] Settings → **Domains** → thêm tên miền, rồi trỏ DNS theo hướng dẫn của Vercel.
- [ ] Cập nhật `VITE_PUBLIC_URL` sang tên miền mới, rồi Redeploy.

---

## Phần E. Nối Vercel với đăng nhập Supabase

Supabase → Authentication → **URL Configuration**:
- [ ] **Site URL**: tên miền chính, ví dụ `https://hosomat.vercel.app`
- [ ] **Redirect URLs**, thêm:
  - `https://hosomat.vercel.app/**` (tên miền chính)
  - `https://*-<tên-team>.vercel.app/**` (các bản preview của Vercel)
  - `http://localhost:5173/**` (chạy trên máy)
  - tên miền riêng (nếu có), dạng `https://<tên-miền>/**`

Thiếu bước này thì liên kết đăng nhập trong email sẽ đưa người chơi về sai trang. Nhập mã số vẫn chạy được.

---

## Phần F. Kiểm tra sau khi deploy

Dùng 2 thiết bị (ví dụ máy tính + iPad), hoặc 2 trình duyệt khác nhau:

- [ ] Trang chủ hiện đủ 3 hồ sơ, có ảnh bìa.
- [ ] Mở `https://<tên-miền>/phong/abc` rồi tải lại trang: không bị lỗi 404.
- [ ] **Chơi một mình:** vào một hồ sơ, giải được vòng 1, tải lại trang vẫn giữ tiến trình.
- [ ] **Đăng nhập:** nhận được email, nhập mã 6 số thì vào được. Thử cả bấm liên kết trong email.
- [ ] **Tạo phòng (thiết bị 1):** trang hồ sơ → "Chơi nhóm", sảnh chờ hiện mã 6 số, đồng hồ đếm ngược và mã QR.
- [ ] **Tham gia (thiết bị 2):** quét QR bằng camera, đăng nhập, rồi vào thẳng sảnh chờ. Thiết bị 1 thấy người mới, có chấm "Đang online".
- [ ] Chủ phòng bấm "Bắt đầu điều tra": cả hai thiết bị cùng vào bàn.
- [ ] Thiết bị 2 ghim một tài liệu: thiết bị 1 thấy thông báo và ô bằng chứng thay đổi.
- [ ] Thiết bị 1 giải đúng vòng 1: thiết bị 2 tự mở niêm phong vòng 2.
- [ ] Sổ tay → "Sổ nhóm": ghi chú của người này hiện ngay ở máy người kia.
- [ ] **iPad:** Safari → Chia sẻ → "Thêm vào màn hình chính". Mở từ biểu tượng, chơi toàn màn hình, Apple Pencil viết được, ngón tay di chuyển được.

Nếu một bước lỗi, mở Console của trình duyệt (trên máy tính) và Supabase → **Logs**, rồi gửi lỗi cho Claude.

---

## Phần G. Vận hành hằng ngày

| Việc | Cách làm |
|---|---|
| Thêm hoặc sửa hồ sơ | Làm theo `prompts/antigravity/README.md`, chạy `npm run validate`, rồi `npm run sync-cases`, rồi `git push` (Vercel tự deploy) |
| Xem trước trước khi phát hành | Đẩy lên một nhánh khác `main`: Vercel tạo bản preview riêng |
| Đổi tên thương hiệu | `src/lib/config.ts`, `index.html`, `public/manifest.webmanifest` |
| Xem ai đang chơi, phòng nào đang mở | Supabase → Table Editor → bảng `rooms`, `room_members` |

**Lưu ý:**
- Sửa nội dung chữ thì tiến trình người chơi được giữ nguyên.
- Thêm, bớt, đánh số lại tài liệu hoặc đổi đáp án thì người chơi phải bắt đầu lại hồ sơ đó.

---

## Phần H. Giới hạn cần biết

| Gói | Giới hạn chính | Khi nào cần nâng |
|---|---|---|
| Supabase Free | Tự **tạm dừng project sau ~1 tuần không ai dùng** (vào Dashboard bấm Restore). Giới hạn số kết nối realtime cùng lúc và dung lượng database | Khi mở cho người lạ chơi, hoặc không muốn bị tạm dừng: gói Pro |
| Vercel Hobby | Chỉ dành cho dự án **phi thương mại** | Khi bán hồ sơ hoặc chạy quảng cáo: gói Pro |

**Trước khi bán hồ sơ trả phí:**
- `case.json` (kể cả đáp án) đang công khai trên web.
- Cần chuyển đáp án và tài liệu của các vòng trả phí sang Supabase, chỉ trả về cho người đã mua.
- Bảng `case_questions` đã có sẵn làm nền cho việc này.
- Xem thêm `docs/phan-tich-unsolvedcasevietnam.md`, mục 2.4.
