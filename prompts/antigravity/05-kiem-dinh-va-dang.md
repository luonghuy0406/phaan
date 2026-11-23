# Bước 5: Chơi thử, kiểm định và đăng hồ sơ

> Gửi khi hồ sơ đã đủ chữ và ảnh. Thay `{{CASE_ID}}`.

---

Hãy kiểm định hồ sơ `{{CASE_ID}}` như một người chơi khó tính, rồi như một biên tập viên.

## 1. Kiểm tra kỹ thuật
- Chạy `node tools/validate-case.mjs {{CASE_ID}}`. Phải hợp lệ, không cảnh báo.
- Chạy `npm run dev`, mở trình duyệt tới:
  - `http://localhost:5173/`: hồ sơ hiện trong kho, bìa đúng.
  - `http://localhost:5173/ho-so/{{CASE_ID}}`: thông tin đúng, không lộ đáp án.
  - `http://localhost:5173/choi/{{CASE_ID}}`: chơi hết từ đầu đến cuối.
- Trên bàn điều tra: mọi ảnh hiện đúng, không tài liệu nào tràn chữ hoặc quá dài (lời khai > 18 dòng nên tách ra), các tài liệu của cùng một trọng điểm không chồng lên nhau quá xấu. Nếu cần, đặt `x`, `y`, `width` cho từng tài liệu.
- Kiểm tra cả màn hình hẹp (khoảng 400px).

## 2. Chơi thử "mù"
Giả vờ chưa từng đọc bible. Với mỗi trọng điểm, chỉ dùng tài liệu đang mở:
- Ghi lại chuỗi suy luận bạn dùng để trả lời. Nó có trùng với bible không?
- Có đáp án sai nào trông hợp lý ngang đáp án đúng không? Nếu có: thêm chi tiết loại trừ, hoặc thêm `nudges`.
- Câu hỏi có quá dễ (đọc một tài liệu là ra) hoặc quá khó (cần đoán) không?
- Gợi ý 1→2→3 có tăng dần hợp lý, và gợi ý 3 có đủ để người kẹt vượt qua không?

## 3. Biên tập
- Chính tả, dấu tiếng Việt, cách xưng hô nhất quán giữa các tài liệu.
- Ngày giờ, tuổi, số tiền, địa chỉ khớp nhau ở mọi nơi xuất hiện.
- `synopsis` và `intro` không tiết lộ manh mối.
- Không có tên người thật, thương hiệu thật, địa chỉ có thật cụ thể.

## 4. Báo cáo và sửa
Liệt kê mọi vấn đề tìm được theo mức độ (nghiêm trọng / nên sửa / nhỏ), đề xuất cách sửa, **hỏi tôi trước** những thay đổi ảnh hưởng tới cốt truyện, rồi sửa các lỗi còn lại.
Sau khi sửa, chạy lại validator và báo kết quả.

## 5. Đăng
Khi tôi xác nhận: kiểm tra `"status": "available"` ở cả `case.json` và `public/cases/index.json`, chạy lại validator lần cuối, rồi tóm tắt hồ sơ (tên, số tài liệu, số trọng điểm, thời lượng ước tính).
Nhắc tôi: khi deploy lên hosting, **không** đưa thư mục `authoring/` lên.
