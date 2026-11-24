import math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1200
# Forensic evidence tray / blue tarp background
img = Image.new("RGB", (W, H), "#233342")
draw = ImageDraw.Draw(img)

# Tarpaulin / forensic table texture (grid lines)
for x in range(0, W, 40):
    draw.line([(x, 0), (x, H)], fill="#2c3e50", width=1)
for y in range(0, H, 40):
    draw.line([(0, y), (W, y)], fill="#2c3e50", width=1)

# Fonts
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)

# 1. Top Bar
draw.rectangle([0, 0, W, 50], fill="#131c24")
draw.text((40, 25), "CÔNG AN TỈNH HÀ TÂY - BẢN ẢNH VẬT CHỨNG VỤ ÁN HÌNH SỰ SỐ 42/2004", fill="#e1b12c", font=font_bold, anchor="lm")
draw.text((W - 40, 25), "TANG VẬT THU GIỮ TẠI GÁC CHUÔNG CHÙA CỔ SƠN - NÚI SÀI SƠN (01/04/2004)", fill="#ffffff", font=font_small, anchor="rm")
draw.line([(0, 50), (W, 50)], fill="#e1b12c", width=2)

# 2. Main Evidence: Bamboo Water Rocker Cylinder (Ống bương tre dài 40cm)
# Placed diagonally on the forensic table
b_cx, b_cy = 760, 560
b_len = 650
b_rad = 55
angle = -0.32  # slight diagonal tilt

cos_a = math.cos(angle)
sin_a = math.sin(angle)

