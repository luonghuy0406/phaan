"""Vẽ minh hoạ một số ảnh lẻ bằng Pillow, không cần mô hình tạo ảnh.

Chạy: python3 authoring/draw_misc_images.py [bale_d05|tuyet_d01|tuyet_d04 ...]
  bale_d05   bong-nang-hoi-an/images/d05-tranh-co.webp        (tranh lụa 'Thập mục ngưu đồ', 40 x 120 cm)
  tuyet_d01  buc-thu-dem-tuyet-trang/images/d01-bao-chi.webp  (ảnh bản tin: ngôi nhà trong tuyết, xe cảnh sát)
  tuyet_d04  buc-thu-dem-tuyet-trang/images/d04-so-do-biet-thu.webp (sơ đồ bốn tầng)
Ảnh hồ sơ có thật chỉ dựng cảnh chung chung, không mô phỏng ngôi nhà hay người thật.
"""
import importlib.util
import math
import random
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

_spec = importlib.util.spec_from_file_location('lib', Path(__file__).resolve().parent / 'lua-than-tay-nguyen' / 'draw_photos.py')
lib = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lib)
noise, tint, vignette, light_spot, soft_shadow, paste_shadow, bezier, grain = (
    lib.noise, lib.tint, lib.vignette, lib.light_spot, lib.soft_shadow, lib.paste_shadow, lib.bezier, lib.grain)

F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'


def save(im, path, q=86):
    im.save('public/cases/' + path, 'WEBP', quality=q, method=6)
    print('ok', path, im.size)


