# Ảnh cho bản 2 (tháng 11/2026)

Hung thủ đổi thành Y Ksor + Phan Văn Lợi (đồng phạm). Bìa cũ (hộp game có chữ tiếng Anh) và ảnh d06-anh-the đã gỡ. Sơ đồ vẽ lại bằng
`draw_so_do.py`. Dùng lại: d01-bao-chi, d05-xa-gac, d11-rui-dien.

## Ảnh thẻ (một ảnh ghép 3 cột × 2 hàng)

Cắt bằng: `python3 tools/crop-portraits.py <ảnh-ghép> public/cases/lua-than-tay-nguyen/images 2 3 krak bang nhi ksor loi -`
rồi `python3 authoring/lua-than-tay-nguyen/build_case.py`.

```text
A 3-column by 2-row grid of six Vietnamese ID card portrait photos from 2001, Central Highlands of Vietnam, separated by thin white lines, each cell a head-and-shoulders front-facing shot, neutral dignified expression, plain pale blue background, flat studio lighting, slightly faded film colour, realistic skin texture, no text.
Top row, left to right:
(1) a 63-year-old Ede ethnic minority village elder from Dak Lak, deeply lined dark tan face, short grey hair, calm wise eyes, traditional dark indigo Ede jacket with red and white woven trim;
(2) a 34-year-old Ede man, strong jaw, short black hair, tired eyes, faded blue work shirt;
(3) a 29-year-old Ede woman, gentle face, black hair tied back, traditional dark Ede blouse with red woven stripes;
Bottom row, left to right:
(4) a 40-year-old Ede man, lean weathered face, short messy hair, wary look, worn dark brown shirt;
(5) a 46-year-old ethnic Kinh Vietnamese businessman, round face, neatly combed hair, small mustache, light beige short-sleeved shirt with a pen in the pocket, gold wristwatch partly visible;
(6) an empty plain pale blue cell.
```

## Bìa (khổ ngang hoặc 4:5; có chữ tên hồ sơ ở một bên cũng được)

```text
Cinematic night photograph in a Central Highlands Ede village in Vietnam, dry season 2001: in the foreground the smouldering ashes and charred stilts of a small thatched rice granary on stilts, thin smoke rising, a few embers glowing; in the middle distance a long Ede longhouse on stilts lit warm orange from inside, silhouettes of gongs hanging at the entrance, a tall bamboo ceremonial pole with woven decorations; on the right a parked old pickup truck in shadow; red basalt soil, coffee bushes and tall dry trees, full moon in a hazy sky. Quiet, mournful, warm ember orange and deep night blue, 35mm film grain, realistic, no people, no visible faces.
```
Negative: `cartoon, 3D render, CGI, oversaturated, people, blood, bodies, modern objects, English text`

---

# Bảng Prompt Tạo Hình Chi Tiết: Đêm lửa tàn Buôn Ea Kral (Hồ sơ 07)

Toàn bộ prompt được viết bằng tiếng Việt chi tiết, hướng dẫn cụ thể về ánh sáng Tây Nguyên mùa khô năm 2001, nhà sàn, tro than kho thóc và kỹ thuật hình sự. Tuyệt đối không chứa chữ trên ảnh.

---

### 1. Ảnh bìa hồ sơ: `images/cover.webp`
- **Tên file**: `images/cover.webp`
- **Mô tả bối cảnh**: Khung cảnh đống tro tàn của kho thóc nhà sàn sau trận hỏa hoạn trong đêm tĩnh mịch giữa buôn làng Tây Nguyên.
- **Chi tiết khung hình**: Góc chụp chéo từ mặt đất nhìn lên tàn tích cột gỗ cháy đen nham nhở của ngôi nhà sàn chứa thóc. Những thanh nứa và vì kèo gỗ cháy rụi đổ sụp trên nền đất đỏ bazan nứt nẻ. Những đốm than đỏ hồng âm ỉ còn bốc khói xám lơ lửng trong gió đêm khô nóng. Phía hậu cảnh xa xa là mái nhà rông cao vút sừng sững dưới bầu trời đầy sao của cao nguyên Đắk Lắk. Dưới đống tro nguội phía trước, một chiếc xà gạc truyền thống chuôi gỗ bọc mạ đồng khảm hoa văn Ê Đê nằm chỏng chơ bám đầy bụi tro xám.
- **Ánh sáng & Màu sắc**: Ánh sáng đỏ cam le lói từ các tàn than đang cháy ngún kết hợp với ánh trăng lạnh trên bầu trời đêm Tây Nguyên. Tông màu khói xám, than đen và ánh than hồng tương phản mạnh mẽ, tạo không khí bi tráng, bí hiểm và căng thẳng.

