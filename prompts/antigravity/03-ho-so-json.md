# Bước 3: Viết toàn bộ hồ sơ thành `case.json`

> Gửi sau khi đã duyệt `authoring/{{CASE_ID}}/bible.md`. Thay `{{CASE_ID}}` và `{{SO}}`.

---

Dựa trên `authoring/{{CASE_ID}}/bible.md`, hãy viết hồ sơ hoàn chỉnh vào `public/cases/{{CASE_ID}}/case.json`.

**Đọc trước:**
- `docs/case-schema.md`: đặc tả đầy đủ các trường. Làm đúng tuyệt đối.
- `public/cases/con-nuoc-ram-thang-gieng/case.json`: hồ sơ mẫu 5 vòng đang chạy được. Bắt chước cấu trúc và nhịp vòng, **không** bắt chước nội dung.
- `src/board/papers.tsx`: xem mỗi loại tài liệu hiển thị những trường nào.

**Yêu cầu chung:**
- `"id": "{{CASE_ID}}"`, `"no": {{SO}}`, `"status": "available"`.
- `synopsis`: 2 đoạn giới thiệu gây tò mò, **không lộ** hung thủ hay manh mối then chốt.
- `intro.objective`: một câu nhiệm vụ rõ ràng.
- Mọi ảnh để `"image": null` ở bước này (bước 4 sẽ tạo ảnh). Chỉ đặt trường `image` cho tài liệu thực sự cần ảnh.
- Không viết thẻ HTML. Chỉ dùng `**đậm**`, `__gạch chân__`, `~~gạch xoá~~`. Không lạm dụng in đậm: in đậm chi tiết then chốt là làm lộ manh mối. Chỉ in đậm những gì một cán bộ thật sẽ in đậm trên giấy tờ.

**Viết từng tài liệu như giấy tờ thật:**
- `report` (biên bản): văn phong hành chính, ngắn gọn, có số hiệu, giờ lập, người lập. `header` là tên cơ quan **hư cấu**, ví dụ "Công an quận Gác Chuông".
- `testimony` (lời khai): văn nói tự nhiên, có ngập ngừng, có chi tiết thừa giống người thật. Manh mối nằm lẫn trong dòng bình thường, không đứng riêng một dòng "đáng ngờ". Đánh số dòng `n` liên tục từ 1.
- `newspaper`: giọng báo chí, có thể đưa tin sai hoặc thiếu (báo chí dễ bị dắt mũi).
- `letter`, `note`: giọng riêng của từng nhân vật, nhất quán với tính cách trong bible.
- `receipt`, `evidence`: số liệu chính xác, khớp dòng thời gian.

**Câu hỏi (`questions`):**
- Đúng thứ tự và đúng trọng điểm như bible.
- Đúng nhịp vòng của `docs/case-schema.md` (mục 0). Câu vòng 1 là `choice` 2 lựa chọn.
- Mỗi câu có 3 gợi ý: (1) chỉ hướng tới loại tài liệu cần đọc lại, (2) chỉ ra chi tiết cần đối chiếu, (3) gần như nói thẳng đáp án.
- `nudges`: dự đoán **ít nhất 2 câu trả lời sai phổ biến** cho mỗi câu, với lời nhắn giải thích vì sao sai mà không lộ đáp án. Câu trả lời "đúng một nửa" thì đặt `"near": true`.
- `solved`: 1–2 câu tóm tắt lý do đúng, và báo trọng điểm tiếp theo đã mở (nếu có).
- `explanation`: lời giải chi tiết theo từng ý, trích dẫn tài liệu bằng số hiệu (ví dụ "Tài liệu 04, dòng 007").
- Câu `choice` cuối: 4 phương án, mỗi phương án là một giả thuyết đủ hợp lý (không có phương án "cho có").

**`finale`** và **`epilogue`**: lấy từ mục 7 của bible. Có thể thêm `tour` (4 bước hướng dẫn) nếu hồ sơ có thao tác đặc biệt.
- Đánh mã tài liệu `d01`, `d02`… **theo đúng thứ tự đọc** trong danh sách, để mã trùng số hiển thị.

**Sau khi viết xong:**
1. Thêm mục cho hồ sơ vào `public/cases/index.json` (các trường `id, no, status, title, tagline, difficulty, players, duration, setting, tags, cover`), giữ nguyên các hồ sơ khác. Nếu đang có mục giữ chỗ "đang biên soạn" cùng số `no`, thay thế mục đó.
2. Chạy `node tools/validate-case.mjs {{CASE_ID}}`. Sửa **hết** lỗi (✗). Cảnh báo thiếu ảnh (!) là bình thường ở bước này.
3. Báo lại cho tôi: số tài liệu theo từng trọng điểm, danh sách câu hỏi kèm đáp án, và mọi chỗ bạn phải lệch khỏi bible (kèm lý do).
