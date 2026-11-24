"""Vẽ minh hoạ ảnh tư liệu cho hồ sơ 07 (Đêm lửa tàn Buôn Ea Kral) bằng Pillow, không cần mô hình tạo ảnh.

Chạy: python3 authoring/lua-than-tay-nguyen/draw_photos.py [d01|d05|d06|d11 ...]
Kết quả ghi vào public/cases/lua-than-tay-nguyen/images/. Các ảnh này là minh hoạ dựng hình,
có thể thay bằng ảnh tạo từ prompt trong image-prompts.md khi có công cụ tạo ảnh.
"""
import math
import random
import sys
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

OUT = 'public/cases/lua-than-tay-nguyen/images/'
FONTS = '/System/Library/Fonts/Supplemental/'


# ── helpers ──────────────────────────────────────────────────────────────────
def noise(size, sigma=40, blur=0.0):
    n = Image.effect_noise(size, sigma)
    return n.filter(ImageFilter.GaussianBlur(blur)) if blur else n


def tint(gray, dark, light):
    """Map a grayscale image to a colour ramp dark→light."""
    return ImageOps.colorize(gray, dark, light)


def vignette(im, strength=0.55, power=2.2):
    w, h = im.size
    small = Image.new('L', (64, 48))
    for y in range(48):
        for x in range(64):
            dx, dy = (x - 31.5) / 32, (y - 23.5) / 24
            v = max(0.0, 1 - (dx * dx + dy * dy) ** (power / 2) * strength)
            small.putpixel((x, y), int(255 * v))
    mask = small.resize((w, h), Image.BICUBIC)
    black = Image.new('RGB', (w, h), (0, 0, 0))
    return Image.composite(im, black, mask)


def light_spot(im, cx, cy, radius, amount=0.35):
    """Brighten around (cx, cy): a camera flash / lamp hot spot."""
    w, h = im.size
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=int(255 * amount))
    m = m.filter(ImageFilter.GaussianBlur(radius * 0.5))
    return Image.composite(Image.new('RGB', (w, h), (255, 248, 235)), im, m)


def soft_shadow(size, poly, blur=14, offset=(10, 14), alpha=150):
    m = Image.new('L', size, 0)
    ImageDraw.Draw(m).polygon([(x + offset[0], y + offset[1]) for x, y in poly], fill=alpha)
    return m.filter(ImageFilter.GaussianBlur(blur))


def paste_shadow(base, mask):
    base.paste((0, 0, 0), (0, 0), mask)


