# Bước 2: Viết kịch bản gốc (bible)

> Gửi sau khi đã chọn một ý tưởng ở bước 1. Thay `{{CASE_ID}}` và dán ý tưởng đã chọn (kèm chỉnh sửa của bạn, nếu có).

---

Chúng ta chọn ý tưởng sau:

```
{{DÁN Ý TƯỞNG ĐÃ CHỌN + GHI CHÚ CHỈNH SỬA CỦA BẠN}}
```

Hãy viết **kịch bản gốc** vào file `authoring/{{CASE_ID}}/bible.md`. Đây là tài liệu nội bộ chứa toàn bộ sự thật; mọi bước sau đều dựa vào nó. Viết bằng tiếng Việt, theo đúng các mục sau:

## 1. Tóm tắt sự thật
Một đoạn kể lại chính xác chuyện đã xảy ra: ai, làm gì, ở đâu, lúc nào, bằng cách nào, vì sao, và đã che giấu ra sao.

## 2. Nhân vật
Bảng gồm: họ tên (tên Việt tự nhiên, không trùng người nổi tiếng), tuổi, nghề, quan hệ với nạn nhân, động cơ bề ngoài, **bí mật thật**, chứng cứ ngoại phạm và việc nó đúng hay sai, đặc điểm ngoại hình (dùng cho ảnh ở bước 4).
Mỗi nghi phạm vô tội phải có một bí mật riêng khiến họ trông đáng ngờ, và một tài liệu cụ thể giúp loại trừ họ.

## 3. Dòng thời gian
Theo từng mốc giờ, từ vài ngày trước vụ án đến lúc hồ sơ được lập. Mỗi mốc ghi: sự kiện thật, ai biết, để lại dấu vết gì trên giấy tờ nào.

## 4. Bản đồ manh mối
Bảng: `manh mối | nằm ở tài liệu nào | chứng minh điều gì | cần đối chiếu với tài liệu nào`.
Quy tắc:
- Mọi kết luận quan trọng phải có **ít nhất 2 nguồn độc lập** cùng hướng tới.
- Mỗi mâu thuẫn phải nằm ở **chi tiết cụ thể, kiểm tra được** (giờ giấc, số liệu, thời tiết, đồ vật, cách xưng hô, chữ viết tay…), không phải cảm giác.
- Có 2–4 manh mối gây nhiễu (red herring); mỗi cái đều bị một tài liệu khác hoá giải.

## 5. Cấu trúc trọng điểm
Theo **nhịp vòng khuyến nghị** trong `docs/case-schema.md` (mục 0): 5 vòng, số tài liệu giảm dần (khoảng 8 → 7 → 5 → 3 → 3).
Vòng 1 là câu `choice` chỉ **2 lựa chọn** để người chơi làm quen (ví dụ: tai nạn hay án mạng?); vòng cuối là `choice` 4 phương án gọi tên hung thủ.
Mỗi nghi phạm vô tội phải có tài liệu ngoại phạm riêng (lời khai + giấy tờ xác nhận), thường ở vòng 2–3. Với từng trọng điểm:
- Danh sách tài liệu mở ra (đặt mã `d01`, `d02`… và loại: newspaper, report, testimony, photo, letter, receipt, evidence, note).
- Câu hỏi kết luận (loại `evidence`, `line` hoặc `choice`) và đáp án.
- Chuỗi suy luận người chơi cần đi qua, từng bước.
- Kiểm tra công bằng: chứng minh câu hỏi giải được **chỉ** bằng tài liệu đã mở tới trọng điểm đó.
Ưu tiên đa dạng loại câu hỏi: ít nhất 1 câu `evidence` và 1 câu `line`. Câu cuối cùng là `choice` gọi tên hung thủ kèm động cơ hoặc thủ đoạn.

## 6. Danh mục tài liệu
Với mỗi tài liệu: mã, loại, tiêu đề, trọng điểm, nội dung chính (gạch đầu dòng), manh mối cài bên trong, và cần ảnh hay không.
Mục tiêu: {{24–30}} tài liệu cho {{90–120}} phút chơi. Lời khai dài 6–16 dòng, mỗi dòng 1–2 câu văn nói.

## 7. Kết thúc
Lời kể lại toàn bộ sự thật dành cho màn kết thúc (3–6 đoạn), giọng điều tra viên khép hồ sơ.
Thêm 3–4 dòng "sau khi hồ sơ khép lại": số phận các nghi phạm vô tội và những gì còn lại (sẽ thành trường `epilogue`).

---

**Trước khi lưu file, tự kiểm tra và ghi kết quả vào cuối bible.md, mục "Tự kiểm tra":**
1. Có mốc giờ nào trong dòng thời gian mâu thuẫn với nhau không?
2. Có câu hỏi nào cần thông tin chưa có trên bàn ở trọng điểm đó không?
3. Có cách giải thích khác (cũng hợp lý) cho bằng chứng then chốt không? Nếu có, thêm tài liệu để loại trừ nó.
4. Hung thủ có xuất hiện ngay từ trọng điểm 1 không? (bắt buộc có)
5. Mỗi nghi phạm vô tội đã có tài liệu loại trừ chưa?
6. Có chi tiết nào đòi hỏi kiến thức chuyên môn mà người chơi không thể tự có không?

Chưa tạo `case.json` ở bước này.
