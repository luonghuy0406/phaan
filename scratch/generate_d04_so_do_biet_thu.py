import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1200
# Classic forensic case file blueprint paper (aged cream technical paper)
img = Image.new("RGB", (W, H), "#f5f0e2")
draw = ImageDraw.Draw(img)

# 1. Technical Grid Lines
grid_minor = (236, 228, 210)
grid_major = (215, 202, 178)

for x in range(0, W, 20):
    c = grid_major if x % 100 == 0 else grid_minor
    draw.line([(x, 0), (x, H)], fill=c, width=1)
for y in range(0, H, 20):
    c = grid_major if y % 100 == 0 else grid_minor
    draw.line([(0, y), (W, y)], fill=c, width=1)

# Outer Border
draw.rectangle([30, 30, W - 30, H - 30], outline="#1c2c48", width=3)
draw.rectangle([36, 36, W - 36, H - 36], outline="#4a5d7c", width=1)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_label = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 11)

# 2. Header
draw.text((60, 50), "BOULDER POLICE DEPARTMENT - CRIMINAL INVESTIGATION DIVISION", fill="#1c2c48", font=font_sub)
draw.text((60, 72), "HỒ SƠ ĐIỀU TRA TRỌNG ÁN: VỤ ÁN JONBENÉT RAMSEY (CASE NO: 96-6232)", fill="#1c2c48", font=font_sub)
draw.line([(60, 96), (620, 96)], fill="#1c2c48", width=1)

