"""Ghi chữ tiếng Việt lên nền sơ đồ vẽ tay nen/so-do-dinh.webp → images/d03-so-do-dinh.webp.
Chạy: python3 authoring/tieng-dan-day-pho-hien/label_so_do.py   (toạ độ theo ảnh nền gốc 498×501)"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

HERE = Path(__file__).resolve().parent
K = 2.8
F = '/System/Library/Fonts/Supplemental/'
INK, RED, GREEN, PAPER = (28, 48, 110), (175, 30, 30), (40, 100, 60), (244, 244, 240)
im = Image.open(HERE / 'nen' / 'so-do-dinh.webp').convert('RGB')
im = im.resize((round(im.width * K), round(im.height * K)), Image.LANCZOS)
d = ImageDraw.Draw(im, 'RGBA')
def font(name, size): return ImageFont.truetype(F + name, round(size * K))


def tag(x, y, lines, size=10, col=INK, first_bold=True):
    fs = [font('Arial Bold.ttf' if (first_bold and i == 0) else 'Arial.ttf', size if i == 0 else size - 1.5) for i in range(len(lines))]
    hs = [f.getbbox(t)[3] - f.getbbox(t)[1] for f, t in zip(fs, lines)]
    W = max(f.getlength(t) for f, t in zip(fs, lines)); H = sum(hs) + (len(lines) - 1) * 3 * K
    cx, cy = x * K, y * K
    d.rounded_rectangle([cx - W / 2 - 4 * K, cy - H / 2 - 3 * K, cx + W / 2 + 4 * K, cy + H / 2 + 3 * K], radius=2.5 * K,
                        fill=PAPER + (232,), outline=col + (200,), width=max(1, round(0.8 * K)))
    yy = cy - H / 2
    for f, t, h in zip(fs, lines, hs):
        d.text((cx, yy + h / 2), t, font=f, fill=col, anchor='mm'); yy += h + 3 * K


def marker(x, y, n):
    r = 7 * K
    d.ellipse([x * K - r, y * K - r, x * K + r, y * K + r], fill=PAPER + (240,), outline=RED, width=round(1.3 * K))
    d.text((x * K, y * K), str(n), font=font('Arial Bold.ttf', 9), fill=RED, anchor='mm')


tag(130, 30, ['SƠ ĐỒ ĐÌNH HOA NGUYỆT', 'đêm 30/9/1993 · không theo tỷ lệ'], 10.5)
tag(400, 30, ['HỒ BÁN NGUYỆT'], 10)
tag(247, 82, ['hậu cung'], 8, first_bold=False)
tag(248, 170, ['ĐẠI BÁI (chiếu diễn)'], 10)
tag(248, 272, ['TIỀN ĐÌNH · hương án'], 9)
tag(117, 262, ['BUỒNG', 'HOÁ TRANG'], 8.5)
tag(384, 262, ['PHÒNG', 'THỦ TỪ'], 8.5)
tag(150, 362, ['cửa sổ nhỏ'], 7.5, col=GREEN, first_bold=False)
tag(65, 395, ['quán nước bà Mùi'], 7.5, col=GREEN)
tag(247, 400, ['SÂN ĐÌNH'], 9)
tag(330, 478, ['CỔNG ĐÌNH'], 9)
marker(248, 228, 1); marker(105, 320, 2); marker(282, 300, 3)
tag(410, 405, ['GHI CHÚ', '(1) nơi nạn nhân ngã', '(2) tráp đàn trên án', '(3) hương án 19:30–20:00'], 8)
tag(438, 125, ['N'], 8)
tag(185, 488, ['CÔNG AN THỊ XÃ HƯNG YÊN'], 7, col=RED)
out = HERE.parents[1] / 'public/cases/tieng-dan-day-pho-hien/images/d03-so-do-dinh.webp'
im.save(out, 'WEBP', quality=86, method=6)
print('ok', im.size)
