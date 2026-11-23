# Bước phụ: Tái cấu trúc một hồ sơ đã có theo nhịp 5 vòng

> Dùng cho hồ sơ viết theo cấu trúc cũ (ví dụ `mua-dong-binh-ty`: 18 tài liệu, 4 vòng). Thay `{{CASE_ID}}`.
> Lưu ý: đổi cấu trúc sẽ làm người đã chơi hồ sơ này phải bắt đầu lại.

---

Hãy tái cấu trúc hồ sơ `{{CASE_ID}}` theo **nhịp vòng khuyến nghị** trong `docs/case-schema.md` (mục 0).

**Đọc trước:**
- `docs/case-schema.md`, nhất là mục 0.
- `authoring/con-nuoc-ram-thang-gieng/bible.md`, mục 8: ví dụ đã tái cấu trúc từ 16 tài liệu / 4 vòng thành 26 tài liệu / 5 vòng, kèm bảng mã cũ → mã mới và lý do từng thay đổi.
- `public/cases/con-nuoc-ram-thang-gieng/case.json`: kết quả đang chạy được.
- `authoring/{{CASE_ID}}/bible.md` và `public/cases/{{CASE_ID}}/case.json`: hồ sơ cần làm.

**Yêu cầu:**
1. **Giữ nguyên sự thật vụ án**: hung thủ, thủ đoạn, động cơ, dòng thời gian. Không đổi cốt truyện.
2. Giữ mọi tài liệu cũ (chỉ sửa lỗi nếu phát hiện). Thêm tài liệu mới để đủ khoảng 24–30 tài liệu, chia 5 vòng giảm dần (~8 → 7 → 5 → 3 → 3).
   Tài liệu mới nên là: lời khai người phát hiện / nhân chứng phụ, giấy tờ xác nhận ngoại phạm cho từng nghi phạm vô tội,
   giám định bổ sung, sổ tay hiện trường. Mỗi tài liệu mới phải khớp dòng thời gian trong bible.
3. Câu hỏi: vòng 1 là `choice` **2 lựa chọn** để làm quen; vòng cuối là `choice` 4 phương án. Mỗi câu 3 gợi ý, lời giải 3 ý,
   ít nhất 2 `nudges` cho đáp án sai phổ biến. Tránh câu hỏi có hai bộ đáp án cùng hợp lý (nếu có, siết lại `prompt`).
4. Đánh lại mã tài liệu `d01`… theo thứ tự đọc. Mọi tham chiếu trong câu hỏi phải dùng mã mới.
5. Thêm `epilogue` (3–4 mục) và cập nhật `duration` trong cả `case.json` lẫn `public/cases/index.json`.
6. **Rà lỗ hổng cốt truyện** trong bản cũ: vật chứng xuất hiện ở nơi hung thủ không thể có mặt, dòng trùng lặp, mốc giờ lệch. Báo lại từng lỗi trước khi sửa.
7. Viết mục "Bản chơi 5 vòng" vào cuối `authoring/{{CASE_ID}}/bible.md`, theo mẫu mục 8 của hồ sơ 1 (bảng mã cũ → mới, câu hỏi, lỗi đã sửa, ảnh cần tạo).
8. Tài liệu mới cần ảnh thì để `"image": null` và thêm prompt vào `authoring/{{CASE_ID}}/image-prompts.md`.
9. Chạy `npm run validate` (không lỗi) và `npm run dev`, rồi chơi thử hết 5 vòng tại `http://localhost:5173/choi/{{CASE_ID}}`.

Báo lại: số tài liệu mỗi vòng, 5 câu hỏi kèm đáp án, danh sách tài liệu mới, và các lỗi cốt truyện đã sửa.
