"""Vẽ minh hoạ ảnh tư liệu cho hồ sơ 11 (Hồi chuông núi Sài Sơn) bằng Pillow, không cần mô hình tạo ảnh.

Chạy: python3 authoring/hoi-chuong-chua-thay/draw_images.py [d01|d03|d05|d08|d11 ...]
Dùng chung bộ hàm vẽ của authoring/lua-than-tay-nguyen/draw_photos.py.
d08 cố ý KHÔNG vẽ cơ chế bẫy nước (đáp án câu 3, vòng 3): đó là bản phác tay của người làm bếp theo lời khai vòng 2.
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

OUT = 'public/cases/hoi-chuong-chua-thay/images/'
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(name if name.startswith('/') else F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
HAND = '/System/Library/Fonts/Noteworthy.ttc'  # has full Vietnamese diacritics


def save(im, name, q=86):
    im.save(OUT + name + '.webp', 'WEBP', quality=q, method=6)
    print('ok', name, im.size)


def pagoda_roof(d, cx, y, w, h, fill, tiers=1, curl=18):
    """Vietnamese temple roof seen from the front: curved ridge, upturned eave corners."""
    for t in range(tiers):
        yy = y + t * h * 0.9
        ww = w * (1 + t * 0.28)
        pts = bezier((cx - ww / 2 - curl, yy + h - curl), (cx - ww / 2 + ww * 0.1, yy + h * 0.9), (cx - ww * 0.25, yy + h * 0.15), (cx - ww * 0.18, yy), 16)
        pts += [(cx + ww * 0.18, yy)]
        pts += bezier((cx + ww * 0.25, yy + h * 0.15), (cx + ww / 2 - ww * 0.1, yy + h * 0.9), (cx + ww / 2 + curl, yy + h - curl), (cx + ww / 2 + curl * 0.4, yy + h), 16)
        pts += [(cx - ww / 2 - curl * 0.4, yy + h)]
        d.polygon(pts, fill=fill)


# ── d01: ảnh báo đen trắng: núi Sài Sơn, mái chùa thấp thoáng, lối bậc đá ─────
def d01():
    random.seed(1)
    W, H = 1280, 800
    im = Image.new('L', (W, H), 210)
    d = ImageDraw.Draw(im)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=int(218 - 28 * y / H))
    # far hills and the rounded limestone mountain
    d.polygon([(0, 520)] + [(x, 520 - 40 * math.sin(x / 260)) for x in range(0, W + 20, 20)] + [(W, 800), (0, 800)], fill=176)
    mtn = bezier((140, 640), (260, 250), (520, 110), (700, 120), 30) + bezier((700, 120), (900, 130), (1060, 300), (1180, 640), 30)
    d.polygon(mtn + [(1180, 800), (140, 800)], fill=122)
    tex = noise((W, H), 60, 2.2).point(lambda v: int((v - 128) * 0.4 + 128))
    m = Image.new('L', (W, H), 0)
    ImageDraw.Draw(m).polygon(mtn + [(1180, 800), (140, 800)], fill=255)
    im = Image.composite(ImageChops.add(im, tex, 1, -128), im, m)
    d = ImageDraw.Draw(im)
    # tree clumps over the mountain
    for _ in range(420):
        x = random.uniform(170, 1150); y = random.uniform(150, 720)
        if not m.getpixel((int(x), int(y))): continue
        r = random.uniform(10, 26)
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=int(random.uniform(78, 120)))
    # zig-zag stone steps up the slope
    steps = [(620, 760), (600, 640), (700, 560), (650, 460), (720, 380), (690, 300), (720, 210)]
    for a, b in zip(steps, steps[1:]):
        d.line([a, b], fill=196, width=10)
        L = int(math.dist(a, b) // 12)
        for k in range(L):
            t = k / L
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            d.line([(x - 7, y), (x + 7, y)], fill=150, width=1)
    # temple roofs: main hall mid-slope, bell tower (two-tier) and hermitage on the summit
    pagoda_roof(d, 560, 470, 170, 46, 58)
    d.rectangle([500, 516, 620, 560], fill=70)
    pagoda_roof(d, 735, 142, 70, 30, 52, tiers=2, curl=10)
    d.rectangle([712, 196, 758, 226], fill=66)
    pagoda_roof(d, 820, 170, 80, 26, 60, curl=10)
    d.rectangle([790, 194, 850, 222], fill=72)
    # three-entrance gate at the foot, small figures far away (no faces)
    d.rectangle([560, 690, 700, 760], fill=96)
    for x in (580, 620, 660): d.rectangle([x, 712, x + 24, 760], fill=60)
    pagoda_roof(d, 630, 660, 150, 34, 56, curl=12)
    for x in (470, 492, 760, 784, 806):
        d.ellipse([x - 6, 728, x + 6, 740], fill=56); d.rectangle([x - 8, 740, x + 8, 772], fill=56)
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    im = Image.merge('RGB', (im, im, im))
    im = grain(im, 24, 0.6).convert('L')
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageOps.colorize(im, (22, 20, 18), (238, 232, 218))
    save(vignette(im, 0.35), 'd01-bao-chi')


# ── d03: sơ đồ quần thể chùa theo ba tầng núi ────────────────────────────────
def d03():
    random.seed(3)
    W, H = 1400, 1050
    im = Image.new('RGB', (W, H), (242, 238, 226))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(224, 226, 226) if x % 125 else (206, 212, 214))
    for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(224, 226, 226) if y % 125 else (206, 212, 214))
    INK, SOFT, RED, GREEN = (40, 48, 76), (112, 120, 140), (178, 34, 30), (72, 112, 70)
    d.text((60, 46), 'CÔNG AN TỈNH HÀ TÂY', font=font(BOLD, 22), fill=INK, anchor='lm')
    d.text((60, 74), 'Phòng Kỹ thuật hình sự', font=font(SANS, 20), fill=INK, anchor='lm')
    d.text((W / 2 + 90, 52), 'SƠ ĐỒ QUẦN THỂ CHÙA CỔ SƠN, NÚI SÀI SƠN', font=font(BOLD, 30), fill=INK, anchor='mm')
    d.text((W / 2 + 90, 88), 'Lập 15h30 ngày 01/04/2004 · không theo tỷ lệ', font=font(ITAL, 20), fill=INK, anchor='mm')
    # mountain profile (side view) with contour lines
    prof = bezier((80, 980), (300, 760), (520, 330), (760, 210), 40) + bezier((760, 210), (980, 230), (1180, 600), (1340, 980), 40)
    for k in range(6):
        d.line([(x, y + k * 34) for x, y in prof if y + k * 34 < 990], fill=(176, 186, 196), width=1)
    d.line(prof, fill=INK, width=4)
    # 300 stone steps zig-zagging up
    path = [(230, 930), (360, 860), (300, 790), (470, 700), (420, 620), (560, 520), (520, 440), (650, 340), (620, 280), (720, 236)]
    for a, b in zip(path, path[1:]):
        d.line([a, b], fill=SOFT, width=5)
    for (x, y) in path[1::2]:
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=SOFT)
    d.text((240, 560), '300 bậc đá →', font=font(BOLD, 20), fill=SOFT, anchor='mm')
    def building(x, y, w, h, label, sub=None, col=INK, roof=True):
        d.rectangle([x - w / 2, y - h / 2, x + w / 2, y + h / 2], outline=col, width=3, fill=(242, 238, 226))
        if roof:
            d.polygon([(x - w / 2 - 10, y - h / 2), (x, y - h / 2 - 22), (x + w / 2 + 10, y - h / 2)], outline=col, fill=None)
        d.text((x, y - (8 if sub else 0)), label, font=font(BOLD, 18), fill=col, anchor='mm')
        if sub: d.text((x, y + 16), sub, font=font(ITAL, 15), fill=SOFT, anchor='mm')
    # foot of the mountain
    building(180, 960, 150, 50, 'NHÀ KHÁCH', 'phật tử thụ lộc trưa')
    building(380, 980, 130, 40, 'BẾP CHAY')
    building(560, 980, 150, 40, 'TAM QUAN')
    # mid-slope
    building(860, 560, 190, 60, 'CHÍNH ĐIỆN')
    building(1060, 640, 160, 50, 'TĂNG XÁ', 'chỗ ở của đệ tử')
    d.line([(560, 520), (765, 556)], fill=SOFT, width=2)
    # summit: bell tower and hermitage, 15 m apart
    building(620, 158, 150, 56, 'GÁC CHUÔNG', 'hai tầng mái', col=INK)
    building(900, 158, 170, 56, 'TỊNH THẤT', 'am thiền sư trụ trì', col=RED)
    d.line([(695, 200), (815, 200)], fill=INK, width=2)
    for x in (695, 815): d.line([(x, 192), (x, 208)], fill=INK, width=2)
    d.text((755, 186), '15 m', font=font(BOLD, 17), fill=INK, anchor='mm')
    # level labels on the right
    for (y, t) in [(400, 'ĐỈNH NÚI ↑'), (760, 'LƯNG CHỪNG NÚI'), (1022, 'CHÂN NÚI')]:
        d.text((40, y), t, font=font(BOLD, 18), fill=SOFT, anchor='lm')
    # trees
    for _ in range(40):
        x, y = random.uniform(120, 1300), random.uniform(260, 900)
        if (abs(x - 860) < 140 and abs(y - 560) < 60) or (abs(x - 1060) < 110 and abs(y - 640) < 50) or x < 300 and y > 380: continue
        d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=GREEN, width=2)
    # legend + stamp
    LX, LY = 1020, 250
    d.rectangle([LX, LY, LX + 320, LY + 110], outline=INK, width=2, fill=(242, 238, 226))
    d.text((LX + 16, LY + 22), 'GHI CHÚ', font=font(BOLD, 18), fill=INK, anchor='lm')
    d.rectangle([LX + 16, LY + 44, LX + 40, LY + 62], outline=RED, width=3); d.text((LX + 52, LY + 53), 'Nơi phát hiện nạn nhân', font=font(SANS, 17), fill=INK, anchor='lm')
    d.line([(LX + 16, LY + 86), (LX + 40, LY + 86)], fill=SOFT, width=5); d.text((LX + 52, LY + 86), 'Lối bậc đá lên đỉnh', font=font(SANS, 17), fill=INK, anchor='lm')
    st = Image.new('RGBA', (210, 210), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.ellipse([8, 8, 202, 202], outline=RED + (210,), width=6); sd.ellipse([40, 40, 170, 170], outline=RED + (210,), width=3)
    sd.text((105, 92), 'CÔNG AN', font=font(BOLD, 20), fill=RED + (220,), anchor='mm'); sd.text((105, 120), 'HÀ TÂY', font=font(BOLD, 20), fill=RED + (220,), anchor='mm')
    st = st.rotate(-10, resample=Image.BICUBIC)
    im.paste(st, (60, 120), st)
    im = im.filter(ImageFilter.GaussianBlur(0.35))
    save(grain(im, 5, 0.4), 'd03-so-do-chua')


# ── d05: tầng 2 gác chuông: đại hồng chung, chày gỗ, dây dù xanh, vũng nước ──
def d05():
    random.seed(5)
    W, H = 1200, 900
    im = tint(noise((W, H), 30, 2), (28, 22, 18), (70, 56, 44))  # dim timber interior
    d = ImageDraw.Draw(im)
    # roof beams + rafters
    for y, w in ((60, 34), (150, 26)):
        d.rectangle([0, y, W, y + w], fill=(52, 38, 26)); d.line([(0, y + w), (W, y + w)], fill=(20, 14, 10), width=3)
    for x in range(-100, W + 100, 90):
        d.line([(x, 0), (x + 140, 60)], fill=(44, 32, 22), width=10)
    for x in (120, 1080):
        d.rectangle([x - 26, 0, x + 26, H], fill=(60, 44, 30)); d.line([(x + 26, 0), (x + 26, H)], fill=(24, 18, 12), width=3)
    # floor planks (lim wood), perspective
    for k in range(14):
        y = 640 + k * k * 1.6
        d.line([(0, y), (W, y)], fill=(40, 28, 18), width=2)
    floor = Image.new('L', (W, H), 0)
    ImageDraw.Draw(floor).rectangle([0, 640, W, H], fill=255)
    im.paste(tint(noise((W, H), 30, 1.4), (58, 38, 24), (110, 78, 50)), (0, 0), floor)
    d = ImageDraw.Draw(im)
    for k in range(10):
        y = 640 + k * k * 2.6
        d.line([(0, y), (W, y)], fill=(36, 24, 16), width=2)
    # the bronze bell (dark), hung from the main beam
    bx, top, bot = 520, 210, 640
    d.line([(bx, 86), (bx, top)], fill=(30, 26, 22), width=14)
    bell = bezier((bx - 40, top - 10), (bx - 120, top - 4), (bx - 128, top + 40), (bx - 128, top + 80), 20) + [(bx - 132, bot - 80)] \
        + bezier((bx - 132, bot - 80), (bx - 134, bot - 30), (bx - 148, bot - 6), (bx - 156, bot), 12) + [(bx + 156, bot)] \
        + bezier((bx + 156, bot), (bx + 148, bot - 6), (bx + 134, bot - 30), (bx + 132, bot - 80), 12) + [(bx + 128, top + 80)] \
        + bezier((bx + 128, top + 80), (bx + 128, top + 40), (bx + 120, top - 4), (bx + 40, top - 10), 20)
    paste_shadow(im, soft_shadow((W, H), bell, 24, (20, 26), 160))
    bm = Image.new('L', (W, H), 0)
    ImageDraw.Draw(bm).polygon(bell, fill=255)
    bronze = tint(noise((W, H), 36, 2), (40, 30, 18), (150, 118, 70))
    shade = Image.new('L', (W, H))
    for x in range(W):
        v = int(70 + 150 * max(0, math.cos((x - bx + 50) / 160)))
        ImageDraw.Draw(shade).line([(x, 0), (x, H)], fill=max(0, min(255, v)))
    bronze = Image.composite(bronze, Image.new('RGB', (W, H), (16, 14, 10)), shade)
    im.paste(bronze, (0, 0), bm)
    d = ImageDraw.Draw(im)
    for y in (top + 60, top + 230, bot - 50):  # cast horizontal bands
        d.line([(bx - 130, y), (bx + 130, y)], fill=(170, 140, 88), width=5)
        d.line([(bx - 130, y + 6), (bx + 130, y + 6)], fill=(40, 30, 18), width=2)
    for x in (-66, 0, 66):  # vertical panel ribs
        d.line([(bx + x, top + 60), (bx + x, top + 230)], fill=(150, 120, 74), width=4)
    d.ellipse([bx + 70, bot - 120, bx + 110, bot - 80], outline=(170, 140, 88), width=4)  # striking boss (lotus)
    d.rectangle([bx - 40, top - 26, bx + 40, top + 4], fill=(56, 48, 34))  # crown loop
    # horizontal lim-wood striker hung by two ropes, a green parachute cord leading up to the roof beam
    sx0, sx1, sy = 720, 1100, 400
    for x in (790, 1020):
        d.line([(x, 86), (x, sy - 14)], fill=(150, 126, 86), width=4)
    paste_shadow(im, soft_shadow((W, H), [(sx0, sy - 24), (sx1, sy - 24), (sx1, sy + 24), (sx0, sy + 24)], 12, (10, 16), 150))
    d.rounded_rectangle([sx0, sy - 24, sx1, sy + 24], 22, fill=(96, 62, 34))
    d.line([(sx0 + 20, sy - 12), (sx1 - 20, sy - 12)], fill=(146, 100, 58), width=4)
    d.line(bezier((sx0 + 40, sy - 20), (sx0 + 60, 300), (900, 200), (930, 86), 40), fill=(40, 150, 72), width=5)  # green cord
    # wet puddle on the floor under the bell rim
    pud = Image.new('L', (W, H), 0)
    pd = ImageDraw.Draw(pud)
    for k in range(9):
        x = bx + random.uniform(-110, 140); y = 700 + random.uniform(-14, 24); r = random.uniform(40, 90)
        pd.ellipse([x - r, y - r * 0.28, x + r, y + r * 0.28], fill=255)
    pud = pud.filter(ImageFilter.GaussianBlur(4))
    im.paste((22, 20, 20), (0, 0), pud.point(lambda v: int(v * 0.8)))
    refl = ImageChops.multiply(pud, noise((W, H), 70, 2).point(lambda v: 200 if v > 175 else 0))
    im.paste((200, 196, 186), (0, 0), refl)
    d = ImageDraw.Draw(im)
    im = light_spot(im, 700, 330, 520, 0.3)  # flash
    im = vignette(im, 0.6)
    save(grain(im, 10, 0.5), 'd05-gac-chuong')


# ── d08: bản phác tay của người làm bếp (theo lời khai vòng 2) ────────────────
def d08():
    random.seed(8)
    W, H = 1200, 900
    desk = tint(noise((W, H), 30, 1.6), (62, 44, 30), (120, 88, 60))
    im = desk
    pw, ph = 980, 760
    page = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
    paper = tint(noise((pw, ph), 14, 0.8), (226, 220, 200), (246, 242, 226))
    page.paste(paper, (0, 0))
    pd = ImageDraw.Draw(page)
    for y in range(80, ph, 34): pd.line([(0, y), (pw, y)], fill=(150, 176, 206, 255), width=1)  # ruled school notebook
    pd.line([(90, 0), (90, ph)], fill=(206, 90, 90, 255), width=2)
    for y in range(40, ph, 70): pd.ellipse([24, y, 44, y + 20], fill=(70, 52, 36, 255))  # ring holes
    ink, red = (34, 52, 120, 255), (178, 40, 36, 255)
    hand = font(HAND, 24); small = font(HAND, 20)
    pd.text((130, 50), 'Chỗ tôi đứng làm bếp - sáng 01/4', font=font(HAND, 28), fill=ink, anchor='lm')
    # wobbly hand-drawn mountain, path and buildings
    def wob(pts, a=2.4): return [(x + random.uniform(-a, a), y + random.uniform(-a, a)) for x, y in pts]
    mtn = bezier((300, 640), (380, 380), (470, 170), (600, 150), 30) + bezier((600, 150), (730, 170), (790, 420), (860, 640), 30)
    pd.line(wob(mtn), fill=ink, width=3)
    path = [(470, 640), (430, 560), (520, 480), (470, 400), (560, 320), (530, 250), (610, 180)]
    pd.line(wob(path), fill=ink, width=2)
    for x, y in path[1:-1]: pd.line([(x - 8, y), (x + 8, y)], fill=ink, width=2)
    pd.text((380, 470), 'đường bậc đá', font=small, fill=ink, anchor='mm')
    pd.text((600, 120), 'đỉnh núi (chùa trên)', font=small, fill=ink, anchor='mm')
    for (x, y, label) in [(240, 690, 'nhà khách'), (470, 700, 'bếp'), (700, 690, 'tam quan')]:
        pd.rectangle(wob([(x - 60, y - 24), (x + 60, y + 24)], 1), outline=ink, width=2)
        pd.text((x, y), label, font=small, fill=ink, anchor='mm')
    # where she stood, looking at the bottom of the steps
    pd.text((470, 652), 'X', font=font(HAND, 34), fill=red, anchor='mm')
    pd.line(wob([(470, 640), (450, 600)]), fill=red, width=2)
    for k, t in enumerate(['~10h15: thấy thầy Quảng Chân', 'từ trên núi đi xuống, áo ướt', 'mồ hôi, tay cầm nải chuối']):
        pd.text((120, 190 + k * 32), t, font=hand, fill=ink, anchor='lm')
    pd.line(wob(bezier((300, 290), (330, 420), (400, 560), (462, 622), 14)), fill=ink, width=2)
    pd.polygon([(466, 628), (444, 620), (458, 604)], fill=ink)
    pd.text((120, 560), '11h15: thầy ngồi ăn với', font=hand, fill=ink, anchor='lm')
    pd.text((120, 592), 'đoàn Hà Nội ở nhà khách', font=hand, fill=ink, anchor='lm')
    pd.line(wob(bezier((200, 610), (210, 640), (225, 655), (235, 664), 8)), fill=ink, width=2)
    pd.text((860, 712), 'Nga', font=font(HAND, 30), fill=ink, anchor='mm')
    page = page.rotate(-2.5, resample=Image.BICUBIC, expand=True)
    ox, oy = (W - page.size[0]) // 2, (H - page.size[1]) // 2
    sh = page.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.55))
    im.paste((0, 0, 0), (ox + 10, oy + 14), sh)
    im.paste(page, (ox, oy), page)
    im = light_spot(im, 520, 320, 560, 0.2)
    im = vignette(im, 0.5)
    save(grain(im, 6, 0.4), 'd08-so-do-co-hoc')


# ── d11: ống bương tre cưa vát, trục xoay gỗ, nhựa mủ trắng, dây dù xanh ─────
def d11():
    random.seed(11)
    W, H = 1200, 900
    im = tint(noise((W, H), 16, 2), (64, 88, 104), (104, 132, 148))  # blue-grey evidence sheet
    d = ImageDraw.Draw(im)
    # bamboo tube lying diagonally: 40 cm ≈ 640 px
    ang = -0.22
    cx, cy = 560, 400
    def R(x, y):
        return (cx + x * math.cos(ang) - y * math.sin(ang), cy + x * math.sin(ang) + y * math.cos(ang))
    L, r = 320, 62
    body = [R(-L, -r), R(L - 60, -r), R(L + 40, r), R(-L, r)]  # slanted cut at the right end
    paste_shadow(im, soft_shadow((W, H), body, 18, (14, 20), 170))
    bm = Image.new('L', (W, H), 0)
    ImageDraw.Draw(bm).polygon(body, fill=255)
    bamboo = tint(noise((W, H), 26, 1.0), (118, 108, 58), (196, 184, 112))
    shade = Image.new('L', (W, H), 0)
    sd = ImageDraw.Draw(shade)
    for k in range(-r, r + 1):  # cylinder shading across the tube
        v = int(255 * (0.35 + 0.65 * math.cos(k / r * 1.3)))
        sd.line([R(-L, k), R(L + 40, k)], fill=max(0, v), width=2)
    bamboo = Image.composite(bamboo, Image.new('RGB', (W, H), (60, 54, 26)), shade)
    im.paste(bamboo, (0, 0), bm)
    d = ImageDraw.Draw(im)
    for x in (-210, -20, 170):  # nodes
        d.line([R(x, -r), R(x, r)], fill=(92, 80, 40), width=8)
        d.line([R(x + 6, -r + 4), R(x + 6, r - 4)], fill=(216, 204, 140), width=2)
    for k in range(-r + 10, r, 16):  # fibres
        d.line([R(-L, k), R(L - 60 + (k + r) / (2 * r) * 100, k)], fill=(150, 138, 76), width=1)
    # open slanted mouth (hollow inside) with fresh milky sap at the cut
    mouth = [R(L - 60, -r), R(L + 40, r), R(L + 20, r - 12), R(L - 62, -r + 14)]
    d.polygon(mouth, fill=(46, 40, 20))
    d.line([R(L - 60, -r), R(L + 40, r)], fill=(236, 226, 176), width=6)
    for k in range(7):
        p = R(L - 40 + k * 12, -r + 18 + k * 16)
        d.ellipse([p[0] - 6, p[1] - 4, p[0] + 6, p[1] + 10], fill=(246, 244, 232))
    # wooden pivot pin drilled through the centre (see-saw axle)
    for side in (-1, 1):
        p0, p1 = R(40, side * (r - 6)), R(40, side * (r + 52))
        d.line([p0, p1], fill=(110, 72, 40), width=16); d.line([p0, p1], fill=(160, 112, 66), width=6)
    d.ellipse([R(40, -r - 52)[0] - 10, R(40, -r - 52)[1] - 10, R(40, -r - 52)[0] + 10, R(40, -r - 52)[1] + 10], fill=(130, 88, 50))
    # green parachute cord coil
    cx2, cy2 = 900, 680
    for k in range(5):
        rr = 60 - k * 8
        d.ellipse([cx2 - rr + k * 6, cy2 - rr * 0.6, cx2 + rr + k * 6, cy2 + rr * 0.6], outline=(28, 120, 58), width=6)
        d.ellipse([cx2 - rr + k * 6, cy2 - rr * 0.6, cx2 + rr + k * 6, cy2 + rr * 0.6], outline=(70, 176, 100), width=2)
    d.line(bezier((cx2 - 60, cy2), (cx2 - 160, cy2 + 40), (cx2 - 220, cy2 - 30), (cx2 - 300, cy2 + 20), 30), fill=(28, 120, 58), width=6)
    # ruler + evidence tag
    d.rectangle([140, 760, 780, 806], fill=(240, 240, 236), outline=(40, 40, 40), width=2)
    for i in range(0, 641, 16):
        cm = i // 16
        d.line([(140 + i, 760), (140 + i, 782 if cm % 5 == 0 else 772)], fill=(20, 20, 20), width=2 if cm % 5 == 0 else 1)
        if cm % 10 == 0: d.text((140 + i, 795), str(cm), font=font(BOLD, 16), fill=(20, 20, 20), anchor='mm')
    d.rectangle([960, 90, 1150, 180], fill=(248, 244, 232), outline=(40, 40, 40), width=2)
    d.text((980, 118), 'TANG VẬT', font=font(BOLD, 22), fill=(40, 40, 40), anchor='lm')
    d.text((980, 156), 'Số: 11', font=font(SANS, 24), fill=(160, 30, 28), anchor='lm')
    im = light_spot(im, 520, 360, 560, 0.2)
    im = vignette(im, 0.45)
    save(grain(im, 7, 0.4), 'd11-ong-tre')


if __name__ == '__main__':
    for name in sys.argv[1:] or ['d01', 'd03', 'd05', 'd08', 'd11']:
        globals()[name]()
