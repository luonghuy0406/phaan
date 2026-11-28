#!/usr/bin/env python3
"""Cắt một ảnh ghép nhiều chân dung (lưới hàng × cột, ngăn bằng đường kẻ trắng hoặc không) thành ảnh thẻ 3:4, 480×640 WebP.

    python3 tools/crop-portraits.py <ảnh-ghép> <thư-mục-images> <số hàng> <số cột> <id1> <id2> …

Các id đi theo thứ tự đọc (trái → phải, trên → dưới); id "-" bỏ qua ô đó. Ví dụ:
    python3 tools/crop-portraits.py grid.png public/cases/demo-01/images 2 2 tu minh hoa loc
Tạo id-<id>.webp trong thư mục images. Mỗi ô được cắt khung 3:4 quanh phần không phải nền (khuôn mặt, tóc).
"""
import sys
from PIL import Image


def whiteish(p): return min(p[:3]) > 235


def dividers(px, n_parts, length, other, axis):
    """Vị trí các đường kẻ trắng chia ảnh thành n_parts phần; không có thì chia đều."""
    cuts = []
    for k in range(1, n_parts):
        guess = round(length * k / n_parts)
        best = None
        for c in range(max(1, guess - length // 10), min(length - 1, guess + length // 10)):
            pts = [px[c, o] if axis == 'x' else px[o, c] for o in range(0, other, 8)]
            if sum(whiteish(p) for p in pts) > 0.85 * len(pts):
                best = (best[0], c) if best else (c, c)
        cuts.append(best or (guess, guess))
    return cuts


def main():
    if len(sys.argv) < 6:
        sys.exit(__doc__)
    src, out_dir, rows, cols, ids = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5:]
    im = Image.open(src).convert('RGB'); W, H = im.size; px = im.load()
    vx = dividers(px, cols, W, H, 'x'); hy = dividers(px, rows, H, W, 'y')
    xs = [0] + [b for a, b in vx]; xe = [a for a, b in vx] + [W]
    ys = [0] + [b for a, b in hy]; ye = [a for a, b in hy] + [H]
    for i, pid in enumerate(ids):
        if pid == '-': continue
        r, c = divmod(i, cols)
        cell = im.crop((xs[c] + 4, ys[r] + 4, xe[c] - 4, ye[r] - 4)); cw, ch = cell.size; cp = cell.load()
        bg = cp[4, 4]
        def is_bg(p): return sum(abs(p[k] - bg[k]) for k in range(3)) < 60
        cols_fg = [x for x in range(cw) if sum(1 for y in range(0, ch // 2, 4) if not is_bg(cp[x, y])) > 6]
        cx = (cols_fg[0] + cols_fg[-1]) // 2 if cols_fg else cw // 2
        if cw * 4 >= ch * 3:  # wide cell: full height, 3:4 width around the face
            h = ch; w = h * 3 // 4; x0 = max(0, min(cw - w, cx - w // 2)); box = (x0, 0, x0 + w, h)
        else:                 # tall cell: full width, crop height from the top
            w = cw; h = w * 4 // 3; box = (0, 0, w, min(ch, h))
        out = cell.crop(box).resize((480, 640), Image.LANCZOS)
        out.save(f'{out_dir}/id-{pid}.webp', 'WEBP', quality=84)
        print(f'id-{pid}.webp  ô {r + 1},{c + 1}')


if __name__ == '__main__':
    main()
