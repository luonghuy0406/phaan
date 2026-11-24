#!/usr/bin/env python3
import os
import random
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/Users/huynguyen/Documents/game_pha_an/public/cases/gac-den-hon-dau/images"
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

def add_grain(img, strength=10):
    w, h = img.size
    noise = Image.new('RGB', (w, h))
    npix = noise.load()
    random.seed(42)
    for y in range(h):
        for x in range(w):
            v = random.randint(128 - strength, 128 + strength)
            npix[x, y] = (v, v, v)
    return Image.blend(img, noise, 0.10)

def save_webp(img, filename):
    out_img = add_grain(img)
    p = os.path.join(OUT_DIR, filename)
    out_img.save(p, "WEBP", quality=88)
    print(f"✓ Saved: {filename} ({os.path.getsize(p)} bytes)")

# 1. d03-giai-phau.webp (800x600) - Forensic Autopsy Chart of victim Đỗ Đình Quyết
def render_d03():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (242, 244, 246))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 19)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(170, 180, 190), width=2)
    draw.rectangle([30, 30, w - 30, 80], fill=(228, 234, 240), outline=(160, 175, 185))
    
    draw.text((45, 36), "CÔNG AN THÀNH PHỐ HẢI PHÒNG - PHÒNG KỸ THUẬT HÌNH SỰ", fill=(30, 45, 60), font=f_bold)
    draw.text((45, 54), "BẢN VẼ GIÁM ĐỊNH TỔN THƯƠNG PHÁP Y TỬ THI: ĐỖ ĐÌNH QUYẾ (56 TUỔI)", fill=(140, 20, 20), font=f_title)
    
    # Left Box: Anatomical Body Outline (Back View)
    draw.rectangle([40, 95, 450, 410], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((50, 105), "SƠ ĐỒ TỔN THƯƠNG TIÊN PHÁT (MẶT SAU LƯNG)", fill=(40, 50, 60), font=f_bold)
    
    # Head & Shoulders & Torso outline
    draw.ellipse([215, 135, 275, 195], outline=(120, 130, 140), width=2) # Head
    draw.polygon([(170, 215), (215, 195), (275, 195), (320, 215), (300, 370), (190, 370)], outline=(120, 130, 140), width=2) # Torso back
    
    # Lethal Stab Wound (Right upper back, scapula region)
    draw.ellipse([255, 230, 280, 255], fill=(210, 30, 30))
    draw.line([(280, 242), (390, 242)], fill=(180, 20, 20), width=2)
    draw.text((290, 222), "◄ VẾT ĐÂM THẤU NGỰC (TIÊN PHÁT)", fill=(180, 0, 0), font=f_bold)
    draw.text((290, 245), "Độ sâu: 12cm, xuyên màng phổi", fill=(140, 20, 20), font=f_mono)
    draw.text((290, 260), "Bản dao dày có rãnh thoát khí", fill=(140, 20, 20), font=f_mono)
    draw.text((290, 275), "(Đặc trưng dao găm thợ lặn)", fill=(140, 20, 20), font=f_mono)
    
    # Skull Fracture & Secondary impact
    draw.line([(220, 150), (110, 150)], fill=(160, 50, 50), width=2)
    draw.text((60, 135), "VỠ XƯƠNG HỘP SỌ", fill=(160, 40, 40), font=f_bold)
    draw.text((60, 152), "Đa chấn thương do rơi", fill=(60, 60, 60), font=f_mono)
    draw.text((60, 167), "từ độ cao 25 mét đập đá", fill=(60, 60, 60), font=f_mono)
    
    # Right Box: Forensic Conclusion Notes
    draw.rectangle([465, 95, 760, 410], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((475, 105), "ĐẶC ĐIỂM BỆNH LÝ HÌNH SỰ", fill=(40, 50, 60), font=f_bold)
    
    points = [
        "1. Vết đâm sau lưng xảy ra khi tim còn",
        "   đập mạnh (phản ứng sống cấp tính).",
        "2. Nạn nhân bị sốc mất máu cấp và tràn",
        "   khí màng phổi trước khi rơi tự do.",
        "3. Chiếc áo len có một cúc bị giật đứt,",
        "   trùng khớp chiếc nút rơi tại lan can.",
        "4. Thời điểm tử vong ước tính:",
        "   Khoảng 23h20 đến 23h35 ngày 24/09.",
        "5. Cơ chế: Bị sát hại trước bằng hung",
        "   khí, sau đó bị xô rơi khỏi ban công."
    ]
    for i, pt in enumerate(points):
        draw.text((475, 135 + i * 22), pt, fill=(40, 40, 40), font=f_sub)
        
    # Bottom Summary Box & Seal
    draw.rectangle([40, 425, 760, 565], fill=(255, 255, 250), outline=(180, 190, 200))
    draw.text((55, 435), "KẾT LUẬN GIÁM ĐỊNH PHÁP Y:", fill=(30, 40, 50), font=f_bold)
    draw.text((55, 460), "Cái chết của Trạm trưởng Đỗ Đình Quyết là một vụ ÁN MẠNG GIẾT NGƯỜI CÓ CHỦ ĐÍCH,", fill=(180, 20, 20), font=f_bold)
    draw.text((55, 482), "không phải tai nạn trượt chân trong bão biển. Hung khí gây án là dao găm lưỡi dày quân dụng.", fill=(50, 50, 50), font=f_sub)
    draw.text((55, 505), "Thời gian tử vong xảy ra TRƯỚC thời điểm trạm nổ cầu chì tổng 17 phút (23h43).", fill=(30, 45, 90), font=f_bold)
    
    # Official Red Seal
    draw.ellipse([640, 455, 730, 545], outline=(200, 30, 30), width=3)
    draw.text((652, 480), "GIÁM ĐỊNH", fill=(200, 30, 30), font=f_mono)
    draw.text((655, 500), "PHÁP Y", fill=(200, 30, 30), font=f_mono)
    
    save_webp(img, "d03-giai-phau.webp")

# 2. d04-so-do-thap-den.webp (800x600) - French Colonial Lighthouse Elevation Cross-Section Blueprint
def render_d04():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (16, 38, 62)) # Blueprint navy cyan
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Grid lines
    for x in range(30, w - 30, 25):
        draw.line([(x, 30), (x, h - 30)], fill=(25, 52, 85), width=1)
    for y in range(30, h - 30, 25):
        draw.line([(30, y), (w - 30, y)], fill=(25, 52, 85), width=1)
        
    draw.rectangle([30, 30, w - 30, h - 30], outline=(80, 150, 210), width=2)
    
    # Title
    draw.text((50, 45), "SƠ ĐỒ MẶT CẮT KỸ THUẬT THÁP HẢI ĐĂNG CỔ HÒN DÁU (XÂY DỰNG NĂM 1892)", fill=(255, 255, 255), font=f_title)
    draw.text((50, 70), "Công an TP Hải Phòng trích xuất hồ sơ kiến trúc phục vụ điều tra trọng án - Tỷ lệ 1:200", fill=(140, 190, 230), font=f_sub)
    
    # Elevation Tower (Centered)
    # Lantern Room (Top)
    draw.polygon([(340, 110), (460, 110), (480, 160), (320, 160)], fill=(30, 70, 110), outline=(255, 220, 80), width=2)
    draw.text((400, 130), "ĐÀI QUANG HẢI ĐĂNG", fill=(255, 230, 90), font=f_bold, anchor="mm")
    draw.text((400, 148), "Thấu kính Fresnel - Nơi Tùng trực ca 20h-04h", fill=(200, 230, 255), font=f_mono, anchor="mm")
    
    # 3rd Floor (Radio Room)
    draw.rectangle([330, 165, 470, 225], fill=(22, 50, 82), outline=(100, 170, 230), width=2)
    draw.text((400, 185), "TẦNG 3: ĐÀI VÔ TUYẾN", fill=(220, 240, 255), font=f_bold, anchor="mm")
    draw.text((400, 205), "Máy bộ đàm ICOM ắc-quy (Nghĩa trực)", fill=(160, 200, 240), font=f_mono, anchor="mm")
    
    # 2nd Floor (Station Master Room & Fatal Balcony)
    draw.rectangle([310, 230, 490, 320], fill=(25, 60, 95), outline=(255, 100, 100), width=3)
    draw.text((400, 255), "TẦNG 2: PHÒNG LÀM VIỆC TRẠM TRƯỞNG", fill=(255, 220, 100), font=f_bold, anchor="mm")
    draw.text((400, 275), "Đỗ Đình Quyết (Nơi xảy ra xô xát lúc 23h25)", fill=(255, 180, 180), font=f_mono, anchor="mm")
    
    # Balcony extending to the right cliff
    draw.rectangle([490, 280, 580, 320], fill=(40, 80, 120), outline=(255, 80, 80), width=2)
    draw.text((535, 295), "LAN CAN ĐÁ", fill=(255, 120, 120), font=f_bold, anchor="mm")
    draw.text((535, 310), "[Rơi cúc áo]", fill=(255, 220, 80), font=f_mono, anchor="mm")
    
    # Cliff drop arrow
    draw.line([(550, 325), (550, 480)], fill=(255, 50, 50), width=3)
    draw.text((560, 400), "◄ VÁCH ĐÁ BIỂN DỰNG ĐỨNG SÂU 25 MÉT", fill=(255, 80, 80), font=f_bold)
    draw.text((560, 420), "Thi thể nạn nhân nằm tại bãi đá ngầm", fill=(255, 200, 200), font=f_mono)
    
    # 1st Floor (Living Area & Kitchen)
    draw.rectangle([280, 325, 520, 395], fill=(22, 50, 82), outline=(100, 170, 230), width=2)
    draw.text((400, 345), "TẦNG 1: PHÒNG SINH HOẠT CHUNG & BẾP", fill=(200, 230, 255), font=f_bold, anchor="mm")
    draw.text((400, 365), "Vị trí tủ sấy quần áo bị tháo rơ-le nhiệt", fill=(160, 200, 240), font=f_mono, anchor="mm")
    
    # Basement (Machine Room & Generators)
    draw.rectangle([250, 400, 550, 485], fill=(20, 45, 75), outline=(255, 220, 80), width=3)
    draw.text((400, 420), "TẦNG HẦM: PHÒNG MÁY PHÁT ĐIỆN DIESEL", fill=(255, 230, 90), font=f_bold, anchor="mm")
    draw.text((400, 440), "• Máy phát chính Yanmar 50kVA (Gài bẫy nhiệt)", fill=(255, 150, 150), font=f_mono, anchor="mm")
    draw.text((400, 458), "• Máy phát phụ 15kVA & Kho 3 tấn dầu diesel", fill=(200, 220, 240), font=f_mono, anchor="mm")
    draw.text((400, 475), "Vũ Văn Thắng vờ túc trực để tạo chứng cứ ngoại phạm", fill=(255, 220, 100), font=f_mono, anchor="mm")
    
    # Rocky Island Base
    draw.polygon([(80, 485), (720, 485), (740, 550), (60, 550)], fill=(35, 45, 55), outline=(100, 130, 160))
    draw.text((150, 515), "RẶNG ĐÁ GRANITE CỔ ĐẢO HÒN DÁU", fill=(140, 170, 200), font=f_sub)
    
    save_webp(img, "d04-so-do-thap-den.webp")

# 3. d05-nhat-ky-hai-dang.webp (800x600) - Technical Logbook of Hon Dau Lighthouse
def render_d05():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (244, 241, 232)) # Weathered logbook paper
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 14)
    f_hand = get_font(FONT_ARIAL, 14)
    
    # Outer book border
    draw.rectangle([25, 25, w - 25, h - 25], outline=(160, 150, 130), width=2)
    
    # Header bar
    draw.rectangle([35, 35, w - 35, 90], fill=(232, 227, 215), outline=(180, 170, 150))
    draw.text((50, 45), "TY HẢI ĐĂNG VÙNG 1 - TRẠM ĐÈN BIỂN TIỀN TIÊU HÒN DÁU", fill=(60, 50, 40), font=f_bold)
    draw.text((50, 68), "SỔ NHẬT KÝ CA TRỰC KỸ THUẬT VẬN HÀNH (MẪU SỐ 04/HĐ-1998)", fill=(120, 30, 30), font=f_title)
    
    # Info line
    draw.text((50, 105), "Ngày trực: 24/09/1998 | Tình trạng: BÃO SỐ 5 ĐỔ BỘ (GIÓ GIẬT CẤP 11) | Trưởng ca: Đỗ Đình Quyết", fill=(40, 40, 40), font=f_sub)
    draw.line([(40, 125), (w - 40, 125)], fill=(140, 130, 110), width=2)
    
    # Table Header
    draw.rectangle([40, 135, w - 40, 170], fill=(220, 215, 200))
    draw.text((50, 145), "GIỜ", fill=(30, 30, 30), font=f_bold)
    draw.text((120, 145), "THIẾT BỊ HOẠT ĐỘNG", fill=(30, 30, 30), font=f_bold)
    draw.text((310, 145), "DIỄN BIẾN KỸ THUẬT & GHI CHÚ VẬN HÀNH", fill=(30, 30, 30), font=f_bold)
    draw.text((680, 145), "KÝ TÊN", fill=(30, 30, 30), font=f_bold)
    
    # Rows
    rows = [
        ("18:00", "Máy chính Yanmar 50kVA", "Khởi động máy chính cấp điện thấu kính Fresnel dẫn luồng bão.", "Thắng"),
        ("20:00", "Tháp đèn chính 2000W", "Tùng nhận ca trực đài quang. Gió cấp 9, mưa mù mịt.", "Tùng"),
        ("22:00", "Máy chính + Bơm chống ngập", "Bật thêm 2 máy hút nước tầng hầm, máy phát chạy 95% công suất.", "Thắng"),
        ("23:00", "Điện đài ICOM tầng 3", "Nghĩa phát điện báo đất liền: đèn luồng hoạt động tốt.", "Nghĩa"),
        ("23:43", "TỦ ĐIỆN CẦU CHÌ TỔNG", "CẦU CHÌ TỔNG PHÁT NỔ CHẬP CHÁY DỮ DỘI! ĐÈN BIỂN VỤT TẮT!", "Tùng"),
        ("23:45", "Máy chính Yanmar", "Tùng xuống hầm gặp Thắng kiểm tra tủ điện bốc khói đen.", "Tùng"),
        ("00:00", "Máy phụ Yanmar 15kVA", "ĐÓNG ĐIỆN MÁY PHỤ THÀNH CÔNG. ĐÈN SÁNG LẠI SAU ĐÚNG 17 PHÚT!", "Thắng"),
        ("00:05", "Điện đài ICOM tầng 3", "Báo đất liền sự cố nổ cầu chì đã được máy phụ khắc phục.", "Nghĩa")
    ]
    
    y = 180
    blue_ink = (20, 35, 95)
    red_alert = (180, 20, 20)
    for t, eq, note, sign in rows:
        draw.line([(40, y + 25), (w - 40, y + 25)], fill=(210, 205, 190), width=1)
        draw.text((50, y), t, fill=(30, 30, 30), font=f_mono)
        draw.text((120, y), eq, fill=(50, 50, 50), font=f_sub)
        color = red_alert if "23:43" in t or "17 PHÚT" in note else blue_ink
        draw.text((310, y), note, fill=color, font=f_hand)
        draw.text((690, y), sign, fill=blue_ink, font=f_hand)
        y += 36
        
    # Highlight Box around 17-minute blackout
    draw.rectangle([45, 318, w - 45, 428], outline=(200, 30, 30), width=2)
    draw.text((55, 435), "◄ ĐỐI CHỨNG HÌNH SỰ: Ngọn đèn biển bị tắt chính xác 17 phút (từ 23h43 đến 00h00).", fill=(180, 20, 20), font=f_bold)
    draw.text((55, 455), "Đây là khoảng thời gian Thắng dàn cảnh sửa máy để Tùng làm nhân chứng ngoại phạm giả.", fill=(50, 50, 50), font=f_sub)
    
    # Official evidence stamp
    draw.rectangle([540, 480, w - 50, 555], fill=(255, 245, 200), outline=(180, 140, 80))
    draw.text((550, 492), "TANG VẬT VỤ ÁN HÌNH SỰ", fill=(160, 30, 20), font=f_bold)
    draw.text((550, 512), "Thu giữ tại phòng trực trạm Hòn Dáu", fill=(50, 50, 50), font=f_mono)
    draw.text((550, 530), "Ngày 25/09/1998 - Niêm phong số 02", fill=(50, 50, 50), font=f_mono)
    
    save_webp(img, "d05-nhat-ky-hai-dang.webp")

