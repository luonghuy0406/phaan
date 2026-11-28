"""Vẽ sơ đồ toa 6 tàu SE3 (d03) theo biên bản d02, d08. Chạy: python3 authoring/chuyen-tau-dem-muong-man/draw_so_do.py"""
import random
from PIL import Image, ImageDraw, ImageFont

random.seed(6)
W, H = 1400, 760
F = '/System/Library/Fonts/Supplemental/'
def font(n, s): return ImageFont.truetype(F + n, s)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (32, 66, 128); SOFT = (110, 135, 175); RED = (190, 36, 40); GREY = (120, 120, 120)
im = Image.new('RGB', (W, H), (241, 244, 246)); d = ImageDraw.Draw(im)
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(205, 220, 236) if x % 125 else (175, 198, 224), width=1)
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(205, 220, 236) if y % 125 else (175, 198, 224), width=1)
def label(xy, t, s=20, f=BOLD, c=INK, a='mm'): d.text(xy, t, font=font(f, s), fill=c, anchor=a)
def box(x1, y1, x2, y2, w=3, c=INK): d.rectangle([x1, y1, x2, y2], outline=c, width=w)

label((40, 38), 'CÔNG AN TỈNH BÌNH THUẬN', 22, BOLD, INK, 'lm'); label((40, 66), 'Phòng Cảnh sát hình sự', 19, SANS, INK, 'lm')
label((W / 2 + 90, 44), 'SƠ ĐỒ TOA 6 TÀU SE3 (GIƯỜNG NẰM KHOANG 4 ĐIỀU HOÀ)', 28, BOLD)
label((W / 2 + 90, 80), 'Kèm biên bản 112/KNHT · 06 giờ 15 ngày 13/10/2008 · Không theo tỷ lệ', 20, ITAL)

X1, X2, Y1, Y2 = 60, 1340, 170, 520   # car body
d.rounded_rectangle([X1, Y1, X2, Y2], 28, outline=INK, width=6)
CY = 430  # corridor line (corridor below the compartments)
d.line([(X1 + 170, CY), (X2 - 170, CY)], fill=INK, width=3)
label(((X1 + X2) / 2, 478), 'HÀNH LANG  →  hướng chạy của tàu (vào Nam)', 20, ITAL, SOFT)
# head end: staff room + WC
box(X1 + 10, Y1 + 10, X1 + 170, CY - 2, 4); label((X1 + 90, 250), 'Buồng', 18); label((X1 + 90, 274), 'nhân viên', 18); label((X1 + 90, 300), '(tủ đồ)', 15, ITAL)
box(X1 + 10, CY + 6, X1 + 110, Y2 - 10, 3); label((X1 + 60, 470), 'WC', 16)
label((X1 + 30, Y2 + 28), '← Toa 5', 18, BOLD, INK, 'lm')
# compartments 1..7
cw = (X2 - 170 - (X1 + 170)) / 7
names = ['Gia đình', '1 khách + 3', 'Bà Sen', 'G01 · G02', '4 sinh viên', 'trống', '2 cán bộ']
subs = ['Lương Văn Toàn', 'công nhân', 'và cháu', '(G03, G04 trống)', '', '', 'ngân hàng']
for i in range(7):
    x1 = X1 + 170 + i * cw; x2 = x1 + cw
    box(x1, Y1 + 10, x2, CY - 2, 4, RED if i == 3 else INK)
    label(((x1 + x2) / 2, 210), f'KHOANG {i + 1}', 20, BOLD, RED if i == 3 else INK)
    label(((x1 + x2) / 2, 262), names[i], 16, SANS); label(((x1 + x2) / 2, 286), subs[i], 14, ITAL)
    # door (sliding) on the corridor side
    dx = x1 + cw * 0.62
    d.line([(dx, CY - 2), (dx + cw * 0.28, CY - 2)], fill=(241, 244, 246), width=7)
    d.line([(dx, CY + 6), (dx + cw * 0.28, CY + 6)], fill=SOFT, width=3)
label((X1 + 170 + 3.5 * cw, 355), 'hiện trường', 16, BOLD, RED); label((X1 + 170 + 3.5 * cw, 378), 'cửa trượt: ổ khoá', 13, ITAL, RED); label((X1 + 170 + 3.5 * cw, 396), '+ lẫy gập mặt trong', 13, ITAL, RED)
# tail end: WC + technical AC hatch
bx = X2 - 170
box(bx + 2, Y1 + 10, X2 - 10, CY - 2, 4); label((bx + 85, 240), 'Nhà vệ sinh', 17); label((bx + 85, 264), '(thùng rác)', 14, ITAL)
box(bx + 20, CY + 6, X2 - 10, Y2 - 10, 3); label((bx + 95, 462), 'Ngăn kỹ thuật', 14); label((bx + 95, 482), 'điều hoà', 14)
label((X2 - 30, Y2 + 28), 'Toa 7 →', 18, BOLD, INK, 'rm')
# notes
notes = ['Cửa lên xuống ở hai đầu toa khoá suốt hành trình 00:41–05:30.', 'Ngăn kỹ thuật điều hoà mở bằng chìa vuông chuyên dụng.',
         'Toa căng-tin là toa 9 (đi qua toa 7, 8).']
for k, t in enumerate(notes): label((60, 590 + k * 30), '— ' + t, 18, ITAL, INK, 'lm')
label((W - 60, 700), 'Người vẽ: Thiếu tá Phan Đình Quân', 17, ITAL, INK, 'rm')
im.save('public/cases/chuyen-tau-dem-muong-man/images/d03-so-do-toa-tau.webp', 'WEBP', quality=86)
print('ok')
