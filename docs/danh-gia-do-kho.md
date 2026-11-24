# Đánh giá độ khó và độ hấp dẫn của 17 hồ sơ

Ngày đánh giá: 24/11/2026. Dữ liệu: `public/cases/*/case.json` ở trạng thái làm việc (gồm cả bản "nâng cấp độ khó" Antigravity đang sửa, chưa commit) và `authoring/*/bible.md`.

Chạy `npm run validate` để thấy các lỗi dưới đây dưới dạng cảnh báo cho từng hồ sơ.

## 1. Kết luận nhanh

Các vụ án có ý tưởng tốt (bóng nắng thiên văn, bẫy lưỡng kim, đá khô CO2, bẫy nước gõ chuông…), nhưng **cách trình bày làm người chơi thắng mà không cần suy luận**. Năm nguyên nhân chính, đo được trên cả 17 hồ sơ:

| Vấn đề | Mức độ | Số hồ sơ |
|---|---|---|
| Đáp án đúng của câu chỉ mặt hung thủ **luôn dài nhất**, thường gấp đôi các phương án sai | Rất nặng: chọn câu dài nhất là thắng | 17/17 |
| Người chơi **thử sai không giới hạn, không bị phạt**; vòng 1 chỉ có 10 cách chọn 2/5 tài liệu | Nặng: bấm thử là qua | 17/17 (đã sửa ở engine, xem mục 3) |
| **Bản tự thú / lời nhận tội** mở trước hoặc cùng lúc với câu chỉ mặt hung thủ | Nặng: câu cuối thành thủ tục | 9/17 |
| **Đề bài tả lại tài liệu cần chọn** ("ghim biên bản trục vớt… và hóa đơn mua ống nhựa…"), người chơi chỉ dò chữ | Trung bình | 17/51 câu chọn tài liệu |
| **Tài liệu tự suy luận thay người chơi** (giám định ghi "kết luận: đồng hồ bị chỉnh lùi để ngụy tạo ngoại phạm"), tiêu đề nói trước kết luận ("…gài lén…", "Bản tự thú…") | Trung bình | ~11 tài liệu |

Ngoài độ khó còn ba lỗi khác:

- **14/17 hồ sơ có màn kết thúc trống.** `finale` được viết dạng `{culprit, text}` trong khi màn kết thúc đọc `paragraphs`. **Đã sửa ở engine.**
- **Vụ có thật:** "Bức thư đêm tuyết trắng" khẳng định **bà Patsy Ramsey (người thật, đã mất) viết thư tống tiền và gia đình dàn dựng hiện trường**. Ngoài đời vụ án chưa được phá, và năm 2008 công tố viên đã chính thức minh oan cho gia đình Ramsey nhờ ADN. "Quái vật 21 khuôn mặt" khẳng định động cơ thao túng chứng khoán cấu kết Yakuza như sự thật, dù vụ án chưa bao giờ được phá. **Cần sửa trước khi phát hành** (mục 4).
- **Mâu thuẫn số liệu** giữa gợi ý, tài liệu và đáp án. Ví dụ ở Bá Lễ: gợi ý ghi "bóng nắng 65°, 14h15", tài liệu ghi "45°, 14h20–14h40"; bản tự thú ghi nợ 200 triệu, đáp án ghi "hơn 300 triệu".

## 2. Nguyên tắc để game khó hơn và cuốn hơn

Áp dụng cho mọi hồ sơ. Phần lớn chỉ cần sửa chữ, không phải thêm tài liệu.

