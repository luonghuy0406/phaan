#!/usr/bin/env python3
import os
import random
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "/Users/huynguyen/Documents/game_pha_an/public/cases/ly-tra-trao-doc/images"
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

# 1. d03-giam-dinh-doc-chat.webp (800x600) - Forensic Toxicology Chart & Stomach Pathology
def render_d03():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (242, 244, 245))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 20)
    f_sub = get_font(FONT_HELVETICA, 13)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 14)
    
    # Header border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(180, 190, 195), width=2)
    draw.rectangle([30, 30, w - 30, 85], fill=(230, 236, 240), outline=(160, 175, 185))
    
    draw.text((45, 38), "VIỆN PHÁP Y QUÂN ĐỘI - PHÂN VIỆN PHÁP Y ĐỘC CHẤT", fill=(20, 40, 60), font=f_bold)
    draw.text((45, 58), "PHIẾU KẾT QUẢ SẮC KÝ KHÍ KHỐI PHỔ (GC-MS) & ĐỘC CHẤT HỌC", fill=(100, 30, 30), font=f_title)
    
    # Left Box: Toxicology Spectrogram Chart
    draw.rectangle([40, 105, 470, 370], fill=(255, 255, 255), outline=(170, 180, 190))
    draw.text((50, 115), "BIỂU ĐỒ SẮC KÝ ĐỘC CHẤT: MẪU MÁU & DỊCH DẠ DÀY ĐOÀN THỊ THỦY", fill=(40, 50, 60), font=f_sub)
    
    # Grid lines
    for y in range(145, 330, 30):
        draw.line([(70, y), (450, y)], fill=(235, 238, 240), width=1)
    for x in range(70, 460, 50):
        draw.line([(x, 145), (x, 330)], fill=(235, 238, 240), width=1)
    draw.line([(70, 330), (450, 330)], fill=(80, 90, 100), width=2)
    draw.line([(70, 145), (70, 330)], fill=(80, 90, 100), width=2)
    
    # Spectrogram baseline & giant NaCN peak
    pts = [
        (70, 328), (110, 327), (140, 328), (170, 326), (195, 325),
        (210, 324), (220, 170), (225, 160), (230, 324), # Huge Cyanide peak
        (260, 326), (290, 310), (300, 326), # Minor metabolite
        (340, 327), (380, 328), (450, 328)
    ]
    draw.line(pts, fill=(180, 20, 20), width=2)
    draw.polygon([(215, 328), (220, 170), (225, 160), (230, 324), (230, 328)], fill=(255, 200, 200))
    
    draw.text((235, 165), "◄ ĐỈNH NATRI XYANUA (NaCN)", fill=(180, 0, 0), font=f_bold)
    draw.text((235, 185), "Nồng độ: 4.8 mg/L (Gấp 8 lần liều tử vong)", fill=(140, 20, 20), font=f_mono)
    draw.text((235, 205), "Thời gian lưu (tR): 3.42 phút", fill=(80, 80, 80), font=f_mono)
    
    # Right Box: Forensic Pathology Diagram / Findings
    draw.rectangle([485, 105, 760, 370], fill=(255, 255, 255), outline=(170, 180, 190))
    draw.text((495, 115), "DẤU HIỆU GIẢI PHẪU ĐẶC TRƯNG", fill=(40, 50, 60), font=f_sub)
    
    # Graphic stomach silhouette representation
    draw.ellipse([540, 150, 700, 250], fill=(240, 160, 160), outline=(190, 40, 40), width=2)
    draw.ellipse([570, 175, 660, 225], fill=(220, 50, 50))
    draw.text((545, 260), "Niêm mạc dạ dày sung huyết", fill=(160, 20, 20), font=f_sub)
    draw.text((545, 278), "ĐỎ TƯƠI ANH ĐÀO (CHERRY-RED)", fill=(180, 0, 0), font=f_bold)
    draw.text((500, 305), "• Khí thở & dịch dạ dày: Mùi hạnh nhân đắng", fill=(40, 40, 40), font=f_sub)
    draw.text((500, 325), "• Ngừng hô hấp tế bào tối cấp (ức chế Cytochrome c)", fill=(40, 40, 40), font=f_sub)
    draw.text((500, 345), "• Thời gian tử vong: < 5 phút sau uống ngụm đầu", fill=(120, 20, 20), font=f_mono)
    
    # Bottom Summary & Stamp
    draw.rectangle([40, 385, 760, 565], fill=(255, 255, 250), outline=(170, 180, 190))
    draw.text((55, 395), "KẾT LUẬN GIÁM ĐỊNH PHÁP Y:", fill=(20, 30, 40), font=f_bold)
    concl = [
        "1. Nạn nhân Đoàn Thị Thủy tử vong do suy tuần hoàn và hô hấp tối cấp vì ngộ độc Natri Xyanua liều lượng cực cao.",
        "2. Độc chất hấp thu qua đường tiêu hóa từ cốc trà sữa nạn nhân uống dở lúc 07h15 ngày 03/12/2019.",
        "3. Lượng độc chất trong dịch dạ dày đủ để gây tử vong cho nhiều người trưởng thành."
    ]
    for i, line in enumerate(concl):
        draw.text((55, 420 + i * 22), line, fill=(40, 40, 40), font=f_sub)
        
    # Red circular rubber seal
    draw.ellipse([620, 450, 710, 540], outline=(200, 40, 40), width=3)
    draw.text((632, 475), "GIÁM ĐỊNH", fill=(200, 40, 40), font=f_mono)
    draw.text((635, 495), "PHÁP Y", fill=(200, 40, 40), font=f_mono)
    
    save_webp(img, "d03-giam-dinh-doc-chat.webp")

