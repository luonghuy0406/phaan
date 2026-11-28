# Ảnh còn thiếu cho bản 2 (tháng 11/2026)

Hồ sơ đã viết lại (18 tài liệu, 4 nghi phạm). Ảnh thẻ: 3:4, lưu 480×640 WebP (~20 KB) ở `public/cases/demo-01/images/id-<id>.webp`.
Có rồi: `id-hau.webp` (ông Hậu). Tạo xong ảnh thì chạy `python3 authoring/demo-01/build_case.py` để gắn ảnh vào hồ sơ.

Phong cách chung (giống ảnh ông Hậu): ảnh căn cước năm 2024, chính diện, nền xanh nhạt trơn, ánh sáng đều, không chữ.

**id-tu.webp: Phạm Thị Tư, 59 tuổi, giúp việc**
```text
Vietnamese citizen ID card portrait photo, 2024, head and shoulders, front facing, neutral tired expression, plain pale blue studio background, even flat lighting. A 59-year-old Vietnamese countryside woman working as a housemaid, sun-tanned skin, gentle weary eyes, black hair with grey strands pulled back into a low bun, simple faded floral cotton blouse. Realistic skin texture, sharp focus, 85mm lens, documentary realism, no text.
```

**id-minh.webp: Nguyễn Quang Minh, 27 tuổi, cháu ông Hậu**
```text
Vietnamese citizen ID card portrait photo, 2024, head and shoulders, front facing, neutral expression, plain pale blue studio background, even flat lighting. A 27-year-old slim Vietnamese young man, short undercut black hair, pale skin, dark circles under restless eyes, slight stubble, plain dark grey crew-neck t-shirt. Realistic skin texture, sharp focus, 85mm lens, documentary realism, no text.
```

**id-hoa.webp: Lâm Văn Hoà, 61 tuổi, buôn đồ cổ**
```text
Vietnamese citizen ID card portrait photo, 2024, head and shoulders, front facing, neutral confident expression, plain pale blue studio background, even flat lighting. A 61-year-old portly Vietnamese businessman and antique dealer, round full face, thinning combed-back hair, gold-rimmed rectangular glasses, navy blue polo shirt. Realistic skin texture, sharp focus, 85mm lens, documentary realism, no text.
```

**id-loc.webp: Đào Quang Lộc, 52 tuổi, thợ sửa đồng hồ**
```text
Vietnamese citizen ID card portrait photo, 2024, head and shoulders, front facing, neutral serious expression, plain pale blue studio background, even flat lighting. A 52-year-old lean Vietnamese watchmaker, short greying hair, thin moustache, hollow cheeks, narrow focused eyes, beige short-sleeve button shirt. Realistic skin texture, sharp focus, 85mm lens, documentary realism, no text.
```

**cover.webp (thay bìa mockup có chữ, 2,5 MB): 4:5, 1200×1500, dưới 400 KB, một phần ba dưới tối và trống**
```text
Cinematic night photograph inside an antique collector's study in a narrow tube house in Hanoi Old Quarter, March 2024, light drizzle outside. A dark wooden desk, below it a small steel combination safe stands open and empty. On the desk an open velvet watch box with an empty round hollow where a pocket watch used to lie, a brass desk lamp casting a warm amber pool of light. Behind, an old wooden casement window with one shattered glass pane, the glass broken outward, cold blue streetlight and rain mist seeping through; tiled rooftops and tangled power lines faintly visible beyond. A few small glass shards glinting on the windowsill. Moody chiaroscuro, warm and cold light, 35mm film grain, realistic, no people, no text. Vertical 4:5, safe and window in the upper two thirds, dark wooden floor in the lower third.
```
Negative: `text, letters, logo, watermark, police tape, box mockup, packaging, people, hands, cartoon, 3D render, CGI, oversaturated`

---

# Bảng Prompt Tạo Hình Chi Tiết: Chiếc đồng hồ ở ngõ Gác Chuông (Hồ sơ 00)
## (MASTER ART DIRECTION & IMAGE PROMPT GUIDE - CASE 00)