# 4. d10-cau-chi-got-mong.webp (800x600) - Forensic Inspection of Thinned Fuse Wire
def render_d10():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (238, 240, 242))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Header
    draw.rectangle([25, 25, w - 25, 80], fill=(30, 45, 60))
    draw.text((40, 34), "VIỆN KHOA HỌC HÌNH SỰ - BỘ CÔNG AN (PHÂN VIỆN HẢI PHÒNG)", fill=(200, 215, 230), font=f_sub)
    draw.text((40, 54), "BẢN GIÁM ĐỊNH KỸ THUẬT: CẦU CHÌ TỔNG 100A BỊ GỌT MỎNG RUỘT CHÌ", fill=(255, 255, 255), font=f_title)
    
    # Left: Macro photo frame of blown ceramic fuse
    draw.rectangle([40, 95, 430, 410], fill=(40, 45, 50), outline=(120, 130, 140))
    draw.text((50, 105), "VẬT CHỨNG: CẦU CHÌ SỨ 100A BỊ NỔ TỦ ĐIỆN CHÍNH", fill=(255, 220, 80), font=f_bold)
    
    # Ceramic fuse body
    draw.rectangle([100, 210, 370, 290], fill=(235, 235, 230), outline=(180, 180, 175), width=2)
    # Copper end caps
    draw.rectangle([80, 205, 110, 295], fill=(190, 120, 50))
    draw.rectangle([360, 205, 390, 295], fill=(190, 120, 50))
    # Black soot blast mark in the center
    draw.ellipse([200, 215, 270, 285], fill=(30, 30, 30))
    draw.ellipse([215, 225, 255, 275], fill=(15, 15, 15))
    draw.text((175, 310), "◄ VẾT CHÁY XÉM HỒ QUANG DO ĐOẢN MẠCH", fill=(255, 120, 120), font=f_bold)
    
    # Right: Vernier Caliper measuring thinned lead wire
    draw.rectangle([450, 95, 760, 410], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((465, 105), "ĐO ĐẠC TRẮC VI DÂY CHÌ CẦU CHÌ", fill=(30, 40, 50), font=f_bold)
    
    # Simulated lead wire diagram
    draw.rectangle([480, 150, 730, 180], fill=(160, 165, 170), outline=(100, 105, 110))
    # Thinned carved notch
    draw.rectangle([580, 160, 640, 180], fill=(240, 240, 240), outline=(200, 50, 50), width=2)
    draw.text((550, 195), "◄ VỊ TRÍ BỊ DÙNG DAO GỌT MỎNG", fill=(200, 30, 30), font=f_bold)
    
    caliper_data = [
        "• Đường kính dây chì tiêu chuẩn 100A: 3.2 mm",
        "• Đo thực tế tại vị trí bị gọt: 0.95 mm",
        "• Tiết diện chì chỉ còn: 29.6% (giảm > 70%)",
        "• Khả năng chịu tải thực tế: Hạ xuống ~28A",
        "• Lưỡi kẹp kìm thu từ Thắng dính mạt chì mềm",
        "  trùng khớp hợp kim với dây chì này 100%."
    ]
    for i, line in enumerate(caliper_data):
        draw.text((465, 230 + i * 26), line, fill=(40, 40, 40), font=f_mono)
        
    # Bottom Conclusion Box
    draw.rectangle([40, 425, 760, 565], fill=(255, 250, 240), outline=(200, 170, 120))
    draw.text((55, 435), "KẾT LUẬN GIÁM ĐỊNH KỸ THUẬT ĐIỆN:", fill=(160, 30, 20), font=f_bold)
    draw.text((55, 460), "1. Cầu chì tổng KHÔNG PHẢI bị đứt ngẫu nhiên do quá tải bão mà đã bị CỐ Ý GỌT MỎNG TIẾT DIỆN.", fill=(30, 30, 30), font=f_bold)
    draw.text((55, 485), "2. Mục đích: Đảm bảo khi thanh lưỡng kim nhiệt T-85 chạm mát gây ngắn mạch, cầu chì sẽ nổ tung NGAY LẬP TỨC", fill=(50, 50, 50), font=f_sub)
    draw.text((55, 505), "   mà không kích hoạt aptomat bảo vệ phụ của máy nổ, dập tắt hoàn toàn ánh sáng đèn biển.", fill=(50, 50, 50), font=f_sub)
    
    save_webp(img, "d10-cau-chi-got-mong.webp")

# 5. d13-so-do-ngan-mach.webp (800x600) - Delayed Thermal Short-Circuit Schematic
def render_d13():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (18, 32, 52)) # Circuit schematic navy
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Outer Frame
    draw.rectangle([25, 25, w - 25, h - 25], outline=(80, 140, 200), width=2)
    draw.text((45, 40), "SƠ ĐỒ NGUYÊN LÝ BẪY ĐOẢN MẠCH NHIỆT TRỄ (DELAYED THERMAL SHORT-CIRCUIT)", fill=(255, 255, 255), font=f_title)
    draw.text((45, 65), "Phục dựng cơ chế hẹn giờ mất điện 103 phút của thủ phạm Vũ Văn Thắng đêm 24/09/1998", fill=(140, 190, 230), font=f_sub)
    
    # Circuit Box 1: Yanmar Generator Stator Coil
    draw.rectangle([50, 110, 280, 270], fill=(25, 50, 80), outline=(255, 220, 80), width=2)
    draw.text((65, 125), "MÁY NỔ YANMAR 50kVA", fill=(255, 220, 90), font=f_bold)
    draw.text((65, 145), "Cuộn dây stato sinh nhiệt", fill=(200, 220, 240), font=f_sub)
    
    # Coil graphic
    for cy in range(175, 250, 15):
        draw.ellipse([80, cy, 140, cy + 20], outline=(220, 120, 40), width=2)
    draw.text((155, 195), "Nhiệt độ tăng dần:", fill=(255, 180, 180), font=f_mono)
    draw.text((155, 215), "22h00: 45°C", fill=(200, 220, 240), font=f_mono)
    draw.text((155, 235), "23h43: 85°C (ĐỈNH)", fill=(255, 80, 80), font=f_bold)
    
    # Arrow to Bimetal Strip
    draw.line([(280, 190), (360, 190)], fill=(255, 220, 80), width=3)
    
    # Circuit Box 2: Bimetallic Strip Mechanism
    draw.rectangle([360, 110, 550, 270], fill=(25, 50, 80), outline=(255, 100, 100), width=2)
    draw.text((375, 125), "THANH LƯỠNG KIM T-85", fill=(255, 120, 120), font=f_bold)
    draw.text((375, 145), "(Tháo từ tủ sấy quần áo)", fill=(200, 220, 240), font=f_sub)
    
    # Bent Strip graphic
    draw.arc([390, 170, 520, 250], 180, 0, fill=(240, 240, 240), width=4)
    draw.ellipse([515, 205, 535, 225], fill=(255, 50, 50)) # Spark contact point
    draw.text((380, 235), "Độ cong 4mm chạm vỏ mát!", fill=(255, 80, 80), font=f_bold)
    
    # Arrow to Fuse
    draw.line([(550, 190), (620, 190)], fill=(255, 80, 80), width=3)
    
    # Circuit Box 3: Thinned Fuse explosion
    draw.rectangle([620, 110, 750, 270], fill=(35, 20, 20), outline=(255, 50, 50), width=2)
    draw.text((630, 125), "CẦU CHÌ GỌT MỎNG", fill=(255, 80, 80), font=f_bold)
    draw.text((630, 145), "(Tiết diện còn 30%)", fill=(255, 200, 200), font=f_sub)
    draw.ellipse([660, 180, 710, 230], fill=(255, 200, 50))
    draw.text((645, 240), "NỔ TUNG 23:43!", fill=(255, 255, 255), font=f_bold)
    
    # Bottom Timeline Step-by-step
    draw.rectangle([50, 300, 750, 550], fill=(24, 45, 72), outline=(100, 160, 220))
    draw.text((65, 315), "TRÌNH TỰ THỦ PHÁP TẠO CHỨNG CỨ NGOẠI PHẠM CỦA VŨ VĂN THẮNG:", fill=(255, 220, 80), font=f_bold)
    
    steps = [
        "• Bước 1 (22:00): Gọt mỏng dây chì cầu chì tổng + kẹp thanh lưỡng kim T-85 vào cuộn stato máy phát Yanmar.",
        "• Bước 2 (23:25): Lên phòng tầng 2 đâm Trạm trưởng Quyết bằng dao găm, đẩy xác xuống vách biển sâu 25 mét.",
        "• Bước 3 (23:35): Chạy nhanh xuống hầm máy nổ, cầm kìm và cờ-lê đứng chờ sẵn.",
        "• Bước 4 (23:43): Sau đúng 103 phút sinh nhiệt, thanh lưỡng kim đạt 85°C chạm vỏ mát -> Cầu chì nổ tung, đèn tắt ngấm.",
        "• Bước 5 (23:46): Tùng trên tháp chạy thục mạng xuống hầm, thấy Thắng đã đứng sẵn trong khói, tưởng Thắng ở đó cả đêm!",
        "• Bước 6 (00:00): Thắng kéo dài 17 phút 'sửa chữa giả vờ' rồi đóng máy phụ, ngọn đèn sáng lại hoàn tất ngoại phạm."
    ]
    for i, s in enumerate(steps):
        color = (255, 180, 180) if "Bước 2" in s else ((255, 230, 120) if "Bước 4" in s else (220, 235, 250))
        draw.text((65, 345 + i * 32), s, fill=color, font=f_mono)
        
    save_webp(img, "d13-so-do-ngan-mach.webp")

