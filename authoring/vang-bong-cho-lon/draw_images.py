"""Vẽ minh hoạ ảnh tư liệu cho hồ sơ 09 (Vàng bóng Chợ Lớn) bằng Pillow, không cần mô hình tạo ảnh.

Chạy: python3 authoring/vang-bong-cho-lon/draw_images.py [d01|d04|d05|d09|d10 ...]
Dùng chung bộ hàm vẽ của authoring/lua-than-tay-nguyen/draw_photos.py.
"""
import importlib.util
import itertools
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

OUT = 'public/cases/vang-bong-cho-lon/images/'
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL, SERIF, SERIF_B, HAND = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf', 'Times New Roman.ttf', 'Times New Roman Bold.ttf', 'Bradley Hand Bold.ttf'


def save(im, name, q=86):
    im.save(OUT + name + '.webp', 'WEBP', quality=q, method=6)
    print('ok', name, im.size)


def person(d, x, y, s, shade, cap=False):
    d.ellipse([x - 9 * s, y - 72 * s, x + 9 * s, y - 54 * s], fill=shade)
    if cap:
        d.ellipse([x - 13 * s, y - 78 * s, x + 13 * s, y - 66 * s], fill=shade - 12)
    d.polygon([(x - 15 * s, y - 52 * s), (x + 15 * s, y - 52 * s), (x + 13 * s, y - 14 * s), (x - 13 * s, y - 14 * s)], fill=shade)
    d.rectangle([x - 11 * s, y - 14 * s, x - 2 * s, y], fill=shade - 8)
    d.rectangle([x + 2 * s, y - 14 * s, x + 11 * s, y], fill=shade - 8)


# ── d01: ảnh báo đen trắng: mặt tiền tiệm kim hoàn phố Chợ Lớn sáng 18/05/1995 ─
def d01():
    random.seed(9)
    W, H = 1280, 800
    im = Image.new('L', (W, H), 180)
    d = ImageDraw.Draw(im)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=int(196 - 30 * y / H))
    # row of narrow Chợ Lớn shophouses, 3 storeys, the jewellery shop in the middle
    fronts = [(-40, 230, 150), (190, 470, 128), (470, 830, 104), (830, 1070, 136), (1070, 1320, 160)]
    for k, (x0, x1, shade) in enumerate(fronts):
        top = 70 + (k % 2) * 30
        d.rectangle([x0, top, x1, 600], fill=shade)
        d.rectangle([x0, top - 18, x1, top], fill=shade - 26)  # parapet
        for fl in range(2):  # balconies with shutters
            fy = top + 40 + fl * 150
            d.rectangle([x0 + 20, fy + 70, x1 - 20, fy + 84], fill=shade - 40)
            for j in range(4):
                wx = x0 + 30 + j * (x1 - x0 - 60) / 4
                d.rectangle([wx + 6, fy, wx + (x1 - x0 - 60) / 4 - 6, fy + 66], fill=shade - 30)
                for b in range(0, 60, 8):
                    d.line([(wx + 8, fy + 4 + b), (wx + (x1 - x0 - 60) / 4 - 8, fy + 4 + b)], fill=shade - 50, width=2)
            for b in range(x0 + 24, x1 - 20, 14):
                d.line([(b, fy + 50), (b, fy + 70)], fill=shade - 44, width=2)  # balustrade
    # jewellery shop ground floor: blank signboard, half-raised roller shutter, dark interior
    sx0, sx1 = 470, 830
    d.rectangle([sx0 + 10, 368, sx1 - 10, 420], fill=60)  # signboard (no readable text)
    d.rectangle([sx0 + 22, 378, sx1 - 22, 410], fill=84)
    d.rectangle([sx0 + 20, 430, sx1 - 20, 600], fill=28)  # dark shop interior
    for y in range(430, 520, 7):
        d.line([(sx0 + 20, y), (sx1 - 20, y)], fill=120, width=4)  # rolled-up shutter slats
    d.rectangle([sx0 + 60, 540, sx1 - 60, 600], fill=70)  # glass counter
    d.line([(sx0 + 60, 548), (sx1 - 60, 548)], fill=150, width=2)
    for x0, x1, shade in fronts:  # other shops: closed shutters
        if x0 == sx0: continue
        for y in range(440, 600, 9):
            d.line([(x0 + 14, y), (x1 - 14, y)], fill=shade - 36, width=5)
    # sidewalk + street
    d.rectangle([0, 600, W, 640], fill=150)
    d.rectangle([0, 640, W, H], fill=112)
    for k in range(-200, W, 120):
        d.line([(k, H), (k + 300, 640)], fill=104, width=1)
    # cordon, police (pith helmets), Honda Cub motorbikes, onlookers without faces
    d.line([(380, 632), (920, 632)], fill=230, width=4)
    for x in (380, 650, 920):
        d.rectangle([x - 3, 600, x + 3, 650], fill=60)
    def cub(x, y, s, shade):
        d.ellipse([x - 26 * s, y - 26 * s, x + 26 * s, y + 26 * s], outline=shade, width=int(6 * s))
        d.ellipse([x + 84 * s, y - 26 * s, x + 136 * s, y + 26 * s], outline=shade, width=int(6 * s))
        d.polygon([(x, y - 10 * s), (x + 40 * s, y - 50 * s), (x + 100 * s, y - 52 * s), (x + 110 * s, y - 10 * s), (x + 60 * s, y)], fill=shade)
        d.line([(x + 100 * s, y - 52 * s), (x + 108 * s, y - 90 * s)], fill=shade, width=int(6 * s))
        d.line([(x + 94 * s, y - 92 * s), (x + 122 * s, y - 88 * s)], fill=shade, width=int(5 * s))
    for (x, s, cap) in [(560, 1.7, True), (700, 1.75, True), (300, 1.5, False), (338, 1.45, False), (1180, 1.6, False), (1215, 1.55, False)]:
        person(d, x, 700 if cap else 690, s, 40 if cap else 58, cap)
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    im = Image.merge('RGB', (im, im, im))
    im = grain(im, 24, 0.6).convert('L')
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageOps.colorize(im, (22, 20, 18), (238, 232, 218))
    save(vignette(im, 0.35), 'd01-bao-chi')


