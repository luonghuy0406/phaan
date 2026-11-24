"""Vẽ minh hoạ ảnh tư liệu cho hồ sơ 12 (Vết mực làng Đông Hồ) bằng Pillow, không cần mô hình tạo ảnh.

Chạy: python3 authoring/vet-muc-lang-dong-ho/draw_images.py [d01|d03|d04|d07|d10 ...]
Dùng chung bộ hàm vẽ của authoring/lua-than-tay-nguyen/draw_photos.py.
"""
import importlib.util
import math
import random
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

_spec = importlib.util.spec_from_file_location('lib', Path(__file__).resolve().parents[1] / 'lua-than-tay-nguyen' / 'draw_photos.py')
lib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lib)
noise, tint, vignette, light_spot, soft_shadow, paste_shadow, bezier, grain = (
    lib.noise, lib.tint, lib.vignette, lib.light_spot, lib.soft_shadow, lib.paste_shadow, lib.bezier, lib.grain)

OUT = 'public/cases/vet-muc-lang-dong-ho/images/'
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(name if name.startswith('/') else F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
VERMILION, BLACK_INK = (196, 44, 30), (28, 24, 22)


def save(im, name, q=86):
    im.save(OUT + name + '.webp', 'WEBP', quality=q, method=6)
    print('ok', name, im.size)


def tag(d, x, y, no):
    d.rectangle([x, y, x + 190, y + 90], fill=(248, 244, 232), outline=(40, 40, 40), width=2)
    d.text((x + 20, y + 28), 'TANG VẬT', font=font(BOLD, 22), fill=(40, 40, 40), anchor='lm')
    d.text((x + 20, y + 66), f'Số: {no}', font=font(SANS, 24), fill=(160, 30, 28), anchor='lm')


def ruler(d, x, y, cm, px_per_cm, label_every=5):
    w = cm * px_per_cm
    d.rectangle([x, y, x + w, y + 46], fill=(240, 240, 236), outline=(40, 40, 40), width=2)
    for c in range(cm + 1):
        X = x + c * px_per_cm
        d.line([(X, y), (X, y + (22 if c % label_every == 0 else 12))], fill=(20, 20, 20), width=2 if c % label_every == 0 else 1)
        if c % label_every == 0:
            d.text((X, y + 34), str(c), font=font(BOLD, 16), fill=(20, 20, 20), anchor='mm')


# ── d01: ảnh báo đen trắng: sân phơi giấy điệp trong làng tranh ──────────────
def d01():
    random.seed(1)
    W, H = 1280, 800
    im = Image.new('L', (W, H), 210)
    d = ImageDraw.Draw(im)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=int(222 - 30 * y / H))
    # village houses with tiled roofs and a bamboo hedge behind the yard
    for x in range(-40, W + 60, 70):
        h = random.uniform(80, 150)
        for k in range(6):
            d.line([(x + k * 6, 360), (x + 20 + k * 4, 360 - h)], fill=110, width=3)
        d.ellipse([x - 20, 360 - h - 40, x + 70, 360 - h + 30], fill=126)
    for (x0, x1, top) in [(80, 520, 250), (760, 1220, 230)]:
        d.polygon([(x0 - 40, top + 80), (x0 + 60, top), (x1 - 60, top), (x1 + 40, top + 80)], fill=62)
        for k in range(12): d.line([(x0 - 30 + k * (x1 - x0 + 60) / 12, top + 76), (x0 + 60 + k * (x1 - x0 - 120) / 12, top + 4)], fill=48, width=2)
        d.rectangle([x0, top + 80, x1, 470], fill=128)
        for j in range(4):
            cx = x0 + 40 + j * (x1 - x0 - 80) / 3
            d.rectangle([cx - 34, top + 120, cx + 34, 470], fill=70)
    # brick courtyard
    d.rectangle([0, 470, W, H], fill=150)
    for y in range(480, H, 22):
        off = 0 if (y // 22) % 2 else 20
        d.line([(0, y), (W, y)], fill=132, width=1)
        for x in range(off, W, 40): d.line([(x, y), (x, y + 22)], fill=132, width=1)
    # rows of điệp paper sheets drying on the ground, in perspective
    for r in range(5):
        y = 500 + r * 56
        s = 0.7 + r * 0.14
        for k in range(9):
            x = 90 + k * 128 + (r % 2) * 50
            w, h = 86 * s, 40 * s
            d.polygon([(x, y), (x + w, y - 6 * s), (x + w + 10 * s, y + h), (x + 8 * s, y + h + 6 * s)], fill=int(222 - r * 4), outline=176)
    # two people bending far away (no faces)
    for x in (300, 960):
        d.ellipse([x - 9, 430, x + 9, 448], fill=60); d.polygon([(x - 16, 450), (x + 18, 446), (x + 24, 488), (x - 12, 492)], fill=60)
        d.polygon([(x - 26, 426), (x + 26, 426), (x, 410)], fill=80)  # nón lá
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    im = Image.merge('RGB', (im, im, im))
    im = grain(im, 24, 0.6).convert('L')
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageOps.colorize(im, (22, 20, 18), (238, 232, 218))
    save(vignette(im, 0.35), 'd01-bao-chi')


# ── shared: a carved woodblock relief (mice wedding procession, simplified) ──
def carve_scene(d, x0, y0, w, h, line, fill_mode=None, broken_parasol=False):
    """Simplified folk-print composition: mice carrying a palanquin under a parasol, cat at the left."""
    def mouse(cx, cy, s, carry=False):
        d.ellipse([cx - 26 * s, cy - 16 * s, cx + 26 * s, cy + 16 * s], outline=line, width=3, fill=fill_mode and fill_mode('body'))
        d.ellipse([cx + 18 * s, cy - 26 * s, cx + 42 * s, cy - 4 * s], outline=line, width=3, fill=fill_mode and fill_mode('head'))
        d.ellipse([cx + 22 * s, cy - 40 * s, cx + 34 * s, cy - 26 * s], outline=line, width=2)
        d.line([(cx - 26 * s, cy), (cx - 60 * s, cy - 18 * s)], fill=line, width=2)  # tail
        d.line([(cx - 10 * s, cy + 14 * s), (cx - 14 * s, cy + 34 * s)], fill=line, width=3)
        d.line([(cx + 12 * s, cy + 14 * s), (cx + 16 * s, cy + 34 * s)], fill=line, width=3)
        if carry: d.line([(cx - 4 * s, cy - 16 * s), (cx + 6 * s, cy - 50 * s)], fill=line, width=3)
    s = w / 900
    base = y0 + h * 0.72
    # cat waiting at the left
    cx = x0 + 110 * s
    d.ellipse([cx - 60 * s, base - 120 * s, cx + 40 * s, base], outline=line, width=3, fill=fill_mode and fill_mode('cat'))
    d.ellipse([cx - 30 * s, base - 190 * s, cx + 40 * s, base - 120 * s], outline=line, width=3, fill=fill_mode and fill_mode('cat'))
    d.polygon([(cx - 26 * s, base - 182 * s), (cx - 18 * s, base - 214 * s), (cx - 4 * s, base - 188 * s)], outline=line, fill=None)
    d.polygon([(cx + 14 * s, base - 186 * s), (cx + 30 * s, base - 212 * s), (cx + 36 * s, base - 180 * s)], outline=line, fill=None)
    # procession
    for k, px in enumerate([280, 400, 560, 680, 800]):
        mouse(x0 + px * s, base - 40 * s, s * 1.9, carry=k in (1, 2, 3))
    # palanquin on the shoulders of mice 2–3
    pxa, pxb = x0 + 380 * s, x0 + 700 * s
    d.line([(pxa, base - 136 * s), (pxb, base - 136 * s)], fill=line, width=4)
    d.rectangle([x0 + 470 * s, base - 260 * s, x0 + 610 * s, base - 138 * s], outline=line, width=3, fill=fill_mode and fill_mode('palanquin'))
    d.polygon([(x0 + 450 * s, base - 260 * s), (x0 + 540 * s, base - 316 * s), (x0 + 630 * s, base - 260 * s)], outline=line, fill=fill_mode and fill_mode('roof'))
    # parasol (lọng) held by the front mouse; its pointed tip may be broken off
    tx, ty = x0 + 820 * s, base - 300 * s
    d.line([(x0 + 812 * s, base - 120 * s), (tx, ty)], fill=line, width=3)
    d.pieslice([tx - 80 * s, ty - 50 * s, tx + 80 * s, ty + 50 * s], 180, 360, outline=line, fill=fill_mode and fill_mode('parasol'))
    if not broken_parasol:
        d.polygon([(tx - 8 * s, ty - 50 * s), (tx, ty - 78 * s), (tx + 8 * s, ty - 50 * s)], fill=line)
    # border frame of the block
    d.rectangle([x0 + 10, y0 + 10, x0 + w - 10, y0 + h - 10], outline=line, width=5)
    return (tx, ty - 50 * s)


# ── d03: bản khắc gỗ thị gãy đôi, mẻ chóp lọng, giọt son đỏ ở mép gãy ──────────
def d03():
    random.seed(3)
    W, H = 1200, 900
    im = tint(noise((W, H), 22, 2), (40, 34, 30), (84, 74, 62))  # dark workbench
    bw, bh = 760, 560  # 30 x 40 cm board (landscape), ~19 px / cm
    board = Image.new('RGB', (bw, bh))
    grainb = noise((bw // 8, bh), 60, 0).resize((bw, bh), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.5))
    board.paste(tint(grainb, (150, 110, 52), (214, 170, 96)), (0, 0))
    bd = ImageDraw.Draw(board)
    for k in range(40):
        x = random.uniform(0, bw)
        bd.line(bezier((x, 0), (x + random.uniform(-20, 20), bh / 3), (x + random.uniform(-20, 20), 2 * bh / 3), (x + random.uniform(-10, 10), bh)), fill=(150, 108, 54), width=1)
    # relief: ink-blackened raised lines from years of printing
    tip = carve_scene(bd, 0, 0, bw, bh, (34, 26, 20), broken_parasol=True)
    # split the board in two along a jagged line and shift the halves apart
    cut = [(bw * 0.52 + random.uniform(-16, 16), y) for y in range(0, bh + 1, 28)]
    left = Image.new('L', (bw, bh), 0)
    ImageDraw.Draw(left).polygon([(0, 0)] + cut + [(0, bh)], fill=255)
    right = ImageChops.invert(left)
    ox, oy = (W - bw) // 2, (H - bh) // 2 - 20
    for mask, dx, rot in ((left, -28, 2.0), (right, 26, -2.4)):
        piece = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
        piece.paste(board, (0, 0), mask)
        piece = piece.rotate(rot, resample=Image.BICUBIC, center=(bw / 2, bh / 2))
        sh = piece.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.7))
        im.paste((0, 0, 0), (ox + dx + 12, oy + 16), sh)
        im.paste(piece, (ox + dx, oy), piece)
    d = ImageDraw.Draw(im)
    # splintered fibres along the break
    for (x, y) in cut[1:-1]:
        for side, dx in ((-1, -28), (1, 26)):
            X = ox + dx + x
            d.line([(X, oy + y), (X + side * random.uniform(4, 14), oy + y + random.uniform(-8, 8))], fill=(232, 196, 130), width=2)
    # fresh vermilion drop on the break edge
    vx, vy = ox - 28 + cut[9][0], oy + cut[9][1]
    d.ellipse([vx - 12, vy - 9, vx + 10, vy + 11], fill=VERMILION)
    d.ellipse([vx - 6, vy - 6, vx - 1, vy - 1], fill=(240, 120, 100))
    d.line([(vx, vy + 10), (vx + 2, vy + 30)], fill=VERMILION, width=4)
    # missing parasol tip: a fresh light notch where it broke off
    tx, ty = ox + 26 + tip[0], oy + tip[1]
    d.polygon([(tx - 10, ty + 2), (tx, ty - 26), (tx + 10, ty + 2)], fill=(226, 190, 126))
    ruler(d, 220, 800, 30, 19)
    tag(d, 960, 60, '03')
    im = light_spot(im, 600, 380, 520, 0.24)
    im = vignette(im, 0.55)
    save(grain(im, 8, 0.4), 'd03-ban-khac')


# ── d04: sơ đồ làng: sân đình, xưởng tranh, đường cái, ngõ tắt ven đê ───────
def d04():
    random.seed(4)
    W, H = 1400, 1000
    im = Image.new('RGB', (W, H), (243, 240, 228))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(224, 226, 224) if x % 125 else (206, 212, 212))
    for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(224, 226, 224) if y % 125 else (206, 212, 212))
    INK, SOFT, RED, BLUE, MUD, GREEN = (40, 48, 76), (112, 120, 140), (178, 34, 30), (70, 120, 180), (176, 86, 50), (72, 112, 70)
    d.text((60, 46), 'CÔNG AN XÃ SONG HỒ', font=font(BOLD, 22), fill=INK, anchor='lm')
    d.text((60, 74), 'huyện Thuận Thành, tỉnh Bắc Ninh', font=font(SANS, 18), fill=INK, anchor='lm')
    d.text((W / 2 + 90, 52), 'SƠ ĐỒ KHU VỰC LÀNG ĐÔNG HỒ', font=font(BOLD, 32), fill=INK, anchor='mm')
    d.text((W / 2 + 90, 90), 'Lập 23h30 ngày 22/01/2001 (đêm 28 Tết) · tỷ lệ gần đúng', font=font(ITAL, 20), fill=INK, anchor='mm')
    # Đuống river along the top, dyke parallel to it
    river = [(0, 200), (300, 180), (650, 210), (1000, 190), (1400, 214)]
    d.polygon(river + [(1400, 120), (0, 120)], fill=(196, 216, 236))
    d.line(river, fill=BLUE, width=3)
    d.text((1060, 150), 'SÔNG ĐUỐNG', font=font(BOLD, 24), fill=BLUE, anchor='mm')
    dyke = [(0, 256), (300, 236), (650, 266), (1000, 246), (1400, 270)]
    d.line(dyke, fill=GREEN, width=10)
    d.text((180, 226), 'đê sông Đuống', font=font(ITAL, 18), fill=GREEN, anchor='mm')
    # village pond, houses, bamboo
    d.ellipse([560, 560, 760, 660], fill=(206, 224, 236), outline=BLUE, width=2)
    d.text((660, 610), 'ao làng', font=font(ITAL, 16), fill=BLUE, anchor='mm')
    for _ in range(26):
        x, y = random.uniform(120, 1300), random.uniform(380, 900)
        if abs(x - 660) < 140 and abs(y - 610) < 80: continue
        if abs(x - 260) < 150 and abs(y - 470) < 120: continue
        if abs(x - 1120) < 150 and abs(y - 470) < 120: continue
        if 380 < y < 500 or (x > 1080 and y > 700) or (x < 380 and y > 740) or (560 < x < 860 and y > 860): continue
        d.rectangle([x - 26, y - 14, x + 26, y + 14], outline=SOFT, width=2)
    # đình (left) and the workshop (right)
    def building(x, y, w, h, label, sub, col):
        d.rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], outline=col, width=4, fill=(243, 240, 228))
        d.polygon([(x - w / 2 - 14, y - h / 2), (x, y - h / 2 - 32), (x + w / 2 + 14, y - h / 2)], outline=col, fill=None)
        d.text((x, y - 8), label, font=font(BOLD, 20), fill=col, anchor='mm')
        d.text((x, y + 18), sub, font=font(ITAL, 15), fill=SOFT, anchor='mm')
    building(260, 470, 220, 90, 'ĐÌNH LÀNG', 'sân đình: chiếu bóng tối 28 Tết', INK)
    d.rectangle([150, 530, 370, 610], outline=INK, width=2)
    d.text((260, 570), 'SÂN ĐÌNH', font=font(BOLD, 17), fill=INK, anchor='mm')
    building(1120, 470, 240, 90, 'XƯỞNG TRANH', 'nghệ nhân Nguyễn Đăng Thao', RED)
    d.rectangle([1176, 404, 1210, 424], fill=(243, 240, 228), outline=RED, width=2)
    d.text((1194, 390), 'cổng sau', font=font(SANS, 15), fill=RED, anchor='mm')
    # main road (dry crushed stone), long way round through the village
    road = [(370, 560), (430, 760), (700, 860), (1000, 800), (1120, 560)]
    for k in range(len(road) - 1):
        d.line([road[k], road[k + 1]], fill=(150, 150, 150), width=18)
        d.line([road[k], road[k + 1]], fill=(214, 212, 204), width=12)
    for _ in range(140):
        k = random.randrange(len(road) - 1); t = random.random()
        x = road[k][0] + (road[k + 1][0] - road[k][0]) * t; y = road[k][1] + (road[k + 1][1] - road[k][1]) * t
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(130, 130, 128))
    d.text((700, 900), 'Đường cái rải đá dăm, khô ráo · đi bộ khoảng 15 phút', font=font(BOLD, 18), fill=INK, anchor='mm')
    # shortcut along the dyke: red alluvial mud path from behind the đình to the workshop back gate
    short = [(300, 425), (330, 300), (650, 300), (1000, 290), (1190, 300), (1194, 404)]
    for k in range(len(short) - 1):
        a, b = short[k], short[k + 1]
        L = int(math.dist(a, b) // 18)
        for j in range(L):
            t0, t1 = j / L, (j + 0.6) / L
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=MUD, width=6)
    d.text((760, 326), 'Ngõ tắt ven đê: lối mòn đất bùn đỏ phù sa · khoảng 5 phút', font=font(BOLD, 18), fill=MUD, anchor='mm')
    # straight-line distance
    d.line([(370, 470), (1000, 470)], fill=SOFT, width=1)
    for x in (370, 1000): d.line([(x, 462), (x, 478)], fill=SOFT, width=2)
    d.text((685, 456), '≈ 800 m đường chim bay', font=font(ITAL, 17), fill=SOFT, anchor='mm')
    # legend, north, stamp
    LX, LY = 60, 760
    d.rectangle([LX, LY, LX + 300, LY + 120], outline=INK, width=2, fill=(243, 240, 228))
    d.text((LX + 16, LY + 22), 'GHI CHÚ', font=font(BOLD, 18), fill=INK, anchor='lm')
    d.line([(LX + 16, LY + 56), (LX + 50, LY + 56)], fill=(214, 212, 204), width=10); d.text((LX + 62, LY + 56), 'Đường cái đá dăm', font=font(SANS, 16), fill=INK, anchor='lm')
    d.line([(LX + 16, LY + 92), (LX + 30, LY + 92)], fill=MUD, width=6); d.line([(LX + 38, LY + 92), (LX + 50, LY + 92)], fill=MUD, width=6)
    d.text((LX + 62, LY + 92), 'Ngõ tắt bùn đỏ ven đê', font=font(SANS, 16), fill=INK, anchor='lm')
    nx, ny = 1320, 820
    d.polygon([(nx, ny - 50), (nx - 16, ny + 10), (nx, ny), (nx + 16, ny + 10)], fill=INK); d.text((nx, ny - 70), 'N', font=font(BOLD, 24), fill=INK, anchor='mm')
    st = Image.new('RGBA', (200, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.ellipse([8, 8, 192, 192], outline=RED + (210,), width=6); sd.ellipse([38, 38, 162, 162], outline=RED + (210,), width=3)
    sd.text((100, 88), 'CÔNG AN XÃ', font=font(BOLD, 18), fill=RED + (220,), anchor='mm'); sd.text((100, 116), 'SONG HỒ', font=font(BOLD, 20), fill=RED + (220,), anchor='mm')
    st = st.rotate(-10, resample=Image.BICUBIC)
    im.paste(st, (1120, 740), st)
    im = im.filter(ImageFilter.GaussianBlur(0.35))
    save(grain(im, 5, 0.4), 'd04-so-do-lang-tranh')


# ── d07: bản dập thử tranh Đám cưới chuột trên giấy điệp ─────────────────────
def d07():
    random.seed(7)
    W, H = 1200, 900
    im = tint(noise((W, H), 26, 2), (60, 44, 32), (112, 86, 62))  # wooden table
    pw, ph = 900, 640
    paper = tint(noise((pw, ph), 26, 0.6), (222, 212, 186), (248, 242, 224))
    shimmer = noise((pw, ph), 80, 0.5).point(lambda v: 255 if v > 214 else 0)  # điệp shell sparkle
    paper.paste((255, 255, 250), (0, 0), shimmer.point(lambda v: v // 3))
    pd = ImageDraw.Draw(paper)
    COL = {'body': (126, 126, 120), 'head': (126, 126, 120), 'cat': (214, 162, 52), 'palanquin': (190, 50, 34), 'roof': (70, 120, 70), 'parasol': (204, 56, 36)}
    # colour blocks printed slightly off-register, then the black key block on top
    layer = Image.new('RGB', (pw, ph), (0, 0, 0)); lm = Image.new('L', (pw, ph), 0)
    carve_scene(ImageDraw.Draw(layer), 34, 54, 840, 560, (0, 0, 0), fill_mode=lambda k: COL[k])
    carve_scene(ImageDraw.Draw(lm), 34, 54, 840, 560, 0, fill_mode=lambda k: 230)
    paper.paste(layer.filter(ImageFilter.GaussianBlur(0.6)), (5, -3), lm.filter(ImageFilter.GaussianBlur(1)))
    ink = Image.new('L', (pw, ph), 0)
    carve_scene(ImageDraw.Draw(ink), 30, 50, 840, 560, 255)
    ink = ImageChops.multiply(ink, noise((pw, ph), 60, 0.6).point(lambda v: 255 if v > 70 else 120))  # woodblock texture in the ink
    paper.paste(BLACK_INK, (0, 0), ink)
    pd = ImageDraw.Draw(paper)
    # a tiny spot where the parasol tip printed light (worn)
    page = paper.rotate(-1.5, resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0))
    m = Image.new('L', paper.size, 255).rotate(-1.5, resample=Image.BICUBIC, expand=True)
    ox, oy = (W - page.size[0]) // 2, (H - page.size[1]) // 2
    im.paste((0, 0, 0), (ox + 10, oy + 14), m.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.55)))
    im.paste(page, (ox, oy), m)
    im = light_spot(im, 520, 340, 560, 0.18)
    im = vignette(im, 0.45)
    save(grain(im, 6, 0.4), 'd07-tranh-dong-ho')


# ── d10: dăm gỗ thị hình chóp lọng dài 2 cm dính son, đặt cạnh mép vỡ ─────────
def d10():
    random.seed(10)
    W, H = 1200, 900
    im = tint(noise((W, H), 14, 2), (200, 202, 204), (238, 240, 242))  # white evidence tray (macro)
    d = ImageDraw.Draw(im)
    # macro scale: 1 cm = 150 px
    cx, cy = 560, 420
    chip = [(cx - 60, cy + 120), (cx + 70, cy + 110), (cx + 14, cy - 170), (cx - 4, cy - 176)]  # 2 cm cone
    paste_shadow(im, soft_shadow((W, H), chip, 14, (14, 20), 150))
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon(chip, fill=255)
    wood = tint(noise((W // 6, H), 60, 0).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1)), (164, 118, 56), (224, 182, 108))
    im.paste(wood, (0, 0), m)
    d = ImageDraw.Draw(im)
    for k in range(9):  # wood grain running along the cone
        t = k / 8
        d.line([(cx - 56 + 124 * t, cy + 116 - 10 * t), (cx + 4 + 10 * t, cy - 168)], fill=(150, 104, 48), width=1)
    d.line([(cx - 56, cy + 118), (cx + 68, cy + 110)], fill=(240, 206, 140), width=4)  # fresh broken base (light)
    for k in range(10):
        x = cx - 50 + k * 12
        d.line([(x, cy + 116), (x + random.uniform(-4, 4), cy + 128)], fill=(236, 200, 130), width=2)
    # the ink-blackened carved surface on one face + vermilion smear
    d.polygon([(cx - 4, cy - 176), (cx + 14, cy - 170), (cx + 40, cy + 20), (cx + 6, cy + 30)], fill=(52, 40, 30))
    smear = Image.new('L', (W, H), 0)
    sd = ImageDraw.Draw(smear)
    for _ in range(18):
        x, y = cx + random.uniform(-30, 50), cy + random.uniform(-20, 90)
        r = random.uniform(8, 20)
        sd.ellipse([x - r, y - r * 0.7, x + r, y + r * 0.7], fill=int(random.uniform(150, 240)))
    smear = ImageChops.multiply(smear.filter(ImageFilter.GaussianBlur(3)), m)
    im.paste(VERMILION, (0, 0), smear)
    d = ImageDraw.Draw(im)
    # tweezers holding position + scale bar 0–3 cm
    d.polygon([(860, 120), (1140, 40), (1150, 60), (880, 150)], fill=(160, 164, 170)); d.polygon([(880, 150), (1150, 60), (1156, 84), (890, 176)], fill=(130, 134, 140))
    ruler(d, 300, 760, 3, 150, label_every=1)
    d.text((300 + 225, 830), 'cm (ảnh phóng đại)', font=font(ITAL, 18), fill=(60, 60, 60), anchor='mm')
    tag(d, 940, 700, '10')
    im = light_spot(im, 560, 360, 480, 0.18)
    im = vignette(im, 0.4)
    save(grain(im, 6, 0.4), 'd10-dam-go')


if __name__ == '__main__':
    for name in sys.argv[1:] or ['d01', 'd03', 'd04', 'd07', 'd10']:
        globals()[name]()