# 2. d04-so-do-khoa-noi.webp (800x600) - Hospital Inpatient Ward Blueprint
def render_d04():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (18, 42, 68)) # Blueprint navy cyan
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Grid lines
    for x in range(30, w - 30, 25):
        draw.line([(x, 30), (x, h - 30)], fill=(28, 58, 92), width=1)
    for y in range(30, h - 30, 25):
        draw.line([(30, y), (w - 30, y)], fill=(28, 58, 92), width=1)
        
    draw.rectangle([30, 30, w - 30, h - 30], outline=(90, 160, 220), width=2)
    
    # Title
    draw.text((50, 45), "SƠ ĐỒ HIỆN TRƯỜNG: KHOA NỘI - BỆNH VIỆN ĐA KHOA TỈNH THÁI BÌNH (TẦNG 3)", fill=(255, 255, 255), font=f_title)
    draw.text((50, 70), "Vụ việc tử vong ngày 03/12/2019 - Tỷ lệ 1:100 - Khám nghiệm kỹ thuật hình sự", fill=(140, 190, 230), font=f_sub)
    
    # Corridor
    draw.rectangle([60, 250, 740, 310], outline=(100, 170, 230), width=2)
    draw.text((320, 275), "◄ HÀNH LANG CHÍNH TẦNG 3 ►", fill=(140, 200, 255), font=f_bold)
    
    # Room 1: Phòng Giao ban (Án mạng)
    draw.rectangle([60, 105, 340, 250], outline=(255, 220, 80), width=3)
    draw.text((70, 115), "PHÒNG GIAO BAN & TRỰC ĐIỀU DƯỠNG [HIỆN TRƯỜNG]", fill=(255, 230, 90), font=f_bold)
    
    # Inside Room 1: Refrigerator & Table
    draw.rectangle([80, 150, 140, 200], fill=(40, 90, 140), outline=(255, 80, 80), width=2)
    draw.text((85, 165), "TỦ LẠNH", fill=(255, 255, 255), font=f_mono)
    draw.text((85, 180), "CHUNG", fill=(255, 255, 255), font=f_mono)
    
    # Arrow to fridge
    draw.text((150, 165), "◄ Nơi cất 6 cốc trà sữa (02/12)", fill=(255, 120, 120), font=f_bold)
    
    # Table where Thuy collapsed
    draw.rectangle([200, 150, 320, 200], fill=(30, 70, 110), outline=(140, 200, 255))
    draw.text((210, 160), "BÀN TRỰC KHOA", fill=(200, 230, 255), font=f_sub)
    draw.text((210, 180), "[Cốc trà dở số 1]", fill=(255, 200, 100), font=f_mono)
    
    # Restroom where Thuy collapsed
    draw.rectangle([60, 205, 140, 245], outline=(140, 200, 255))
    draw.text((70, 215), "VỆ SINH", fill=(180, 220, 255), font=f_mono)
    draw.text((150, 218), "◄ Nạn nhân ngã gục lúc 07h20", fill=(255, 100, 100), font=f_mono)
    
    # Room 2: Bàn làm việc Bác sĩ Yến (mục tiêu)
    draw.rectangle([350, 105, 540, 250], outline=(100, 170, 230), width=2)
    draw.text((360, 115), "PHÒNG BÁC SĨ ĐIỀU TRỊ", fill=(200, 230, 255), font=f_bold)
    draw.rectangle([380, 150, 500, 195], fill=(30, 70, 110), outline=(255, 200, 80))
    draw.text((390, 160), "BÀN BS ĐỖ THỊ YẾN", fill=(255, 220, 90), font=f_bold)
    draw.text((390, 178), "(Nghỉ bù ngày 02-03/12)", fill=(180, 210, 240), font=f_mono)
    
    # Room 3: Phòng hành chính / tiếp dân
    draw.rectangle([550, 105, 740, 250], outline=(100, 170, 230), width=2)
    draw.text((560, 115), "PHÒNG HÀNH CHÍNH KHOA", fill=(200, 230, 255), font=f_sub)
    draw.text((560, 160), "Nơi shipper gửi túi trà", fill=(180, 210, 240), font=f_mono)
    draw.text((560, 178), "kèm túi quýt (16h 02/12)", fill=(180, 210, 240), font=f_mono)
    
    # Patient Rooms bottom
    draw.rectangle([60, 320, 270, 480], outline=(100, 170, 230), width=2)
    draw.text((70, 330), "PHÒNG BỆNH NHÂN 301", fill=(180, 210, 240), font=f_sub)
    draw.rectangle([290, 320, 510, 480], outline=(100, 170, 230), width=2)
    draw.text((300, 330), "PHÒNG BỆNH NHÂN 302", fill=(180, 210, 240), font=f_sub)
    draw.rectangle([530, 320, 740, 480], outline=(100, 170, 230), width=2)
    draw.text((540, 330), "CẦU THANG BỘ & THANG MÁY", fill=(180, 210, 240), font=f_sub)
    
    # Legend box bottom
    draw.rectangle([60, 495, 740, 555], fill=(24, 52, 82), outline=(100, 170, 230))
    draw.text((75, 505), "CHÚ DẪN PHÁP LÝ:", fill=(255, 220, 80), font=f_bold)
    draw.text((75, 525), "• Vệt đỏ đứt đoạn: Lộ trình shipper mang túi trà lên khoa 02/12 -> Cất vào tủ lạnh chung -> Nạn nhân Thủy lấy uống sáng 03/12.", fill=(220, 235, 250), font=f_mono)
    
    save_webp(img, "d04-so-do-khoa-noi.webp")