Tài liệu hướng dẫn đạo diễn nghệ thuật và đặc tả thông số kỹ thuật tạo hình ảnh bằng AI (Art Direction & Master Prompt Guide) cho Hồ sơ mở đầu: **Chiếc đồng hồ ở ngõ Gác Chuông (`demo-01`)**.

> [!IMPORTANT]
> **Quy chuẩn mỹ thuật chủ đạo (Master Visual Style Guide):**
> - **Bối cảnh & Thời đại:** Căn nhà cổ số 17, ngõ Gác Chuông, khu phố cổ Hà Nội (tháng 3 năm 2024).
> - **Phong cách cốt lõi:** Trinh thám hiện đại kết hợp hoài cổ phố cổ Hà Nội (*Hanoi Old Quarter Neo-Noir*). Sự đan xen giữa nét kiến trúc nhà ống rêu phong (tường vàng vôi vữa loang lổ, cầu thang gỗ lim, cửa sổ chấn song lá sách) và nhịp sống đô thị đêm khuya tĩnh mịch.
> - **Chất liệu & Vật phẩm chủ đạo:** Đồng hồ quả quýt bỏ túi vỏ vàng 18K chạm trổ hoa hồng (phong cách nghệ thuật Art Deco thập niên 1920), kính cửa sổ vỡ vụn văng ra sân sau, áo nỉ hoodie xám có mũ trùm đầu, camera an ninh ngõ phố mờ nhòe (*CCTV security camera footage*).
> - **Cảm xúc định hướng:** Thanh lịch, bí ẩn, gợi tò mò, mang tính suy luận phá án cổ điển kiểu Agatha Christie đặt trong bối cảnh phố cổ Hà Nội.

---

## 1. Ảnh bìa hộp hồ sơ điều tra: `images/cover.webp`

1. **Ý tưởng hình ảnh:** Mockup hộp boardgame trinh thám cao cấp đứng thẳng trong không gian studio tối giản, khắc họa căn phòng làm việc tĩnh lặng của nhà sưu tầm cổ vật trong đêm định mệnh: chiếc đồng hồ vàng quý giá, két sắt mở toang và ô cửa kính vỡ hé lộ ánh trăng phố cổ.
2. **Phương án nghệ thuật:** *Product Mockup Boardgame Noir* trên nền tối giản sang trọng. Bìa hộp là bức ảnh chụp nghệ thuật tĩnh vật điện ảnh (*editorial still life photography*), có dải băng niêm phong công an và huy hiệu tiêu đề dập nổi sắc nét.
3. **Mô tả bố cục & Ánh sáng:**
   - *Bố cục:* Tỷ lệ 3:4 chuẩn hộp boardgame đứng thẳng trên bệ đá phiến xám hoặc mặt bàn gỗ gụ. Bìa hộp chụp góc cận cảnh bàn làm việc gỗ lim sẫm màu trong phòng sưu tầm đồ cổ: Chiếc đồng hồ quả quýt bỏ túi vỏ vàng óng 18K chạm khắc hoa văn cổ điển nằm mở nắp bên cạnh một cuốn sổ tay bìa da cũ và bút mực. Phía sau bàn là khung cửa sổ gỗ lá sách kiểu Pháp có một ô kính bị đập vỡ toang, để lọt vào luồng ánh sáng xanh lam lạnh lẽo từ bóng đèn đường ngõ Gác Chuông. Dải băng niêm phong cảnh sát vàng đen dán vắt góc hộp kèm nhãn dán: **"HỒ SƠ MẪU"**, **"TRỘM CỔ VẬT PHỐ CỔ"**. Khung huy hiệu tiêu đề in đậm phía dưới: **CHIẾC ĐỒNG HỒ Ở NGÕ GÁC CHUÔNG - HÀ NỘI**.
   - *Ánh sáng:* Ánh sáng tương phản điện ảnh (*cinematic chiaroscuro*): Viền sáng xanh lạnh (cool blue streetlight) xuyên qua ô kính vỡ đối lập với quầng sáng vàng ấm áp (warm tungsten amber) từ chiếc đèn bàn chao đồng cổ điển rọi lên vỏ vàng chiếc đồng hồ.
