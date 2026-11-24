#!/usr/bin/env python3
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = "/Users/huynguyen/Documents/game_pha_an/public/cases"

FONT_HELVETICA = "/System/Library/Fonts/Helvetica.ttc"
FONT_ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_COURIER = "/System/Library/Fonts/Supplemental/Courier New.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(FONT_ARIAL, size)
        except Exception:
            return ImageFont.load_default()

def add_paper_grain(img, strength=12):
    w, h = img.size
    noise = Image.new('RGB', (w, h))
    npix = noise.load()
    random.seed(123)
    for y in range(h):
        for x in range(w):
            v = random.randint(128 - strength, 128 + strength)
            npix[x, y] = (v, v, v)
    return Image.blend(img, noise, 0.12)

def save_image(img, case_id, filename):
    final_img = add_paper_grain(img)
    out_dir = os.path.join(BASE_DIR, case_id, "images")
    os.makedirs(out_dir, exist_ok=True)
    out_p = os.path.join(out_dir, filename)
    final_img.save(out_p, "WEBP", quality=86)
    print(f"✓ Saved visual: {case_id}/images/{filename} ({os.path.getsize(out_p)//1024} KB)")

# ==================== TEMPLATE RENDERERS ====================

def make_newspaper_photo(w=800, h=500, title="", scene_fn=None):
    # Black and white retro newsprint photo with halftone look
    img = Image.new('RGB', (w, h), (220, 220, 215))
    draw = ImageDraw.Draw(img)
    # Background scene
    if scene_fn:
        scene_fn(draw, w, h)
    else:
        # Generic architectural / news scene
        for y in range(h):
            t = y / h
            v = int(140 - t*60)
            draw.line([(0, y), (w, y)], fill=(v, v, v))
        # Police cordon tape
        draw.line([(0, int(h*0.7)), (w, int(h*0.75))], fill=(240, 240, 240), width=8)
    
    # Newsprint halftone grain overlay
    for y in range(0, h, 4):
        draw.line([(0, y), (w, y)], fill=(20, 20, 20, 30), width=1)
        
    # Corner stamp "ẢNH TƯ LIỆU"
    f_stamp = get_font(FONT_COURIER, 13)
    draw.rectangle([w - 150, h - 36, w - 15, h - 12], outline=(30, 30, 30), width=1)
    draw.text((w - 140, h - 32), "[ ẢNH TƯ LIỆU ]", fill=(40, 40, 40), font=f_stamp)
    return img

def make_blueprint(w=800, h=600, title="SƠ ĐỒ HIỆN TRƯỜNG", plan_fn=None):
    # Professional forensic architectural floor plan on blue/slate grid
    img = Image.new('RGB', (w, h), (28, 42, 60))
    draw = ImageDraw.Draw(img)
    
    # Blueprint cyan/blue grid lines
    grid_col = (40, 60, 85)
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=grid_col, width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=grid_col, width=1)
        
    # Outer blueprint border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(100, 160, 210), width=2)
    draw.rectangle([25, 25, w - 25, h - 25], outline=(60, 100, 140), width=1)
    
    # Title box (bottom right)
    draw.rectangle([w - 320, h - 90, w - 30, h - 30], fill=(20, 32, 48), outline=(100, 160, 210), width=2)
    f_title = get_font(FONT_HELVETICA, 16)
    f_sub = get_font(FONT_COURIER, 12)
    draw.text((w - 305, h - 80), title.upper(), fill=(230, 240, 255), font=f_title)
    draw.text((w - 305, h - 55), "TỶ LỆ: 1/100 • BỘ PHẬN ĐIỀU TRA", fill=(140, 180, 220), font=f_sub)
    
    # Compass Rose (North Arrow)
    cx, cy = 60, 65
    draw.polygon([(cx, cy - 25), (cx + 8, cy), (cx, cy + 15), (cx - 8, cy)], fill=(220, 240, 255), outline=(100, 160, 210))
    draw.text((cx - 4, cy - 40), "B", fill=(220, 240, 255), font=f_title)
    
    # Custom floor plan drawing
    if plan_fn:
        plan_fn(draw, w, h)
        
    return img

def make_autopsy_chart(w=800, h=600, victim_name="NẠN NHÂN", wound_fn=None):
    # Medical examiner anatomical human body chart
    img = Image.new('RGB', (w, h), (245, 244, 238))
    draw = ImageDraw.Draw(img)
    
    # Header
    f_head = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_COURIER, 13)
    draw.text((40, 30), "SƠ ĐỒ PHÁC HỌA THƯƠNG TÍCH Y PHÁP", fill=(30, 30, 35), font=f_head)
    draw.text((40, 58), f"NẠN NHÂN: {victim_name.upper()} • PHÒNG PHÁP Y HÌNH SỰ", fill=(90, 85, 75), font=f_sub)
    draw.line([(40, 82), (w - 40, 82)], fill=(120, 115, 105), width=2)
    
    # Outline figure: Front & Back body silhouettes
    for offset_x in [240, 520]:
        # Head
        draw.ellipse([offset_x - 30, 120, offset_x + 30, 180], outline=(80, 85, 95), width=2)
        # Torso
        draw.polygon([(offset_x - 45, 190), (offset_x + 45, 190), (offset_x + 35, 340), (offset_x - 35, 340)], outline=(80, 85, 95), width=2)
        # Arms
        draw.line([(offset_x - 45, 190), (offset_x - 75, 320)], fill=(80, 85, 95), width=12)
        draw.line([(offset_x + 45, 190), (offset_x + 75, 320)], fill=(80, 85, 95), width=12)
        # Legs
        draw.line([(offset_x - 20, 340), (offset_x - 25, 520)], fill=(80, 85, 95), width=14)
        draw.line([(offset_x + 20, 340), (offset_x + 25, 520)], fill=(80, 85, 95), width=14)
        
    f_view = get_font(FONT_HELVETICA, 13)
    draw.text((240, 545), "MẶT TRƯỚC", fill=(100, 105, 115), font=f_view, anchor="mm")
    draw.text((520, 545), "MẶT SAU", fill=(100, 105, 115), font=f_view, anchor="mm")
    
    # Custom wound marks
    if wound_fn:
        wound_fn(draw, w, h)
        
    return img

