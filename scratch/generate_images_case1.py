import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageOps

def create_noise(w, h, opacity=0.08):
    noise = Image.new('L', (w, h))
    pixels = noise.load()
    for y in range(h):
        for x in range(w):
            pixels[x, y] = random.randint(0, 255)
    return noise

def apply_grain(base_img, strength=20):
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
    img = Image.new('RGB', (w, h), (18, 22, 28))
    draw = ImageDraw.Draw(img)

    # Dusk sky gradient (deep indigo to warm dusky amber)
    for y in range(int(h * 0.55)):
        t = y / (h * 0.55)
        r = int(18 + t * (90 - 18))
        g = int(22 + t * (48 - 22))
        b = int(35 + t * (40 - 35))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Water gradient (murky reddish alluvial silt river with reflections)
    water_y = int(h * 0.52)
    for y in range(water_y, h):
        t = (y - water_y) / (h - water_y)
        r = int(70 * (1 - t*0.5) + 35 * (t*0.5))
        g = int(38 * (1 - t*0.5) + 20 * (t*0.5))
        b = int(25 * (1 - t*0.5) + 18 * (t*0.5))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Riverbank silhouettes (coconut palms, nipa palms)
    # Left bank
    draw.polygon([(0, water_y - 20), (280, water_y + 40), (0, water_y + 120)], fill=(12, 14, 18))
    # Right bank
    draw.polygon([(w, water_y - 40), (w - 320, water_y + 20), (w, water_y + 160)], fill=(10, 12, 15))

    # Distant palm trees silhouettes
    def draw_palm(cx, cy, height):
        # trunk
        draw.line([(cx, cy), (cx - 15, cy - height)], fill=(12, 14, 16), width=5)
        # fronds
        top_x, top_y = cx - 15, cy - height
        for angle in range(-80, 90, 25):
            rad = math.radians(angle)
            fx = top_x + math.sin(rad) * 65
            fy = top_y - math.cos(rad) * 35 + 20
            draw.line([(top_x, top_y), (fx, fy)], fill=(15, 18, 20), width=3)

    draw_palm(120, water_y + 10, 130)
    draw_palm(80, water_y + 20, 100)
    draw_palm(180, water_y + 35, 90)
    draw_palm(w - 140, water_y + 10, 140)
    draw_palm(w - 80, water_y + 20, 110)

    # Boat hull (traditional Mekong Delta ghe chài)
    bx = int(w * 0.28)
    by = int(h * 0.62)
    bw = int(w * 0.52)
    bh = int(h * 0.16)

    # Boat hull polygon
    hull_pts = [
        (bx, by), # prow
        (bx + int(bw * 0.12), by + bh), # keel bottom front
        (bx + int(bw * 0.85), by + bh), # keel bottom back
        (bx + bw, by + int(bh * 0.3)), # stern top
        (bx + int(bw * 0.82), by - int(bh * 0.1)),
        (bx + int(bw * 0.25), by - int(bh * 0.05)),
    ]
    draw.polygon(hull_pts, fill=(28, 24, 20))
    draw.line(hull_pts + [hull_pts[0]], fill=(45, 38, 30), width=3)

    # Cabin roof (curved bamboo / timber hatch cover)
    cab_x1 = bx + int(bw * 0.22)
    cab_x2 = bx + int(bw * 0.72)
    cab_y = by - int(bh * 0.38)
    draw.chord([cab_x1, cab_y - 30, cab_x2, by + 10], 180, 360, fill=(38, 30, 22), outline=(55, 45, 32))

    # Mooring wooden post & rope
    post_x = bx - 40
    post_y = by + 30
    draw.rectangle([post_x, post_y - 120, post_x + 22, post_y + 80], fill=(22, 18, 14))
    # Rope
    draw.line([(post_x + 10, post_y - 40), (bx + 15, by + 15)], fill=(120, 100, 70), width=4)

    # Amber lantern glow at the prow
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    lamp_x, lamp_y = bx + 25, by - 35
    for r in range(160, 0, -8):
        alpha = int((1.0 - r / 160) * 110)
        gdraw.ellipse([lamp_x - r, lamp_y - r, lamp_x + r, lamp_y + r], fill=(255, 175, 50, alpha))
    # Water reflection
    for r in range(120, 0, -10):
        alpha = int((1.0 - r / 120) * 70)
        gdraw.ellipse([lamp_x - int(r*1.8), lamp_y + 80 - r//2, lamp_x + int(r*1.8), lamp_y + 80 + r//2], fill=(240, 150, 40, alpha))

    img = Image.alpha_composite(img.convert('RGBA'), glow).convert('RGB')
    draw = ImageDraw.Draw(img)
    # Lantern body
    draw.rectangle([lamp_x - 7, lamp_y - 12, lamp_x + 7, lamp_y + 12], fill=(255, 230, 150))
    draw.rectangle([lamp_x - 9, lamp_y - 16, lamp_x + 9, lamp_y - 12], fill=(40, 35, 30))
    draw.rectangle([lamp_x - 9, lamp_y + 12, lamp_x + 9, lamp_y + 16], fill=(40, 35, 30))
    draw.line([(lamp_x, lamp_y - 16), (bx + 15, by - 45)], fill=(80, 70, 60), width=2)

    # Water ripples
    for i in range(40):
        ry = random.randint(water_y + 30, h - 20)
        rx = random.randint(100, w - 100)
        rw = random.randint(40, 180)
        draw.line([(rx, ry), (rx + rw, ry)], fill=(90, 50, 32, 100), width=1)

    # Final film grain & vignette
    img = apply_grain(img, 18)
    img.save('cases/con-nuoc-ram-thang-gieng/images/cover.webp', 'WEBP', quality=85)
    print("cover.webp created successfully")

def make_d01():
    w, h = 960, 540 # 16:9
    img = Image.new('RGB', (w, h), (180, 185, 190))
    draw = ImageDraw.Draw(img)

    # Foggy river morning gradient
    for y in range(h):
        t = y / h
        r = int(140 + t * 40)
        g = int(145 + t * 35)
        b = int(150 + t * 30)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Muddy river water
    water_y = int(h * 0.45)
    for y in range(water_y, h):
        t = (y - water_y) / (h - water_y)
        val = int(120 - t * 30)
        draw.line([(0, y), (w, y)], fill=(val + 10, val + 5, val))

    # Rural timber boatyard workshop structure (stilts, rafters, tin roof)
    shed_x = int(w * 0.15)
    shed_w = int(w * 0.5)
    draw.rectangle([shed_x, water_y - 140, shed_x + shed_w, water_y - 100], fill=(70, 70, 75)) # roof
    for px in range(shed_x + 20, shed_x + shed_w, 70):
        draw.line([(px, water_y - 100), (px, water_y + 40)], fill=(50, 50, 55), width=6) # stilt pillars

    # Boat hull under repair inside shed
    draw.chord([shed_x + 40, water_y - 60, shed_x + shed_w - 40, water_y + 20], 0, 180, fill=(60, 55, 50))

    # Moored boat at riverside
    draw.polygon([(w * 0.6, water_y + 20), (w * 0.88, water_y + 25), (w * 0.82, water_y + 75), (w * 0.65, water_y + 70)], fill=(45, 42, 40))

    # Yellow/white police tape along the wooden fence
    draw.line([(w * 0.05, water_y - 20), (w * 0.45, water_y + 10)], fill=(220, 200, 50), width=4)
    draw.line([(w * 0.45, water_y + 10), (w * 0.75, water_y - 10)], fill=(220, 200, 50), width=4)

    # Distant trees
    for tx in [w*0.08, w*0.12, w*0.78, w*0.85, w*0.92]:
        draw.ellipse([tx - 40, water_y - 160, tx + 40, water_y - 30], fill=(80, 85, 80))

    # Newsprint grain / monochrome sepia tint
    img = ImageOps.grayscale(img).convert('RGB')
    # Warm newsprint tone
    sepia = Image.new('RGB', (w, h), (215, 205, 190))
    img = Image.blend(img, sepia, 0.25)
    img = apply_grain(img, 30)
    img.save('cases/con-nuoc-ram-thang-gieng/images/d01-newspaper.webp', 'WEBP', quality=85)
    print("d01-newspaper.webp created successfully")

def make_d04():
    w, h = 800, 600 # 4:3
    img = Image.new('RGB', (w, h), (40, 42, 45))
    draw = ImageDraw.Draw(img)

    # Muddy river water background
    for y in range(h):
        t = y / h
        r = int(90 - t * 30)
        g = int(65 - t * 25)
        b = int(45 - t * 20)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # Wooden boat deck & closed cabin hatch view
    # Boat side deck
    draw.polygon([(80, 80), (720, 70), (740, 520), (60, 530)], fill=(55, 45, 38), outline=(75, 62, 50), width=4)

    # Wood plank lines on deck
    for py in range(120, 500, 45):
        draw.line([(90, py), (710, py - 5)], fill=(40, 32, 28), width=3)

    # Closed central hatch (nắp khoang gỗ lim dày)
    hx1, hy1, hx2, hy2 = 220, 160, 580, 440
    draw.rectangle([hx1, hy1, hx2, hy2], fill=(35, 26, 20), outline=(85, 68, 52), width=6)
    # Hatch wooden planks
    for px in range(hx1 + 45, hx2, 45):
        draw.line([(px, hy1), (px, hy2)], fill=(25, 18, 14), width=3)

    # Lim wood locking crossbar (thanh then cài)
    draw.rectangle([hx1 + 30, hy1 + 120, hx2 - 30, hy1 + 155], fill=(28, 20, 15), outline=(60, 45, 35), width=3)
    # Heavy iron latch / bracket
    draw.rectangle([hx1 + 140, hy1 + 115, hx1 + 175, hy1 + 160], fill=(80, 82, 85))
    draw.rectangle([hx2 - 175, hy1 + 115, hx2 - 140, hy1 + 160], fill=(80, 82, 85))

    # Water flooded over lower deck edge
    draw.polygon([(60, 450), (740, 440), (760, 600), (40, 600)], fill=(75, 52, 36))
    # Water foam / ripples
    for i in range(15):
        wx = random.randint(100, 650)
        wy = random.randint(460, 560)
        draw.line([(wx, wy), (wx + random.randint(30, 90), wy)], fill=(120, 95, 70), width=2)

    # Coconut rope tied to mooring post
    draw.line([(80, 150), (30, 220)], fill=(110, 85, 55), width=8)
    draw.line([(700, 140), (760, 200)], fill=(110, 85, 55), width=8)

    img = apply_grain(img, 20)
    img.save('cases/con-nuoc-ram-thang-gieng/images/d04-boat.webp', 'WEBP', quality=85)
    print("d04-boat.webp created successfully")

def make_d10():
    w, h = 800, 600 # 4:3
    # Forensic lab slate-grey table
    img = Image.new('RGB', (w, h), (85, 88, 92))
    draw = ImageDraw.Draw(img)

    # Subtle lab table texture
    for y in range(h):
        t = y / h
        val = int(80 + (t - 0.5) * 15)
        draw.line([(0, y), (w, y)], fill=(val, val + 2, val + 4))

    # Shadow for brass valve plug
    vx, vy = 360, 300
    draw.ellipse([vx - 110, vy - 90, vx + 130, vy + 120], fill=(50, 52, 55))

    # Large octagonal brass valve plug (chốt van lù bằng đồng thau giác ốc số 24)
    # Outer circle / flange
    draw.ellipse([vx - 95, vy - 95, vx + 95, vy + 95], fill=(165, 128, 48), outline=(135, 100, 35), width=4)
    # Threads (ren xoắn)
    for r in range(85, 60, -6):
        draw.ellipse([vx - r, vy - r, vx + r, vy + r], outline=(145, 110, 40), width=3)

    # Octagonal nut head in center (giác ốc số 24)
    oct_pts = []
    nut_r = 55
    for a in range(0, 360, 45):
        rad = math.radians(a + 22.5)
        oct_pts.append((vx + math.cos(rad) * nut_r, vy + math.sin(rad) * nut_r))
    draw.polygon(oct_pts, fill=(185, 145, 60), outline=(120, 90, 30), width=3)
    # Inner indent
    draw.ellipse([vx - 20, vy - 20, vx + 20, vy + 20], fill=(140, 105, 40))

    # Visible fresh metallic scratch marks on octagonal edges (vết cọ xước kim loại từ kìm mỏ quạ)
    for sp in [(vx - 48, vy - 25), (vx - 45, vy + 22), (vx + 35, vy - 35), (vx + 42, vy + 20)]:
        sx, sy = sp
        draw.line([(sx, sy), (sx + random.randint(12, 22), sy + random.randint(-8, 8))], fill=(255, 235, 170), width=3)
        draw.line([(sx - 5, sy + 3), (sx + random.randint(10, 18), sy + random.randint(5, 12))], fill=(245, 220, 150), width=2)

    # Green nylon braided cord (mẩu sợi cước xanh lá mạ)
    cord_pts = [
        (560, 200), (590, 240), (620, 310), (580, 380), (630, 430), (660, 460)
    ]
    # Shadow for cord
    s_cord = [(x + 8, y + 8) for x, y in cord_pts]
    for i in range(len(s_cord) - 1):
        draw.line([s_cord[i], s_cord[i+1]], fill=(55, 58, 60), width=8)
    # Green cord
    for i in range(len(cord_pts) - 1):
        draw.line([cord_pts[i], cord_pts[i+1]], fill=(65, 165, 80), width=7)
        draw.line([cord_pts[i], cord_pts[i+1]], fill=(120, 215, 130), width=3)

    # Steel metric scale ruler at bottom
    rx1, ry1, rx2, ry2 = 120, 480, 680, 520
    draw.rectangle([rx1, ry1, rx2, ry2], fill=(175, 180, 185), outline=(130, 135, 140), width=2)
    # Ruler tick marks (no numbers to comply with NO TEXT rule)
    for x in range(rx1 + 20, rx2 - 10, 15):
        h_tick = 14 if (x - rx1 - 20) % 75 == 0 else 7
        draw.line([(x, ry1), (x, ry1 + h_tick)], fill=(50, 52, 55), width=2)

    img = apply_grain(img, 15)
    img.save('cases/con-nuoc-ram-thang-gieng/images/d10-valve.webp', 'WEBP', quality=85)
    print("d10-valve.webp created successfully")

def make_d16():
    w, h = 800, 600 # 4:3
    # Striped blue-orange woven tarpaulin background (bạt dứa)
    img = Image.new('RGB', (w, h), (45, 85, 125))
    draw = ImageDraw.Draw(img)

    # Tarpaulin woven weave pattern
    for y in range(0, h, 16):
        col = (205, 105, 45) if (y // 16) % 3 == 0 else (35, 75, 115)
        draw.rectangle([0, y, w, y + 14], fill=col)
    for x in range(0, w, 8):
        draw.line([(x, 0), (x, h)], fill=(20, 50, 80, 40), width=1)

    # Folded wet black diving suit in upper area
    suit_pts = [(100, 80), (380, 60), (410, 240), (120, 260)]
    draw.polygon(suit_pts, fill=(28, 28, 30), outline=(45, 45, 48), width=3)
    # Folds
    draw.line([(140, 120), (360, 100)], fill=(40, 40, 45), width=6)
    draw.line([(130, 180), (370, 160)], fill=(40, 40, 45), width=5)
    # Dried river mud stains on wetsuit
    for mp in [(180, 130), (280, 110), (220, 200), (320, 180)]:
        draw.ellipse([mp[0] - 25, mp[1] - 15, mp[0] + 25, mp[1] + 15], fill=(75, 60, 45))

    # Pipe wrench / water pump pliers (kìm mỏ quạ số 24)
    # Shadow
    draw.line([(240, 370), (580, 440)], fill=(25, 45, 65), width=26)
    draw.line([(240, 390), (550, 480)], fill=(25, 45, 65), width=22)

    # Steel jaws (mỏ kìm thép tôi)
    draw.polygon([(180, 330), (260, 310), (280, 360), (220, 390)], fill=(120, 125, 130), outline=(80, 82, 85), width=3)
    draw.polygon([(170, 360), (240, 340), (250, 380), (190, 410)], fill=(110, 115, 120), outline=(70, 72, 75), width=3)
    # Teeth on jaws
    for i in range(5):
        draw.line([(190 + i*10, 345 + i*2), (195 + i*10, 355 + i*2)], fill=(50, 50, 55), width=3)

    # Metallic brass specks on jaw teeth
    for i in range(4):
        draw.point((192 + i*11, 348 + i*2), fill=(240, 205, 80))
        draw.point((193 + i*11, 349 + i*2), fill=(255, 225, 110))

    # Handles with worn black rubber sleeve
    draw.line([(260, 360), (560, 420)], fill=(25, 26, 28), width=20)
    draw.line([(240, 380), (540, 470)], fill=(25, 26, 28), width=18)
    # Rubber sleeve texture
    draw.line([(320, 372), (550, 418)], fill=(38, 40, 42), width=14)
    draw.line([(300, 395), (530, 466)], fill=(38, 40, 42), width=12)

    # Spool of bright green nylon cord (cuộn cước xanh)
    cx, cy = 600, 260
    draw.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(25, 45, 65)) # shadow
    draw.ellipse([cx - 65, cy - 65, cx + 65, cy + 65], fill=(50, 145, 65), outline=(30, 95, 40), width=4)
    for r in range(55, 25, -6):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(95, 195, 110), width=3)
    # Core hole
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(220, 220, 220), outline=(160, 160, 160), width=3)
    # Loose green string trailing off
    draw.line([(cx + 45, cy + 45), (cx + 100, cy + 90), (cx + 130, cy + 160)], fill=(85, 185, 100), width=4)

    img = apply_grain(img, 18)
    img.save('cases/con-nuoc-ram-thang-gieng/images/d16-tools.webp', 'WEBP', quality=85)
    print("d16-tools.webp created successfully")

make_cover()
make_d01()
make_d04()
make_d10()
make_d16()
