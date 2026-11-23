# Bước 4: Tạo hình ảnh và tang vật

> Gửi sau khi `case.json` đã hợp lệ. Thay `{{CASE_ID}}`. Có thể chỉnh "Phong cách" theo ý bạn.

---

Hãy tạo bộ hình ảnh cho hồ sơ `{{CASE_ID}}`. Đọc `authoring/{{CASE_ID}}/bible.md` (ngoại hình nhân vật, bối cảnh) và `public/cases/{{CASE_ID}}/case.json` (các trường `image` đang là `null`, cùng chú thích ảnh `caption` / `imageCaption`).

## Phần A: Viết `authoring/{{CASE_ID}}/image-prompts.md`

1. **Bảng phong cách chung** (dùng lại cho mọi ảnh để cả bộ đồng nhất):
   - Phong cách: {{ảnh chụp tư liệu hồ sơ điều tra, chân thực, ánh sáng tự nhiên hơi tối, hạt film nhẹ, tông màu ấm trầm, giống ảnh chụp bằng máy ảnh thật của thời điểm diễn ra vụ án}}
   - Thời đại và chất liệu: đồ vật, quần áo, xe cộ, biển hiệu phải đúng năm diễn ra vụ án và đúng vùng miền Việt Nam.
   - Câu phủ định dùng chung: không chữ, không logo, không watermark, không chữ ký, không người nổi tiếng, không máu me rõ.
2. **Hồ sơ nhân vật** (nếu có ảnh chân dung): mô tả cố định từng người (tuổi, khuôn mặt, kiểu tóc, trang phục đặc trưng) để mọi ảnh của cùng một người trông nhất quán.
3. **Danh sách ảnh**, với mỗi ảnh:
   - Tên file (ví dụ `d07-camera.webp`), tài liệu sử dụng, tỉ lệ khung hình.
   - Prompt đầy đủ (tiếng Anh cho mô hình ảnh), gồm: bảng phong cách, chủ thể, bố cục, góc máy, ánh sáng, và **chi tiết manh mối phải thấy rõ trong ảnh**.
   - Ghi chú kiểm tra: chi tiết nào bắt buộc đúng (ví dụ "đồng hồ treo tường chỉ 10 giờ 40", "mảnh kính nằm phía ngoài bậu cửa").
4. Ảnh bìa `cover.webp` tỉ lệ 4:5: một vật thể hoặc khung cảnh mang tính biểu tượng của vụ án, không lộ hung thủ.

## Phần B: Tạo ảnh

- Dùng công cụ tạo ảnh sẵn có của Antigravity, theo đúng từng prompt ở phần A.
- **Ảnh không được chứa chữ.** Mọi chữ (biển hiệu, giấy tờ, giờ trên camera) đều do trang web hiển thị. Nếu bắt buộc có giấy tờ trong ảnh, để giấy trắng hoặc nét chữ mờ không đọc được.
- Ảnh camera an ninh: góc cao, độ phân giải thấp, hơi nhoè, tông xanh xám, không có lớp chữ giờ.
- Ảnh tang vật: chụp trên nền trơn có thước đo hoặc thẻ số trống, ánh sáng đều.
- Không tạo ảnh thi thể rõ mặt hay vết thương ghê rợn. Chỉ gợi ý (bóng người phủ khăn, vệt đánh dấu trên sàn…).
- Lưu vào `public/cases/{{CASE_ID}}/images/` dưới dạng `.webp`, cạnh dài tối đa 1600px, mỗi file dưới 400 KB. Nếu công cụ trả về PNG/JPG, hãy chuyển sang WebP (ví dụ bằng `cwebp -q 80 in.png -o out.webp` hoặc thư viện Pillow của Python).
- Tự xem lại từng ảnh. Nếu chi tiết manh mối không thấy rõ, hoặc ảnh có chữ lỗi, hãy tạo lại.

## Phần C: Gắn ảnh vào hồ sơ

1. Cập nhật các trường `image` trong `case.json` thành `"images/<tên-file>.webp"`, và `cover` trong cả `case.json` lẫn `public/cases/index.json`.
2. Nếu ảnh thực tế khác mô tả (khác góc, khác chi tiết), sửa `caption`/`imageCaption` cho khớp. **Không** để chú thích nói điều ảnh không thể hiện.
3. Chạy `node tools/validate-case.mjs {{CASE_ID}}`: không còn lỗi, không còn cảnh báo thiếu ảnh.
4. Báo lại: danh sách ảnh đã tạo, ảnh nào phải tạo lại nhiều lần, và ảnh nào bạn chưa hài lòng.