---

### 2. Ảnh tư liệu hiện trường: `images/d05-xa-gac.webp`
- **Tên file**: `images/d05-xa-gac.webp`
- **Mô tả bối cảnh**: Ảnh chụp cận cảnh chiếc xà gạc vùi dưới đống tro than lúa cháy tại góc kho thóc.
- **Chi tiết khung hình**: Góc chụp cận cảnh từ trên xuống (flatlay macro). Nửa thân chiếc dao quắm xà gạc bản địa vùi trong lớp vỏ trấu cháy xám xịt. Lưỡi dao bằng thép rèn thủ công bị ám khói đen, phần sống dao dày gồ ghề có dính vệt máu khô thẫm lẫn sợi tóc người. Ở phần chuôi gỗ tròn mài nhẵn, khắc chìm một ký tự chữ cái 'B' hoa cách điệu bằng mũi dao nhọn rất rõ nét.
- **Ánh sáng & Màu sắc**: Đèn flash chụp kỹ thuật hình sự trực diện làm nổi bật ký tự khắc trên chuôi gỗ và vết máu khô trên sống thép. Thước đo tỷ lệ cm bằng nhựa vàng đặt song song với thân dao.

---

### 3. Ảnh vật chứng bẫy nhiệt: `images/d11-rui-dien.webp`
- **Tên file**: `images/d11-rui-dien.webp`
- **Mô tả bối cảnh**: Các mảnh vỡ thiết bị kích hoạt cháy được thu thập tại tâm điểm phát hỏa trong kho thóc.
- **Chi tiết khung hình**: Đặt trên một tấm khay kim loại giám định: Những mảnh vỡ thủy tinh cong của bóng đèn sợi đốt 100W bị nung nhiệt cao ám khói đen, đui đèn xoáy bằng đồng dính dây điện đôi bọc nhựa vàng bị cháy sun lại. Cạnh đó là cụm bánh răng đồng thau và lò xo cót của chiếc đồng hồ rơ-le hẹn giờ cơ khí (dùng trong máy ấp trứng gia cầm) bị cháy xém một nửa.
- **Ánh sáng & Màu sắc**: Ánh sáng trắng huỳnh quang phòng kỹ thuật hình sự, sắc nét đến từng chi tiết răng cưa kim loại và sợi tóc vonfram đứt gãy.

---

### 4. Ảnh báo: `images/d01-bao-chi.webp`
- **Tên file**: `images/d01-bao-chi.webp` (ngang 16:10)
- **Mô tả bối cảnh**: Ảnh tư liệu báo Đắk Lắk sáng 10/04/2001: hiện trường kho thóc cộng đồng buôn Ea Kral sau đêm cháy.
- **Chi tiết khung hình**: Ảnh báo chí đen trắng hơi nhoè hạt. Nền đất đỏ bazan, tàn tích kho thóc nhà sàn gỗ nứa cháy rụi chỉ còn vài cột gỗ đen trơ trụi và mái ngói sụp, khói xám mỏng còn bốc lên. Phía sau, cách khoảng 50 m, mái nhà rông cao vút. Vài người dân Ê Đê đứng xa nhìn, quay lưng hoặc mờ mặt; một công an mặc sắc phục xanh lá năm 2001 căng dây phong toả. Không có chữ, không có biển hiệu.
- **Ánh sáng & Màu sắc**: Nắng sớm mùa khô Tây Nguyên, khói làm dịu ánh sáng; đen trắng tương phản vừa, kiểu ảnh in báo.