# 3. d09-giay-nhan.webp (700x500) - Scanned student lined note with purple ink
def render_d09():
    w, h = 700, 500
    img = Image.new('RGB', (w, h), (248, 246, 238)) # Kraft paper desk
    draw = ImageDraw.Draw(img)
    
    f_hand = get_font(FONT_ARIAL, 20)
    f_hand_bold = get_font(FONT_HELVETICA, 22)
    f_mono = get_font(FONT_COURIER, 12)
    
    # Student paper note with blue/red grid lines
    draw.rectangle([60, 50, w - 60, h - 50], fill=(255, 255, 252), outline=(210, 205, 190), width=1)
    
    # Notebook grid lines
    for y in range(90, h - 70, 32):
        draw.line([(80, y), (w - 80, y)], fill=(220, 230, 245), width=1)
    draw.line([(140, 60), (140, h - 60)], fill=(245, 190, 190), width=1) # Margin line
    
    # Paper clip at top left
    draw.rectangle([90, 40, 110, 80], outline=(120, 125, 130), width=2)
    
    # Purple handwritten note
    purple = (90, 30, 130)
    draw.text((160, 110), "Gửi chị Yến Khoa Nội!", fill=purple, font=f_hand_bold)
    draw.text((160, 175), "Em cảm ơn chị và các bác sĩ", fill=purple, font=f_hand)
    draw.text((160, 240), "Khoa Nội đã tận tình chăm sóc", fill=purple, font=f_hand)
    draw.text((160, 305), "cho người nhà em thời gian qua ạ!", fill=purple, font=f_hand)
    draw.text((360, 368), "(Em gửi chút quà biếu các chị!)", fill=(110, 50, 140), font=f_hand)
    
    # Evidence tape / label bottom right
    draw.rectangle([350, 415, w - 80, 470], fill=(255, 240, 180), outline=(180, 160, 90))
    draw.text((365, 422), "VẬT CHỨNG VỤ ÁN HÌNH SỰ", fill=(140, 40, 20), font=f_mono)
    draw.text((365, 442), "Kẹp ngoài túi trà sữa ngày 02/12/2019", fill=(60, 60, 60), font=f_mono)
    
    save_webp(img, "d09-giay-nhan.webp")

