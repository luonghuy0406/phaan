"""Vẽ sơ đồ hiện trường d03 (buôn Ea Kral) theo biên bản d02, d04. Chạy: python3 authoring/lua-than-tay-nguyen/draw_so_do.py"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(4)
W, H = 1400, 1050
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (32, 66, 128); INK_SOFT = (90, 120, 170); RED = (190, 36, 40); GREEN = (64, 120, 72); EARTH = (176, 92, 54)

im = Image.new('RGB', (W, H), (241, 244, 246)); d = ImageDraw.Draw(im)
# graph paper
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(205, 220, 236) if x % 125 else (175, 198, 224), width=1)
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(205, 220, 236) if y % 125 else (175, 198, 224), width=1)

def wobble(pts, amp=1.2):
    return [(x + random.uniform(-amp, amp), y + random.uniform(-amp, amp)) for x, y in pts]
def pline(pts, w=3, col=INK, closed=False):
    pts = wobble(pts)
    if closed: pts = pts + [pts[0]]
    d.line(pts, fill=col, width=w, joint='curve')
def dashed(a, b, col=INK, w=3, dash=16, gap=10):
    (x1, y1), (x2, y2) = a, b; L = math.hypot(x2 - x1, y2 - y1); n = int(L // (dash + gap)) + 1
    for i in range(n):
        s = i * (dash + gap) / L; e = min(1, (i * (dash + gap) + dash) / L)
        d.line([(x1 + (x2 - x1) * s, y1 + (y2 - y1) * s), (x1 + (x2 - x1) * e, y1 + (y2 - y1) * e)], fill=col, width=w)
def label(xy, text, size=24, f=BOLD, col=INK, anchor='mm'):
    d.text(xy, text, font=font(f, size), fill=col, anchor=anchor)

# header
label((40, 40), 'CÔNG AN TỈNH ĐẮK LẮK', 22, BOLD, INK, 'lm'); label((40, 68), 'Phòng Kỹ thuật hình sự', 20, SANS, INK, 'lm')
label((W / 2 + 60, 48), 'SƠ ĐỒ KHU VỰC TRUNG TÂM BUÔN EA KRAL', 30, BOLD, INK); label((W / 2 + 60, 84), 'Đêm lễ cúng bến nước 09/04/2001 · Tỷ lệ 1:1000', 22, ITAL, INK)
# north arrow
nx, ny = 1320, 90; d.polygon([(nx, ny - 40), (nx - 14, ny + 10), (nx, ny), (nx + 14, ny + 10)], fill=INK); label((nx, ny - 58), 'N', 24)

# red-earth road along the village
road = [(60, 760), (300, 735), (560, 745), (820, 760), (1080, 750), (1340, 735)]
for off in (-22, 22): pline([(x, y + off) for x, y in road], 2, EARTH)
label((1180, 800), 'Đường đất đỏ ra cuối buôn →', 20, ITAL, EARTH)

# scale: 5 px = 1 m (1:1000 on the original sheet)
M = 5
# nhà rông (tall roof seen from above + side elevation hint)
rx, ry = 250, 470
RW = 140
pline([(rx - RW, ry - 70), (rx + RW, ry - 70), (rx + RW, ry + 70), (rx - RW, ry + 70)], 4, INK, True)
pline([(rx - RW, ry - 70), (rx, ry - 160), (rx + RW, ry - 70)], 4, INK)
for k in range(-110, 120, 40): d.line([(rx + k, ry - 70), (rx + k * 0.12, ry - 150)], fill=INK_SOFT, width=1)
label((rx, ry - 8), 'NHÀ RÔNG LỚN', 26); label((rx, ry + 26), '(lễ cúng bến nước, từ 19h30)', 18, ITAL)
# low-voltage pole
px, py = rx + RW + 40, ry - 30
d.ellipse([px - 11, py - 11, px + 11, py + 11], outline=INK, width=3); d.line([(px - 8, py - 8), (px + 8, py + 8)], fill=INK, width=3); d.line([(px - 8, py + 8), (px + 8, py - 8)], fill=INK, width=3)
label((px + 6, py - 52), 'Cột điện', 18, SANS, INK); label((px + 6, py - 30), 'hạ thế', 18, SANS, INK)

# kho thóc 50 m east of the nhà rông
kx = rx + RW + 50 * M + 75; ky = ry
kw, kh = 150, 120
pline([(kx - kw / 2, ky - kh / 2), (kx + kw / 2, ky - kh / 2), (kx + kw / 2, ky + kh / 2), (kx - kw / 2, ky + kh / 2)], 5, INK, True)
for i in range(1, 4): d.line([(kx - kw / 2 + i * kw / 4, ky - kh / 2), (kx - kw / 2 + i * kw / 4, ky + kh / 2)], fill=INK_SOFT, width=1)  # sàn / bồ thóc
label((kx, ky - kh / 2 - 26), 'KHO THÓC (nhà sàn)', 24)
# hatching = burnt area
d.rectangle([kx - kw / 2 + 4, ky - kh / 2 + 4, kx + kw / 2 - 4, ky + kh / 2 - 4], fill=(214, 220, 229))
for i in range(1, 4): d.line([(kx - kw / 2 + i * kw / 4, ky - kh / 2 + 4), (kx - kw / 2 + i * kw / 4, ky + kh / 2 - 4)], fill=INK_SOFT, width=1)
label((kx, ky + 4), 'vùng cháy', 16, ITAL, INK_SOFT)
# body position: south-east corner
bx, by = kx + kw / 2 - 22, ky + kh / 2 - 22
d.ellipse([bx - 15, by - 15, bx + 15, by + 15], outline=RED, width=3); label((bx, by), '1', 20, BOLD, RED)
# single wire pole -> kho
dashed((px + 12, py), (kx - kw / 2, ky - 35), INK, 3, 14, 8)
# 50 m dimension
y0 = ry + 120
d.line([(rx + RW, y0), (kx - kw / 2, y0)], fill=INK, width=2)
for x in (rx + RW, kx - kw / 2): d.line([(x, y0 - 10), (x, y0 + 10)], fill=INK, width=2)
label(((rx + RW + kx - kw / 2) / 2, y0 + 20), '50 m', 20, BOLD)
# hibiscus hedge + open ground
hx = (rx + RW + kx - kw / 2) / 2 + 45
for y in range(ry - 120, ry + 90, 18):
    d.ellipse([hx - 8 + random.uniform(-2, 2), y - 8, hx + 8 + random.uniform(-2, 2), y + 8], outline=GREEN, width=2)
label((hx, ry - 140), 'Hàng rào dâm bụt', 18, ITAL, GREEN)
label((hx - 80, ry + 92), 'Bãi đất trống', 18, ITAL, INK_SOFT)

# Y Bang's machine workshop 120 m further towards the end of the village
wx = kx + kw / 2 + 300 + 130  # drawn shorter: sheet is cut, see broken dimension line
wy = ry + 40
pline([(wx - 130, wy - 55), (wx + 130, wy - 55), (wx + 130, wy + 55), (wx - 130, wy + 55)], 4, INK, True)
label((wx, wy - 14), 'XƯỞNG SỬA MÁY', 22); label((wx, wy + 16), 'NÔNG NGHIỆP (Y Bang)', 19)
y1 = ry + 140
d.line([(kx + kw / 2, y1), (wx - 130, y1)], fill=INK, width=2)
for x in (kx + kw / 2, wx - 130): d.line([(x, y1 - 10), (x, y1 + 10)], fill=INK, width=2)
mx = (kx + kw / 2 + wx - 130) / 2
d.line([(mx - 8, y1 + 12), (mx + 8, y1 - 12)], fill=INK, width=2); d.line([(mx + 4, y1 + 12), (mx + 20, y1 - 12)], fill=INK, width=2)  # break mark
label((mx + 70, y1 - 20), '120 m', 20, BOLD)

# other houses (nhà dài) and trees for context
for (hx2, hy2) in [(140, 230), (420, 230), (720, 250), (1000, 300), (1230, 330), (160, 900), (520, 905), (900, 905), (1230, 900)]:
    pline([(hx2 - 55, hy2 - 22), (hx2 + 55, hy2 - 22), (hx2 + 55, hy2 + 22), (hx2 - 55, hy2 + 22)], 2, INK_SOFT, True)
for _ in range(26):
    tx, ty = random.choice([(random.uniform(60, 1340), random.uniform(140, 200)), (random.uniform(60, 1340), random.uniform(950, 1010))])
    d.ellipse([tx - 12, ty - 12, tx + 12, ty + 12], outline=GREEN, width=2)
label((140, 268), 'nhà dài', 16, ITAL, INK_SOFT)

# legend
lx, ly = 40, 600
d.rectangle([lx, ly, lx + 330, ly + 120], outline=INK, width=2, fill=(241, 244, 246))
label((lx + 14, ly + 22), 'GHI CHÚ', 20, BOLD, INK, 'lm')
d.ellipse([lx + 14, ly + 42, lx + 38, ly + 66], outline=RED, width=3); label((lx + 26, ly + 54), '1', 16, BOLD, RED)
label((lx + 50, ly + 54), 'Vị trí tử thi (góc đông nam kho)', 18, SANS, INK, 'lm')
dashed((lx + 14, ly + 90), (lx + 40, ly + 90), INK, 3, 8, 5); label((lx + 50, ly + 90), 'Đường dây điện tự kéo', 18, SANS, INK, 'lm')

# red stamp
sx, sy = 1230, 960
stamp = Image.new('RGBA', (220, 220), (0, 0, 0, 0)); sd = ImageDraw.Draw(stamp)
sd.ellipse([8, 8, 212, 212], outline=RED + (210,), width=6); sd.ellipse([40, 40, 180, 180], outline=RED + (210,), width=3)
sd.text((110, 92), 'CÔNG AN', font=font(BOLD, 22), fill=RED + (220,), anchor='mm'); sd.text((110, 122), 'ĐẮK LẮK', font=font(BOLD, 22), fill=RED + (220,), anchor='mm')
sd.text((110, 26), '★', font=font('Arial Unicode.ttf', 22), fill=RED + (220,), anchor='mm')
stamp = stamp.rotate(-14, resample=Image.BICUBIC)
im.paste(stamp, (sx - 110, sy - 110), stamp)

# slight paper softness
im = im.filter(ImageFilter.GaussianBlur(0.4))
im.save('public/cases/lua-than-tay-nguyen/images/d03-so-do-buon-lang.webp', 'WEBP', quality=88, method=6)
print('ok', im.size)
