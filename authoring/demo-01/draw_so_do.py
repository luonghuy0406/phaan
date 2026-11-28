"""Vẽ sơ đồ tầng 2 và sân sau nhà số 17 ngõ Gác Chuông theo biên bản d02. Chạy: python3 authoring/demo-01/draw_so_do.py"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

random.seed(17)
W, H = 1400, 1050
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (32, 66, 128); SOFT = (110, 135, 175); RED = (190, 36, 40); GREEN = (64, 120, 72); GREY = (120, 120, 120)

im = Image.new('RGB', (W, H), (241, 244, 246)); d = ImageDraw.Draw(im)
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(205, 220, 236) if x % 125 else (175, 198, 224), width=1)
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(205, 220, 236) if y % 125 else (175, 198, 224), width=1)

def wob(pts, a=1.1): return [(x + random.uniform(-a, a), y + random.uniform(-a, a)) for x, y in pts]
def pline(pts, w=3, col=INK, closed=False):
    pts = wob(pts)
    if closed: pts = pts + [pts[0]]
    d.line(pts, fill=col, width=w, joint='curve')
def dashed(a, b, col=INK, w=2, dash=14, gap=9):
    (x1, y1), (x2, y2) = a, b; L = math.hypot(x2 - x1, y2 - y1); n = int(L // (dash + gap)) + 1
    for i in range(n):
        s = i * (dash + gap) / L; e = min(1, (i * (dash + gap) + dash) / L)
        d.line([(x1 + (x2 - x1) * s, y1 + (y2 - y1) * s), (x1 + (x2 - x1) * e, y1 + (y2 - y1) * e)], fill=col, width=w)
def label(xy, text, size=22, f=BOLD, col=INK, anchor='mm'): d.text(xy, text, font=font(f, size), fill=col, anchor=anchor)
def rect(x1, y1, x2, y2, w=4, col=INK): pline([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], w, col, True)

# header
label((40, 40), 'CÔNG AN QUẬN HOÀN KIẾM', 22, BOLD, INK, 'lm'); label((40, 68), 'Đội Cảnh sát hình sự', 20, SANS, INK, 'lm')
label((W / 2 + 80, 46), 'SƠ ĐỒ HIỆN TRƯỜNG NHÀ SỐ 17 NGÕ GÁC CHUÔNG', 30, BOLD)
label((W / 2 + 80, 82), 'Kèm biên bản 17/KNHT · 08 giờ 30 ngày 15/3/2024 · Tỷ lệ 1:100', 21, ITAL)
nx, ny = 1330, 150; d.polygon([(nx, ny - 40), (nx - 14, ny + 10), (nx, ny), (nx + 14, ny + 10)], fill=INK); label((nx, ny - 58), 'B', 24)

# ── tầng 2 (top part): x 120..1180, y 150..560 ──
X1, X2, Y1, Y2 = 120, 1180, 150, 560
label((X1, Y1 - 22), 'TẦNG 2', 22, BOLD, INK, 'lm')
rect(X1, Y1, X2, Y2, 6)
# front: gian thờ (left) | hành lang + cầu thang (middle) | phòng làm việc (right, rear side)
pline([(470, Y1), (470, Y2)], 4); pline([(760, Y1), (760, Y2)], 4)
label((295, 230), 'GIAN THỜ', 26); label((295, 262), '(phía ngõ trước)', 18, ITAL)
d.rectangle([230, 300, 360, 340], outline=INK, width=3); label((295, 320), 'bàn thờ', 17, SANS)
# stairs
for k in range(10): d.line([(500, 200 + k * 26), (620, 200 + k * 26)], fill=SOFT, width=2)
rect(500, 200, 620, 460, 3); label((560, 485), 'CẦU THANG', 18); label((690, 330), 'Hành lang', 18, ITAL, SOFT)
# door to study
d.arc([710, 400, 810, 500], 270, 360, fill=INK, width=2); label((830, 530), 'cửa', 16, ITAL)
label((970, 200), 'PHÒNG LÀM VIỆC', 26)
d.rectangle([860, 330, 1060, 420], outline=INK, width=3); label((960, 362), 'bàn làm việc', 17, SANS)
d.rectangle([905, 392, 965, 416], fill=(255, 255, 255), outline=RED, width=3); label((935, 440), 'Két sắt (gầm bàn, mở đúng mã)', 16, BOLD, RED)
d.rectangle([1090, 180, 1160, 300], outline=INK, width=3); label((1125, 240), 'tủ', 16, SANS)

# rear wall with window (right edge is the rear of the house -> sân sau below/right)
# draw the rear wall at the bottom of tầng 2 block: window on bottom wall of phòng làm việc
wx1, wx2 = 900, 1040
d.line([(wx1, Y2), (wx2, Y2)], fill=(241, 244, 246), width=8)
d.line([(wx1, Y2 - 5), (wx2, Y2 - 5)], fill=RED, width=4); d.line([(wx1, Y2 + 5), (wx2, Y2 + 5)], fill=RED, width=4)
label((970, Y2 - 30), 'Cửa sổ vỡ 1 ô kính', 18, BOLD, RED)
for _ in range(7):  # few shards inside on the sill
    x = random.uniform(wx1 + 10, wx2 - 10); y = random.uniform(Y2 - 16, Y2 - 9)
    d.polygon([(x, y), (x + 5, y + 2), (x + 2, y + 5)], fill=SOFT)

# ── sân sau (tầng 1, below the window) ──
SY1, SY2 = 600, 960
label((X1, SY1 - 14), 'TẦNG 1 · SÂN SAU (nhìn từ trên xuống)', 20, BOLD, INK, 'lm')
rect(760, SY1, X2, SY2, 4)
# glass fall area 1–3 m from the wall (1 m = 40 px at 1:100 on this sheet)
M = 40
d.line([(wx1 - 20, SY1), (wx2 + 20, SY1)], fill=INK, width=6)
label((970, SY1 + 16), 'chân tường (cửa sổ cao 4,2 m)', 15, ITAL)
for _ in range(110):
    x = random.uniform(wx1 - 30, wx2 + 40); y = random.uniform(SY1 + 1 * M, SY1 + 3 * M + 10)
    s = random.uniform(3, 8); d.polygon([(x, y), (x + s, y + s * 0.4), (x + s * 0.3, y + s)], fill=(140, 170, 205), outline=SOFT)
dashed((wx1 - 40, SY1 + 1 * M), (wx2 + 60, SY1 + 1 * M), RED, 2); dashed((wx1 - 40, SY1 + 3 * M + 14), (wx2 + 60, SY1 + 3 * M + 14), RED, 2)
label((970, SY1 + 3 * M + 40), 'Mảnh kính rơi, cách chân tường 1–3 m', 18, BOLD, RED)
# clothes line (empty)
dashed((800, 860), (1150, 860), GREY, 2, 6, 6); label((975, 885), 'dây phơi (không có đồ phơi)', 16, ITAL, GREY)
# rear wall to back alley, kitchen door, back stairs with shoes
d.line([(760, SY2), (X2, SY2)], fill=INK, width=8); label((970, SY2 + 22), 'Tường sau cao 2,2 m · giáp ngõ sau', 17, BOLD)
d.line([(760, 700), (760, 760)], fill=(241, 244, 246), width=8); label((774, 730), 'cửa bếp', 16, ITAL, INK, 'lm')
rect(560, 640, 740, 760, 3); label((650, 676), 'Bếp', 18); label((650, 704), '(tầng 1)', 15, ITAL)
d.rectangle([600, 790, 730, 930], outline=INK, width=3)
for k in range(5): d.line([(600, 800 + k * 26), (730, 800 + k * 26)], fill=SOFT, width=2)
label((665, 950), 'cầu thang sau', 16, ITAL)
d.ellipse([610, 905, 640, 925], outline=RED, width=2); d.ellipse([645, 905, 675, 925], outline=RED, width=2)
label((540, 915), 'giày trắng cỡ 42', 15, BOLD, RED, 'rm'); label((540, 935), '(4 mảnh kính ở đế)', 14, ITAL, RED, 'rm')
d.rectangle([680, 885, 725, 925], outline=GREEN, width=3); label((560, 870), 'giỏ đồ bẩn', 15, BOLD, GREEN, 'rm')
d.line([(565, 870), (680, 900)], fill=GREEN, width=1)

# legend + scale
label((120, 990), '— Không phát hiện dấu leo bám trên tường sau, ống thoát nước, bậu cửa sổ. Không có thang.', 17, ITAL, INK, 'lm')
d.line([(120, 1020), (320, 1020)], fill=INK, width=3)
for k in range(6): d.line([(120 + k * 40, 1012), (120 + k * 40, 1028)], fill=INK, width=2)
label((340, 1020), '5 m', 16, SANS, INK, 'lm')
label((1180, 1015), 'Người vẽ: Đại uý Lương Minh Khải', 17, ITAL, INK, 'rm')

out = 'public/cases/demo-01/images/d02-so-do-nha.webp'
im.save(out, 'WEBP', quality=86)
print(out)
