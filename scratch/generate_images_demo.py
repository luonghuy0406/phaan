import math
import random
from PIL import Image, ImageDraw, ImageOps

def apply_grain(base_img, strength=15):
    w, h = base_img.size
    grain = Image.new('RGB', (w, h))
    g_pix = grain.load()
    for y in range(h):
        for x in range(w):
            val = random.randint(128 - strength, 128 + strength)
            g_pix[x, y] = (val, val, val)
    return Image.blend(base_img, grain, 0.15)

def make_demo_cover():
    w, h = 960, 1200 # 4:5
    img = Image.new('RGB', (w, h), (25, 22, 20))
    draw = ImageDraw.Draw(img)

    # Dark atmospheric study room desk
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(45 - t*20), int(38 - t*16), int(30 - t*12)))

    # Window in background with night Hanoi alley
    wx1, wy1, wx2, wy2 = 200, 100, 760, 600
    draw.rectangle([wx1, wy1, wx2, wy2], fill=(20, 25, 35), outline=(60, 50, 40), width=6)
    # Broken pane of glass
    draw.polygon([(400, wy1), (580, wy1), (530, 350), (380, 320)], fill=(35, 45, 60))
    draw.line([(380, 320), (530, 350)], fill=(180, 200, 220), width=3)
    draw.line([(450, wy1), (430, 280)], fill=(180, 200, 220), width=2)

    # Desk surface
    desk_y = 650
    draw.rectangle([0, desk_y, w, h], fill=(65, 45, 30))

    # Vintage gold pocket watch on desk (Chiếc đồng hồ bỏ túi vỏ vàng)
    cx, cy = 480, 850
    # Shadow
    draw.ellipse([cx - 160, cy - 80, cx + 180, cy + 180], fill=(25, 18, 12))
    # Watch body
    draw.ellipse([cx - 140, cy - 140, cx + 140, cy + 140], fill=(225, 180, 50), outline=(170, 130, 30), width=8)
    # Dial face
    draw.ellipse([cx - 105, cy - 105, cx + 105, cy + 105], fill=(245, 240, 225), outline=(180, 150, 60), width=4)
    # Hour ticks
    for a in range(0, 360, 30):
        rad = math.radians(a)
        draw.line([(cx + math.sin(rad)*85, cy - math.cos(rad)*85), (cx + math.sin(rad)*98, cy - math.cos(rad)*98)], fill=(60, 50, 40), width=3)
    # Watch hands
    draw.line([(cx, cy), (cx + 45, cy - 35)], fill=(40, 35, 30), width=4) # hour
    draw.line([(cx, cy), (cx - 20, cy - 70)], fill=(40, 35, 30), width=3) # min
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(40, 35, 30))
    # Top winding crown & ring
    draw.rectangle([cx - 18, cy - 175, cx + 18, cy - 140], fill=(210, 165, 40), outline=(150, 110, 25), width=3)
    draw.arc([cx - 30, cy - 220, cx + 30, cy - 160], 0, 360, fill=(210, 165, 40), width=6)

    img = apply_grain(img, 18)
    img.save('cases/demo-01/images/cover.webp', 'WEBP', quality=85)
    print("demo-01 cover.webp created")

