# Ảnh cho bản 2 (tháng 11/2026)

Hung thủ đổi thành kế toán Tạ Thục Nghi. Bìa cũ (hộp game có chữ tiếng Anh) đã gỡ. Sơ đồ d04 vẽ lại bằng `draw_images.py d04`.
Dùng lại: d01-bao-chi, d05-num-ket, d09-cuong-ve, d10-manh-giay.

## Ảnh thẻ (một ảnh ghép 3 cột × 2 hàng)

Cắt bằng: `python3 tools/crop-portraits.py <ảnh-ghép> public/cases/vang-bong-cho-lon/images 2 3 thanh hao my buu nghi -`
rồi `python3 authoring/vang-bong-cho-lon/build_case.py`.

```text
A 3-column by 2-row grid of six Vietnamese ID card portrait photos from 1995, Saigon Chinatown, separated by thin white lines, each cell a head-and-shoulders front-facing shot, neutral expression, plain pale blue background, flat studio lighting, slightly faded film colour, realistic skin texture, no text.
Top row, left to right:
(1) a 60-year-old Vietnamese-Chinese gold shop owner, stern face, slicked-back grey hair, thin gold-rimmed glasses, white short-sleeved shirt;
(2) a 32-year-old Vietnamese-Chinese goldsmith, lean face, slightly long side-parted hair, floral print shirt open at the collar, thin gold chain;
(3) a 26-year-old Vietnamese woman, pretty, sharp eyes, permed shoulder-length hair, light pink blouse, small earrings.
Bottom row, left to right:
(4) a 48-year-old Vietnamese night security guard, tanned weathered face, short hair, plain khaki uniform shirt;
(5) a 40-year-old Vietnamese female bookkeeper, composed and neat, hair tied in a low bun, thin face, light blue traditional áo bà ba top;
(6) an empty plain pale blue cell.
```

## Bìa (4:5 hoặc ngang; có chữ tên hồ sơ cũng được, tôi sẽ cắt phần không có chữ làm ảnh nền thẻ)

```text
Cinematic night photograph inside a 1990s Saigon Chinatown gold shop office: a heavy old green steel safe stands open and empty, its combination dial dusted with fine white powder, four clean spots on the dial; in front, a wooden desk with a plastic cup of Vietnamese drip coffee half drunk beside an abacus and a ledger book; a carved armchair with a man's jacket draped over it (no person); warm tungsten desk lamp, red Chinese calligraphy scrolls and a gold shop altar softly out of focus; through a half-open side door, a dark narrow alley with a street coffee stall light far away. Moody, warm gold and deep green tones, 35mm film grain, realistic, no people.
```
Negative: `cartoon, 3D render, CGI, oversaturated, people, blood, modern objects, English text`

---

# Bảng Prompt Tạo Hình Chi Tiết: Vàng bóng Chợ Lớn (Hồ sơ 09)

Toàn bộ prompt được viết bằng tiếng Việt chi tiết, hướng dẫn cụ thể về ánh sáng phố người Hoa Chợ Lớn năm 1995, tiệm kim hoàn cổ, két sắt và kỹ thuật hình sự. Tuyệt đối không chứa chữ trên ảnh.

---

### 1. Ảnh bìa hồ sơ: `images/cover.webp`
- **Tên file**: `images/cover.webp`
- **Mô tả bối cảnh**: Không gian phòng khách kiêm quầy giao dịch tiệm vàng cổ điển trên đường Hải Thượng Lãn Ông, Quận 5 Chợ Lớn năm 1995.
- **Chi tiết khung hình**: Góc chụp chéo từ ngoài cửa nhìn vào gian phòng lát gạch bông hoa văn cổ điển kiểu Pháp. Tủ kính trưng bày trang sức bằng gỗ gụ viền đồng sáng bóng trống trơn một góc. Phía sau quầy là một chiếc két sắt sắt đúc màu xanh lục đậm khổng lồ nhãn hiệu Chubb, cánh cửa sắt dày cộp đang mở toang để lộ các ngăn kéo bên trong trống rỗng. Trên chiếc bàn gỗ cẩm lai đặt giữa phòng, một tách cà phê vợt bằng sứ trắng viền hoa lam bị nguội ngắt bên cạnh chiếc phin nhôm cũ, tàn thuốc lá vương vãi trên đĩa gạt tàn.
- **Ánh sáng & Màu sắc**: Ánh sáng vàng ấm từ chiếc đèn chùm cổ điển trên trần gỗ kết hợp ánh sáng hắt từ biển hiệu đèn neon đỏ ngoài phố người Hoa. Không khí hoài cổ của Sài Gòn thập niên 90, bí ẩn, giàu có nhưng đầy cạm bẫy.

---

### 2. Ảnh tư liệu hiện trường: `images/d05-num-ket.webp`
- **Tên file**: `images/d05-num-ket.webp`
- **Mô tả bối cảnh**: Ảnh chụp cận cảnh núm xoay kim loại của chiếc két sắt Chubb tại hiện trường.
- **Chi tiết khung hình**: Góc chụp macro trực diện vào núm xoay hình tròn bằng đồng mạ niken sáng bóng có khắc các vạch số từ 0 đến 99. Trên bề mặt kim loại phủ một lớp bột phấn khoáng màu trắng ngà mỏng manh, trong đó có 4 vị trí con số bị đầu ngón tay người lau sạch để lộ kim loại sáng bóng rõ nét, các hạt bụi phấn li ti đọng quanh viền gờ số.
- **Ánh sáng & Màu sắc**: Đèn flash chụp kỹ thuật hình sự góc xiên 30 độ làm nổi bật kết cấu vi hạt của lớp bột phấn và các vết vân tay quẹt mờ trên bề mặt kim loại.

---

### 3. Ảnh vật chứng: `images/d10-manh-giay.webp`
- **Tên file**: `images/d10-manh-giay.webp`
- **Mô tả bối cảnh**: Mảnh giấy ghi chép tìm thấy kẹt dưới chân bàn trà tiệm vàng.
- **Chi tiết khung hình**: Một mẩu giấy xé từ bao thuốc lá hoa cúc màu nâu nhạt đặt trên tấm bìa xanh giám định. Trên mảnh giấy có viết các hàng số bút bi xanh liệt kê các dãy 4 số hoán vị (như 18-42-65-89, 18-42-89-65...). Các hàng đầu tiên có vệt gạch chéo bằng mực đỏ, riêng một hàng số ở giữa được khoanh tròn một vòng tròn mực xanh rất đậm.
- **Ánh sáng & Màu sắc**: Ánh sáng trắng bàn làm việc phòng giám định, độ phóng đại cao, nổi rõ các thớ giấy xơ và nét mực bi lún trên mặt giấy.

---

### Gợi ý tinh chỉnh khi dùng công cụ AI (Midjourney / Bing / Stable Diffusion):
- Thêm từ khóa: `Cholon Chinatown Saigon 1995, retro jewelry shop interior, Chubb safe dial macro forensic photo, vintage safe combination paper note, 1990s documentary photography, film grain Kodak 200, authentic Vietnamese Chinese interior details`.
- Tránh: Không xuất hiện chữ viết nhân tạo tiếng Anh hay tiếng Trung lung tung trên ảnh, không phong cách hoạt hình anime.
