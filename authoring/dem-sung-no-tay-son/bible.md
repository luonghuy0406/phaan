# Kịch bản gốc: Chiếc cặp da đêm thứ Tư (Hồ sơ 15, bản 2)

**Hư cấu hoá** (11/2026). Bản 1 dựa trên một vụ cướp có thật và bịa thêm chi tiết về người thật; bản 2 đổi tên tiệm, thời gian, toàn bộ
nhân vật và tình tiết, bỏ nhãn "vụ án có thật", gỡ mọi ảnh cũ. Đổi luôn tên hồ sơ (bản 1: "Đêm súng nổ phố Tây Sơn") và con phố để không gợi tới vụ thật. Phố Chùa Bộc là địa danh thật; tiệm vàng Phúc Hưng và mọi người đều hư cấu.

5 vòng, 26 tài liệu, 12 câu hỏi, 90–120 phút, **độ khó 4, có đồng phạm**. Nội dung dựng bằng `build_case.py`. **Chứa lời giải.**

## 1. Sự thật
**Nổ súng: Tạ Văn Cường** ("Cường sẹo", 34), truy nã vì vụ cướp tiệm vàng Bắc Giang 12/1997 (cùng khẩu K54).
**Báo tin: Đặng Quốc Tuấn** (29), lái xe riêng của ông Phúc ba năm.
- Tuấn thua cá độ World Cup 1998 60 triệu; ổ cá độ giao Cường đòi. 20/8 Cường xoá nợ đổi "việc thứ Tư".
- Tối thứ Tư nào ông Phúc cũng lên chi nhánh Hàng Bạc lấy vàng về két nhà, đi cửa ngách. Cường thuê máy nhắn tin 107-5523 (2/8, CMND
  giả). Các tối 5, 12, 19/8 Tuấn gọi từ bốt điện thoại thẻ Hàng Bạc (thẻ sê-ri 0812774) nhắn giờ về.
- 26/8: 22:15 Tuấn "đi mua thuốc lá", 22:16 nhắn "22H40 CAP DEN CUA NGACH", mua Vinataba của bà Vân. 22:25 rời Hàng Bạc. 22:40 thả ông
  Phúc ở miệng ngõ, đi gửi xe (sổ 22:44), đứng dưới mái hiên đợi tới 22:47. Cường chờ trong ngõ, bắn hai phát, giật cặp, chạy Simson
  ra ngõ sau. 28/8 bán 20 lượng vàng nung cho Hùng (Giáp Bát). 30/8 Tuấn mua Dream II 25 triệu tiền mặt.

**Nghi phạm giả:** Đông (thợ cũ bị đuổi, nói dối không biết lịch; ở Bạch Mai), Hùng (tiêu thụ vàng; ở Giáp Bát tối 26/8).

## 2. Chuỗi suy luận
- **Vòng 1 (8):** d00–d07. q1 kẻ cướp biết trước. q2 thẻ, nhiều: ai biết lịch (Đông, Tuấn).
- **Vòng 2 (6):** d08 Đông, d09 Hùng, d10 đạn đạo, d11 ông Bảy, d12 xác minh Đông và Hùng, d13 hồ sơ Cường.
  q3 line d08:004. q4 evidence (d10, d13). q5 thẻ, nhiều: không cầm súng (Đông, Tuấn, Hùng).
- **Vòng 3 (5):** d14 chị Lan, d15 tổng đài nhắn tin, d16 bưu điện, d17 Tuấn lần 2, d18 bà Vân.
  q6 line d06:002. q7 evidence (d15, d16). q8 line d17:004.
- **Vòng 4 (4):** d19 sổ cá độ, d20 khám xét tiệm cầm đồ, d21 chi tiêu Tuấn, d22 chủ quán bia. q9 line d09:004. q10 evidence (d19, d21).
- **Vòng 5 (3):** d23 bắt Cường, d24 khám xét Tuấn, d25 giám định. q-accuse (Cường, Tuấn). q11 kết luận + kiểm sát viên AI.
