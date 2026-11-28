"""Vẽ sơ đồ làng Đông Hồ (d04) cho bản 2. Chạy: python3 authoring/vet-muc-lang-dong-ho/draw_so_do.py"""
import math
from PIL import Image, ImageDraw, ImageFont
W, H = 1400, 900
F = '/System/Library/Fonts/Supplemental/'
def font(n, s): return ImageFont.truetype(F + n, s)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (32, 66, 128); SOFT = (110, 135, 175); RED = (190, 36, 40); GREEN = (64, 120, 72); EARTH = (176, 92, 54); WATER = (150, 190, 225)
im = Image.new('RGB', (W, H), (241, 244, 246)); d = ImageDraw.Draw(im)
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(205, 220, 236) if x % 125 else (175, 198, 224), width=1)
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(205, 220, 236) if y % 125 else (175, 198, 224), width=1)
def label(xy, t, s=20, f=BOLD, c=INK, a='mm'): d.text(xy, t, font=font(f, s), fill=c, anchor=a)
def box(x1, y1, x2, y2, w=4, c=INK): d.rectangle([x1, y1, x2, y2], outline=c, width=w)
def dashed(pts, col, w=3, dash=14, gap=9):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1); n = int(L // (dash + gap)) + 1
        for i in range(n):
            s = i * (dash + gap) / L; e = min(1, (i * (dash + gap) + dash) / L)
            d.line([(x1 + (x2 - x1) * s, y1 + (y2 - y1) * s), (x1 + (x2 - x1) * e, y1 + (y2 - y1) * e)], fill=col, width=w)
label((40, 38), 'CÔNG AN HUYỆN THUẬN THÀNH', 22, BOLD, INK, 'lm'); label((40, 66), 'Đội Cảnh sát điều tra', 19, SANS, INK, 'lm')
label((W / 2 + 100, 44), 'SƠ ĐỒ LÀNG ĐÔNG HỒ VÀ CÁC LỐI ĐI', 28, BOLD)
label((W / 2 + 100, 80), 'Kèm biên bản 07/KNHT · ngày 23/1/2001 (29 tháng Chạp) · Không theo tỷ lệ', 20, ITAL)
# river and dyke along the top
d.rectangle([0, 120, W, 190], fill=WATER); label((W / 2, 155), 'SÔNG ĐUỐNG', 24, BOLD, (40, 90, 150))
d.line([(0, 225), (W, 225)], fill=GREEN, width=8); label((60, 248), 'Đê sông Đuống (bờ đất bùn đỏ)', 16, ITAL, GREEN, 'lm')
# bridge to Đông Khê (right)
d.rectangle([1150, 120, 1190, 225], fill=(200, 200, 200), outline=INK, width=2); label((1240, 262), 'Cầu sang thôn Đông Khê →', 16, BOLD, INK)
# quán chè at the foot of the dyke
box(700, 240, 790, 290, 3, EARTH); label((745, 265), 'Quán chè', 15, BOLD, EARTH); label((745, 308), 'bà Tý', 14, ITAL, EARTH)
# đình + sân đình (left)
box(140, 420, 360, 540); label((250, 465), 'ĐÌNH LÀNG', 22); label((250, 495), 'sân đình: chiếu phim', 15, ITAL)
label((250, 518), '(nghỉ 20:15–20:45)', 15, ITAL, RED)
# nhà văn hoá
box(430, 600, 600, 680); label((515, 630), 'Nhà văn hoá thôn', 16); label((515, 655), '(họp hội xuân 19:30–21:30)', 13, ITAL)
# xóm Đông: xưởng tranh cụ Thao (right-middle)
box(880, 400, 1100, 540, 4, RED); label((990, 440), 'XƯỞNG TRANH', 22, BOLD, RED); label((990, 470), 'cụ Vũ Đình Thao', 16, ITAL, RED)
box(1110, 420, 1200, 520, 3); label((1155, 470), 'nhà ở', 14, ITAL)
box(880, 550, 1100, 610, 2, SOFT); label((990, 580), 'sân phơi giấy điệp', 14, ITAL, SOFT)
label((1110, 385), 'XÓM ĐÔNG', 18, BOLD, SOFT, 'lm')
# xóm Ngoài far bottom-left
label((150, 800), 'Xóm Ngoài (đám cưới) cách xưởng ~1,5 km về phía tây nam', 16, ITAL, INK, 'lm')
# roads
d.line([(360, 480), (880, 470)], fill=(160, 160, 160), width=6); label((620, 455), 'đường làng ~500 m', 14, ITAL, (110, 110, 110))
# paths: đình -> quán chè (Khiêm), ngõ xưởng -> đê -> cầu
dashed([(300, 420), (520, 300), (700, 270)], EARTH, 3)
label((600, 340), 'lối ra chân đê', 14, ITAL, EARTH)
dashed([(990, 400), (960, 300), (1000, 228), (1150, 215)], RED, 3)
label((1000, 320), 'ngõ xưởng → đê → cầu', 14, BOLD, RED, 'lm')
# north arrow & notes
nx, ny = 1330, 820; d.polygon([(nx, ny - 40), (nx - 14, ny + 10), (nx, ny), (nx + 14, ny + 10)], fill=INK); label((nx, ny - 58), 'B', 22)
label((40, 860), '— Cửa xưởng cài then gỗ phía ngoài, không khoá. Bà Đỗ Thị Hoa ở sát xưởng nghe tiếng đập khoảng 20:30.', 16, ITAL, INK, 'lm')
im.save('public/cases/vet-muc-lang-dong-ho/images/d04-so-do-lang-tranh.webp', 'WEBP', quality=86)
print('ok')
