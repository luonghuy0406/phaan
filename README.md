# Hồ Sơ Mật: website game phá án

Kho nhiều hồ sơ vụ án, chơi trên một "bàn điều tra" chung trong trình duyệt. Tối ưu cho iPad và Apple Pencil.

## Chạy thử

```bash
npm install
npm run dev          # http://localhost:5173
```
Lệnh `dev` mở sẵn cho mạng nội bộ: trên iPad cùng Wi-Fi, mở địa chỉ "Network" mà Vite in ra (ví dụ `http://192.168.1.20:5173`).

> Nếu `npm install` báo lỗi quyền với thư mục `~/.npm` (do từng chạy npm bằng sudo), sửa một lần bằng:
> `sudo chown -R $(id -u):$(id -g) ~/.npm`

| Lệnh | Việc |
|---|---|
| `npm run validate` | Kiểm định mọi hồ sơ trong `public/cases/` |
| `npm test` | Unit test (hình học xoay tài liệu, nét bút, kiểm tra đáp án, lọc dữ liệu lưu) |
| `npm run build` | Bản production vào `dist/` |

## Chơi nhóm (Supabase)

- Đăng nhập bằng mã một lần qua email (không mật khẩu). Chủ phòng tạo phòng từ trang hồ sơ → nhận **mã mời 6 số** (hết hạn sau 30 phút, đổi được) và **mã QR**.
  Người chơi quét QR hoặc nhập mã ở `/tham-gia`.
- Chia sẻ theo thời gian thực: kết luận, bằng chứng đang ghim, dòng khai đang chọn, gợi ý, sổ tay nhóm, ai đang online, nhật ký hoạt động.
  Bàn giấy, nét bút, giấy ghi chú và sổ tay cá nhân là của riêng mỗi người.
- Server chấm đáp án (hàm `submit_answer`), nên cả nhóm luôn cùng một tiến trình.
- Thiết kế database: `supabase/migrations/20261123000000_multiplayer.sql` (bảng, RLS, hàm, realtime).
- Sau mỗi lần sửa câu hỏi của một hồ sơ: `npm run sync-cases` (nạp đáp án lên server, dùng `SUPABASE_SECRET_KEY` trong `.env.local`).
- Mời người chơi qua mạng LAN khi chủ phòng mở trang bằng `localhost`: đặt `VITE_PUBLIC_URL=http://<ip-máy>:5173` trong `.env.local` để mã QR trỏ đúng.
- Bật `requireLoginForSolo` trong `src/lib/config.ts` nếu muốn bắt đăng nhập cả khi chơi một mình.

## Tài khoản & lưu tiến độ
- Đăng nhập bằng mã email, hoặc SSO (Google, Apple, Facebook, Microsoft, GitHub, Discord). Nút SSO tự hiện khi nhà cung cấp được bật trong Supabase.
- Đã đăng nhập: tiến độ, cách bày bàn, nét bút, giấy ghi chú, sổ tay **tự lưu lên cloud** (bảng `user_progress`) và mở tiếp được trên thiết bị khác.
  Bản nào mới hơn thì thắng. Chưa đăng nhập thì vẫn lưu trên máy như trước.
- Trang `/tai-khoan`: hồ sơ đang chơi, phòng đang tham gia (vào lại / rời phòng), phòng đã phá án, đổi tên hiển thị.
  Trang chủ có mục "Tiếp tục điều tra", trang hồ sơ có nút "Vào lại phòng" / "Tiếp tục một mình (x/y)".

## Trang chủ, PWA & cài lên màn hình chính
- Trang chủ dùng **GSAP + ScrollTrigger** (`src/pages/Home.tsx`, `src/styles/home.css`):
  - mở đầu: chữ hiện theo từng từ, ảnh tang vật bay vào, dây đỏ tự kéo, bàn nghiêng theo chuột;
  - dải chữ chạy, kho hồ sơ hiện dần khi cuộn;
  - "Cách chơi" ghim màn hình trên máy lớn, xếp dọc trên điện thoại;
  - tính năng có nét bút tự vẽ và thông báo đồng đội.

  Người dùng bật "giảm chuyển động" sẽ thấy bản tĩnh.