# 4. d10-trich-xuat-dien-thoai.webp (800x600) - Cellebrite Digital Forensics Report
def render_d10():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (245, 247, 250))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Header bar
    draw.rectangle([25, 20, w - 25, 75], fill=(30, 45, 65))
    draw.text((40, 28), "CƠ QUAN AN NINH MẠNG & KỸ THUẬT HÌNH SỰ - CÔNG AN THÁI BÌNH", fill=(200, 215, 230), font=f_sub)
    draw.text((40, 48), "BÁO CÁO PHỤC HỒI DỮ LIỆU ĐIỆN THOẠI (CELLEBRITE UFED REPORT)", fill=(255, 255, 255), font=f_title)
    
    # Device Info Box
    draw.rectangle([25, 85, w - 25, 145], fill=(255, 255, 255), outline=(200, 210, 220))
    draw.text((40, 95), "THIẾT BỊ THU GIỮ: Apple iPhone 7 (A1778) - IMEI: 359142084729104", fill=(30, 40, 50), font=f_bold)
    draw.text((40, 115), "CHỦ THIẾT BỊ: Lại Thị Kiều Trang (SN: 1998, Kiến Xương, Thái Bình)", fill=(50, 60, 70), font=f_sub)
    draw.text((450, 115), "Thời gian trích xuất: 04/12/2019 08:45:10", fill=(100, 100, 100), font=f_mono)
    
    # Table Header
    draw.rectangle([25, 155, w - 25, 185], fill=(225, 232, 240))
    draw.text((40, 162), "THỜI GIAN", fill=(30, 40, 50), font=f_bold)
    draw.text((170, 162), "ỨNG DỤNG / NGUỒN", fill=(30, 40, 50), font=f_bold)
    draw.text((330, 162), "NỘI DUNG TÌM KIẾM / TIN NHẮN PHỤC HỒI", fill=(180, 30, 30), font=f_bold)
    
    # Table rows
    rows = [
        ("15/11/2019 21:14", "Safari / Google", "chat doc xyanua mua o dau tai mien bac"),
        ("18/11/2019 14:02", "Safari / Google", "mua natri xyanua o dau tai hai phong xi ma vang"),
        ("23/11/2019 09:20", "Tin nhắn SMS", "Gửi anh Hùng: 'Nếu anh bỏ em, em sẽ làm anh ân hận cả đời!'"),
        ("27/11/2019 23:45", "Safari / Google", "uong xyanua sau bao lau thi chet ngat tho"),
        ("28/11/2019 01:10", "Safari / Google", "cach bom thuoc vao coc nuoc khong bi phat hien lo kim"),
        ("02/12/2019 11:30", "Điện thoại cuộc gọi", "Gọi số tài xế ship Lê Văn Nam (thời lượng 45 giây)"),
        ("03/12/2019 08:12", "Safari / Báo mạng", "doc bao thai binh: nu dieu duong benh vien phoi tu vong"),
        ("03/12/2019 08:35", "Cài đặt hệ thống", "[THAO TÁC XÓA LỊCH SỬ DUYỆT WEB VÀ BỘ NHỚ ĐỆM]")
    ]
    
    y = 195
    for i, (t, app, content) in enumerate(rows):
        bg = (255, 255, 255) if i % 2 == 0 else (248, 250, 252)
        draw.rectangle([25, y - 5, w - 25, y + 25], fill=bg, outline=(230, 235, 240))
        draw.text((40, y), t, fill=(60, 70, 80), font=f_mono)
        draw.text((170, y), app, fill=(40, 80, 120), font=f_sub)
        color = (180, 20, 20) if "xyanua" in content or "bom thuoc" in content or "ân hận" in content else (30, 30, 30)
        draw.text((330, y), content, fill=color, font=f_mono)
        y += 32
        
    # Bottom Note
    draw.rectangle([25, 475, w - 25, 565], fill=(255, 250, 240), outline=(220, 190, 140))
    draw.text((40, 485), "ĐÁNH GIÁ CỦA GIÁM ĐỊNH VIÊN KỸ THUẬT SỐ:", fill=(140, 40, 20), font=f_bold)
    draw.text((40, 508), "• Nghi phạm đã có hành vi chuẩn bị công cụ độc chất từ nửa tháng trước khi gây án.", fill=(40, 40, 40), font=f_sub)
    draw.text((40, 528), "• Thao tác tìm kiếm 'cách bơm thuốc vào cốc nước không bị phát hiện' trùng khớp với thủ đoạn lỗ kim 26G tại d05.", fill=(40, 40, 40), font=f_sub)
    
    save_webp(img, "d10-trich-xuat-dien-thoai.webp")

