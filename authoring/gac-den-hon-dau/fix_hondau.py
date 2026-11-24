import random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC=sys.argv[1]; OUT=sys.argv[2]; S=sys.argv[3]
im=Image.open(SRC).convert('RGB'); px=im.load()
random.seed(7)

def ring_fill(box, pad=4, keep=lambda c: True):
    """Fill box with pixels sampled from a clean ring around it (texture-preserving erase)."""
    x0,y0,x1,y1=box; pool=[]
    for x in range(x0-pad,x1+pad):
        for y in (*range(y0-pad,y0), *range(y1,y1+pad)):
            c=px[x,y]; pool.append(c) if keep(c) else None
    for y in range(y0,y1):
        for x in (*range(x0-pad,x0), *range(x1,x1+pad)):
            c=px[x,y]; pool.append(c) if keep(c) else None
    for x in range(x0,x1):
        for y in range(y0,y1): px[x,y]=random.choice(pool)

def hfill(box):
    """Erase on a smooth gradient background: per row, interpolate between the left and right edge colours, add slight noise."""
    x0,y0,x1,y1=box
    for y in range(y0,y1):
        L=px[x0-2,y]; R=px[x1+1,y]
        for x in range(x0,x1):
            t=(x-x0)/max(1,x1-x0)
            px[x,y]=tuple(max(0,min(255,int(L[i]*(1-t)+R[i]*t+random.randint(-3,3)))) for i in range(3))

def clone(dst, dx, dy, feather=4):
    """Copy a patch from (dst shifted by dx,dy) onto dst with feathered edges."""
    x0,y0,x1,y1=dst; w,h=x1-x0,y1-y0
    patch=im.crop((x0+dx,y0+dy,x1+dx,y1+dy))
    mask=Image.new('L',(w,h),0); d=ImageDraw.Draw(mask); d.rectangle((feather,feather,w-feather,h-feather),fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(feather/2))
    im.paste(patch,(x0,y0),mask)

# 1) d13: drop the 23h25 / 23h35 milestones (labels + dots) that name the killer's moves
for box in [(988,758,1086,822),(1114,758,1200,822)]: hfill(box)
for cx in (1040,1157):                     # dots on the yellow line: copy the plain line from 30 px to the left
    for x in range(cx-12,cx+13):
        for y in range(737,762): px[x,y]=px[x-30,y]

# 2) d02: remove the separate "Trạm máy nổ" building (the generator room is at the foot of the tower, see d04)
clone((1150,147,1268,184), -118, 0)

# 3) d01: 26/09/1998 was a Saturday
ring_fill((809,18,878,37), pad=5, keep=lambda c: sum(c)>480)
f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 14)
d=ImageDraw.Draw(im)
tw=d.textlength('Thứ Bảy', font=f)
d.text((875-tw, 19), 'Thứ Bảy', font=f, fill=(28,28,28))
im.save(OUT)
for name,box in [('z2-d13',(873,584,1445,828)),('z2-d02',(913,2,1445,297)),('z2-d01',(489,2,906,297))]:
    t=im.crop(box); t.resize((t.width*2,t.height*2)).save(f'{S}/{name}.png')