def make_demo_d01():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (60, 62, 65))
    draw = ImageDraw.Draw(img)

    # Courtyard brick floor outside window
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(110 - t*30), int(75 - t*20), int(60 - t*18)))

    # Window frame on right/top wall
    draw.rectangle([100, 40, 700, 320], fill=(45, 35, 28), outline=(75, 60, 45), width=6)
    # Broken glass pane in center
    draw.polygon([(250, 80), (550, 80), (520, 280), (280, 280)], fill=(30, 35, 45))
    # Jagged remaining glass edges
    draw.polygon([(250, 80), (310, 80), (280, 140)], fill=(160, 180, 200))
    draw.polygon([(500, 80), (550, 80), (530, 150)], fill=(160, 180, 200))

    # Glass shards scattered outside on courtyard brick
    for _ in range(40):
        sx = random.randint(180, 620)
        sy = random.randint(340, 540)
        sw = random.randint(10, 28)
        sh = random.randint(8, 22)
        draw.polygon([(sx, sy), (sx + sw, sy + sh//2), (sx + sw//2, sy + sh)], fill=(190, 210, 230), outline=(140, 160, 180))

    img = apply_grain(img, 20)
    img.save('cases/demo-01/images/d01-window.webp', 'WEBP', quality=85)
    print("demo-01 d01-window.webp created")

def make_demo_d07():
    w, h = 800, 600
    # CCTV high-angle view of alley at night
    img = Image.new('RGB', (w, h), (40, 45, 48))
    draw = ImageDraw.Draw(img)

    # Concrete walls of alley
    draw.polygon([(0, 0), (260, 0), (200, h), (0, h)], fill=(32, 35, 38))
    draw.polygon([(540, 0), (w, 0), (w, h), (600, h)], fill=(28, 30, 34))
    # Alley pavement
    draw.polygon([(260, 0), (540, 0), (600, h), (200, h)], fill=(48, 52, 55))

    # Person in grey hoodie walking into alley (silhouette from high angle)
    px, py = 400, 380
    # Shadow
    draw.ellipse([px - 40, py + 40, px + 50, py + 70], fill=(22, 24, 26))
    # Grey hoodie figure
    draw.ellipse([px - 22, py - 60, px + 22, py - 20], fill=(120, 125, 130)) # hood
    draw.polygon([(px - 32, py - 20), (px + 32, py - 20), (px + 36, py + 40), (px - 36, py + 40)], fill=(105, 110, 115)) # body
    # Dark trousers
    draw.line([(px - 16, py + 40), (px - 14, py + 85)], fill=(45, 48, 50), width=10)
    draw.line([(px + 16, py + 40), (px + 18, py + 85)], fill=(45, 48, 50), width=10)

    # CCTV scanlines and noise
    for y in range(0, h, 4):
        draw.line([(0, y), (w, y)], fill=(25, 28, 30), width=1)

    img = apply_grain(img, 35)
    img.save('cases/demo-01/images/d07-camera.webp', 'WEBP', quality=85)
    print("demo-01 d07-camera.webp created")

def make_demo_d08():
    w, h = 800, 600
    # Dark green pawn shop velvet felt
    img = Image.new('RGB', (w, h), (25, 48, 32))
    draw = ImageDraw.Draw(img)

    # Gold pocket watch close-up
    cx, cy = 400, 300
    # Shadow
    draw.ellipse([cx - 150, cy - 80, cx + 170, cy + 170], fill=(15, 28, 20))
    # Body
    draw.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=(225, 180, 45), outline=(175, 135, 25), width=8)
    # Dial
    draw.ellipse([cx - 95, cy - 95, cx + 95, cy + 95], fill=(245, 242, 230), outline=(180, 150, 50), width=3)
    # Ticks
    for a in range(0, 360, 30):
        rad = math.radians(a)
        draw.line([(cx + math.sin(rad)*75, cy - math.cos(rad)*75), (cx + math.sin(rad)*88, cy - math.cos(rad)*88)], fill=(50, 45, 35), width=3)
    # Hands
    draw.line([(cx, cy), (cx + 40, cy - 25)], fill=(35, 30, 25), width=4)
    draw.line([(cx, cy), (cx - 15, cy - 60)], fill=(35, 30, 25), width=3)
    # Engraved T.Đ.H initials monogram in elegant lines
    draw.line([(cx - 25, cy + 35), (cx - 15, cy + 35)], fill=(120, 100, 40), width=2)
    draw.line([(cx - 20, cy + 35), (cx - 20, cy + 55)], fill=(120, 100, 40), width=2)
    draw.arc([cx - 8, cy + 35, cx + 8, cy + 55], 270, 90, fill=(120, 100, 40), width=2)
    draw.line([(cx + 12, cy + 35), (cx + 12, cy + 55)], fill=(120, 100, 40), width=2)
    draw.line([(cx + 24, cy + 35), (cx + 24, cy + 55)], fill=(120, 100, 40), width=2)
    draw.line([(cx + 12, cy + 45), (cx + 24, cy + 45)], fill=(120, 100, 40), width=2)

    img = apply_grain(img, 15)
    img.save('cases/demo-01/images/d08-watch.webp', 'WEBP', quality=85)
    print("demo-01 d08-watch.webp created")

make_demo_cover()
make_demo_d01()
make_demo_d07()
make_demo_d08()
