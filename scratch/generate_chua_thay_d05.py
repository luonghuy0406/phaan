import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1600, 1200
img = Image.new("RGB", (W, H), "#120e0a")
draw = ImageDraw.Draw(img)

# 1. Background: Dark antique pagoda bell tower interior (Gác chuông gỗ lim cổ)
# Ceiling and wooden rafters
for y in range(H):
    t = y / H
    r = int(24 * (1 - t) + 16 * t)
    g = int(18 * (1 - t) + 12 * t)
    b = int(14 * (1 - t) + 9 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Timber framework (Cột gỗ lim và xà ngang)
# Massive top beam
draw.rectangle([100, 80, W - 100, 200], fill="#3a2718", outline="#22160d", width=3)
# Left and right huge columns
draw.rectangle([120, 80, 260, H], fill="#302013", outline="#1c120a", width=3)
draw.rectangle([W - 260, 80, W - 120, H], fill="#302013", outline="#1c120a", width=3)

# Floor planks (sàn gỗ lim bóng)
floor_y = 860
for y in range(floor_y, H, 35):
    draw.line([(0, y), (W, y)], fill="#24180e", width=2)

# Wooden balustrade / window louvers in background
for x in range(300, W - 300, 45):
    draw.line([(x, 220), (x, 700)], fill="#2b1c11", width=8)

# 2. Golden sunlight beams slicing through timber slats from upper left
# We can draw translucent golden polygons
sunbeam_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(sunbeam_overlay)

beams = [
    ([(0, 150), (450, 0), (1100, H), (500, H)], (255, 230, 160, 35)),
    ([(100, 100), (600, 0), (1350, H), (800, H)], (255, 220, 140, 45)),
    ([(250, 50), (800, 0), (W, 900), (1100, H)], (255, 240, 180, 25))
]
for poly, color in beams:
    sdraw.polygon(poly, fill=color)

# 3. Giant Antique Bronze Bell (Đại Hồng Chung)
bell_cx, bell_cy = W // 2 + 60, 520
# Iron hanger hooks from ceiling beam
draw.line([(bell_cx - 40, 200), (bell_cx - 20, 300)], fill="#222426", width=12)
draw.line([(bell_cx + 40, 200), (bell_cx + 20, 300)], fill="#222426", width=12)

# Bell crown (quai chuông chạm hình Bồ Lao thời Lê)
draw.rectangle([bell_cx - 70, 300, bell_cx + 70, 350], fill="#32383c", outline="#1f2326", width=3)
# Bell Body: Curved bell silhouette
bell_top_w = 260
bell_bot_w = 480
bell_h = 420
y_top = 350
y_bot = y_top + bell_h

bell_poly = [
    (bell_cx - bell_top_w // 2, y_top),
    (bell_cx + bell_top_w // 2, y_top),
    (bell_cx + bell_top_w // 2 + 40, y_top + 160),
    (bell_cx + bell_bot_w // 2, y_bot),
    (bell_cx - bell_bot_w // 2, y_bot),
    (bell_cx - bell_top_w // 2 - 40, y_top + 160)
]
draw.polygon(bell_poly, fill="#2c3338", outline="#15191c", width=4)

# Bell ancient bronze details: relief bands and dragon cloud inscriptions
for dy in [y_top + 60, y_top + 120, y_top + 220, y_top + 320, y_bot - 30]:
    draw.line([(bell_cx - 200, dy), (bell_cx + 200, dy)], fill="#1f2427", width=5)
    draw.line([(bell_cx - 200, dy + 6), (bell_cx + 200, dy + 6)], fill="#3d464d", width=2)

# Antique greenish patina (rêu đồng cổ)
draw.ellipse([bell_cx - 80, y_top + 140, bell_cx + 40, y_top + 260], fill="#354845")
draw.ellipse([bell_cx + 30, y_top + 230, bell_cx + 140, y_top + 330], fill="#2d3d3a")

# 4. Wooden Mallet (Chày gỗ lim giộng chuông) & Green Nylon Cord
# The mallet hangs horizontally to the left of the bell
mal_y = y_top + 280
mal_x1 = 280
mal_x2 = bell_cx - bell_bot_w // 2 + 15
mallet_h = 48

# Hanging hemp rope from top beam
draw.line([(mal_x1 + 60, 200), (mal_x1 + 60, mal_y)], fill="#8a7356", width=6)
draw.line([(mal_x2 - 50, 200), (mal_x2 - 50, mal_y)], fill="#8a7356", width=6)

# Wooden Mallet body (cylindrical ironwood log)
draw.rounded_rectangle([mal_x1, mal_y, mal_x2, mal_y + mallet_h], radius=15, fill="#52321a", outline="#2b1a0e", width=3)
draw.ellipse([mal_x2 - 20, mal_y, mal_x2 + 10, mal_y + mallet_h], fill="#694021", outline="#2b1a0e", width=2)

# GREEN NYLON CORD tied tightly around mallet neck and going up towards roof
draw.line([(mal_x2 - 30, mal_y - 2), (mal_x2 - 30, mal_y + mallet_h + 2)], fill="#1fa348", width=6)
draw.line([(mal_x2 - 25, mal_y - 2), (mal_x2 - 25, mal_y + mallet_h + 2)], fill="#178037", width=4)
# Cord going up diagonally to trigger beam
draw.line([(mal_x2 - 28, mal_y), (mal_x2 - 80, 200)], fill="#22b851", width=5)

# 5. Puddle of Water on Floor directly below the bell rim
puddle_cx, puddle_cy = bell_cx - 30, 950
puddle_w, puddle_h = 280, 110

# Wet floor reflection
draw.ellipse([puddle_cx - puddle_w // 2, puddle_cy - puddle_h // 2,
              puddle_cx + puddle_w // 2, puddle_cy + puddle_h // 2], fill="#1c2830", outline="#3d5666", width=2)
# Concentric rippling rings from dripping water
for r in [20, 50, 90]:
    draw.ellipse([puddle_cx - r, puddle_cy - r // 2, puddle_cx + r, puddle_cy + r // 2], outline="#527085", width=1)

# Water drop falling in mid-air
draw.ellipse([puddle_cx - 4, 870, puddle_cx + 4, 882], fill="#8fc0e2")
draw.ellipse([puddle_cx - 3, 910, puddle_cx + 3, 920], fill="#8fc0e2")

# 6. Apply translucent sunbeams
img.paste(sunbeam_overlay, (0, 0), sunbeam_overlay)
draw = ImageDraw.Draw(img)

# 7. Dust Motes in Sunbeams
random.seed(101)
for _ in range(450):
    mx = random.randint(150, W - 200)
    my = random.randint(150, 900)
    mr = random.randint(1, 3)
    draw.circle((mx, my), mr, fill=(255, 245, 215, 180))

# 8. Forensic Evidence Labels & Case Overlays
font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)

# Top Bar
draw.rectangle([0, 0, W, 50], fill="#0a0c0e")
draw.text((40, 25), "CÔNG AN TỈNH HÀ TÂY - PHÒNG KỸ THUẬT HÌNH SỰ (PC21)", fill="#e1b12c", font=font_bold, anchor="lm")
draw.text((W - 40, 25), "HỒ SƠ HIỆN TRƯỜNG GÁC CHUÔNG - VỤ ÁN CHÙA CỔ SƠN (01/04/2004)", fill="#ffffff", font=font_small, anchor="rm")
draw.line([(0, 50), (W, 50)], fill="#e1b12c", width=2)

# Forensic Callout 1: Green Nylon Cord on Mallet
call_x1 = mal_x2 - 120
call_y1 = mal_y - 120
draw.line([(mal_x2 - 28, mal_y - 20), (call_x1, call_y1 + 40)], fill="#22b851", width=2)
draw.rectangle([call_x1 - 180, call_y1, call_x1 + 60, call_y1 + 50], fill="#0a1c12", outline="#22b851", width=2)
draw.text((call_x1 - 60, call_y1 + 16), "DÂY DÙ XANH LÁ CÂY BUỘC ĐẦU CHÀY", fill="#4cdb7b", font=font_bold, anchor="mm")
draw.text((call_x1 - 60, call_y1 + 34), "Nối lên đòn bẩy giật chốt tự động trên xà", fill="#b8e6c4", font=font_small, anchor="mm")

# Forensic Callout 2: Water Puddle under bell
call_x2 = puddle_cx + 180
call_y2 = puddle_cy - 40
draw.line([(puddle_cx + 60, puddle_cy), (call_x2, call_y2 + 20)], fill="#4ea8de", width=2)
draw.rectangle([call_x2, call_y2, call_x2 + 280, call_y2 + 65], fill="#0a1520", outline="#4ea8de", width=2)
draw.text((call_x2 + 140, call_y2 + 20), "VŨNG NƯỚC RỈ GIỌT TRÊN SÀN GỖ LIM", fill="#4ea8de", font=font_bold, anchor="mm")
draw.text((call_x2 + 140, call_y2 + 45), "Nước rò rỉ từ cơ cấu bập bênh nhỏ giọt hẹn giờ\ntạo tiếng chuông 11h45 khi hung thủ đã xuống núi", fill="#cfe8f7", font=font_small, anchor="mm")

# L-shaped Forensic Metric Scale beside puddle
sc_x, sc_y = puddle_cx - 190, puddle_cy - 20
draw.line([(sc_x, sc_y), (sc_x, sc_y + 80)], fill="#ffffff", width=4)
draw.line([(sc_x, sc_y + 80), (sc_x + 80, sc_y + 80)], fill="#ffffff", width=4)
for i in range(0, 81, 10):
    draw.line([(sc_x - 4, sc_y + i), (sc_x + 4, sc_y + i)], fill="#ffffff", width=2)
    draw.line([(sc_x + i, sc_y + 76), (sc_x + i, sc_y + 84)], fill="#ffffff", width=2)
draw.text((sc_x + 35, sc_y + 95), "10 cm", fill="#ffffff", font=font_small, anchor="mm")

# Save as WebP
out_path = "public/cases/hoi-chuong-chua-thay/images/d05-gac-chuong.webp"
img.save(out_path, "WEBP", quality=90)
print(f"Generated {out_path} successfully!")
