import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1200
img = Image.new("RGB", (W, H), "#f6f1e3")
draw = ImageDraw.Draw(img)

# 1. Grid lines (technical millimeter paper)
grid_color_minor = (235, 226, 206)
grid_color_major = (212, 199, 172)

for x in range(0, W, 20):
    c = grid_color_major if x % 100 == 0 else grid_color_minor
    draw.line([(x, 0), (x, H)], fill=c, width=1)
for y in range(0, H, 20):
    c = grid_color_major if y % 100 == 0 else grid_color_minor
    draw.line([(0, y), (W, y)], fill=c, width=1)

# Outer technical border
draw.rectangle([30, 30, W - 30, H - 30], outline="#2a3b5c", width=3)
draw.rectangle([36, 36, W - 36, H - 36], outline="#526485", width=1)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
font_label_lg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
font_label = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)

# 2. Header
draw.text((60, 50), "CÔNG AN TỈNH QUẢNG NAM - CÔNG AN THỊ XÃ HỘI AN", fill="#1f2d48", font=font_sub)
draw.text((60, 72), "ĐỘI CẢNH SÁT ĐIỀU TRA TỘI PHẠM VỀ TRẬT TỰ XÃ HỘI", fill="#1f2d48", font=font_sub)
draw.line([(60, 96), (460, 96)], fill="#1f2d48", width=1)

