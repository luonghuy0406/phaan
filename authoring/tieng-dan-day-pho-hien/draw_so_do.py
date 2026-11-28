"""Vẽ sơ đồ đình Hoa Nguyệt (images/d03-so-do-dinh.webp). Chạy: python3 authoring/tieng-dan-day-pho-hien/draw_so_do.py"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

W, H = 1400, 1000
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (32, 58, 120); SOFT = (110, 130, 170); RED = (185, 35, 35); WATER = (90, 140, 200); GREEN = (70, 120, 80)
im = Image.new('RGB', (W, H), (238, 243, 248)); d = ImageDraw.Draw(im)
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(212, 224, 238) if x % 125 else (186, 204, 228))
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(212, 224, 238) if y % 125 else (186, 204, 228))
def label(xy, t, s=20, f=BOLD, c=INK, a='mm'): d.text(xy, t, font=font(f, s), fill=c, anchor=a)
def marker(x, y, n):
    d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(250, 250, 250), outline=RED, width=3); label((x, y), str(n), 18, BOLD, RED)

label((40, 40), 'CÔNG AN THỊ XÃ HƯNG YÊN', 22, BOLD, INK, 'lm'); label((40, 68), 'Đội Cảnh sát hình sự', 20, SANS, INK, 'lm')
label((W / 2 + 120, 44), 'SƠ ĐỒ ĐÌNH HOA NGUYỆT ĐÊM 30/9/1993', 30)
label((W / 2 + 120, 80), 'Lập 22h00 ngày 30/9/1993 · không theo tỷ lệ', 19, ITAL)
# lake (north)
d.rectangle([0, 110, W, 200], fill=(205, 222, 240))
for k in range(6): d.arc([100 + k * 220, 130, 220 + k * 220, 170], 200, 340, fill=WATER, width=2)
label((W / 2, 160), 'HỒ BÁN NGUYỆT', 24, BOLD, WATER)
# temple building
X0, X1, Y0, Y1 = 330, 1070, 260, 760
d.rectangle([X0, Y0, X1, Y1], outline=INK, width=6)
for x in range(X0 + 80, X1, 120):
    for y in (Y0 + 40, 520): d.rectangle([x - 8, y - 8, x + 8, y + 8], fill=INK)
d.rectangle([640, Y0 - 50, 760, Y0], outline=INK, width=4); label((700, Y0 - 25), 'hậu cung', 16, ITAL)
# đại bái (inner) and tiền đình (front)
d.line([(X0, 560), (X1, 560)], fill=INK, width=4)
d.rectangle([600, 380, 800, 480], outline=SOFT, width=2); label((700, 400), 'chiếu hoa', 17, ITAL, SOFT)
label((700, 330), 'ĐẠI BÁI (chiếu diễn)', 22)
label((780, 640), 'TIỀN ĐÌNH', 22); label((780, 668), '(hương án, chiếu khách)', 16, ITAL)
d.rectangle([640, 690, 760, 730], outline=SOFT, width=2); label((700, 710), 'hương án', 14, ITAL, SOFT)
# dressing room (SW corner) with door to đại bái and window to gate
d.rectangle([X0, 470, 520, Y1], outline=INK, width=5, fill=(246, 240, 230))
label((425, 590), 'BUỒNG', 20); label((425, 616), 'HOÁ TRANG', 20)
d.rectangle([380, 650, 470, 690], outline=SOFT, width=2); label((425, 670), 'án, tráp đàn', 13, ITAL, SOFT)
d.line([(520, 500), (520, 540)], fill=(246, 240, 230), width=8); label((560, 520), 'cửa', 14, ITAL, SOFT, 'lm')
d.line([(380, Y1), (440, Y1)], fill=(238, 243, 248), width=8); d.line([(380, Y1 - 4), (440, Y1 - 4)], fill=INK, width=2); d.line([(380, Y1 + 4), (440, Y1 + 4)], fill=INK, width=2)
label((410, Y1 + 24), 'cửa sổ nhỏ', 14, ITAL)
# keeper's room (SE corner)
d.rectangle([900, 600, X1, Y1], outline=INK, width=4); label((985, 690), 'phòng thủ từ', 16, BOLD)
# front steps, yard, gate, tea stall
d.rectangle([640, Y1, 760, Y1 + 30], outline=INK, width=3)
label((700, 820), 'SÂN ĐÌNH', 22, BOLD, SOFT)
d.rectangle([250, 900, 1150, 916], fill=INK); d.rectangle([620, 896, 780, 920], fill=(238, 243, 248)); label((700, 940), 'CỔNG ĐÌNH', 18)
d.rectangle([380, 930, 520, 980], outline=GREEN, width=3); label((450, 955), 'quán nước bà Mùi', 14, BOLD, GREEN)
# sightline
for i in range(14):
    t0 = i / 14; t1 = t0 + 0.035
    d.line([(450 + (410 - 450) * t0, 930 + (Y1 - 930) * t0), (450 + (410 - 450) * t1, 930 + (Y1 - 930) * t1)], fill=GREEN, width=3)
label((300, 860), 'tầm nhìn từ quán', 14, ITAL, GREEN)
# markers
marker(700, 448, 1); marker(425, 718, 2); marker(800, 710, 3)
lx, ly = 1100, 300
d.rectangle([lx - 10, ly - 20, lx + 280, ly + 110], outline=INK, width=2, fill=(246, 248, 252))
label((lx + 4, ly), 'GHI CHÚ', 18, BOLD, INK, 'lm')
marker(lx + 14, ly + 32, 1); label((lx + 38, ly + 32), 'Nơi nạn nhân ngã', 15, SANS, INK, 'lm')
marker(lx + 14, ly + 64, 2); label((lx + 38, ly + 64), 'Tráp đàn trên án', 15, SANS, INK, 'lm')
marker(lx + 14, ly + 96, 3); label((lx + 38, ly + 96), 'Hương án (19:30–20:00)', 15, SANS, INK, 'lm')
nx, ny = 1330, 260
d.polygon([(nx, ny - 40), (nx - 14, ny + 10), (nx, ny), (nx + 14, ny + 10)], fill=INK); label((nx, ny - 58), 'N', 22)
im = im.filter(ImageFilter.GaussianBlur(0.35))
im.save('public/cases/tieng-dan-day-pho-hien/images/d03-so-do-dinh.webp', 'WEBP', quality=86, method=6)
print('ok')