- Ảnh trang chủ ở `public/site/`. Bộ ảnh riêng chờ tạo bằng FLUX: `authoring/site/image-prompts.md`.
- **PWA** (`vite-plugin-pwa`): lưu sẵn khung ứng dụng; hồ sơ và ảnh đã mở dùng được khi mất mạng. Supabase không bị lưu tạm.
  Mỗi lần deploy, bản mới tự cập nhật ở lần mở sau.
- **Gợi ý cài đặt** (`src/components/install.tsx`):
  - Android/Chrome: hiện nút "Cài đặt" thật;
  - iPhone/iPad: hướng dẫn qua nút Chia sẻ (nhận cả iPad đang báo mình là Mac);
  - Zalo/Facebook/Instagram: hướng dẫn mở bằng trình duyệt trước.

  Tự hiện sau 12 giây hoặc khi cuộn quá 1 màn hình. Không hiện khi đã cài hay đang chơi. Bấm "Để sau" thì ẩn 14 ngày.
  Chân trang luôn có link "Cài ứng dụng lên màn hình chính".

## Trang
| Đường dẫn | Nội dung |
|---|---|
| `/` | Trang chủ: giới thiệu, kho hồ sơ, cách chơi, hỏi đáp |
| `/ho-so/:id` | Chi tiết một hồ sơ |
| `/choi/:id` | Bàn điều tra (một mình) |
| `/dang-nhap` | Đăng nhập bằng mã email hoặc SSO |
| `/tai-khoan` | Tài khoản, hồ sơ đang chơi, phòng đã tham gia |
| `/tham-gia?ma=` | Nhập mã mời 6 số / mở từ QR |
| `/phong/:roomId` | Sảnh chờ: mã mời, QR, thành viên |
| `/phong/:roomId/choi` | Bàn điều tra của nhóm |

## Bàn điều tra
- **Apple Pencil luôn viết** lên tài liệu, giấy ghi chú hoặc mặt bàn; **ngón tay di chuyển** và chụm để phóng to.
  Chạm lòng bàn tay khi đang viết sẽ bị bỏ qua. Nét bút có lực nhấn (`perfect-freehand`), bám theo tài liệu khi kéo hoặc xoay.
- Bút (3 màu, 3 cỡ), dạ quang, tẩy, hoàn tác / làm lại (⌘Z).
- **Chạm vào đoạn văn** để mở menu: tô dạ quang, trích vào Sổ tay, nối dây đỏ, ghim bằng chứng, chọn dòng khai.
- **Sổ tay điều tra**: trích dẫn kèm nguồn (bấm "Xem" để bay tới đúng đoạn), ghi chép tự do. Scribble của iPadOS hoạt động trong mọi ô chữ.
- Các vòng điều tra: nhãn vòng trên bàn, phong bì niêm phong cho từng vòng khoá, 4 bước hướng dẫn lần đầu, màn kết có phần kết mở rộng.
- Tiến trình, nét vẽ, sổ tay được lưu tự động trong IndexedDB của trình duyệt.
- Trên iPad: Safari → Chia sẻ → "Thêm vào màn hình chính" để chơi toàn màn hình.

## Thêm hoặc sửa vụ án
1. Làm theo `prompts/antigravity/README.md` (dùng AI Antigravity). Hồ sơ cũ: `prompts/antigravity/06-tai-cau-truc-ho-so.md`.
2. Đặc tả và nhịp vòng: `docs/case-schema.md`. Mẫu chuẩn: `public/cases/con-nuoc-ram-thang-gieng/`.
3. `npm run validate`.

## Tuỳ biến
- Tên thương hiệu: `src/lib/config.ts`, `index.html`, `public/manifest.webmanifest`.
- Màu sắc, font: `src/styles/tokens.css`.

## Deploy
`npm run build`, rồi đưa thư mục `dist/` lên Netlify, Vercel, Cloudflare Pages… Đã có sẵn cấu hình chuyển hướng cho ứng dụng
một trang (`public/_redirects`, `vercel.json`). Thư mục `authoring/` (chứa lời giải) không nằm trong `dist/`.

Đáp án nằm trong `case.json` nên người rành kỹ thuật vẫn xem được. Nếu sau này bán hồ sơ trả phí, cần chuyển đáp án của
các vòng trả phí sang API phía server (xem `docs/phan-tich-unsolvedcasevietnam.md`, mục 2.4).