4. **Prompt tạo ảnh hoàn chỉnh (English Master Prompt):**
   ```text
   Commercial product photo mockup of a premium murder mystery boardgame box, standing vertically on a dark slate studio pedestal with subtle cinematic rim light. The front cover art features a moody atmospheric night scene in an antique collector's study in Hanoi Old Quarter: on a dark mahogany wooden desk lies an exquisite open antique 18k gold pocket watch with ornate floral engravings, next to a leather journal. In the background, an old French-colonial wooden window with one shattered glass pane, letting in cold blue moonlight and streetlamp glow, contrasting with the warm amber glow of a brass desk lamp. Diagonal yellow police crime scene tape across the corner, elegant typography title badge 'CHIẾC ĐỒNG HỒ Ở NGÕ GÁC CHUÔNG'. High-end tabletop game packaging design, sharp 8k focus, cinematic noir atmosphere --ar 3:4 --v 6.0
   ```
5. **Negative Prompt:**
   ```text
   cartoon, 3d render plastic, low resolution, blurry, oversaturated colors, smiling faces, modern smartphones, clean digital graphics, deformed fingers, extra limbs
   ```
6. **Tỷ lệ & Thông số kỹ thuật:** Khung hình **3:4**, định dạng WebP, xuất 900x1200px (hoặc 1200x1600px cho bản HD), dung lượng < 400 KB.

---

## 2. Ảnh tư liệu báo chí hiện trường: `images/d01-window.webp`

1. **Ý tưởng hình ảnh:** Bức ảnh chụp phóng sự hiện trường của phóng viên Báo Phố Cũ vào sáng sớm ngày 15/03/2024: Góc chụp từ sân sau nhà số 17 nhìn lên ô cửa sổ phòng làm việc bị đập vỡ, nơi chứa **manh mối then chốt**: hầu hết các mảnh kính vỡ đều văng ra ngoài sân sau (chứng minh cửa kính bị đập từ bên trong để ngụy tạo trộm đột nhập).
2. **Phương án nghệ thuật:** *Documentary Press Photography*, ảnh báo chí hiện thực, chất ảnh sắc nét trung thực như chụp từ máy ảnh kỹ thuật số DSLR (35mm f/2.8), ánh sáng ban mai nhẹ nhàng của buổi sáng mùa xuân Hà Nội nhiều mây.
3. **Mô tả bố cục & Ánh sáng:**
   - *Bố cục:* Góc chụp từ sân sau ngước lên cửa sổ tầng 2 hoặc nhìn thẳng vào khoảng sân gạch đỏ sau nhà ống cổ. Cửa sổ khung gỗ sơn xanh lá cây phong cách Pháp đã cũ sờn với một ô kính kích thước khoảng 30x40cm bị đập vỡ thủng một lỗ lớn. Dưới nền sân lát gạch bát tràng hoặc gạch tàu đỏ phủ rêu xanh mép tường, **hàng chục mảnh kính vỡ sắc nhọn nằm vương vãi lấp lánh trên mặt sân gạch ngay phía ngoài bậu cửa sổ**. Bậu cửa sổ bằng gỗ bám bụi không hề có vết giày dép trèo qua. Xung quanh có vài chậu cây cảnh, tường vôi vàng rêu phong ẩm ướt đặc trưng ngõ nhỏ Hà Nội.
   - *Ánh sáng:* Ánh sáng ban ngày nhiều mây dịu nhẹ (*overcast morning light*), không khí hơi ẩm ướt sau đêm mưa phùn xuân, phản chiếu ánh sáng lấp lánh trên các mảnh thủy tinh vỡ trên mặt sân.
4. **Prompt tạo ảnh hoàn chỉnh (English Master Prompt):**
   ```text
   Documentary press crime scene photograph taken in the morning light, Hanoi Old Quarter 2024. View of the rear courtyard of an old yellow-walled Vietnamese townhouse. A traditional French-colonial wooden window with green weathered paint has one shattered glass pane. On the red clay courtyard tiles directly below outside the window, numerous sharp shards of broken glass are scattered on the ground, revealing the glass was struck from the inside. Mossy weathered plaster wall, potted bonsai plants, wet ground from spring drizzle. Crisp 35mm documentary photography, natural soft overcast daylight, authentic forensic details, highly realistic --ar 4:3 --v 6.0
   ```