# ── d04: sơ đồ mặt bằng tầng trệt tiệm vàng ──────────────────────────────────
def d04():
    random.seed(4)
    W, H = 1400, 1000
    im = Image.new('RGB', (W, H), (243, 240, 230))
    d = ImageDraw.Draw(im)
    for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(222, 226, 228) if x % 125 else (204, 212, 218))
    for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(222, 226, 228) if y % 125 else (204, 212, 218))
    INK, SOFT, RED, BLUE = (36, 46, 74), (110, 120, 140), (180, 34, 30), (40, 80, 150)
    d.text((60, 50), 'CÔNG AN QUẬN 5', font=font(BOLD, 22), fill=INK, anchor='lm')
    d.text((60, 78), 'Đội Cảnh sát hình sự', font=font(SANS, 20), fill=INK, anchor='lm')
    d.text((W / 2 + 80, 56), 'SƠ ĐỒ MẶT BẰNG TẦNG TRỆT TIỆM VÀNG VẠN THÀNH', font=font(BOLD, 28), fill=INK, anchor='mm')
    d.text((W / 2 + 80, 92), 'Số 62 Hải Thượng Lãn Ông, Phường 10, Quận 5 · lập 09h30 ngày 18/05/1995', font=font(ITAL, 20), fill=INK, anchor='mm')
    # building shell: narrow deep shophouse, front at the bottom (street), back at the top (alley)
    X0, X1, Y0, Y1 = 380, 1020, 170, 900
    d.rectangle([X0, Y0, X1, Y1], outline=INK, width=8)
    d.rectangle([X0 + 70, Y1 - 4, X1 - 70, Y1 + 4], fill=(243, 240, 230))  # front opening (shutter)
    for x in range(X0 + 70, X1 - 70, 18): d.line([(x, Y1 - 4), (x + 9, Y1 - 4)], fill=INK, width=3)
    d.text(((X0 + X1) / 2, Y1 + 40), 'ĐƯỜNG HẢI THƯỢNG LÃN ÔNG', font=font(BOLD, 22), fill=INK, anchor='mm')
    d.text(((X0 + X1) / 2, Y1 + 66), '(cửa cuốn mặt tiền)', font=font(ITAL, 18), fill=SOFT, anchor='mm')
    # partition between front shop and back area
    PY = 520
    d.line([(X0, PY), (X0 + 380, PY)], fill=INK, width=6)
    d.line([(X0 + 470, PY), (X1, PY)], fill=INK, width=6)
    d.arc([X0 + 380, PY - 90, X0 + 560, PY + 90], 180, 270, fill=SOFT, width=2)  # door swing
    # FRONT: display counters (U shape) + safe against the partition behind the counter
    d.rectangle([X0 + 60, 760, X1 - 60, 800], outline=INK, width=3)
    d.rectangle([X0 + 60, 600, X0 + 100, 800], outline=INK, width=3)
    d.rectangle([X1 - 100, 600, X1 - 60, 800], outline=INK, width=3)
    d.text(((X0 + X1) / 2, 780), 'QUẦY TỦ KÍNH TRƯNG BÀY VÀNG', font=font(BOLD, 18), fill=INK, anchor='mm')
    d.rectangle([X1 - 230, PY + 12, X1 - 130, PY + 92], fill=(60, 80, 70), outline=INK, width=3)  # safe
    d.ellipse([X1 - 196, PY + 36, X1 - 164, PY + 68], outline=(230, 230, 220), width=3)
    d.line([(X1 - 130, PY + 92), (X1 - 72, PY + 140)], fill=INK, width=3)  # door ajar 45°
    d.text((X1 - 180, PY + 112), 'KÉT SẮT CHUBB', font=font(BOLD, 18), fill=INK, anchor='mm')
    d.text((X1 - 180, PY + 134), '(cửa mở hé 45°)', font=font(ITAL, 16), fill=SOFT, anchor='mm')
    d.text((X0 + 250, 650), 'GIAN TRƯNG BÀY', font=font(BOLD, 22), fill=SOFT, anchor='mm')
    # BACK: owner's desk with the coffee cup, tea table, workshop, stairs, back door
    d.rectangle([X0 + 60, 380, X0 + 260, 460], outline=INK, width=3)
    d.text((X0 + 160, 420), 'BÀN LÀM VIỆC', font=font(BOLD, 17), fill=INK, anchor='mm')
    d.text((X0 + 160, 476), '(gỗ cẩm lai)', font=font(ITAL, 15), fill=SOFT, anchor='mm')
    d.ellipse([X0 + 214, 392, X0 + 238, 416], outline=RED, width=3)  # the cup
    d.ellipse([X0 + 120, 280, X0 + 200, 340], outline=INK, width=3)
    d.text((X0 + 160, 310), 'BÀN TRÀ', font=font(BOLD, 15), fill=INK, anchor='mm')
    d.rectangle([X0 + 330, 230, X1 - 40, 470], outline=INK, width=3)
    d.text(((X0 + 330 + X1 - 40) / 2, 330), 'XƯỞNG CHẾ TÁC', font=font(BOLD, 20), fill=INK, anchor='mm')
    d.text(((X0 + 330 + X1 - 40) / 2, 356), 'KIM HOÀN', font=font(BOLD, 20), fill=INK, anchor='mm')
    for k in range(3): d.rectangle([X0 + 360 + k * 90, 400, X0 + 430 + k * 90, 450], outline=SOFT, width=2)  # benches
    for k in range(9):  # stairs to floors 1 & 2
        d.line([(X0 + 20, Y0 + 20 + k * 16), (X0 + 100, Y0 + 20 + k * 16)], fill=INK, width=2)
    d.rectangle([X0 + 20, Y0 + 20, X0 + 100, Y0 + 164], outline=INK, width=2)
    d.text((X0 + 22, Y0 + 182), 'Cầu thang lên lầu 1, 2', font=font(SANS, 15), fill=INK, anchor='lm')
    d.rectangle([X1 - 220, Y0 - 4, X1 - 130, Y0 + 4], fill=(243, 240, 230))  # back door
    d.arc([X1 - 220, Y0 - 90, X1 - 40, Y0 + 90], 0, 90, fill=SOFT, width=2)
    d.text((X1 - 175, Y0 + 26), 'CỬA SAU', font=font(BOLD, 18), fill=INK, anchor='mm')
    d.text(((X0 + X1) / 2, 140), '↑ Hẻm thông ra đường Triệu Quang Phục', font=font(BOLD, 20), fill=INK, anchor='mm')
    # legend + markers
    d.ellipse([X1 - 270, PY + 40, X1 - 246, PY + 64], outline=RED, width=3); d.text((X1 - 258, PY + 52), '2', font=font(BOLD, 16), fill=RED, anchor='mm')
    d.ellipse([X0 + 272, 400, X0 + 296, 424], outline=RED, width=3); d.text((X0 + 284, 412), '1', font=font(BOLD, 16), fill=RED, anchor='mm')
    LX, LY = 1060, 200
    d.rectangle([LX, LY, LX + 300, LY + 190], outline=INK, width=2)
    d.text((LX + 16, LY + 24), 'GHI CHÚ', font=font(BOLD, 20), fill=INK, anchor='lm')
    d.ellipse([LX + 16, LY + 50, LX + 40, LY + 74], outline=RED, width=3); d.text((LX + 28, LY + 62), '1', font=font(BOLD, 15), fill=RED, anchor='mm')
    d.text((LX + 52, LY + 62), 'Vị trí nạn nhân, tách cà phê', font=font(SANS, 17), fill=INK, anchor='lm')
    d.ellipse([LX + 16, LY + 90, LX + 40, LY + 114], outline=RED, width=3); d.text((LX + 28, LY + 102), '2', font=font(BOLD, 15), fill=RED, anchor='mm')
    d.text((LX + 52, LY + 102), 'Két sắt mở hé', font=font(SANS, 17), fill=INK, anchor='lm')
    d.text((LX + 16, LY + 142), 'Cửa sau: chốt trong ở', font=font(SANS, 17), fill=INK, anchor='lm')
    d.text((LX + 16, LY + 166), 'chế độ tự do khi phát hiện', font=font(SANS, 17), fill=INK, anchor='lm')
    nx, ny = 1300, 820
    d.polygon([(nx, ny - 50), (nx - 16, ny + 10), (nx, ny), (nx + 16, ny + 10)], fill=INK); d.text((nx, ny - 70), 'N', font=font(BOLD, 24), fill=INK, anchor='mm')
    d.line([(80, 900), (280, 900)], fill=INK, width=3)
    for k in range(3): d.line([(80 + k * 100, 890), (80 + k * 100, 910)], fill=INK, width=3)
    d.text((80, 930), '0', font=font(SANS, 18), fill=INK, anchor='mm'); d.text((280, 930), '4 m', font=font(SANS, 18), fill=INK, anchor='mm')
    st = Image.new('RGBA', (210, 210), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.ellipse([8, 8, 202, 202], outline=RED + (210,), width=6); sd.ellipse([40, 40, 170, 170], outline=RED + (210,), width=3)
    sd.text((105, 92), 'CÔNG AN', font=font(BOLD, 20), fill=RED + (220,), anchor='mm'); sd.text((105, 120), 'QUẬN 5', font=font(BOLD, 20), fill=RED + (220,), anchor='mm')
    st = st.rotate(-12, resample=Image.BICUBIC)
    im.paste(st, (80, 560), st)
    im = im.filter(ImageFilter.GaussianBlur(0.35))
    save(grain(im, 5, 0.4), 'd04-so-do-tiem-vang')


# ── d05: núm xoay két Chubb phủ bột phấn, 4 vạch bị lau sạch ──────────────────
def d05():
    random.seed(5)
    W, H = 1200, 900
    door = tint(noise((W, H), 30, 1.4), (34, 58, 46), (78, 112, 92))  # dark green safe door
    im = door
    cx, cy, R = 600, 450, 330
    paste_shadow(im, soft_shadow((W, H), [(cx + R * math.cos(a), cy + R * math.sin(a)) for a in [k * math.pi / 30 for k in range(60)]], 22, (18, 22), 200))
    # nickel-plated dial with radial brushing
    dial = Image.new('L', (2 * R, 2 * R), 0)
    dd = ImageDraw.Draw(dial)
    for k in range(720):
        a = k * math.pi / 360
        v = int(150 + 70 * math.cos(a * 2 + 0.6) + random.uniform(-20, 20))
        dd.line([(R, R), (R + R * math.cos(a), R + R * math.sin(a))], fill=max(0, min(255, v)), width=3)
    dial = dial.filter(ImageFilter.GaussianBlur(1.2))
    dial = ImageOps.colorize(dial, (90, 92, 96), (238, 240, 244))
    m = Image.new('L', (2 * R, 2 * R), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
    im.paste(dial, (cx - R, cy - R), m)
    d = ImageDraw.Draw(im)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(60, 62, 66), width=6)
    # graduations 0–99 (rotating ring), numbers every 10
    def at(n, r):
        a = -math.pi / 2 + n / 100 * 2 * math.pi
        return (cx + r * math.cos(a), cy + r * math.sin(a))
    for n in range(100):
        L = 40 if n % 10 == 0 else (28 if n % 5 == 0 else 18)
        d.line([at(n, R - 14), at(n, R - 14 - L)], fill=(28, 28, 30), width=4 if n % 10 == 0 else 2)
        if n % 10 == 0:
            d.text(at(n, R - 82), str(n), font=font(BOLD, 34), fill=(24, 24, 26), anchor='mm')
    # central grip knob
    d.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], fill=(84, 86, 90), outline=(40, 40, 44), width=5)
    for k in range(36):
        a = k * math.pi / 18
        d.line([(cx + 108 * math.cos(a), cy + 108 * math.sin(a)), (cx + 120 * math.cos(a), cy + 120 * math.sin(a))], fill=(140, 142, 146), width=4)
    d.ellipse([cx - 70, cy - 70, cx + 70, cy + 70], fill=(150, 152, 156), outline=(70, 70, 74), width=3)
    # index mark on the door above the dial
    d.polygon([(cx - 16, cy - R - 34), (cx + 16, cy - R - 34), (cx, cy - R - 6)], fill=(228, 220, 180))
    # ivory-white mineral powder over the whole ring …
    powder = Image.new('L', (W, H), 0)
    ring = Image.new('L', (W, H), 0)
    ImageDraw.Draw(ring).ellipse([cx - R + 4, cy - R + 4, cx + R - 4, cy + R - 4], fill=255)
    ImageDraw.Draw(ring).ellipse([cx - 122, cy - 122, cx + 122, cy + 122], fill=0)
    powder = ImageChops.multiply(ring, noise((W, H), 70, 1.0).point(lambda v: int(max(0, min(255, (v - 40) * 1.6)))))
    # … except where a fingertip wiped the four numbers clean
    wipe = Image.new('L', (W, H), 0)
    wd = ImageDraw.Draw(wipe)
    for n in (18, 42, 65, 89):
        x, y = at(n, R - 52)
        a = math.atan2(y - cy, x - cx)
        for k in range(16):
            t = k / 15 - 0.5
            px, py = x + math.cos(a + math.pi / 2) * 30 * t, y + math.sin(a + math.pi / 2) * 30 * t
            wd.ellipse([px - 26, py - 30, px + 26, py + 30], fill=255)
    wipe = wipe.filter(ImageFilter.GaussianBlur(5))
    powder = ImageChops.subtract(powder, wipe)
    im.paste((214, 204, 180), (0, 0), ImageChops.subtract(ring, wipe).point(lambda v: int(v * 0.55)))  # dull film over the ring
    im.paste((236, 228, 208), (0, 0), powder)
    clean = ImageChops.multiply(wipe, ring)
    im.paste((250, 252, 255), (0, 0), clean.point(lambda v: int(v * 0.5)))  # polished metal shows through
    d = ImageDraw.Draw(im)
    for n in range(100):  # engraved graduations still read through the thin powder
        L = 40 if n % 10 == 0 else (28 if n % 5 == 0 else 18)
        d.line([at(n, R - 14), at(n, R - 14 - L)], fill=(40, 40, 42), width=4 if n % 10 == 0 else 2)
        if n % 10 == 0:
            d.text(at(n, R - 82), str(n), font=font(BOLD, 34), fill=(36, 36, 38), anchor='mm')
    # whorl traces at the edge of each wiped patch
    for n in (18, 42, 65, 89):
        x, y = at(n, R - 52)
        for k in range(5):
            r = 18 + k * 5
            d.arc([x - r, y - r * 1.2, x + r, y + r * 1.2], 200, 330, fill=(214, 206, 186), width=1)
    im = light_spot(im, 420, 300, 420, 0.24)  # flash from the upper left
    im = vignette(im, 0.6)
    save(grain(im, 8, 0.4), 'd05-num-ket')


