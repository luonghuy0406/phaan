import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1200
img = Image.new("RGB", (W, H), "#f5f0e1")
draw = ImageDraw.Draw(img)

# 1. Technical Grid Lines
grid_minor = (235, 226, 206)
grid_major = (212, 199, 172)

for x in range(0, W, 20):
    c = grid_major if x % 100 == 0 else grid_minor
    draw.line([(x, 0), (x, H)], fill=c, width=1)
for y in range(0, H, 20):
    c = grid_major if y % 100 == 0 else grid_minor
    draw.line([(0, y), (W, y)], fill=c, width=1)

# Outer Borders
draw.rectangle([30, 30, W - 30, H - 30], outline="#1f2d48", width=3)
draw.rectangle([36, 36, W - 36, H - 36], outline="#526485", width=1)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 25)
font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)
font_micro = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 11)

# 2. Header
draw.text((60, 50), "CÔNG AN TỈNH HÀ TÂY - PHÒNG KỸ THUẬT HÌNH SỰ (PC21)", fill="#1f2d48", font=font_sub)
draw.text((60, 72), "TỔ GIÁM ĐỊNH DẤU VẾT CƠ HỌC - BIÊN BẢN THỰC NGHIỆM ĐIỀU TRA", fill="#1f2d48", font=font_sub)
draw.line([(60, 96), (620, 96)], fill="#1f2d48", width=1)