5. **Negative Prompt:**
   ```text
   people in frame, cartoon, 3d render, glossy modern mansion, clean pristine walls, tropical beach, bright neon colors, blurry
   ```
6. **Tỷ lệ & Thông số kỹ thuật:** Khung hình **4:3** (hoặc 16:9), định dạng WebP, xuất 800x600px (hoặc 1024x640px), dung lượng < 300 KB.

---

## 3. Sơ đồ hiện trường căn nhà cổ ngõ Gác Chuông: `images/d02-so-do-nha.webp`

1. **Ý tưởng hình ảnh:** Bản vẽ sơ đồ kỹ thuật hình sự trích từ Biên bản khám nghiệm hiện trường số 17/KNHT của Công an quận Gác Chuông, thể hiện chi tiết mặt bằng căn nhà số 17 ngõ Gác Chuông, lối đi cầu thang, vị trí két sắt, con chó becgie và cửa sổ vỡ.
2. **Phương án nghệ thuật:** *Forensic Blueprint / Architectural Floor Plan*, phong cách bản vẽ kỹ thuật hình sự trên giấy ô ly xanh (*cyan grid graph paper*), nét mực kỹ thuật chính xác, ghi chú các điểm nút giao thông và góc quan sát.
3. **Mô tả bố cục & Ánh sáng:**
   - *Bố cục:* Bản vẽ mặt bằng phẳng nhìn từ trên xuống (top-down 2D floor plan) thể hiện cấu trúc căn nhà ống 2 tầng:
     - **Tầng 1:** Cổng sắt bên ngoài (cài then trong), khoảng sân trước có vị trí con chó becgie xích cạnh cổng, phòng khách, phòng ngủ bà Tư (người giúp việc) và cầu thang gỗ lim dẫn lên tầng 2.
     - **Tầng 2 (Khu vực xảy ra vụ việc):** Phòng ngủ cháu trai Nguyễn Quang Minh ở phía trước; Hành lang hẹp dẫn vào Phòng làm việc của ông Trần Đức Hậu ở phía sau.
     - **Trong phòng làm việc:** Bàn làm việc gỗ lim, vị trí **két sắt đặt dưới gầm bàn** (khoanh đỏ: cửa két mở, không có dấu vết cạy phá), và **cửa sổ phía sân sau** (đánh dấu mũi tên đỏ: hướng văng của mảnh kính vỡ ra ngoài sân sau).
     Góc bản vẽ có hoa tiêu la bàn chỉ hướng Bắc, thước tỷ lệ kỹ thuật và con dấu mực đỏ của Đội Cảnh sát Hình sự.
   - *Ánh sáng:* Bản quét phẳng kỹ thuật số sắc nét, độ tương phản cao, rõ ràng từng vạch kẻ ô ly và chú thích chữ in kỹ thuật.
4. **Prompt tạo ảnh hoàn chỉnh (English Master Prompt):**
   ```text
   Official police forensic blueprint and architectural crime scene floor plan drawn on blue-toned cyan grid graph paper. A detailed 2D architectural layout of a two-story traditional Hanoi tube house (nhà số 17 ngõ Gác Chuông). Clearly labeled rooms: front courtyard with dog kennel, ground floor living room, wooden staircase, and second-floor private study. In the study room, specific forensic callouts mark the undamaged open floor safe beneath the desk and the rear window with red directional arrows showing glass shards blown outward into the back courtyard. North-pointing compass rose, technical scale ratio 1:100, official red rubber stamp of the Criminal Investigation Bureau. Sharp, authentic architectural draftsman style --ar 4:3 --v 6.0
   ```
5. **Negative Prompt:**
   ```text
   3D perspective view, isometric fantasy map, oil painting, artistic watercolor, colorful cartoon graphics, blurry text, satellite photo
   ```