def make_ticket_scan(w=800, h=500, title="VÉ TÀU HỎA", details=None):
    # Realistic paper ticket / receipt with stamps and barcode
    img = Image.new('RGB', (w, h), (242, 238, 226))
    draw = ImageDraw.Draw(img)
    
    # Ticket outer border with perforation notch
    draw.rectangle([40, 40, w - 40, h - 40], fill=(250, 247, 238), outline=(160, 150, 135), width=2)
    # Perforation dashed line
    for y in range(40, h - 40, 12):
        draw.line([(w - 180, y), (w - 180, y + 6)], fill=(180, 170, 155), width=2)
        
    f_head = get_font(FONT_HELVETICA, 22)
    f_txt = get_font(FONT_COURIER, 15)
    f_stamp = get_font(FONT_HELVETICA, 14)
    
    draw.text((70, 70), title.upper(), fill=(180, 35, 35), font=f_head)
    
    if details:
        for idx, (label, val) in enumerate(details):
            draw.text((70, 125 + idx*36), f"{label}:", fill=(80, 75, 65), font=f_txt)
            draw.text((260, 125 + idx*36), str(val), fill=(20, 20, 25), font=f_txt)
            
    # Red official round stamp on the ticket
    cx, cy = w - 100, 150
    draw.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], outline=(190, 40, 40), width=3)
    draw.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], outline=(190, 40, 40), width=1)
    draw.text((cx, cy), "ĐÃ SOÁT", fill=(190, 40, 40), font=f_stamp, anchor="mm")
    
    # Barcode
    bx, by = 70, h - 110
    random.seed(42)
    for i in range(45):
        bw = random.choice([2, 4, 1, 3])
        draw.line([(bx + i*8, by), (bx + i*8, by + 40)], fill=(30, 30, 30), width=bw)
        
    return img

def make_mugshot_profile(w=800, h=600, name="NGHI PHẠM", details=None, face_fn=None):
    # Police criminal file mugshot sheet with paperclip & fingerprint
    img = Image.new('RGB', (w, h), (238, 235, 228))
    draw = ImageDraw.Draw(img)
    
    # Header
    f_head = get_font(FONT_HELVETICA, 20)
    f_sub = get_font(FONT_COURIER, 14)
    draw.text((50, 40), "HỒ SƠ LƯU TRỮ ĐỐI TƯỢNG HÌNH SỰ", fill=(30, 30, 35), font=f_head)
    draw.line([(50, 75), (w - 50, 75)], fill=(100, 95, 85), width=2)
    
    # Photo box with paperclip
    px, py, pw, ph = 80, 110, 260, 340
    draw.rectangle([px, py, px + pw, py + ph], fill=(200, 205, 210), outline=(50, 50, 55), width=2)
    
    if face_fn:
        face_fn(draw, px, py, pw, ph)
    else:
        # Generic portrait silhouette
        cx = px + pw // 2
        draw.ellipse([cx - 50, py + 50, cx + 50, py + 160], fill=(60, 65, 75))
        draw.ellipse([cx - 90, py + 170, cx + 90, py + 340], fill=(50, 55, 65))
        
    # Paperclip on top-left of photo
    draw.line([(px + 20, py - 15), (px + 20, py + 35)], fill=(160, 165, 175), width=4)
    draw.line([(px + 28, py - 15), (px + 28, py + 45)], fill=(160, 165, 175), width=4)
    draw.line([(px + 20, py - 15), (px + 28, py - 15)], fill=(160, 165, 175), width=4)
    
    # Details on right side
    tx = px + pw + 50
    draw.text((tx, 120), f"HỌ TÊN: {name.upper()}", fill=(20, 20, 25), font=f_head)
    if details:
        for idx, (label, val) in enumerate(details):
            draw.text((tx, 175 + idx*38), f"{label}:", fill=(80, 75, 65), font=f_sub)
            draw.text((tx + 160, 175 + idx*38), str(val), fill=(20, 20, 25), font=f_sub)
            
    # Fingerprint stamp box at bottom right
    fx, fy = w - 220, h - 170
    draw.rectangle([fx, fy, fx + 140, fy + 120], outline=(140, 135, 125), width=1)
    draw.text((fx + 70, fy + 10), "ĐIỂM CHỈ", fill=(120, 115, 105), font=f_sub, anchor="mm")
    # Fingerprint whorls
    for r in range(15, 45, 6):
        draw.ellipse([fx + 70 - r, fy + 65 - r*0.8, fx + 70 + r, fy + 65 + r*0.8], outline=(40, 45, 80), width=2)
        
    return img

# ==================== CASE SPECIFIC EXECUTIONS ====================