# 6. d14-dao-gam-va-kim.webp (800x600) - Evidence Table: Diving Dagger and Needle-nose Pliers
def render_d14():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (42, 45, 48)) # Stainless steel evidence table
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Table border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(80, 90, 100), width=2)
    
    # Header banner
    draw.rectangle([30, 30, w - 30, 80], fill=(25, 28, 32))
    draw.text((45, 40), "CÔNG AN TP HẢI PHÒNG - BÀN KIỂM KÊ TANG VẬT TRỌNG ÁN HÒN DÁU", fill=(200, 210, 220), font=f_bold)
    draw.text((45, 58), "TANG VẬT THU GIỮ TỪ TÚI ĐỒ NGHỀ VÀ HỐC MÁY CỦA VŨ VĂN THẮNG", fill=(255, 100, 100), font=f_title)
    
    # Evidence 1: Diving Dagger (Dao găm thợ lặn US Divers)
    draw.rectangle([40, 95, 760, 290], fill=(32, 35, 38), outline=(90, 100, 110))
    # Knife blade
    draw.polygon([(260, 180), (600, 160), (620, 180), (600, 200), (260, 200)], fill=(190, 195, 200), outline=(100, 105, 110), width=2)
    # Blood groove (rãnh thoát máu)
    draw.line([(280, 185), (570, 180)], fill=(120, 20, 20), width=4)
    # Knife handle (chuôi cao su đen)
    draw.rectangle([130, 165, 260, 215], fill=(20, 22, 24), outline=(60, 65, 70), width=2)
    # L-marker 01
    draw.rectangle([60, 130, 110, 180], fill=(240, 210, 50))
    draw.text((75, 140), "01", fill=(0, 0, 0), font=f_bold)
    
    draw.text((130, 135), "TANG VẬT 01: DAO GĂM THỢ LẶN QUÂN DỤNG (US DIVERS 25CM)", fill=(255, 220, 90), font=f_bold)
    draw.text((130, 230), "• Giấu kín trong hốc thông gió máy nổ phụ Yanmar 15kVA.", fill=(200, 210, 220), font=f_sub)
    draw.text((130, 250), "• Trong rãnh thoát máu còn đọng vết máu khô có kiểu gen ADN trùng khớp Trạm trưởng Quyết.", fill=(255, 150, 150), font=f_mono)
    draw.text((130, 268), "• Kích thước bản dao khớp 100% với vết đâm thấu ngực sâu 12cm tại d03.", fill=(255, 200, 200), font=f_mono)
    
    # Evidence 2: Needle-nose pliers (Kìm mỏ nhọn cán nhựa đỏ)
    draw.rectangle([40, 305, 760, 480], fill=(32, 35, 38), outline=(90, 100, 110))
    # Pliers body
    draw.polygon([(280, 380), (420, 360), (450, 380), (420, 400), (280, 400)], fill=(170, 175, 180))
    # Red insulated handles
    draw.rectangle([140, 355, 280, 385], fill=(200, 40, 40))
    draw.rectangle([140, 395, 280, 425], fill=(200, 40, 40))
    # L-marker 02
    draw.rectangle([60, 340, 110, 390], fill=(240, 210, 50))
    draw.text((75, 350), "02", fill=(0, 0, 0), font=f_bold)
    
    draw.text((130, 335), "TANG VẬT 02: KÌM MỎ NHỌN CÁN NHỰA ĐỎ CỦA THẮNG", fill=(255, 220, 90), font=f_bold)
    draw.text((130, 435), "• Thu giữ trong túi đồ nghề cơ điện dưới chân giường ngủ của Thắng.", fill=(200, 210, 220), font=f_sub)
    draw.text((130, 455), "• Trên lưỡi kẹp dính mạt kim loại chì mềm trùng khớp thành phần dây cầu chì bị gọt mỏng tại d10.", fill=(255, 200, 120), font=f_mono)
    
    # Bottom Forensic Tag
    draw.rectangle([40, 495, 760, 565], fill=(20, 25, 30), outline=(100, 120, 140))
    draw.text((55, 510), "KẾT LUẬN TANG CHỨNG: Cặp vật chứng hoàn hảo chứng minh Vũ Văn Thắng vừa là kẻ chế tạo", fill=(255, 220, 90), font=f_bold)
    draw.text((55, 535), "bẫy ngắn mạch cầu chì (tang vật 02), vừa là kẻ trực tiếp đâm chết Trạm trưởng Quyết (tang vật 01).", fill=(255, 255, 255), font=f_sub)
    
    save_webp(img, "d14-dao-gam-va-kim.webp")