def bezier(p0, p1, p2, p3, n=60):
    pts = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def grain(im, amount=18, blur=0.4):
    n = noise(im.size, amount, blur).convert('RGB')
    return ImageChops.add(ImageChops.subtract(im, Image.new('RGB', im.size, (amount // 2,) * 3)), n.point(lambda v: max(0, v - 128 + amount // 2)))


def save(im, name, q=86):
    im.save(OUT + name + '.webp', 'WEBP', quality=q, method=6)
    print('ok', name, im.size)


# ── d05: xà gạc vùi trong tro, đèn flash, thước vàng ─────────────────────────
def d05():
    random.seed(5)
    W, H = 1200, 900
    ash = tint(noise((W, H), 52, 1.1), (62, 59, 56), (186, 180, 170))
    im = ash.copy()
    d = ImageDraw.Draw(im)
    # burnt rice husk flakes
    for _ in range(2600):
        x, y = random.uniform(0, W), random.uniform(0, H)
        r = random.uniform(2, 6)
        c = random.choice([(48, 44, 40), (96, 90, 84), (150, 142, 128), (205, 196, 176), (120, 98, 70)])
        a = random.uniform(0, math.pi)
        pts = [(x + math.cos(a) * r * 1.8, y + math.sin(a) * r * 1.8), (x + math.cos(a + 1.7) * r * 0.6, y + math.sin(a + 1.7) * r * 0.6),
               (x - math.cos(a) * r * 1.8, y - math.sin(a) * r * 1.8), (x + math.cos(a - 1.4) * r * 0.6, y + math.sin(a - 1.4) * r * 0.6)]
        d.polygon(pts, fill=c)
    im = im.filter(ImageFilter.GaussianBlur(0.6))

    # machete: blade from left (partly buried) to a forward hook, handle on the right
    angle = -0.18
    def rot(x, y, cx=620, cy=470):
        x, y = x - cx, y - cy
        return (cx + x * math.cos(angle) - y * math.sin(angle), cy + x * math.sin(angle) + y * math.cos(angle))
    spine = [(205, 440), (420, 420), (700, 412), (840, 420)]
    edge = [(840, 500), (700, 520), (430, 532), (250, 540), (165, 520), (118, 478), (112, 430), (132, 398), (160, 392), (150, 420), (165, 446)]
    blade = [rot(*p) for p in spine + edge]
    handle = [rot(*p) for p in [(835, 428), (1075, 420), (1100, 432), (1108, 456), (1100, 482), (1075, 494), (835, 490)]]

    paste_shadow(im, soft_shadow((W, H), blade + handle, 16, (12, 16), 170))
    layer = Image.new('RGB', (W, H))
    steel = tint(noise((W, H), 30, 2.5).resize((W, H)), (28, 29, 31), (128, 130, 134))
    ImageDraw.Draw(layer)
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).polygon(blade, fill=255)
    im.paste(steel, (0, 0), mask)
    d = ImageDraw.Draw(im)
    # soot towards the spine, honed bright edge, thick spine line
    soot = Image.new('L', (W, H), 0)
    ImageDraw.Draw(soot).polygon([rot(*p) for p in [(170, 430), (840, 420), (840, 470), (170, 482)]], fill=150)
    soot = ImageChops.multiply(soot.filter(ImageFilter.GaussianBlur(10)), mask)
    im.paste((14, 13, 12), (0, 0), soot)
    d.line([rot(*p) for p in edge[:5]], fill=(196, 198, 200), width=3)
    d.line([rot(*p) for p in spine], fill=(20, 20, 22), width=7)
    # dried blood + hair on the spine
    blood = Image.new('L', (W, H), 0)
    bd = ImageDraw.Draw(blood)
    for _ in range(70):
        x, y = rot(random.gauss(480, 50), random.uniform(410, 446))
        r = random.uniform(2, 9)
        bd.ellipse([x - r * 1.6, y - r * 0.6, x + r * 1.6, y + r * 0.6], fill=int(random.uniform(120, 230)))
    blood = ImageChops.multiply(blood.filter(ImageFilter.GaussianBlur(2.2)), mask)
    im.paste((58, 12, 10), (0, 0), blood)
    d = ImageDraw.Draw(im)
    d.line(bezier(rot(430, 410), rot(470, 380), rot(520, 450), rot(575, 404)), fill=(18, 14, 12), width=1)
    d.line(bezier(rot(436, 412), rot(480, 392), rot(515, 440), rot(560, 410)), fill=(30, 24, 20), width=1)

    # wooden handle with carved B
    hmask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(hmask).polygon(handle, fill=255)
    wood = tint(noise((W, H), 34, 1.0), (72, 40, 18), (160, 104, 58))
    grain_lines = Image.new('L', (W, H), 0)
    gd = ImageDraw.Draw(grain_lines)
    for k in range(18):
        yy = 424 + k * 4 + random.uniform(-1, 1)
        gd.line([rot(835, yy), rot(1100, yy + random.uniform(-3, 3))], fill=90, width=1)
    wood.paste((48, 26, 10), (0, 0), grain_lines)
    im.paste(wood, (0, 0), hmask)
    # brass ferrule
    d = ImageDraw.Draw(im)
    d.polygon([rot(*p) for p in [(828, 422), (850, 422), (850, 496), (828, 496)]], fill=(150, 118, 56))
    d.line([rot(839, 424), rot(839, 494)], fill=(214, 186, 112), width=2)
    # carved letter (engraved: dark cut with a light lower lip)
    txt = Image.new('L', (220, 120), 0)
    ImageDraw.Draw(txt).text((110, 60), 'B', font=ImageFont.truetype(FONTS + 'Georgia Bold.ttf', 66), fill=255, anchor='mm')
    txt = txt.rotate(math.degrees(-angle), resample=Image.BICUBIC, expand=False)
    cx, cy = rot(965, 457)
    im.paste((198, 150, 96), (int(cx - 110) + 1, int(cy - 60) + 2), txt.filter(ImageFilter.GaussianBlur(0.8)))
    im.paste((40, 20, 8), (int(cx - 110), int(cy - 60)), txt)

    # ash drifting over the buried left half of the blade
    cover = Image.new('L', (W, H), 0)
    ImageDraw.Draw(cover).polygon([(0, 280), (330, 300), (390, 470), (300, 660), (0, 660)], fill=255)
    cover = cover.filter(ImageFilter.GaussianBlur(34))
    cover = ImageChops.multiply(cover, noise((W, H), 90, 3).point(lambda v: 255 if v > 118 else int(v * 1.2)))
    im = Image.composite(ash, im, cover)

    # yellow scale ruler, parallel to the blade
    rl = Image.new('RGBA', (820, 70), (0, 0, 0, 0))
    rd = ImageDraw.Draw(rl)
    rd.rounded_rectangle([0, 0, 819, 69], 6, fill=(236, 196, 40, 255), outline=(170, 130, 20, 255), width=2)
    for i in range(0, 801, 16):
        L = 28 if i % 80 == 0 else 14
        rd.line([(10 + i, 0), (10 + i, L)], fill=(30, 26, 18, 255), width=2 if i % 80 == 0 else 1)
        if i % 80 == 0:
            rd.text((10 + i, 46), str(i // 16), font=ImageFont.truetype(FONTS + 'Arial Bold.ttf', 20), fill=(30, 26, 18, 255), anchor='mm')
    rl = rl.rotate(math.degrees(-angle), resample=Image.BICUBIC, expand=True)
    sh = Image.new('L', rl.size, 0)
    sh.paste(rl.split()[3].filter(ImageFilter.GaussianBlur(8)), (0, 0))
    im.paste((0, 0, 0), (230 + 8, 640 + 10), sh.point(lambda v: v * 0.6))
    im.paste(rl, (230, 640), rl)

    im = light_spot(im, 640, 420, 420, 0.22)
    im = vignette(im, 0.6)
    im = ImageEnhance.Contrast(im).enhance(1.08)
    save(grain(im, 10, 0.5), 'd05-xa-gac')


# ── d11: khay inox giám định: mảnh bóng đèn, đui đèn, bánh răng, lò xo ────────
def gear(d, cx, cy, r, teeth, fill, edge, hole=0.28, rot=0.0, dark=(40, 36, 30), hole_fill=(30, 30, 32)):
    pts = []
    for i in range(teeth * 2):
        a = rot + i * math.pi / teeth
        rr = r if i % 2 == 0 else r * 0.84
        a1, a2 = a - math.pi / teeth * 0.35, a + math.pi / teeth * 0.35
        pts += [(cx + math.cos(a1) * rr, cy + math.sin(a1) * rr), (cx + math.cos(a2) * rr, cy + math.sin(a2) * rr)]
    d.polygon(pts, fill=fill, outline=edge)
    d.ellipse([cx - r * 0.62, cy - r * 0.62, cx + r * 0.62, cy + r * 0.62], outline=edge, width=2)
    for k in range(4):
        a = rot + k * math.pi / 2 + 0.4
        d.ellipse([cx + math.cos(a) * r * 0.42 - r * 0.1, cy + math.sin(a) * r * 0.42 - r * 0.1,
                   cx + math.cos(a) * r * 0.42 + r * 0.1, cy + math.sin(a) * r * 0.42 + r * 0.1], fill=dark)
    d.ellipse([cx - r * hole, cy - r * hole, cx + r * hole, cy + r * hole], fill=hole_fill, outline=edge)


def d11():
    random.seed(11)
    W, H = 1200, 900
    # brushed steel tray
    streak = noise((W // 6, H), 60, 0).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1))
    streak = streak.transform((W, H), Image.AFFINE, (1, 0, 0, 0, 0.02, 0)).filter(ImageFilter.BoxBlur(0))
    base = tint(noise((W, H), 18, 0.3), (150, 154, 158), (214, 218, 222))
    im = Image.blend(base, tint(streak, (140, 144, 148), (226, 230, 234)), 0.45)
    d = ImageDraw.Draw(im)
    # tray rim
    for k, c in enumerate([(120, 124, 128), (196, 200, 204), (236, 238, 240), (170, 174, 178)]):
        d.rounded_rectangle([30 + k * 6, 30 + k * 6, W - 30 - k * 6, H - 30 - k * 6], 46 - k * 4, outline=c, width=6)
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    d = ImageDraw.Draw(im)

    # bulb shards: curved pieces of a smoked glass sphere (two arcs + jagged ends)
    def shard(cx, cy, R, a1, a2, thick, seed):
        rnd = random.Random(seed)
        outer = [(cx + R * math.cos(a), cy + R * math.sin(a) * 0.8) for a in [a1 + (a2 - a1) * k / 18 for k in range(19)]]
        inner = [(cx + (R - thick) * math.cos(a), cy + (R - thick) * math.sin(a) * 0.8) for a in [a2 - (a2 - a1) * k / 18 for k in range(19)]]
        jag = lambda p, q: [(p[0] + (q[0] - p[0]) * t + rnd.uniform(-6, 6), p[1] + (q[1] - p[1]) * t + rnd.uniform(-6, 6)) for t in (0.33, 0.66)]
        return outer + jag(outer[-1], inner[0]) + inner + jag(inner[-1], outer[0]), outer
    glass = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd2 = ImageDraw.Draw(glass)
    smoke_tex = noise((W, H), 60, 6)
    for k, (cx, cy, R, a1, a2, th) in enumerate([(330, 300, 120, 3.4, 4.6, 70), (470, 420, 90, 5.0, 6.2, 60), (260, 470, 70, 0.3, 1.5, 48),
                                                 (420, 560, 64, 3.9, 5.0, 40), (560, 270, 54, 0.9, 2.2, 36)]):
        poly, outer = shard(cx, cy, R, a1, a2, th, k)
        paste_shadow(im, soft_shadow((W, H), poly, 7, (6, 9), 90))
        m = Image.new('L', (W, H), 0)
        ImageDraw.Draw(m).polygon(poly, fill=255)
        # smoked inside: darker where the soot settled, clearer near the rim
        soot = ImageChops.multiply(m, smoke_tex.point(lambda v: int(max(0, min(255, (v - 70) * 2.2)))))
        glass.paste((26, 22, 18, 255), (0, 0), soot.point(lambda v: int(v * 0.75)))
        glass.paste((236, 240, 244, 255), (0, 0), ImageChops.subtract(m.point(lambda v: int(v * 0.32)), soot.point(lambda v: int(v * 0.3))))
        gd2.line(poly + [poly[0]], fill=(250, 252, 255, 150), width=1)
        gd2.line(outer[2:-2], fill=(255, 255, 255, 235), width=3)  # specular rim highlight
    glass = glass.filter(ImageFilter.GaussianBlur(0.8))
    im.paste(glass, (0, 0), glass)
    d = ImageDraw.Draw(im)
    # broken tungsten filament
    fx, fy = 380, 300  # tight helix, snapped in two
    helix = [(fx + t * 1.6 + 4 * math.cos(t * 1.9), fy + 5 * math.sin(t * 1.9) + t * 0.35) for t in [i * 0.12 for i in range(0, 260)]]
    d.line(helix[:150], fill=(58, 54, 48), width=1)
    d.line([(x + 6, y + 10) for x, y in helix[165:]], fill=(58, 54, 48), width=1)
    d.line([helix[0], (helix[0][0] - 18, helix[0][1] + 26)], fill=(90, 86, 80), width=1)

    # brass screw socket (side view) + scorched twin cable
    sx, sy = 760, 300
    paste_shadow(im, soft_shadow((W, H), [(sx - 70, sy - 120), (sx + 70, sy - 120), (sx + 70, sy + 120), (sx - 70, sy + 120)], 14, (14, 16), 140))
    brass = tint(noise((140, 240), 25, 1), (110, 80, 30), (230, 192, 110))
    shade = Image.new('L', (140, 240))
    for x in range(140):
        v = int(110 + 120 * math.sin(math.pi * x / 139))
        ImageDraw.Draw(shade).line([(x, 0), (x, 239)], fill=v)
    brass = Image.composite(brass, Image.new('RGB', (140, 240), (60, 40, 14)), shade)
    im.paste(brass, (sx - 70, sy - 120))
    d = ImageDraw.Draw(im)
    for k in range(10):
        y = sy - 100 + k * 18
        d.arc([sx - 72, y - 8, sx + 72, y + 8], 0, 180, fill=(92, 66, 26), width=3)
        d.arc([sx - 72, y - 6, sx + 72, y + 10], 200, 340, fill=(236, 206, 132), width=2)
    soot = Image.new('L', (W, H), 0)
    ImageDraw.Draw(soot).ellipse([sx - 80, sy - 140, sx + 60, sy - 10], fill=170)
    im.paste((18, 16, 14), (0, 0), soot.filter(ImageFilter.GaussianBlur(22)))
    d = ImageDraw.Draw(im)
    for off, col in ((-9, (214, 172, 30)), (9, (226, 186, 40))):
        cable = bezier((sx + off, sy + 120), (sx + off + 20, sy + 260), (sx + 200 + off, sy + 160), (sx + 330 + off, sy + 300), 80)
        d.line([(x + 6, y + 8) for x, y in cable], fill=(120, 120, 124), width=16)
        d.line(cable, fill=col, width=14)
        burnt = cable[:42]
        d.line(burnt, fill=(32, 26, 20), width=12)  # heat-shrunk, charred near the socket
        for i in range(0, 40, 2):
            x, y = burnt[i]
            d.line([(x - 5, y - 4), (x + 5, y + 4)], fill=random.choice([(18, 16, 14), (70, 52, 26), (110, 86, 40)]), width=2)
        d.line(cable[40:46], fill=(120, 96, 40), width=13)  # scorched transition
    # copper cores at the cut
    ex, ey = bezier((sx, sy + 120), (sx + 20, sy + 260), (sx + 200, sy + 160), (sx + 330, sy + 300), 80)[-1]
    d.line([(ex, ey), (ex + 30, ey + 18)], fill=(196, 110, 60), width=4)

    # brass gears and coil spring of the incubator timer relay, half burnt
    gl = Image.new('RGB', (W, H), (0, 0, 0))
    gm = Image.new('L', (W, H), 0)
    gdr, gmd = ImageDraw.Draw(gl), ImageDraw.Draw(gm)
    for (cx, cy, r, t, rr) in [(380, 690, 110, 28, 0.1), (560, 640, 70, 20, 0.3), (640, 760, 48, 14, 0.0)]:
        paste_shadow(im, soft_shadow((W, H), [(cx - r, cy - r), (cx + r, cy - r), (cx + r, cy + r), (cx - r, cy + r)], 18, (12, 14), 90))
        gear(gdr, cx, cy, r, t, (190, 148, 64), (110, 80, 30), rot=rr)
        gear(gmd, cx, cy, r, t, 255, 255, rot=rr, dark=0, hole_fill=0)
    brushed = tint(noise((W, H), 30, 1.2), (120, 88, 34), (232, 196, 112))
    gl = Image.blend(gl, brushed, 0.35)
    im.paste(gl, (0, 0), gm)
    burn = Image.new('L', (W, H), 0)
    ImageDraw.Draw(burn).ellipse([260, 600, 520, 820], fill=200)
    burn = ImageChops.multiply(burn.filter(ImageFilter.GaussianBlur(30)), gm)
    im.paste((24, 20, 16), (0, 0), burn)
    d = ImageDraw.Draw(im)
    # coil spring (archimedean spiral)
    cx, cy = 900, 650
    spiral = [(cx + (6 + 5.2 * t) * math.cos(t), cy + (6 + 5.2 * t) * math.sin(t) * 0.92) for t in [i * 0.08 for i in range(0, 360)]]
    d.line([(x + 6, y + 8) for x, y in spiral], fill=(110, 112, 116), width=6)
    d.line(spiral, fill=(176, 136, 62), width=5)
    d.line(spiral, fill=(236, 206, 140), width=1)
    d.line([spiral[-1], (spiral[-1][0] + 60, spiral[-1][1] + 30)], fill=(176, 136, 62), width=5)

    im = light_spot(im, 600, 380, 520, 0.18)
    im = vignette(im, 0.45)
    save(grain(im, 8, 0.4), 'd11-rui-dien')


# ── d01: ảnh báo đen trắng: tàn tích kho thóc, nhà rông phía sau ─────────────
def d01():
    random.seed(1)
    W, H = 1280, 800
    hz = 440
    im = Image.new('L', (W, H), 200)
    d = ImageDraw.Draw(im)
    for y in range(H):  # pale morning sky
        d.line([(0, y), (W, y)], fill=int(226 - 30 * (y / hz)) if y < hz else 0)
    # distant hills + tree line
    d.polygon([(0, hz - 60)] + [(x, hz - 60 - 40 * math.sin(x / 210) - 20 * math.sin(x / 70)) for x in range(0, W + 20, 20)] + [(W, hz + 10), (0, hz + 10)], fill=176)
    for x in range(-20, W + 20, 16):
        h = random.uniform(30, 90)
        d.ellipse([x - 26, hz - h, x + 26, hz + 16], fill=int(146 + random.uniform(-14, 10)))
    # ground: red basalt earth rendered mid-grey, textured, darker towards the camera
    gr = noise((W, H - hz + 10), 40, 0.8)
    ground = Image.new('L', gr.size)
    for y in range(gr.size[1]):
        ImageDraw.Draw(ground).line([(0, y), (W, y)], fill=int(118 - 46 * y / gr.size[1]))
    ground = ImageChops.add(ground, gr.point(lambda v: int((v - 128) * 0.35 + 128)), 1, -128)
    im.paste(ground, (0, hz - 10))
    d = ImageDraw.Draw(im)

    # nhà rông (side view): stilts, floor, tall axe-blade roof with concave flanks
    rx, base = 1000, hz + 50
    for k in range(-120, 125, 24):
        d.line([(rx + k, base), (rx + k, base - 70)], fill=70, width=7)
    d.rectangle([rx - 140, base - 84, rx + 140, base - 66], fill=64)  # floor
    d.rectangle([rx - 120, base - 150, rx + 120, base - 84], fill=82)  # walls
    left = bezier((rx - 175, base - 120), (rx - 120, base - 200), (rx - 70, base - 330), (rx - 36, base - 420), 30)
    right = bezier((rx + 36, base - 420), (rx + 70, base - 330), (rx + 120, base - 200), (rx + 175, base - 120), 30)
    d.polygon(left + right + [(rx + 175, base - 110), (rx - 175, base - 110)], fill=58)
    for t in range(0, 30, 3):  # thatch strokes
        a, b = left[t], right[29 - t]
        d.line([a, (a[0] + 30, a[1] + 40)], fill=72, width=2)
        d.line([b, (b[0] - 30, b[1] + 40)], fill=72, width=2)
    d.line([(rx - 36, base - 420), (rx - 52, base - 446)], fill=50, width=5)  # crossed ridge horns
    d.line([(rx + 36, base - 420), (rx + 52, base - 446)], fill=50, width=5)
    d.line([(rx - 60, base - 70), (rx - 90, base)], fill=60, width=6)  # ladder

    # burnt storehouse ruins: irregular ash mound, charred posts, fallen beams, tiles
    bx, by = 500, 650
    mound = [(bx - 310, by + 30)] + [(bx + x, by - 40 - 50 * math.sin((x + 310) / 620 * math.pi) + random.uniform(-14, 14)) for x in range(-290, 300, 30)] + [(bx + 320, by + 30)]
    d.polygon(mound, fill=40)
    tex = noise((W, H), 70, 1.2).point(lambda v: 255 if v > 150 else 0)
    mm = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mm).polygon(mound, fill=255)
    im.paste(Image.new('L', (W, H), 92), (0, 0), ImageChops.multiply(tex, mm))
    d = ImageDraw.Draw(im)
    for (x, h, tilt) in [(-230, 230, -0.06), (-120, 300, 0.03), (10, 200, 0.14), (120, 270, -0.03), (230, 180, 0.09)]:
        x0 = bx + x
        top = [(x0 - 11 + tilt * h, by - 30 - h), (x0 - 2 + tilt * h, by - 30 - h - random.uniform(10, 26)), (x0 + 11 + tilt * h, by - 30 - h + 6)]
        d.polygon([(x0 - 12, by - 20), (x0 + 12, by - 20)] + top[::-1], fill=22)
        d.line([(x0 + 6, by - 30), (x0 + 6 + tilt * h, by - 30 - h)], fill=48, width=2)  # char cracks
    for (a, b) in [((bx - 260, by - 150), (bx + 40, by - 50)), ((bx - 60, by - 230), (bx + 250, by - 110)), ((bx - 170, by - 50), (bx + 210, by - 190))]:
        d.line([a, b], fill=28, width=13)
    for _ in range(180):
        x, y = random.uniform(bx - 290, bx + 300), random.uniform(by - 70, by + 20)
        d.polygon([(x, y), (x + random.uniform(10, 20), y - 3), (x + random.uniform(10, 20), y + 7), (x, y + 6)], fill=int(random.uniform(50, 96)))
    # smoke: darker than the sky, drifting right
    smoke = Image.new('L', (W, H), 0)
    sd = ImageDraw.Draw(smoke)
    for k in range(40):
        y = by - 110 - k * 14
        x = bx - 30 + k * 9 + math.sin(k * 0.45) * 26
        r = 24 + k * 4.2
        sd.ellipse([x - r, y - r * 0.55, x + r, y + r * 0.55], fill=int(210 - k * 4.5))
    smoke = smoke.filter(ImageFilter.GaussianBlur(20))
    smoke = ImageChops.multiply(smoke, noise((W, H), 50, 8).point(lambda v: int(min(255, v * 1.5))))
    im = Image.composite(Image.new('L', (W, H), 110), im, smoke)
    d = ImageDraw.Draw(im)

    # cordon tape on stakes, a policeman, villagers far away (no faces)
    tape = [(40, 712), (300, 700), (560, 714), (820, 700), (1060, 712), (1250, 698)]
    for x, y in tape:
        d.rectangle([x - 4, y - 48, x + 4, y + 46], fill=52)
    d.line(tape, fill=232, width=5)
    def person(x, y, s, shade, cap=False):
        d.ellipse([x - 9 * s, y - 72 * s, x + 9 * s, y - 54 * s], fill=shade)
        if cap:
            d.ellipse([x - 13 * s, y - 78 * s, x + 13 * s, y - 66 * s], fill=shade - 12)
            d.rectangle([x - 15 * s, y - 70 * s, x + 15 * s, y - 66 * s], fill=shade - 12)
        d.polygon([(x - 15 * s, y - 52 * s), (x + 15 * s, y - 52 * s), (x + 13 * s, y - 14 * s), (x - 13 * s, y - 14 * s)], fill=shade)
        d.rectangle([x - 11 * s, y - 14 * s, x - 2 * s, y], fill=shade - 8)
        d.rectangle([x + 2 * s, y - 14 * s, x + 11 * s, y], fill=shade - 8)
    person(1150, 712, 1.7, 46, cap=True)
    for (x, s) in [(720, 0.75), (748, 0.7), (785, 0.78), (1220, 0.8), (130, 0.85), (162, 0.8), (196, 0.82)]:
        person(x, hz + 110, s, 66)

    im = im.filter(ImageFilter.GaussianBlur(0.8))
    im = Image.merge('RGB', (im, im, im))
    im = grain(im, 24, 0.6).convert('L')
    im = ImageOps.autocontrast(im, cutoff=1)
    im = ImageOps.colorize(im, (22, 20, 18), (238, 232, 218))  # newsprint tone
    im = vignette(im, 0.35)
    save(im, 'd01-bao-chi')


# ── d06: ảnh thẻ kẹp vào hồ sơ trên bàn gỗ ───────────────────────────────────
def d06():
    random.seed(6)
    W, H = 1200, 900
    wood = tint(noise((W // 4, H), 50, 0).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(2)), (58, 34, 18), (128, 84, 48))
    d = ImageDraw.Draw(wood)
    for k in range(60):
        y = random.uniform(0, H)
        d.line(bezier((0, y), (400, y + random.uniform(-20, 20)), (800, y + random.uniform(-20, 20)), (W, y + random.uniform(-10, 10))), fill=(48, 28, 14), width=1)
    im = wood
    # yellowed file sheet, slightly rotated, with unreadable typed lines
    sheet = Image.new('RGBA', (760, 940), (232, 222, 192, 255))
    sd = ImageDraw.Draw(sheet)
    sheet.paste(tint(noise((760, 940), 14, 1), (214, 202, 168), (240, 232, 206)), (0, 0))
    sd.rectangle([0, 0, 759, 939], outline=(190, 176, 140), width=2)
    for i in range(22):
        y = 300 + i * 26
        if y > 900: break
        w = random.uniform(380, 640) if i % 5 else random.uniform(160, 300)
        sd.rounded_rectangle([60 if i % 5 else 60, y, 60 + w, y + 8], 4, fill=(150, 140, 118, 255))
    for i in range(5):  # form lines near the photo
        sd.line([(290, 80 + i * 40), (700, 80 + i * 40)], fill=(170, 158, 128, 255), width=2)
        sd.rounded_rectangle([290, 64 + i * 40, 290 + random.uniform(120, 320), 72 + i * 40], 3, fill=(110, 104, 96, 255))
    sheet = sheet.rotate(-4, resample=Image.BICUBIC, expand=True)
    sh = sheet.split()[3].filter(ImageFilter.GaussianBlur(14))
    im.paste((0, 0, 0), (250 + 14, -60 + 18), sh.point(lambda v: int(v * 0.55)))
    im.paste(sheet, (250, -60), sheet)

    # 4x6 ID photo: light-blue backdrop, head-and-shoulders portrait in low detail
    pw, ph = 260, 360
    photo = Image.new('RGB', (pw, ph), (170, 198, 222))
    pd = ImageDraw.Draw(photo)
    for y in range(ph):
        pd.line([(0, y), (pw, y)], fill=(int(176 - y * 0.05), int(204 - y * 0.06), int(226 - y * 0.05)))
    # shoulders + light-blue collared shirt
    pd.polygon([(20, ph), (40, 270), (100, 238), (160, 238), (220, 270), (240, ph)], fill=(132, 168, 200))
    pd.polygon([(100, 238), (130, 300), (160, 238)], fill=(96, 72, 54))  # neck V
    pd.polygon([(100, 238), (122, 262), (112, 296), (88, 252)], fill=(214, 228, 240))  # collar L
    pd.polygon([(160, 238), (138, 262), (148, 296), (172, 252)], fill=(214, 228, 240))  # collar R
    pd.rectangle([112, 200, 148, 246], fill=(104, 74, 50))  # neck
    # head: tanned skin, short black hair following the skull, simple features
    SKIN, SKIN_D, HAIR = (128, 90, 60), (96, 64, 42), (24, 20, 18)
    pd.ellipse([70, 150, 90, 196], fill=SKIN_D); pd.ellipse([170, 150, 190, 196], fill=SKIN_D)  # ears
    pd.ellipse([84, 78, 176, 232], fill=SKIN)  # face
    pd.polygon([(92, 196), (104, 224), (130, 238), (156, 224), (168, 196)], fill=SKIN)  # jaw
    hair = [(80, 150), (78, 112), (90, 84), (114, 66), (146, 64), (170, 80), (182, 110), (180, 150), (172, 128), (162, 112)]
    fringe = [(162, 112), (150, 118), (140, 110), (128, 120), (116, 110), (104, 120), (94, 112), (88, 128)]
    pd.polygon(hair + fringe, fill=HAIR)
    shade = Image.new('L', (pw, ph), 0)
    sh = ImageDraw.Draw(shade)
    sh.ellipse([136, 96, 196, 236], fill=120)  # side of the face away from the lamp
    sh.ellipse([110, 210, 150, 246], fill=90)  # under the chin
    photo.paste((60, 40, 26), (0, 0), shade.filter(ImageFilter.GaussianBlur(14)))
    pd = ImageDraw.Draw(photo)
    pd.line([(102, 140), (122, 137)], fill=(34, 24, 18), width=4); pd.line([(138, 137), (158, 140)], fill=(34, 24, 18), width=4)  # brows
    for ex in (112, 148):
        pd.ellipse([ex - 7, 150, ex + 7, 158], fill=(236, 226, 214)); pd.ellipse([ex - 4, 150, ex + 4, 158], fill=(30, 22, 18))  # eyes
    pd.line([(130, 160), (126, 186)], fill=(98, 66, 44), width=2); pd.arc([118, 180, 140, 194], 20, 160, fill=(88, 58, 38), width=2)  # nose
    pd.line([(116, 206), (144, 206)], fill=(78, 48, 34), width=3); pd.arc([116, 202, 144, 214], 200, 340, fill=(140, 96, 68), width=1)  # mouth
    photo = photo.filter(ImageFilter.GaussianBlur(1.1))
    photo = ImageEnhance.Color(photo).enhance(0.75)
    photo = ImageOps.expand(photo, 12, fill=(244, 242, 236))
    photo = photo.rotate(3, resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0))
    m = Image.new('L', photo.size, 0)
    ImageDraw.Draw(m).polygon([(6, 18), (photo.size[0] - 18, 4), (photo.size[0] - 4, photo.size[1] - 18), (20, photo.size[1] - 4)], fill=255)
    px_, py_ = 300, 40
    im.paste((0, 0, 0), (px_ + 10, py_ + 14), m.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.6)))
    im.paste(photo, (px_, py_), m)
    # paper clip over the photo's top edge
    d = ImageDraw.Draw(im)
    cx, cy = px_ + 170, py_ + 6
    for w, col in ((9, (70, 72, 76)), (5, (196, 200, 206))):
        d.rounded_rectangle([cx, cy - 34, cx + 46, cy + 96], 22, outline=col, width=w)
        d.rounded_rectangle([cx + 10, cy - 20, cx + 36, cy + 70], 13, outline=col, width=w)

    im = light_spot(im, 420, 180, 520, 0.26)
    im = ImageEnhance.Color(im).enhance(0.92)
    im = vignette(im, 0.7)
    save(grain(im, 8, 0.5), 'd06-anh-the')


if __name__ == '__main__':
    todo = sys.argv[1:] or ['d01', 'd05', 'd06', 'd11']
    for name in todo:
        globals()[name]()