### 5. Ảnh thẻ nhân chứng: `images/d06-anh-the.webp`
- **Tên file**: `images/d06-anh-the.webp` (ngang 4:3)
- **Mô tả bối cảnh**: Ảnh thẻ kèm hồ sơ lời khai của Y Bang (con nuôi già làng, khoảng 30 tuổi, chủ tiệm thu mua cà phê). Nhân vật hư cấu.
- **Chi tiết khung hình**: Tấm ảnh thẻ chân dung 4x6 cũ, kẹp ghim vào góc một tờ hồ sơ giấy ngả vàng trên mặt bàn gỗ. Người đàn ông Ê Đê khoảng 30 tuổi, da rám nắng, tóc ngắn, áo sơ mi cổ bẻ màu xanh nhạt, nét mặt lì, nhìn thẳng. Nền ảnh thẻ xanh dương nhạt kiểu tiệm ảnh năm 2001. Không có chữ đọc được trên giấy.
- **Ánh sáng & Màu sắc**: Ánh đèn bàn vàng ấm chiếu xiên; ảnh thẻ hơi phai màu, mép giấy sờn.

---

### Prompt ảnh tổng hợp (một lần tạo cho cả 4 ảnh chụp, sau đó cắt thành từng ô)

Dán nguyên đoạn dưới vào công cụ tạo ảnh, tỉ lệ 3:2 (ví dụ 1536×1024). Ô thứ tự trái sang phải, trên xuống dưới: d01, d05, d06, d11. Ảnh sơ đồ d03 đã được vẽ bằng code (`draw_so_do.py`), không cần tạo.

```
A 2x2 grid of four separate documentary photographs from a 2001 police case file in the Central Highlands of Vietnam, separated by thin pure-white gutters (8 px) on a white background, no text, no captions, no logos, no watermarks.
Top-left: black-and-white newspaper photograph, slightly grainy: the burnt ruins of a wooden stilt rice storehouse on red basalt earth at dawn, only a few charred posts and a collapsed tile roof left, thin grey smoke rising; a tall Ede communal house (nha rong) roof about 50 metres behind; a few villagers far away with faces not visible; a Vietnamese policeman in 2001 olive-green uniform stretching a cordon tape.
Top-right: forensic flat-lay macro under direct camera flash: a traditional Ede machete (xa gac) half buried in grey burnt rice husk ash, hand-forged blade blackened by smoke, thick spine with dark dried blood and a strand of hair, round polished wooden handle with a stylised capital letter B carved into it, a yellow plastic centimetre scale ruler laid parallel to the blade.
Bottom-left: an old faded 4x6 cm passport-style ID photo of a fictional Ede man about 30, tanned skin, short hair, light-blue collared shirt, blank stare, light-blue studio backdrop typical of 2001, paper-clipped to the corner of a yellowed blank file sheet on a wooden desk, warm desk-lamp light.
Bottom-right: evidence laid out on a stainless-steel forensic tray under white fluorescent lab light: curved shards of a smoke-blackened 100 W incandescent bulb with a broken tungsten filament, a brass screw lamp socket with a scorched yellow twin-core cable shrunk by heat, and next to it the brass gears and coil spring of a half-burnt mechanical timer relay from a poultry egg incubator, razor-sharp detail.
Photorealistic, authentic 2001 documentary look, no illustration, no anime.
```

### Gợi ý tinh chỉnh khi dùng công cụ AI (Midjourney / Bing / Stable Diffusion):
- Thêm từ khóa: `Central Highlands Vietnam village, burnt wooden stilt storehouse ruins, glowing embers, smoke, Ede traditional knife xa gac, forensic crime scene photo, 2001 documentary photograph, high detail texture, authentic cultural artifacts`.
- Tránh: Không xuất hiện chữ viết nhân tạo trên ảnh, không hình ảnh hoạt hình anime.