# 7. d16-trang-nhat-ky-xe.webp (700x520) - Scanned Restored Torn Diary Page
def render_d16():
    w, h = 700, 520
    img = Image.new('RGB', (w, h), (235, 230, 215)) # Weathered crumpled paper desk
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    f_hand = get_font(FONT_ARIAL, 14)
    f_hand_bold = get_font(FONT_HELVETICA, 15)
    
    # Torn page rectangle with ragged edges
    draw.rectangle([50, 40, w - 50, h - 40], fill=(250, 246, 235), outline=(180, 160, 130), width=1)
    
    # Oil stains (dầu diesel) from air filter
    draw.ellipse([80, 60, 180, 150], fill=(235, 215, 165))
    draw.ellipse([480, 320, 620, 440], fill=(230, 210, 155))
    
    # Crumple fold lines
    draw.line([(50, 180), (650, 220)], fill=(210, 195, 175), width=1)
    draw.line([(220, 40), (310, 480)], fill=(210, 195, 175), width=1)
    
    # Handwritten diary text (Trạm trưởng Quyết's handwriting)
    blue_ink = (25, 45, 110)
    draw.text((80, 70), "Hòn Dáu, chiều 24/09/1998 (trước bão số 5)", fill=blue_ink, font=f_hand_bold)
    
    text_lines = [
        "Hôm nay tôi đã tiến hành kiểm kê đột xuất kho dầu ngầm",
        "dự trữ chiến lược của trạm. Kết quả hao hụt tới 3.200 lít dầu",
        "diesel chuyên dụng cấp phát cho máy phát điện tháp đèn.",
        "",
        "Phó trạm trưởng Vũ Văn Thắng đã phải thừa nhận hành vi",
        "thông đồng với các tàu cá ngoài luồng để rút trộm dầu đem bán.",
        "Thắng quỳ lạy xin tôi bỏ qua và hứa sẽ đền bù dần,",
        "nhưng đây là tội ác đe dọa trực tiếp an toàn luồng hàng hải!",
        "",
        "Tôi kiên quyết lập biên bản vi phạm kỷ luật nghiêm trọng.",
        "Ngay sau khi tan bão số 5, tôi sẽ trực tiếp giao biên bản này",
        "cho Đoàn thanh tra của Sở Giao thông ra đảo vào thứ Hai tới.",
        "",
        "Ký tên: Đỗ Đình Quyết (Trạm trưởng)"
    ]
    
    y = 110
    for line in text_lines:
        color = (180, 30, 30) if "3.200 lít dầu" in line or "Vũ Văn Thắng" in line or "Đoàn thanh tra" in line else blue_ink
        draw.text((80, y), line, fill=color, font=f_hand)
        y += 24
        
    # Police Forensic restoration stamp
    draw.rectangle([340, 410, w - 70, 465], fill=(255, 240, 190), outline=(180, 150, 80))
    draw.text((355, 418), "BẢN PHỤC CHẾ TÀI LIỆU BỊ TIÊU HỦY", fill=(160, 30, 20), font=f_bold)
    draw.text((355, 438), "Thu giữ trong bầu lọc gió máy nổ phụ - 26/09/1998", fill=(50, 50, 50), font=f_mono)
    
    save_webp(img, "d16-trang-nhat-ky-xe.webp")

if __name__ == "__main__":
    render_d03()
    render_d04()
    render_d05()
    render_d10()
    render_d13()
    render_d14()
    render_d16()
    print("All Case 08 standard visual assets generated successfully.")