# ── Bá Lễ d05: tranh lụa treo 40 x 120 cm, viền chỉ vàng, trục gỗ mun đầu ngọc ─
def bale_d05():
    random.seed(55)
    W, H = 900, 1200
    im = tint(noise((W, H), 26, 2), (58, 30, 22), (110, 60, 42))  # red lacquered wall of the ancestral hall
    d = ImageDraw.Draw(im)
    sx0, sx1, sy0, sy1 = 250, 650, 120, 1080  # 40 x 120 cm → 400 x 960 px
    paste_shadow(im, soft_shadow((W, H), [(sx0 - 20, sy0), (sx1 + 20, sy0), (sx1 + 20, sy1), (sx0 - 20, sy1)], 20, (16, 22), 190))
    # red silk mounting (lụa điều) with gold thread borders
    d.rectangle([sx0, sy0, sx1, sy1], fill=(156, 32, 28))
    for k, col in enumerate([(214, 176, 82), (240, 210, 120)]):
        d.rectangle([sx0 + 14 + k * 4, sy0 + 40 + k * 4, sx1 - 14 - k * 4, sy1 - 40 - k * 4], outline=col, width=3)
    # aged silk painting panel
    px0, py0, px1, py1 = sx0 + 40, sy0 + 80, sx1 - 40, sy1 - 80
    silk = tint(noise((px1 - px0, py1 - py0), 18, 1.2), (198, 172, 124), (232, 212, 168))
    weave = Image.new('L', silk.size, 0)
    wd = ImageDraw.Draw(weave)
    for x in range(0, silk.size[0], 3): wd.line([(x, 0), (x, silk.size[1])], fill=40)
    silk.paste((176, 150, 104), (0, 0), weave)
    im.paste(silk, (px0, py0))
    d = ImageDraw.Draw(im)
    # ten ox-herding roundels in ink wash, two columns of five
    INK = (54, 42, 32)
    r = 62
    for i in range(10):
        col, row = i % 2, i // 2
        cx = px0 + 80 + col * 160; cy = py0 + 90 + row * 166
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
        # stage i: the ox fades from dark to white, then to empty circle (stage 8) and landscape (9, 10)
        if i < 7:
            shade = int(40 + i * 28)
            c = (shade, shade - 6, shade - 14)
            ox, oy = cx - 14, cy + 6
            d.rounded_rectangle([ox - 34, oy - 16, ox + 22, oy + 12], 12, fill=c)  # heavy body
            d.polygon([(ox + 16, oy - 14), (ox + 38, oy - 8), (ox + 40, oy + 6), (ox + 18, oy + 6)], fill=c)  # head, lowered
            d.arc([ox + 18, oy - 30, ox + 40, oy - 6], 200, 340, fill=INK, width=3)  # curved horns
            for lx in (ox - 28, ox - 18, ox + 6, ox + 14):
                d.line([(lx, oy + 10), (lx, oy + 26)], fill=c, width=6)
            d.line([(ox - 34, oy - 10), (ox - 46, oy + 12)], fill=c, width=3)  # tail
            hx = cx + 38
            d.polygon([(hx - 14, cy - 18), (hx + 14, cy - 18), (hx, cy - 34)], fill=INK)  # conical hat
            d.ellipse([hx - 6, cy - 18, hx + 6, cy - 6], fill=INK)
            d.line([(hx, cy - 6), (hx, cy + 16)], fill=INK, width=4)
            d.line([(hx, cy + 16), (hx - 6, cy + 32)], fill=INK, width=3); d.line([(hx, cy + 16), (hx + 6, cy + 32)], fill=INK, width=3)
            if i in (2, 3, 4): d.line(bezier((hx - 2, cy), (hx - 20, cy - 16), (ox + 46, cy - 10), (ox + 36, oy - 2), 12), fill=INK, width=1)  # rope
            if i in (5, 6): d.line([(hx, cy), (hx - 14, cy - 10)], fill=INK, width=2)  # flute
        elif i == 7:
            pass  # empty circle
        else:
            d.line(bezier((cx - 50, cy + 30), (cx - 20, cy - 20), (cx + 10, cy + 10), (cx + 50, cy - 30), 20), fill=INK, width=2)  # mountains
            d.line([(cx - 20, cy + 30), (cx + 40, cy + 26)], fill=INK, width=1)
    # foxing / age stains and a little gold leaf flecking
    stains = noise((W, H), 80, 18).point(lambda v: 90 if v > 168 else 0)
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle([px0, py0, px1, py1], fill=255)
    im.paste((150, 120, 76), (0, 0), ImageChops.multiply(stains, m))
    for _ in range(140):
        x, y = random.uniform(sx0 + 10, sx1 - 10), random.choice([random.uniform(sy0 + 30, sy0 + 60), random.uniform(sy1 - 60, sy1 - 30)])
        d.point((x, y), fill=(250, 220, 130))
    # ebony rollers with jade end caps
    for y in (sy0 - 6, sy1 + 6):
        d.rounded_rectangle([sx0 - 30, y - 16, sx1 + 30, y + 16], 14, fill=(26, 20, 18))
        d.line([(sx0 - 20, y - 8), (sx1 + 20, y - 8)], fill=(80, 70, 64), width=2)
        for x in (sx0 - 52, sx1 + 30):
            d.ellipse([x, y - 20, x + 22, y + 20], fill=(70, 150, 112))
            d.ellipse([x + 4, y - 14, x + 10, y - 6], fill=(170, 226, 196))
    d.line([(W / 2, 20), (sx0 - 20, sy0 - 14)], fill=(196, 160, 80), width=2)  # hanging cord
    d.line([(W / 2, 20), (sx1 + 20, sy0 - 14)], fill=(196, 160, 80), width=2)
    d.ellipse([W / 2 - 8, 12, W / 2 + 8, 28], fill=(150, 120, 60))
    im = light_spot(im, W / 2, 500, 520, 0.18)
    im = vignette(im, 0.55)
    save(grain(im, 7, 0.4), 'bong-nang-hoi-an/images/d05-tranh-co.webp')


