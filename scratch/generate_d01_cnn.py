import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1600, 1000
img = Image.new("RGB", (W, H), "#0b121e")
draw = ImageDraw.Draw(img)

# 1. Background: Winter twilight snowy landscape with Tudor mansion
# Gradient sky: dusky dark slate blue to cold winter navy
for y in range(500):
    t = y / 500
    r = int(15 * (1 - t) + 30 * t)
    g = int(22 * (1 - t) + 42 * t)
    b = int(40 * (1 - t) + 65 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Snow ground (lower half)
for y in range(480, 780):
    t = (y - 480) / 300
    # snowy blue-white
    r = int(185 + 20 * t)
    g = int(195 + 15 * t)
    b = int(215 + 15 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# 2. Draw Pine Trees with snow in background
def draw_pine(cx, cy, height, width):
    layers = 5
    for i in range(layers):
        ly = cy - height + int(i * (height / layers))
        lw = int(width * ((i + 1) / layers))
        # dark green needle branch
        draw.polygon([(cx, ly), (cx - lw // 2, ly + 40), (cx + lw // 2, ly + 40)], fill="#172e22")
        # snow cap on branch
        draw.polygon([(cx, ly), (cx - lw // 3, ly + 18), (cx + lw // 3, ly + 18)], fill="#e1ecf4")

draw_pine(120, 520, 240, 140)
draw_pine(220, 500, 200, 120)
draw_pine(1400, 520, 260, 150)
draw_pine(1500, 500, 210, 130)

# 3. Draw Tudor Mansion Architecture (Ramsey 15-room residence in Boulder)
# Main mansion body
mx, my = 360, 220
mw, mh = 880, 320

# Brick/stone walls
draw.rectangle([mx, my + 80, mx + mw, my + mh], fill="#42342c")

# Tudor gables & steep pitched roof covered in deep snow
gable1 = [(mx + 40, my + 80), (mx + 200, my - 60), (mx + 360, my + 80)]
gable2 = [(mx + 380, my + 80), (mx + 560, my - 100), (mx + 740, my + 80)]
gable3 = [(mx + 720, my + 80), (mx + 840, my - 20), (mx + 920, my + 80)]

for g in [gable1, gable2, gable3]:
    draw.polygon(g, fill="#2c221e")
    # thick snow layer on roof slopes
    p_left, p_top, p_right = g[0], g[1], g[2]
    draw.line([p_left, p_top], fill="#f0f5fa", width=14)
    draw.line([p_top, p_right], fill="#f0f5fa", width=14)

# Tudor dark timber beam patterns
for gx1, gx2 in [(mx + 60, mx + 340), (mx + 400, mx + 720)]:
    for x in range(gx1, gx2, 50):
        draw.line([(x, my + 80), (x, my + mh)], fill="#1f1612", width=4)
    draw.line([(gx1, my + 180), (gx2, my + 180)], fill="#1f1612", width=4)
    draw.line([(gx1, my + 260), (gx2, my + 260)], fill="#1f1612", width=4)

# Warm glowing interior windows (Christmas lighting)
windows = [
    (mx + 90, my + 100, 50, 60),
    (mx + 170, my + 100, 50, 60),
    (mx + 250, my + 100, 50, 60),
    (mx + 440, my + 100, 60, 70),
    (mx + 540, my + 100, 60, 70),
    (mx + 640, my + 100, 60, 70),
    # Ground floor windows
    (mx + 100, my + 200, 60, 80),
    (mx + 220, my + 200, 60, 80),
    (mx + 480, my + 200, 80, 90),
    (mx + 620, my + 200, 80, 90),
]

for wx, wy, ww, wh in windows:
    draw.rectangle([wx, wy, wx + ww, wy + wh], fill="#ffcf59")
    # mullions
    draw.line([(wx + ww // 2, wy), (wx + ww // 2, wy + wh)], fill="#2c221e", width=2)
    draw.line([(wx, wy + wh // 2), (wx + ww, wy + wh // 2)], fill="#2c221e", width=2)

# Ground snow drifts
draw.ellipse([mx - 60, my + mh - 20, mx + mw + 80, my + mh + 120], fill="#e2edf5")

# 4. Boulder Police Cruiser in snow driveway (Front left)
pc_x, pc_y = 260, 620
# Car body
draw.rectangle([pc_x, pc_y, pc_x + 220, pc_y + 60], fill="#f5f7fa")
draw.rectangle([pc_x + 40, pc_y - 35, pc_x + 180, pc_y], fill="#111c2e")
# Police stripe
draw.rectangle([pc_x, pc_y + 20, pc_x + 220, pc_y + 35], fill="#1c4482")
# Red/Blue flashers
draw.rectangle([pc_x + 90, pc_y - 45, pc_x + 115, pc_y - 35], fill="#ff2222")
draw.rectangle([pc_x + 125, pc_y - 45, pc_x + 150, pc_y - 35], fill="#2266ff")
# Wheels in snow
draw.circle((pc_x + 45, pc_y + 60), 22, fill="#1c222c")
draw.circle((pc_x + 175, pc_y + 60), 22, fill="#1c222c")

# Yellow Crime Scene Tape
draw.line([(100, 680), (W - 100, 710)], fill="#ffd700", width=8)

# 5. Falling Snow Effect
random.seed(42)
for _ in range(350):
    sx = random.randint(0, W)
    sy = random.randint(0, 760)
    sr = random.randint(1, 3)
    draw.circle((sx, sy), sr, fill="#ffffff")

# 6. CRT TV Broadcast Upper Bar & Lower Third Banner (1996 CNN Graphic)
font_cnn = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 36)
font_head = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
font_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)

# Top TV Banner
draw.rectangle([0, 0, W, 45], fill="#080e18")
draw.text((30, 22), "CNN LIVE / SPECIAL REPORT", fill="#ff2d2d", font=font_sub, anchor="lm")
draw.text((W - 30, 22), "BOULDER, COLORADO - DEC 26, 1996 [16:45 MST]", fill="#e1e8f0", font=font_sub, anchor="rm")
draw.line([(0, 45), (W, 45)], fill="#ff2d2d", width=2)

# Lower Third Graphic Box
lt_y = 750
draw.rectangle([0, lt_y, W, H], fill="#0a1322")
draw.line([(0, lt_y), (W, lt_y)], fill="#ff2222", width=4)

# CNN Red Logo Badge
draw.rectangle([40, lt_y + 20, 180, lt_y + 90], fill="#cc0000")
draw.text((110, lt_y + 55), "CNN", fill="#ffffff", font=font_cnn, anchor="mm")

# Headline Banner
draw.rectangle([200, lt_y + 20, W - 40, lt_y + 60], fill="#ffcc00")
draw.text((220, lt_y + 40), "BREAKING NEWS: 6-YEAR-OLD BEAUTY QUEEN FOUND DEAD IN BASEMENT", fill="#000000", font=font_head, anchor="lm")

# Subtext Box
draw.text((220, lt_y + 85), "RAMSEY MANSION INVESTIGATION - BOULDER POLICE DEPARTMENT EXAMINES SCENE", fill="#ffffff", font=font_sub)
draw.text((220, lt_y + 115), "DETECTIVES CONFIRM: DEEP SNOW SURROUNDING 15-ROOM MANSION HAS NO UNEXPLAINED FOOTPRINTS", fill="#99ccff", font=font_sub)
draw.text((220, lt_y + 145), "THREE-PAGE HANDWRITTEN RANSOM NOTE DEMANDING $118,000 FOUND ON REAR SPIRAL STAIRCASE", fill="#e1ecf5", font=font_sub)

# Bottom Ticker Bar
draw.rectangle([0, H - 45, W, H], fill="#050a12")
draw.text((40, H - 22), "LIVE FEED: BOULDER COUNTY SHERIFF & FBI FORENSIC UNITS ON SITE /// NO SIGNS OF FORCED ENTRY", fill="#ffd24d", font=font_sub, anchor="lm")

# CRT Scanlines effect overlay (horizontal faint lines)
for y in range(0, H, 4):
    draw.line([(0, y), (W, y)], fill=(0, 0, 0, 30), width=1)

# Save as WebP
out_path = "public/cases/buc-thu-dem-tuyet-trang/images/d01-bao-chi.webp"
img.save(out_path, "WEBP", quality=88)
print(f"Generated {out_path} successfully!")