draw.text((W // 2, 65), "SƠ ĐỒ MẶT BẰNG HIỆN TRƯỜNG BIỆT THỰ RAMSEY", fill="#8c1d18", font=font_title, anchor="mm")
draw.text((W // 2, 95), "755 15TH STREET, BOULDER, COLORADO - ĐO VẼ HỒI 08H00 NGÀY 26/12/1996", fill="#2a3b5c", font=font_sub, anchor="mm")
draw.text((W // 2, 118), "(Chi tiết phân bố vết tích: Tầng trệt, Cầu thang xoắn & Tầng hầm chứa rượu)", fill="#505f77", font=font_small, anchor="mm")

# North Arrow top right
cx, cy = W - 140, 110
draw.circle((cx, cy), 32, outline="#1c2c48", width=2)
draw.line([(cx, cy - 42), (cx, cy + 42)], fill="#1c2c48", width=2)
draw.line([(cx - 42, cy), (cx + 42, cy)], fill="#1c2c48", width=2)
draw.polygon([(cx, cy - 40), (cx - 7, cy - 7), (cx + 7, cy - 7)], fill="#8c1d18")
draw.polygon([(cx, cy + 40), (cx - 7, cy + 7), (cx + 7, cy + 7)], fill="#1c2c48")
draw.text((cx, cy - 54), "NORTH (BẮC)", fill="#8c1d18", font=font_bold, anchor="mm")

# 3. PLAN 1: TẦNG TRỆT (GROUND FLOOR) - Left Side
gf_x1, gf_y1 = 60, 160
gf_w, gf_h = 680, 560
draw.rectangle([gf_x1, gf_y1, gf_x1 + gf_w, gf_y1 + gf_h], fill="#ece4d0", outline="#1c2c48", width=2)
draw.rectangle([gf_x1, gf_y1, gf_x1 + gf_w, gf_y1 + 35], fill="#1c2c48")
draw.text((gf_x1 + 15, gf_y1 + 18), "MẶT BẰNG TẦNG TRỆT (GROUND FLOOR) - KHÔNG GIAN SINH HOẠT", fill="#ffffff", font=font_bold, anchor="lm")

# Rooms in Ground Floor
# Living Room (Front Left)
draw.rectangle([gf_x1 + 20, gf_y1 + 55, gf_x1 + 320, gf_y1 + 260], fill="#dfd4bc", outline="#3a4b66", width=2)
draw.text((gf_x1 + 170, gf_y1 + 140), "PHÒNG KHÁCH CHÍNH\n(LIVING ROOM)", fill="#25354e", font=font_bold, anchor="mm")
draw.text((gf_x1 + 170, gf_y1 + 180), "Cây thông Noel & quà Giáng sinh", fill="#627084", font=font_small, anchor="mm")

# Formal Dining Room (Front Right)
draw.rectangle([gf_x1 + 340, gf_y1 + 55, gf_x1 + 660, gf_y1 + 260], fill="#dfd4bc", outline="#3a4b66", width=2)
draw.text((gf_x1 + 500, gf_y1 + 140), "PHÒNG ĂN LỚN\n(FORMAL DINING)", fill="#25354e", font=font_bold, anchor="mm")

# Kitchen & Breakfast Nook (Back Right)
draw.rectangle([gf_x1 + 340, gf_y1 + 280, gf_x1 + 660, gf_y1 + 540], fill="#e5dac3", outline="#3a4b66", width=2)
draw.text((gf_x1 + 500, gf_y1 + 390), "BẾP & PHÒNG ĂN PHỤ (KITCHEN)", fill="#25354e", font=font_bold, anchor="mm")

# [D] Bàn ăn phụ có bát dứa
bowl_x, bowl_y = gf_x1 + 450, gf_y1 + 450
draw.rectangle([bowl_x, bowl_y, bowl_x + 100, bowl_y + 60], fill="#fff2db", outline="#b27300", width=2)
draw.circle((bowl_x + 50, bowl_y + 30), 16, fill="#ffe299", outline="#b27300", width=1)
draw.text((bowl_x + 50, bowl_y + 15), "[D] BÁT DỨA TƯƠI", fill="#b27300", font=font_bold, anchor="mm")
draw.text((bowl_x + 50, bowl_y + 46), "(ADN của Burke & mẹ)", fill="#7a5200", font=font_small, anchor="mm")

# Main Hallway & Spiral Staircase (Back Left)
draw.rectangle([gf_x1 + 20, gf_y1 + 280, gf_x1 + 320, gf_y1 + 540], fill="#dfd4bc", outline="#3a4b66", width=2)
draw.text((gf_x1 + 170, gf_y1 + 330), "SẢNH TRUNG TÂM & HÀNH LANG", fill="#25354e", font=font_bold, anchor="mm")

# Spiral Staircase [A]
stair_x, stair_y = gf_x1 + 100, gf_y1 + 400
for r in range(45, 10, -8):
    draw.circle((stair_x, stair_y), r, outline="#8c1d18", width=1)
draw.circle((stair_x, stair_y), 50, outline="#8c1d18", width=2)
draw.text((stair_x, stair_y), "CẦU THANG\nXOẮN", fill="#8c1d18", font=font_small, anchor="mm")

# Label [A]
draw.rectangle([stair_x - 70, stair_y + 58, stair_x + 130, stair_y + 115], fill="#fff0f0", outline="#c5221f", width=2)
draw.text((stair_x + 30, stair_y + 72), "[A] NƠI ĐẶT BỨC THƯ TỐNG TIỀN", fill="#c5221f", font=font_bold, anchor="mm")
draw.text((stair_x + 30, stair_y + 92), "3 trang thư viết tay đặt trên bậc thang thứ ba", fill="#8c1d18", font=font_small, anchor="mm")
draw.text((stair_x + 30, stair_y + 106), "Cạnh cuốn sổ tay xé rách của mẹ Patsy", fill="#505f77", font=font_small, anchor="mm")


# 4. PLAN 2: TẦNG HẦM (BASEMENT PLAN) - Right Side
bm_x1, bm_y1 = W - 740, 160
bm_w, bm_h = 680, 560
draw.rectangle([bm_x1, bm_y1, bm_x1 + bm_w, bm_y1 + bm_h], fill="#e8dfcb", outline="#1c2c48", width=2)
draw.rectangle([bm_x1, bm_y1, bm_x1 + bm_w, bm_y1 + 35], fill="#1c2c48")
draw.text((bm_x1 + 15, bm_y1 + 18), "MẶT BẰNG TẦNG HẦM (BASEMENT) - NƠI PHÁT HIỆN THI THỂ", fill="#ffffff", font=font_bold, anchor="lm")

# Rooms in Basement
# Train hobby room (Front Left)
draw.rectangle([bm_x1 + 20, bm_y1 + 55, bm_x1 + 340, bm_y1 + 280], fill="#dbcfb8", outline="#3a4b66", width=2)
draw.text((bm_x1 + 180, bm_y1 + 140), "PHÒNG ĐỒ CHƠI XE LỬA\n(TRAIN HOBBY ROOM)", fill="#25354e", font=font_bold, anchor="mm")
draw.text((bm_x1 + 180, bm_y1 + 180), "Bàn mô hình đường ray của hai đứa trẻ", fill="#627084", font=font_small, anchor="mm")

# Basement Window [B]
win_x, win_y = bm_x1 + 180, bm_y1 + 55
draw.rectangle([win_x - 60, win_y - 8, win_x + 60, win_y + 8], fill="#ffffff", outline="#2b78e4", width=2)
draw.rectangle([win_x - 120, win_y - 45, win_x + 120, win_y - 12], fill="#f0f6ff", outline="#2b78e4", width=1)
draw.text((win_x, win_y - 34), "[B] CỬA SỔ HẦM: Ô KÍNH VỠ", fill="#1a56b0", font=font_bold, anchor="mm")
draw.text((win_x, win_y - 20), "Mạng nhện còn nguyên vẹn, không dấu chân trên tuyết", fill="#1a56b0", font=font_small, anchor="mm")

# Boiler & Storage (Right side)
draw.rectangle([bm_x1 + 360, bm_y1 + 55, bm_x1 + 660, bm_y1 + 300], fill="#dbcfb8", outline="#3a4b66", width=2)
draw.text((bm_x1 + 510, bm_y1 + 150), "PHÒNG NỒI HƠI & KHO KỸ THUẬT\n(BOILER & STORAGE)", fill="#25354e", font=font_bold, anchor="mm")

# Corridor leading to wine cellar
draw.rectangle([bm_x1 + 20, bm_y1 + 300, bm_x1 + 380, bm_y1 + 540], fill="#dbcfb8", outline="#3a4b66", width=2)
draw.text((bm_x1 + 200, bm_y1 + 420), "HÀNH LANG TẦNG HẦM TỐI TĂM", fill="#25354e", font=font_bold, anchor="mm")

# WINE CELLAR [C] (Back right corner - hidden room)
wc_x1, wc_y1 = bm_x1 + 400, bm_y1 + 320
wc_w, wc_h = 260, 220
draw.rectangle([wc_x1, wc_y1, wc_x1 + wc_w, wc_y1 + wc_h], fill="#c9b99e", outline="#8c1d18", width=3)
draw.text((wc_x1 + wc_w // 2, wc_y1 + 40), "HẦM CHỨA RƯỢU (WINE CELLAR)", fill="#8c1d18", font=font_bold, anchor="mm")
draw.text((wc_x1 + wc_w // 2, wc_y1 + 65), "Cửa gỗ then cài then gỗ ngoài", fill="#505f77", font=font_small, anchor="mm")

# Victim location [C]
vic_x, vic_y = wc_x1 + wc_w // 2, wc_y1 + 130
draw.rectangle([vic_x - 90, vic_y - 25, vic_x + 90, vic_y + 40], fill="#fff0f0", outline="#c5221f", width=2)
draw.text((vic_x, vic_y - 8), "[C] VỊ TRÍ TÌM THẤY THI THỂ", fill="#c5221f", font=font_bold, anchor="mm")
draw.text((vic_x, vic_y + 12), "Cô bé JonBenét (6 tuổi) bị trùm chăn trắng", fill="#8c1d18", font=font_small, anchor="mm")
draw.text((vic_x, vic_y + 26), "Miệng dán băng keo đen dính sợi len đỏ tía", fill="#505f77", font=font_small, anchor="mm")


# 5. LEGEND & FORENSIC ANALYSIS SUMMARY - Bottom Full Width
leg_y = 745
draw.rectangle([60, leg_y, W - 60, H - 70], fill="#ffffff", outline="#1c2c48", width=2)
draw.rectangle([60, leg_y, W - 60, leg_y + 35], fill="#1c2c48")
draw.text((80, leg_y + 18), "BẢNG TỔNG HỢP VẬT CHỨNG HIỆN TRƯỜNG & KẾT LUẬN CỦA ĐỘI ĐIỀU TRA BOULDER POLICE", fill="#ffffff", font=font_bold, anchor="lm")

col1_x = 90
col2_x = W // 2 + 30

rows_col1 = [
    ("[A] Bậc thang xoắn thứ ba:", "#c5221f", "Nơi tìm thấy bức thư tống tiền dài 3 trang viết tay bằng bút dạ đen của người mẹ Patsy."),
    ("[B] Cửa sổ tầng hầm vỡ:", "#1a56b0", "Mạng nhện phủ kín khung cửa sổ không hề đứt rách; không hề có dấu vết đột nhập (No Forced Entry)."),
    ("[C] Hầm chứa rượu góc khuất:", "#c5221f", "Phòng kín sâu trong hầm nơi người cha John dẫn thẳng bạn bè xuống tìm thấy xác con gái lúc 13h05.")
]

rows_col2 = [
    ("[D] Bàn bếp ăn dở:", "#b27300", "Bát dứa tươi và trà có dấu vân tay vi thể của Burke và mẹ, chứng minh nạn nhân đã ăn trước khi chết."),
    ("[E] Lớp tuyết dày quanh nhà:", "#1c2c48", "Đêm Giáng sinh bão tuyết; quanh toàn bộ biệt thự 15 phòng không hề có dấu chân người lạ bên ngoài."),
    ("★ KẾT LUẬN HIỆN TRƯỜNG:", "#8c1d18", "Hiện trường khép kín hoàn toàn; thủ phạm và người dàn dựng bức thư tống tiền là người sống trong nhà.")
]

for idx, (code, col, desc) in enumerate(rows_col1):
    yp = leg_y + 60 + idx * 55
    draw.text((col1_x, yp), code, fill=col, font=font_bold)
    draw.text((col1_x, yp + 20), desc, fill="#25354e", font=font_label)

for idx, (code, col, desc) in enumerate(rows_col2):
    yp = leg_y + 60 + idx * 55
    draw.text((col2_x, yp), code, fill=col, font=font_bold)
    draw.text((col2_x, yp + 20), desc, fill="#25354e", font=font_label)

# Scale & Signatures at bottom
draw.line([(60, H - 110), (W - 60, H - 110)], fill="#d0c7b2", width=1)
draw.text((90, H - 90), "DETECTIVE LINDA ARNDT - LEAD CRIME SCENE INVESTIGATOR", fill="#505f77", font=font_small)
draw.text((W - 90, H - 90), "CONFIDENTIAL - LAW ENFORCEMENT EVIDENCE ARCHIVE (DEC 1996)", fill="#505f77", font=font_small, anchor="ra")

# Save as WebP
out_path = "public/cases/buc-thu-dem-tuyet-trang/images/d04-so-do-biet-thu.webp"
img.save(out_path, "WEBP", quality=90)
print(f"Generated {out_path} successfully!")
