import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1200
img = Image.new("RGB", (W, H), "#f6f1e2")
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

# 2. Header
draw.text((60, 50), "CÔNG AN TỈNH HÀ TÂY - PHÒNG CẢNH SÁT HÌNH SỰ (PC14)", fill="#1f2d48", font=font_sub)
draw.text((60, 72), "ĐỘI KHÁM NGHIỆM HIỆN TRƯỜNG & PHÁP Y - BIÊN BẢN SỐ 42/2004", fill="#1f2d48", font=font_sub)
draw.line([(60, 96), (620, 96)], fill="#1f2d48", width=1)

draw.text((W // 2, 65), "SƠ ĐỒ HIỆN TRƯỜNG KHUÔN VIÊN CHÙA CỔ SƠN - NÚI SÀI SƠN", fill="#8c1d18", font=font_title, anchor="mm")
draw.text((W // 2, 95), "ĐỊA BÀN XÃ SÀI SƠN, HUYỆN QUỐC OAI, TỈNH HÀ TÂY", fill="#2a3b5c", font=font_sub, anchor="mm")
draw.text((W // 2, 118), "(Khám nghiệm hồi 14h00 ngày 01/04/2004 - Đo vẽ thực địa tỷ lệ 1:250)", fill="#505f77", font=font_small, anchor="mm")

# North Arrow top right
cx, cy = W - 140, 110
draw.circle((cx, cy), 32, outline="#1f2d48", width=2)
draw.line([(cx, cy - 42), (cx, cy + 42)], fill="#1f2d48", width=2)
draw.line([(cx - 42, cy), (cx + 42, cy)], fill="#1f2d48", width=2)
draw.polygon([(cx, cy - 40), (cx - 7, cy - 7), (cx + 7, cy - 7)], fill="#8c1d18")
draw.polygon([(cx, cy + 40), (cx - 7, cy + 7), (cx + 7, cy + 7)], fill="#1f2d48")
draw.text((cx, cy - 54), "BẮC (N)", fill="#8c1d18", font=font_bold, anchor="mm")

# 3. DRAWING MAIN PLAN
# Zone A: Chân núi (Nhà khách & Bếp ăn phật tử) - Bottom Left
# Zone B: 300 bậc đá tam cấp (Stairs up the mountain)
# Zone C: Đỉnh núi (Tam Bảo, Gác Chuông, Tịnh Thất Sư Trụ Trì)

# 3.1 Chân núi Sài Sơn (Bottom Left)
bot_x1, bot_y1 = 60, H - 260
bot_w, bot_h = 440, 170
draw.rectangle([bot_x1, bot_y1, bot_x1 + bot_w, bot_y1 + bot_h], fill="#e5ddcb", outline="#6e624e", width=2)
draw.text((bot_x1 + bot_w // 2, bot_y1 + 30), "[E] KHU VỰC CHÂN NÚI SÀI SƠN", fill="#202f4a", font=font_bold, anchor="mm")
draw.rectangle([bot_x1 + 30, bot_y1 + 55, bot_x1 + 210, bot_y1 + 140], fill="#dbcfb8", outline="#202f4a", width=2)
draw.text((bot_x1 + 120, bot_y1 + 90), "BẾP ĂN PHẬT TỬ\n(Bà Nga nấu cơm)", fill="#202f4a", font=font_small, anchor="mm")

draw.rectangle([bot_x1 + 230, bot_y1 + 55, bot_x1 + 410, bot_y1 + 140], fill="#dbcfb8", outline="#202f4a", width=2)
draw.text((bot_x1 + 320, bot_y1 + 80), "NHÀ KHÁCH CHÙA", fill="#202f4a", font=font_bold, anchor="mm")
draw.text((bot_x1 + 320, bot_y1 + 105), "Nơi Quảng Chân ăn cơm\ntrưa 11h15 - 12h30", fill="#8c1d18", font=font_small, anchor="mm")

# 3.2 Đỉnh núi Sài Sơn (Top Right & Middle: Chùa Cổ Sơn)
top_x1, top_y1 = 520, 160
top_w, top_h = 1020, 560
draw.rectangle([top_x1, top_y1, top_x1 + top_w, top_y1 + top_h], fill="#ece4d0", outline="#1c2c48", width=2)
draw.rectangle([top_x1, top_y1, top_x1 + top_w, top_y1 + 35], fill="#1c2c48")
draw.text((top_x1 + 15, top_y1 + 18), "KHUÔN VIÊN CHÙA CỔ SƠN TRÊN ĐỈNH NÚI ĐÁ VÔI SÀI SƠN", fill="#ffffff", font=font_bold, anchor="lm")

# Cliff edge (Vách đá dựng đứng)
draw.line([(top_x1, top_y1 + top_h - 40), (top_x1 + top_w, top_y1 + top_h - 40)], fill="#7a6b57", width=3)
draw.text((top_x1 + top_w // 2, top_y1 + top_h - 20), "VÁCH NÚI ĐÁ VÔI HIỂM TRỞ DỰNG ĐỨNG - KHÔNG THỂ LEO TRÈO BÊN NGOÀI", fill="#5a4933", font=font_small, anchor="mm")

# 1. Tam Bảo Chính Điện (Chính giữa)
tb_x1, tb_y1 = top_x1 + 360, top_y1 + 70
tb_w, tb_h = 320, 240
draw.rectangle([tb_x1, tb_y1, tb_x1 + tb_w, tb_y1 + tb_h], fill="#dfd4bc", outline="#202f4a", width=2)
draw.text((tb_x1 + tb_w // 2, tb_y1 + 40), "TÒA CHÍNH ĐIỆN (TAM BẢO)", fill="#202f4a", font=font_bold, anchor="mm")
draw.rectangle([tb_x1 + 60, tb_y1 + 75, tb_x1 + tb_w - 60, tb_y1 + 145], fill="#b39d7b", outline="#202f4a", width=2)
draw.text((tb_x1 + tb_w // 2, tb_y1 + 110), "BỆ THỜ TAM THẾ PHẬT", fill="#ffffff", font=font_bold, anchor="mm")
draw.text((tb_x1 + tb_w // 2, tb_y1 + 190), "Hành lang gạch Bát Tràng cổ kính", fill="#627084", font=font_small, anchor="mm")

# 2. Gác Chuông Cổ [A] (Phía Tây Chính Điện - Left)
gc_x1, gc_y1 = top_x1 + 60, top_y1 + 90
gc_w, gc_h = 240, 220
draw.rectangle([gc_x1, gc_y1, gc_x1 + gc_w, gc_y1 + gc_h], fill="#dfd4bc", outline="#8c1d18", width=3)
draw.text((gc_x1 + gc_w // 2, gc_y1 + 35), "[A] GÁC CHUÔNG 2 TẦNG", fill="#8c1d18", font=font_bold, anchor="mm")

# Big Bronze Bell inside Gác Chuông
draw.circle((gc_x1 + gc_w // 2, gc_y1 + 115), 38, fill="#474f54", outline="#1c2429", width=2)
draw.text((gc_x1 + gc_w // 2, gc_y1 + 115), "ĐẠI HỒNG\nCHUNG", fill="#ffffff", font=font_small, anchor="mm")

# Mallet & Trigger details
draw.line([(gc_x1 + gc_w // 2 - 50, gc_y1 + 115), (gc_x1 + gc_w // 2 - 10, gc_y1 + 115)], fill="#7a4218", width=8)
draw.text((gc_x1 + gc_w // 2, gc_y1 + 175), "Vũng nước rỉ & dây dù xanh", fill="#1b5e20", font=font_bold, anchor="mm")
draw.text((gc_x1 + gc_w // 2, gc_y1 + 195), "(Cơ cấu bập bênh nhỏ giọt hẹn giờ)", fill="#505f77", font=font_small, anchor="mm")

# 3. Tịnh thất Am thiền [B] & [C] (Phía Đông Chính Điện - Right)
tt_x1, tt_y1 = top_x1 + 740, top_y1 + 90
tt_w, tt_h = 240, 220
draw.rectangle([tt_x1, tt_y1, tt_x1 + tt_w, tt_y1 + tt_h], fill="#dfd4bc", outline="#8c1d18", width=3)
draw.text((tt_x1 + tt_w // 2, tt_y1 + 35), "TỊNH THẤT AM THIỀN", fill="#8c1d18", font=font_bold, anchor="mm")

# Altar with stolen golden Buddha statue [C]
alt_x = tt_x1 + 30
alt_y = tt_y1 + 65
draw.rectangle([alt_x, alt_y, alt_x + 180, alt_y + 40], fill="#fff2db", outline="#b27300", width=2)
draw.text((alt_x + 90, alt_y + 20), "[C] NƠI MẤT TƯỢNG VÀNG", fill="#b27300", font=font_bold, anchor="mm")

# Crime scene: Sư trụ trì [B]
bed_x = tt_x1 + 30
bed_y = tt_y1 + 120
draw.rectangle([bed_x, bed_y, bed_x + 180, bed_y + 70], fill="#ffd9d9", outline="#c5221f", width=2)
draw.text((bed_x + 90, bed_y + 25), "[B] NƠI PHÁT HIỆN THI THỂ", fill="#c5221f", font=font_bold, anchor="mm")
draw.text((bed_x + 90, bed_y + 48), "Đại đức Thích Tâm Viên bị siết cổ", fill="#8c1d18", font=font_small, anchor="mm")

# 3.3 300 Bậc đá tam cấp nối chân núi lên đỉnh núi [D]
stair_pts = [
    (bot_x1 + bot_w - 40, bot_y1 + 30),
    (bot_x1 + bot_w + 60, bot_y1 - 60),
    (bot_x1 + bot_w + 60, bot_y1 - 180),
    (top_x1 + 180, top_y1 + top_h - 40)
]

for i in range(len(stair_pts) - 1):
    p1, p2 = stair_pts[i], stair_pts[i + 1]
    # Draw stairs path
    draw.line([p1, p2], fill="#968974", width=22)
    # Step notches
    dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    steps = int(dist // 14)
    for s in range(steps):
        t = s / steps
        sx = p1[0] + (p2[0] - p1[0]) * t
        sy = p1[1] + (p2[1] - p1[1]) * t
        draw.line([(sx - 8, sy), (sx + 8, sy)], fill="#5c5344", width=2)

draw.rectangle([bot_x1 + bot_w + 80, bot_y1 - 120, bot_x1 + bot_w + 340, bot_y1 - 40], fill="#ffffff", outline="#5c5344", width=1)
draw.text((bot_x1 + bot_w + 210, bot_y1 - 95), "[D] 300 BẬC ĐÁ TAM CẤP", fill="#5c5344", font=font_bold, anchor="mm")
draw.text((bot_x1 + bot_w + 210, bot_y1 - 75), "Đường độc đạo • Đi bộ mất 25–30 phút", fill="#8c1d18", font=font_small, anchor="mm")
draw.text((bot_x1 + bot_w + 210, bot_y1 - 58), "Quảng Chân xuống núi lúc 10h15", fill="#505f77", font=font_small, anchor="mm")


# 4. LEGEND BOX Bottom Right
leg_x1 = 540
leg_y1 = H - 430
leg_w = W - 600
leg_h = 240
draw.rectangle([leg_x1, leg_y1, leg_x1 + leg_w, leg_y1 + leg_h], fill="#ffffff", outline="#202f4a", width=2)
draw.rectangle([leg_x1, leg_y1, leg_x1 + leg_w, leg_y1 + 35], fill="#202f4a")
draw.text((leg_x1 + 15, leg_y1 + 18), "BẢNG CHÚ GIẢI KỸ THUẬT HÌNH SỰ (PC14 CÔNG AN TỈNH HÀ TÂY)", fill="#ffffff", font=font_bold, anchor="lm")

legends = [
    ("[A]", "#8c1d18", "Gác chuông tầng 2: Đại hồng chung & vũng nước nhỏ giọt hẹn giờ 11h45"),
    ("[B]", "#c5221f", "Tịnh thất am thiền: Vị trí phát hiện thi thể sư trụ trì Thích Tâm Viên"),
    ("[C]", "#b27300", "Mật thất tịnh thất: Nơi pho tượng Phật cổ dát vàng bị lấy cắp"),
    ("[D]", "#5c5344", "300 bậc đá tam cấp: Lối đi bộ độc đạo duy nhất lên chùa (mất 25-30 phút di chuyển)"),
    ("[E]", "#202f4a", "Chân núi Sài Sơn: Nơi nghi phạm Quảng Chân ngồi ăn cơm tạo chứng cứ ngoại phạm giả")
]

for idx, (code, col, desc) in enumerate(legends):
    y_pos = leg_y1 + 55 + idx * 34
    draw.text((leg_x1 + 15, y_pos), code, fill=col, font=font_bold)
    draw.text((leg_x1 + 60, y_pos), desc, fill="#1f2d48", font=font_small)

# 5. SIGNATURE & STAMP bottom left
sig_x = 70
sig_y = H - 80
draw.text((sig_x, sig_y), "CÁN BỘ ĐO VẼ HIỆN TRƯỜNG: Trung tá TRẦN ĐĂNG KHOA (PC14 Hà Tây)", fill="#1f2d48", font=font_small)

# Red Stamp
stamp_cx, stamp_cy = 440, H - 75
draw.circle((stamp_cx, stamp_cy), 35, outline="#d32f2f", width=2)
draw.text((stamp_cx, stamp_cy - 10), "CÔNG AN TỈNH", fill="#d32f2f", font=font_small, anchor="mm")
draw.text((stamp_cx, stamp_cy + 5), "HÀ TÂY", fill="#d32f2f", font=font_bold, anchor="mm")

# Scale Bar
bar_x = W - 300
bar_y = H - 65
draw.text((bar_x, bar_y - 18), "THƯỚC TỶ LỆ ĐO VẼ", fill="#1f2d48", font=font_small)
draw.rectangle([bar_x, bar_y, bar_x + 200, bar_y + 8], fill="#ffffff", outline="#1f2d48", width=1)
draw.rectangle([bar_x, bar_y, bar_x + 50, bar_y + 8], fill="#1f2d48")
draw.rectangle([bar_x + 100, bar_y, bar_x + 150, bar_y + 8], fill="#1f2d48")
draw.text((bar_x, bar_y + 14), "0m", fill="#1f2d48", font=font_small, anchor="mm")
draw.text((bar_x + 50, bar_y + 14), "10m", fill="#1f2d48", font=font_small, anchor="mm")
draw.text((bar_x + 100, bar_y + 14), "20m", fill="#1f2d48", font=font_small, anchor="mm")
draw.text((bar_x + 200, bar_y + 14), "50m", fill="#1f2d48", font=font_small, anchor="mm")

# Save as WebP
out_path = "public/cases/hoi-chuong-chua-thay/images/d03-so-do-chua.webp"
img.save(out_path, "WEBP", quality=90)
print(f"Generated {out_path} successfully!")
