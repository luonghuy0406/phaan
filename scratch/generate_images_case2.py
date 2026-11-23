import math
import random
from PIL import Image, ImageDraw, ImageOps

def apply_grain(base_img, strength=18):
    w, h = base_img.size
    grain = Image.new('RGB', (w, h))
    g_pix = grain.load()
    for y in range(h):
        for x in range(w):
            val = random.randint(128 - strength, 128 + strength)
            g_pix[x, y] = (val, val, val)
    return Image.blend(base_img, grain, 0.15)

def make_cover():
    w, h = 960, 1200 # 4:5 ratio
    img = Image.new('RGB', (w, h), (20, 24, 30))
    draw = ImageDraw.Draw(img)

    # Cold winter night sky gradient (dark greyish blue)
    for y in range(int(h * 0.45)):
        t = y / (h * 0.45)
        r = int(15 + t * 25)
        g = int(20 + t * 25)
        b = int(32 + t * 25)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Ground / courtyard in rain
    ground_y = int(h * 0.78)
    for y in range(ground_y, h):
        t = (y - ground_y) / (h - ground_y)
        draw.line([(0, y), (w, y)], fill=(25 + int(t*15), 26 + int(t*12), 28 + int(t*10)))

    # 4-story Soviet-style residential block building facade (Khu tập thể Dệt)
    bx1, by1, bx2, by2 = int(w * 0.08), int(h * 0.14), int(w * 0.92), ground_y
    draw.rectangle([bx1, by1, bx2, by2], fill=(42, 45, 48), outline=(30, 32, 35), width=4)

    # Concrete balconies and "chuồng cọp" (cage ironwork)
    floor_h = (by2 - by1) // 4
    for f in range(4):
        fy = by1 + f * floor_h
        # Floor line / concrete ledge
        draw.line([(bx1, fy), (bx2, fy)], fill=(65, 68, 70), width=6)

        # Windows and balconies for each floor
        for win_idx in range(4):
            wx1 = bx1 + 35 + win_idx * 200
            wx2 = wx1 + 140
            wy1 = fy + 20
            wy2 = fy + floor_h - 20

            # Lit window or dark window
            is_lit = (f == 1 and win_idx == 1) or (f == 2 and win_idx == 2) or (f == 0 and win_idx == 0)
            if is_lit:
                draw.rectangle([wx1, wy1, wx2, wy2], fill=(195, 145, 55)) # warm incandescent glow
                # Window frame cross
                draw.line([(wx1, (wy1+wy2)//2), (wx2, (wy1+wy2)//2)], fill=(40, 35, 25), width=3)
                draw.line([((wx1+wx2)//2, wy1), ((wx1+wx2)//2, wy2)], fill=(40, 35, 25), width=3)
            else:
                draw.rectangle([wx1, wy1, wx2, wy2], fill=(22, 24, 26))

            # Iron cage frame (chuồng cọp)
            draw.rectangle([wx1 - 8, wy1 - 5, wx2 + 8, wy2 + 10], outline=(75, 78, 80), width=2)
            for lx in range(wx1, wx2, 25):
                draw.line([(lx, wy1 - 5), (lx, wy2 + 10)], fill=(60, 62, 65), width=1)

    # Highlight apartment 204 (floor 1 in 0-indexed, win 1)
    p204_x1 = bx1 + 35 + 1 * 200
    p204_y1 = by1 + 1 * floor_h + 20

    # Fire / hearth in courtyard (luộc bánh chưng đêm 29 Tết)
    fire_x, fire_y = int(w * 0.4), ground_y + 45
    # Warm fire glow
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for r in range(180, 0, -8):
        alpha = int((1.0 - r / 180) * 120)
        gdraw.ellipse([fire_x - r, fire_y - r//2, fire_x + r, fire_y + r//2], fill=(255, 120, 25, alpha))
    img = Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Large aluminium pot (nồi luộc bánh chưng)
    draw.rectangle([fire_x - 30, fire_y - 65, fire_x + 30, fire_y - 10], fill=(110, 115, 120), outline=(75, 78, 80), width=3)
    draw.arc([fire_x - 30, fire_y - 75, fire_x + 30, fire_y - 55], 180, 360, fill=(130, 135, 140), width=4)
    # Fire flames
    draw.polygon([(fire_x - 35, fire_y), (fire_x - 10, fire_y - 30), (fire_x + 5, fire_y - 5), (fire_x + 35, fire_y)], fill=(245, 90, 20))
    draw.polygon([(fire_x - 15, fire_y), (fire_x, fire_y - 25), (fire_x + 15, fire_y)], fill=(255, 210, 60))

    # Smoke rising into winter drizzle
    for i in range(25):
        sy = fire_y - 80 - i * 15
        sx = fire_x + int(math.sin(i * 0.4) * 35) + random.randint(-15, 15)
        sr = 25 + i * 4
        # subtle grey puff
        puff = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        pdraw = ImageDraw.Draw(puff)
        pdraw.ellipse([sx - sr, sy - sr//2, sx + sr, sy + sr//2], fill=(160, 165, 170, max(5, 35 - i)))
        img = Image.alpha_composite(img.convert('RGBA'), puff).convert('RGB')
        draw = ImageDraw.Draw(img)

    # Fine Hanoi winter drizzle (mưa phùn)
    for _ in range(300):
        dx = random.randint(0, w)
        dy = random.randint(0, h)
        draw.line([(dx, dy), (dx + 2, dy + 8)], fill=(130, 140, 150), width=1)

    img = apply_grain(img, 20)
    img.save('cases/mua-dong-binh-ty/images/cover.webp', 'WEBP', quality=85)
    print("cover.webp created")

def make_d01():
    w, h = 960, 540 # 16:9
    img = Image.new('RGB', (w, h), (160, 165, 168))
    draw = ImageDraw.Draw(img)

    # Concrete courtyard and facade in gloomy morning
    draw.rectangle([0, 0, w, int(h * 0.7)], fill=(120, 125, 128))
    draw.rectangle([0, int(h * 0.7), w, h], fill=(85, 88, 90))

    # Staircase tower of block A6
    stair_x1, stair_x2 = int(w * 0.35), int(w * 0.65)
    draw.rectangle([stair_x1, 30, stair_x2, int(h * 0.7)], fill=(95, 100, 102), outline=(65, 68, 70), width=3)
    # Concrete window slats on staircase
    for sy in range(70, int(h * 0.65), 55):
        draw.rectangle([stair_x1 + 30, sy, stair_x2 - 30, sy + 30], fill=(45, 48, 50))

    # Yellow police line tape across building entrance
    draw.line([(stair_x1 - 80, int(h * 0.65)), (stair_x2 + 80, int(h * 0.68))], fill=(215, 195, 40), width=5)

    # Distant group of onlookers (silhouettes)
    for px in [120, 160, 200, 750, 790, 830]:
        draw.ellipse([px - 12, int(h * 0.68) - 45, px + 12, int(h * 0.68) - 20], fill=(40, 42, 45))
        draw.rectangle([px - 18, int(h * 0.68) - 20, px + 18, int(h * 0.78)], fill=(35, 38, 40))

    # 1990s newspaper print halftone / sepia
    img = ImageOps.grayscale(img).convert('RGB')
    sepia = Image.new('RGB', (w, h), (210, 202, 190))
    img = Image.blend(img, sepia, 0.25)
    img = apply_grain(img, 28)
    img.save('cases/mua-dong-binh-ty/images/d01-newspaper.webp', 'WEBP', quality=85)
    print("d01-newspaper.webp created")

def make_d04():
    w, h = 800, 600 # 4:3
    # Living room under warm incandescent bulb
    img = Image.new('RGB', (w, h), (45, 38, 30))
    draw = ImageDraw.Draw(img)

    # Wall with faded floral 1990s wallpaper texture
    for y in range(int(h * 0.65)):
        t = y / (h * 0.65)
        draw.line([(0, y), (w, y)], fill=(int(115 - t*30), int(95 - t*25), int(68 - t*20)))

    # Floor with patterned decorative floor tiles (gạch hoa cũ)
    tile_y = int(h * 0.65)
    draw.rectangle([0, tile_y, w, h], fill=(75, 62, 50))
    for tx in range(0, w, 60):
        draw.line([(tx, tile_y), (tx, h)], fill=(55, 45, 35), width=2)
    for ty in range(tile_y, h, 40):
        draw.line([(0, ty), (w, ty)], fill=(55, 45, 35), width=2)

    # Wooden armchair (ghế bành gỗ lim cũ)
    ax, ay = 120, 220
    draw.rectangle([ax, ay, ax + 180, ay + 260], fill=(58, 38, 22), outline=(35, 22, 12), width=4)
    draw.rectangle([ax + 20, ay + 40, ax + 160, ay + 180], fill=(85, 52, 30)) # backrest

    # Low wooden tea table (bàn trà gỗ)
    bx, by, bw, bh = 340, 320, 380, 200
    draw.polygon([(bx, by + 40), (bx + 80, by), (bx + bw, by), (bx + bw - 80, by + 40)], fill=(75, 52, 32), outline=(45, 30, 18), width=3)
    # Table legs
    draw.rectangle([bx + 10, by + 40, bx + 28, by + bh], fill=(45, 30, 18))
    draw.rectangle([bx + bw - 90, by + 40, bx + bw - 72, by + bh], fill=(45, 30, 18))

    # Traditional straw-padded tea cozy basket (ấm tích ủ giỏ rơm)
    draw.chord([bx + 40, by - 40, bx + 140, by + 35], 0, 180, fill=(145, 115, 65), outline=(100, 75, 40), width=3)

    # Small porcelain teacup with white powder residue (chén trà cặn bột trắng)
    cx, cy = bx + 190, by + 15
    draw.ellipse([cx - 18, cy - 10, cx + 18, cy + 10], fill=(235, 230, 220), outline=(180, 175, 165), width=2)
    draw.ellipse([cx - 12, cy - 6, cx + 12, cy + 6], fill=(130, 100, 45)) # tea liquid
    draw.ellipse([cx - 8, cy - 3, cx + 8, cy + 3], fill=(240, 240, 235)) # white powder sediment

    # Small dish with ginger candy (đĩa mứt gừng)
    dx, dy = bx + 260, by + 12
    draw.ellipse([dx - 28, dy - 14, dx + 28, dy + 14], fill=(225, 220, 210), outline=(160, 155, 145), width=2)
    # Pieces of sugar-coated ginger
    for off in [(-12, -2), (2, -4), (10, 1)]:
        draw.ellipse([dx + off[0] - 6, dy + off[1] - 4, dx + off[0] + 6, dy + off[1] + 4], fill=(185, 140, 70), outline=(235, 230, 210))

    # Pried open Danisa butter cookie tin under bed edge (hộp bánh quy sắt bị cạy nắp)
    box_x, box_y = 520, 490
    draw.ellipse([box_x - 55, box_y - 25, box_x + 55, box_y + 25], fill=(30, 50, 95), outline=(180, 140, 50), width=3)
    # Displaced tin lid beside it
    draw.ellipse([box_x + 60, box_y - 15, box_x + 140, box_y + 25], fill=(25, 45, 85), outline=(180, 140, 50), width=2)

    img = apply_grain(img, 18)
    img.save('cases/mua-dong-binh-ty/images/d04-room.webp', 'WEBP', quality=85)
    print("d04-room.webp created")

def make_d12():
    w, h = 800, 600 # 4:3
    # Black velvet laboratory examination surface
    img = Image.new('RGB', (w, h), (22, 24, 28))
    draw = ImageDraw.Draw(img)

    # Overhead neutral lab spotlight
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    for r in range(260, 0, -10):
        alpha = int((1.0 - r / 260) * 60)
        gdraw.ellipse([400 - r, 300 - r, 400 + r, 300 + r], fill=(220, 230, 245, alpha))
    img = Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')
    draw = ImageDraw.Draw(img)

    # Metal inhaler canister (ống xịt kim loại hình trụ)
    ix, iy = 320, 280
    # Shadow
    draw.polygon([(ix - 45, iy + 60), (ix + 160, iy + 60), (ix + 140, iy + 85), (ix - 65, iy + 85)], fill=(12, 14, 16))
    # Canister cylinder (aluminum body)
    draw.rectangle([ix, iy - 45, ix + 140, iy + 45], fill=(175, 180, 185), outline=(135, 140, 145), width=3)
    draw.ellipse([ix - 15, iy - 45, ix + 15, iy + 45], fill=(160, 165, 170), outline=(135, 140, 145), width=3)
    draw.ellipse([ix + 125, iy - 45, ix + 155, iy + 45], fill=(195, 200, 205), outline=(135, 140, 145), width=3)
    # Valve stem nozzle on front
    draw.rectangle([ix - 35, iy - 12, ix - 15, iy + 12], fill=(225, 225, 230), outline=(160, 160, 165), width=2)

    # Blue plastic mouthpiece casing (vỏ nhựa màu xanh dương đã tháo rời)
    mx, my = 540, 300
    # L-shaped plastic inhaler mouthpiece
    draw.polygon([(mx, my - 60), (mx + 60, my - 60), (mx + 60, my + 10), (mx + 110, my + 10), (mx + 110, my + 60), (mx, my + 60)], fill=(30, 95, 180), outline=(20, 65, 130), width=3)
    draw.ellipse([mx + 100, my + 15, mx + 115, my + 55], fill=(20, 65, 130)) # oral opening

    # Glass petri dish with clear liquid droplets (khay đựng giọt nước cất)
    px, py = 200, 380
    draw.ellipse([px - 60, py - 30, px + 60, py + 30], fill=(45, 52, 60), outline=(140, 155, 170), width=2)
    # Clear droplet
    draw.ellipse([px - 15, py - 10, px + 15, py + 10], fill=(190, 215, 235), outline=(160, 190, 215), width=1)
    draw.ellipse([px - 6, py - 6, px + 2, py - 2], fill=(255, 255, 255)) # highlight

    img = apply_grain(img, 15)
    img.save('cases/mua-dong-binh-ty/images/d12-inhaler.webp', 'WEBP', quality=85)
    print("d12-inhaler.webp created")

def make_d16():
    w, h = 800, 600 # 4:3
    # Neutral wooden surface
    img = Image.new('RGB', (w, h), (145, 125, 105))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(145 - t*20), int(125 - t*18), int(105 - t*15)))

    # Pair of Tiền Phong army plastic sandals (dép rọ bộ đội nhựa Tiền Phong)
    # Left sandal
    lx, ly = 240, 280
    # Shadow
    draw.ellipse([lx - 55, ly - 105, lx + 65, ly + 145], fill=(70, 58, 48))
    # Brown plastic sole
    draw.ellipse([lx - 45, ly - 95, lx + 45, ly + 125], fill=(95, 62, 38), outline=(65, 40, 22), width=4)
    # Straps (dây rọ đan chéo)
    for sy in range(ly - 60, ly + 60, 26):
        draw.line([(lx - 40, sy), (lx + 40, sy)], fill=(125, 82, 48), width=8)
    draw.line([(lx, ly - 80), (lx, ly + 80)], fill=(125, 82, 48), width=10)

    # Right sandal
    rx, ry = 380, 280
    draw.ellipse([rx - 55, ry - 105, rx + 65, ry + 145], fill=(70, 58, 48))
    draw.ellipse([rx - 45, ry - 95, rx + 45, ry + 125], fill=(95, 62, 38), outline=(65, 40, 22), width=4)
    for sy in range(ry - 60, ry + 60, 26):
        draw.line([(rx - 40, sy), (rx + 40, sy)], fill=(125, 82, 48), width=8)
    draw.line([(rx, ry - 80), (rx, ry + 80)], fill=(125, 82, 48), width=10)

    # White plaster dust on right heel edge (bụi vôi trắng ở gót dép)
    draw.arc([rx - 35, ry + 70, rx + 35, ry + 120], 30, 150, fill=(245, 245, 240), width=7)

    # Classic Vietnamese Thiên Long ballpoint pen with purple cap (bút bi Thiên Long nắp tím)
    pen_x1, pen_y1 = 540, 160
    pen_x2, pen_y2 = 640, 420
    # Pen shadow
    draw.line([(pen_x1 + 8, pen_y1 + 8), (pen_x2 + 8, pen_y2 + 8)], fill=(75, 62, 52), width=12)
    # White hexagonal plastic barrel
    draw.line([(pen_x1, pen_y1), (pen_x2, pen_y2)], fill=(245, 245, 248), width=10)
    # Purple cap on top
    cap_len = 0.35
    cx1 = int(pen_x1 + (pen_x2 - pen_x1) * (1 - cap_len))
    cy1 = int(pen_y1 + (pen_y2 - pen_y1) * (1 - cap_len))
    draw.line([(cx1, cy1), (pen_x2, pen_y2)], fill=(120, 45, 145), width=12)
    # Cap clip
    draw.line([(cx1 + 8, cy1 + 8), (pen_x2 - 15, pen_y2 - 15)], fill=(145, 65, 175), width=4)

    img = apply_grain(img, 16)
    img.save('cases/mua-dong-binh-ty/images/d16-shoes.webp', 'WEBP', quality=85)
    print("d16-shoes.webp created")

def make_d17():
    w, h = 800, 600 # 4:3
    # Office desk paper sheet background
    img = Image.new('RGB', (w, h), (210, 205, 195))
    draw = ImageDraw.Draw(img)

    # Blue plastic bag from vent (túi bọc nilon xanh bám bụi)
    draw.polygon([(80, 80), (280, 60), (310, 240), (100, 260)], fill=(30, 65, 110), outline=(20, 45, 80), width=3)
    # Dust on bag
    for dp in [(150, 120), (220, 160), (180, 200)]:
        draw.ellipse([dp[0] - 30, dp[1] - 15, dp[0] + 30, dp[1] + 15], fill=(95, 88, 80))

    # 12 SJC gold bars arranged in 3x4 grid on white paper (12 cây vàng lá SJC)
    grid_x, grid_y = 350, 100
    for row in range(3):
        for col in range(4):
            gx = grid_x + col * 95
            gy = grid_y + row * 140

            # Shadow
            draw.rectangle([gx + 5, gy + 5, gx + 75, gy + 115], fill=(155, 150, 140))
            # Transparent blister pack border
            draw.rectangle([gx - 6, gy - 6, gx + 76, gy + 116], fill=(240, 242, 245), outline=(190, 195, 200), width=2)
            # Shiny gold bar
            draw.rectangle([gx, gy, gx + 70, gy + 110], fill=(225, 175, 45), outline=(180, 135, 25), width=2)
            # Inner stamped gold frame (no readable text)
            draw.rectangle([gx + 8, gy + 10, gx + 62, gy + 100], outline=(245, 205, 75), width=2)
            draw.ellipse([gx + 22, gy + 25, gx + 48, gy + 51], fill=(245, 195, 60), outline=(200, 155, 35))
            draw.rectangle([gx + 20, gy + 65, gx + 50, gy + 85], fill=(240, 190, 55))

    img = apply_grain(img, 15)
    img.save('cases/mua-dong-binh-ty/images/d17-gold.webp', 'WEBP', quality=85)
    print("d17-gold.webp created")

make_cover()
make_d01()
make_d04()
make_d12()
make_d16()
make_d17()