1. **Tài liệu ghi sự kiện, không ghi kết luận.** Giám định viên đưa số liệu ("góc bóng đổ 45°, hướng Đông Bắc"; "mặt trời qua thiên đỉnh lúc 11h50"), người chơi tự tính ra giờ thật. Bỏ các câu "chứng tỏ…", "kết luận: … ngụy tạo…".
2. **Tiêu đề trung tính theo loại giấy tờ**: "Biên bản giám định số 14/KT", "Ảnh chụp tang vật số 03", "Lời khai bổ sung lần 2". Không dùng "gài lén", "giả mạo", "tự thú".
3. **Đề bài hỏi điều cần chứng minh, không tả tài liệu.** Thay "Ghim biên bản trục vớt và hóa đơn mua ống nhựa" bằng "Chứng minh bức tranh chưa từng rời khỏi phố cổ, và chỉ ra ai đã chuẩn bị việc cất giấu nó".
4. **Mỗi vòng có ít nhất 2 nghi phạm còn đứng vững**, mỗi người có động cơ, cơ hội và **một điều giấu giếm riêng**, không nhất thiết là tội giết người (ngoại tình, nợ, buôn lậu nhỏ). Lời nói dối của họ phải bị lật ở vòng sau. Hiện nghi phạm giả thường có chứng cứ ngoại phạm kín ngay từ đầu, nên người chơi loại được ngay.
5. **Có ít nhất một cú lật** ở giữa hồ sơ: giả thuyết hợp lý nhất ở vòng 2 bị chứng minh sai ở vòng 3, hoặc có đồng phạm hay người che giấu.
6. **Câu chỉ mặt hung thủ có 4 phương án dài ngang nhau**, mỗi phương án tự nhất quán với một phần bằng chứng, và chỉ sai ở 1–2 chi tiết. Thêm `nudges` (`near: true`) cho phương án "gần đúng" để phản hồi có ý nghĩa.
7. **Bản tự thú chuyển vào `finale` / `epilogue`**, không đặt thành tài liệu trước câu cuối.
8. **Vòng 1 có ít nhất 7 tài liệu**, hoặc câu đầu cần 3 bằng chứng, để có ít nhất 35 cách chọn.
9. **Câu chọn dòng lời khai lấy trên nhiều lời khai cùng lúc** (ít nhất 20 dòng), và dòng đúng chỉ sai khi đối chiếu với một tài liệu khác.
10. **Bằng chứng cần tính toán chéo:** bảng giờ thủy triều, lịch tàu, tốc độ đi bộ, nhiệt độ kho lạnh… với dữ liệu nằm rải ở 2–3 tài liệu khác nhau.
11. **Gợi ý theo bậc:** gợi ý 1 chỉ hướng ("Để ý thời điểm mặt trời trong ảnh"), gợi ý 2 nói loại tài liệu, chỉ gợi ý cuối mới nêu mã tài liệu.
12. **Màn kết thúc có `finale.paragraphs`** kể lại toàn bộ diễn biến theo thời gian và một `epilogue` ngắn về số phận các nhân vật. Đây là phần thưởng cảm xúc của người chơi.

Mẫu đã làm tốt nhất: **"Con nước Rằm tháng Giêng"** (26 tài liệu, 17 tài liệu không thuộc đáp án nào, câu chọn dòng 1/73, không có bản tự thú, có finale và epilogue) và **"Mùa đông năm Bính Tý"**. Hai vụ này chỉ còn lỗi đáp án dài nhất.

## 3. Đã sửa ở engine (áp dụng cho mọi hồ sơ, không đụng `case.json`)

- **Chống đoán mò:** lần sai đầu tiên không bị gì; từ lần sai thứ hai, nút gửi khoá 15, 30, 45, tối đa 60 giây, kèm lời nhắc. Câu trả lời thiếu ý hoặc "gần đúng" không bị khoá.
- **Xếp hạng điều tra viên** ở màn kết thúc: điểm = 100 − 12 × số lần kết luận sai − 8 × số gợi ý. Có 3 hạng sao: Thám tử lừng danh, Điều tra viên vững nghề, Điều tra viên (thấp nhất là "tập sự", 0 sao).
- **Màn kết thúc đọc được `finale` dạng `{text}` hoặc chuỗi**, nên 14 hồ sơ không còn trống.
- **`npm run validate` cảnh báo**: đáp án dài bất thường, bản tự thú mở sớm, tiêu đề nói trước kết luận, đề bài lặp từ khoá tài liệu đáp án, gợi ý nêu mã tài liệu quá sớm, vòng 1 quá ít cách chọn, finale trống.

## 4. Nhận xét và việc cần làm cho từng hồ sơ

