"""Vẽ sơ đồ d04 (ảnh images/d03-so-do-buon-lang.webp) cho bản 2. Chạy: python3 authoring/lua-than-tay-nguyen/draw_so_do.py"""
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(4)
W, H = 1400, 1000
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (32, 66, 128); SOFT = (100, 125, 170); RED = (190, 36, 40); GREEN = (64, 120, 72); EARTH = (176, 92, 54); WATER = (70, 130, 190)

im = Image.new('RGB', (W, H), (241, 244, 246)); d = ImageDraw.Draw(im)
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(205, 220, 236) if x % 125 else (175, 198, 224))
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(205, 220, 236) if y % 125 else (175, 198, 224))


def label(xy, text, size=22, f=BOLD, col=INK, anchor='mm'):
    d.text(xy, text, font=font(f, size), fill=col, anchor=anchor)


def dashed(a, b, col=INK, w=3, dash=14, gap=9):
    (x1, y1), (x2, y2) = a, b; L = math.hypot(x2 - x1, y2 - y1); n = int(L // (dash + gap)) + 1
    for i in range(n):
        s = i * (dash + gap) / L; e = min(1, (i * (dash + gap) + dash) / L)
        d.line([(x1 + (x2 - x1) * s, y1 + (y2 - y1) * s), (x1 + (x2 - x1) * e, y1 + (y2 - y1) * e)], fill=col, width=w)


def marker(x, y, n):
    d.ellipse([x - 15, y - 15, x + 15, y + 15], outline=RED, width=3); label((x, y), str(n), 18, BOLD, RED)


def tree(x, y, r=12):
    d.ellipse([x - r, y - r, x + r, y + r], outline=GREEN, width=2)


label((40, 40), 'CÔNG AN TỈNH ĐẮK LẮK', 22, BOLD, INK, 'lm'); label((40, 68), 'Phòng Cảnh sát hình sự', 20, SANS, INK, 'lm')
label((W / 2 + 80, 44), 'SƠ ĐỒ TRUNG TÂM BUÔN EA KRAL ĐÊM 8/4/2001', 30, BOLD)
label((W / 2 + 80, 80), 'Lập 07h00 ngày 9/4/2001 · khoảng cách đo bằng thước dây', 20, ITAL)

# stream + water wharf on the west
pts = [(150 + 40 * math.sin(y / 90), y) for y in range(120, H, 10)]
d.line(pts, fill=WATER, width=6); d.line([(x + 26, y) for x, y in pts], fill=WATER, width=3)
label((95, 330), 'suối', 18, ITAL, WATER)
bx, by = 260, 790
d.rectangle([bx - 30, by - 22, bx + 50, by + 22], outline=WATER, width=3)
label((bx + 10, by + 46), 'BẾN NƯỚC', 20, BOLD, WATER); label((bx + 10, by + 70), '(dọn lễ, 6 phụ nữ)', 16, ITAL, WATER)

# longhouse of the village elder
L0, L1, T0, T1 = 360, 820, 440, 530
d.rectangle([L0, T0, L1, T1], outline=INK, width=5)
label(((L0 + L1) / 2, (T0 + T1) / 2 - 12), 'NHÀ DÀI CỦA GIÀ LÀNG', 24); label(((L0 + L1) / 2, (T0 + T1) / 2 + 16), '(lễ, chiếu khách, chiêng)', 17, ITAL)
d.rectangle([L1 - 70, T0 - 6, L1 - 30, T0 + 6], fill=(241, 244, 246)); label((L1 - 50, T0 - 20), 'cửa sau', 16, ITAL)
d.rectangle([L0 + 40, T1 - 6, L0 + 110, T1 + 6], fill=(241, 244, 246)); label((L0 + 75, T1 + 22), 'cầu thang trước', 16, ITAL)
# ceremonial pole yard
px, py = 590, 640
d.line([(px, py - 50), (px, py + 10)], fill=INK, width=4); d.line([(px - 20, py - 40), (px + 20, py - 40)], fill=INK, width=2)
label((px, py + 32), 'Cây nêu (dựng chiều 8/4)', 17, SANS)

# power pole and wire to the granary
cx, cy = 860, 470
d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=INK); label((cx + 14, cy + 26), 'Cột điện', 16, SANS, INK, 'lm')
K0, K1, KT0, KT1 = 930, 1080, 190, 300
dashed((cx, cy), (K0 + 10, KT0 + 12), INK, 3)
# granary on stilts
d.rectangle([K0, KT0, K1, KT1], outline=INK, width=5)
for x in (K0 + 12, K1 - 12):
    d.line([(x, KT1), (x, KT1 + 14)], fill=INK, width=4)
