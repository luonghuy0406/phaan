"""Vẽ minh hoạ ảnh tư liệu cho hồ sơ 10 (Tiếng hú cảng Vân Đồn) bằng Pillow, không cần mô hình tạo ảnh.

Chạy: python3 authoring/tieng-huan-van-don/draw_images.py [d01|d03|d04|d05|d11 ...]
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

OUT = 'public/cases/tieng-huan-van-don/images/'
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL, SERIF, SERIF_B = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf', 'Times New Roman.ttf', 'Times New Roman Bold.ttf'


def save(im, name, q=86):
    im.save(OUT + name + '.webp', 'WEBP', quality=q, method=6)
    print('ok', name, im.size)


# ── d01: ảnh báo đen trắng: tàu cá cập cảng Cái Rồng lúc rạng sáng ──────────
def d01():
    random.seed(10)
    W, H = 1280, 800
    hz = 430
    im = Image.new('L', (W, H), 200)
    d = ImageDraw.Draw(im)
    for y in range(hz):
        d.line([(0, y), (W, y)], fill=int(214 - 26 * y / hz))
    # limestone karsts of Bái Tử Long, layered in mist
    for layer, (shade, base_h, n) in enumerate([(178, 170, 7), (150, 120, 6)]):
        x = -60
        while x < W + 60:
            w = random.uniform(70, 150); h = random.uniform(base_h * 0.9, base_h * 1.6)
            pts = bezier((x, hz), (x + w * 0.02, hz - h * 0.7), (x + w * 0.15, hz - h * 1.05), (x + w * 0.45, hz - h), 20)
            pts += bezier((x + w * 0.45, hz - h), (x + w * 0.8, hz - h * 0.98), (x + w * 0.98, hz - h * 0.75), (x + w, hz), 20)
            d.polygon(pts, fill=shade + random.randint(-6, 6))
            x += w * random.uniform(0.6, 0.95)
    mist = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mist).rectangle([0, hz - 90, W, hz + 10], fill=170)
    im = Image.composite(Image.new('L', (W, H), 206), im, mist.filter(ImageFilter.GaussianBlur(30)))
    d = ImageDraw.Draw(im)
    # sea with soft ripples
    for y in range(hz, H):
        d.line([(0, y), (W, y)], fill=int(150 - 40 * (y - hz) / (H - hz)))
    for _ in range(420):
        y = random.uniform(hz + 4, H); x = random.uniform(0, W); L = random.uniform(10, 50) * (1 + (y - hz) / 300)
        d.line([(x, y), (x + L, y)], fill=int(random.uniform(150, 190)), width=1)

    # trawler, side view, moored to the right
    bx, wl = 330, 560  # bow x, waterline
    hull = bezier((bx, wl - 120), (bx + 60, wl - 30), (bx + 140, wl + 30), (bx + 300, wl + 32), 24) + [(bx + 760, wl + 32), (bx + 800, wl - 20), (bx + 810, wl - 100)]
    d.polygon(hull, fill=64)
    d.line([(bx + 10, wl - 112), (bx + 810, wl - 104)], fill=40, width=8)  # gunwale
    d.line([(bx + 40, wl - 70), (bx + 800, wl - 64)], fill=150, width=10)  # painted stripe (orange in colour)
    d.polygon([(bx + 520, wl - 112), (bx + 520, wl - 250), (bx + 720, wl - 250), (bx + 740, wl - 104)], fill=92)  # wheelhouse
    for k in range(3):
        d.rectangle([bx + 540 + k * 60, wl - 230, bx + 585 + k * 60, wl - 195], fill=168)
    d.line([(bx + 600, wl - 250), (bx + 600, wl - 420)], fill=40, width=6)  # mast
    d.line([(bx + 600, wl - 380), (bx + 200, wl - 120)], fill=60, width=2)  # stay
    d.line([(bx + 600, wl - 380), (bx + 800, wl - 110)], fill=60, width=2)
    d.polygon([(bx + 604, wl - 418), (bx + 650, wl - 404), (bx + 604, wl - 390)], fill=60)  # flag
    for k in range(4):  # hatch covers on deck
        d.rectangle([bx + 170 + k * 80, wl - 126, bx + 230 + k * 80, wl - 112], fill=48)
    # reflection of the hull
    refl = im.crop((bx, wl - 130, bx + 820, wl + 34)).transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(3))
    m = Image.new('L', refl.size, 0)
    for y in range(refl.size[1]):
        ImageDraw.Draw(m).line([(0, y), (refl.size[0], y)], fill=int(120 * (1 - y / refl.size[1])))
    im.paste(refl, (bx, wl + 34), m)
    d = ImageDraw.Draw(im)

    # wooden wharf in the foreground with border guards / police (no faces)
    d.polygon([(0, 700), (W, 672), (W, H), (0, H)], fill=96)
    for k in range(0, W, 46):
        d.line([(k, 690 - k * 0.031), (k + 30, H)], fill=78, width=2)
    for x in (120, 420, 760, 1100):
        d.rectangle([x, 660 - x * 0.022, x + 14, 712 - x * 0.022], fill=56)
    d.line([(bx + 790, wl - 90), (1114, 666)], fill=40, width=3)  # mooring line
    def person(x, y, s, shade, cap=False):
        d.ellipse([x - 9 * s, y - 72 * s, x + 9 * s, y - 54 * s], fill=shade)
        if cap:
            d.ellipse([x - 13 * s, y - 78 * s, x + 13 * s, y - 66 * s], fill=shade - 12)
        d.polygon([(x - 15 * s, y - 52 * s), (x + 15 * s, y - 52 * s), (x + 13 * s, y - 14 * s), (x - 13 * s, y - 14 * s)], fill=shade)
        d.rectangle([x - 11 * s, y - 14 * s, x - 2 * s, y], fill=shade - 8)
        d.rectangle([x + 2 * s, y - 14 * s, x + 11 * s, y], fill=shade - 8)
    for (x, s, cap) in [(860, 1.6, True), (930, 1.55, True), (1180, 1.7, True), (220, 1.4, False), (262, 1.35, False)]:
        person(x, 770 - x * 0.022, s, 44 if cap else 60, cap)
    im = im.filter(ImageFilter.GaussianBlur(0.8))
    im = Image.merge('RGB', (im, im, im))
    im = grain(im, 24, 0.6).convert('L')
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageOps.colorize(im, (22, 20, 18), (238, 232, 218))
    save(vignette(im, 0.35), 'd01-bao-chi')


# ── d03: sơ đồ pháp y (bản vẽ nét): 4 vết phỏng lạnh Ø 20 mm ────────────────
def d03():
    random.seed(3)
    W, H = 1400, 1050
    paper = tint(noise((W, H), 14, 1.2), (226, 214, 188), (246, 238, 218))
    im = paper; d = ImageDraw.Draw(im)
    INK, RED = (52, 46, 40), (178, 34, 30)
    d.text((W / 2, 52), 'SƠ ĐỒ GIÁM ĐỊNH PHÁP Y', font=font(SERIF_B, 40), fill=INK, anchor='mm')
    d.text((W / 2, 96), 'Tử thi: Trần Văn Đạt, 50 tuổi · Tàu QN-9288-TS, khoang lạnh số 3', font=font(SERIF, 24), fill=INK, anchor='mm')
    d.line([(60, 124), (W - 60, 124)], fill=INK, width=2)
    # torso outline (front view), line art with hatching
    cx = 470
    OY = 110
    def P(x, y): return (cx + x, y + OY)
    body = bezier(P(-60, 170), P(-62, 230), P(-90, 250), P(-200, 290)) + bezier(P(-200, 290), P(-260, 320), P(-270, 420), P(-262, 560)) \
        + bezier(P(-262, 560), P(-250, 700), P(-200, 820), P(-180, 960)) + [P(180, 960)] + bezier(P(180, 960), P(200, 820), P(250, 700), P(262, 560)) \
        + bezier(P(262, 560), P(270, 420), P(260, 320), P(200, 290)) + bezier(P(200, 290), P(90, 250), P(62, 230), P(60, 170))
    d.line(body, fill=INK, width=3)
    d.ellipse([cx - 78, 60 + OY, cx + 78, 210 + OY], outline=INK, width=3)  # head outline only, no facial detail
    d.line(bezier(P(-40, 180), P(-30, 200), P(30, 200), P(40, 180)), fill=INK, width=2)  # jaw line hint
    for side in (-1, 1):  # clavicles, pectoral and rib hints
        d.line(bezier(P(side * 20, 300), P(side * 80, 286), P(side * 150, 296), P(side * 205, 300)), fill=INK, width=2)
        d.arc([cx + (side * 40 if side > 0 else -230), 330, cx + (230 if side > 0 else -40), 470], 0 if side > 0 else 0, 180, fill=INK, width=2)
        for k in range(4):
            d.arc([cx + (side * 60 if side > 0 else -240), 470 + k * 50, cx + (240 if side > 0 else -60), 560 + k * 50], 200 if side < 0 else -20, 340 if side < 0 else 160, fill=(120, 110, 96), width=1)
    d.line([P(0, 300), P(0, 700)], fill=(120, 110, 96), width=1)
    for k in range(0, 60):  # shoulder hatching
        y = 300 + k * 6
        d.line([P(-262 + (k % 3) * 2, y), P(-240, y - 10)], fill=(150, 140, 124), width=1)
    # the four 20 mm frostbite marks: right clavicle / upper chest (patient's right = viewer's left)
    marks = [P(-130, 318), P(-96, 334), P(-150, 356), P(-112, 372)]
    for (x, y) in marks:
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=(246, 244, 240), outline=RED, width=3)
    d.line([P(-150, 330), (150, 262)], fill=RED, width=2)
    d.text((30, 180), 'Vùng xương quai xanh phải:', font=font(SERIF_B, 24), fill=RED, anchor='lm')
    d.text((30, 212), '4 vết phỏng lạnh tròn Ø 20 mm,', font=font(SERIF, 24), fill=RED, anchor='lm')
    d.text((30, 244), 'hoại tử trắng tái', font=font(SERIF, 24), fill=RED, anchor='lm')
    # detail inset of one mark
    ix, iy = 960, 820
    d.ellipse([ix - 90, iy - 90, ix + 90, iy + 90], outline=INK, width=2)
    d.ellipse([ix - 46, iy - 46, ix + 46, iy + 46], fill=(242, 240, 236), outline=RED, width=3)
    for k in range(12):
        a = k * math.pi / 6
        d.line([(ix + 46 * math.cos(a), iy + 46 * math.sin(a)), (ix + 58 * math.cos(a), iy + 58 * math.sin(a))], fill=(196, 120, 110), width=2)
    d.line([(ix - 46, iy + 70), (ix + 46, iy + 70)], fill=INK, width=2)
    for x in (ix - 46, ix + 46): d.line([(x, iy + 62), (x, iy + 78)], fill=INK, width=2)
    d.text((ix, iy + 94), '20 mm', font=font(SERIF_B, 22), fill=INK, anchor='mm')
    d.line([(ix + 64, iy - 64), marks[0]], fill=(130, 120, 104), width=1)
    # conclusion box
    bx0, by0, bx1, by1 = 860, 170, 1340, 640
    d.rectangle([bx0, by0, bx1, by1], outline=INK, width=2)
    d.text((bx0 + 24, by0 + 36), 'KẾT LUẬN', font=font(SERIF_B, 30), fill=INK, anchor='lm')
    d.line([(bx0 + 24, by0 + 60), (bx0 + 200, by0 + 60)], fill=INK, width=2)
    lines = [('–', 'Nguyên nhân tử vong: ngạt cấp'), ('', 'trong môi trường bão hòa khí'), ('', 'CO2, thiếu hụt oxy nặng, kèm'), ('', 'hạ thân nhiệt cấp.'),
             ('–', 'Niêm mạc hô hấp sung huyết,'), ('', 'không có dị vật đường thở.'), ('–', 'Thời gian tử vong ước tính:'), ('', '01h00 – 02h00 ngày 14/11/2006.')]
    for k, (b, t) in enumerate(lines):
        y = by0 + 100 + k * 40
        if b: d.text((bx0 + 24, y), b, font=font(SERIF, 24), fill=INK, anchor='lm')
        d.text((bx0 + 50, y), t, font=font(SERIF, 24), fill=INK, anchor='lm')
    # stamp + signature
    st = Image.new('RGBA', (240, 240), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.ellipse([10, 10, 230, 230], outline=RED + (200,), width=6); sd.ellipse([44, 44, 196, 196], outline=RED + (200,), width=3)
    sd.text((120, 104), 'PHÒNG KỸ THUẬT', font=font(BOLD, 18), fill=RED + (210,), anchor='mm')
    sd.text((120, 132), 'HÌNH SỰ', font=font(BOLD, 22), fill=RED + (210,), anchor='mm')
    sd.text((120, 162), 'QUẢNG NINH', font=font(BOLD, 16), fill=RED + (210,), anchor='mm')
    st = st.rotate(12, resample=Image.BICUBIC)
    im.paste(st, (1110, 790), st)
    d = ImageDraw.Draw(im)
    d.text((1230, 690), 'Giám định viên', font=font(SERIF_B, 24), fill=INK, anchor='mm')
    d.line(bezier((1150, 770), (1180, 720), (1200, 800), (1230, 750)) + bezier((1230, 750), (1260, 720), (1280, 790), (1320, 740)), fill=(44, 72, 120), width=3)
    im = vignette(im.filter(ImageFilter.GaussianBlur(0.4)), 0.3)
    save(grain(im, 6, 0.4), 'd03-giai-phau')


# ── d04: sơ đồ mặt cắt tàu cá (blueprint) ───────────────────────────────────
def d04():
    W, H = 1400, 1000
    im = Image.new('RGB', (W, H), (20, 52, 96)); d = ImageDraw.Draw(im)
    for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(34, 70, 120) if x % 125 else (46, 88, 142))
    for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(34, 70, 120) if y % 125 else (46, 88, 142))
    L, WH, YEL, RED = (226, 236, 248), (200, 216, 236), (238, 200, 64), (226, 64, 52)
    d.text((60, 60), 'TÀU CÁ QN-9288-TS', font=font(BOLD, 36), fill=L, anchor='lm')
    d.text((60, 102), 'Sơ đồ mặt cắt dọc · hệ thống hầm bảo quản lạnh', font=font(SANS, 24), fill=WH, anchor='lm')
    # hull section
    deck_y, keel_y = 430, 760
    bow, stern = 160, 1240
    hull = bezier((bow, deck_y - 60), (bow + 60, keel_y - 40), (bow + 220, keel_y), (bow + 380, keel_y), 30) + [(stern - 80, keel_y), (stern, keel_y - 120), (stern + 10, deck_y)]
    d.line(hull, fill=L, width=4)
    d.line([(bow + 40, deck_y), (stern + 10, deck_y)], fill=L, width=4)  # main deck
    d.line([(bow, deck_y - 60), (bow + 40, deck_y)], fill=L, width=4)  # bow sheer
    d.line([(bow + 60, deck_y + 160), (stern - 20, deck_y + 160)], fill=WH, width=2)  # hold floor / engine room ceiling
    # 4 refrigerated holds on the main deck level
    hx0, hw = 300, 150
    for k in range(4):
        x = hx0 + k * (hw + 20)
        col = RED if k == 2 else WH
        d.rectangle([x, deck_y + 8, x + hw, deck_y + 150], outline=col, width=4 if k == 2 else 2)
        for j in range(4): d.line([(x + 6, deck_y + 30 + j * 30), (x + hw - 6, deck_y + 30 + j * 30)], fill=(60, 100, 150), width=1)
        d.rectangle([x + 30, deck_y - 14, x + hw - 30, deck_y], fill=col)  # hatch lid
        d.text((x + hw / 2, deck_y + 80), f'KHOANG {k + 1}', font=font(BOLD, 22), fill=col, anchor='mm')
    k3 = hx0 + 2 * (hw + 20)
    d.text((k3 + hw / 2, deck_y + 112), '(nơi phát hiện', font=font(SANS, 17), fill=RED, anchor='mm')
    d.text((k3 + hw / 2, deck_y + 132), 'nạn nhân)', font=font(SANS, 17), fill=RED, anchor='mm')
    # exhaust fan duct beside hold 3 rising to a funnel mouth on deck
    fx = k3 + hw + 8
    d.line([(fx, deck_y + 140), (fx, deck_y - 70)], fill=YEL, width=6)
    d.polygon([(fx - 22, deck_y - 70), (fx + 22, deck_y - 70), (fx + 12, deck_y - 50), (fx - 12, deck_y - 50)], outline=YEL, fill=None)
    d.ellipse([fx - 12, deck_y + 60, fx + 12, deck_y + 84], outline=YEL, width=3)  # fan
    d.line([(fx - 26, deck_y - 66), (620, deck_y - 150)], fill=YEL, width=2)
    d.text((614, deck_y - 176), 'Ống quạt hút khí xả', font=font(BOLD, 22), fill=YEL, anchor='rm')
    d.text((614, deck_y - 148), 'lên miệng phễu trên boong', font=font(SANS, 20), fill=YEL, anchor='rm')
    # wheelhouse (top level), crew cabin aft, engine room below
    d.rectangle([980, deck_y - 230, 1180, deck_y - 6], outline=L, width=3)
    d.line([(960, deck_y - 230), (1200, deck_y - 230)], fill=L, width=4)
    for k in range(3): d.rectangle([1000 + k * 60, deck_y - 200, 1040 + k * 60, deck_y - 160], outline=WH, width=2)
    d.text((1080, deck_y - 110), 'CABIN LÁI', font=font(BOLD, 22), fill=L, anchor='mm')
    d.text((1080, deck_y - 82), 'bánh lái · la bàn', font=font(SANS, 17), fill=WH, anchor='mm')
    d.text((1080, deck_y - 60), 'đài ICOM', font=font(SANS, 17), fill=WH, anchor='mm')
    d.line([(1080, deck_y - 230), (1080, deck_y - 330)], fill=L, width=3)  # mast
    d.rectangle([1000, deck_y + 8, 1180, deck_y + 150], outline=WH, width=2)
    d.text((1090, deck_y + 64), 'CABIN NGHỈ', font=font(BOLD, 20), fill=WH, anchor='mm')
    d.text((1090, deck_y + 92), 'thủy thủ đoàn', font=font(SANS, 17), fill=WH, anchor='mm')
    d.rectangle([420, deck_y + 176, 980, keel_y - 24], outline=WH, width=2)
    d.rectangle([460, deck_y + 210, 640, keel_y - 50], outline=L, width=2); d.text((550, deck_y + 244), 'ĐỘNG CƠ', font=font(BOLD, 20), fill=L, anchor='mm'); d.text((550, deck_y + 270), 'diesel chính', font=font(SANS, 17), fill=WH, anchor='mm')
    d.rectangle([700, deck_y + 210, 940, keel_y - 50], outline=L, width=2); d.text((820, deck_y + 244), 'DÀN MÁY NÉN', font=font(BOLD, 20), fill=L, anchor='mm'); d.text((820, deck_y + 270), 'lạnh', font=font(SANS, 17), fill=WH, anchor='mm')
    d.text((700, keel_y - 38), 'TẦNG HẦM MÁY', font=font(BOLD, 20), fill=WH, anchor='mm')
    d.text((160, deck_y - 96), 'MŨI', font=font(BOLD, 22), fill=WH, anchor='mm'); d.text((1280, deck_y - 30), 'ĐUÔI', font=font(BOLD, 22), fill=WH, anchor='mm')
    # waterline + scale
    d.line([(100, 640), (1320, 640)], fill=(90, 150, 210), width=2)
    d.text((1320, 624), 'mớn nước', font=font(ITAL, 18), fill=(120, 170, 220), anchor='rm')
    d.line([(60, 900), (360, 900)], fill=L, width=3)
    for k in range(4): d.line([(60 + k * 100, 890), (60 + k * 100, 910)], fill=L, width=3)
    d.text((60, 930), '0', font=font(SANS, 18), fill=L, anchor='mm'); d.text((360, 930), '6 m', font=font(SANS, 18), fill=L, anchor='mm')
    # legend
    d.rectangle([900, 840, 1340, 960], outline=WH, width=2)
    d.rectangle([920, 862, 960, 882], outline=RED, width=3); d.text((975, 872), 'Khoang lạnh số 3', font=font(SANS, 20), fill=L, anchor='lm')
    d.line([(920, 912), (960, 912)], fill=YEL, width=6); d.text((975, 912), 'Đường ống quạt hút khí xả', font=font(SANS, 20), fill=L, anchor='lm')
    # stamp
    st = Image.new('RGBA', (200, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
    sd.ellipse([8, 8, 192, 192], outline=RED + (220,), width=5); sd.ellipse([38, 38, 162, 162], outline=RED + (220,), width=2)
    sd.text((100, 88), 'CÔNG AN', font=font(BOLD, 20), fill=RED + (230,), anchor='mm'); sd.text((100, 116), 'VÂN ĐỒN', font=font(BOLD, 20), fill=RED + (230,), anchor='mm')
    st = st.rotate(-10, resample=Image.BICUBIC)
    im.paste(st, (1170, 40), st)
    im = im.filter(ImageFilter.GaussianBlur(0.35))
    save(grain(im, 6, 0.4), 'd04-so-do-tau-ca')


# ── d05: nắp khoang lạnh số 3, then sắt xỏ ngang, vệt dầu in vân găng tay ────
def d05():
    random.seed(5)
    W, H = 1200, 900
    # wet wooden deck boards
    wood = tint(noise((W, H // 6), 46, 0).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.5)), (52, 38, 26), (128, 98, 66))
    d = ImageDraw.Draw(wood)
    for y in range(0, H, 90):
        d.line([(0, y), (W, y)], fill=(30, 22, 16), width=4)
        for _ in range(8):
            yy = y + random.uniform(10, 80)
            d.line(bezier((0, yy), (400, yy + random.uniform(-6, 6)), (800, yy + random.uniform(-6, 6)), (W, yy)), fill=(70, 52, 36), width=1)
    wet = noise((W, H), 70, 12).point(lambda v: 90 if v > 160 else 0)
    im = Image.composite(Image.new('RGB', (W, H), (176, 170, 160)), wood, wet.filter(ImageFilter.GaussianBlur(3)))
    # hatch lid: thick timber frame clad with rusty zinc sheet
    lx0, ly0, lx1, ly1 = 170, 130, 1030, 780
    paste_shadow(im, soft_shadow((W, H), [(lx0, ly0), (lx1, ly0), (lx1, ly1), (lx0, ly1)], 18, (14, 18), 170))
    zinc = tint(noise((W, H), 40, 1.2), (98, 104, 108), (176, 182, 186))
    rust = noise((W, H), 80, 9).point(lambda v: int(max(0, (v - 140) * 4)))
    zinc = Image.composite(tint(noise((W, H), 40, 1), (96, 52, 26), (170, 98, 52)), zinc, rust)
    lid = Image.new('L', (W, H), 0)
    ImageDraw.Draw(lid).rectangle([lx0 + 30, ly0 + 30, lx1 - 30, ly1 - 30], fill=255)
    frame = Image.new('L', (W, H), 0)
    ImageDraw.Draw(frame).rectangle([lx0, ly0, lx1, ly1], fill=255)
    timber = tint(noise((W, H), 40, 1.0), (60, 36, 18), (122, 80, 44))
    im.paste(timber, (0, 0), frame)
    im.paste(zinc, (0, 0), lid)
    d = ImageDraw.Draw(im)
    for x in range(lx0 + 40, lx1 - 30, 70):  # sheet seams + rivets
        d.line([(x, ly0 + 30), (x, ly1 - 30)], fill=(86, 90, 94), width=2)
        for y in range(ly0 + 50, ly1 - 30, 90):
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(70, 72, 74)); d.ellipse([x - 2, y - 3, x + 1, y], fill=(196, 200, 204))
    # U-shaped staples and the heavy iron bar through them
    by = 455
    for sx in (330, 870):
        d.rounded_rectangle([sx - 40, by - 50, sx + 40, by + 50], 26, outline=(40, 40, 42), width=16)
        d.rounded_rectangle([sx - 40, by - 50, sx + 40, by + 50], 26, outline=(122, 124, 128), width=6)
        d.rectangle([sx - 60, by + 44, sx + 60, by + 70], fill=(60, 62, 64))  # base plate
    bar = [(110, by - 16), (1090, by - 16), (1090, by + 16), (110, by + 16)]
    paste_shadow(im, soft_shadow((W, H), bar, 8, (8, 14), 190))
    steel = tint(noise((W, H), 26, 0.8), (40, 40, 42), (150, 152, 156))
    bm = Image.new('L', (W, H), 0)
    ImageDraw.Draw(bm).rectangle([110, by - 16, 1090, by + 16], fill=255)
    im.paste(steel, (0, 0), bm)
    d = ImageDraw.Draw(im)
    d.line([(110, by - 10), (1090, by - 10)], fill=(214, 216, 220), width=2)  # specular edge
    d.ellipse([1080, by - 26, 1120, by + 26], fill=(58, 58, 60))  # bar knob
    for sx in (330, 870):  # front arm of each staple over the bar
        d.line([(sx + 40, by - 30), (sx + 40, by + 30)], fill=(40, 40, 42), width=16)
        d.line([(sx + 40, by - 30), (sx + 40, by + 30)], fill=(122, 124, 128), width=6)
    # black machine grease smears printed with ribbed rubber-glove texture
    grease = Image.new('L', (W, H), 0)
    gd = ImageDraw.Draw(grease)
    for (cx, w) in ((540, 110), (700, 80), (610, 60)):
        for _ in range(14):
            x = random.gauss(cx, w * 0.45); r = random.uniform(12, 30)
            gd.ellipse([x - r, by - 20 + random.uniform(-6, 6), x + r, by + 18 + random.uniform(-6, 6)], fill=int(random.uniform(170, 240)))
    ribs = Image.new('L', (W, H), 90)
    rd = ImageDraw.Draw(ribs)
    for x in range(430, 800, 11):  # glove palm ribs: short curved dashes, slightly wavy
        x2 = x + random.uniform(-2, 2)
        rd.line(bezier((x2, by - 22), (x2 + 5, by - 8), (x2 - 3, by + 6), (x2 + 4, by + 22), 8), fill=255, width=3)
    grease = ImageChops.multiply(grease.filter(ImageFilter.GaussianBlur(4)), ribs.filter(ImageFilter.GaussianBlur(1.2)))
    grease = ImageChops.multiply(grease, bm.filter(ImageFilter.GaussianBlur(2)))
    # a solid smear first, then the glove ribs pressed into it, then wet highlights
    smear = Image.new('L', (W, H), 0)
    sd2 = ImageDraw.Draw(smear)
    for (x0, x1) in ((430, 660), (640, 790)):
        sd2.rounded_rectangle([x0, by - 15, x1, by + 15], 12, fill=200)
    smear = ImageChops.multiply(smear.filter(ImageFilter.GaussianBlur(3)), bm)
    im.paste((14, 12, 10), (0, 0), smear)
    im.paste((2, 2, 2), (0, 0), grease.point(lambda v: min(255, int(v * 1.6))))
    shine = ImageChops.multiply(smear, noise((W, H), 90, 0.8).point(lambda v: 230 if v > 196 else 0))
    im.paste((196, 196, 192), (0, 0), shine)
    d = ImageDraw.Draw(im)
    for x in range(436, 790, 11):  # light rims of each rib groove
        d.line([(x + 3, by - 13), (x + 5, by - 6)], fill=(92, 90, 86), width=1)
    # scratches of bright steel
    d = ImageDraw.Draw(im)
    for _ in range(20):
        x = random.uniform(140, 1060); d.line([(x, by - 14 + random.uniform(0, 8)), (x + random.uniform(10, 40), by - 12 + random.uniform(0, 8))], fill=(222, 224, 228), width=1)
    im = light_spot(im, 620, 430, 480, 0.2)
    im = vignette(im, 0.55)
    save(grain(im, 9, 0.5), 'd05-nap-khoang')


# ── d11: khay inox: viên đá khô CO2 bốc hơi, ống quạt hút đóng tuyết ────────
def d11():
    random.seed(11)
    W, H = 1200, 900
    streak = noise((W // 6, H), 60, 0).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1))
    base = tint(noise((W, H), 18, 0.3), (150, 154, 158), (214, 218, 222))
    im = Image.blend(base, tint(streak, (140, 144, 148), (226, 230, 234)), 0.45)
    d = ImageDraw.Draw(im)
    for k, c in enumerate([(120, 124, 128), (196, 200, 204), (236, 238, 240), (170, 174, 178)]):
        d.rounded_rectangle([30 + k * 6, 30 + k * 6, W - 30 - k * 6, H - 30 - k * 6], 46 - k * 4, outline=c, width=6)
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    # dry-ice pellets: white cylinders, 20 mm (≈ 44 px), seen at an angle
    pellets = []
    for _ in range(14):
        x, y = random.uniform(180, 560), random.uniform(260, 640)
        a = random.uniform(0, math.pi)
        pellets.append((x, y, a, random.uniform(70, 120)))
    for (x, y, a, L) in sorted(pellets, key=lambda p: p[1]):
        dx, dy = math.cos(a) * L / 2, math.sin(a) * L / 2 * 0.6
        nx, ny = -math.sin(a) * 22, math.cos(a) * 22
        body = [(x - dx + nx, y - dy + ny), (x + dx + nx, y + dy + ny), (x + dx - nx, y + dy - ny), (x - dx - nx, y - dy - ny)]
        paste_shadow(im, soft_shadow((W, H), body, 8, (6, 10), 110))
        m = Image.new('L', (W, H), 0)
        md = ImageDraw.Draw(m)
        md.polygon(body, fill=255)
        md.ellipse([x + dx - 22, y + dy - 22, x + dx + 22, y + dy + 22], fill=255)
        snow = tint(noise((W, H), 40, 0.6), (196, 202, 208), (252, 253, 255))
        im.paste(snow, (0, 0), m)
        d = ImageDraw.Draw(im)
        d.ellipse([x - dx - 22, y - dy - 22, x - dx + 22, y - dy + 22], fill=(236, 240, 244), outline=(176, 184, 192), width=2)  # end face
        d.line([body[0], body[1]], fill=(255, 255, 255), width=3)
    # metal fan-duct section with a narrow funnel mouth crusted with frost
    duct = Image.new('L', (W, H), 0)
    dd = ImageDraw.Draw(duct)
    dd.polygon([(700, 300), (1040, 230), (1080, 420), (740, 490)], fill=255)  # duct body
    dd.polygon([(700, 300), (740, 490), (640, 450), (620, 350)], fill=255)  # narrowing funnel
    paste_shadow(im, soft_shadow((W, H), [(620, 350), (700, 300), (1040, 230), (1080, 420), (740, 490), (640, 450)], 16, (12, 16), 150))
    metal = tint(noise((W, H), 30, 1), (70, 74, 78), (170, 176, 182))
    im.paste(metal, (0, 0), duct)
    d = ImageDraw.Draw(im)
    for k in range(1, 6):
        t = k / 6
        d.line([(700 + 340 * t, 300 - 70 * t), (740 + 340 * t, 490 - 70 * t)], fill=(96, 100, 104), width=3)  # corrugation
    d.ellipse([600, 340, 660, 460], fill=(40, 42, 46), outline=(200, 206, 212), width=3)  # mouth
    frost = Image.new('L', (W, H), 0)
    ImageDraw.Draw(frost).ellipse([570, 300, 720, 500], fill=255)
    ring = Image.new('L', (W, H), 0)
    ImageDraw.Draw(ring).ellipse([586, 322, 674, 478], outline=255, width=18)
    frost = ImageChops.multiply(ring.filter(ImageFilter.GaussianBlur(5)), noise((W, H), 50, 0.6).point(lambda v: min(255, v + 60)))
    im.paste((248, 250, 253), (0, 0), frost)
    d = ImageDraw.Draw(im)
    for _ in range(160):  # frost crystals around the rim
        a = random.uniform(0, 2 * math.pi); r = random.uniform(30, 52)
        x, y = 630 + math.cos(a) * r, 400 + math.sin(a) * r * 1.65
        d.line([(x, y), (x + math.cos(a) * random.uniform(3, 9), y + math.sin(a) * random.uniform(3, 9))], fill=(252, 253, 255), width=1)
    # cold CO2 vapour drifting low over the tray
    fog = Image.new('L', (W, H), 0)
    fd = ImageDraw.Draw(fog)
    for (x, y, a, L) in pellets:
        for k in range(5):
            r = random.uniform(40, 90)
            fd.ellipse([x - r + k * 26, y - r * 0.4 - k * 10, x + r + k * 26, y + r * 0.4 - k * 10], fill=int(random.uniform(40, 90)))
    for k in range(8):
        fd.ellipse([600 - k * 40, 380 - k * 6, 720 - k * 30, 430 - k * 4], fill=60)
    fog = ImageChops.multiply(fog.filter(ImageFilter.GaussianBlur(26)), noise((W, H), 60, 10).point(lambda v: int(min(255, v * 1.6))))
    im = Image.composite(Image.new('RGB', (W, H), (244, 247, 250)), im, fog.point(lambda v: min(255, int(v * 1.7))))
    # scale ruler (cm)
    d = ImageDraw.Draw(im)
    d.rectangle([180, 730, 820, 780], fill=(240, 240, 236), outline=(60, 60, 60), width=2)
    for i in range(0, 641, 22):
        cm = i // 22
        d.line([(180 + i, 730), (180 + i, 752 if cm % 5 == 0 else 742)], fill=(20, 20, 20), width=2 if cm % 5 == 0 else 1)
        if cm % 5 == 0:
            d.text((180 + i, 766), str(cm), font=font(BOLD, 16), fill=(20, 20, 20), anchor='mm')
    im = light_spot(im, 560, 420, 520, 0.16)
    im = vignette(im, 0.45)
    save(grain(im, 7, 0.4), 'd11-da-kho')


if __name__ == '__main__':
    for name in sys.argv[1:] or ['d01', 'd03', 'd04', 'd05', 'd11']:
        globals()[name]()
