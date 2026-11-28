# Ảnh cho "Ly trà tráo độc" (bản 2, hư cấu)

Bản 1 dựng theo vụ án có thật nên ảnh cũ (vận đơn, trích xuất điện thoại, camera quán, bìa có mặt và tên người thật) đã bị gỡ khỏi
`public/`. Không tạo lại các ảnh đó. Sơ đồ khoa Dược (d04) vẽ bằng code: `authoring/ly-tra-trao-doc/draw_so_do.py`.
Ảnh còn dùng: `d05-nap-coc.webp` (lỗ kim trên nắp, dùng cho d18).

## Ảnh thẻ (một ảnh ghép 3 cột × 2 hàng)

Cắt bằng: `python3 tools/crop-portraits.py <ảnh-ghép> public/cases/ly-tra-trao-doc/images 2 3 han nhung bao son tai -`
rồi `python3 authoring/ly-tra-trao-doc/build_case.py`.

```text
A 3-column by 2-row grid of six Vietnamese ID card portrait photos from 2016, separated by thin white lines, each cell a head-and-shoulders front-facing shot, neutral expression, plain pale blue background, flat studio lighting, realistic skin texture, no text.
Top row, left to right:
(1) a 27-year-old gentle young Vietnamese woman, round face, black hair tied back, light pink hospital staff uniform;
(2) a 41-year-old elegant Vietnamese businesswoman, sharp features, shoulder-length dark brown hair with soft waves, small pearl earrings, cream blazer over a black top;
(3) a 33-year-old Vietnamese male pharmacist, slim face, neat short side-parted hair, thin rectangular glasses, white lab coat over a light blue shirt.
Bottom row, left to right:
(4) a 45-year-old Vietnamese dock worker, broad tanned face, buzz-cut greying hair, thick eyebrows, faded navy work shirt;
(5) a 24-year-old Vietnamese delivery rider, boyish face, short messy hair, green delivery company polo shirt;
(6) an empty plain pale blue cell.
```

## Bìa (4:5, 1200×1500, dưới 400 KB, không chữ, một phần ba dưới tối và trống)

```text
Cinematic still life photograph at night inside a small hospital staff room in Vietnam, 2016: an old white refrigerator with its door half open, its interior light glowing cold blue-white; on the top shelf two plastic cups of milk tea with sealed film lids and round paper stickers, condensation droplets on the cups; one cup slightly apart from the other. On a steel desk in the foreground, out of focus, a printed thank-you card and a paper bag. Dim fluorescent corridor light through a frosted glass door. Clinical, quiet, ominous mood, teal and amber palette, 35mm film grain, realistic, no people, no text, no logos. Vertical 4:5, fridge and cups in the upper two thirds, dark floor and desk edge in the lower third.
```
Negative: `text, letters, logo, watermark, brand, poster, box mockup, people, blood, cartoon, 3D render, CGI, oversaturated`


## Ảnh tư liệu (tuỳ chọn, một ảnh ghép 2 × 2, mỗi ô ảnh ngang 4:3)

Cắt bằng: `python3 tools/crop-portraits.py <ảnh-ghép> public/cases/ly-tra-trao-doc/images 2 2 d01-benh-vien d15-camera-bai-xe d25-tang-vat-nha-bao d26-tang-vat-xe-lead --whole`
rồi báo để gắn vào d01, d15, d25, d26.

```text
A 2 by 2 grid of four separate realistic documentary photographs, each cell landscape 4:3, separated by thin white lines, Vietnam 2016, no readable text anywhere, no logos, no faces visible.
(1) top-left: daytime news photo of the gate of a small provincial Vietnamese district hospital, yellow colonial-style building, a few police officers and hospital staff in white coats standing near the entrance, motorbikes parked, overcast light, slightly grainy press photo look;
(2) top-right: grainy wide-angle washed-out colour security camera frame from above of a hospital back parking lot at 2:44 pm, a woman fully covered in a pink sun-protection jacket with hood, face mask and sunglasses, holding a paper bag, opening the passenger door of a red compact sedan, a white scooter parked beside it, timestamp-style blur but no readable digits;
(3) bottom-left: police evidence photo on a steel tray with a small numbered yellow marker: a small amber glass bottle with dark brown liquid, two 1 ml syringes with very thin needles, and a torn round paper sticker, forensic flash lighting, ruler at the edge without numbers;
(4) bottom-right: police evidence photo on a grey table: a folded pink hooded sun-protection jacket, dark sunglasses, a half-used roll of black tape, and an old smartphone with its SIM tray open, forensic flash lighting.
```
Negative: `text, letters, numbers, watermark, logo, brand names, blood, gore, cartoon, 3D render, CGI`