# ── Tuyết trắng d01: khung hình bản tin TV: ngôi nhà trong tuyết, đèn xe cảnh sát ─
def tuyet_d01():
    random.seed(61)
    W, H = 1280, 720
    im = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):  # winter dusk sky
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(40 + 40 * t), int(52 + 46 * t), int(84 + 40 * t)))
    # bare trees silhouettes
    for x in (90, 260, 1100, 1220):
        d.line([(x, 560), (x + 6, 220)], fill=(30, 30, 38), width=10)
        for k in range(14):
            y = 260 + k * 18; L = random.uniform(40, 110); s = random.choice((-1, 1))
            d.line([(x + 4, y), (x + 4 + s * L, y - L * 0.6)], fill=(36, 36, 44), width=3)
    # generic large two-and-a-half storey brick house (not a likeness of any real house)
    hx0, hx1, hy0, hy1 = 330, 980, 300, 560
    d.rectangle([hx0, hy0, hx1, hy1], fill=(110, 62, 48))
    for y in range(hy0, hy1, 12):  # brick courses
        d.line([(hx0, y), (hx1, y)], fill=(96, 52, 40), width=1)
    d.polygon([(hx0 - 30, hy0), (hx0 + 120, hy0 - 150), (hx1 - 120, hy0 - 150), (hx1 + 30, hy0)], fill=(62, 58, 64))
    d.polygon([(560, hy0), (640, hy0 - 120), (720, hy0)], fill=(70, 66, 72))  # gable
    d.polygon([(hx0 - 30, hy0), (hx0 + 120, hy0 - 150), (hx1 - 120, hy0 - 150), (hx1 + 30, hy0), (hx1 + 30, hy0 + 10), (hx0 - 30, hy0 + 10)], outline=(236, 240, 246))
    snow_roof = [(hx0 - 30, hy0), (hx0 + 120, hy0 - 150), (hx1 - 120, hy0 - 150), (hx1 + 30, hy0)]
    d.line(snow_roof, fill=(236, 240, 248), width=12)
    for (wx, wy) in [(400, 340), (500, 340), (780, 340), (880, 340), (400, 450), (500, 450), (780, 450), (880, 450), (620, 210)]:
        lit = random.random() < 0.7
        d.rectangle([wx, wy, wx + 56, wy + 70], fill=(236, 196, 120) if lit else (40, 44, 56), outline=(230, 226, 214), width=3)
        d.line([(wx + 28, wy), (wx + 28, wy + 70)], fill=(230, 226, 214), width=2)
    d.rectangle([610, 470, 670, hy1], fill=(70, 40, 30), outline=(230, 226, 214), width=3)  # door
    # snow ground + yard, footpath, police car with light bar, cordon tape
    d.polygon([(0, 540), (W, 520), (W, H), (0, H)], fill=(220, 226, 236))
    snow = noise((W, H), 30, 1.2).point(lambda v: int((v - 128) * 0.4 + 128))
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon([(0, 540), (W, 520), (W, H), (0, H)], fill=255)
    im = Image.composite(ImageChops.add(im, Image.merge('RGB', (snow, snow, snow)), 1, -128), im, m)
    d = ImageDraw.Draw(im)
    d.polygon([(620, 560), (660, 560), (720, H), (560, H)], fill=(190, 196, 208))
    cx, cy = 1000, 640
    d.rounded_rectangle([cx - 150, cy - 30, cx + 150, cy + 24], 16, fill=(232, 234, 238))
    d.polygon([(cx - 90, cy - 30), (cx - 56, cy - 72), (cx + 60, cy - 72), (cx + 98, cy - 30)], fill=(232, 234, 238))
    d.polygon([(cx - 80, cy - 32), (cx - 52, cy - 66), (cx - 4, cy - 66), (cx - 4, cy - 32)], fill=(60, 72, 96))
    d.polygon([(cx + 4, cy - 32), (cx + 4, cy - 66), (cx + 56, cy - 66), (cx + 86, cy - 32)], fill=(60, 72, 96))
    d.rectangle([cx - 150, cy - 6, cx + 150, cy + 4], fill=(30, 40, 70))  # stripe
    d.rectangle([cx - 30, cy - 84, cx - 2, cy - 72], fill=(230, 40, 40)); d.rectangle([cx + 2, cy - 84, cx + 30, cy - 72], fill=(50, 100, 240))
    for x in (cx - 92, cx + 92):
        d.ellipse([x - 26, cy + 2, x + 26, cy + 52], fill=(20, 20, 24)); d.ellipse([x - 10, cy + 18, x + 10, cy + 38], fill=(120, 120, 126))
    glow = Image.new('L', (W, H), 0)
    ImageDraw.Draw(glow).ellipse([cx - 140, cy - 160, cx + 140, cy], fill=150)
    im.paste((220, 60, 60), (0, 0), glow.filter(ImageFilter.GaussianBlur(40)).point(lambda v: v // 2))
    d = ImageDraw.Draw(im)
    d.line([(120, 600), (520, 590), (820, 604)], fill=(236, 200, 40), width=5)
    # falling snow
    for _ in range(500):
        x, y = random.uniform(0, W), random.uniform(0, H); r = random.uniform(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(236, 240, 248))
    im = im.filter(ImageFilter.GaussianBlur(1.0))
    # TV scanlines + slight colour bleed
    lines = Image.new('L', (W, H), 0)
    ld = ImageDraw.Draw(lines)
    for y in range(0, H, 3): ld.line([(0, y), (W, y)], fill=40)
    im.paste((0, 0, 0), (0, 0), lines)
    im = vignette(im, 0.45)
    save(grain(im, 14, 0.6), 'buc-thu-dem-tuyet-trang/images/d01-bao-chi.webp')


# ── Tuyết trắng d04: sơ đồ biệt thự: tầng hầm, tầng 1, 2, 3 ─────────────────
def tuyet_d04():
    W, H = 1600, 1000
    im = Image.new('RGB', (W, H), (243, 241, 234))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(224, 228, 230) if x % 125 else (208, 214, 220))
    for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(224, 228, 230) if y % 125 else (208, 214, 220))
    INK, SOFT, RED = (36, 44, 70), (110, 118, 138), (178, 34, 30)
    d.text((W / 2, 46), 'SƠ ĐỒ MẶT BẰNG BIỆT THỰ BA TẦNG VÀ TẦNG HẦM', font=font(BOLD, 30), fill=INK, anchor='mm')
    d.text((W / 2, 84), 'Lập 18h00 ngày 26/12/1996 · không theo tỷ lệ', font=font(ITAL, 20), fill=INK, anchor='mm')
    panels = [('TẦNG HẦM', 40), ('TẦNG 1', 430), ('TẦNG 2', 820), ('TẦNG 3', 1210)]
    PW, PY0, PY1 = 350, 150, 880
    def room(x0, y0, x1, y1, label, sub=None, col=INK):
        d.rectangle([x0, y0, x1, y1], outline=col, width=3)
        d.text(((x0 + x1) / 2, (y0 + y1) / 2 - (10 if sub else 0)), label, font=font(BOLD, 17), fill=col, anchor='mm')
        if sub: d.text(((x0 + x1) / 2, (y0 + y1) / 2 + 14), sub, font=font(ITAL, 14), fill=SOFT, anchor='mm')
    for name, x in panels:
        d.text((x + PW / 2, PY0 - 24), name, font=font(BOLD, 22), fill=INK, anchor='mm')
        d.rectangle([x, PY0, x + PW, PY1], outline=INK, width=6)
    # stair core shared at the same spot on every floor
    def stair(x, y, spiral=False):
        if spiral:
            d.ellipse([x, y, x + 90, y + 90], outline=INK, width=2)
            for k in range(10):
                a = k * math.pi / 5
                d.line([(x + 45, y + 45), (x + 45 + 45 * math.cos(a), y + 45 + 45 * math.sin(a))], fill=SOFT, width=1)
        else:
            d.rectangle([x, y, x + 90, y + 90], outline=INK, width=2)
            for k in range(1, 9): d.line([(x, y + k * 10), (x + 90, y + k * 10)], fill=SOFT, width=1)
    # basement
    x = 40
    room(x, PY0, x + 200, PY0 + 220, 'PHÒNG GIẶT')
    room(x + 200, PY0, x + PW, PY0 + 220, 'PHÒNG', 'LÒ SƯỞI')
    room(x, PY0 + 220, x + 200, PY0 + 470, 'HẦM RƯỢU', 'nơi tìm thấy thi thể', col=RED)
    d.rectangle([x + 4, PY0 + 600, x + 24, PY0 + 680], fill=(196, 216, 236), outline=INK, width=2)  # window well
    d.text((x + 34, PY0 + 640), 'Cửa sổ tầng hầm', font=font(SANS, 15), fill=INK, anchor='lm')
    d.text((x + 34, PY0 + 660), '(giếng sáng)', font=font(ITAL, 14), fill=SOFT, anchor='lm')
    stair(x + 240, PY0 + 600)
    d.text((x + 175, PY1 - 30), 'Kho, hành lang', font=font(ITAL, 15), fill=SOFT, anchor='mm')
    # ground floor
    x = 430
    room(x, PY0, x + PW, PY0 + 260, 'PHÒNG KHÁCH')
    room(x, PY0 + 260, x + 200, PY0 + 500, 'NHÀ BẾP')
    stair(x + 240, PY0 + 330, spiral=True)
    d.text((x + 275, PY0 + 290), 'Cầu thang xoắn ốc', font=font(BOLD, 14), fill=INK, anchor='mm')
    d.text((x + 275, PY0 + 440), 'nơi thấy 3 trang', font=font(ITAL, 13), fill=RED, anchor='mm')
    d.text((x + 275, PY0 + 458), 'thư trên bậc', font=font(ITAL, 13), fill=RED, anchor='mm')
    room(x, PY0 + 500, x + PW, PY1, 'PHÒNG ĂN', 'cửa chính, sảnh')
    stair(x + 240, PY0 + 600)
    # second floor
    x = 820
    room(x, PY0, x + PW, PY0 + 260, 'PHÒNG NGỦ', 'nạn nhân')
    room(x, PY0 + 260, x + PW, PY0 + 500, 'PHÒNG NGỦ', 'anh trai (9 tuổi)')
    stair(x + 240, PY0 + 600)
    room(x, PY0 + 500, x + 200, PY1, 'PHÒNG TẮM')
    # third floor
    x = 1210
    room(x, PY0, x + PW, PY0 + 400, 'PHÒNG NGỦ', 'cha mẹ')
    room(x, PY0 + 400, x + 200, PY1, 'PHÒNG THAY ĐỒ')
    stair(x + 240, PY0 + 600)
    # legend
    d.rectangle([40, 910, 700, 970], outline=INK, width=2)
    d.rectangle([60, 930, 90, 950], outline=RED, width=3); d.text((100, 940), 'Nơi phát hiện thi thể', font=font(SANS, 16), fill=INK, anchor='lm')
    d.rectangle([330, 924, 350, 956], fill=(196, 216, 236), outline=INK, width=2); d.text((360, 940), 'Cửa sổ tầng hầm', font=font(SANS, 16), fill=INK, anchor='lm')
    d.rectangle([520, 925, 550, 955], outline=INK, width=2); d.text((560, 940), 'Cầu thang', font=font(SANS, 16), fill=INK, anchor='lm')
    im = im.filter(ImageFilter.GaussianBlur(0.35))
    save(grain(im, 5, 0.4), 'buc-thu-dem-tuyet-trang/images/d04-so-do-biet-thu.webp')


