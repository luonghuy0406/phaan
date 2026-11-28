# Prompt ảnh: Chiếc cặp da đêm thứ Tư (bản 2, hư cấu)

Mọi ảnh cũ (dính tên vụ thật, tên báo thật, nhãn tang vật sai thời đại) đã gỡ. Sơ đồ d04 vẽ bằng `draw_so_do.py`.

## 1. Ảnh thẻ (ghép 3 cột × 2 hàng)
Cắt: `python3 tools/crop-portraits.py <ảnh> public/cases/dem-sung-no-tay-son/images 2 3 phuc cuong dong tuan hung -`

```text
A 3-column by 2-row grid of six Vietnamese ID card portrait photos from 1998, Hanoi, separated by thin white lines, each cell a head-and-shoulders front-facing shot, neutral expression, plain pale blue background, flat studio lighting, slightly faded film colour, realistic skin texture, no text.
Top row, left to right:
(1) a 58-year-old Vietnamese gold shop owner, kind round face, thinning grey hair combed back, white short-sleeved shirt;
(2) a 34-year-old Vietnamese man with a hard cold stare, very short hair, a long visible scar on the left side of his chin, dark grey t-shirt;
(3) a 30-year-old Vietnamese goldsmith, thin face, stubborn look, short side-parted hair, light blue work shirt;
Bottom row, left to right:
(4) a 29-year-old Vietnamese private driver, neat polite face, short tidy hair, white shirt with collar buttoned;
(5) a 45-year-old Vietnamese pawnshop owner, plump face, slicked-back hair, thin gold chain, floral print shirt;
(6) an empty plain pale blue cell.
```

## 2. Bìa và ảnh tư liệu (ghép 2 × 2)
Cắt: `python3 tools/crop-portraits.py <ảnh> public/cases/dem-sung-no-tay-son/images 2 2 cover d01-bao-chi d07-vo-dan x --whole`

```text
A 2-by-2 grid of four realistic photographs, Hanoi 1998, separated by thin white lines, slightly faded film colour, no people's faces, no text.
Top left: cinematic night scene of a narrow side alley next to an old Hanoi gold shop on a rainy night, heavy rain, wet street reflecting the red and yellow light of the gold shop sign glow (no readable letters), a black leather briefcase lying on the wet doorstep of a small side door, a black 1990s Toyota sedan's red tail lights leaving at the end of the street, moody, cinematic.
Top right: black-and-white newspaper-style photo of the same alley the next morning, police tape across the alley mouth, a few onlookers seen from behind, wet ground.
Bottom left: police evidence photo on a grey table: two brass pistol cartridge cases and two deformed bullets next to a centimetre ruler and a paper evidence tag (blank, no writing).
Bottom right: a dark empty cell.
```
