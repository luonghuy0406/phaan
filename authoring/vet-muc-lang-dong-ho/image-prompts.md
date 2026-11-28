# Ảnh cho bản 2 (tháng 11/2026)

Nhân vật đổi tên (bản 1 dùng họ "Nguyễn Đăng" trùng một dòng họ nghệ nhân có thật). Bìa cũ (mockup ghép mặt người) và ảnh d10 đã gỡ.
Sơ đồ làng (d04) vẽ lại: `authoring/vet-muc-lang-dong-ho/draw_so_do.py`. Dùng lại: d01-bao-chi, d03-ban-khac, d07-tranh-dong-ho.

## Ảnh thẻ (một ảnh ghép 3 cột × 2 hàng)

Cắt bằng: `python3 tools/crop-portraits.py <ảnh-ghép> public/cases/vet-muc-lang-dong-ho/images 2 3 thao khiem vinh hung luc -`
rồi `python3 authoring/vet-muc-lang-dong-ho/build_case.py`.

```text
A 3-column by 2-row grid of six Vietnamese ID card portrait photos from 2001, separated by thin white lines, each cell a head-and-shoulders front-facing shot, neutral expression, plain pale blue background, flat studio lighting, slightly faded film colour, realistic skin texture, no text.
Top row, left to right:
(1) a 60-year-old Vietnamese village folk-print artisan, thin face, short white hair, wispy white goatee, kind deep-set eyes, dark brown traditional collarless shirt;
(2) a 24-year-old Vietnamese village young man, defiant expression, short spiky black hair, faded denim jacket over a white t-shirt;
(3) a 38-year-old Vietnamese small-business owner, round face, neat side-parted hair, short-sleeved light grey shirt with a pen in the pocket.
Bottom row, left to right:
(4) a 19-year-old shy Vietnamese apprentice, boyish face, short cropped hair, plain brown work shirt;
(5) a 52-year-old Vietnamese woodcarver, weathered face, greying crew cut, thick calloused look, small scar on the eyebrow, faded olive army-style shirt;
(6) an empty plain pale blue cell.
```

## Bìa (4:5, 1200×1500, dưới 400 KB; có chữ ở 1/3 dưới cũng được, thẻ trang chủ chỉ lấy phần trên)

```text
Cinematic night photograph inside a traditional Vietnamese folk woodblock print workshop, Đông Hồ village, the night before Tết 2001: an old carved woodblock of a mouse wedding procession lies broken in two on a brick floor scattered with sheets of shimmering seashell-coated paper; a heavy stone pestle beside it; a single oil lamp casting warm amber light; behind, wooden racks of woodblocks and red and yellow folk prints drying on strings; through the open wooden door, faint blue light of a village film screening far away. Quiet, melancholic, rich warm and cold tones, 35mm film grain, realistic, no people.
```
Negative: `cartoon, 3D render, CGI, oversaturated, people, blood, modern objects`

---

# Bảng Prompt Tạo Hình Chi Tiết: Vết mực làng Đông Hồ (Hồ sơ 12)

Toàn bộ prompt được viết bằng tiếng Việt chi tiết, hướng dẫn cụ thể về làng tranh Đông Hồ Bắc Ninh giáp Tết năm 2000, bản khắc gỗ thị cổ, giấy điệp óng ánh và kỹ thuật hình sự. Tuyệt đối không chứa chữ trên ảnh.

---

### 1. Ảnh bìa hồ sơ: `images/cover.webp`
- **Tên file**: `images/cover.webp`
- **Mô tả bối cảnh**: Không gian xưởng tranh dân gian Đông Hồ trong đêm mưa bụi giáp Tết năm 2000 bên dòng sông Đuống.
- **Chi tiết khung hình**: Góc chụp chéo một góc sân phơi lợp mái rạ truyền thống. Hàng trăm tờ giấy dó quét điệp màu trắng ngà óng ánh xà cừ vỏ sò điệp đang được kẹp phơi trên các dây thép chăng ngang sân. Dưới nền gạch đỏ rêu phong, một tấm bản khắc gỗ thị màu nâu sẫm cổ kính bị gãy đôi làm hai nửa, những đường nét chạm khắc nổi hình đàn chuột rước dâu tinh xảo bị vỡ vụn một góc. Cạnh đó là một chậu đất nung đựng phẩm màu đỏ son tự nhiên bị đổ nghiêng, vệt phẩm đỏ tươi như máu loang lổ trên mặt giấy điệp lấp lánh ánh kim sa.
- **Ánh sáng & Màu sắc**: Ánh sáng vàng mờ ấm áp từ ngọn đèn dầu treo dưới mái hiên hòa cùng ánh mưa xuân lất phất của đêm đông Kinh Bắc. Tông màu đỏ son, nâu gỗ cổ và trắng ánh điệp tương phản rực rỡ, đậm chất văn hóa dân gian Việt Nam.

---

### 2. Ảnh tư liệu hiện trường: `images/d03-ban-khac.webp`
- **Tên file**: `images/d03-ban-khac.webp`
- **Mô tả bối cảnh**: Ảnh chụp cận cảnh bản khắc gỗ thị bị đập vỡ trên nền xưởng in tranh.
- **Chi tiết khung hình**: Góc chụp thẳng từ trên xuống (flatlay macro). Tấm ván gỗ thị dày 3cm kích thước 30x40cm có niên đại cổ xưa bị nứt gãy toác làm đôi từ chính giữa. Phần khắc gỗ tinh xảo vẽ cảnh chuột thổi kèn và chú rể chuột cưỡi ngựa bị mẻ một mảng lớn. Trên mép gãy của thớ gỗ thị vàng nhạt có dính một giọt phẩm màu đỏ son tươi rói chưa kịp khô hẳn, cạnh đó là chiếc chày đá giã điệp chuôi sứt mẻ dính phẩm đỏ.
- **Ánh sáng & Màu sắc**: Ánh sáng đèn flash kỹ thuật hình sự trực diện làm rõ thớ gỗ thị mịn màng và độ sắc nét của các đường đục chạm dân gian.

---

### 3. Ảnh vật chứng: `images/d10-dam-go.webp`
- **Tên file**: `images/d10-dam-go.webp`
- **Mô tả bối cảnh**: Dăm gỗ thị và vết bùn trên y phục nghi phạm tại trụ sở công an xã.
- **Chi tiết khung hình**: Đặt trên một tờ giấy trắng kẻ ô ly: Một mảnh dăm gỗ thị nhỏ hình tam giác dài khoảng 2cm, một mặt có đường nét đục nổi hoa văn chiếc lọng che rước dâu dính phẩm đỏ son. Cạnh mảnh dăm gỗ là chiếc dép tổ ong nhựa trắng cũ bám đầy lớp bùn đỏ phù sa sông Đuống bết dính ở các rãnh đế.
- **Ánh sáng & Màu sắc**: Ánh sáng bàn làm việc ban ngày, độ chi tiết cao, làm nổi bật sự khớp nối hoàn hảo giữa mảnh dăm gỗ và góc gãy của bản khắc cổ.

---

### Gợi ý tinh chỉnh khi dùng công cụ AI (Midjourney / Bing / Stable Diffusion):
- Thêm từ khóa: `Dong Ho folk painting workshop, traditional Vietnamese woodblock print, diep paper sparkles, crushed seashell paste, red vermilion pigment, Tet festival 2000, 35mm documentary photography, Northern Vietnam rural village`.
- Tránh: Không xuất hiện chữ viết nhân tạo trên ảnh, không phong cách hoạt hình anime.