draw.text((W // 2, 65), "SƠ ĐỒ NGUYÊN LÝ CƠ HỌC THỦY LỰC ĐÁNH CHUÔNG TỰ ĐỘNG", fill="#8c1d18", font=font_title, anchor="mm")
draw.text((W // 2, 95), "CƠ CẤU BẬP BÊNH ỐNG TRE NHỎ GIỌT NGỤY TẠO BẰNG CHỨNG NGOẠI PHẠM LÚC 11H45", fill="#2a3b5c", font=font_sub, anchor="mm")
draw.text((W // 2, 118), "(Bản vẽ phục dựng nguyên lý cơ khí của hung thủ trên xà gác chuông chùa Cổ Sơn)", fill="#505f77", font=font_small, anchor="mm")

# 3. 4-STAGE MECHANICAL DIAGRAM PANELS (Divided into 4 quadrants/steps)
panel_w = 700
panel_h = 420

panels = [
    (60, 150, "BƯỚC 1: THIẾT LẬP CHỐT HÃM & MÁNG NƯỚC NHỎ GIỌT (09H45)", [
        "1. Chày gỗ lim nặng 30kg được kéo căng lệch góc 35 độ so với vành chuông.",
        "2. Đầu chày buộc dây dù xanh nối với chốt gỗ ngáng trên xà ngang.",
        "3. Ống bương tre 40cm đặt nằm nghiêng trên trục xoay gỗ xuyên tâm.",
        "4. Máng nước nhỏ từng giọt li ti (tốc độ đo đạc: 1 giọt / 1.5 giây)."
    ]),
    (840, 150, "BƯỚC 2: TÍCH TRỌNG LỰC TRONG 2 TIẾNG - HUNG THỦ XUỐNG NÚI (09H45 - 11H45)", [
        "1. Nước nhỏ giọt liên tục lấp đầy khoang trong của ống bương tre già.",
        "2. Trọng tâm của ống tre dần dịch chuyển từ phía đuôi về phía miệng vát.",
        "3. Trong 2 tiếng này, Quảng Chân xuống núi lúc 10h15 và ngồi ăn cơm",
        "   trưa cùng đoàn phật tử tại nhà khách (11h15 - 12h30) để tạo ngoại phạm."
    ]),
    (60, 600, "BƯỚC 3: MÔ-MEN LẬT ĐỘT NGỘT & GIẬT TUNG LẪY HÃM (ĐÚNG 11H45)", [
        "1. Lượng nước đạt ngưỡng ~1.2 lít, mô-men quay vượt qua điểm cân bằng.",
        "2. Ống tre bất ngờ lật úp chúc xuống, đổ ào toàn bộ nước xuống sàn gỗ lim.",
        "3. Phần đuôi ống tre bật mạnh lên, giật căng sợi dây dù xanh nối vào lẫy.",
        "4. Lẫy hãm chày gỗ lim bị giật tung khỏi khe ngáng trên xà gồ."
    ]),
    (840, 600, "BƯỚC 4: CHÀY VUNG QUÁN TÍNH ĐẬP VÀO ĐẠI HỒNG CHUNG (11H45)", [
        "1. Chày gỗ lim tự do vung mạnh theo quán tính đập vào thân chuông đồng.",
        "2. Sau cú va đập đầu tiên, chày dao động điều hòa đánh tiếp 2 nhịp phụ.",
        "3. Tiếng đại hồng chung ngân vang 3 hồi gián đoạn khắp thung lũng Sài Sơn.",
        "4. Phật tử dưới chân núi lầm tưởng sư trụ trì vẫn còn sống tự tay đánh chuông."
    ])
]

for px, py, ptitle, psteps in panels:
    draw.rectangle([px, py, px + panel_w, py + panel_h], fill="#ece4d0", outline="#202f4a", width=2)
    draw.rectangle([px, py, px + panel_w, py + 32], fill="#202f4a")
    draw.text((px + 12, py + 16), ptitle, fill="#ffffff", font=font_bold, anchor="lm")
    
    # Schematic Illustration Box inside panel
    diag_box = [px + 15, py + 42, px + panel_w - 15, py + 260]
    draw.rectangle(diag_box, fill="#ded3bc", outline="#526485", width=1)
    
    # Text explanation in lower half of panel
    tx_y = py + 275
    for step in psteps:
        draw.text((px + 20, tx_y), step, fill="#1c2838", font=font_small)
        tx_y += 24

# SPECIFIC DRAWINGS FOR EACH PANEL:

# Panel 1: Step 1 (Setting up)
p1_x, p1_y = 60 + 15, 150 + 42
# Bronze bell outline right
draw.ellipse([p1_x + 500, p1_y + 30, p1_x + 640, p1_y + 190], fill="#3d464d", outline="#1c2429", width=2)
# Hanging Mallet pulled back left
draw.line([(p1_x + 280, p1_y + 10), (p1_x + 280, p1_y + 110)], fill="#8a7356", width=4)
draw.rounded_rectangle([p1_x + 220, p1_y + 90, p1_x + 400, p1_y + 130], radius=10, fill="#694021", outline="#2b1a0e", width=2)
# Wooden latch holding it back
draw.rectangle([p1_x + 210, p1_y + 80, p1_x + 225, p1_y + 140], fill="#c5221f", outline="#8c1d18", width=2)
draw.text((p1_x + 190, p1_y + 60), "LẪY GỖ HÃM CHÀY", fill="#c5221f", font=font_small)
# Bamboo pipe on pivot
draw.line([(p1_x + 80, p1_y + 150), (p1_x + 80, p1_y + 180)], fill="#2b1a0e", width=6)
draw.circle((p1_x + 80, p1_y + 150), 6, fill="#c5221f")
# Bamboo angled up
draw.line([(p1_x + 30, p1_y + 165), (p1_x + 140, p1_y + 130)], fill="#829c3a", width=14)
# Water dropper above
draw.rectangle([p1_x + 120, p1_y + 40, p1_x + 160, p1_y + 80], fill="#5b7f95", outline="#233e50", width=2)
draw.text((p1_x + 140, p1_y + 30), "BÁT NƯỚC", fill="#233e50", font=font_small, anchor="mm")
draw.ellipse([p1_x + 138, p1_y + 95, p1_x + 142, p1_y + 105], fill="#4da3d4")
# Green cord connecting bamboo tail to latch
draw.line([(p1_x + 30, p1_y + 165), (p1_x + 210, p1_y + 110)], fill="#1fa348", width=3)


# Panel 2: Step 2 (Filling water)
p2_x, p2_y = 840 + 15, 150 + 42
draw.ellipse([p2_x + 500, p2_y + 30, p2_x + 640, p2_y + 190], fill="#3d464d", outline="#1c2429", width=2)
draw.rounded_rectangle([p2_x + 220, p2_y + 90, p2_x + 400, p2_y + 130], radius=10, fill="#694021", outline="#2b1a0e", width=2)
# Bamboo almost horizontal now due to water weight
draw.line([(p2_x + 80, p2_y + 150), (p2_x + 80, p2_y + 180)], fill="#2b1a0e", width=6)
draw.circle((p2_x + 80, p2_y + 150), 6, fill="#c5221f")
draw.line([(p2_x + 20, p2_y + 155), (p2_x + 150, p2_y + 145)], fill="#829c3a", width=14)
# Blue water filling inside
draw.line([(p2_x + 80, p2_y + 145), (p2_x + 145, p2_y + 145)], fill="#2980b9", width=8)
draw.text((p2_x + 110, p2_y + 120), "NƯỚC ĐẦY 95%", fill="#2980b9", font=font_bold, anchor="mm")
draw.text((p2_x + 300, p2_y + 60), "THỜI GIAN CHỜ: 2 TIẾNG ĐỒNG HỒ", fill="#8c1d18", font=font_bold, anchor="mm")


# Panel 3: Step 3 (Tripping trigger)
p3_x, p3_y = 60 + 15, 600 + 42
draw.ellipse([p3_x + 500, p3_y + 30, p3_x + 640, p3_y + 190], fill="#3d464d", outline="#1c2429", width=2)
# Bamboo tilted down, water spilling
draw.line([(p3_x + 80, p3_y + 150), (p3_x + 80, p3_y + 180)], fill="#2b1a0e", width=6)
draw.circle((p3_x + 80, p3_y + 150), 6, fill="#c5221f")
# Tilted steeply down
draw.line([(p3_x + 30, p3_y + 105), (p3_x + 140, p3_y + 185)], fill="#829c3a", width=14)
# Water splash onto ground
draw.ellipse([p3_x + 120, p3_y + 180, p3_x + 200, p3_y + 205], fill="#4da3d4")
draw.text((p3_x + 160, p3_y + 215), "VŨNG NƯỚC ĐỔ", fill="#2980b9", font=font_small, anchor="mm")
# Green cord pulling latch away!
draw.line([(p3_x + 30, p3_y + 105), (p3_x + 180, p3_y + 70)], fill="#1fa348", width=3)
# Latch flying off
draw.rectangle([p3_x + 180, p3_y + 60, p3_x + 195, p3_y + 80], fill="#c5221f", outline="#8c1d18", width=2)
draw.text((p3_x + 240, p3_y + 50), "LÃY GỖ BỊ GIẬT TUNG!", fill="#c5221f", font=font_bold, anchor="mm")


# Panel 4: Step 4 (Striking Bell)
p4_x, p4_y = 840 + 15, 600 + 42
draw.ellipse([p4_x + 500, p4_y + 30, p4_x + 640, p4_y + 190], fill="#3d464d", outline="#1c2429", width=2)
# Mallet slamming right into the bell!
draw.line([(p4_x + 380, p4_y + 10), (p4_x + 440, p4_y + 110)], fill="#8a7356", width=4)
draw.rounded_rectangle([p4_x + 340, p4_y + 90, p4_x + 520, p4_y + 130], radius=10, fill="#694021", outline="#2b1a0e", width=2)
# Sound Waves bursting from point of impact
for r in [20, 45, 75]:
    draw.arc([p4_x + 500 - r, p4_y + 110 - r, p4_x + 500 + r, p4_y + 110 + r], start=-60, end=60, fill="#f39c12", width=3)
draw.text((p4_x + 580, p4_y + 110), "BOOONG! (11H45)", fill="#c0392b", font=font_bold, anchor="lm")
draw.text((p4_x + 300, p4_y + 180), "TIẾNG CHUÔNG NGÂN VANG ĐÚNG GIỜ NGỌ", fill="#8c1d18", font=font_bold, anchor="mm")


# 5. BOTTOM SUMMARY BAR & STAMP
sum_y = H - 150
draw.rectangle([60, sum_y, W - 60, H - 55], fill="#ffffff", outline="#202f4a", width=2)
draw.text((80, sum_y + 25), "KẾT LUẬN THỰC NGHIỆM ĐIỀU TRA CỦA PHÒNG KỸ THUẬT HÌNH SỰ (PC21 HÀ TÂY):", fill="#8c1d18", font=font_bold)
draw.text((80, sum_y + 55), "• Khẳng định 100% tiếng chuông chùa lúc 11h45 được kích hoạt bởi cơ cấu bập bênh thủy lực, hoàn toàn không cần sự hiện diện của con người tại thời điểm phát chuông.", fill="#1f2d48", font=font_small)
draw.text((80, sum_y + 75), "• Bằng chứng ngoại phạm của nghi phạm Quảng Chân (ngồi ăn cơm lúc 11h15–12h30 dưới chân núi) bị vô hiệu hóa hoàn toàn bởi khoa học hình sự.", fill="#1f2d48", font=font_small)

# Red stamp PC21
stamp_cx, stamp_cy = W - 140, sum_y + 50
draw.circle((stamp_cx, stamp_cy), 36, outline="#d32f2f", width=2)
draw.text((stamp_cx, stamp_cy - 10), "KỸ THUẬT HÌNH SỰ", fill="#d32f2f", font=font_micro, anchor="mm")
draw.text((stamp_cx, stamp_cy + 5), "PC21 HÀ TÂY", fill="#d32f2f", font=font_bold, anchor="mm")

# Save as WebP
out_path = "public/cases/hoi-chuong-chua-thay/images/d08-so-do-co-hoc.webp"
img.save(out_path, "WEBP", quality=90)
print(f"Generated {out_path} successfully!")