# Bamboo body shadow
s_off = 25
draw.line([(b_cx - b_len // 2 * cos_a + s_off, b_cy - b_len // 2 * sin_a + s_off),
           (b_cx + b_len // 2 * cos_a + s_off, b_cy + b_len // 2 * sin_a + s_off)], fill="#15202a", width=b_rad * 2 + 10)

# Bamboo body: yellowish-green mature bamboo stalk with nodes
# Draw the cylinder with segments
seg_colors = ["#7c9443", "#8da84c", "#9ab556", "#8da84c", "#7c9443"]
p_start = (b_cx - b_len // 2 * cos_a, b_cy - b_len // 2 * sin_a)
p_end = (b_cx + b_len // 2 * cos_a, b_cy + b_len // 2 * sin_a)

draw.line([p_start, p_end], fill="#8ba64e", width=b_rad * 2)

# Bamboo Nodes (mấu đốt tre)
for frac in [0.25, 0.55, 0.85]:
    nx = p_start[0] + (p_end[0] - p_start[0]) * frac
    ny = p_start[1] + (p_end[1] - p_start[1]) * frac
    # draw perpendicular ring
    r_dx = -sin_a * b_rad
    r_dy = cos_a * b_rad
    draw.line([(nx - r_dx, ny - r_dy), (nx + r_dx, ny + r_dy)], fill="#5c6e33", width=10)
    draw.line([(nx - r_dx, ny - r_dy), (nx + r_dx, ny + r_dy)], fill="#435223", width=4)

# Slanted cut open mouth (Cưa vát miệng ống tre) at the right end
# Right end is cut at 45 degrees
cut_x = p_end[0]
cut_y = p_end[1]
draw.ellipse([cut_x - 30, cut_y - b_rad, cut_x + 50, cut_y + b_rad], fill="#d5e3aa", outline="#435223", width=3)
# Hollow inner cavity
draw.ellipse([cut_x - 15, cut_y - b_rad + 12, cut_x + 35, cut_y + b_rad - 12], fill="#3a4521")

# Fresh white bamboo sap / milky resin droplets along cut edge (Nhựa mủ tre tươi mới cưa)
draw.circle((cut_x + 10, cut_y - 25), 6, fill="#fcfcf7")
draw.circle((cut_x + 25, cut_y + 10), 8, fill="#fcfcf7")
draw.circle((cut_x + 18, cut_y + 35), 5, fill="#fcfcf7")

# Wooden pivot axle drilled through center (Trục gỗ xuyên tâm bập bênh)
pivot_x = p_start[0] + (p_end[0] - p_start[0]) * 0.45
pivot_y = p_start[1] + (p_end[1] - p_start[1]) * 0.45
# Axle dowel extending above and below
axle_len = 120
ax_dx = -sin_a * axle_len
ax_dy = cos_a * axle_len
draw.line([(pivot_x - ax_dx, pivot_y - ax_dy), (pivot_x + ax_dx, pivot_y + ax_dy)], fill="#8a5b2d", width=14)
draw.circle((pivot_x, pivot_y), 10, fill="#38210c")


# 3. Mini Hand-Saw with fresh sawdust (Cưa tay mini dính mùn cưa) bottom left
saw_x, saw_y = 380, 840
# Wooden handle
draw.rounded_rectangle([saw_x - 100, saw_y - 20, saw_x, saw_y + 25], radius=8, fill="#78421c", outline="#3d1d07", width=2)
# Steel blade with teeth
draw.rectangle([saw_x, saw_y - 12, saw_x + 320, saw_y + 18], fill="#9ba8b5", outline="#475361", width=2)
# Saw teeth
for st_x in range(saw_x + 10, saw_x + 310, 8):
    draw.polygon([(st_x, saw_y + 18), (st_x + 4, saw_y + 28), (st_x + 8, saw_y + 18)], fill="#9ba8b5")

# Fresh bamboo sawdust powder scattered around saw blade
random.seed(88)
for _ in range(180):
    dx = random.randint(saw_x, saw_x + 300)
    dy = random.randint(saw_y - 25, saw_y + 55)
    draw.circle((dx, dy), random.randint(1, 2), fill="#d6ddaa")


# 4. Coil of Green Nylon Cord (Cuộn dây dù xanh lá cây) upper left
cord_cx, cord_cy = 380, 320
# Coiled loop rings
for r in range(120, 40, -14):
    draw.ellipse([cord_cx - r, cord_cy - r // 2, cord_cx + r, cord_cy + r // 2], outline="#1fa348", width=8)
    draw.ellipse([cord_cx - r + 3, cord_cy - r // 2 + 2, cord_cx + r - 3, cord_cy + r // 2 - 2], outline="#146c30", width=4)

# Tail of green cord extending towards the bamboo tail
draw.line([(cord_cx + 80, cord_cy + 20), (p_start[0] - 10, p_start[1] + 10)], fill="#22b851", width=6)


# 5. Evidence Markers & L-shaped Metric Scale
# Yellow Evidence Placard 01 (Ống tre)
draw.polygon([(b_cx - 20, b_cy - 160), (b_cx + 60, b_cy - 160), (b_cx + 50, b_cy - 100), (b_cx - 30, b_cy - 100)], fill="#f1c40f", outline="#b7950b", width=2)
draw.text((b_cx + 15, b_cy - 130), "01", fill="#111111", font=font_title, anchor="mm")

# Yellow Evidence Placard 02 (Cưa tay)
draw.polygon([(saw_x + 40, saw_y - 80), (saw_x + 110, saw_y - 80), (saw_x + 100, saw_y - 25), (saw_x + 30, saw_y - 25)], fill="#f1c40f", outline="#b7950b", width=2)
draw.text((saw_x + 70, saw_y - 52), "02", fill="#111111", font=font_title, anchor="mm")

# Yellow Evidence Placard 03 (Dây dù)
draw.polygon([(cord_cx - 30, cord_cy - 120), (cord_cx + 40, cord_cy - 120), (cord_cx + 30, cord_cy - 65), (cord_cx - 40, cord_cy - 65)], fill="#f1c40f", outline="#b7950b", width=2)
draw.text((cord_cx, cord_cy - 92), "03", fill="#111111", font=font_title, anchor="mm")

# Callout Annotations
draw.rectangle([980, 260, 1540, 390], fill="#111c26", outline="#22b851", width=2)
draw.text((1000, 285), "VẬT CHỨNG 01: ỐNG BƯƠNG TRE CƯA VÁT", fill="#4cdb7b", font=font_bold)
draw.text((1000, 315), "• Kích thước: Dài 40cm, đường kính 9.5cm, cưa vát miệng 45 độ.", fill="#ffffff", font=font_small)
draw.text((1000, 340), "• Khoan lỗ xuyên tâm lắp chốt quay bập bênh tích nước.", fill="#ffffff", font=font_small)
draw.text((1000, 365), "• Vết cưa rất mới, còn rỉ nhựa mủ tre tươi màu trắng sữa.", fill="#f1c40f", font=font_small)

draw.rectangle([980, 420, 1540, 530], fill="#111c26", outline="#1fa348", width=2)
draw.text((1000, 445), "VẬT CHỨNG 02 & 03: DÂY DÙ VÀ CƯA TAY", fill="#4cdb7b", font=font_bold)
draw.text((1000, 475), "• Dây dù xanh lá cây chịu lực trùng khớp với đoạn dây buộc trên chày chuông.", fill="#ffffff", font=font_small)
draw.text((1000, 500), "• Cưa tay mini chuôi gỗ dính mùn cưa tre tươi thu giữ trong bồ củi của Quảng Chân.", fill="#ffffff", font=font_small)

# L-shaped Forensic Metric Scale (Bottom Right)
sc_x, sc_y = 1100, 940
draw.line([(sc_x, sc_y), (sc_x, sc_y + 120)], fill="#ffffff", width=6)
draw.line([(sc_x, sc_y + 120), (sc_x + 240, sc_y + 120)], fill="#ffffff", width=6)
# Metric ticks
for i in range(0, 121, 20):
    draw.line([(sc_x - 8, sc_y + i), (sc_x + 8, sc_y + i)], fill="#ffffff", width=3)
for i in range(0, 241, 20):
    draw.line([(sc_x + i, sc_y + 112), (sc_x + i, sc_y + 128)], fill="#ffffff", width=3)
draw.text((sc_x + 120, sc_y + 145), "THƯỚC TỶ LỆ HÌNH SỰ (20 CM)", fill="#ffffff", font=font_small, anchor="mm")

# Bottom Official Evidence Card
draw.rectangle([60, H - 120, 850, H - 40], fill="#0e171f", outline="#526485", width=2)
draw.text((80, H - 98), "ĐƠN VỊ THU GIỮ: Đội Trọng án - Phòng CSHS (PC14) Công an tỉnh Hà Tây", fill="#ffffff", font=font_small)
draw.text((80, H - 72), "ĐỊA ĐIỂM: Giấu sau bệ tượng Hộ Pháp tầng 2 gác chuông chùa Cổ Sơn lúc 16h30 ngày 01/04/2004", fill="#99ccff", font=font_small)

# Save as WebP
out_path = "public/cases/hoi-chuong-chua-thay/images/d11-ong-tre.webp"
img.save(out_path, "WEBP", quality=90)
print(f"Generated {out_path} successfully!")
