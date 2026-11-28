"""Vẽ sơ đồ hiện trường d04 (images/d04-so-do-hien-truong.webp). Chạy: python3 authoring/dem-sung-no-tay-son/draw_so_do.py"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1400, 1000
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (32, 44, 80); SOFT = (110, 122, 148); RED = (185, 35, 35); ROAD = (226, 222, 210)

im = Image.new('RGB', (W, H), (244, 241, 232)); d = ImageDraw.Draw(im)
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(224, 226, 228) if x % 125 else (206, 212, 218))
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(224, 226, 228) if y % 125 else (206, 212, 218))
def label(xy, t, s=20, f=BOLD, c=INK, a='mm'): d.text(xy, t, font=font(f, s), fill=c, anchor=a)
def marker(x, y, n):
    d.ellipse([x - 15, y - 15, x + 15, y + 15], outline=RED, width=3); label((x, y), str(n), 17, BOLD, RED)
def dashed(pts, c=RED, w=3, dash=14, gap=9):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1); n = int(L // (dash + gap)) + 1
        for i in range(n):
            s = i * (dash + gap) / L; e = min(1, (i * (dash + gap) + dash) / L)
            d.line([(x1 + (x2 - x1) * s, y1 + (y2 - y1) * s), (x1 + (x2 - x1) * e, y1 + (y2 - y1) * e)], fill=c, width=w)

label((40, 40), 'CÔNG AN THÀNH PHỐ HÀ NỘI', 22, BOLD, INK, 'lm'); label((40, 68), 'Phòng Cảnh sát hình sự', 20, SANS, INK, 'lm')
label((W / 2 + 100, 44), 'SƠ ĐỒ HIỆN TRƯỜNG TIỆM VÀNG PHÚC HƯNG', 30)
label((W / 2 + 100, 80), 'Phố Chùa Bộc, quận Đống Đa · lập 23h30 ngày 26/8/1998 · không theo tỷ lệ', 19, ITAL)

# main street at the bottom
d.rectangle([0, 800, W, 900], fill=ROAD, outline=SOFT); label((W / 2, 850), 'PHỐ CHÙA BỘC', 26, BOLD, SOFT)
# shop block
d.rectangle([420, 420, 760, 800], outline=INK, width=5, fill=(244, 241, 232))
label((590, 540), 'TIỆM VÀNG PHÚC HƯNG', 22); label((590, 570), '(nhà ở phía trên, két trong nhà)', 16, ITAL, SOFT)
d.rectangle([450, 640, 730, 690], outline=INK, width=3); label((590, 665), 'Tủ kính bày vàng (nguyên vẹn)', 16, SANS)
d.rectangle([480, 794, 700, 806], fill=INK); label((590, 780), 'cửa sắt kéo (khoá)', 15, ITAL, SOFT)
# neighbour blocks
for x0, x1 in [(80, 380), (840, 1100)]:
    d.rectangle([x0, 420, x1, 800], outline=SOFT, width=3); label(((x0 + x1) / 2, 610), 'nhà dân', 18, ITAL, SOFT)
# side alley between shop and right neighbour
d.rectangle([760, 300, 840, 800], fill=ROAD, outline=SOFT); label((800, 720), 'NGÕ', 18, BOLD, SOFT); label((800, 744), 'bên hông', 15, ITAL, SOFT)
# back lane at the top
d.rectangle([0, 300, W, 380], fill=ROAD, outline=SOFT); label((300, 340), 'NGÕ SAU (ra phố bên)', 20, BOLD, SOFT)
# side door
d.rectangle([754, 600, 766, 660], fill=RED); label((700, 630), 'cửa ngách', 16, BOLD, RED, 'rm')
marker(805, 630, 1)
marker(812, 570, 2)
# shooter waiting spot and escape route
marker(800, 470, 3)
dashed([(800, 470), (800, 340), (1300, 340)])
label((1150, 312), 'hướng tẩu thoát (xe máy)', 16, ITAL, RED)
# car route & parking
d.rectangle([840, 820, 940, 860], outline=INK, width=3); label((890, 880), 'xe đỗ miệng ngõ 22:40', 14, ITAL)
dashed([(940, 840), (1250, 840)], INK, 3)
d.rectangle([1180, 420, 1360, 560], outline=INK, width=3); label((1270, 470), 'NHÀ GỬI XE', 18); label((1270, 496), '(ông Bảy)', 15, ITAL, SOFT)
label((1270, 590), '≈ 150 m từ cửa ngách', 15, ITAL, SOFT)
d.line([(1270, 610), (1270, 800)], fill=INK, width=2)
# legend
lx, ly = 60, 918
d.rectangle([lx - 10, ly - 10, lx + 600, ly + 90], outline=INK, width=2)
marker(lx + 10, ly + 10, 1); label((lx + 34, ly + 10), 'Tử thi trên bậc cửa ngách', 16, SANS, INK, 'lm')
marker(lx + 10, ly + 42, 2); label((lx + 34, ly + 42), 'Hai vỏ đạn (cách tử thi 2–3 m, phía trong ngõ)', 16, SANS, INK, 'lm')
marker(lx + 10, ly + 74, 3); label((lx + 34, ly + 74), 'Chỗ tay súng chờ; vệt lốp xe máy bánh nhỏ', 16, SANS, INK, 'lm')
nx, ny = 1330, 160
d.polygon([(nx, ny - 40), (nx - 14, ny + 10), (nx, ny), (nx + 14, ny + 10)], fill=INK); label((nx, ny - 58), 'N', 22)
im = im.filter(ImageFilter.GaussianBlur(0.35))
im.save('public/cases/dem-sung-no-tay-son/images/d04-so-do-hien-truong.webp', 'WEBP', quality=86, method=6)
print('ok')
