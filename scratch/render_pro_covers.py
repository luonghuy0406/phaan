#!/usr/bin/env python3
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "/Users/huynguyen/Documents/game_pha_an/public/cases"

FONT_HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
FONT_ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_COURIER = "/System/Library/Fonts/Supplemental/Courier New.ttf"
FONT_GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"

def get_font(path, size, index=0):
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        try:
            return ImageFont.truetype(FONT_ARIAL, size)
        except Exception:
            return ImageFont.load_default()

def add_noise(img, strength=14):
    w, h = img.size
    noise = Image.new('RGB', (w, h))
    npix = noise.load()
    random.seed(42)
    for y in range(h):
        for x in range(w):
            v = random.randint(128 - strength, 128 + strength)
            npix[x, y] = (v, v, v)
    return Image.blend(img, noise, 0.12)

def draw_tilted_tape(draw, x1, y1, x2, y2, width, color=(240, 200, 30), text="EVIDENCE // CHỨNG CỨ HÌNH SỰ // NIÊM PHONG", font=None):
    # Calculate angle and rectangle
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    angle = math.atan2(dy, dx)
    
    # Perpendicular vector
    px = -math.sin(angle) * (width / 2)
    py = math.cos(angle) * (width / 2)
    
    poly = [
        (x1 + px, y1 + py),
        (x2 + px, y2 + py),
        (x2 - px, y2 - py),
        (x1 - px, y1 - py)
    ]
    draw.polygon(poly, fill=color, outline=(20, 20, 20))
    
    # Hazard stripes on tape edges
    step = 25
    for dist in range(0, int(length), step):
        t = dist / length
        cx = x1 + dx * t
        cy = y1 + dy * t
        draw.line([(cx + px*0.8, cy + py*0.8), (cx + px*0.3, cy + py*0.3)], fill=(20, 20, 20), width=2)
        draw.line([(cx - px*0.8, cy - py*0.8), (cx - px*0.3, cy - py*0.3)], fill=(20, 20, 20), width=2)