d.line([(K0 + 30, KT0 + 30), (K1 - 30, KT1 - 30)], fill=SOFT, width=1); d.line([(K1 - 30, KT0 + 30), (K0 + 30, KT1 - 30)], fill=SOFT, width=1)
label(((K0 + K1) / 2, KT0 - 46), 'KHO LÚA CHUNG', 24); label(((K0 + K1) / 2, KT0 - 20), '(nhà sàn, cháy)', 17, ITAL)
d.rectangle([K1 - 60, KT1 - 6, K1 - 20, KT1 + 6], fill=(241, 244, 246))
d.ellipse([K1 - 8, KT1 + 16, K1 + 4, KT1 + 28], fill=INK); label((K1 + 12, KT1 + 22), 'công tắc (cột ngoài cửa)', 15, SANS, INK, 'lm')
d.ellipse([K0 + 6, KT0 + 6, K0 + 20, KT0 + 20], outline=INK, width=2)
marker(K0 + 30, KT0 + 34, 2)
marker(K1 - 34, KT1 - 30, 1)
dashed((L1 - 50, T0 - 30), (K0 + 40, KT1 + 20), SOFT, 2, 8, 8)
label((790, 375), '≈ 80 m', 18, BOLD, SOFT)

# pickup truck
tx, ty = 1150, 330
d.rectangle([tx, ty, tx + 110, ty + 50], outline=INK, width=3); d.rectangle([tx + 70, ty + 6, tx + 104, ty + 44], outline=INK, width=2)
label((tx + 55, ty + 72), 'Xe bán tải (ông Lợi)', 17, BOLD); label((tx + 55, ty + 94), 'đỗ từ 17:30', 16, ITAL)

# Y Bang's workshop
wx0, wy0 = 980, 640
d.rectangle([wx0, wy0, wx0 + 200, wy0 + 80], outline=INK, width=4)
label((wx0 + 100, wy0 + 28), 'XƯỞNG SỬA MÁY', 18); label((wx0 + 100, wy0 + 54), '(Y Bang)', 17, ITAL)

# red dirt road to the town
d.line([(820, 900), (1000, 830), (1200, 800), (1390, 790)], fill=EARTH, width=10)
d.line([(700, 560), (760, 760), (820, 900)], fill=EARTH, width=6)
label((1210, 840), '→ Thị trấn Quảng Phú (12 km)', 20, BOLD, EARTH)
d.line([(760, 760), (980, 690)], fill=EARTH, width=4)

# houses and trees around
for x, y in [(300, 250), (480, 230), (650, 250), (330, 640), (420, 860), (620, 870)]:
    d.rectangle([x - 40, y - 18, x + 40, y + 18], outline=SOFT, width=2)
label((480, 200), 'nhà dài các hộ', 15, ITAL, SOFT)
for x, y in [(840, 140), (880, 110), (1180, 160), (1230, 210), (1270, 470), (300, 360), (260, 580), (720, 960)]:
    tree(x, y)

# legend
lx, ly = 1110, 540
d.rectangle([lx - 8, ly - 30, lx + 280, ly + 92], outline=INK, width=2)
label((lx + 4, ly - 12), 'GHI CHÚ', 18, BOLD, INK, 'lm')
marker(lx + 14, ly + 16, 1); label((lx + 38, ly + 16), 'Tử thi (góc đông nam)', 16, SANS, INK, 'lm')
marker(lx + 14, ly + 46, 2); label((lx + 38, ly + 46), 'Điểm phát cháy', 16, SANS, INK, 'lm')
dashed((lx + 2, ly + 76), (lx + 28, ly + 76), INK, 3, 8, 5); label((lx + 38, ly + 76), 'Dây điện tự kéo (1999)', 16, SANS, INK, 'lm')

nx, ny = 1330, 110
d.polygon([(nx, ny - 40), (nx - 14, ny + 10), (nx, ny), (nx + 14, ny + 10)], fill=INK); label((nx, ny - 58), 'N', 22)

im = im.filter(ImageFilter.GaussianBlur(0.35))
im.save('public/cases/lua-than-tay-nguyen/images/d03-so-do-buon-lang.webp', 'WEBP', quality=86, method=6)
print('ok')