# ── d09: cuống vé ca nhạc rạp Hào Huê (bản chụp) ─────────────────────────────
def d09():
    random.seed(19)
    W, H = 1200, 800
    bg = tint(noise((W, H), 20, 2), (60, 96, 120), (96, 136, 160))  # blue evidence card
    im = bg
    tw, th = 820, 380
    t = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
    td = ImageDraw.Draw(t)
    paper = tint(noise((tw, th), 18, 0.8), (214, 186, 150), (240, 222, 190))
    shape = Image.new('L', (tw, th), 0)
    sd = ImageDraw.Draw(shape)
    sd.rectangle([0, 0, tw - 1, th - 1], fill=255)
    for y in range(0, th, 14):  # torn edge on the right (stub torn at the door)
        x = tw - 1 - random.uniform(0, 22)
        sd.polygon([(x, y), (tw, y), (tw, y + 14), (x - random.uniform(0, 10), y + 14)], fill=0)
    t.paste(paper, (0, 0), shape)
    td = ImageDraw.Draw(t)
    INK, RED = (60, 36, 24), (178, 30, 28)
    td.rectangle([20, 20, tw - 60, th - 20], outline=INK, width=3)
    td.line([(560, 24), (560, th - 24)], fill=INK, width=2)
    for y in range(30, th - 30, 16): td.ellipse([556, y, 564, y + 8], fill=(214, 186, 150))  # perforation
    td.text((290, 70), 'RẠP HÀO HUÊ', font=font(SERIF_B, 46), fill=INK, anchor='mm')
    td.text((290, 112), 'Đường Trần Hưng Đạo B · Quận 5', font=font(SERIF, 20), fill=INK, anchor='mm')
    td.line([(70, 136), (510, 136)], fill=INK, width=2)
    td.text((290, 170), 'Chương trình ca nhạc tạp kỹ', font=font(SERIF, 24), fill=INK, anchor='mm')
    td.text((290, 204), 'SÀI GÒN ĐÊM TRẮNG', font=font(SERIF_B, 30), fill=INK, anchor='mm')
    td.text((70, 254), 'Đêm diễn:  17/05/1995', font=font(SERIF, 24), fill=INK, anchor='lm')
    td.text((70, 290), 'Giờ diễn:   20h30 – 23h00', font=font(SERIF, 24), fill=INK, anchor='lm')
    td.text((70, 326), 'Giá vé:      15.000 đ', font=font(SERIF, 24), fill=INK, anchor='lm')
    td.text((680, 70), 'GHẾ', font=font(SERIF_B, 26), fill=INK, anchor='mm')
    td.text((680, 130), 'D', font=font(SERIF_B, 64), fill=INK, anchor='mm')
    td.text((680, 210), '14', font=font(SERIF_B, 64), fill=INK, anchor='mm')
    td.text((680, 290), 'Số 004127', font=font(SERIF, 20), fill=INK, anchor='mm')
    stamp = Image.new('RGBA', (220, 220), (0, 0, 0, 0)); st = ImageDraw.Draw(stamp)
    st.ellipse([10, 10, 210, 210], outline=RED + (190,), width=6); st.ellipse([40, 40, 180, 180], outline=RED + (190,), width=2)
    st.text((110, 96), 'RẠP', font=font(BOLD, 22), fill=RED + (200,), anchor='mm'); st.text((110, 126), 'HÀO HUÊ', font=font(BOLD, 24), fill=RED + (200,), anchor='mm')
    stamp = stamp.rotate(18, resample=Image.BICUBIC)
    t.paste(stamp, (330, 170), stamp)
    t = t.rotate(-5, resample=Image.BICUBIC, expand=True)
    ox, oy = (W - t.size[0]) // 2, (H - t.size[1]) // 2
    sh = t.split()[3].filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.6))
    im.paste((0, 0, 0), (ox + 12, oy + 16), sh)
    im.paste(t, (ox, oy), t)
    # evidence tag in the corner
    d = ImageDraw.Draw(im)
    d.rectangle([60, 640, 330, 740], fill=(248, 244, 232), outline=(40, 40, 40), width=2)
    d.text((80, 668), 'TANG VẬT', font=font(BOLD, 22), fill=(40, 40, 40), anchor='lm')
    d.text((80, 708), 'Số: 09', font=font(SANS, 24), fill=(160, 30, 28), anchor='lm')
    im = light_spot(im, 560, 360, 520, 0.18)
    im = vignette(im, 0.45)
    save(grain(im, 7, 0.4), 'd09-cuong-ve')