def draw_evidence_tag(draw, x, y, w, h, text, font, angle=0):
    tag = Image.new('RGBA', (w, h), (255, 255, 255, 0))
    tdraw = ImageDraw.Draw(tag)
    tdraw.rectangle([0, 0, w-1, h-1], fill=(245, 240, 220, 240), outline=(100, 80, 60, 220), width=1)
    # top pin hole
    tdraw.ellipse([w//2 - 4, 4, w//2 + 4, 12], fill=(60, 50, 40))
    tdraw.text((w//2, h//2 + 4), text, fill=(30, 25, 20), font=font, anchor="mm")
    return tag

def render_case_cover(case_id, no_str, title, subtitle, setting, color_accent, draw_art_fn):
    w, h = 900, 1200
    img = Image.new('RGB', (w, h), (20, 22, 26))
    draw = ImageDraw.Draw(img)
    
    # 1. Studio backdrop lighting
    for y in range(h):
        t = y / h
        r = int(24 * (1 - t*0.4) + 12 * (t*0.4))
        g = int(27 * (1 - t*0.4) + 14 * (t*0.4))
        b = int(32 * (1 - t*0.4) + 16 * (t*0.4))
        draw.line([(0, y), (w, y)], fill=(r, g, b))
        
    # Elliptical floor shadow under the box
    shadow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.ellipse([80, 1080, 820, 1160], fill=(0, 0, 0, 160))
    shadow = shadow.filter(ImageFilter.GaussianBlur(25))
    img.paste(shadow, (0, 0), shadow)
    
    # 2. Main Box Dimensions
    bx, by, bw, bh = 100, 70, 700, 1030
    
    # Box body (deep charcoal matte)
    draw.rectangle([bx, by, bx+bw, by+bh], fill=(22, 24, 28))
    
    # Box side bevel highlight (subtle 3D look)
    draw.line([(bx, by), (bx+bw, by)], fill=(75, 80, 90), width=2)
    draw.line([(bx, by), (bx, by+bh)], fill=(65, 70, 80), width=2)
    draw.line([(bx+bw, by), (bx+bw, by+bh)], fill=(10, 12, 14), width=2)
    draw.line([(bx, by+bh), (bx+bw, by+bh)], fill=(8, 10, 12), width=3)
    
    # Box top header
    f_mono_small = get_font(FONT_COURIER, 16)
    f_header = get_font(FONT_HELVETICA, 18)
    draw.text((bx + 30, by + 28), f"HỒ SƠ MẬT • CASE #{no_str}", fill=(240, 200, 30), font=f_header)
    draw.text((bx + bw - 30, by + 28), "BÀN ĐIỀU TRA HÌNH SỰ", fill=(160, 165, 175), font=f_header, anchor="ra")
    draw.line([(bx + 30, by + 58), (bx + bw - 30, by + 58)], fill=(45, 50, 60), width=1)
    
    # 3. Center Art Frame
    art_x, art_y, art_w, art_h = bx + 30, by + 75, bw - 60, 640
    # Art frame border
    draw.rectangle([art_x - 2, art_y - 2, art_x + art_w + 2, art_y + art_h + 2], outline=(40, 45, 55), width=2)
    
    art_img = Image.new('RGB', (art_w, art_h), (25, 28, 35))
    art_draw = ImageDraw.Draw(art_img)
    
    # Call case-specific art drawing
    draw_art_fn(art_draw, art_w, art_h)
    
    img.paste(art_img, (art_x, art_y))
    
    # Redraw main draw for overlays
    draw = ImageDraw.Draw(img)
    
    # 4. Yellow Neon Hazard Tape slicing across
    f_tape = get_font(FONT_ARIAL, 14)
    draw_tilted_tape(draw, art_x - 20, art_y + 310, art_x + art_w + 20, art_y + 350, 32, color=(245, 205, 25), font=f_tape)
    
    # Forensic note tag
    f_tag = get_font(FONT_COURIER, 14)
    tag = draw_evidence_tag(draw, 0, 0, 160, 50, f"FILE NO: {no_str}", f_tag)
    tag_rot = tag.rotate(-8, expand=True, resample=Image.BICUBIC)
    img.paste(tag_rot, (bx + bw - 180, art_y + 30), tag_rot)
    
    # 5. Lower Title Badge
    badge_x = bx + 30
    badge_y = by + 740
    badge_w = bw - 60
    badge_h = 240
    
    # Bold yellow rectangular title badge
    draw.rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], fill=(245, 205, 25))
    draw.rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], outline=(20, 20, 20), width=4)
    
    # Title badge content
    f_title = get_font(FONT_HELVETICA, 36)
    f_sub = get_font(FONT_ARIAL, 18)
    f_meta = get_font(FONT_COURIER, 14)
    
    draw.text((badge_x + 30, badge_y + 32), title.upper(), fill=(15, 15, 15), font=f_title)
    draw.text((badge_x + 30, badge_y + 82), subtitle, fill=(40, 35, 20), font=f_sub)
    
    draw.line([(badge_x + 30, badge_y + 120), (badge_x + badge_w - 30, badge_y + 120)], fill=(30, 25, 10), width=2)
    
    draw.text((badge_x + 30, badge_y + 140), f"BỐI CẢNH: {setting.upper()}", fill=(20, 20, 20), font=f_meta)
    draw.text((badge_x + 30, badge_y + 170), "HỘP TƯ LIỆU ĐIỀU TRA HÌNH SỰ • SUY LUẬN LOGIC", fill=(60, 50, 20), font=f_meta)
    
    # Barcode representation on bottom right of badge
    bx_bar = badge_x + badge_w - 180
    by_bar = badge_y + 140
    for i in range(28):
        bw_line = random.choice([2, 4, 1, 3])
        draw.line([(bx_bar + i*5, by_bar), (bx_bar + i*5, by_bar + 45)], fill=(15, 15, 15), width=bw_line)
    draw.text((bx_bar, by_bar + 52), f"978-604-00-{no_str}4", fill=(15, 15, 15), font=f_mono_small)
    
    # Bottom margin text
    f_foot = get_font(FONT_COURIER, 13)
    draw.text((bx + bw // 2, by + bh - 24), "TRUNG TÂM LƯU TRỮ HỒ SƠ VỤ ÁN • ĐỀ NGHỊ BẢO MẬT", fill=(100, 105, 115), font=f_foot, anchor="mm")
    
    # Apply subtle realistic film grain
    final_img = add_noise(img, strength=10)
    
    # Save as high quality WebP
    out_dir = os.path.join(OUTPUT_DIR, case_id, "images")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "cover.webp")
    final_img.save(out_path, "WEBP", quality=88)
    print(f"✓ Generated Cover: {out_path} ({os.path.getsize(out_path) // 1024} KB)")

# Specific art drawing functions for each case

def art_demo_01(draw, w, h):
    # Case 00: Hanoi Old Quarter clock mystery (1990s)
    # Background: Hanoi old townhouse interior with arched doorway
    for y in range(h):
        draw.line([(0, y), (w, y)], fill=(int(20 + y/h*30), int(22 + y/h*25), int(26 + y/h*20)))
    # Window silhouette with wooden bars
    draw.rectangle([40, 40, 240, 360], outline=(70, 60, 50), width=4)
    draw.line([(140, 40), (140, 360)], fill=(70, 60, 50), width=3)
    draw.line([(40, 200), (240, 200)], fill=(70, 60, 50), width=3)
    # Fragmented split face 1: Old homeowner with spectacles (center left)
    draw.polygon([(260, 100), (460, 120), (430, 460), (240, 440)], fill=(45, 40, 35), outline=(120, 100, 70))
    # Spectacles on homeowner
    draw.ellipse([300, 220, 370, 290], outline=(220, 190, 100), width=3)
    draw.line([(370, 255), (410, 255)], fill=(220, 190, 100), width=3)
    # Fragmented split face 2: Sneaky nephew (top right)
    draw.polygon([(465, 80), (600, 100), (580, 340), (445, 320)], fill=(35, 40, 45), outline=(80, 100, 120))
    draw.ellipse([500, 180, 540, 215], fill=(210, 215, 220)) # eye highlight
    draw.ellipse([515, 190, 532, 207], fill=(15, 15, 20)) # pupil looking left
    # Fragmented face 3: Maid (bottom right)
    draw.polygon([(435, 345), (595, 360), (570, 580), (410, 560)], fill=(40, 32, 35), outline=(110, 80, 90))
    # Vintage mantle clock silhouette
    draw.ellipse([100, 420, 200, 520], outline=(220, 180, 70), width=5)
    draw.line([(150, 470), (150, 440)], fill=(240, 200, 70), width=4) # hour hand
    draw.line([(150, 470), (180, 470)], fill=(240, 200, 70), width=3) # min hand

def art_con_nuoc(draw, w, h):
    # Case 01: Mekong delta river boat mystery (Ben Tre)
    # Muddy alluvial river dusk gradient
    for y in range(h):
        t = y / h
        r = int(50 * (1-t) + 90 * t * 0.7)
        g = int(30 * (1-t) + 45 * t * 0.7)
        b = int(25 * (1-t) + 30 * t * 0.7)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    # River silhouettes (coconut palms)
    draw.polygon([(0, 240), (180, 320), (0, 480)], fill=(12, 14, 18))
    draw.polygon([(w, 200), (w-200, 300), (w, 460)], fill=(10, 12, 16))
    # Split face collage: Weathered boat owner (bronzed skin, stern look)
    draw.polygon([(180, 120), (420, 100), (390, 520), (160, 490)], fill=(48, 32, 24), outline=(160, 110, 70), width=2)
    draw.ellipse([250, 230, 310, 270], fill=(220, 200, 180)) # eye
    draw.ellipse([270, 240, 295, 265], fill=(30, 20, 15)) # dark pupil
    # Split face: Young boatman / mechanic
    draw.polygon([(425, 95), (580, 115), (550, 510), (395, 490)], fill=(32, 38, 44), outline=(80, 110, 130), width=2)
    draw.ellipse([460, 225, 520, 265], fill=(210, 210, 215)) # suspicious eye
    draw.ellipse([475, 235, 500, 260], fill=(15, 20, 25))
    # River boat hull silhouette in lower foreground
    draw.polygon([(80, 540), (560, 540), (500, 620), (140, 620)], fill=(18, 20, 25), outline=(180, 140, 70), width=2)

def art_binh_ty(draw, w, h):
    # Case 02: Cold winter collective apartment Hanoi 1996
    # Bleak cold gray-blue overcast winter background
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(24 + t*20), int(30 + t*26), int(42 + t*32)))
    # Collective quarter balcony railings silhouette
    for yb in range(80, 300, 40):
        draw.line([(40, yb), (200, yb)], fill=(50, 60, 75), width=2)
    # Split face: Elderly textile worker with round reading glasses
    draw.polygon([(190, 110), (400, 90), (380, 510), (170, 490)], fill=(40, 42, 48), outline=(130, 140, 160), width=2)
    draw.ellipse([240, 220, 320, 300], outline=(200, 180, 140), width=3) # glasses frame
    # Split face: Nurse / daughter-in-law
    draw.polygon([(405, 90), (560, 110), (540, 520), (385, 500)], fill=(36, 42, 46), outline=(90, 130, 140), width=2)
    draw.ellipse([450, 230, 505, 265], fill=(225, 225, 230))
    draw.ellipse([465, 238, 490, 260], fill=(20, 25, 30))
    # Teacup & chrysanthemum steam silhouette
    draw.arc([80, 460, 160, 540], 0, 180, fill=(220, 190, 100), width=3)

