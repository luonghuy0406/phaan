# Ảnh cho bản 2 (tháng 11/2026)

Thủ phạm đổi thành máy trưởng Sáu. Bìa cũ (hộp game chữ tiếng Anh) và d03-giai-phau (ghi sai dấu hiệu ngộ độc CO) đã gỡ. Bìa và ảnh
nền thẻ cắt từ d01-bao-chi. Sơ đồ d04 vẽ lại bằng `draw_so_do.py`. Dùng lại: d01-bao-chi, d05-nap-khoang, d11-da-kho.

## Ảnh thẻ (một ảnh ghép 3 cột × 2 hàng)

Cắt bằng: `python3 tools/crop-portraits.py <ảnh-ghép> public/cases/tieng-huan-van-don/images 2 3 dat tuan sau hai khuong -`
rồi `python3 authoring/tieng-huan-van-don/build_case.py`.

```text
A 3-column by 2-row grid of six Vietnamese ID card portrait photos from 2006, northern Vietnamese fishermen from Quang Ninh, separated by thin white lines, each cell a head-and-shoulders front-facing shot, neutral expression, plain pale blue background, flat studio lighting, slightly faded colour, realistic sun-weathered skin, no text.
Top row, left to right:
(1) a 50-year-old Vietnamese fishing boat captain, stern square face, short greying hair, deep sun wrinkles, dark navy jacket over a white undershirt;
(2) a 42-year-old Vietnamese first mate, sharp eyes, short black hair, thin mustache, faded olive green shirt;
(3) a 46-year-old Vietnamese ship engineer, calm tired face, receding hairline, small scar on the chin, grey work shirt with oil stains on the collar.
Bottom row, left to right:
(4) a 26-year-old Vietnamese deckhand, boyish nervous face, spiky short hair, red and black striped polo shirt;
(5) a 55-year-old Vietnamese ship cook, round kind face, thinning grey hair, white t-shirt under an open brown shirt;
(6) an empty plain pale blue cell.
```

---

# Bảng Prompt Tạo Hình Chi Tiết: Tiếng hú cảng Vân Đồn (Hồ sơ 10)

Toàn bộ prompt được viết bằng tiếng Việt chi tiết, hướng dẫn cụ thể về tàu cá xa bờ Quảng Ninh năm 2006, khoang lạnh ướp đá, cảng cá Cái Rồng và kỹ thuật hình sự. Tuyệt đối không chứa chữ trên ảnh.

---

### 1. Ảnh bìa hồ sơ: `images/cover.webp`
- **Tên file**: `images/cover.webp`
- **Mô tả bối cảnh**: Rạng sáng mịt mù sương muối lạnh tại cảng cá Cái Rồng, Vân Đồn năm 2006.
- **Chi tiết khung hình**: Góc chụp chéo từ cầu cảng gỗ nhìn lên boong một con tàu đánh cá xa bờ vỏ gỗ công suất lớn sơn xanh viền cam đặc trưng miền biển Quảng Ninh. Trên boong tàu ướt sũng nước biển và dăm đá vảy tuyết lấp lánh, một nắp khoang lạnh bằng gỗ bọc thép đang mở hé, hơi sương lạnh ngưng tụ màu trắng đục bốc lên nghi ngút từ lòng khoang tối sẫm. Phía xa là các mỏm núi đá vôi vịnh Bái Tử Long mờ ảo trong làn sương sớm xám xanh ảm đạm.
- **Ánh sáng & Màu sắc**: Ánh sáng ban mai lạnh lẽo xám xịt của mùa đông miền biển phía Bắc, ánh đèn vàng mờ từ cột cẩu boong tàu chiếu xiên qua làn hơi lạnh bốc lên từ khoang tàu. Tông màu xanh lam sẫm, xám thép và hơi lạnh băng giá, tạo cảm giác nghẹt thở, rùng rợn và u ám.

---

### 2. Ảnh tư liệu hiện trường: `images/d05-nap-khoang.webp`
- **Tên file**: `images/d05-nap-khoang.webp`
- **Mô tả bối cảnh**: Ảnh chụp cận cảnh nắp khoang lạnh số 3 trên sàn boong tàu gỗ.
- **Chi tiết khung hình**: Góc chụp từ trên xuống vào nắp khoang lạnh đóng kín bằng khung gỗ lim dày bọc tôn kẽm rỉ sét. Một thanh then cài bằng sắt đúc nặng trịch đang được xỏ ngang qua móc khóa chữ U trên mặt nắp. Trên bề mặt thanh then cài bằng sắt có vệt dầu mỡ máy màu đen bết dính và in rõ hoa văn gân cao su của găng tay bảo hộ lao động.
- **Ánh sáng & Màu sắc**: Ánh sáng đèn flash kỹ thuật hình sự chụp cận cảnh, làm rõ vết trầy xước kim loại sáng ánh thép và vệt dầu mỡ đen trên nền gỗ boong tàu ẩm ướt.

---

### 3. Ảnh vật chứng đá khô: `images/d11-da-kho.webp`
- **Tên file**: `images/d11-da-kho.webp`
- **Mô tả bối cảnh**: Khay mẫu vật chứng thu thập dưới đáy khoang lạnh số 3 và đường ống quạt hút.
- **Chi tiết khung hình**: Đặt trên một tấm khay inox y tế: Vài viên đá khô CO2 dạng viên nén hình trụ tròn đường kính 2cm màu trắng đục như tuyết đang bốc khói hơi sương nghi ngút tan dần. Cạnh đó là một đoạn ống kim loại của quạt hút thông gió bị ám muội trắng đông đá ở miệng phễu xả khí hẹp.
- **Ánh sáng & Màu sắc**: Ánh sáng trắng lạnh phòng khám nghiệm, độ phân giải cao, làm rõ cấu trúc hạt tuyết nén mịn của viên đá khô và làn khói CO2 trắng mỏng bảng lảng.

---

### Gợi ý tinh chỉnh khi dùng công cụ AI (Midjourney / Bing / Stable Diffusion):
- Thêm từ khóa: `Van Don fishing port dawn, Vietnamese wooden offshore fishing trawler, refrigerated fish hold opening, icy mist rising, dry ice pellets forensic close up photo, cold gloomy winter morning, limestone karsts background, 2006 documentary aesthetic`.
- Tránh: Không xuất hiện chữ viết nhân tạo trên ảnh, không phong cách hoạt hình anime.
