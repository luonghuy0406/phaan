"""Vẽ sơ đồ khoa Dược (d04). Chạy: python3 authoring/ly-tra-trao-doc/draw_so_do.py"""
from PIL import Image, ImageDraw, ImageFont
W, H = 1400, 910
F = '/System/Library/Fonts/Supplemental/'
def font(n, s): return ImageFont.truetype(F + n, s)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (32, 66, 128); SOFT = (110, 135, 175); RED = (190, 36, 40); GREY = (120, 120, 120)
im = Image.new('RGB', (W, H), (241, 244, 246)); d = ImageDraw.Draw(im)
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(205, 220, 236) if x % 125 else (175, 198, 224), width=1)
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(205, 220, 236) if y % 125 else (175, 198, 224), width=1)
def label(xy, t, s=20, f=BOLD, c=INK, a='mm'): d.text(xy, t, font=font(f, s), fill=c, anchor=a)
def box(x1, y1, x2, y2, w=4, c=INK): d.rectangle([x1, y1, x2, y2], outline=c, width=w)
label((40, 38), 'CÔNG AN THỊ XÃ HƯNG THÁI', 22, BOLD, INK, 'lm'); label((40, 66), 'Đội Cảnh sát hình sự', 19, SANS, INK, 'lm')
label((W / 2 + 90, 44), 'SƠ ĐỒ TẦNG 2 NHÀ C (KHOA DƯỢC) VÀ BÃI XE SAU', 28, BOLD)
label((W / 2 + 90, 80), 'Kèm biên bản 41/KNHT · 14 giờ 00 ngày 19/11/2016 · Không theo tỷ lệ', 20, ITAL)
# floor block
X1, Y1, X2, Y2 = 80, 130, 1320, 520
box(X1, Y1, X2, Y2, 6)
CY1, CY2 = 300, 350  # corridor
d.line([(X1, CY1), (X2, CY1)], fill=INK, width=3); d.line([(X1, CY2), (X2, CY2)], fill=INK, width=3)
label(((X1 + X2) / 2, 325), 'HÀNH LANG', 18, ITAL, SOFT)
rooms_top = [('Phòng trưởng khoa', 'DS. Phạm Đức Minh'), ('Phòng phó khoa', 'DS. Vũ Quốc Bảo'), ('PHÒNG GIAO BAN', 'tủ lạnh chung'), ('Kho cấp phát', '')]
w = (X2 - X1) / 4
for i, (a, b) in enumerate(rooms_top):
    x1 = X1 + i * w; x2 = x1 + w
    if i: d.line([(x1, Y1), (x1, CY1)], fill=INK, width=4)
    hot = i == 2
    if hot: box(x1 + 6, Y1 + 6, x2 - 6, CY1 - 6, 3, RED)
    label(((x1 + x2) / 2, 200), a, 20 if hot else 18, BOLD, RED if hot else INK); label(((x1 + x2) / 2, 228), b, 15, ITAL, RED if hot else INK)
fx = X1 + 2 * w + w - 70
box(fx, 245, fx + 40, 290, 3, RED); label((fx + 20, 267), 'TL', 13, BOLD, RED)
rooms_bot = [('Cầu thang', 'lên từ cửa nhà C'), ('Kho đông dược', 'chìa: trưởng, phó khoa'), ('Phòng pha chế', ''), ('WC', '')]
for i, (a, b) in enumerate(rooms_bot):
    x1 = X1 + i * w; x2 = x1 + w
    if i: d.line([(x1, CY2), (x1, Y2)], fill=INK, width=4)
    label(((x1 + x2) / 2, 420), a, 18); label(((x1 + x2) / 2, 446), b, 15, ITAL)
# stairs hatch
for k in range(6): d.line([(X1 + 20 + k * 14, CY2 + 20), (X1 + 20 + k * 14, Y2 - 20)], fill=SOFT, width=2)
# parking
PY1, PY2 = 600, 820
box(X1, PY1, X2, PY2, 3, GREY)
label((X1 + 10, PY1 - 18), 'BÃI XE PHÍA SAU NHÀ C (tầng trệt)', 18, BOLD, GREY, 'lm')
for k in range(10):
    x = X1 + 60 + k * 118; d.rectangle([x, PY1 + 30, x + 90, PY1 + 120], outline=SOFT, width=2)
label((X1 + 60 + 6 * 118 + 45, PY1 + 145), 'ô đỗ ô tô cán bộ', 14, ITAL, GREY)
d.line([(X1 + 30, PY2 - 40), (X1 + 360, PY2 - 40)], fill=GREY, width=2); label((X1 + 195, PY2 - 20), 'dải để xe máy', 14, ITAL, GREY)
label((X2, PY2 + 28), 'Cổng sau → phố Lê Lai (quán trà Mộc 300 m; quán cà phê Lá Me đối diện cổng)', 16, ITAL, INK, 'rm')
label((X1, PY2 + 28), '— Camera: cửa nhà C, bãi xe sau.', 16, ITAL, INK, 'lm')
label((W - 40, 880), 'Người vẽ: Đại uý Nguyễn Hải Đăng', 16, ITAL, INK, 'rm')
im.save('public/cases/ly-tra-trao-doc/images/d04-so-do-khoa-duoc.webp', 'WEBP', quality=86)
print('ok')