draw.text((W // 2, 65), "SƠ ĐỒ HIỆN TRƯỜNG KHU VỰC VỤ ÁN TRỘM CỔ VẬT", fill="#8c1d18", font=font_title, anchor="mm")
draw.text((W // 2, 98), "LỐI ĐỘT NHẬP & TẨU TÁN TỪ TỪ ĐƯỜNG HỌ LƯƠNG RA GIẾNG CỔ BÁ LỄ", fill="#2a3b5c", font=font_sub, anchor="mm")
draw.text((W // 2, 122), "(Đo vẽ thực địa hồi 15h00 ngày 19/08/2005 - Tỷ lệ 1:200)", fill="#4f5d75", font=font_small, anchor="mm")

# 3. North Arrow (Compass Rose) top right
cx, cy = W - 140, 110
draw.circle((cx, cy), 35, outline="#2a3b5c", width=2)
draw.line([(cx, cy - 45), (cx, cy + 45)], fill="#2a3b5c", width=2)
draw.line([(cx - 45, cy), (cx + 45, cy)], fill="#2a3b5c", width=2)
draw.polygon([(cx, cy - 43), (cx - 8, cy - 8), (cx + 8, cy - 8)], fill="#8c1d18")
draw.polygon([(cx, cy + 43), (cx - 8, cy + 8), (cx + 8, cy + 8)], fill="#2a3b5c")
draw.text((cx, cy - 58), "BẮC (N)", fill="#8c1d18", font=font_bold, anchor="mm")

# 4. DRAWING MAIN PLAN
# Zone A: Đường Trần Phú (Phía dưới)
# Zone B: Từ đường họ Lương
# Zone C: Ngõ nhỏ 80m
# Zone D: Giếng cổ Bá Lễ

# 4.1 Đường Trần Phú (Front street at bottom)
street_top = H - 220
draw.rectangle([60, street_top, W - 60, H - 90], fill="#e8dfcb", outline="#726650", width=2)
draw.text((W // 2, street_top + 45), "ĐƯỜNG TRẦN PHÚ (PHỐ CỔ HỘI AN)", fill="#544738", font=font_title, anchor="mm")
draw.text((W // 2, street_top + 80), "Lòng đường lát đá cổ & vỉa hè gạch thẻ - Cửa trước từ đường khóa chốt trong", fill="#756755", font=font_small, anchor="mm")

# 4.2 Từ đường họ Lương (Ancestral Hall)
# Center x around 450, y from street_top - 320 to street_top
th_w = 400
th_h = 240
th_x1 = 250
th_y1 = street_top - th_h
th_x2 = th_x1 + th_w
th_y2 = street_top

draw.rectangle([th_x1, th_y1, th_x2, th_y2], fill="#ded3bc", outline="#243450", width=3)
# Sub-rooms:
# Front room
draw.line([(th_x1, th_y1 + 100), (th_x2, th_y1 + 100)], fill="#243450", width=2)
draw.text((th_x1 + th_w // 2, th_y1 + 170), "TIỀN ĐƯỜNG (SỐ 48 TRẦN PHÚ)", fill="#1e2c44", font=font_bold, anchor="mm")
draw.text((th_x1 + th_w // 2, th_y1 + 195), "Cửa chính gỗ lim - Khóa then cài phía trong", fill="#505f77", font=font_small, anchor="mm")

# Main altar room (Gian chính thờ tổ)
draw.text((th_x1 + th_w // 2, th_y1 + 45), "GIAN CHÍNH TỪ ĐƯỜNG HỌ LƯƠNG", fill="#1e2c44", font=font_bold, anchor="mm")

# Altar
altar_x1, altar_y1 = th_x1 + 120, th_y1 + 15
draw.rectangle([altar_x1, altar_y1, altar_x1 + 160, altar_y1 + 40], fill="#b39d7b", outline="#1e2c44", width=2)
draw.text((altar_x1 + 80, altar_y1 + 20), "BÀN THỜ TỔ", fill="#ffffff", font=font_bold, anchor="mm")

# Painting wall location [A]
p_x1, p_y1 = th_x1 + 130, th_y1 + 5
draw.rectangle([p_x1, p_y1, p_x1 + 140, p_y1 + 10], fill="#d32f2f", outline="#8c1d18", width=1)
draw.rectangle([p_x1 - 10, p_y1 - 18, p_x1 + 150, p_y1 + 2], fill="#fff2f2", outline="#d32f2f", width=1)
draw.text((p_x1 + 70, p_y1 - 8), "[A] VỊ TRÍ TREO TRANH LỤA CỔ", fill="#d32f2f", font=font_bold, anchor="mm")

# Back door [B] (Cửa hậu)
door_x = th_x1 + 60
door_y = th_y1
draw.rectangle([door_x - 20, door_y - 6, door_x + 20, door_y + 6], fill="#fff", outline="#243450", width=2)
draw.text((door_x, door_y - 20), "[B] CỬA HẬU", fill="#8c1d18", font=font_bold, anchor="mm")
draw.text((door_x + 60, door_y - 20), "(Ổ khóa Việt Tiệp không cạy phá)", fill="#505f77", font=font_small)

# 4.3 The narrow alleyway (Ngõ nhỏ 80 mét lát gạch thẻ)
# Path from (door_x, door_y) zigzagging up and right to Ba Le Well
pts = [
    (door_x, door_y),
    (door_x, door_y - 120),
    (door_x + 250, door_y - 120),
    (door_x + 250, door_y - 300),
    (door_x + 650, door_y - 300),
    (door_x + 650, door_y - 380),
    (door_x + 850, door_y - 380)
]

# Draw alley corridor (walls on both sides, 40px wide)
w_half = 26
corridor_polys = []
for i in range(len(pts) - 1):
    p1, p2 = pts[i], pts[i + 1]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    nx = -dy / dist * w_half
    ny = dx / dist * w_half
    poly = [
        (p1[0] + nx, p1[1] + ny),
        (p2[0] + nx, p2[1] + ny),
        (p2[0] - nx, p2[1] - ny),
        (p1[0] - nx, p1[1] - ny)
    ]
    draw.polygon(poly, fill="#ebd9c0", outline="#b09e85")

# Draw red dashed movement line of culprit
for i in range(len(pts) - 1):
    p1, p2 = pts[i], pts[i + 1]
    # dashed
    dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    steps = int(dist // 16)
    for s in range(steps):
        if s % 2 == 0:
            t1 = s / steps
            t2 = min(1.0, (s + 0.7) / steps)
            x1 = p1[0] + (p2[0] - p1[0]) * t1
            y1 = p1[1] + (p2[1] - p1[1]) * t1
            x2 = p1[0] + (p2[0] - p1[0]) * t2
            y2 = p1[1] + (p2[1] - p1[1]) * t2
            draw.line([(x1, y1), (x2, y2)], fill="#c62828", width=3)

# Arrow heads along the path
def draw_arrow(cx, cy, angle_rad):
    l = 14
    w = 8
    p_tip = (cx + l * math.cos(angle_rad), cy + l * math.sin(angle_rad))
    p_left = (cx - w * math.sin(angle_rad), cy + w * math.cos(angle_rad))
    p_right = (cx + w * math.sin(angle_rad), cy - w * math.cos(angle_rad))
    draw.polygon([p_tip, p_left, p_right], fill="#c62828")

draw_arrow(door_x, door_y - 60, -math.pi / 2)
draw_arrow(door_x + 130, door_y - 120, 0)
draw_arrow(door_x + 250, door_y - 210, -math.pi / 2)
draw_arrow(door_x + 460, door_y - 300, 0)
draw_arrow(door_x + 750, door_y - 380, 0)

# Annotation for alley
draw.text((door_x + 350, door_y - 270), "[C] NGÕ NHỎ LÁT GẠCH THẺ (DÀI 80 MÉT)", fill="#8c1d18", font=font_bold, anchor="mm")
draw.text((door_x + 350, door_y - 250), "Lối đi quanh co giữa các tường nhà cổ, vắng bóng người lúc trưa rằm", fill="#4f5d75", font=font_small, anchor="mm")

# 4.4 Khu vực Giếng cổ Bá Lễ [D]
well_cx = door_x + 850
well_cy = door_y - 380

# Well area surround
draw.rectangle([well_cx - 100, well_cy - 90, well_cx + 120, well_cy + 90], fill="#dcd7c7", outline="#54637a", width=2)
# Ancient stone well (Square Champa brick outer, circular inner)
draw.rectangle([well_cx - 40, well_cy - 40, well_cx + 40, well_cy + 40], fill="#b3aa94", outline="#243450", width=3)
draw.circle((well_cx, well_cy), 32, fill="#7496ab", outline="#243450", width=2)
draw.text((well_cx, well_cy), "NƯỚC\nSÂU 3M", fill="#ffffff", font=font_small, anchor="mm")

# Slippery stone steps [E]
step_x = well_cx - 85
draw.rectangle([step_x, well_cy - 30, step_x + 35, well_cy + 30], fill="#a3b899", outline="#3b5930", width=2)
draw.text((step_x + 18, well_cy), "BẬC\nĐÁ", fill="#233a1c", font=font_small, anchor="mm")

# Well labels
draw.text((well_cx, well_cy - 65), "[D] GIẾNG CỔ BÁ LỄ", fill="#8c1d18", font=font_bold, anchor="mm")
draw.text((well_cx, well_cy - 48), "(Ống nhựa chứa tranh giấu chìm đáy giếng)", fill="#1e2c44", font=font_small, anchor="mm")

draw.text((step_x + 18, well_cy + 45), "[E] DẤU GIÀY & BÙN VÀNG", fill="#3b5930", font=font_bold, anchor="mm")
draw.text((step_x + 18, well_cy + 62), "(Trùng khớp giày thể thao của Bảo)", fill="#505f77", font=font_small, anchor="mm")

# 5. LEGEND BOX (Bảng chú giải) bottom right
leg_x1 = W - 520
leg_y1 = H - 460
leg_w = 460
leg_h = 220
draw.rectangle([leg_x1, leg_y1, leg_x1 + leg_w, leg_y1 + leg_h], fill="#ffffff", outline="#243450", width=2)
draw.rectangle([leg_x1, leg_y1, leg_x1 + leg_w, leg_y1 + 35], fill="#243450")
draw.text((leg_x1 + 15, leg_y1 + 18), "BẢNG CHÚ GIẢI KỸ THUẬT HÌNH SỰ", fill="#ffffff", font=font_bold, anchor="lm")

legends = [
    ("[A]", "#d32f2f", "Vị trí bức tranh lụa cổ 'Thập mục ngưu đồ' bị đánh cắp"),
    ("[B]", "#8c1d18", "Cửa hậu từ đường họ Lương (mở bằng chìa khóa riêng)"),
    ("[C]", "#8c1d18", "Ngõ ngách 80m nối từ đường với khu dân cư giếng cổ"),
    ("[D]", "#1e2c44", "Giếng Bá Lễ: Nơi thả chìm ống nhựa PVC phi 90 chứa tranh"),
    ("[E]", "#3b5930", "Bậc đá xanh: Vệt bùn vàng phù sa & dấu vân đế giày thể thao"),
    ("-->", "#c62828", "Tuyến đường di chuyển tẩu tán tài sản của thủ phạm (11h45)")
]

for idx, (code, col, desc) in enumerate(legends):
    y_pos = leg_y1 + 55 + idx * 26
    draw.text((leg_x1 + 15, y_pos), code, fill=col, font=font_bold)
    draw.text((leg_x1 + 60, y_pos), desc, fill="#1f2d48", font=font_small)

# 6. SIGNATURE & STAMP BOX bottom left
sig_x = 70
sig_y = H - 150
draw.text((sig_x, sig_y), "CÁN BỘ KHÁM NGHIỆM ĐO VẼ", fill="#1f2d48", font=font_bold)
draw.text((sig_x, sig_y + 22), "Đại úy: LÊ THANH HẢI (Ký & ghi rõ họ tên)", fill="#4f5d75", font=font_small)

# Red official seal stamp
stamp_cx, stamp_cy = sig_x + 300, sig_y + 20
draw.circle((stamp_cx, stamp_cy), 42, outline="#d32f2f", width=3)
draw.circle((stamp_cx, stamp_cy), 38, outline="#d32f2f", width=1)
draw.text((stamp_cx, stamp_cy - 16), "CÔNG AN THỊ XÃ", fill="#d32f2f", font=font_small, anchor="mm")
draw.text((stamp_cx, stamp_cy), "HỘI AN", fill="#d32f2f", font=font_bold, anchor="mm")
draw.text((stamp_cx, stamp_cy + 16), "★ QUẢNG NAM ★", fill="#d32f2f", font=font_small, anchor="mm")

# Scale Bar
bar_x = W - 320
bar_y = H - 65
draw.text((bar_x, bar_y - 18), "THƯỚC TỶ LỆ ĐO ĐẠC", fill="#1f2d48", font=font_small)
draw.rectangle([bar_x, bar_y, bar_x + 200, bar_y + 8], fill="#ffffff", outline="#1f2d48", width=1)
draw.rectangle([bar_x, bar_y, bar_x + 50, bar_y + 8], fill="#1f2d48")
draw.rectangle([bar_x + 100, bar_y, bar_x + 150, bar_y + 8], fill="#1f2d48")
draw.text((bar_x, bar_y + 14), "0m", fill="#1f2d48", font=font_small, anchor="mm")
draw.text((bar_x + 50, bar_y + 14), "20m", fill="#1f2d48", font=font_small, anchor="mm")
draw.text((bar_x + 100, bar_y + 14), "40m", fill="#1f2d48", font=font_small, anchor="mm")
draw.text((bar_x + 200, bar_y + 14), "80m", fill="#1f2d48", font=font_small, anchor="mm")

# Save as WebP
out_path = "public/cases/bong-nang-hoi-an/images/d04-so-do-tu-duong.webp"
img.save(out_path, "WEBP", quality=90)
print(f"Generated {out_path} successfully!")
