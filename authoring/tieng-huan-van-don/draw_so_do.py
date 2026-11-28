"""Vẽ sơ đồ tàu QN-9288-TS (images/d04-so-do-tau-ca.webp) cho bản 2. Chạy: python3 authoring/tieng-huan-van-don/draw_so_do.py"""
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(7)
W, H = 1400, 1000
F = '/System/Library/Fonts/Supplemental/'
def font(name, size): return ImageFont.truetype(F + name, size)
SANS, BOLD, ITAL = 'Arial.ttf', 'Arial Bold.ttf', 'Arial Italic.ttf'
INK = (30, 50, 90); SOFT = (110, 125, 155); RED = (185, 35, 35); BLUE = (60, 110, 170)

im = Image.new('RGB', (W, H), (243, 241, 233)); d = ImageDraw.Draw(im)
for x in range(0, W, 25): d.line([(x, 0), (x, H)], fill=(222, 225, 226) if x % 125 else (204, 210, 216))
for y in range(0, H, 25): d.line([(0, y), (W, y)], fill=(222, 225, 226) if y % 125 else (204, 210, 216))


def label(xy, text, size=20, f=BOLD, col=INK, anchor='mm'):
    d.text(xy, text, font=font(f, size), fill=col, anchor=anchor)


def marker(x, y, n):
    d.ellipse([x - 15, y - 15, x + 15, y + 15], outline=RED, width=3); label((x, y), str(n), 17, BOLD, RED)


label((40, 40), 'CÔNG AN TỈNH QUẢNG NINH', 22, BOLD, INK, 'lm'); label((40, 68), 'Phòng Cảnh sát hình sự', 20, SANS, INK, 'lm')
label((W / 2 + 90, 44), 'SƠ ĐỒ TÀU CÁ QN-9288-TS', 30); label((W / 2 + 90, 80), 'Lập 07h15 ngày 14/11/2006 tại cầu cảng số 2, cảng Cái Rồng', 20, ITAL)

# ── side section (top) ──
label((60, 140), 'MẶT CẮT DỌC', 20, BOLD, INK, 'lm')
deck_y, keel_y, X0, X1 = 260, 400, 140, 1260
hull = [(X0, deck_y), (X1, deck_y - 30), (X1 - 160, keel_y), (X0 + 60, keel_y), (X0, deck_y + 60)]
d.polygon(hull, outline=INK, width=4)
d.line([(X0, deck_y), (X1, deck_y - 30)], fill=INK, width=4)
label((X0 - 10, deck_y + 30), 'LÁI', 16, BOLD, INK, 'rm'); label((X1 + 10, deck_y - 30), 'MŨI', 16, BOLD, INK, 'lm')
# wheelhouse
d.rectangle([330, 170, 500, deck_y - 4], outline=INK, width=3); label((415, 212), 'BUỒNG LÁI', 16)
# compartments under deck (from stern to bow): engine room, kitchen above, tuna hold, hold 3, hold 2, hold 1
secs = [(170, 330, 'BUỒNG MÁY'), (330, 440, 'HẦM CÁ NGỪ\n(đá khô)'), (440, 640, 'KHOANG 3'), (640, 880, 'KHOANG 2'), (880, 1060, 'KHOANG 1')]
for a, b, t in secs:
    d.line([(b, deck_y - (b - X0) * 30 / (X1 - X0)), (b, keel_y - 6)], fill=INK, width=3)
    yy = (deck_y + keel_y) / 2 + 8
    for k, line in enumerate(t.split('\n')): label(((a + b) / 2, yy + k * 22 - (len(t.split('\n')) - 1) * 11), line, 14 if b - a < 150 else 16)
# ladder in hold 3
for k in range(6): d.line([(470, 280 + k * 18), (494, 280 + k * 18)], fill=SOFT, width=2)
d.line([(470, 270), (470, 380)], fill=SOFT, width=2); d.line([(494, 270), (494, 380)], fill=SOFT, width=2)
marker(530, 365, 1)
# vent pipe from hold 3
d.line([(600, 300), (600, 190)], fill=BLUE, width=5); d.line([(586, 190), (614, 190)], fill=BLUE, width=6)
label((620, 175), 'ống xả quạt hút khoang 3', 15, ITAL, BLUE, 'lm')
label((505, 300), 'sâu 2,2 m', 14, ITAL, SOFT, 'lm')

# ── deck plan (bottom) ──
label((60, 470), 'MẶT BOONG', 20, BOLD, INK, 'lm')
T, B = 540, 860
d.polygon([(X0, T + 30), (X1 - 140, T), (X1, (T + B) / 2), (X1 - 140, B), (X0, B - 30)], outline=INK, width=4)
label((X0 - 10, (T + B) / 2), 'LÁI', 16, BOLD, INK, 'rm'); label((X1 + 10, (T + B) / 2), 'MŨI', 16, BOLD, INK, 'lm')
# kitchen + wheelhouse block
d.rectangle([330, 600, 500, 800], outline=INK, width=3); label((415, 660), 'BUỒNG LÁI', 17); label((415, 690), '(tầng trên)', 15, ITAL)
label((415, 740), 'BẾP · phòng ngủ', 16); label((415, 764), 'thuyền viên (dưới)', 15, ITAL)
# engine-room hatch
d.rectangle([250, 650, 300, 700], outline=INK, width=3); label((275, 720), 'cửa sập', 15, SANS); label((275, 740), 'buồng máy', 15, SANS)
# hold hatches
for a, b, t in [(540, 620, 'Nắp\nkhoang 3'), (720, 800, 'Nắp\nkhoang 2'), (960, 1040, 'Nắp\nkhoang 1')]:
    d.rectangle([a, 660, b, 740], outline=INK, width=3)
    for k, line in enumerate(t.split('\n')): label(((a + b) / 2, 690 + k * 22), line, 15)
marker(580, 640, 2)
d.ellipse([600, 735, 616, 751], fill=BLUE); label((630, 760), 'ống xả', 14, ITAL, BLUE, 'lm')
marker(1180, 700, 3)
# distances
d.line([(300, 880), (540, 880)], fill=SOFT, width=2); d.line([(300, 870), (300, 890)], fill=SOFT, width=2); d.line([(540, 870), (540, 890)], fill=SOFT, width=2)
label((420, 900), 'cửa sập buồng máy → nắp khoang 3: khoảng 3 m', 15, ITAL, SOFT)
label((800, 600), 'tầm nhìn từ buồng lái: về phía mũi', 15, ITAL, SOFT)
d.line([(500, 615), (1100, 615)], fill=SOFT, width=1)

# legend
lx, ly = 900, 905
d.rectangle([lx - 10, ly - 18, lx + 470, ly + 80], outline=INK, width=2)
marker(lx + 10, ly + 6, 1); label((lx + 32, ly + 6), 'Tử thi dưới chân thang khoang 3', 16, SANS, INK, 'lm')
marker(lx + 10, ly + 36, 2); label((lx + 32, ly + 36), 'Then sắt nắp khoang 3 (gài từ boong)', 16, SANS, INK, 'lm')
marker(lx + 10, ly + 66, 3); label((lx + 32, ly + 66), 'Mũi tàu (chỗ có người hút thuốc)', 16, SANS, INK, 'lm')

im = im.filter(ImageFilter.GaussianBlur(0.35))
im.save('public/cases/tieng-huan-van-don/images/d04-so-do-tau-ca.webp', 'WEBP', quality=86, method=6)
print('ok')
