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
draw.text((60, 50), "CÔNG AN THÀNH PHỐ HÀ NỘI - PHÒNG CẢNH SÁT HÌNH SỰ (PC14)", fill="#1f2d48", font=font_sub)
draw.text((60, 72), "ĐỘI ĐIỀU TRA TRỌNG ÁN - BIÊN BẢN KHÁM NGHIỆM HIỆN TRƯỜNG SỐ 88/1999", fill="#1f2d48", font=font_sub)
draw.line([(60, 96), (620, 96)], fill="#1f2d48", width=1)

draw.text((W // 2, 65), "SƠ ĐỒ HIỆN TRƯỜNG VỤ CƯỚP VŨ TRANG TIỆM VÀNG KIM SINH", fill="#8c1d18", font=font_title, anchor="mm")
draw.text((W // 2, 95), "SỐ 38 PHỐ TÂY SƠN, PHƯỜNG QUANG TRUNG, QUẬN ĐỐNG ĐA, HÀ NỘI", fill="#2a3b5c", font=font_sub, anchor="mm")
draw.text((W // 2, 118), "(Khám nghiệm hồi 01h30 ngày 19/07/1999 - Đo vẽ thực địa tỷ lệ 1:200)", fill="#505f77", font=font_small, anchor="mm")

# North Arrow top right
cx, cy = W - 140, 110
draw.circle((cx, cy), 32, outline="#1f2d48", width=2)
draw.line([(cx, cy - 42), (cx, cy + 42)], fill="#1f2d48", width=2)
draw.line([(cx - 42, cy), (cx + 42, cy)], fill="#1f2d48", width=2)
draw.polygon([(cx, cy - 40), (cx - 7, cy - 7), (cx + 7, cy - 7)], fill="#8c1d18")
draw.polygon([(cx, cy + 40), (cx - 7, cy + 7), (cx + 7, cy + 7)], fill="#1f2d48")
draw.text((cx, cy - 54), "BẮC (N)", fill="#8c1d18", font=font_bold, anchor="mm")

# 3. DRAWING PLAN
# Street: Phố Tây Sơn at bottom
street_top = H - 220
draw.rectangle([60, street_top, W - 60, H - 90], fill="#e5ddcb", outline="#6e624e", width=2)
draw.text((W // 2, street_top + 45), "PHỐ TÂY SƠN (MẶT ĐƯỜNG RỘNG 16M)", fill="#544738", font=font_title, anchor="mm")
draw.text((W // 2, street_top + 80), "Vỉa hè lát gạch rộng 4 mét • Hướng đi gò Đống Đa và Ngã Tư Sở", fill="#756755", font=font_small, anchor="mm")

# Tiệm vàng Kim Sinh (Số 38 Tây Sơn)
store_x = 220
store_y = street_top - 340
store_w = 440
store_h = 340

draw.rectangle([store_x, store_y, store_x + store_w, store_y + store_h], fill="#dfd4bc", outline="#202f4a", width=3)

# Inside tiệm vàng:
# Gian trước: Quầy giao dịch và tủ kính trưng bày
draw.line([(store_x, store_y + 200), (store_x + store_w, store_y + 200)], fill="#202f4a", width=2)
draw.text((store_x + store_w // 2, store_y + 30), "GIAN TRONG & KHO BẢO QUẢN", fill="#202f4a", font=font_bold, anchor="mm")
draw.text((store_x + store_w // 2, store_y + 285), "TIỆM VÀNG KIM SINH (SỐ 38 TÂY SƠN)", fill="#202f4a", font=font_bold, anchor="mm")
draw.text((store_x + store_w // 2, store_y + 310), "Cửa sắt xếp mặt phố bị giật tung", fill="#627084", font=font_small, anchor="mm")

# [A] Shattered glass gold jewelry counter
counter_x = store_x + 120
counter_y = store_y + 215
counter_w = 200
counter_h = 50
draw.rectangle([counter_x, counter_y, counter_x + counter_w, counter_y + counter_h], fill="#ffd9d9", outline="#c5221f", width=2)
draw.text((counter_x + counter_w // 2, counter_y + 16), "[A] TỦ KÍNH BỊ ĐẬP VỠ", fill="#c5221f", font=font_bold, anchor="mm")
draw.text((counter_x + counter_w // 2, counter_y + 34), "(Cướp 100 lượng vàng ta & vệt máu bảo vệ)", fill="#8c1d18", font=font_small, anchor="mm")

# [B] 3 Spent K54 bullet casings on floor
casing_x = store_x + 60
casing_y = store_y + 240
draw.circle((casing_x, casing_y), 6, fill="#b58900", outline="#6e5200")
draw.circle((casing_x + 16, casing_y + 8), 6, fill="#b58900", outline="#6e5200")
draw.circle((casing_x + 8, casing_y + 22), 6, fill="#b58900", outline="#6e5200")
draw.rectangle([casing_x - 30, casing_y - 45, casing_x + 120, casing_y - 12], fill="#fff9db", outline="#b58900", width=1)
draw.text((casing_x + 45, casing_y - 28), "[B] 3 VỎ ĐẠN ĐỒNG K54", fill="#8a6700", font=font_bold, anchor="mm")

# Bullet hole in wooden pillar
draw.rectangle([store_x + 360, store_y + 230, store_x + 390, store_y + 260], fill="#5c4533", outline="#202f4a", width=2)
draw.text((store_x + 375, store_y + 215), "VẾT ĐẠN CHÌ", fill="#8c1d18", font=font_small, anchor="mm")

# Back Exit Door [D] (Cửa ngách hậu ra ngõ chùa Đồng Quang)
door_x = store_x + 80
door_y = store_y
draw.rectangle([door_x - 20, door_y - 6, door_x + 20, door_y + 6], fill="#ffffff", outline="#202f4a", width=2)
draw.text((door_x, door_y - 20), "[D] CỬA NGÁCH HẬU", fill="#8c1d18", font=font_bold, anchor="mm")
draw.text((door_x, door_y - 6), "Lối kẻ cướp tẩu thoát", fill="#505f77", font=font_small, anchor="mm")

# 4. Ngõ chùa Đồng Quang (Escape route alley to Đặng Tiến Đông)
alley_pts = [
    (door_x, door_y),
    (door_x, door_y - 140),
    (door_x + 320, door_y - 140),
    (door_x + 320, door_y - 300),
    (door_x + 720, door_y - 300),
    (door_x + 720, door_y - 380),
    (door_x + 920, door_y - 380)
]

# Corridor
w_half = 28
for i in range(len(alley_pts) - 1):
    p1, p2 = alley_pts[i], alley_pts[i + 1]
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

# Dashed Red Escape Line
for i in range(len(alley_pts) - 1):
    p1, p2 = alley_pts[i], alley_pts[i + 1]
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

# Arrow heads
def draw_arrow(cx, cy, angle_rad):
    l = 14
    w = 8
    p_tip = (cx + l * math.cos(angle_rad), cy + l * math.sin(angle_rad))
    p_left = (cx - w * math.sin(angle_rad), cy + w * math.cos(angle_rad))
    p_right = (cx + w * math.sin(angle_rad), cy - w * math.cos(angle_rad))
    draw.polygon([p_tip, p_left, p_right], fill="#c62828")

draw_arrow(door_x, door_y - 70, -math.pi / 2)
draw_arrow(door_x + 160, door_y - 140, 0)
draw_arrow(door_x + 320, door_y - 220, -math.pi / 2)
draw_arrow(door_x + 520, door_y - 300, 0)
draw_arrow(door_x + 820, door_y - 380, 0)

# [C] 30m Evidence Point: Cigarette Pack & Ferry Ticket Stub
ev_x = door_x + 180
ev_y = door_y - 140
draw.circle((ev_x, ev_y), 10, fill="#2e7d32", outline="#1b5e20", width=2)
draw.rectangle([ev_x - 30, ev_y + 20, ev_x + 230, ev_y + 80], fill="#e8f5e9", outline="#2e7d32", width=2)
draw.text((ev_x + 100, ev_y + 36), "[C] TANG VẬT BỊ ĐÁNH RƠI (CÁCH CỬA 30M)", fill="#1b5e20", font=font_bold, anchor="mm")
draw.text((ev_x + 100, ev_y + 55), "• Vỏ bao thuốc lá Du Lịch in dấu vân tay hung thủ", fill="#2e7d32", font=font_small, anchor="mm")
draw.text((ev_x + 100, ev_y + 70), "• Cuống vé qua phà Đen in ngày 18/07/1999", fill="#505f77", font=font_small, anchor="mm")

# Alley label
draw.text((door_x + 460, door_y - 270), "NGÕ CHÙA ĐỒNG QUANG (NGÕ HẸP TỐI TĂM ĐÊM MƯA BÃO)", fill="#8c1d18", font=font_bold, anchor="mm")

# Destination: Đường Đặng Tiến Đông & Bến phà Đen
dest_x = door_x + 920
dest_y = door_y - 380
draw.rectangle([dest_x, dest_y - 60, dest_x + 200, dest_y + 60], fill="#e5ddcb", outline="#6e624e", width=2)
draw.text((dest_x + 100, dest_y - 15), "ĐƯỜNG ĐẶNG TIẾN ĐÔNG", fill="#202f4a", font=font_bold, anchor="mm")
draw.text((dest_x + 100, dest_y + 10), "--> Hướng ra đê sông Hồng", fill="#c62828", font=font_small, anchor="mm")
draw.text((dest_x + 100, dest_y + 28), "vượt Bến phà Đen sang Gia Lâm", fill="#505f77", font=font_small, anchor="mm")


# 5. LEGEND BOX bottom right
leg_x1 = W - 540
leg_y1 = H - 470
leg_w = 480
leg_h = 230
draw.rectangle([leg_x1, leg_y1, leg_x1 + leg_w, leg_y1 + leg_h], fill="#ffffff", outline="#202f4a", width=2)
draw.rectangle([leg_x1, leg_y1, leg_x1 + leg_w, leg_y1 + 35], fill="#202f4a")
draw.text((leg_x1 + 15, leg_y1 + 18), "BẢNG CHÚ GIẢI KỸ THUẬT HÌNH SỰ (PC14 HÀ NỘI)", fill="#ffffff", font=font_bold, anchor="lm")

legends = [
    ("[A]", "#c5221f", "Tủ kính quầy vàng bị đập vỡ, cướp 100 lượng vàng ta"),
    ("[B]", "#8a6700", "Cụm 3 vỏ đạn súng ngắn K54 dập 1968 & đầu đạn chì biến dạng"),
    ("[C]", "#1b5e20", "Vỏ bao thuốc lá Du Lịch có vân tay & cuống vé phà Đen"),
    ("[D]", "#8c1d18", "Cửa ngách hậu thông ra ngõ chùa Đồng Quang (lối tẩu thoát)"),
    ("-->", "#c62828", "Tuyến đường tháo chạy trong đêm mưa bằng xe máy Simson")
]

for idx, (code, col, desc) in enumerate(legends):
    y_pos = leg_y1 + 55 + idx * 30
    draw.text((leg_x1 + 15, y_pos), code, fill=col, font=font_bold)
    draw.text((leg_x1 + 60, y_pos), desc, fill="#1f2d48", font=font_small)

# 6. SIGNATURE & STAMP bottom left
sig_x = 70
sig_y = H - 150
draw.text((sig_x, sig_y), "CÁN BỘ ĐIỀU TRA KHÁM NGHIỆM TỬ THI & HIỆN TRƯỜNG", fill="#1f2d48", font=font_bold)
draw.text((sig_x, sig_y + 22), "Thiếu tá: PHẠM VĂN ĐỨC (Đội Trọng án PC14 Hà Nội)", fill="#4f5d75", font=font_small)

# Red Stamp
stamp_cx, stamp_cy = sig_x + 340, sig_y + 20
draw.circle((stamp_cx, stamp_cy), 42, outline="#d32f2f", width=3)
draw.circle((stamp_cx, stamp_cy), 38, outline="#d32f2f", width=1)
draw.text((stamp_cx, stamp_cy - 16), "CÔNG AN THÀNH PHỐ", fill="#d32f2f", font=font_small, anchor="mm")
draw.text((stamp_cx, stamp_cy), "HÀ NỘI", fill="#d32f2f", font=font_bold, anchor="mm")
draw.text((stamp_cx, stamp_cy + 16), "★ PHÒNG PC14 ★", fill="#d32f2f", font=font_small, anchor="mm")

# Scale Bar
bar_x = W - 320
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
out_path = "public/cases/dem-sung-no-tay-son/images/d04-so-do-hien-truong.webp"
img.save(out_path, "WEBP", quality=90)
print(f"Generated {out_path} successfully!")