| # | Hồ sơ | Đánh giá hiện tại | Việc cần làm |
|---|---|---|---|
| 00 | Chiếc đồng hồ ở ngõ Gác Chuông | Hồ sơ hướng dẫn, dễ là hợp lý | Cân bằng độ dài 4 phương án ở câu cuối |
| 01 | Con nước Rằm tháng Giêng | **Tốt nhất.** Nhiều nhiễu, câu chọn dòng khó, có cú lật thủy triều | Cân bằng độ dài phương án |
| 02 | Mùa đông năm Bính Tý | Tốt. Có lời khai mâu thuẫn tiếng còi tàu | Cân bằng độ dài phương án; ảnh d06 sơ đồ giải phẫu có kết luận in sẵn |
| 03 | Tiếng đàn đáy Phố Hiến | Ngắn (3 vòng); giới thiệu nói luôn chất độc; sơ đồ d02 vẽ đường đi của Chu Văn Bình | Bỏ bản tự thú d15; viết lại giới thiệu; thêm một nghi phạm có lý do dâng trà |
| 04 | Sương mù Trại Mát | Ý tưởng kho lạnh hay, nhưng sơ đồ d03 có mũi tên kho lạnh → đồi thông, biểu đồ d11 khoanh sẵn giờ mở cửa | Xoá mũi tên d03, bỏ chữ chú thích d11; bỏ bản tự thú d17 |
| 05 | Chuyến tàu đêm Mường Mán | Phòng kín dây cước rõ ràng; d03 vòng 1 đã gọi Long là "nghi phạm" | Đổi thành "hành khách"; thêm nghi phạm thứ hai trong toa (Bùi Bích Thảo có động cơ thừa kế?); bỏ bản tự thú d17 |
| 06 | Bóng nắng giếng Bá Lễ | Ý tưởng bóng nắng rất hay nhưng bị lộ: d10 tự kết luận, d14 có nhân chứng thấy Bảo vặn đồng hồ, d15 là bản tự thú; Bảo tự nhắc "nợ cá độ" trong lời khai | Để d10 chỉ ghi số đo góc bóng và giờ thiên đỉnh; bỏ dòng 003–004 của d14 hoặc chuyển sang vòng sau; d15 vào finale; sửa mâu thuẫn 45°/65° và 200/300 triệu; cho thợ mộc Trực giữ chìa khoá và có nợ thật |
| 07 | Đêm lửa tàn Buôn Ea Kral | Tiêu đề d10, d11 nói trước cơ chế bẫy; đề bài câu 1 lặp tiêu đề | Đổi tiêu đề trung tính; viết lại đề bài |
| 08 | Gác đèn Hòn Dáu | Bẫy lưỡng kim chặt chẽ; tiêu đề d11 "gài lén", d10 tự kết luận "phá hoại", giới thiệu nói luôn "ngắn mạch trễ", d19 tự thú | Viết lại giới thiệu; đổi tiêu đề d11; bỏ câu kết luận trong d10; d19 vào finale |
| 09 | Vàng bóng Chợ Lớn | Không có tự thú; bảng 24 hoán vị là câu đố tính toán tốt | Cân bằng độ dài phương án; thêm nghi phạm có lý do biết mật mã |
| 10 | Tiếng hú cảng Vân Đồn | Giới thiệu gợi thẳng "hóa chất băng giá"; d16 tự thú | Viết lại giới thiệu; d16 vào finale |
| 11 | Hồi chuông núi Sài Sơn | Giới thiệu nói luôn giờ chết và "mắt xích cơ học"; d16 tự thú | Viết lại giới thiệu để tiếng chuông 12h là chứng cứ ngoại phạm thật đến vòng 3; d16 vào finale |
| 12 | Vết mực làng Đông Hồ | Ngắn nhất (12 tài liệu), vòng 1 chỉ 4 tài liệu (6 cách chọn); d12 tự thú | Thêm 2–3 tài liệu nhiễu ở vòng 1; d12 vào finale |
| 13 | Ly trà tráo độc (có thật) | Dùng tên thật người đã bị kết án, tên bệnh viện và thương hiệu thật; d10 ảnh tô đỏ sẵn lịch sử tìm kiếm; d15 tự thú; tên bệnh viện lệch nhau (Đa khoa / Phổi) | Thống nhất tên bệnh viện; bỏ tô đỏ trong ảnh d10; d15 vào finale; cân nhắc đổi tên nhân vật |
| 14 | Bức thư đêm tuyết trắng (có thật) | **Đáp án khẳng định người thật đã được minh oan là thủ phạm** | Đổi câu cuối thành "giả thuyết nào khớp nhất với hồ sơ", và finale nói rõ vụ án chưa có lời giải, gia đình đã được minh oan; hoặc hư cấu hoá toàn bộ tên người |
| 15 | Đêm súng nổ phố Tây Sơn (có thật) | Cần xác minh tên hung thủ "Phạm Đức Thắng" và các chi tiết có khớp người thật hay không | Nếu là người thật chưa bị kết án đúng như mô tả, đổi tên; cân bằng độ dài phương án |
| 16 | Quái vật 21 khuôn mặt (có thật) | Đáp án khẳng định động cơ chứng khoán cho một vụ chưa phá | Đổi câu cuối thành "giả thuyết hồ sơ ủng hộ mạnh nhất"; finale ghi rõ vụ án hết thời hiệu năm 2000, không ai bị truy tố |

## 5. Thứ tự nên làm

1. Ba hồ sơ có thật (14, 16, và kiểm tra 15): sửa cách kết luận trước khi phát hành.
2. Cân bằng độ dài phương án câu cuối ở cả 17 hồ sơ (sửa chữ, không đổi cấu trúc).
3. Chuyển các bản tự thú vào finale (9 hồ sơ). Việc này **bớt một tài liệu**, tức là đổi cấu trúc, nên làm cùng lúc với đợt nâng cấp đang chạy để người chơi chỉ phải chơi lại một lần.
4. Đổi tiêu đề và đề bài trung tính, viết lại các giới thiệu lộ cơ chế (03, 08, 10, 11).
5. Thêm nghi phạm thứ hai và cú lật cho các vụ một nghi phạm (05, 06, 09, 12).