# ── Bá Lễ d04: sơ đồ từ đường họ Lương và ngõ gạch thẻ 80 m ra giếng Bá Lễ ──────
def bale_d04():
    random.seed(44)
    W, H = 1400, 1050
    im = Image.new('RGB', (W, H), (243, 240, 228))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(224, 226, 224) if x % 125 else (206, 212, 212))
    for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(224, 226, 224) if y % 125 else (206, 212, 212))
    INK, SOFT, RED, GREEN, BRICK = (40, 48, 76), (112, 120, 140), (178, 34, 30), (72, 112, 70), (170, 92, 60)
    d.text((60, 46), 'CÔNG AN THỊ XÃ HỘI AN', font=font(BOLD, 22), fill=INK, anchor='lm')
    d.text((60, 74), 'Đội Cảnh sát điều tra', font=font(SANS, 20), fill=INK, anchor='lm')
    d.text((W / 2 + 90, 52), 'SƠ ĐỒ KHU VỰC HIỆN TRƯỜNG', font=font(BOLD, 32), fill=INK, anchor='mm')
    d.text((W / 2 + 90, 90), 'Từ đường họ Lương, số 48 Trần Phú · lập 15h00 ngày 19/08/2005', font=font(ITAL, 20), fill=INK, anchor='mm')
    # Trần Phú street along the bottom
    d.rectangle([0, 900, W, 990], fill=(222, 220, 212))
    d.line([(0, 900), (W, 900)], fill=INK, width=3)
    d.text((W / 2, 948), 'ĐƯỜNG TRẦN PHÚ', font=font(BOLD, 24), fill=INK, anchor='mm')
    # neighbouring tube houses on both sides
    for x0, x1 in ((80, 300), (760, 980), (980, 1200)):
        d.rectangle([x0, 620, x1, 900], outline=SOFT, width=2)
        d.text(((x0 + x1) / 2, 760), 'nhà dân', font=font(ITAL, 17), fill=SOFT, anchor='mm')
    # the ancestral house (deep tube house): front hall at the street, main hall, back courtyard
    X0, X1, Y0, Y1 = 320, 740, 520, 900
    d.rectangle([X0, Y0, X1, Y1], outline=INK, width=7)
    d.rectangle([X0 + 120, Y1 - 4, X1 - 120, Y1 + 4], fill=(243, 240, 228))
    for x in range(X0 + 120, X1 - 120, 16): d.line([(x, Y1 - 4), (x + 8, Y1 - 4)], fill=INK, width=3)
    d.text(((X0 + X1) / 2, Y1 - 30), 'Cửa chính (khoá chốt)', font=font(SANS, 16), fill=INK, anchor='mm')
    d.line([(X0, 720), (X1, 720)], fill=INK, width=4)
    d.text(((X0 + X1) / 2, 800), 'GIAN TIỀN SẢNH', font=font(BOLD, 20), fill=SOFT, anchor='mm')
    d.text(((X0 + X1) / 2, 640), 'GIAN CHÍNH', font=font(BOLD, 22), fill=INK, anchor='mm')
    d.rectangle([X0 + 150, 544, X1 - 150, 570], outline=INK, width=2)  # altar
    d.text(((X0 + X1) / 2, 557), 'bàn thờ', font=font(SANS, 14), fill=INK, anchor='mm')
    # where the painting hung (two empty brass hooks) on the side wall of the main hall
    d.line([(X0 + 6, 590), (X0 + 6, 690)], fill=RED, width=6)
    d.ellipse([X0 + 16, 588, X0 + 40, 612], outline=RED, width=3); d.text((X0 + 28, 600), '1', font=font(BOLD, 15), fill=RED, anchor='mm')
    # back side door (cửa nách) leading out to the lane
    d.rectangle([X1 - 110, Y0 - 4, X1 - 50, Y0 + 4], fill=(243, 240, 228))
    d.arc([X1 - 170, Y0 - 60, X1 - 50, Y0 + 60], 270, 330, fill=SOFT, width=2)
    d.ellipse([X1 - 96, Y0 + 14, X1 - 72, Y0 + 38], outline=RED, width=3); d.text((X1 - 84, Y0 + 26), '2', font=font(BOLD, 15), fill=RED, anchor='mm')
    d.text((X1 - 40, Y0 - 24), 'Cửa nách phía sau', font=font(BOLD, 16), fill=INK, anchor='lm')
    # brick lane (gạch thẻ) ~80 m to the well
    lane = [(X1 - 80, Y0 - 4), (X1 - 80, 400), (1060, 400), (1060, 350)]
    for a, b in zip(lane, lane[1:]):
        d.line([a, b], fill=(214, 196, 176), width=34)
    for a, b in zip(lane, lane[1:]):
        L = int(math.dist(a, b) // 14)
        for k in range(L):
            t = k / L
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            if a[0] == b[0]: d.line([(x - 15, y), (x + 15, y)], fill=BRICK, width=1)
            else: d.line([(x, y - 15), (x, y + 15)], fill=BRICK, width=1)
    for (x0, x1, y) in ((X1 - 120, X1 - 98, 320), (X1 - 60, 1040, 280), (X1 - 60, 1040, 320)):
        pass
    d.line([(X1 - 100, 420), (X1 - 100, Y0 - 10)], fill=SOFT, width=2)  # lane walls
    d.line([(X1 - 60, 420), (X1 - 60, Y0 - 10)], fill=SOFT, width=2)
    d.line([(X1 - 60, 420), (1080, 420)], fill=SOFT, width=2); d.line([(X1 - 100, 380), (1040, 380)], fill=SOFT, width=2)
    d.text((880, 446), 'Ngõ hẹp lát gạch thẻ · dài khoảng 80 m', font=font(BOLD, 18), fill=BRICK, anchor='mm')
    # Bá Lễ well: square stone curb inside a low wall, shade trees around
    gx, gy = 1060, 290
    d.rectangle([gx - 120, gy - 110, gx + 120, gy + 50], outline=INK, width=3)
    d.text((gx + 132, gy - 100), 'tường rào thấp', font=font(ITAL, 15), fill=SOFT, anchor='lm')
    d.rectangle([gx - 34, gy - 64, gx + 34, gy + 4], outline=INK, width=4, fill=(206, 222, 236))
    d.rectangle([gx - 22, gy - 52, gx + 22, gy - 8], fill=(120, 160, 200))
    d.text((gx, gy + 28), 'GIẾNG BÁ LỄ', font=font(BOLD, 20), fill=INK, anchor='mm')
    for (tx, ty) in ((gx - 160, gy - 90), (gx - 170, gy - 20), (gx + 160, gy - 40), (gx + 150, gy + 30), (gx - 60, gy - 140), (gx + 60, gy - 140)):
        d.ellipse([tx - 28, ty - 28, tx + 28, ty + 28], outline=GREEN, width=2)
        d.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=GREEN)
    d.text((gx - 230, gy - 110), 'lùm cây', font=font(ITAL, 15), fill=GREEN, anchor='mm')
    # legend, north, stamp
    LX, LY = 60, 180
    d.rectangle([LX, LY, LX + 360, LY + 150], outline=INK, width=2, fill=(243, 240, 228))
    d.text((LX + 16, LY + 24), 'GHI CHÚ', font=font(BOLD, 18), fill=INK, anchor='lm')
    d.ellipse([LX + 16, LY + 50, LX + 40, LY + 74], outline=RED, width=3); d.text((LX + 28, LY + 62), '1', font=font(BOLD, 15), fill=RED, anchor='mm')
    d.text((LX + 52, LY + 62), 'Vị trí treo tranh (2 móc đồng)', font=font(SANS, 16), fill=INK, anchor='lm')
    d.ellipse([LX + 16, LY + 88, LX + 40, LY + 112], outline=RED, width=3); d.text((LX + 28, LY + 100), '2', font=font(BOLD, 15), fill=RED, anchor='mm')
    d.text((LX + 52, LY + 100), 'Cửa nách sau, khép hờ', font=font(SANS, 16), fill=INK, anchor='lm')
    d.line([(LX + 16, LY + 132), (LX + 40, LY + 132)], fill=(214, 196, 176), width=10); d.text((LX + 52, LY + 132), 'Ngõ gạch thẻ', font=font(SANS, 16), fill=INK, anchor='lm')
    nx, ny = 1320, 560
    d.polygon([(nx, ny - 50), (nx - 16, ny + 10), (nx, ny), (nx + 16, ny + 10)], fill=INK); d.text((nx, ny - 70), 'N', font=font(BOLD, 24), fill=INK, anchor='mm')
    st = Image.new('RGBA', (200, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.ellipse([8, 8, 192, 192], outline=RED + (210,), width=6); sd.ellipse([38, 38, 162, 162], outline=RED + (210,), width=3)
    sd.text((100, 88), 'CÔNG AN', font=font(BOLD, 20), fill=RED + (220,), anchor='mm'); sd.text((100, 116), 'HỘI AN', font=font(BOLD, 20), fill=RED + (220,), anchor='mm')
    st = st.rotate(-10, resample=Image.BICUBIC)
    im.paste(st, (110, 390), st)
    im = im.filter(ImageFilter.GaussianBlur(0.35))
    save(grain(im, 5, 0.4), 'bong-nang-hoi-an/images/d04-so-do-tu-duong.webp')


if __name__ == '__main__':
    for name in sys.argv[1:] or ['bale_d05', 'tuyet_d01', 'tuyet_d04']:
        globals()[name]()