def run_all():
    print("Generating 44 expanded visual assets...")

    # Case 00: demo-01
    bp0 = make_blueprint(title="SƠ ĐỒ TẦNG 2 NGÕ GÁC CHUÔNG", plan_fn=lambda d, w, h: (
        # Living room with clock cabinet and window
        d.rectangle([140, 120, 560, 480], outline=(220, 240, 255), width=4),
        d.rectangle([180, 440, 320, 475], fill=(80, 130, 180)), # Clock display case
        d.text((250, 455), "TỦ KÍNH ĐỒNG HỒ", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Broken window
        d.line([(560, 240), (560, 360)], fill=(240, 80, 80), width=6),
        d.text((580, 300), "CỬA SỔ VỠ", fill=(240, 100, 100), font=get_font(FONT_HELVETICA, 12)),
        # Stairs
        d.rectangle([140, 120, 240, 220], outline=(140, 180, 220), width=2),
        d.text((190, 170), "CẦU THANG", fill=(180, 210, 240), font=get_font(FONT_HELVETICA, 12), anchor="mm")
    ))
    save_image(bp0, "demo-01", "d02-so-do-nha.webp")

    # Case 01: con-nuoc-ram-thang-gieng
    bp1 = make_blueprint(title="BẢN ĐỒ RẠCH CÂY BẦN & SÔNG HÀM LUÔNG", plan_fn=lambda d, w, h: (
        # River curves
        d.arc([60, 80, 740, 520], 160, 320, fill=(80, 160, 220), width=35),
        # Boat Phước Hải 09 location
        d.polygon([(360, 270), (420, 270), (400, 330), (380, 330)], fill=(220, 180, 60)),
        d.text((390, 345), "GHE PHƯỚC HẢI 09", fill=(240, 240, 240), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Ferry watch hut
        d.rectangle([200, 360, 280, 420], outline=(220, 220, 220), width=2),
        d.text((240, 390), "CHÒI CANH ĐÒ", fill=(220, 220, 220), font=get_font(FONT_HELVETICA, 11), anchor="mm")
    ))
    save_image(bp1, "con-nuoc-ram-thang-gieng", "d02-ban-do-song.webp")

    at1 = make_autopsy_chart(victim_name="LÊ VĂN HOÀNG (CHỦ GHE)", wound_fn=lambda d, w, h: (
        # Water in lungs marker
        d.ellipse([225, 230, 255, 260], fill=(60, 140, 210)),
        d.line([(255, 245), (340, 245)], fill=(40, 100, 180), width=2),
        d.text((345, 240), "XUNG HUYẾT PHỔI & NƯỚC NGỌT", fill=(20, 80, 160), font=get_font(FONT_HELVETICA, 12)),
        # Neck bruise
        d.ellipse([510, 185, 530, 200], fill=(200, 40, 40)),
        d.line([(530, 192), (620, 192)], fill=(180, 30, 30), width=2),
        d.text((625, 186), "BẦM TÍM VÙNG CỔ GÁY", fill=(180, 30, 30), font=get_font(FONT_HELVETICA, 12))
    ))
    save_image(at1, "con-nuoc-ram-thang-gieng", "d05-giai-phau.webp")

    # Case 02: mua-dong-binh-ty
    bp2 = make_blueprint(title="SƠ ĐỒ CĂN HỘ 204 NHÀ A6 TẬP THỂ DỆT", plan_fn=lambda d, w, h: (
        d.rectangle([120, 120, 580, 480], outline=(220, 240, 255), width=4),
        # Tea table
        d.rectangle([300, 260, 420, 360], fill=(80, 130, 180)),
        d.text((360, 310), "BÀN TRÀ CÚC", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Balcony
        d.rectangle([120, 480, 580, 540], outline=(140, 180, 220), width=2),
        d.text((350, 510), "BAN CÔNG HƯỚNG SÂN CHUNG", fill=(180, 210, 240), font=get_font(FONT_HELVETICA, 12), anchor="mm")
    ))
    save_image(bp2, "mua-dong-binh-ty", "d02-so-do-can-ho.webp")

    at2 = make_autopsy_chart(victim_name="TRỊNH VĂN HẠP (67 TUỔI)", wound_fn=lambda d, w, h: (
        # Trachea spasm
        d.ellipse([230, 185, 250, 205], fill=(210, 40, 40)),
        d.line([(250, 195), (340, 195)], fill=(180, 30, 30), width=2),
        d.text((345, 190), "CO THẮT KHÍ QUẢN CẤP TÍNH", fill=(180, 30, 30), font=get_font(FONT_HELVETICA, 12))
    ))
    save_image(at2, "mua-dong-binh-ty", "d06-so-do-tu-thi.webp")

    # Case 03: tieng-dan-day-pho-hien
    np3 = make_newspaper_photo(title="BÁO HẢI HƯNG 1993", scene_fn=lambda d, w, h: (
        # Temple roof silhouette against moonlit lake
        d.ellipse([620, 60, 720, 160], fill=(240, 240, 240)), # Full moon
        d.polygon([(100, 340), (450, 240), (800, 340)], fill=(40, 40, 45)), # Pagoda roof
        d.rectangle([180, 340, 720, 480], fill=(25, 25, 30))
    ))
    save_image(np3, "tieng-dan-day-pho-hien", "d01-bao-chi.webp")

    bp3 = make_blueprint(title="SƠ ĐỒ MẶT BẰNG ĐÌNH HOA NGUYỆT", plan_fn=lambda d, w, h: (
        d.rectangle([140, 140, 600, 460], outline=(220, 240, 255), width=4),
        d.rectangle([300, 240, 440, 360], fill=(80, 130, 180)), # Stage
        d.text((370, 300), "SÂN KHẤU CA TRÙ", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        d.text((200, 400), "BUỒNG THAY ĐỒ", fill=(180, 210, 240), font=get_font(FONT_HELVETICA, 12))
    ))
    save_image(bp3, "tieng-dan-day-pho-hien", "d03-so-do-dinh.webp")

    mg3 = make_mugshot_profile(name="CHU VĂN BÌNH & PHƯỜNG CHÈO", details=[
        ("Năm sinh", "1932 (61 tuổi)"),
        ("Nghề nghiệp", "Nghệ nhân đàn đáy"),
        ("Tổ chức", "Phường ca trù Phố Hiến"),
        ("Địa điểm", "Thị xã Hưng Yên")
    ])
    save_image(mg3, "tieng-dan-day-pho-hien", "d06-anh-chan-dung.webp")

    # Case 04: suong-mu-trai-trai
    np4 = make_newspaper_photo(title="BÁO LÂM ĐỒNG 2003", scene_fn=lambda d, w, h: (
        # Greenhouse and pine trees in fog
        d.rectangle([0, 0, w, h], fill=(160, 170, 175)),
        d.polygon([(120, 220), (280, 160), (440, 220)], fill=(70, 80, 85)),
        d.rectangle([140, 220, 420, 420], fill=(50, 60, 65))
    ))
    save_image(np4, "suong-mu-trai-trai", "d01-bao-chi.webp")

    bp4 = make_blueprint(title="SƠ ĐỒ TRANG TRẠI HOA LÂM VIÊN", plan_fn=lambda d, w, h: (
        d.rectangle([100, 120, 380, 360], outline=(220, 240, 255), width=2), # Greenhouses
        d.text((240, 240), "NHÀ KÍNH HOA HỒNG", fill=(180, 210, 240), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        d.rectangle([440, 120, 640, 280], fill=(80, 130, 180)), # Cold storage #2
        d.text((540, 200), "KHO LẠNH SỐ 2", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Steep hill slope
        d.line([(440, 340), (660, 460)], fill=(220, 100, 100), width=4),
        d.text((560, 420), "DỐC THÔNG XUỐNG VỰC", fill=(240, 120, 120), font=get_font(FONT_HELVETICA, 12))
    ))
    save_image(bp4, "suong-mu-trai-trai", "d03-so-do-trang-trai.webp")

    # d11 dial recorder
    img_dh = Image.new('RGB', (800, 600), (45, 48, 52))
    draw_dh = ImageDraw.Draw(img_dh)
    draw_dh.ellipse([200, 100, 600, 500], fill=(235, 235, 230), outline=(80, 85, 95), width=6)
    # Circle dial graduations
    for a in range(0, 360, 15):
        rad = math.radians(a)
        draw_dh.line([(400 + math.cos(rad)*160, 300 + math.sin(rad)*160), (400 + math.cos(rad)*185, 300 + math.sin(rad)*185)], fill=(30, 30, 35), width=2)
    # Temperature graph curve showing plunge to -18C at 01:15
    draw_dh.line([(260, 280), (340, 280), (370, 390), (460, 395), (540, 310)], fill=(200, 35, 35), width=4)
    draw_dh.text((400, 430), "ĐỘT BIẾN LẠNH SÂU: -18°C (LÚC 01:15)", fill=(190, 30, 30), font=get_font(FONT_HELVETICA, 14), anchor="mm")
    save_image(img_dh, "suong-mu-trai-trai", "d11-dong-ho-nhiet-do.webp")

    # Case 05: chuyen-tau-dem-muong-man
    def scene_np5(d, w, h):
        d.rectangle([120, 200, 720, 380], fill=(40, 45, 55))
        for wx in range(160, 700, 90):
            d.rectangle([wx, 240, wx + 60, 300], fill=(220, 235, 180))
    np5 = make_newspaper_photo(title="BÁO BÌNH THUẬN 2008", scene_fn=scene_np5)
    save_image(np5, "chuyen-tau-dem-muong-man", "d01-bao-chi.webp")

    def plan_bp5(d, w, h):
        d.rectangle([60, 200, 740, 420], outline=(220, 240, 255), width=4)
        for i in range(6):
            cx = 80 + i * 105
            d.rectangle([cx, 215, cx + 95, 350], outline=(140, 180, 220), width=2)
            d.text((cx + 47, 280), f"KH.{i+1}", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 13), anchor="mm")
        d.rectangle([395, 215, 490, 350], fill=(80, 130, 180), outline=(240, 80, 80), width=3)
        d.text((442, 280), "KH.4 (ÁN)", fill=(255, 255, 255), font=get_font(FONT_HELVETICA, 13), anchor="mm")
        d.line([(80, 365), (710, 365)], fill=(180, 210, 240), width=2)
        d.text((400, 390), "HÀNH LANG LỐI ĐI TOA XE", fill=(180, 210, 240), font=get_font(FONT_HELVETICA, 12), anchor="mm")
    bp5 = make_blueprint(title="SƠ ĐỒ MẶT BẰNG TOA 6 TÀU THỐNG NHẤT SE3", plan_fn=plan_bp5)
    save_image(bp5, "chuyen-tau-dem-muong-man", "d03-so-do-toa-tau.webp")

    tk5 = make_ticket_scan(title="ĐƯỜNG SẮT VIỆT NAM • VÉ TÀU THỐNG NHẤT", details=[
        ("Tàu / Toa", "SE3 / Toa 06"),
        ("Khoang / Giường", "Khoang 04 / Giường 02 tầng 1"),
        ("Hành trình", "Hà Nội → Sài Gòn (Ga Mường Mán)"),
        ("Ngày đi", "17/09/2008 • 22h00"),
        ("Hành khách", "Vũ Đình Cường")
    ])
    save_image(tk5, "chuyen-tau-dem-muong-man", "d09-ve-tau-se3.webp")

    # Case 06: bong-nang-hoi-an
    np6 = make_newspaper_photo(title="BÁO QUẢNG NAM 2005", scene_fn=lambda d, w, h: (
        # Hoi An ancient street mossy wall
        d.rectangle([0, 0, w, h], fill=(180, 170, 140)),
        d.polygon([(100, 240), (700, 220), (680, 480), (120, 480)], fill=(90, 85, 70)),
        # Well shape
        d.ellipse([340, 320, 480, 420], fill=(45, 45, 50))
    ))
    save_image(np6, "bong-nang-hoi-an", "d01-bao-chi.webp")

    bp6 = make_blueprint(title="SƠ ĐỒ TỪ ĐƯỜNG HỌ LƯƠNG & GIẾNG BÁ LỄ", plan_fn=lambda d, w, h: (
        # Ancestral Hall
        d.rectangle([100, 120, 360, 420], outline=(220, 240, 255), width=3),
        d.text((230, 270), "TỪ ĐƯỜNG HỌ LƯƠNG", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 13), anchor="mm"),
        # Brick alley to well
        d.line([(360, 270), (560, 270)], fill=(180, 210, 240), width=18),
        # Ba Le Well
        d.ellipse([560, 220, 680, 320], fill=(80, 130, 180), outline=(220, 240, 255), width=3),
        d.text((620, 270), "GIẾNG BÁ LỄ", fill=(255, 255, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Sun shadow angles
        d.line([(620, 270), (520, 180)], fill=(240, 220, 60), width=3),
        d.text((510, 160), "BÓNG NẮNG 16H (CHIỀU TÀ)", fill=(240, 220, 60), font=get_font(FONT_HELVETICA, 11))
    ))
    save_image(bp6, "bong-nang-hoi-an", "d04-so-do-tu-duong.webp")

    # Case 07: lua-than-tay-nguyen
    np7 = make_newspaper_photo(title="AN NINH ĐẮK LẮK 2001", scene_fn=lambda d, w, h: (
        # Burned rubble of barn
        d.rectangle([0, 0, w, h], fill=(60, 55, 50)),
        d.polygon([(160, 280), (400, 180), (640, 280)], fill=(30, 28, 26)),
        d.line([(240, 280), (220, 440)], fill=(20, 18, 16), width=14)
    ))
    save_image(np7, "lua-than-tay-nguyen", "d01-bao-chi.webp")

    bp7 = make_blueprint(title="SƠ ĐỒ BUÔN EA KRAL & KHO CÀ PHÊ", plan_fn=lambda d, w, h: (
        d.rectangle([120, 140, 360, 320], outline=(220, 240, 255), width=2),
        d.text((240, 230), "NHÀ DÀI Ê-ĐÊ", fill=(180, 210, 240), font=get_font(FONT_HELVETICA, 13), anchor="mm"),
        d.rectangle([440, 180, 660, 380], fill=(80, 130, 180)), # Burned warehouse
        d.text((550, 280), "KHO SẤY CÀ PHÊ (CHÁY)", fill=(255, 255, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm")
    ))
    save_image(bp7, "lua-than-tay-nguyen", "d03-so-do-buon-lang.webp")

    mg7 = make_mugshot_profile(name="AMA RIN (GIÀ LÀNG)", details=[
        ("Năm sinh", "1940 (61 tuổi)"),
        ("Dân tộc", "Ê-đê"),
        ("Địa bàn", "Buôn Ea Kral, Krông Pắc"),
        ("Vai trò", "Chủ sở hữu kho thóc & xà gạc")
    ])
    save_image(mg7, "lua-than-tay-nguyen", "d06-anh-the.webp")

    # Case 08: gac-den-hon-dau
    np8 = make_newspaper_photo(title="BÁO HẢI PHÒNG 1998", scene_fn=lambda d, w, h: (
        # Lighthouse tower in stormy waves
        d.rectangle([0, 0, w, h], fill=(80, 95, 110)),
        d.polygon([(360, 100), (440, 100), (460, 460), (340, 460)], fill=(220, 220, 225)),
        # Lantern room
        d.rectangle([350, 70, 450, 100], fill=(240, 240, 180))
    ))
    save_image(np8, "gac-den-hon-dau", "d01-bao-chi.webp")

    bp8 = make_blueprint(title="BẢN ĐỒ ĐẢO HÒN DÁU & CÁC TRẠM TRỰC", plan_fn=lambda d, w, h: (
        # Island outline
        d.ellipse([100, 100, 680, 500], outline=(100, 160, 220), width=3),
        # Lighthouse
        d.ellipse([370, 200, 430, 260], fill=(80, 130, 180)),
        d.text((400, 180), "THÁP HẢI ĐĂNG (ĐỈNH ĐỒI)", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Yanmar generator house
        d.rectangle([220, 340, 340, 420], fill=(80, 130, 180)),
        d.text((280, 380), "NHÀ MÁY PHÁT YANMAR", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 11), anchor="mm"),
        # Rocky path
        d.line([(400, 260), (280, 340)], fill=(220, 180, 60), width=3)
    ))
    save_image(bp8, "gac-den-hon-dau", "d02-ban-do-dao.webp")

    at8 = make_autopsy_chart(victim_name="ĐẶNG VĂN TIẾN (TRẠM TRƯỞNG)", wound_fn=lambda d, w, h: (
        d.ellipse([510, 135, 535, 155], fill=(200, 35, 35)),
        d.line([(535, 145), (630, 145)], fill=(180, 30, 30), width=2),
        d.text((635, 140), "VẾT RÁCH HỘP SỌ DO CỜ-LÊ", fill=(180, 30, 30), font=get_font(FONT_HELVETICA, 12))
    ))
    save_image(at8, "gac-den-hon-dau", "d04-giai-phau.webp")

    # Case 09: vang-bong-cho-lon
    np9 = make_newspaper_photo(title="SÀI GÒN GIẢI PHÓNG 1995", scene_fn=lambda d, w, h: (
        d.rectangle([0, 0, w, h], fill=(160, 150, 130)),
        d.rectangle([160, 160, 640, 440], fill=(60, 50, 40)),
        d.text((400, 220), "TIỆM VÀNG VẠN THÀNH", fill=(230, 210, 80), font=get_font(FONT_HELVETICA, 24), anchor="mm")
    ))
    save_image(np9, "vang-bong-cho-lon", "d01-bao-chi.webp")

    bp9 = make_blueprint(title="SƠ ĐỒ TIỆM KIM HOÀN VẠN THÀNH", plan_fn=lambda d, w, h: (
        d.rectangle([120, 120, 600, 480], outline=(220, 240, 255), width=4),
        d.rectangle([160, 160, 560, 240], fill=(80, 130, 180)), # Glass display counters
        d.text((360, 200), "TỦ KÍNH TRƯNG BÀY VÀNG", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Hidden safe room
        d.rectangle([480, 360, 580, 460], outline=(240, 100, 100), width=3),
        d.text((530, 410), "KÉT SẮT CHUBB", fill=(240, 100, 100), font=get_font(FONT_HELVETICA, 11), anchor="mm")
    ))
    save_image(bp9, "vang-bong-cho-lon", "d04-so-do-tiem-vang.webp")

    tk9 = make_ticket_scan(title="RẠP HÀO HUÊ • ĐÊM CA NHẠC DẠ THẢO", details=[
        ("Suất diễn", "19h30 - 21h30 (14/08/1995)"),
        ("Khán phòng", "Tầng 1 • Ghế A-14"),
        ("Giá vé", "25.000 VNĐ"),
        ("Người mua", "Trương Chấn Hào (Dấu mộc xé)")
    ])
    save_image(tk9, "vang-bong-cho-lon", "d09-cuong-ve.webp")

    # Case 10: tieng-huan-van-don
    np10 = make_newspaper_photo(title="BÁO QUẢNG NINH 2004", scene_fn=lambda d, w, h: (
        # Fishing boat docked at Cái Rồng port
        d.rectangle([0, 0, w, h], fill=(120, 135, 145)),
        d.polygon([(140, 320), (660, 320), (580, 440), (220, 440)], fill=(40, 45, 50))
    ))
    save_image(np10, "tieng-huan-van-don", "d01-bao-chi.webp")

    def plan_bp10(d, w, h):
        d.polygon([(80, 180), (720, 180), (620, 460), (180, 460)], outline=(220, 240, 255), width=4)
        for idx in range(3):
            hx = 180 + idx * 160
            d.rectangle([hx, 220, hx + 130, 420], outline=(140, 180, 220), width=2)
            d.text((hx + 65, 300), f"HẦM {idx+1}", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 13), anchor="mm")
        d.rectangle([500, 220, 630, 420], fill=(80, 130, 180)) # Hold 3
        d.text((565, 320), "HẦM 3 (CO2)", fill=(255, 240, 80), font=get_font(FONT_HELVETICA, 12), anchor="mm")
    bp10 = make_blueprint(title="MẶT CẮT HẦM LẠNH TÀU CÁ QN-9288-TS", plan_fn=plan_bp10)
    save_image(bp10, "tieng-huan-van-don", "d04-so-do-tau-ca.webp")

    at10 = make_autopsy_chart(victim_name="TRẦN VĂN ĐẠT (THUYỀN TRƯỞNG)", wound_fn=lambda d, w, h: (
        d.ellipse([220, 220, 260, 260], fill=(60, 80, 160)),
        d.line([(260, 240), (350, 240)], fill=(40, 60, 140), width=2),
        d.text((355, 235), "TÍM TÁI NỘI TẠNG DO NGẠT KHÍ CO2", fill=(30, 50, 130), font=get_font(FONT_HELVETICA, 12))
    ))
    save_image(at10, "tieng-huan-van-don", "d03-giai-phau.webp")

    # Case 11: hoi-chuong-chua-thay
    np11 = make_newspaper_photo(title="BẢN TIN HÀ TÂY 1997", scene_fn=lambda d, w, h: (
        # Sai Son mountain and Thay pagoda
        d.rectangle([0, 0, w, h], fill=(150, 155, 150)),
        d.polygon([(100, 260), (320, 120), (540, 260)], fill=(70, 75, 70)),
        d.rectangle([200, 260, 440, 420], fill=(50, 45, 40))
    ))
    save_image(np11, "hoi-chuong-chua-thay", "d01-bao-chi.webp")

    bp11 = make_blueprint(title="SƠ ĐỒ GÁC CHUÔNG VÀ ĐIỆN PHẬT CHÙA THẦY", plan_fn=lambda d, w, h: (
        d.rectangle([120, 140, 380, 460], outline=(220, 240, 255), width=3),
        d.text((250, 300), "TÒA CHÍNH ĐIỆN", fill=(180, 210, 240), font=get_font(FONT_HELVETICA, 13), anchor="mm"),
        # Bell tower
        d.rectangle([460, 180, 640, 380], fill=(80, 130, 180)),
        d.text((550, 280), "GÁC ĐẠI HỒNG CHUNG", fill=(255, 255, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Water gutter
        d.line([(380, 220), (460, 220)], fill=(120, 220, 255), width=4),
        d.text((420, 200), "MÁNG NƯỚC", fill=(120, 220, 255), font=get_font(FONT_HELVETICA, 11), anchor="mm")
    ))
    save_image(bp11, "hoi-chuong-chua-thay", "d03-so-do-chua.webp")

    # d08 mechanism sketch
    img_sk11 = Image.new('RGB', (800, 600), (242, 238, 226))
    d_sk11 = ImageDraw.Draw(img_sk11)
    d_sk11.text((50, 40), "SƠ ĐỒ NGUYÊN LÝ BẪY NƯỚC THỦY LỰC ĐÒN BẨY", fill=(30, 30, 35), font=get_font(FONT_HELVETICA, 18))
    # Bamboo tube lever
    d_sk11.polygon([(220, 240), (580, 200), (580, 260), (220, 300)], fill=(160, 175, 110), outline=(80, 90, 50), width=3)
    d_sk11.ellipse([390, 240, 410, 260], fill=(20, 20, 20)) # Fulcrum
    d_sk11.polygon([(380, 260), (420, 260), (400, 340)], fill=(80, 80, 85)) # Support
    # Water drop
    d_sk11.ellipse([230, 160, 250, 190], fill=(60, 140, 220))
    d_sk11.text((240, 130), "NƯỚC MÁNG XỐI NHỎ GIỌT", fill=(30, 90, 160), font=get_font(FONT_HELVETICA, 13), anchor="mm")
    d_sk11.text((580, 290), "SỢI CƯỚC NỐI CHÀY GÕ", fill=(180, 40, 30), font=get_font(FONT_HELVETICA, 13))
    save_image(img_sk11, "hoi-chuong-chua-thay", "d08-so-do-co-hoc.webp")

    # Case 12: vet-muc-lang-dong-ho
    def scene_np12(d, w, h):
        d.rectangle([0, 0, w, h], fill=(165, 160, 150))
        d.line([(0, 340), (w, 360)], fill=(80, 75, 65), width=25) # Dike
        for ix in range(80, 720, 120):
            d.ellipse([ix, 280, ix + 90, 330], fill=(240, 240, 235))
    np12 = make_newspaper_photo(title="VĂN HÓA BẮC NINH 2000", scene_fn=scene_np12)
    save_image(np12, "vet-muc-lang-dong-ho", "d01-bao-chi.webp")

    bp12 = make_blueprint(title="SƠ ĐỒ LÀNG ĐÔNG HỒ & LỐI BỜ ĐÊ SÔNG ĐUỐNG", plan_fn=lambda d, w, h: (
        # River
        d.arc([40, -100, 760, 300], 0, 180, fill=(80, 160, 220), width=35),
        d.text((400, 120), "SÔNG ĐUỐNG", fill=(140, 200, 255), font=get_font(FONT_HELVETICA, 14), anchor="mm"),
        # Master Thao workshop
        d.rectangle([280, 260, 500, 420], fill=(80, 130, 180)),
        d.text((390, 340), "XƯỞNG TRANH CỤ THAO", fill=(255, 255, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        d.text((220, 440), "BÃI BÙN PHÙ SA (DÉP TỔ ONG)", fill=(240, 180, 60), font=get_font(FONT_HELVETICA, 11))
    ))
    save_image(bp12, "vet-muc-lang-dong-ho", "d04-so-do-lang-tranh.webp")

    # d07 Dong Ho print scan
    img_dh12 = Image.new('RGB', (800, 600), (242, 236, 215)) # DIEP paper sparkle tone
    d_dh12 = ImageDraw.Draw(img_dh12)
    d_dh12.text((50, 40), "BẢN DẬP THỬ TRANH DÂN GIAN ĐÔNG HỒ", fill=(40, 35, 30), font=get_font(FONT_HELVETICA, 18))
    # Red woodblock print outlines (Đám cưới chuột)
    d_dh12.rectangle([120, 90, 680, 520], outline=(180, 40, 35), width=4)
    # Mice silhouettes
    for mx in range(160, 620, 110):
        d_dh12.ellipse([mx, 260, mx + 50, 320], fill=(195, 35, 30))
        d_dh12.line([(mx+20, 320), (mx+10, 360)], fill=(195, 35, 30), width=4)
    d_dh12.text((400, 460), "TRANH: ĐÁM CƯỚI CHUỘT (PHẨM SON ĐỎ)", fill=(180, 30, 25), font=get_font(FONT_HELVETICA, 14), anchor="mm")
    save_image(img_dh12, "vet-muc-lang-dong-ho", "d07-tranh-dong-ho.webp")

    # Case 13: ly-tra-trao-doc
    np13 = make_newspaper_photo(title="TUỔI TRẺ ONLINE 2021", scene_fn=lambda d, w, h: (
        d.rectangle([0, 0, w, h], fill=(200, 205, 210)),
        d.rectangle([160, 120, 640, 400], fill=(45, 50, 55)),
        d.text((400, 200), "THE ALLEY - NGUYỄN HUỆ", fill=(240, 240, 245), font=get_font(FONT_HELVETICA, 22), anchor="mm")
    ))
    save_image(np13, "ly-tra-trao-doc", "d01-bao-chi.webp")

    bp13 = make_blueprint(title="SƠ ĐỒ QUÁN TRÀ SỮA THE ALLEY (QUẬN 1)", plan_fn=lambda d, w, h: (
        d.rectangle([100, 120, 680, 480], outline=(220, 240, 255), width=4),
        # Order counter & sealing machine
        d.rectangle([140, 160, 420, 250], fill=(80, 130, 180)),
        d.text((280, 205), "QUẦY PHA CHẾ & MÁY DẬP NẮP", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Table 04 where victim sat
        d.ellipse([500, 320, 580, 400], fill=(240, 100, 100)),
        d.text((540, 360), "BÀN SỐ 04 (NẠN NHÂN)", fill=(255, 255, 255), font=get_font(FONT_HELVETICA, 11), anchor="mm")
    ))
    save_image(bp13, "ly-tra-trao-doc", "d03-so-do-quan-tra.webp")

    tk13 = make_ticket_scan(title="HÓA ĐƠN THANH TOÁN • THE ALLEY", details=[
        ("Số hóa đơn", "HD-2021-0819-44"),
        ("Giờ in", "14:22:15 • 19/08/2021"),
        ("Mặt hàng", "2x Trà sữa trân châu đường đen (Size M)"),
        ("Đơn giá", "75.000 x 2 = 150.000 VNĐ"),
        ("Thu ngân", "Trần Thu Trang (Ca chiều)")
    ])
    save_image(tk13, "ly-tra-trao-doc", "d07-hoa-don-tra-sua.webp")

    # Case 14: buc-thu-dem-tuyet-trang
    np14 = make_newspaper_photo(title="CNN BREAKING NEWS 1996", scene_fn=lambda d, w, h: (
        # Snow villa Boulder Colorado
        d.rectangle([0, 0, w, h], fill=(210, 215, 225)),
        d.polygon([(140, 260), (400, 160), (660, 260)], fill=(60, 65, 75)),
        d.rectangle([180, 260, 620, 440], fill=(45, 50, 58))
    ))
    save_image(np14, "buc-thu-dem-tuyet-trang", "d01-bao-chi.webp")

    bp14 = make_blueprint(title="SƠ ĐỒ TẦNG HẦM BIỆT THỰ RAMSEY (BOULDER)", plan_fn=lambda d, w, h: (
        d.rectangle([100, 120, 680, 480], outline=(220, 240, 255), width=4),
        # Wine cellar (body found)
        d.rectangle([480, 160, 640, 320], fill=(80, 130, 180)),
        d.text((560, 240), "HẦM RƯỢU (THI THỂ)", fill=(255, 240, 80), font=get_font(FONT_HELVETICA, 12), anchor="mm"),
        # Broken basement window
        d.line([(640, 200), (680, 200)], fill=(240, 80, 80), width=6),
        d.text((610, 145), "Ô CỬA SỔ VỠ", fill=(240, 100, 100), font=get_font(FONT_HELVETICA, 11)),
        # Spiral staircase where ransom note was found
        d.ellipse([140, 360, 240, 440], outline=(180, 210, 240), width=2),
        d.text((190, 400), "CẦU THANG (THƯ TỐNG TIỀN)", fill=(180, 210, 240), font=get_font(FONT_HELVETICA, 10), anchor="mm")
    ))
    save_image(bp14, "buc-thu-dem-tuyet-trang", "d04-so-do-biet-thu.webp")

    mg14 = make_mugshot_profile(name="JONBENÉT RAMSEY (6 TUỔI)", details=[
        ("Danh hiệu", "Little Miss Colorado 1995"),
        ("Ngày sinh", "06/08/1990"),
        ("Hiện trường", "755 15th St, Boulder, CO"),
        ("Tình trạng", "Nạn nhân đêm Giáng sinh 1996")
    ])
    save_image(mg14, "buc-thu-dem-tuyet-trang", "d07-anh-hoa-khoi.webp")

    # Case 15: dem-sung-no-tay-son
    np15 = make_newspaper_photo(title="AN NINH THỦ ĐÔ 1999", scene_fn=lambda d, w, h: (
        d.rectangle([0, 0, w, h], fill=(35, 38, 42)),
        d.rectangle([140, 160, 660, 420], fill=(70, 75, 80)),
        d.text((400, 220), "TIỆM VÀNG KIM SINH - PHỐ TÂY SƠN", fill=(240, 240, 245), font=get_font(FONT_HELVETICA, 20), anchor="mm")
    ))
    save_image(np15, "dem-sung-no-tay-son", "d01-bao-chi.webp")

    bp15 = make_blueprint(title="SƠ ĐỒ HIỆN TRƯỜNG TIỆM VÀNG KIM SINH", plan_fn=lambda d, w, h: (
        d.rectangle([120, 120, 480, 460], outline=(220, 240, 255), width=4),
        d.text((300, 240), "TIỆM VÀNG KIM SINH", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 13), anchor="mm"),
        # Exit alleyway
        d.line([(480, 360), (660, 360)], fill=(180, 210, 240), width=18),
        d.text((570, 335), "NGÕ CỤT THOÁT HIỂM", fill=(240, 200, 60), font=get_font(FONT_HELVETICA, 11), anchor="mm")
    ))
    save_image(bp15, "dem-sung-no-tay-son", "d04-so-do-hien-truong.webp")

    tk15 = make_ticket_scan(title="BẾN PHÀ ĐEN • VÉ QUA SÔNG HỒNG", details=[
        ("Chuyến phà", "Chuyến đêm 23h45 (18/07/1999)"),
        ("Loại vé", "Bộ hành + Xe máy Simson"),
        ("Mức thu", "2.000 VNĐ"),
        ("Kiểm soát", "Dấu bấm lỗ góc phải")
    ])
    save_image(tk15, "dem-sung-no-tay-son", "d12-ve-pha-den.webp")

    # Case 16: quai-vat-21-khuon-mat
    np16 = make_newspaper_photo(title="ASAHI SHIMBUN 1984", scene_fn=lambda d, w, h: (
        d.rectangle([0, 0, w, h], fill=(180, 185, 190)),
        d.rectangle([120, 140, 680, 420], fill=(55, 60, 70)),
        d.text((400, 210), "GLICO HEADQUARTERS - OSAKA", fill=(245, 245, 250), font=get_font(FONT_HELVETICA, 20), anchor="mm")
    ))
    save_image(np16, "quai-vat-21-khuon-mat", "d01-bao-chi.webp")

    # d08 Fox-Eyed Man police sketch
    img_sk16 = Image.new('RGB', (800, 600), (235, 230, 220))
    d_sk16 = ImageDraw.Draw(img_sk16)
    d_sk16.text((50, 40), "BẢN PHÁC HỌA TRUY NÃ CẢNH SÁT OSAKA (1984)", fill=(30, 30, 35), font=get_font(FONT_HELVETICA, 18))
    d_sk16.text((50, 70), "ĐỐI TƯỢNG: 'NGƯỜI ĐÀN ÔNG MẮT CÁO' (FOX-EYED MAN)", fill=(180, 35, 30), font=get_font(FONT_COURIER, 14))
    # Hand-drawn charcoal sketch look
    cx, cy = 400, 320
    # Baseball cap
    d_sk16.polygon([(cx - 110, cy - 80), (cx + 110, cy - 80), (cx + 140, cy - 40), (cx - 140, cy - 40)], fill=(50, 65, 90))
    # Face outline
    d_sk16.ellipse([cx - 90, cy - 50, cx + 90, cy + 150], fill=(225, 220, 210), outline=(50, 50, 55), width=3)
    # Slanted fox eyes
    d_sk16.line([(cx - 60, cy + 20), (cx - 15, cy + 30)], fill=(30, 30, 35), width=6)
    d_sk16.line([(cx + 15, cy + 30), (cx + 60, cy + 20)], fill=(30, 30, 35), width=6)
    # Eyebrows
    d_sk16.line([(cx - 70, cy), (cx - 15, cy + 10)], fill=(30, 30, 35), width=4)
    d_sk16.line([(cx + 15, cy + 10), (cx + 70, cy)], fill=(30, 30, 35), width=4)
    # Nose & mouth
    d_sk16.line([(cx, cy + 35), (cx - 10, cy + 75), (cx + 5, cy + 78)], fill=(30, 30, 35), width=3)
    d_sk16.line([(cx - 35, cy + 105), (cx + 35, cy + 105)], fill=(30, 30, 35), width=4)
    save_image(img_sk16, "quai-vat-21-khuon-mat", "d08-phac-hoa-mat-cao.webp")

    # d15 Glico stock chart plunge
    img_st16 = Image.new('RGB', (800, 600), (25, 28, 35))
    d_st16 = ImageDraw.Draw(img_st16)
    d_st16.text((50, 40), "BIỂU ĐỒ GIÁ CỔ PHIẾU TẬP ĐOÀN GLICO (1984)", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 18))
    # Grid lines
    for gy in range(120, 500, 60):
        d_st16.line([(80, gy), (720, gy)], fill=(45, 52, 65), width=1)
    # Crashing stock line
    d_st16.line([(80, 160), (200, 170), (280, 380), (360, 410), (520, 440), (700, 460)], fill=(240, 60, 60), width=4)
    d_st16.text((290, 350), "BẮT CÓC EZAKI (-45%)", fill=(240, 80, 80), font=get_font(FONT_HELVETICA, 12))
    d_st16.text((530, 415), "ĐE DỌA XYANUA (-70%)", fill=(240, 80, 80), font=get_font(FONT_HELVETICA, 12))
    save_image(img_st16, "quai-vat-21-khuon-mat", "d15-bieu-do-co-phieu.webp")

    print("All 44 expanded visual assets generated successfully!")

if __name__ == "__main__":
    run_all()
