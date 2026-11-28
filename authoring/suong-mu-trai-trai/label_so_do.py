"""Ghi chữ tiếng Việt lên nền sơ đồ vẽ tay (so-do-nen.webp, không chữ) → images/d03-so-do-trang-trai.webp.
Chạy: python3 authoring/suong-mu-trai-trai/label_so_do.py   (toạ độ theo ảnh nền gốc 876×879)"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

HERE = Path(__file__).resolve().parent
K = 1.6
F = '/System/Library/Fonts/Supplemental/'
INK, RED, PAPER = (34, 40, 62), (178, 30, 30), (238, 240, 242)
im = Image.open(HERE / 'so-do-nen.webp').convert('RGB')
im = im.resize((round(im.width * K), round(im.height * K)), Image.LANCZOS)
d = ImageDraw.Draw(im, 'RGBA')
def font(name, size): return ImageFont.truetype(F + name, round(size * K))


def tag(x, y, lines, size=15, col=INK, bold=True, box=True):
    """Nhãn nhiều dòng, tâm tại (x, y) theo toạ độ gốc, có nền giấy mờ cho dễ đọc."""
    fs = [font('Arial Bold.ttf' if (bold and i == 0) else 'Arial Italic.ttf', size if i == 0 else size - 3) for i in range(len(lines))]
    hs = [f.getbbox(t)[3] - f.getbbox(t)[1] for f, t in zip(fs, lines)]
    ws = [f.getlength(t) for f, t in zip(fs, lines)]
    W, H = max(ws), sum(hs) + (len(lines) - 1) * 6 * K
    cx, cy = x * K, y * K
    if box:
        d.rounded_rectangle([cx - W / 2 - 8 * K, cy - H / 2 - 6 * K, cx + W / 2 + 8 * K, cy + H / 2 + 6 * K], radius=4 * K, fill=PAPER + (225,), outline=col + (200,), width=max(1, round(1.2 * K)))
    yy = cy - H / 2
    for f, t, h in zip(fs, lines, hs):
        d.text((cx, yy + h / 2), t, font=f, fill=col, anchor='mm'); yy += h + 6 * K


def marker(x, y, n):
    r = 13 * K; d.ellipse([x * K - r, y * K - r, x * K + r, y * K + r], fill=PAPER + (235,), outline=RED, width=round(3 * K))
    d.text((x * K, y * K), str(n), font=font('Arial Bold.ttf', 15), fill=RED, anchor='mm')


# tiêu đề
tag(530, 42, ['SƠ ĐỒ TRANG TRẠI HOA LÂM VIÊN', 'Trại Mát, Đà Lạt · lập 8h00 ngày 15/12/2003 · tỷ lệ ước lượng'], size=20)
# công trình
tag(357, 285, ['VĂN PHÒNG'], 14)
tag(545, 285, ['LÒ SẤY HOA'], 14)
tag(390, 420, ['NHÀ KÍNH TRỒNG HỒNG'], 15)
tag(720, 318, ['KHO LẠNH SỐ 2'], 14)
tag(720, 365, ['buồng đệm'], 11, bold=False)
tag(720, 412, ['buồng lạnh sâu'], 11, bold=False)
tag(812, 372, ['CỔNG PHỤ'], 11)
tag(197, 528, ['CỔNG CHÍNH'], 13)
tag(268, 645, ['CHÒI BẢO VỆ'], 12)
tag(130, 690, ['← về trạm khí tượng Trại Mát', '(khoảng 1 km)'], 12)
# dấu vết
tag(628, 505, ['vệt xe rùa'], 12, col=RED)
marker(690, 572, 1)
tag(600, 640, ['DỐC RỪNG THÔNG', '(1) nơi phát hiện tử thi, cách cổng chính ~300 m'], 13, col=RED)
# tỷ lệ + dấu
for x, t in [(35, '0'), (175, '100'), (315, '200 m')]:
    d.text((x * K, 832 * K), t, font=font('Arial.ttf', 12), fill=INK, anchor='mm')
tag(175, 768, ['CÔNG AN TỈNH LÂM ĐỒNG', 'Phòng Kỹ thuật hình sự'], 12, col=RED)
out = HERE.parents[1] / 'public/cases/suong-mu-trai-trai/images/d03-so-do-trang-trai.webp'
im.save(out, 'WEBP', quality=86, method=6)
print('ok', im.size)