# 5. d12-van-don-viettelpost.webp (700x520) - Scanned Viettel Post Express Waybill
def render_d12():
    w, h = 700, 520
    img = Image.new('RGB', (w, h), (242, 242, 238))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Waybill paper
    draw.rectangle([30, 25, w - 30, h - 25], fill=(255, 255, 255), outline=(200, 50, 50), width=2)
    
    # Red Viettel Post header
    draw.rectangle([32, 27, w - 32, 75], fill=(220, 30, 30))
    draw.text((50, 38), "TỔNG CÔNG TY CỔ PHẦN BƯU CHÍNH VIETTEL - PHIẾU GỬI HÀNG (WAYBILL)", fill=(255, 255, 255), font=f_title)
    
    # Tracking barcode area
    draw.rectangle([50, 90, 320, 130], fill=(255, 255, 255), outline=(150, 150, 150))
    # Draw simulated barcode lines
    random.seed(99)
    bx = 60
    while bx < 310:
        bw = random.choice([1, 2, 3, 4])
        draw.rectangle([bx, 95, bx + bw, 120], fill=(0, 0, 0))
        bx += bw + random.choice([2, 3, 4])
    draw.text((95, 122), "VT948201847VN", fill=(40, 40, 40), font=f_mono)
    
    draw.text((360, 95), "NGÀY GỬI: 29/11/2019 - 14:20:15", fill=(30, 30, 30), font=f_bold)
    draw.text((360, 115), "DỊCH VỤ: Chuyển phát nhanh Tiết kiệm", fill=(60, 60, 60), font=f_sub)
    
    # Sender / Receiver Split
    draw.rectangle([50, 145, 335, 290], fill=(250, 252, 255), outline=(180, 190, 200))
    draw.text((60, 155), "1. NGƯỜI GỬI (SENDER):", fill=(180, 30, 30), font=f_bold)
    draw.text((60, 180), "CỬA HÀNG HÓA CHẤT NAM CƯỜNG", fill=(30, 30, 30), font=f_bold)
    draw.text((60, 202), "Địa chỉ: Số 84 Đường Lê Chân, Hải Phòng", fill=(60, 60, 60), font=f_sub)
    draw.text((60, 224), "Điện thoại: 0913.xxx.882", fill=(60, 60, 60), font=f_sub)
    draw.text((60, 246), "Ngành hàng: Xi mạ kim loại, hóa chất", fill=(60, 60, 60), font=f_sub)
    
    draw.rectangle([355, 145, 650, 290], fill=(250, 252, 255), outline=(180, 190, 200))
    draw.text((365, 155), "2. NGƯỜI NHẬN (CONSIGNEE):", fill=(180, 30, 30), font=f_bold)
    draw.text((365, 180), "LẠI THỊ KIỀU TRANG", fill=(30, 30, 30), font=f_bold)
    draw.text((365, 202), "Địa chỉ: Xã Vũ Quý, Kiến Xương, Thái Bình", fill=(60, 60, 60), font=f_sub)
    draw.text((365, 224), "Điện thoại: 0984.xxx.112 (Số cá nhân Trang)", fill=(180, 20, 20), font=f_bold)
    draw.text((365, 246), "Trạng thái: ĐÃ GIAO THÀNH CÔNG 30/11", fill=(20, 120, 40), font=f_bold)
    
    # Goods description
    draw.rectangle([50, 305, 650, 410], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((60, 315), "3. NỘI DUNG HÀNG HÓA & CƯỚC PHÍ:", fill=(40, 40, 40), font=f_bold)
    draw.text((60, 340), "Tên hàng: 'Hóa chất thí nghiệm xi mạ - 1kg Natri Xyanua (dạng bột tinh thể)'", fill=(180, 20, 20), font=f_bold)
    draw.text((60, 362), "Trọng lượng: 1.15 kg | Tiền thu hộ COD: 650.000 VNĐ | Cước: 45.000 VNĐ", fill=(50, 50, 50), font=f_mono)
    draw.text((60, 384), "Ký nhận: 'Đã nhận đủ gói hóa chất nguyên đai' - Chữ ký: Trang", fill=(30, 30, 30), font=f_mono)
    
    # Police Evidence Stamp
    draw.ellipse([510, 395, 630, 485], outline=(200, 30, 30), width=3)
    draw.text((535, 425), "TANG VẬT", fill=(200, 30, 30), font=f_mono)
    draw.text((538, 445), "ÁP GIẢI", fill=(200, 30, 30), font=f_mono)
    
    save_webp(img, "d12-van-don-viettelpost.webp")

# 6. d14-camera-quan-tra.webp (800x550) - CCTV frame at Milk Tea shop & POS validation
def render_d14():
    w, h = 800, 550
    img = Image.new('RGB', (w, h), (15, 20, 25)) # Dark surveillance monitor
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Monitor frame
    draw.rectangle([20, 20, w - 20, h - 20], outline=(70, 85, 95), width=2)
    
    # Camera OSD (On Screen Display)
    draw.text((40, 35), "CAM-01 [QUẦY THU NGÂN POS] - TRÀ SỮA LÝ THƯỜNG KIỆT", fill=(0, 255, 120), font=f_mono)
    draw.text((w - 240, 35), "REC ● 02/12/2019 10:15:22", fill=(255, 60, 60), font=f_mono)
    
    # Left Box: Simulated Surveillance Frame
    draw.rectangle([40, 70, 480, 450], fill=(30, 38, 45), outline=(100, 120, 130))
    # Counter outline
    draw.polygon([(40, 320), (280, 290), (480, 340), (480, 450), (40, 450)], fill=(45, 55, 65))
    draw.text((120, 360), "[QUẦY PHA CHẾ & DẬP MÀNG NHIỆT]", fill=(120, 140, 150), font=f_sub)
    
    # Suspect silhouette
    draw.ellipse([260, 160, 330, 230], fill=(180, 40, 40)) # Red jacket
    draw.ellipse([275, 120, 315, 160], fill=(220, 190, 170)) # Face with mask
    draw.rectangle([280, 140, 310, 155], fill=(240, 240, 240)) # White medical mask
    draw.text((230, 245), "Đối tượng nữ (áo khoác đỏ)", fill=(255, 200, 100), font=f_sub)
    draw.text((230, 265), "Mua 6 cốc trà sữa dập nắp", fill=(255, 255, 255), font=f_bold)
    
    # Right Box: POS Transaction match & Verification
    draw.rectangle([495, 70, 760, 450], fill=(248, 248, 242), outline=(180, 190, 200))
    draw.text((510, 85), "ĐỐI CHIẾU DỮ LIỆU MÁY BÁN HÀNG", fill=(20, 30, 40), font=f_bold)
    draw.line([(510, 105), (745, 105)], fill=(200, 50, 50), width=2)
    
    pos_lines = [
        "Cửa hàng: Trà sữa Lý Thường Kiệt",
        "Số HĐ: #TB19-08291",
        "Giờ in: 10:15:22 (Khớp 100% camera)",
        "---------------------------------",
        "1. Trà Ô long kem cheese (L) x2",
        "2. Trà sữa nướng trân châu (L) x2",
        "3. Trà xoài kem sữa (L) x2",
        "---------------------------------",
        "Tổng tiền: 314.000 VNĐ",
        "Khách trả: 500.000 VNĐ tiền mặt",
        "Nắp cốc: Dập màng nilon nhiệt kín"
    ]
    for i, pline in enumerate(pos_lines):
        color = (180, 20, 20) if "Trà Ô long" in pline or "Dập màng" in pline else (50, 50, 50)
        draw.text((510, 120 + i * 22), pline, fill=color, font=f_mono)
        
    # Footer confirmation
    draw.rectangle([40, 470, w - 40, 520], fill=(25, 32, 40), outline=(80, 100, 120))
    draw.text((55, 485), "KẾT QUẢ TRÍCH XUẤT: Xác nhận Lại Thị Kiều Trang đi xe Vision đỏ BKS 17B1-482.91 vào mua 6 cốc trà mang về nhà bơm xyanua.", fill=(255, 220, 90), font=f_sub)
    
    save_webp(img, "d14-camera-quan-tra.webp")

if __name__ == "__main__":
    render_d03()
    render_d04()
    render_d09()
    render_d10()
    render_d12()
    render_d14()
    print("All Case 13 visual assets successfully generated.")