6. **Tỷ lệ & Thông số kỹ thuật:** Khung hình **4:3**, định dạng WebP, xuất 800x600px, dung lượng < 250 KB.

---

## 4. Ảnh trích xuất camera an ninh ngõ Gác Chuông: `images/d07-camera.webp`

1. **Ý tưởng hình ảnh:** Khung hình trích xuất từ camera giám sát an ninh (CCTV still footage) của tiệm tạp hóa Thanh Mai ở đầu ngõ Gác Chuông lúc 22:53 đêm 14/03/2024: Ghi lại bóng một người mặc áo nỉ hoodie màu xám trùm mũ bước vội vã vào ngõ hướng về nhà số 17.
2. **Phương án nghệ thuật:** *CCTV Surveillance Footage Style*, góc máy nhìn từ trên cao xuống nghiêng 45 độ, độ phân giải camera giám sát an ninh hồng ngoại ban đêm hơi hạt, tông màu xám xanh lạnh (monochrome blue-grey tint), có vệt nhiễu kỹ thuật số (*digital video noise / scanlines*).
3. **Mô tả bố cục & Ánh sáng:**
   - *Bố cục:* Góc máy camera an ninh gắn trên tường cao nhìn dọc theo con ngõ hẹp đặc trưng phố cổ Hà Nội. Hai bên ngõ là những bức tường quét vôi vàng, cổng sắt đóng kín, dây điện chằng chịt phía trên và vài chậu hoa giấy bên hiên. Mặt ngõ bê tông ẩm ướt lấp loáng nước mưa. Ở trung tâm khung hình, một dáng người mảnh khảnh mặc **áo nỉ hoodie màu xám có mũ trùm kín đầu**, hai tay đút túi áo, bước đi thoăn thoắt quay lưng về phía camera, đang tiến sâu vào trong ngõ về hướng nhà số 17. Góc trên cùng bên trái màn hình có dòng chữ kỹ thuật số màu trắng đục: **CAM 02 - TIEM THANH MAI · 14/03/2024 22:53:18**.
   - *Ánh sáng:* Ánh sáng đèn đường vàng yếu ớt từ xa kết hợp ánh đèn hồng ngoại của camera an ninh rọi xuống mặt ngõ ẩm ướt, tạo bóng đổ dài mờ ảo.
4. **Prompt tạo ảnh hoàn chỉnh (English Master Prompt):**
   ```text
   Authentic night CCTV security camera still footage from a wall-mounted surveillance camera in a narrow residential alley in Hanoi Old Quarter. High-angle perspective looking down into the wet concrete alleyway between weathered yellow house walls, tangled overhead electrical cables, and closed metal folding gates. A single dim sodium streetlamp casting a hazy yellow glow on the damp pavement. In midground, a lone person wearing a plain grey hooded sweatshirt with the hood pulled up, walking away down the alley into the darkness, face obscured. Grainy low-light security video texture, subtle digital interlacing scanlines, cold blue-grey vignette tint, authentic surveillance monitor look, timestamp overlay text in top corner --ar 4:3 --v 6.0
   ```
5. **Negative Prompt:**
   ```text
   crisp clean studio portrait, daylight, colorful bright lights, smiling face, modern wide American street, 3d render, cartoon, high-res commercial photo
   ```
6. **Tỷ lệ & Thông số kỹ thuật:** Khung hình **4:3**, định dạng WebP, xuất 800x600px (hoặc 1024x768px), dung lượng < 300 KB.

---

## 5. Ảnh tang vật chiếc đồng hồ quả quýt bỏ túi: `images/d08-watch.webp`

