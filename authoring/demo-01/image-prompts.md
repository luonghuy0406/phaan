# Ảnh hồ sơ demo-01 (tạo ngày 23/11/2026)

Công cụ: Hugging Face MCP → Space `mcp-tools/FLUX.1-Krea-dev`, 28 bước, guidance 4.5.
Lưu ở `public/cases/demo-01/images/` (WebP, quality 82). Ảnh cũ vẽ bằng script nằm ở `authoring/demo-01/anh-cu/`.
Dùng lại đúng seed + prompt + kích thước để tạo lại y hệt ảnh.

| File | Kích thước | Seed | Manh mối phải thấy |
|---|---|---|---|
| `cover.webp` | 768×960 | 17026138 | (bìa) đồng hồ vàng, cửa sổ vỡ, không lộ hung thủ |
| `d01-window.webp` | 1024×640 | 1252863959 | **mảnh kính nằm trên sân, phía ngoài cửa sổ** (kính bị đập từ bên trong) |
| `d07-camera.webp` | 1024×768 | 1115219607 | người mặc **hoodie xám**, đi vào ngõ, không thấy mặt |
| `d08-watch.webp` | 1024×768 | 1460526144 | đồng hồ bỏ túi **vàng**, vỏ chạm hoa |

## Prompt

**cover.webp**
> Moody editorial photograph, old Hanoi townhouse study at night, antique gold pocket watch with ornate engraved case lying open on a dark wooden desk, behind it a window with one shattered glass pane, cold blue streetlight through the window, warm desk lamp glow, film grain, shallow depth of field, 50mm f/1.8, muted warm tones, no text, no people

**d01-window.webp**
> Documentary press photograph 2024, exterior of an old Hanoi tube house back courtyard in morning light, a wooden study window with one broken glass pane, many glass shards scattered on the courtyard tiles directly below outside the window, mossy wall, potted plants, overcast soft light, 35mm lens, realistic, no people, no text, no signs

**d07-camera.webp**
> CCTV still, high angle from a wall-mounted camera, narrow residential alley at night between plain painted house walls and closed iron gates, wet concrete, potted bougainvillea, tangled overhead cables, a single dim streetlamp, one person in a plain grey hoodie with hood up walking away down the alley, grainy low resolution security footage, blue-grey tint, vignette, plain walls

**d08-watch.webp**
> Forensic evidence photograph, a single antique yellow gold pocket watch with closed hunter case, ornate floral engraving and a small blank oval cartouche on the lid, gold chain loosely coiled, lying on plain grey matte paper, top-down view, soft even studio lighting, subtle shadow, macro 100mm lens, crisp metal texture, minimal clean composition

## Kinh nghiệm với FLUX.1 Krea
- Mô hình rất hay tự thêm **chữ vô nghĩa** vào biển hiệu, phiếu giấy, thước đo. Câu "no text" không đủ: phải **bỏ hẳn vật có chữ khỏi khung hình**
  (hẻm nhà ở thay vì dãy cửa hàng; chỉ chụp đồng hồ, không kèm phiếu cầm đồ).
- 2 lần tạo bị loại vì có chữ: camera có biển hiệu, tang vật có phiếu "PWN" và thước có số.
- Ảnh bài báo bị trang web tự chuyển sang đen trắng, nên chi tiết manh mối phải rõ cả khi không có màu.