def art_chua_thay(draw, w, h):
    # Case 11: Thay Pagoda ancient bell tower & Sai Son mountain (1997)
    # Misty spiritual temple dusk
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(35 + t*15), int(32 + t*12), int(28 + t*10)))
    # Pagoda curved roof eaves silhouette
    draw.arc([60, 60, 320, 240], 190, 350, fill=(90, 80, 70), width=5)
    # Giant bronze bell silhouette
    draw.arc([100, 260, 260, 520], 180, 360, fill=(70, 120, 90), width=8) # bronze patina green
    # Split face: Elderly Abbot in meditation
    draw.polygon([(260, 100), (450, 90), (430, 520), (240, 500)], fill=(48, 40, 32), outline=(180, 140, 90), width=2)
    # Split face: Troubled bell ringer monk
    draw.polygon([(455, 90), (590, 110), (570, 510), (435, 490)], fill=(38, 35, 40), outline=(120, 100, 130), width=2)
    draw.ellipse([490, 230, 540, 270], fill=(220, 215, 210))
    draw.ellipse([505, 240, 528, 263], fill=(20, 15, 25))

def art_tuyet_trang(draw, w, h):
    # Case 14: Sapa alpine snow resort noir (1996)
    # Snowy mountain cold gradient
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(18 + t*22), int(28 + t*30), int(45 + t*35)))
    # Snowflakes falling dots
    random.seed(99)
    for _ in range(60):
        sx = random.randint(20, w-20)
        sy = random.randint(20, h-20)
        sr = random.randint(1, 3)
        draw.ellipse([sx-sr, sy-sr, sx+sr, sy+sr], fill=(240, 245, 255))
    # Split face: Young blonde beauty pageant child
    draw.polygon([(180, 100), (380, 90), (360, 510), (160, 490)], fill=(46, 44, 48), outline=(220, 200, 150), width=2)
    draw.arc([220, 90, 340, 160], 180, 360, fill=(240, 210, 80), width=4) # tiara / crown outline
    # Split face: Wealthy tense parents
    draw.polygon([(385, 90), (580, 110), (550, 520), (365, 500)], fill=(32, 36, 46), outline=(100, 120, 150), width=2)
    draw.ellipse([440, 220, 495, 260], fill=(230, 230, 235))
    draw.ellipse([455, 230, 480, 255], fill=(15, 20, 30))

