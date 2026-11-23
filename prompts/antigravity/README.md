# Bộ prompt Antigravity: tạo một hồ sơ vụ án mới

Quy trình 5 bước. Mỗi bước là một prompt riêng, dán vào khung chat agent của Antigravity khi đã mở thư mục dự án
`game_pha_an`. Làm xong, đọc và duyệt kết quả từng bước rồi mới sang bước sau: lỗi ở kịch bản gốc sẽ lan ra toàn bộ hồ sơ.

| Bước | File prompt | Kết quả |
|---|---|---|
| 1 | `01-y-tuong.md` | 3 ý tưởng vụ án để bạn chọn |
| 2 | `02-kich-ban-goc.md` | `authoring/<id>/bible.md`: sự thật, nhân vật, dòng thời gian, chuỗi manh mối |
| 3 | `03-ho-so-json.md` | `public/cases/<id>/case.json`: toàn bộ tài liệu, câu hỏi, gợi ý, lời giải |
| 4 | `04-hinh-anh.md` | `authoring/<id>/image-prompts.md` + ảnh trong `public/cases/<id>/images/` |
| 5 | `05-kiem-dinh-va-dang.md` | Chơi thử, sửa lỗi, đăng lên kho hồ sơ |
| phụ | `06-tai-cau-truc-ho-so.md` | Đưa một hồ sơ cũ về nhịp 5 vòng (mẫu: hồ sơ 1) |

## Trước khi bắt đầu
- Antigravity có thể tự đọc `AGENTS.md` ở thư mục gốc. Nếu không, hãy dán nội dung file đó vào phần Rules của workspace.
- Thay các chỗ `{{...}}` trong prompt trước khi gửi:
  - `{{CASE_ID}}`: mã thư mục, chữ thường không dấu, ví dụ `chung-cu-hoa-sen`
  - `{{SO}}`: số hồ sơ, ví dụ `1`
  - các trường khác được ghi chú ngay trong prompt
- Nên dùng mô hình mạnh nhất có sẵn cho bước 2 và 3 (phần cần suy luận chặt chẽ nhất).

## Mẹo
- Bước 2 là quan trọng nhất. Hãy tự "chơi" bible.md trong đầu: nếu bạn không thấy chuỗi suy luận hợp lý thì người chơi cũng không thấy.
- Nếu agent viết quá dài, yêu cầu "rút gọn, giữ nguyên mọi manh mối". Một hồ sơ 90 phút thường có 14–22 tài liệu.
- Lưu `authoring/` vào git nhưng **không** deploy thư mục đó lên hosting (nó chứa lời giải).