# ── d10: mẩu giấy bao thuốc ghi 24 hoán vị, 11 dòng gạch đỏ, dòng 12 khoanh xanh ─
def d10():
    random.seed(10)
    W, H = 1200, 900
    im = tint(noise((W, H), 18, 2), (52, 104, 92), (86, 144, 128))  # green evidence board
    nums = [18, 42, 65, 89]
    perms = list(itertools.permutations(nums))
    target = (42, 18, 89, 65)
    perms.remove(target)
    perms.insert(11, target)  # the 12th line is the circled one
    pw, ph = 560, 840
    p = Image.new('RGBA', (pw, ph), (0, 0, 0, 0))
    shape = Image.new('L', (pw, ph), 0)
    sd = ImageDraw.Draw(shape)
    edge_l = [(random.uniform(0, 14), y) for y in range(0, ph + 1, 20)]
    edge_r = [(pw - random.uniform(0, 14), y) for y in range(ph, -1, -20)]
    sd.polygon([(14, 0)] + edge_l + [(pw - 10, ph)] + edge_r, fill=255)  # torn from a cigarette pack
    paper = tint(noise((pw, ph), 22, 0.8), (196, 168, 120), (226, 204, 160))
    p.paste(paper, (0, 0), shape)
    pd = ImageDraw.Draw(p)
    blue, red = (30, 52, 140), (196, 30, 30)
    hand = font(HAND, 30)
    for i, row in enumerate(perms):
        y = 40 + i * 33
        x = 70 + random.uniform(-4, 4)
        txt = ' - '.join(str(n) for n in row)
        pd.text((x, y), txt, font=hand, fill=blue, anchor='lm')
        if i < 11:  # crossed out in red ballpoint
            w = pd.textlength(txt, font=hand)
            pd.line([(x - 6, y + 6 + random.uniform(-3, 3)), (x + w + 8, y - 6 + random.uniform(-3, 3))], fill=red, width=3)
        if i == 11:  # heavy blue circle around line 12
            w = pd.textlength(txt, font=hand)
            for k in range(3):
                pd.ellipse([x - 22 - k, y - 26 - k, x + w + 22 + k, y + 24 + k], outline=(24, 40, 120), width=3)
    p = p.rotate(4, resample=Image.BICUBIC, expand=True)
    ox, oy = (W - p.size[0]) // 2 - 40, (H - p.size[1]) // 2
    sh = p.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.55))
    im.paste((0, 0, 0), (ox + 10, oy + 14), sh)
    im.paste(p, (ox, oy), p)
    # scale bar + evidence number on the board
    d = ImageDraw.Draw(im)
    d.rectangle([930, 760, 1150, 800], fill=(240, 240, 236), outline=(40, 40, 40), width=2)
    for k in range(0, 201, 20):
        d.line([(940 + k, 760), (940 + k, 776 if k % 100 else 786)], fill=(20, 20, 20), width=2)
    d.text((1040, 820), '0 — 5 cm', font=font(SANS, 18), fill=(236, 240, 236), anchor='mm')
    d.rectangle([930, 100, 1140, 190], fill=(248, 244, 232), outline=(40, 40, 40), width=2)
    d.text((950, 128), 'TANG VẬT', font=font(BOLD, 22), fill=(40, 40, 40), anchor='lm')
    d.text((950, 166), 'Số: 10', font=font(SANS, 24), fill=(160, 30, 28), anchor='lm')
    im = light_spot(im, 520, 380, 560, 0.2)
    im = vignette(im, 0.45)
    save(grain(im, 6, 0.4), 'd10-manh-giay')


if __name__ == '__main__':
    for name in sys.argv[1:] or ['d01', 'd04', 'd05', 'd09', 'd10']:
        globals()[name]()