def art_tay_son(draw, w, h):
    # Case 15: Hanoi Tay Son gunshot urban noir (1999)
    # Wet asphalt night street under sodium vapor amber glow
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(20 + t*35), int(18 + t*25), int(15 + t*10)))
    # Bullet casing silhouette on street
    draw.polygon([(80, 480), (140, 450), (190, 490), (130, 520)], fill=(210, 170, 60), outline=(240, 200, 80), width=2)
    # Split face: Scarred armed robber
    draw.polygon([(180, 95), (400, 85), (380, 515), (160, 495)], fill=(45, 35, 30), outline=(160, 100, 70), width=2)
    # Scar mark across eye
    draw.line([(240, 220), (320, 280)], fill=(180, 80, 70), width=4)
    # Split face: Silversmith & gold shop witness
    draw.polygon([(405, 85), (580, 105), (550, 525), (385, 505)], fill=(35, 36, 40), outline=(120, 130, 140), width=2)
    draw.ellipse([460, 230, 510, 270], fill=(225, 220, 215))
    draw.ellipse([475, 240, 498, 265], fill=(25, 20, 20))

def art_quai_vat(draw, w, h):
    # Case 16: Monster with 21 Faces (Glico Morinaga Japanese corporate noir)
    # Dark industrial matrix / 1980s retro grid
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(20 + t*15), int(22 + t*18), int(28 + t*25)))
    # Grid lines
    for gx in range(40, w, 40):
        draw.line([(gx, 40), (gx, h-40)], fill=(32, 36, 45), width=1)
    # Split face 1: Police sketch of the "Fox-Eyed Man" with baseball cap
    draw.polygon([(180, 110), (390, 95), (370, 510), (160, 490)], fill=(40, 42, 45), outline=(140, 145, 160), width=2)
    # Cap brim
    draw.polygon([(180, 160), (380, 140), (370, 190), (170, 200)], fill=(30, 50, 80))
    # Slanted fox eyes
    draw.line([(240, 240), (300, 230)], fill=(220, 220, 230), width=6)
    draw.line([(255, 238), (285, 234)], fill=(15, 15, 20), width=6)
    # Split face 2: Ghostly pale Noh theater mask
    draw.polygon([(395, 95), (580, 115), (550, 520), (375, 505)], fill=(65, 68, 72), outline=(180, 185, 195), width=2)
    draw.ellipse([440, 220, 490, 245], fill=(20, 20, 25)) # hollow dark Noh mask eye
    draw.arc([430, 360, 500, 400], 0, 180, fill=(180, 40, 40), width=3) # Noh painted red lips

