#!/usr/bin/env python3
import os
import random
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/Users/huynguyen/Documents/game_pha_an/public/cases/chuyen-tau-dem-muong-man/images"
os.makedirs(OUT_DIR, exist_ok=True)

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

def add_grain(img, strength=8):
    w, h = img.size
    noise = Image.new('RGB', (w, h))
    npix = noise.load()
    random.seed(105)
    for y in range(h):
        for x in range(w):
            v = random.randint(128 - strength, 128 + strength)
            npix[x, y] = (v, v, v)
    return Image.blend(img, noise, 0.08)

def save_webp(img, filename, quality=88):
    out_img = add_grain(img)
    p = os.path.join(OUT_DIR, filename)
    out_img.save(p, "WEBP", quality=quality)
    print(f"✓ Saved: {filename} ({os.path.getsize(p)} bytes)")

def optimize_cover():
    p = os.path.join(OUT_DIR, "cover.webp")
    if os.path.exists(p):
        im = Image.open(p)
        # downscale slightly if large and save as proper WebP
        if im.size[0] > 900:
            ratio = 900 / im.size[0]
            im = im.resize((900, int(im.size[1] * ratio)), Image.Resampling.LANCZOS)
        im.save(p, "WEBP", quality=84)
        print(f"✓ Optimized cover.webp: {os.path.getsize(p)} bytes")

# 1. d01-bao-chi.webp (800x480) - Vintage Newspaper Scan Báo Bình Thuận 13/10/2008
def render_d01():
    w, h = 800, 480
    img = Image.new('RGB', (w, h), (244, 240, 230))
    draw = ImageDraw.Draw(img)
    
    f_mast = get_font(FONT_HELVETICA, 32)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_head = get_font(FONT_HELVETICA, 20)
    f_bold = get_font(FONT_HELVETICA, 13)
    f_text = get_font(FONT_HELVETICA, 11)
    
    # Border
    draw.rectangle([15, 15, w - 15, h - 15], outline=(90, 80, 70), width=2)
    
    # Masthead
    draw.rectangle([25, 25, w - 25, 80], fill=(235, 230, 218), outline=(120, 110, 100))
    draw.text((40, 32), "BÁO BÌNH THUẬN", fill=(140, 20, 20), font=f_mast)
    draw.text((w - 240, 40), "SỐ 2841 • THỨ HAI, 13/10/2008", fill=(80, 70, 60), font=f_sub)
    draw.text((w - 240, 58), "TIẾNG NÓI CỦA ĐẢNG BỘ VÀ NHÂN DÂN BÌNH THUẬN", fill=(110, 100, 90), font=f_sub)
    draw.line([(25, 85), (w - 25, 85)], fill=(90, 80, 70), width=2)
    
    # Main Headline
    draw.text((30, 96), "ÁN MẠNG TRONG PHÒNG KHOÁ KÍN TRÊN ĐOÀN TÀU SE3", fill=(20, 20, 25), font=f_head)
    draw.text((30, 124), "Một giám đốc doanh nghiệp khoáng sản tử vong bí ẩn tại khoang giường nằm số 4 khi tàu qua đèo Cà Ná", fill=(80, 40, 30), font=f_bold)
    draw.line([(30, 146), (w - 30, 146)], fill=(180, 170, 160), width=1)
    
    # Photo box
    draw.rectangle([30, 158, 380, 395], fill=(30, 35, 45), outline=(100, 90, 80), width=2)
    # Train silhouette at dark station
    draw.rectangle([50, 230, 360, 350], fill=(50, 60, 75))
    draw.rectangle([50, 210, 360, 230], fill=(80, 95, 120))
    # Locomotive headlights
    draw.ellipse([70, 260, 110, 300], fill=(255, 250, 200))
    draw.polygon([(90, 280), (360, 240), (360, 350)], fill=(70, 80, 95))
    # Station sign MƯỜNG MÁN
    draw.rectangle([140, 175, 270, 205], fill=(20, 40, 70), outline=(220, 220, 220))
    draw.text((205, 190), "GA MƯỜNG MÁN", fill=(255, 255, 255), font=f_bold, anchor="mm")
    # Red police beacon
    draw.ellipse([310, 290, 335, 315], fill=(220, 40, 40))
    draw.text((205, 375), "Ảnh: Đoàn tàu SE3 dừng khẩn cấp lúc 05h30 sáng tại ga Mường Mán", fill=(200, 210, 220), font=get_font(FONT_HELVETICA, 10), anchor="mm")
    
    # Text Columns on the right
    col_x = 400
    paras = [
        "Rạng sáng nay 13/10, đoàn tàu khách Thống Nhất SE3 hành trình Hà",
        "Nội - TP.HCM đã phải phong tỏa khẩn cấp toa xe số 6 khi cập ga Mường",
        "Mán. Hành khách Đặng Quốc Vinh (58 tuổi, ngụ TP.HCM), Giám đốc",
        "Công ty Khoáng sản Rạng Đông được phát hiện tử vong ngay trên",
        "giường ngủ với vết đâm chí mạng ở vùng ngực trái.",
        "",
        "Điều kỳ lạ gây chấn động dư luận là toàn bộ cửa sổ khoang tàu được",
        "lắp kính chết kiên cố, còn cửa trượt ra hành lang bị gài chốt an toàn",
        "tuyệt đối từ bên trong. Nhân viên đường sắt phải dùng chìa kỹ thuật",
        "lách qua khe hẹp nạy mạnh mới mở được chốt khóa.",
        "",
        "Chiếc cặp da chứa 200 triệu đồng tiền mặt và hồ sơ dự thầu mỏ titan",
        "của nạn nhân đã biến mất. Công an tỉnh Bình Thuận đang phối hợp cùng",
        "Cục Cảnh sát Giao thông đường sắt khẩn trương phong tỏa khám nghiệm."
    ]
    cur_y = 158
    for line in paras:
        if line == "":
            cur_y += 6
            continue
        draw.text((col_x, cur_y), line, fill=(40, 35, 30), font=f_text)
        cur_y += 16
        
    # Official stamp / date box bottom
    draw.rectangle([w - 200, h - 60, w - 30, h - 25], fill=(230, 225, 210), outline=(160, 150, 140))
    draw.text((w - 115, h - 42), "TƯ LIỆU VỤ ÁN HÌNH SỰ 2008", fill=(120, 30, 30), font=f_bold, anchor="mm")
    
    save_webp(img, "d01-bao-chi.webp")

