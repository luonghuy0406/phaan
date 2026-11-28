"""Ghi chữ tiếng Việt lên các ảnh nền không chữ trong nen/ → public/cases/mua-dong-binh-ty/images/.
Chạy: python3 authoring/mua-dong-binh-ty/label_images.py   (toạ độ theo ảnh nền ~503 px)"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / 'public/cases/mua-dong-binh-ty/images'
K = 2.4
F = '/System/Library/Fonts/Supplemental/'
INK, RED, BLUE, PAPER = (30, 38, 70), (170, 28, 28), (30, 52, 120), (246, 240, 226)


def font(name, size): return ImageFont.truetype(F + name, round(size * K))


class Canvas:
    def __init__(self, name):
        im = Image.open(HERE / 'nen' / f'{name}.webp').convert('RGB')
        self.im = im.resize((round(im.width * K), round(im.height * K)), Image.LANCZOS)
        self.d = ImageDraw.Draw(self.im, 'RGBA')

    def text(self, x, y, t, size=12, f='Arial Bold.ttf', col=INK, anchor='mm'):
        self.d.text((x * K, y * K), t, font=font(f, size), fill=col, anchor=anchor)

    def tag(self, x, y, lines, size=12, col=INK, box=True, first_bold=True):
        fs = [font('Arial Bold.ttf' if (first_bold and i == 0) else 'Arial.ttf', size if i == 0 else size - 1.5) for i in range(len(lines))]
        hs = [f.getbbox(t)[3] - f.getbbox(t)[1] for f, t in zip(fs, lines)]
        W = max(f.getlength(t) for f, t in zip(fs, lines)); H = sum(hs) + (len(lines) - 1) * 4 * K
        cx, cy = x * K, y * K
        if box:
            self.d.rounded_rectangle([cx - W / 2 - 5 * K, cy - H / 2 - 4 * K, cx + W / 2 + 5 * K, cy + H / 2 + 4 * K], radius=3 * K,
                                     fill=PAPER + (230,), outline=col + (190,), width=max(1, round(K)))
        yy = cy - H / 2
        for f, t, h in zip(fs, lines, hs):
            self.d.text((cx, yy + h / 2), t, font=f, fill=col, anchor='mm'); yy += h + 4 * K

    def line(self, a, b, col=RED, w=1.2):
        self.d.line([(a[0] * K, a[1] * K), (b[0] * K, b[1] * K)], fill=col, width=max(1, round(w * K)))

    def marker(self, x, y, n, col=RED):
        r = 9 * K
        self.d.ellipse([x * K - r, y * K - r, x * K + r, y * K + r], fill=PAPER + (235,), outline=col, width=round(1.6 * K))
        self.text(x, y, str(n), 11, col=col)

    def save(self, name):
        self.im.save(OUT / f'{name}.webp', 'WEBP', quality=86, method=6)
        print('ok', name, self.im.size)


# ── sơ đồ căn hộ 204 ──
c = Canvas('so-do-can-ho')
c.tag(150, 78, ['HÀNH LANG CHUNG (tầng 2)'], 10, col=BLUE)
c.tag(430, 30, ['Cửa sổ bị bẻ chốt từ bên trong', 'mảnh kính văng ra hành lang'], 8.5, col=RED)
c.line((372, 40), (350, 70))
c.tag(112, 132, ['cửa ra vào'], 8, col=BLUE, first_bold=False)
c.tag(182, 190, ['PHÒNG KHÁCH'], 10, col=BLUE)
c.tag(335, 165, ['PHÒNG NGỦ'], 10, col=BLUE)
c.tag(88, 283, ['kệ thuốc'], 8, col=BLUE, first_bold=False)
c.tag(215, 406, ['góc bếp'], 8, col=BLUE, first_bold=False)
c.marker(156, 334, 1); c.marker(268, 250, 2); c.marker(404, 404, 3)
c.text(250, 455, 'SƠ ĐỒ HIỆN TRƯỜNG CĂN HỘ 204 – NHÀ A6', 13, col=BLUE)
c.text(250, 473, '(1) vị trí nạn nhân · (2) bàn trà, ấm tích · (3) hộp bánh quy dưới gầm giường', 8.5, 'Arial.ttf', col=INK)
c.text(250, 489, 'Công an quận Hai Bà Trưng · Đội Điều tra hình sự · lập 8h30 ngày 18/2/1996', 8, 'Arial Italic.ttf', col=INK)
c.save('d02-so-do-can-ho')

# ── sơ đồ giải phẫu (kết luận pháp y) ──
c = Canvas('giai-phau')
c.text(250, 18, 'SƠ ĐỒ GIẢI PHẪU ĐƯỜNG HÔ HẤP', 13, col=INK)
c.tag(420, 82, ['KẾT LUẬN', 'Sốc phản vệ do dị ứng', 'protein hạt điều', 'Không phát hiện chất độc'], 9.5, col=RED)
c.tag(70, 330, ['Phù nề', 'thanh quản cấp'], 9, col=RED)
c.line((95, 315), (165, 268))
c.tag(250, 482, ['Co thắt phế quản'], 9, col=RED)
c.line((300, 478), (385, 350))
c.text(470, 492, 'Số: 27/96-KL', 7.5, 'Arial Italic.ttf', col=INK)
c.save('d06-so-do-tu-thi')

# ── bình xịt: số lô trên nhãn ──
c = Canvas('inhaler')
c.text(113, 124, 'VENTOLIN', 8.5, col=(40, 40, 40))
c.text(113, 142, 'LOT 91-04', 8, 'Arial.ttf', col=(40, 40, 40))
c.text(113, 157, 'EXP 1991', 7, 'Arial.ttf', col=(70, 70, 70))
c.save('d12-inhaler')

# ── dép rọ và bút: số trên thẻ đánh dấu ──
c = Canvas('shoes')
c.text(313, 55, '1', 26, col=(20, 20, 20))
c.text(420, 65, '2', 26, col=(20, 20, 20))
c.save('d16-shoes')