def main():
    print("Starting generation of remastered covers for cases 00, 01, 02, 11, 14, 15, 16...")
    
    # 00. demo-01
    render_case_cover(
        "demo-01", "00",
        "Chiếc đồng hồ ngõ Gác Chuông",
        "Hồ sơ mất trộm • Cửa sổ vỡ tầng hai",
        "Phố Cổ, Hà Nội (Thập niên 90)",
        (240, 200, 30),
        art_demo_01
    )
    
    # 01. con-nuoc-ram-thang-gieng
    render_case_cover(
        "con-nuoc-ram-thang-gieng", "01",
        "Con nước Rằm tháng Giêng",
        "Án mạng phòng kín trên ghe • Hàm Luông",
        "Xã Tân Mỹ, Bến Tre (Nam Bộ)",
        (240, 200, 30),
        art_con_nuoc
    )
    
    # 02. mua-dong-binh-ty
    render_case_cover(
        "mua-dong-binh-ty", "02",
        "Mùa đông năm Bính Tý",
        "Giao thừa vắng pháo • Chén trà hoa cúc",
        "Khu tập thể Dệt Thống Nhất (Hà Nội 1996)",
        (240, 200, 30),
        art_binh_ty
    )
    
    # 11. hoi-chuong-chua-thay
    render_case_cover(
        "hoi-chuong-chua-thay", "11",
        "Hồi chuông núi Sài Sơn",
        "Đại hồng chung 12h trưa • Bẫy tre cơ học",
        "Chùa Thầy, Sài Sơn, Hà Tây (1997)",
        (240, 200, 30),
        art_chua_thay
    )
    
    # 14. buc-thu-dem-tuyet-trang
    render_case_cover(
        "buc-thu-dem-tuyet-trang", "14",
        "Bức thư đêm tuyết trắng",
        "Vụ án có thật • Tuyết rơi Ô Quy Hồ",
        "Sa Pa, Lào Cai (Đông 1996)",
        (240, 200, 30),
        art_tuyet_trang
    )
    
    # 15. dem-sung-no-tay-son
    render_case_cover(
        "dem-sung-no-tay-son", "15",
        "Đêm súng nổ phố Tây Sơn",
        "Vụ án có thật • Tiếng súng xé toạc màn đêm",
        "Phố Tây Sơn, Hà Nội (1999)",
        (240, 200, 30),
        art_tay_son
    )
    
    # 16. quai-vat-21-khuon-mat
    render_case_cover(
        "quai-vat-21-khuon-mat", "16",
        "Quái vật 21 khuôn mặt",
        "Vụ án có thật • Kẹo độc & Thư khiêu khích",
        "Tập đoàn Bánh kẹo (1984 - 2012)",
        (240, 200, 30),
        art_quai_vat
    )
    
    print("All 7 covers successfully rendered!")

if __name__ == "__main__":
    main()