# 2. d02-hien-truong-khoang-4.webp (800x600) - Crime Scene Photo Berth 4 Carriage 6
def render_d02():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (242, 244, 246))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    f_mono = get_font(FONT_COURIER, 11)
    
    # Border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(170, 180, 190), width=2)
    draw.rectangle([30, 30, w - 30, 75], fill=(225, 232, 240), outline=(160, 175, 185))
    draw.text((45, 38), "CÔNG AN TỈNH BÌNH THUẬN - PHÒNG KỸ THUẬT HÌNH SỰ (PC54)", fill=(30, 45, 60), font=f_bold)
    draw.text((45, 54), "BẢN ẢNH KHÁM NGHIỆM HIỆN TRƯỜNG: KHOANG SỐ 4 - TOA 6 TÀU SE3", fill=(150, 25, 25), font=f_title)
    
    # Main Photo Area: Interior of train sleeper compartment
    draw.rectangle([40, 90, 520, 470], fill=(35, 40, 50), outline=(100, 110, 125), width=2)
    
    # Train wall panels (wood-grain laminate)
    draw.rectangle([42, 92, 518, 220], fill=(95, 75, 55))
    # Fixed window looking out to night
    draw.rectangle([180, 110, 380, 240], fill=(15, 20, 30), outline=(180, 190, 200), width=3)
    # Distant dark sand dunes & sea under crescent moon
    draw.ellipse([330, 125, 360, 155], fill=(230, 235, 240))
    draw.polygon([(185, 210), (260, 185), (320, 220), (375, 195), (375, 238), (185, 238)], fill=(10, 15, 20))
    
    # Lower bunk bed (giường số 1)
    draw.rectangle([50, 270, 510, 440], fill=(45, 80, 130), outline=(160, 170, 180), width=2) # blue mattress
    # White sheet & blue blanket rumpled
    draw.polygon([(120, 290), (450, 280), (480, 420), (140, 430)], fill=(220, 225, 235))
    draw.polygon([(260, 320), (470, 300), (460, 410), (280, 420)], fill=(30, 60, 100))
    # Blood stain near pillow
    draw.ellipse([140, 300, 220, 360], fill=(110, 20, 20))
    draw.ellipse([160, 315, 200, 345], fill=(80, 15, 15))
    
    # Upper luggage rack empty
    draw.rectangle([60, 92, 160, 130], fill=(50, 55, 65), outline=(130, 140, 150))
    draw.text((110, 110), "VỊ TRÍ CẶP DA\n(ĐÃ BỊ CƯỚP)", fill=(255, 150, 150), font=get_font(FONT_HELVETICA, 9), anchor="mm")
    
    # Evidence markers
    # Marker 1: Blood stain
    draw.polygon([(125, 285), (145, 285), (135, 260)], fill=(240, 200, 20))
    draw.text((135, 278), "1", fill=(0, 0, 0), font=f_bold, anchor="mm")
    # Marker 2: Sliding door latch
    draw.polygon([(470, 240), (490, 240), (480, 215)], fill=(240, 200, 20))
    draw.text((480, 233), "2", fill=(0, 0, 0), font=f_bold, anchor="mm")
    
    # Right panel: Technical examination details
    draw.rectangle([535, 90, w - 40, 470], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((550, 105), "ĐẶC ĐIỂM HIỆN TRƯỜNG KHOANG 4", fill=(30, 45, 60), font=f_bold)
    draw.line([(550, 125), (w - 55, 125)], fill=(200, 210, 220), width=1)
    
    details = [
        "• Thời gian khám nghiệm: 06h15 ngày 13/10/2008",
        "• Địa điểm: Toa 6, đoàn tàu Thống Nhất SE3",
        "• Nạn nhân: Đặng Quốc Vinh (58 tuổi, Giám đốc)",
        "• Vị trí: Giường số 1 tầng dưới bên trái",
        "• Cửa sổ kính: 2 lớp chịu lực cố định nguyên vẹn",
        "• Cửa trượt: Khóa chặt chốt lẫy gập từ bên trong",
        "• Dấu vết xâm nhập: Không có dấu cạy phá cơ học",
        "• Tài sản thất thoát:",
        "  - 01 cặp da màu nâu của nạn nhân",
        "  - 200.000.000 đồng tiền mặt (cọc 500k mới)",
        "  - Hồ sơ đấu thầu mỏ sa khoáng titan",
        "",
        "ĐÁNH GIÁ PHÒNG KÍN:",
        "Căn phòng hoàn toàn cô lập từ bên trong,",
        "nhân viên đường sắt phải dùng chìa kỹ thuật",
        "lách giật nảy chốt khóa mới mở được cửa."
    ]
    cur_y = 135
    for d in details:
        if "ĐÁNH GIÁ" in d:
            draw.text((550, cur_y), d, fill=(150, 20, 20), font=f_bold)
        else:
            draw.text((550, cur_y), d, fill=(45, 55, 65), font=get_font(FONT_HELVETICA, 10))
        cur_y += 18
        
    # Bottom stamp
    draw.rectangle([40, 485, w - 40, h - 35], fill=(235, 240, 245), outline=(170, 180, 190))
    draw.text((55, 500), "KỸ THUẬT VIÊN KHÁM NGHIỆM: ĐẠI ÚY TRẦN MINH ĐỨC (KÝ VÀ ĐÓNG DẤU)", fill=(60, 70, 80), font=f_bold)
    draw.text((55, 520), "KẾT LUẬN: HIỆN TRƯỜNG PHÒNG KÍN TỰ NHIÊN HOẶC CÓ THỦ PHÁP CƠ HỌC ĐẶC BIỆT.", fill=(150, 20, 20), font=f_bold)
    
    save_webp(img, "d02-hien-truong-khoang-4.webp")

# 3. d03-so-do-toa-tau.webp (800x600) - Blueprint of Carriage 6 SE3
def render_d03():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (18, 42, 74))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_bold = get_font(FONT_HELVETICA, 12)
    f_small = get_font(FONT_HELVETICA, 10)
    
    # Blueprint grid
    for x in range(0, w, 25):
        draw.line([(x, 0), (x, h)], fill=(28, 56, 94), width=1)
    for y in range(0, h, 25):
        draw.line([(0, y), (w, y)], fill=(28, 56, 94), width=1)
        
    # Title Block
    draw.rectangle([30, 25, w - 30, 80], outline=(100, 180, 255), fill=(12, 30, 56), width=2)
    draw.text((45, 36), "TỔNG CÔNG TY ĐƯỜNG SẮT VIỆT NAM • ĐOÀN TÀU THỐNG NHẤT SE3", fill=(140, 210, 255), font=f_bold)
    draw.text((45, 54), "SƠ ĐỒ BỐ TRÍ MẶT BẰNG TOA SỐ 06 (TOA GIƯỜNG NẰM KHOANG 4 ĐIỀU HÒA)", fill=(255, 255, 255), font=f_title)
    
    # Outer Carriage Boundary
    draw.rectangle([50, 140, 750, 480], outline=(220, 240, 255), fill=(24, 52, 90), width=4)
    
    # Left: Attendant Cabin & WC
    draw.rectangle([54, 144, 150, 360], fill=(30, 65, 110), outline=(140, 190, 240), width=2)
    draw.text((102, 230), "PHÒNG TRỰC\nTIẾP VIÊN\n(Trần V. Hữu)", fill=(200, 230, 255), font=f_small, anchor="mm")
    draw.rectangle([54, 360, 150, 476], fill=(25, 55, 95), outline=(140, 190, 240), width=2)
    draw.text((102, 418), "KHU VỆ SINH\n& BỒN RỬA", fill=(160, 200, 240), font=f_small, anchor="mm")
    
    # 7 Passenger Compartments
    cw = 80
    for i in range(1, 8):
        cx1 = 155 + (i - 1) * cw + (i - 1) * 5
        cx2 = cx1 + cw
        
        # Compartment room (top portion: y 144 to 360)
        if i == 4:
            # Crime scene: Khoang 4
            draw.rectangle([cx1, 144, cx2, 360], fill=(120, 35, 40), outline=(255, 80, 80), width=3)
            draw.text(((cx1 + cx2)//2, 165), "KHOANG 4", fill=(255, 255, 255), font=f_bold, anchor="mm")
            draw.text(((cx1 + cx2)//2, 185), "(HIỆN TRƯỜNG)", fill=(255, 180, 180), font=f_small, anchor="mm")
            draw.text(((cx1 + cx2)//2, 220), "G1: Đặng Q. Vinh\n(NẠN NHÂN †)", fill=(255, 230, 230), font=get_font(FONT_HELVETICA, 8), anchor="mm")
            draw.text(((cx1 + cx2)//2, 275), "G2: Bùi B. Thảo\n(Thư ký)", fill=(255, 230, 230), font=get_font(FONT_HELVETICA, 8), anchor="mm")
            draw.text(((cx1 + cx2)//2, 335), "[CỬA KHOÁ CHỐT]", fill=(255, 255, 100), font=get_font(FONT_HELVETICA, 8), anchor="mm")
        elif i == 2:
            # Suspect: Khoang 2
            draw.rectangle([cx1, 144, cx2, 360], fill=(45, 85, 140), outline=(255, 200, 50), width=2)
            draw.text(((cx1 + cx2)//2, 165), "KHOANG 2", fill=(255, 255, 255), font=f_bold, anchor="mm")
            draw.text(((cx1 + cx2)//2, 200), "G5: N.H. Long\n(NGHI PHẠM)", fill=(255, 230, 100), font=get_font(FONT_HELVETICA, 8), anchor="mm")
            draw.text(((cx1 + cx2)//2, 260), "Hộc điều hòa trần:\n[GIẤU 200 TRIỆU\nVÀ CẶP DA]", fill=(255, 180, 180), font=get_font(FONT_HELVETICA, 8), anchor="mm")
        else:
            draw.rectangle([cx1, 144, cx2, 360], fill=(30, 60, 100), outline=(120, 170, 220), width=1)
            draw.text(((cx1 + cx2)//2, 165), f"KHOANG {i}", fill=(200, 230, 255), font=f_bold, anchor="mm")
            if i == 1:
                draw.text(((cx1 + cx2)//2, 230), "(Trống vé)", fill=(150, 180, 210), font=f_small, anchor="mm")
            elif i == 3:
                draw.text(((cx1 + cx2)//2, 230), "Gia đình\ndu khách (4)", fill=(180, 210, 240), font=f_small, anchor="mm")
            else:
                draw.text(((cx1 + cx2)//2, 230), "Khách du lịch\ntheo đoàn", fill=(180, 210, 240), font=f_small, anchor="mm")
                
    # Hallway Corridor (bottom portion: y 375 to 475)
    draw.rectangle([155, 375, 746, 475], fill=(20, 45, 80), outline=(140, 190, 240), width=2)
    draw.text((450, 425), "◄ HÀNH LANG LỐI ĐI CHUNG TOA SỐ 6 (DÀI 20M) ►", fill=(220, 240, 255), font=f_bold, anchor="mm")
    
    # Arrow route from Compartment 2 to Compartment 4
    draw.line([(280, 400), (450, 400)], fill=(255, 80, 80), width=3)
    draw.polygon([(460, 400), (445, 393), (445, 407)], fill=(255, 80, 80))
    draw.text((365, 388), "Lộ trình Long di chuyển lúc 01h20", fill=(255, 120, 120), font=get_font(FONT_HELVETICA, 9), anchor="mm")
    
    # Bottom Legend
    draw.rectangle([30, 500, w - 30, 575], fill=(12, 30, 56), outline=(80, 150, 220), width=1)
    draw.text((45, 515), "CHÚ DẪN PHÁ ÁN:", fill=(255, 210, 100), font=f_bold)
    draw.text((45, 535), "1. Khoang 4 bị khoá chốt từ bên trong, Thảo ra căng-tin toa 4 lúc 00h20-03h00.", fill=(200, 220, 245), font=f_small)
    draw.text((45, 552), "2. Nguyễn Hoàng Long ở khoang 2 cách khoang 4 chỉ 2 vách ngăn, dễ dàng tiếp cận mà không bị trực toa phát hiện.", fill=(200, 220, 245), font=f_small)
    
    save_webp(img, "d03-so-do-toa-tau.webp")

# 4. d04-giam-dinh-phap-y.webp (800x600) - Forensic Autopsy Chart
def render_d04():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (242, 244, 246))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    f_mono = get_font(FONT_COURIER, 11)
    
    # Header
    draw.rectangle([20, 20, w - 20, h - 20], outline=(170, 180, 190), width=2)
    draw.rectangle([30, 30, w - 30, 75], fill=(228, 234, 240), outline=(160, 175, 185))
    draw.text((45, 38), "BỆNH VIỆN ĐA KHOA TỈNH BÌNH THUẬN - KHOA GIẢI PHẪU BỆNH", fill=(30, 45, 60), font=f_bold)
    draw.text((45, 54), "BẢN VẼ GIÁM ĐỊNH PHÁP Y THƯƠNG TÍCH TỬ THI: ĐẶNG QUỐC VINH (58 TUỔI)", fill=(140, 20, 20), font=f_title)
    
    # Left: Anatomical Chart of Chest & Neck
    draw.rectangle([40, 90, 420, 470], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((55, 105), "SƠ ĐỒ TỔN THƯƠNG VÙNG CỔ - NGỰC TRÁI", fill=(40, 50, 60), font=f_bold)
    
    # Neck & Torso outline
    draw.arc([130, 140, 330, 300], 180, 0, fill=(150, 160, 170), width=3) # head
    draw.line([(180, 250), (180, 310), (120, 340), (100, 450)], fill=(150, 160, 170), width=3) # left neck & shoulder
    draw.line([(280, 250), (280, 310), (340, 340), (360, 450)], fill=(150, 160, 170), width=3) # right neck & shoulder
    draw.line([(180, 310), (280, 310)], fill=(190, 200, 210), width=2) # collar line
    
    # Left clavicle bone
    draw.line([(180, 330), (120, 350)], fill=(120, 130, 140), width=4)
    # Right clavicle bone
    draw.line([(280, 330), (340, 350)], fill=(120, 130, 140), width=4)
    
    # Fatal stab wound
    wx, wy = 155, 360
    draw.ellipse([wx - 10, wy - 10, wx + 10, wy + 10], fill=(220, 30, 30), outline=(140, 10, 10), width=2)
    # Wound trajectory arrow (9cm deep)
    draw.line([(wx, wy), (wx + 30, wy + 60)], fill=(200, 20, 20), width=3)
    draw.polygon([(wx + 32, wy + 64), (wx + 22, wy + 55), (wx + 35, wy + 50)], fill=(200, 20, 20))
    draw.text((wx + 40, wy + 55), "Hướng đâm: Sâu 9cm\nrách tĩnh mạch & đỉnh phổi", fill=(180, 10, 10), font=get_font(FONT_HELVETICA, 10))
    
    # Right: Forensic Measurements
    draw.rectangle([435, 90, w - 40, 470], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((450, 105), "KẾT LUẬN GIÁM ĐỊNH Y PHÁP", fill=(30, 45, 60), font=f_bold)
    draw.line([(450, 125), (w - 55, 125)], fill=(200, 210, 220), width=1)
    
    med = [
        "1. VẾT THƯƠNG TỬ VONG:",
        "• Vị trí: Vùng dưới xương đòn trái, cách hõm ức 5.5cm.",
        "• Kích thước miệng vết thương: 0.8cm x 0.7cm, mép vết",
        "  rách sắc nhọn hình elip tròn, không có khấc sống dao.",
        "• Chiều sâu ống vết thương: 9.0cm theo hướng chếch",
        "  từ trước ra sau, từ trên xuống dưới vào trung thất.",
        "• Hậu quả: Rách tĩnh mạch dưới đòn trái và thùy trên",
        "  phổi trái, gây mất máu cấp tối cấp và suy hô hấp.",
        "",
        "2. HÙNG KHÍ GÂY ÁN:",
        "• Vật nhọn kim loại hình trụ tròn (không phải dao bài",
        "  hay dao găm thường), đường kính thân khoảng 0.7cm.",
        "• Đặc điểm cơ học trùng khớp hoàn toàn với DÙI SẮT",
        "  chuyên dụng niêm chì toa hàng.",
        "",
        "3. THỜI GIAN CHẾT:",
        "• Khoảng 01h30 - 02h00 sáng ngày 13/10/2008.",
        "• Trùng khớp thời điểm tàu qua khu vực đèo Cà Ná."
    ]
    cur_y = 135
    for m in med:
        if m.startswith("1.") or m.startswith("2.") or m.startswith("3."):
            draw.text((450, cur_y), m, fill=(140, 20, 20), font=f_bold)
        else:
            draw.text((450, cur_y), m, fill=(45, 55, 65), font=get_font(FONT_HELVETICA, 10))
        cur_y += 18
        
    # Bottom stamp
    draw.rectangle([40, 485, w - 40, h - 35], fill=(235, 240, 245), outline=(170, 180, 190))
    draw.text((55, 505), "GIÁM ĐỊNH VIÊN PHÁP Y: BS.CKII NGUYỄN VĂN THÀNH (ĐÃ KÝ & ĐÓNG DẤU ĐỎ)", fill=(60, 70, 80), font=f_bold)
    
    save_webp(img, "d04-giam-dinh-phap-y.webp")

# 5. d05-cua-truot.webp (800x600) - Sliding Door Latch & Friction Mark
def render_d05():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (40, 42, 48))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 15)
    f_bold = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    
    # Outer frame
    draw.rectangle([20, 20, w - 20, h - 20], outline=(100, 110, 120), width=2)
    draw.text((35, 30), "VẬT CHỨNG HÌNH SỰ - ẢNH CHỤP MACRO ĐỈNH CỬA TRƯỢT KHOANG 4", fill=(240, 210, 120), font=f_title)
    
    # Sliding door top aluminum frame & rubber seal
    draw.rectangle([40, 70, w - 40, 210], fill=(85, 90, 98), outline=(140, 150, 160), width=2) # aluminum rail
    draw.rectangle([40, 210, w - 40, 260], fill=(20, 22, 25)) # black rubber gasket
    
    # Door top plate (wood laminate)
    draw.rectangle([40, 260, w - 40, h - 40], fill=(130, 95, 65))
    
    # Chrome sliding door latch (lẫy gạt gập xuống 90 độ)
    # Latch base
    draw.rectangle([340, 240, 460, 360], fill=(170, 175, 185), outline=(230, 235, 245), width=2)
    # Latch lever pointing downwards (locked position)
    draw.polygon([(385, 290), (415, 290), (420, 480), (380, 480)], fill=(210, 215, 225), outline=(245, 250, 255), width=2)
    draw.ellipse([380, 460, 420, 500], fill=(190, 195, 205), outline=(255, 255, 255), width=2) # knob
    
    # Friction groove mark on aluminum rail & rubber seal (Vệt cước ma sát)
    draw.line([(390, 120), (410, 270)], fill=(255, 255, 255), width=3) # shiny polished nylon groove
    draw.line([(392, 120), (412, 270)], fill=(50, 50, 50), width=1) # dark grease line
    
    # Magnifying inspection circle
    draw.ellipse([210, 90, 370, 250], outline=(255, 60, 60), width=3)
    draw.line([(350, 120), (450, 100)], fill=(255, 60, 60), width=2)
    draw.text((460, 92), "VẾT MIẾT MA SÁT DÂY CƯỚC (RÃNH SÂU 0.2mm)\nDÍNH MỠ BÔI TRƠN RAY TRƯỢT MÀU XÁM ĐEN", fill=(255, 120, 120), font=f_bold)
    
    # Scale Bar (cm)
    draw.rectangle([60, h - 80, 260, h - 55], fill=(255, 255, 255), outline=(0, 0, 0))
    for i in range(10):
        if i % 2 == 0:
            draw.rectangle([60 + i * 20, h - 80, 80 + i * 20, h - 55], fill=(0, 0, 0))
    draw.text((160, h - 95), "THƯỚC TỶ LỆ HÌNH SỰ (10 CM)", fill=(255, 255, 255), font=get_font(FONT_HELVETICA, 10), anchor="mm")
    
    # Yellow Evidence Marker 1
    draw.polygon([(620, 360), (700, 360), (660, 280)], fill=(240, 210, 20), outline=(0, 0, 0), width=2)
    draw.text((660, 335), "1", fill=(0, 0, 0), font=get_font(FONT_HELVETICA, 28), anchor="mm")
    draw.text((660, 390), "VẬT CHỨNG SỐ 1:\nCHỐT KHOÁ GẬP TRONG", fill=(255, 255, 255), font=f_bold, anchor="mm")
    
    save_webp(img, "d05-cua-truot.webp")

# 6. d09-ve-tau-se3.webp (800x480) - Authentic SE3 Train Ticket Scan
def render_d09():
    w, h = 800, 480
    img = Image.new('RGB', (w, h), (242, 238, 224))
    draw = ImageDraw.Draw(img)
    
    f_mast = get_font(FONT_HELVETICA, 18)
    f_bold = get_font(FONT_HELVETICA, 13)
    f_text = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 13)
    
    # Ticket outline
    draw.rectangle([25, 25, w - 25, h - 25], outline=(120, 110, 95), width=2)
    
    # Ticket 1: Đặng Quốc Vinh (Khoang 4 Giường 1)
    draw.rectangle([40, 40, w - 40, 220], fill=(250, 248, 240), outline=(160, 150, 130), width=1)
    draw.rectangle([40, 40, w - 40, 75], fill=(225, 60, 60))
    draw.text((55, 48), "TỔNG CÔNG TY ĐƯỜNG SẮT VIỆT NAM • THẺ LÊN TÀU HỎA SE3", fill=(255, 255, 255), font=f_mast)
    draw.text((w - 180, 50), "MẪU: VT-08/2008", fill=(255, 240, 240), font=get_font(FONT_HELVETICA, 10))
    
    draw.text((55, 88), "Hành khách: ĐẶNG QUỐC VINH", fill=(20, 20, 20), font=f_bold)
    draw.text((360, 88), "CMND: 023841920", fill=(50, 50, 50), font=f_text)
    draw.text((55, 115), "Tàu / Ngày: SE3 • 12/10/2008 (22h00)", fill=(140, 20, 20), font=f_bold)
    draw.text((360, 115), "Hành trình: GA HÀ NỘI → GA MƯỜNG MÁN", fill=(20, 20, 20), font=f_bold)
    draw.text((55, 142), "Toa xe: TOA SỐ 06 (Giường nằm ĐH)", fill=(20, 20, 20), font=f_bold)
    draw.text((360, 142), "Vị trí: KHOANG 04 - GIƯỜNG 01 (TẦNG 1)", fill=(180, 20, 20), font=f_bold)
    draw.text((55, 170), "Giá vé: 680.000 VNĐ (Đã bao gồm BH)", fill=(60, 60, 60), font=f_text)
    draw.text((360, 170), "Kiểm soát: SOÁT VÉ GA HÀ NỘI [ĐÃ CHECK-IN]", fill=(20, 100, 30), font=f_bold)
    
    # Stamp
    draw.rectangle([w - 170, 95, w - 60, 195], outline=(180, 30, 30), width=2)
    draw.text((w - 115, 125), "ĐÃ SOÁT", fill=(180, 30, 30), font=f_bold, anchor="mm")
    draw.text((w - 115, 155), "12/10/2008", fill=(180, 30, 30), font=f_text, anchor="mm")
    
    # Ticket 2: Bùi Bích Thảo (Khoang 4 Giường 2)
    draw.rectangle([40, 245, w - 40, 425], fill=(250, 248, 240), outline=(160, 150, 130), width=1)
    draw.rectangle([40, 245, w - 40, 280], fill=(45, 95, 160))
    draw.text((55, 253), "TỔNG CÔNG TY ĐƯỜNG SẮT VIỆT NAM • THẺ LÊN TÀU HỎA SE3", fill=(255, 255, 255), font=f_mast)
    draw.text((w - 180, 255), "MẪU: VT-08/2008", fill=(240, 245, 255), font=get_font(FONT_HELVETICA, 10))
    
    draw.text((55, 293), "Hành khách: BÙI BÍCH THẢO", fill=(20, 20, 20), font=f_bold)
    draw.text((360, 293), "CMND: 012984102", fill=(50, 50, 50), font=f_text)
    draw.text((55, 320), "Tàu / Ngày: SE3 • 12/10/2008 (22h00)", fill=(30, 70, 140), font=f_bold)
    draw.text((360, 320), "Hành trình: GA HÀ NỘI → GA MƯỜNG MÁN", fill=(20, 20, 20), font=f_bold)
    draw.text((55, 347), "Toa xe: TOA SỐ 06 (Giường nằm ĐH)", fill=(20, 20, 20), font=f_bold)
    draw.text((360, 347), "Vị trí: KHOANG 04 - GIƯỜNG 02 (TẦNG 1)", fill=(30, 70, 140), font=f_bold)
    draw.text((55, 375), "Giá vé: 680.000 VNĐ (Đã bao gồm BH)", fill=(60, 60, 60), font=f_text)
    draw.text((360, 375), "Ghi chú: CÓ MẶT TẠI CĂNG-TIN TOA 4 TỪ 00H20", fill=(140, 30, 30), font=f_bold)
    
    # Stamp
    draw.rectangle([w - 170, 300, w - 60, 400], outline=(30, 60, 140), width=2)
    draw.text((w - 115, 330), "ĐÃ SOÁT", fill=(30, 60, 140), font=f_bold, anchor="mm")
    draw.text((w - 115, 360), "12/10/2008", fill=(30, 60, 140), font=f_text, anchor="mm")
    
    # Bottom note
    draw.text((w//2, h - 35), "TÀI LIỆU d09: ĐỐI CHIẾU DANH SÁCH PHÂN BỔ KHOANG 4 VÀ BẰNG CHỨNG NGOẠI PHẠM", fill=(100, 90, 80), font=f_text, anchor="mm")
    
    save_webp(img, "d09-ve-tau-se3.webp")

# 7. d10-giam-dinh-co-hoc.webp (800x600) - Forensic Mechanical Exam of Nylon Fiber
def render_d10():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (242, 244, 246))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_bold = get_font(FONT_HELVETICA, 12)
    f_sub = get_font(FONT_HELVETICA, 10)
    
    # Border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(170, 180, 190), width=2)
    draw.rectangle([30, 30, w - 30, 75], fill=(225, 232, 240), outline=(160, 175, 185))
    draw.text((45, 38), "VIỆN KHOA HỌC HÌNH SỰ - BỘ CÔNG AN (PHÂN VIỆN TẠI TP.HCM)", fill=(30, 45, 60), font=f_bold)
    draw.text((45, 54), "BÁO CÁO GIÁM ĐỊNH KỸ THUẬT CƠ HỌC: DẤU VẾT CƯỚC NYLON KHÓA PHÒNG", fill=(140, 20, 20), font=f_title)
    
    # Left: Photomicrograph of 0.45mm nylon fiber
    draw.rectangle([40, 90, 420, 370], fill=(20, 25, 32), outline=(140, 150, 165), width=2)
    draw.text((55, 105), "ẢNH HIỂN VI ĐIỆN TỬ (SEM 150x): SỢI NYLON THU TẠI KHE CỬA", fill=(180, 220, 255), font=f_bold)
    
    # Rubber gasket cross section
    draw.rectangle([60, 140, 200, 340], fill=(40, 42, 48), outline=(100, 110, 120))
    draw.text((130, 240), "GIOĂNG\nCAO SU\nĐỈNH CỬA", fill=(180, 190, 200), font=f_bold, anchor="mm")
    
    # Magnified fiber caught in seam
    draw.line([(180, 200), (380, 280)], fill=(240, 245, 255), width=8) # translucent nylon monofilament
    draw.line([(180, 200), (380, 280)], fill=(120, 160, 200), width=3)
    # Grease smudge
    draw.ellipse([270, 230, 310, 260], fill=(30, 30, 30))
    draw.text((290, 215), "Vệt mỡ ray trượt", fill=(255, 200, 100), font=f_sub, anchor="mm")
    
    # Red caliper measurement
    draw.line([(240, 210), (240, 240)], fill=(255, 60, 60), width=2)
    draw.text((240, 195), "Ø 0.45 mm", fill=(255, 80, 80), font=f_bold, anchor="mm")
    
    # Right: Spectrogram / Polymer match
    draw.rectangle([435, 90, w - 40, 370], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((450, 105), "KẾT QUẢ ĐỐI SÁNH QUANG PHỔ HỒNG NGOẠI (FTIR)", fill=(30, 45, 60), font=f_bold)
    draw.line([(450, 125), (w - 55, 125)], fill=(200, 210, 220), width=1)
    
    # Spectrogram curve
    draw.rectangle([450, 135, w - 55, 240], fill=(245, 248, 252), outline=(200, 210, 220))
    # Two matching curves
    draw.line([(460, 220), (520, 220), (550, 160), (580, 220), (620, 150), (660, 220), (730, 220)], fill=(220, 30, 30), width=2)
    draw.line([(460, 225), (520, 225), (550, 165), (580, 225), (620, 155), (660, 225), (730, 225)], fill=(30, 80, 200), width=2)
    draw.text((470, 145), "— Mẫu xơ khe cửa khoang 4", fill=(220, 30, 30), font=f_sub)
    draw.text((470, 160), "— Mẫu cước Pioneer trong ba lô Long", fill=(30, 80, 200), font=f_sub)
    draw.text((600, 230), "ĐỘ TRÙNG KHỚP: 99.8% (POLYAMIDE-6)", fill=(140, 20, 20), font=f_bold)
    
    txts = [
        "• Bản chất vật liệu: Polyamide-6 (cước nylon chịu tải)",
        "• Đường kính đo đạc: 0.45mm (chịu lực kéo đứt 20kg)",
        "• Vệt bám bề mặt: Dầu mỡ khoáng bôi trơn đường ray",
        "• Cơ chế tạo dấu vết: Lực miết ma sát cao khi giật",
        "  sợi cước qua khe hẹp đỉnh cửa với góc kéo ~60°."
    ]
    cur_y = 255
    for t in txts:
        draw.text((450, cur_y), t, fill=(40, 50, 60), font=f_sub)
        cur_y += 18
        
    # Bottom: Investigation conclusion
    draw.rectangle([40, 385, w - 40, h - 35], fill=(235, 240, 248), outline=(170, 180, 195))
    draw.text((55, 400), "KẾT LUẬN CƠ CHẾ KỸ THUẬT PHÒNG KÍN:", fill=(140, 20, 20), font=f_bold)
    draw.text((55, 420), "1. Cửa trượt khoang 4 bị khoá chốt từ bên ngoài hành lang bằng sợi cước luồn qua khe đỉnh cửa.", fill=(30, 40, 50), font=f_bold)
    draw.text((55, 440), "2. Sợi cước câu cá thu giữ trong ba lô Nguyễn Hoàng Long tại khoang 2 chính là vật liệu đã thực hiện thủ pháp.", fill=(30, 40, 50), font=f_bold)
    draw.text((55, 460), "3. Thao tác khóa chốt từ ngoài và giật rút toàn bộ sợi cước chỉ mất khoảng 3 - 5 giây trong bóng tối.", fill=(30, 40, 50), font=f_bold)
    
    save_webp(img, "d10-giam-dinh-co-hoc.webp")

# 8. d12-cuon-cuoc.webp (800x600) - Pioneer Line & Steel Awl Weapon
def render_d12():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (210, 215, 220))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_bold = get_font(FONT_HELVETICA, 13)
    f_sub = get_font(FONT_HELVETICA, 11)
    
    # Stainless Steel Forensic Tray
    draw.rectangle([30, 30, w - 30, h - 30], fill=(225, 230, 235), outline=(160, 170, 180), width=4)
    draw.rectangle([45, 45, w - 45, h - 45], fill=(235, 240, 245), outline=(190, 200, 210), width=2)
    
    draw.text((60, 60), "CÔNG AN TỈNH BÌNH THUẬN • BÀN KHÁM XÉT VẬT CHỨNG", fill=(30, 45, 60), font=f_bold)
    draw.text((60, 80), "TANG VẬT THU GIỮ TRONG BA LÔ NGUYỄN HOÀNG LONG (KHOANG SỐ 2)", fill=(140, 20, 20), font=f_title)
    
    # 1. Spool of Pioneer Fishing Line
    draw.ellipse([100, 150, 340, 390], fill=(180, 190, 200), outline=(80, 90, 100), width=3)
    draw.ellipse([140, 190, 300, 350], fill=(215, 225, 235), outline=(120, 130, 140), width=2)
    # Pioneer label in center
    draw.ellipse([175, 225, 265, 315], fill=(20, 50, 90), outline=(240, 240, 240), width=2)
    draw.text((220, 255), "PIONEER", fill=(255, 255, 255), font=f_bold, anchor="mm")
    draw.text((220, 275), "BIG GAME 0.45mm", fill=(255, 200, 50), font=get_font(FONT_HELVETICA, 9), anchor="mm")
    draw.text((220, 290), "LOAD: 20 KG", fill=(200, 220, 255), font=get_font(FONT_HELVETICA, 8), anchor="mm")
    
    # Cut end of line with black grease
    draw.line([(310, 230), (370, 190), (410, 210)], fill=(255, 255, 255), width=3)
    draw.ellipse([405, 205, 415, 215], fill=(30, 30, 30))
    draw.text((430, 205), "Đầu mối cắt mới 3m\ndính mỡ ray trượt", fill=(140, 20, 20), font=f_sub)
    
    # 2. Steel Awl Tool (Hung khí dùi sắt)
    # Wood handle (lim bọc đồng)
    draw.polygon([(460, 360), (510, 335), (590, 480), (540, 505)], fill=(65, 40, 25), outline=(110, 80, 50), width=2)
    # Brass ferrule
    draw.polygon([(505, 338), (530, 325), (545, 350), (520, 363)], fill=(200, 170, 70))
    # Sharp cylindrical steel shaft (dài 22cm, Ø 0.7cm)
    draw.polygon([(525, 328), (540, 320), (690, 170), (675, 160)], fill=(185, 195, 205), outline=(120, 130, 140), width=2)
    draw.polygon([(675, 160), (690, 170), (715, 140)], fill=(220, 230, 240)) # sharp needle point
    
    # Dried blood stain on tip
    draw.polygon([(665, 170), (690, 170), (715, 140), (680, 150)], fill=(120, 20, 20))
    draw.ellipse([670, 165, 695, 185], fill=(90, 15, 15))
    draw.text((640, 120), "ĐẦU DÙI DÍNH MÁU KHÔ\n(TRÙNG ADN NẠN NHÂN)", fill=(180, 20, 20), font=f_bold)
    
    # Evidence marker B
    draw.polygon([(80, 450), (140, 450), (110, 390)], fill=(240, 210, 20), outline=(0, 0, 0), width=2)
    draw.text((110, 432), "B", fill=(0, 0, 0), font=get_font(FONT_HELVETICA, 24), anchor="mm")
    
    # Scale Bar (cm)
    draw.rectangle([250, 510, 490, 535], fill=(255, 255, 255), outline=(0, 0, 0))
    for i in range(12):
        if i % 2 == 0:
            draw.rectangle([250 + i * 20, 510, 270 + i * 20, 535], fill=(0, 0, 0))
    draw.text((370, 495), "THƯỚC TỶ LỆ HÌNH SỰ (12 CM)", fill=(50, 50, 50), font=get_font(FONT_HELVETICA, 10), anchor="mm")
    
    save_webp(img, "d12-cuon-cuoc.webp")

# 9. d14-giam-dinh-vet-mau.webp (800x600) - Blood Splatter & DNA Gel Electrophoresis
def render_d14():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (242, 244, 246))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_bold = get_font(FONT_HELVETICA, 12)
    f_sub = get_font(FONT_HELVETICA, 10)
    
    # Header
    draw.rectangle([20, 20, w - 20, h - 20], outline=(170, 180, 190), width=2)
    draw.rectangle([30, 30, w - 30, 75], fill=(225, 232, 240), outline=(160, 175, 185))
    draw.text((45, 38), "VIỆN KHOA HỌC HÌNH SỰ • PHÒNG GIÁM ĐỊNH SINH HỌC PHÁP Y", fill=(30, 45, 60), font=f_bold)
    draw.text((45, 54), "KẾT QUẢ XÉT NGHIỆM GEN ADN VẾT MÁU TRÊN GIÀY VÀ HUNG KHÍ", fill=(140, 20, 20), font=f_title)
    
    # Left: Leather shoe edge macro with high-velocity blood spatter
    draw.rectangle([40, 90, 420, 460], fill=(25, 28, 35), outline=(140, 150, 165), width=2)
    draw.text((55, 105), "ẢNH MACRO MÉP ĐẾ GIÀY DA CỦA NGUYỄN HOÀNG LONG", fill=(255, 220, 120), font=f_bold)
    
    # Leather shoe sole cross section
    draw.rectangle([60, 150, 400, 260], fill=(55, 50, 45), outline=(90, 85, 80))
    draw.rectangle([60, 260, 400, 330], fill=(20, 20, 20)) # black rubber sole
    draw.text((230, 200), "DA GIÀY Ý (BÊN TRÁI)", fill=(180, 170, 160), font=f_bold, anchor="mm")
    
    # Blood spatter dots (li ti tia bắn)
    random.seed(2008)
    for _ in range(35):
        bx = random.randint(180, 380)
        by = random.randint(245, 285)
        br = random.randint(1, 4)
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(180, 20, 20))
        # tail
        draw.line([(bx, by), (bx + random.randint(3, 8), by - random.randint(1, 4))], fill=(140, 15, 15), width=1)
        
    draw.text((230, 360), "Tia máu bắn li ti dạng sương (High-Velocity Spatter)\nBắn ngược vào mép giày khi đâm trực diện ở cự ly < 40cm", fill=(255, 150, 150), font=f_sub, anchor="mm")
    
    # Right: DNA Electrophoresis Gel Lanes
    draw.rectangle([435, 90, w - 40, 460], fill=(20, 30, 45), outline=(140, 150, 165), width=2)
    draw.text((450, 105), "BẢN ĐỒ ĐIỆN DI GEN ADN (STR 16 LOCUS)", fill=(140, 210, 255), font=f_bold)
    
    # Gel lanes
    lanes = [
        ("MẪU NẠN NHÂN (VINH)", 510),
        ("MÁU TRÊN DÙI SẮT", 600),
        ("MÁU TRÊN ĐẾ GIÀY", 690)
    ]
    for name, lx in lanes:
        draw.text((lx, 140), name, fill=(200, 220, 240), font=get_font(FONT_HELVETICA, 8), anchor="mm")
        draw.rectangle([lx - 30, 160, lx + 30, 410], fill=(10, 15, 25), outline=(60, 80, 110))
        
        # DNA bands at matching heights
        band_y = [185, 215, 240, 280, 310, 345, 375, 395]
        for by in band_y:
            draw.rectangle([lx - 25, by, lx + 25, by + 4], fill=(100, 255, 200))
            
    # Connecting dashed lines across all 3 lanes showing 100% match
    for by in [185, 215, 240, 280, 310, 345, 375, 395]:
        draw.line([(470, by + 2), (730, by + 2)], fill=(255, 80, 80), width=1)
        
    draw.text((w - 170, 435), "XÁC SUẤT TRÙNG KHỚP ADN:\n99.99999% VỚI ĐẶNG QUỐC VINH", fill=(255, 100, 100), font=f_bold, anchor="mm")
    
    # Bottom Note
    draw.rectangle([40, 480, w - 40, h - 35], fill=(235, 240, 248), outline=(170, 180, 195))
    draw.text((55, 500), "KẾT LUẬN GIÁM ĐỊNH ADN: BÁC BỎ HOÀN TOÀN LỜI KHAI 'NGỦ SAY SUỐT ĐÊM' CỦA LONG.", fill=(150, 20, 20), font=f_bold)
    draw.text((55, 520), "NGUYỄN HOÀNG LONG LÀ NGƯỜI TRỰC TIẾP CẦM DÙI SẮT TẤN CÔNG NẠN NHÂN TRONG KHOANG 4.", fill=(30, 40, 50), font=f_bold)
    
    save_webp(img, "d14-giam-dinh-vet-mau.webp")

# 10. d15-tien-va-cap-da.webp (800x600) - Retrieved Briefcase & 200M VND Cash in AC Vent
def render_d15():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (242, 244, 246))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_bold = get_font(FONT_HELVETICA, 13)
    f_sub = get_font(FONT_HELVETICA, 10)
    
    # Header
    draw.rectangle([20, 20, w - 20, h - 20], outline=(170, 180, 190), width=2)
    draw.rectangle([30, 30, w - 30, 75], fill=(225, 232, 240), outline=(160, 175, 185))
    draw.text((45, 38), "CÔNG AN TỈNH BÌNH THUẬN • BIÊN BẢN KHÁM XÉT VÀ THU GIỮ TÀI SẢN", fill=(30, 45, 60), font=f_bold)
    draw.text((45, 54), "BẢN ẢNH TANG VẬT THU TRONG HỘC ĐIỀU HÒA TRẦN KHOANG SỐ 2", fill=(140, 20, 20), font=f_title)
    
    # Main Photo Area: Table display of retrieved items
    draw.rectangle([40, 90, w - 40, 470], fill=(235, 238, 242), outline=(150, 160, 175), width=2)
    
    # 1. AC vent filter grill detached (tấm lưới lọc trần)
    draw.rectangle([60, 110, 260, 280], fill=(190, 195, 205), outline=(100, 110, 120), width=3)
    for gy in range(125, 275, 15):
        draw.line([(65, gy), (255, gy)], fill=(80, 90, 100), width=2)
    draw.text((160, 295), "Lưới lọc cửa gió điều hòa trần\nkhoang 2 bị cạy mở ốc vít", fill=(120, 40, 40), font=f_sub, anchor="mm")
    
    # 2. Brown leather briefcase of victim
    draw.rectangle([300, 110, 560, 320], fill=(110, 65, 35), outline=(70, 40, 20), width=3) # leather body
    draw.rectangle([320, 110, 540, 150], fill=(85, 50, 25)) # flap
    draw.rectangle([410, 135, 450, 165], fill=(220, 180, 50)) # brass lock
    draw.text((430, 230), "CẶP DA MÀU NÂU\nCỦA ÔNG ĐẶNG QUỐC VINH\n(DÍNH BỤI THAN TRẦN TÀU)", fill=(245, 220, 200), font=f_bold, anchor="mm")
    
    # 3. 4 Stacks of 500k Polymer Bills (Total 200,000,000 VND)
    for idx, (bx, by) in enumerate([(600, 110), (600, 175), (600, 240), (600, 305)]):
        draw.rectangle([bx, by, bx + 140, by + 50], fill=(70, 150, 190), outline=(20, 80, 120), width=2) # 500k cyan polymer
        draw.text((bx + 70, by + 20), "500.000 Đ", fill=(255, 255, 255), font=f_bold, anchor="mm")
        draw.text((bx + 70, by + 36), "CỌC 50 TRIỆU", fill=(220, 245, 255), font=f_sub, anchor="mm")
        # Paper money band
        draw.rectangle([bx + 55, by, bx + 85, by + 50], fill=(240, 240, 230), outline=(150, 150, 140))
        
    # 4. Dossier Folder of Titan Bidding
    draw.rectangle([100, 335, 420, 450], fill=(240, 225, 185), outline=(160, 140, 100), width=2)
    draw.text((120, 350), "CÔNG TY KHOÁNG SẢN RẠNG ĐÔNG", fill=(30, 40, 50), font=f_bold)
    draw.text((120, 375), "HỒ SƠ DỰ THẦU KHAI THÁC MỎ CÁT TITAN BÌNH THUẬN", fill=(140, 20, 20), font=f_bold)
    draw.text((120, 400), "Dự án: Mỏ sa khoáng ven biển Hàm Thuận Nam - Phan Thiết", fill=(50, 60, 70), font=f_sub)
    draw.text((120, 420), "Toàn bộ tài liệu gốc mật mang theo người của Đặng Quốc Vinh", fill=(70, 80, 90), font=f_sub)
    
    # Bottom Note
    draw.rectangle([40, 485, w - 40, h - 35], fill=(235, 240, 248), outline=(170, 180, 195))
    draw.text((55, 505), "KẾT LUẬN TANG VẬT: TOÀN BỘ 200 TRIỆU ĐỒNG VÀ TẬP HỒ SƠ BỊ CƯỚP ĐƯỢC THU HỒI NGUYÊN VẸN.", fill=(140, 20, 20), font=f_bold)
    draw.text((55, 525), "ĐỐI TƯỢNG NGUYỄN HOÀNG LONG ĐÃ CÚI ĐẦU NHẬN TỘI TRƯỚC VẬT CHỨNG KHÔNG THỂ CHỐI CÃI.", fill=(30, 40, 50), font=f_bold)
    
    save_webp(img, "d15-tien-va-cap-da.webp")

# 11. d16-thuc-nghiem-hien-truong.webp (800x600) - 4-Step Reenactment Diagram
def render_d16():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (18, 40, 68))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_bold = get_font(FONT_HELVETICA, 12)
    f_step = get_font(FONT_HELVETICA, 13)
    f_sub = get_font(FONT_HELVETICA, 10)
    
    # Header
    draw.rectangle([25, 20, w - 25, 75], fill=(12, 28, 50), outline=(80, 150, 220), width=2)
    draw.text((40, 32), "CƠ QUAN CẢNH SÁT ĐIỀU TRA • CÔNG AN TỈNH BÌNH THUẬN", fill=(140, 200, 255), font=f_bold)
    draw.text((40, 50), "BẢN VẼ KỸ THUẬT THỰC NGHIỆM: CƠ CHẾ KHÓA CHỐT PHÒNG KÍN BẰNG DÂY CƯỚC (4 BƯỚC)", fill=(255, 255, 255), font=f_title)
    
    # 4 Quadrants
    coords = [
        ("BƯỚC 1: LUỒN DÂY QUA KHE ĐỈNH CỬA", 40, 90, 390, 280),
        ("BƯỚC 2: QUÀNG NÚT THÒNG LỌNG VÀO CHỐT", 410, 90, 760, 280),
        ("BƯỚC 3: ĐÓNG KHÍT CỬA TRƯỢT TỪ BÊN NGOÀI", 40, 295, 390, 485),
        ("BƯỚC 4: GIẬT SẬP CHỐT & RÚT THU HỒI DÂY", 410, 295, 760, 485)
    ]
    
    for title, x1, y1, x2, y2 in coords:
        draw.rectangle([x1, y1, x2, y2], fill=(24, 50, 85), outline=(100, 160, 220), width=2)
        draw.rectangle([x1, y1, x2, y1 + 30], fill=(35, 70, 115))
        draw.text(((x1 + x2)//2, y1 + 15), title, fill=(255, 220, 100), font=f_step, anchor="mm")
        
    # Drawing Step 1:
    # Door open slightly, threading fishing line through top rubber gap
    draw.rectangle([60, 140, 200, 260], fill=(70, 50, 35), outline=(140, 150, 160)) # door frame
    draw.rectangle([210, 140, 350, 260], fill=(100, 75, 50), outline=(180, 190, 200)) # sliding door
    draw.line([(180, 130), (220, 170)], fill=(255, 255, 255), width=3) # nylon line
    draw.text((200, 245), "Luồn sợi cước 0.45mm qua khe cao su\nkhi cửa mở hé 5cm", fill=(200, 220, 245), font=f_sub, anchor="mm")
    
    # Drawing Step 2:
    # Loose slipknot looped over chrome latch inside
    draw.rectangle([450, 140, 720, 260], fill=(30, 35, 45), outline=(120, 130, 140))
    draw.rectangle([540, 150, 630, 240], fill=(160, 170, 180)) # latch plate
    draw.polygon([(575, 170), (595, 170), (620, 170), (620, 190)], fill=(220, 225, 235)) # latch horizontal (open)
    draw.ellipse([590, 160, 630, 200], outline=(255, 255, 255), width=3) # slipknot loop
    draw.line([(610, 160), (650, 130)], fill=(255, 255, 255), width=2)
    draw.text((585, 245), "Quàng nút thắt trượt ôm hờ đầu chốt gạt\nkhi chốt đang ở thế mở ngang", fill=(200, 220, 245), font=f_sub, anchor="mm")
    
    # Drawing Step 3:
    # Sliding door closed from outside, line hanging out
    draw.rectangle([60, 345, 370, 465], fill=(100, 75, 50), outline=(180, 190, 200))
    draw.line([(215, 335), (215, 410)], fill=(255, 255, 255), width=3) # line pinched in top rail
    draw.polygon([(215, 425), (210, 405), (220, 405)], fill=(255, 80, 80)) # pull arrow
    draw.text((215, 450), "Đóng khít cửa trượt từ bên ngoài hành lang.\nSợi cước kẹp trong nẹp đỉnh cửa.", fill=(200, 220, 245), font=f_sub, anchor="mm")
    
    # Drawing Step 4:
    # Pull line downwards, latch drops to locked, pull out line
    draw.rectangle([430, 345, 740, 465], fill=(30, 35, 45), outline=(120, 130, 140))
    draw.rectangle([540, 355, 630, 445], fill=(160, 170, 180))
    draw.polygon([(575, 375), (595, 375), (595, 435), (575, 435)], fill=(220, 225, 235)) # latch down (locked!)
    draw.line([(585, 355), (660, 335)], fill=(255, 255, 255), width=2) # line pulled out
    draw.polygon([(675, 330), (655, 330), (665, 340)], fill=(255, 80, 80))
    draw.text((585, 450), "Chốt gập sập xuống 90° khóa chặt phòng.\nGiật mạnh bung nút thắt, rút dây ra chỉ 3 giây!", fill=(255, 220, 120), font=f_sub, anchor="mm")
    
    # Bottom Conclusion Banner
    draw.rectangle([25, 500, w - 25, h - 20], fill=(12, 28, 50), outline=(80, 150, 220), width=1)
    draw.text((w//2, 520), "KẾT QUẢ THỰC NGHIỆM ĐIỀU TRA: THÀNH CÔNG 10/10 LẦN THỬ NGHIỆM TRÊN TÀU SE3", fill=(255, 220, 100), font=f_bold, anchor="mm")
    draw.text((w//2, 545), "Giải thích trọn vẹn hiện trường phòng kín mà không cần người ở lại bên trong phòng.", fill=(200, 220, 245), font=f_sub, anchor="mm")
    
    save_webp(img, "d16-thuc-nghiem-hien-truong.webp")

def main():
    print("=== Tối ưu và kết xuất hình ảnh Hồ sơ 05: Chuyến tàu đêm Mường Mán ===")
    optimize_cover()
    render_d01()
    render_d02()
    render_d03()
    render_d04()
    render_d05()
    render_d09()
    render_d10()
    render_d12()
    render_d14()
    render_d15()
    render_d16()
    print("=== Hoàn tất! ===")

if __name__ == "__main__":
    main()