1. **Ý tưởng hình ảnh:** Bức ảnh tang vật giám định hình sự (*Forensic Evidence Macro Photography*): Chiếc đồng hồ quả quýt bỏ túi vỏ vàng đời 1920 quý giá của ông Hậu thu hồi từ tiệm cầm đồ Phát Đạt trên phố Hàng Rèn vào sáng ngày 16/03/2024.
2. **Phương án nghệ thuật:** *Forensic Macro Studio Photography*, chụp macro cận cảnh cực nét trên nền giấy bìa hồ sơ màu xám trung tính, ánh sáng tản đều làm nổi bật chất kim loại vàng 18K cổ và chi tiết chạm khắc hoa văn tinh xảo.
3. **Mô tả bố cục & Ánh sáng:**
   - *Bố cục:* Góc chụp từ trên xuống (top-down flatlay). Đặt chính giữa tấm phông xám mờ kỹ thuật hình sự: Một chiếc đồng hồ bỏ túi cổ điển (antique pocket watch) loại nắp đóng mở (*hunter case*), vỏ bằng vàng vàng 18K sáng bóng nhưng có những vết xước tơ tự nhiên của thời gian. Nắp trước đồng hồ chạm khắc hoa văn dây leo hoa hồng phong cách Art Deco uốn lượn tuyệt mỹ; chính giữa nắp sau có một khung bầu dục nhỏ khắc chìm 3 chữ cái viết tắt sắc nét: **T.Đ.H** (Trần Đức Hậu). Sợi dây xích đồng hồ bằng mắt xích vàng thanh mảnh cuộn lượn sóng mềm mại bên cạnh. Đặt song song mép dưới là thước đo cm tỉ lệ hình sự đen trắng.
   - *Ánh sáng:* Ánh sáng đèn studio tản mềm (*soft diffused light*), loại bỏ phản xạ lóa chói, làm tôn lên sắc vàng ấm sang trọng của vàng ròng và chiều sâu của những đường nét chạm khắc thủ công.
4. **Prompt tạo ảnh hoàn chỉnh (English Master Prompt):**
   ```text
   Forensic evidence macro photograph of an authentic antique 1920s Swiss yellow gold pocket watch with hunter case, resting on a clean neutral gray matte forensic examination surface. The closed lid features exquisite hand-engraved Art Deco floral rose scrollwork, and an oval cartouche with finely engraved initials 'T.Đ.H'. A delicate gold fob chain loosely curled beside the watch case. Next to the timepiece lies a black-and-white centimeter forensic scale ruler. Top-down view, soft even museum-grade studio lighting, subtle soft shadows, crisp sharp metallic texture, pristine macro 100mm lens detail, high-end antique collectible photography --ar 4:3 --v 6.0
   ```
5. **Negative Prompt:**
   ```text
   modern digital smartwatch, wrist watch with leather strap, dirty background, hands holding watch, cartoon, 3D CGI render, blurry, scratches, cheap brass, oversaturated yellow
   ```
6. **Tỷ lệ & Thông số kỹ thuật:** Khung hình **4:3**, định dạng WebP, xuất 800x600px (hoặc 1024x768px), dung lượng < 350 KB.

---

## 📊 BẢNG TỔNG HỢP TOÀN BỘ 5 TÀI NGUYÊN HÌNH ẢNH HỒ SƠ 00

| STT | Tài nguyên ảnh | Tên file xuất | Tỷ lệ | Định dạng | Vai trò hình sự trong hồ sơ vụ án | Vòng / Trọng điểm |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: |
| 1 | Ảnh bìa hộp hồ sơ | `images/cover.webp` | 3:4 | WebP | Bìa hộp boardgame trinh thám chính thức | Toàn bộ hồ sơ |
| 2 | Cửa sổ vỡ & Mảnh kính | `images/d01-window.webp` | 4:3 | WebP | Bằng chứng kính văng ra ngoài (Dàn dựng trộm) | Trọng điểm 1 (Báo chí) |
| 3 | Sơ đồ mặt bằng nhà số 17 | `images/d02-so-do-nha.webp` | 4:3 | WebP | Mặt bằng hiện trường, két sắt & vị trí chó canh | Trọng điểm 1 (Sơ đồ) |
| 4 | Trích xuất camera an ninh | `images/d07-camera.webp` | 4:3 | WebP | Bóng người mặc áo hoodie xám vào ngõ 22h53 | Trọng điểm 2 (Camera) |
| 5 | Đồng hồ bỏ túi vỏ vàng | `images/d08-watch.webp` | 4:3 | WebP | Tang vật thu giữ tại tiệm cầm đồ Phát Đạt | Trọng điểm 3 (Vật chứng) |
