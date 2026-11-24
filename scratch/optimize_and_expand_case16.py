#!/usr/bin/env python3
import os
import random
from PIL import Image, ImageDraw, ImageFont

IMG_DIR = "/Users/huynguyen/Documents/game_pha_an/public/cases/quai-vat-21-khuon-mat/images"
os.makedirs(IMG_DIR, exist_ok=True)

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
    p = os.path.join(IMG_DIR, filename)
    out_img.save(p, "WEBP", quality=88)
    print(f"✓ Saved: {filename} ({os.path.getsize(p)} bytes)")

# 1. Optimize existing oversized images
def optimize_existing():
    oversized = [
        ("cover.webp", (900, 1200), 82),
        ("d01-bao-chi.webp", (1024, 640), 82),
        ("d05-buc-thu.webp", (800, 1000), 82),
        ("d11-hop-keo.webp", (800, 800), 82),
        ("d15-bieu-do-co-phieu.webp", (1024, 600), 82),
    ]
    for fn, max_size, q in oversized:
        p = os.path.join(IMG_DIR, fn)
        if os.path.exists(p):
            with Image.open(p) as im:
                im.thumbnail(max_size, Image.Resampling.LANCZOS)
                im.save(p, "WEBP", quality=q)
            print(f"✓ Optimized {fn} -> {os.path.getsize(p)} bytes")

# 2. Rename / copy d08-phac-hoa-mat-cao.webp to d09-phac-hoa-mat-cao.webp
def fix_d09_sketch():
    src = os.path.join(IMG_DIR, "d08-phac-hoa-mat-cao.webp")
    dst = os.path.join(IMG_DIR, "d09-phac-hoa-mat-cao.webp")
    if os.path.exists(src):
        os.rename(src, dst)
        print("✓ Renamed d08-phac-hoa-mat-cao.webp -> d09-phac-hoa-mat-cao.webp")

# 3. d03-giam-dinh-doc-chat.webp (800x600) - Osaka Police Forensic Science Lab: Potassium Cyanide
def render_d03():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (242, 244, 246))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Outer Border
    draw.rectangle([20, 20, w - 20, h - 20], outline=(170, 180, 190), width=2)
    draw.rectangle([30, 30, w - 30, 80], fill=(230, 235, 240), outline=(160, 170, 180))
    
    draw.text((45, 36), "CỤC CẢNH SÁT QUỐC GIA NHẬT BẢN - PHÂN VIỆN KHOA HỌC HÌNH SỰ OSAKA", fill=(30, 45, 60), font=f_bold)
    draw.text((45, 54), "PHIẾU HÓA NGHIỆM ĐỘC CHẤT PHÁP Y: HỘP KẸO GLICO & MORINAGA (THÁNG 10/1984)", fill=(150, 20, 20), font=f_title)
    
    # Left Box: Spectrogram Graph of Potassium Cyanide (KCN)
    draw.rectangle([40, 95, 450, 400], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((50, 105), "QUANG PHỔ ĐỊNH LƯỢNG KALI XYANUA (KCN)", fill=(30, 40, 50), font=f_bold)
    
    for y in range(140, 320, 30):
        draw.line([(60, y), (430, y)], fill=(235, 240, 245), width=1)
    draw.line([(60, 320), (430, 320)], fill=(80, 90, 100), width=2)
    draw.line([(60, 140), (60, 320)], fill=(80, 90, 100), width=2)
    
    # Massive Cyanide Peak
    pts = [
        (60, 318), (120, 317), (180, 316), (220, 315),
        (235, 160), (240, 150), (245, 315),
        (290, 317), (350, 318), (430, 318)
    ]
    draw.line(pts, fill=(180, 20, 20), width=2)
    draw.polygon([(230, 318), (235, 160), (240, 150), (245, 315), (245, 318)], fill=(255, 200, 200))
    
    draw.text((255, 160), "◄ ĐỈNH KALI XYANUA (KCN)", fill=(180, 0, 0), font=f_bold)
    draw.text((255, 180), "Hàm lượng: 80 mg / viên kẹo", fill=(140, 20, 20), font=f_mono)
    draw.text((255, 200), "(Liều lượng đủ giết chết 2 người lớn)", fill=(140, 20, 20), font=f_mono)
    draw.text((255, 220), "Dạng muối tinh thể hòa tan nhanh", fill=(60, 60, 60), font=f_mono)
    
    draw.text((60, 340), "MẪU VẬT CHỨNG: Viên socola Glico thu tại siêu thị Daiei Osaka.", fill=(40, 40, 40), font=f_sub)
    draw.text((60, 360), "Thủ đoạn: Dùng mũi khoan siêu nhỏ 0.5mm khoét đáy viên kẹo nhét bột KCN.", fill=(160, 30, 20), font=f_mono)
    
    # Right Box: Warning Label & Physical Box Details
    draw.rectangle([465, 95, 760, 400], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((475, 105), "NHÃN CẢNH BÁO CỦA HUNG THỦ", fill=(30, 40, 50), font=f_bold)
    
    # Simulated Warning sticker affixed to the box
    draw.rectangle([485, 140, 740, 240], fill=(255, 255, 200), outline=(200, 30, 30), width=3)
    draw.text((500, 150), "どく入り きけん (DOKUIRI KIKEN)", fill=(200, 20, 20), font=f_bold)
    draw.text((500, 175), "ĐÃ TẨM ĐỘC - NGUY HIỂM", fill=(180, 0, 0), font=f_bold)
    draw.text((500, 195), "Ăn vào sẽ chết. Ai ăn ráng chịu!", fill=(40, 40, 40), font=f_sub)
    draw.text((500, 215), "Ký tên: Quái vật 21 khuôn mặt", fill=(20, 30, 90), font=f_mono)
    
    draw.text((475, 260), "ĐẶC TRƯNG TỘI PHẠM HỌC:", fill=(30, 40, 50), font=f_bold)
    notes = [
        "• Hung thủ dán nhãn độc lộ liễu nhằm",
        "  gây tê liệt xã hội, không nhằm thảm sát.",
        "• Mục đích chính: Buộc tập đoàn thu hồi",
        "  hàng triệu sản phẩm, ép cổ phiếu sụp đổ.",
        "• Độc chất KCN thuộc danh mục hóa chất",
        "  công nghiệp xi mạ hoặc dược phẩm thí nghiệm."
    ]
    for i, line in enumerate(notes):
        draw.text((475, 285 + i * 20), line, fill=(50, 50, 50), font=f_sub)
        
    # Bottom Conclusion
    draw.rectangle([40, 415, 760, 565], fill=(255, 252, 245), outline=(180, 190, 200))
    draw.text((55, 425), "KẾT LUẬN ĐỘC CHẤT PHÁP Y:", fill=(160, 20, 20), font=f_bold)
    draw.text((55, 450), "Xác nhận chất độc Kali Xyanua (KCN) tinh khiết cao. Hành vi chuẩn bị và đưa kẹo độc vào siêu thị", fill=(40, 40, 40), font=f_sub)
    draw.text((55, 472), "được thực hiện bởi nhóm tội phạm có kiến thức sâu về hóa thực phẩm và tâm lý học đám đông.", fill=(40, 40, 40), font=f_sub)
    draw.text((55, 495), "Vật chứng d03 liên kết trực tiếp với thư tống tiền máy đánh chữ d05 cấu thành tội danh Khủng bố kinh tế.", fill=(20, 40, 90), font=f_mono)
    
    # Red Japanese circular seal
    draw.ellipse([640, 450, 730, 540], outline=(200, 40, 40), width=3)
    draw.text((655, 475), "大阪府警", fill=(200, 40, 40), font=f_bold)
    draw.text((660, 495), "科捜研", fill=(200, 40, 40), font=f_mono)
    
    save_webp(img, "d03-giam-dinh-doc-chat.webp")

# 4. d04-ban-do-rai-keo.webp (800x600) - Kansai & Tokyo Poison Candy Map
def render_d04():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (22, 38, 58)) # Blue map slate
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Grid
    for x in range(30, w - 30, 30):
        draw.line([(x, 30), (x, h - 30)], fill=(32, 52, 78), width=1)
    for y in range(30, h - 30, 30):
        draw.line([(30, y), (w - 30, y)], fill=(32, 52, 78), width=1)
        
    draw.rectangle([30, 30, w - 30, h - 30], outline=(80, 150, 210), width=2)
    
    draw.text((50, 45), "SƠ ĐỒ TRINH SÁT: CÁC ĐỊA ĐIỂM RẢI KẸO ĐỘC VÙNG KANSAI & TOKYO (1984)", fill=(255, 255, 255), font=f_title)
    draw.text((50, 70), "Ban Chuyên án Cục Cảnh sát Quốc gia Nhật Bản - Tọa độ 21 siêu thị và ga tàu bị đầu độc", fill=(140, 190, 230), font=f_sub)
    
    # Map nodes: Kansai cluster (Osaka, Kobe, Kyoto) and Tokyo
    # Node 1: Osaka (Center of attacks)
    draw.ellipse([210, 250, 330, 370], outline=(255, 80, 80), width=2)
    draw.ellipse([255, 295, 285, 325], fill=(255, 50, 50))
    draw.text((270, 270), "OSAKA (TÂM ĐIỂM)", fill=(255, 220, 80), font=f_bold, anchor="mm")
    draw.text((270, 335), "• Siêu thị Daiei (kẹo Glico)", fill=(255, 200, 200), font=f_mono, anchor="mm")
    draw.text((270, 350), "• Trụ sở tập đoàn Ezaki Glico", fill=(200, 220, 240), font=f_mono, anchor="mm")
    
    # Node 2: Kobe
    draw.ellipse([110, 220, 150, 260], fill=(255, 100, 100))
    draw.text((130, 205), "KOBE", fill=(255, 220, 90), font=f_bold, anchor="mm")
    draw.text((130, 275), "Nhà máy bao bì PUR-82", fill=(180, 210, 240), font=f_mono, anchor="mm")
    
    # Node 3: Kyoto
    draw.ellipse([340, 160, 380, 200], fill=(255, 100, 100))
    draw.text((360, 145), "KYOTO", fill=(255, 220, 90), font=f_bold, anchor="mm")
    draw.text((360, 215), "Ga Kyoto (Người mắt cáo)", fill=(255, 150, 150), font=f_mono, anchor="mm")
    
    # Shinkansen Railway Line connecting Kansai to Tokyo
    draw.line([(130, 240), (270, 310), (360, 180), (620, 200)], fill=(255, 220, 80), width=3)
    draw.text((480, 175), "◄ TUYẾN TÀU CAO TỐC SHINKANSEN (GIAO TIỀN CHUỘC) ►", fill=(255, 220, 90), font=f_bold, anchor="mm")
    
    # Node 4: Tokyo
    draw.ellipse([590, 170, 650, 230], outline=(255, 80, 80), width=2)
    draw.ellipse([610, 190, 630, 210], fill=(255, 50, 50))
    draw.text((620, 150), "TOKYO (THỦ ĐÔ)", fill=(255, 220, 80), font=f_bold, anchor="mm")
    draw.text((620, 245), "• Siêu thị Seiyu (Kẹo Morinaga)", fill=(255, 200, 200), font=f_mono, anchor="mm")
    draw.text((620, 262), "• Sàn giao dịch chứng khoán TSE", fill=(200, 230, 255), font=f_mono, anchor="mm")
    
    # Legend box bottom
    draw.rectangle([50, 440, 750, 550], fill=(26, 48, 75), outline=(100, 170, 230))
    draw.text((65, 452), "CHÚ DẪN CHIẾN THUẬT RẢI ĐỘC CỦA QUÁI VẬT 21 KHUÔN MẶT:", fill=(255, 220, 80), font=f_bold)
    draw.text((65, 475), "• Điểm chấm đỏ: Các siêu thị tiện lợi nơi kẹo tẩm xyanua dán nhãn cảnh báo được lén đặt lên kệ.", fill=(220, 235, 250), font=f_mono)
    draw.text((65, 498), "• Tuyến vàng nối: Hành trình di chuyển bằng tàu hỏa của nghi phạm 'Người đàn ông mắt cáo' trong các phi vụ tống tiền.", fill=(220, 235, 250), font=f_mono)
    draw.text((65, 520), "• Tầm ảnh hưởng: Gây thiệt hại 7 tỷ Yên cho ngành bánh kẹo Nhật Bản và làm náo loạn toàn bộ thị trường chứng khoán.", fill=(255, 180, 180), font=f_mono)
    
    save_webp(img, "d04-ban-do-rai-keo.webp")

# 5. d10-giam-dinh-may-chu.webp (800x600) - Panwriter Typewriter Chipped 'ka' Key Examination
def render_d10():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (240, 242, 245))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    # Header
    draw.rectangle([25, 25, w - 25, 80], fill=(35, 45, 58))
    draw.text((40, 34), "VIỆN NGHIÊN CỨU KHOA HỌC HÌNH SỰ QUỐC GIA NHẬT BẢN (NRIPS)", fill=(200, 215, 230), font=f_sub)
    draw.text((40, 54), "BÁO CÁO GIÁM ĐỊNH KỸ THUẬT: MÁY ĐÁNH CHỮ CƠ HIỆU PANWRITER / BROTHER", fill=(255, 255, 255), font=f_title)
    
    # Left: Photomicrograph of Chipped 'ka' (か) Character
    draw.rectangle([40, 95, 440, 410], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((50, 105), "ẢNH VI THỂ KÝ TỰ HIRAGANA 'か' (KA) BỊ MÒN SỨT", fill=(30, 40, 50), font=f_bold)
    
    # Stylized drawing of chipped 'ka' character under microscope
    draw.rectangle([110, 150, 370, 340], fill=(245, 245, 240), outline=(120, 130, 140))
    # Character 'ka' with chipped top-left stroke
    draw.line([(170, 180), (310, 180)], fill=(30, 30, 30), width=12) # Top stroke
    draw.line([(220, 175), (200, 310)], fill=(30, 30, 30), width=10) # Main vertical curve
    draw.line([(270, 200), (270, 290)], fill=(30, 30, 30), width=8)  # Right stroke
    # Red circle highlighting chipped corner
    draw.ellipse([150, 165, 190, 205], outline=(220, 20, 20), width=3)
    draw.line([(185, 195), (280, 240)], fill=(220, 20, 20), width=2)
    draw.text((210, 250), "◄ VẾT SỨT MÒN CƠ HỌC 0.3mm", fill=(200, 20, 20), font=f_bold)
    draw.text((210, 270), "Góc trái nét phẩy bị khuyết", fill=(140, 20, 20), font=f_mono)
    draw.text((210, 288), "Trùng khớp 100% qua 14 bức thư", fill=(140, 20, 20), font=f_mono)
    
    draw.text((50, 360), "Kính hiển vi so sánh Leica DMR: Phóng đại 50x", fill=(80, 80, 80), font=f_sub)
    draw.text((50, 380), "Dấu vết độc bản khẳng định mọi bức thư đều từ CÙNG MỘT MÁY ĐÁNH CHỮ.", fill=(160, 20, 20), font=f_bold)
    
    # Right Box: Ribbon & Machine Model Analysis
    draw.rectangle([460, 95, 760, 410], fill=(255, 255, 255), outline=(180, 190, 200))
    draw.text((475, 105), "ĐẶC TRƯNG MÁY ĐÁNH CHỮ", fill=(30, 40, 50), font=f_bold)
    
    specs = [
        "• Dòng máy: Máy đánh chữ cơ Panwriter",
        "  hoặc Brother Model 210 sản xuất 1980.",
        "• Ruy-băng mực: Vải nilon đen 13mm,",
        "  mép trên bị tưa xơ sợi sau ~50 trang.",
        "• Lực gõ phím: Không đều, phím số 2 và",
        "  chữ 'Mon' lún sâu hơn bình thường.",
        "• Giấy sử dụng: Giấy in thương mại A4",
        "  thương hiệu Maruman phổ biến tại Kansai.",
        "• Khoanh vùng điều tra: Truy quét hơn",
        "  12.000 máy đánh chữ tại Osaka và Kobe."
    ]
    for i, line in enumerate(specs):
        draw.text((475, 140 + i * 26), line, fill=(40, 40, 40), font=f_sub)
        
    # Bottom Summary
    draw.rectangle([40, 425, 760, 565], fill=(255, 250, 240), outline=(200, 170, 120))
    draw.text((55, 435), "KẾT LUẬN GIÁM ĐỊNH KỸ THUẬT CƠ HỌC:", fill=(160, 30, 20), font=f_bold)
    draw.text((55, 460), "1. Vết sứt cơ học trên ký tự 'ka' là vật chứng độc bản bất biến xuyên suốt từ Bức thư số 1 đến số 14.", fill=(30, 30, 30), font=f_bold)
    draw.text((55, 485), "2. Cùng với ảnh mép keo nhiệt d11, đây là cặp bằng chứng khoa học vạch trần công cụ gây án của Quái vật.", fill=(40, 40, 90), font=f_sub)
    
    save_webp(img, "d10-giam-dinh-may-chu.webp")

# 6. d13-quang-pho-am-thanh.webp (800x600) - Voice Spectrogram of Child Cassette
def render_d13():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (18, 28, 42)) # Dark acoustic navy
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 18)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    draw.rectangle([25, 25, w - 25, h - 25], outline=(80, 140, 200), width=2)
    draw.text((45, 40), "PHÂN TÍCH QUANG PHỔ TẦN SỐ ÂM THANH (AUDIO SONOGRAM ANALYSIS)", fill=(255, 255, 255), font=f_title)
    draw.text((45, 65), "Băng cassette TDK C-60 thu giữ tại bốt điện thoại ga Kyoto - Giọng đọc chỉ dẫn địa điểm giao tiền", fill=(140, 190, 230), font=f_sub)
    
    # Sonogram Spectrogram Window
    draw.rectangle([45, 95, 755, 340], fill=(12, 18, 28), outline=(100, 160, 220))
    
    # Frequency grid (0 to 8 kHz)
    for y in range(120, 330, 30):
        draw.line([(85, y), (745, y)], fill=(25, 40, 60), width=1)
        freq = (330 - y) * 35
        draw.text((50, y - 6), f"{freq}Hz", fill=(100, 140, 180), font=f_mono)
        
    # Simulated Voice Formants (Child's high-pitch voice 300Hz-3500Hz)
    random.seed(101)
    for bx in range(90, 740, 8):
        h_bar = random.randint(30, 140)
        c_val = random.randint(160, 255)
        draw.rectangle([bx, 280 - h_bar, bx + 5, 280], fill=(c_val, random.randint(80, 200), 50))
        
    draw.text((95, 105), "◄ ĐOẠN GHI ÂM: 'Hãy lên chuyến tàu đêm... nhìn ra phía cửa sổ bên phải có gắn cờ trắng...'", fill=(255, 220, 80), font=f_bold)
    draw.text((95, 315), "Tần số cơ bản F0: 295 Hz (Đặc trưng giọng bé gái khoảng 9-11 tuổi đọc từng từ chậm rãi theo kịch bản)", fill=(255, 180, 180), font=f_mono)
    
    # Lower Analysis Box
    draw.rectangle([45, 360, 755, 550], fill=(24, 40, 65), outline=(100, 160, 220))
    draw.text((60, 375), "KẾT LUẬN CỦA CHUYÊN GIA GIỌNG NÓI HÌNH SỰ:", fill=(255, 220, 80), font=f_bold)
    
    findings = [
        "1. Kẻ thủ ác cố ý sử dụng giọng phụ nữ và trẻ em để vô hiệu hóa máy phân tích âm học của cảnh sát.",
        "2. Âm nền (background noise) ghi nhận tiếng quạt gió công nghiệp và tiếng còi tàu điện tuyến Keihan.",
        "3. Đứa trẻ đọc với ngữ điệu gượng gạo, ngắt nghỉ từng nhịp, chứng minh đang bị ép đọc theo giấy viết sẵn.",
        "4. Băng cassette nhãn hiệu TDK loại D60 sản xuất tại nhà máy Shizuoka, mã lô phân phối riêng vùng Kinki."
    ]
    for i, line in enumerate(findings):
        draw.text((60, 405 + i * 28), line, fill=(220, 235, 250), font=f_sub)
        
    save_webp(img, "d13-quang-pho-am-thanh.webp")

# 7. d14-phuc-kich-shinkansen.webp (800x600) - Hikari Train Ambush & Kyoto Station CCTV
def render_d14():
    w, h = 800, 600
    img = Image.new('RGB', (w, h), (30, 35, 42)) # Surveillance monitor grey
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 17)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 11)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    draw.rectangle([20, 20, w - 20, h - 20], outline=(80, 95, 110), width=2)
    draw.text((40, 35), "CỤC CẢNH SÁT QUỐC GIA - BÁO CÁO PHỤC KÍCH: TÀU SHINKANSEN HIKARI & GA KYOTO", fill=(255, 220, 90), font=f_title)
    draw.text((40, 58), "Chuyến tàu đêm giao tiền chuộc 100 triệu Yên ngày 28/06/1984 - Kế hoạch bắt quả tang bị lộ", fill=(180, 200, 220), font=f_sub)
    
    # Left: Shinkansen Train Car Layout
    draw.rectangle([40, 85, 450, 420], fill=(22, 26, 32), outline=(100, 115, 130))
    draw.text((50, 95), "SƠ ĐỒ TOA SỐ 7 TÀU SHINKANSEN HIKARI", fill=(255, 255, 255), font=f_bold)
    
    # Train car rectangle
    draw.rectangle([60, 130, 430, 260], fill=(45, 52, 60), outline=(160, 175, 190), width=2)
    draw.text((245, 145), "HÀNG GHẾ HÀNH KHÁCH (TOA 7)", fill=(200, 215, 230), font=f_mono, anchor="mm")
    
    # Seat rows
    for sx in range(80, 420, 45):
        draw.rectangle([sx, 170, sx + 30, 200], fill=(80, 95, 110))
        draw.rectangle([sx, 210, sx + 30, 240], fill=(80, 95, 110))
        
    # Suspect Seat (Seat 14B)
    draw.rectangle([215, 170, 245, 200], fill=(220, 50, 50))
    draw.text((230, 185), "14B", fill=(255, 255, 255), font=f_bold, anchor="mm")
    draw.text((230, 275), "◄ VỊ TRÍ NGƯỜI ĐÀN ÔNG MẮT CÁO", fill=(255, 100, 100), font=f_bold, anchor="mm")
    draw.text((230, 295), "Đội mũ len xám, đeo kính mắt, ánh nhìn sắc lạnh", fill=(220, 220, 220), font=f_mono, anchor="mm")
    draw.text((230, 312), "Ngồi quan sát điều tra viên giả dạng nhân viên Glico", fill=(220, 220, 220), font=f_mono, anchor="mm")
    
    draw.text((50, 345), "DIỄN BIẾN: Khi tàu dừng 2 phút tại ga Kyoto, đối tượng", fill=(255, 220, 80), font=f_sub)
    draw.text((50, 365), "nhanh chóng lẩn vào dòng người trên sân ga đông đúc.", fill=(255, 220, 80), font=f_sub)
    draw.text((50, 385), "Trinh sát bám theo nhưng mất dấu do rào cản phân cấp chỉ huy.", fill=(255, 150, 150), font=f_mono)
    
    # Right: CCTV Camera Frame at Kyoto Station Exit
    draw.rectangle([465, 85, 760, 420], fill=(15, 18, 22), outline=(100, 115, 130))
    draw.text((480, 95), "CAMERA AN NINH LỐI RA GA KYOTO", fill=(0, 255, 120), font=f_mono)
    draw.text((660, 95), "REC 21:48", fill=(255, 50, 50), font=f_mono)
    
    # Silhouette with trench coat and beanie
    draw.ellipse([580, 140, 640, 200], fill=(200, 180, 160)) # Head
    draw.rectangle([570, 130, 650, 160], fill=(80, 85, 90))   # Beanie hat
    draw.polygon([(560, 200), (660, 200), (680, 340), (540, 340)], fill=(90, 80, 70)) # Trench coat
    draw.text((540, 355), "[NHÂN DẠNG MẮT CÁO]", fill=(255, 220, 80), font=f_bold)
    draw.text((540, 375), "Cao ~1m75, khoảng 35-45 tuổi", fill=(200, 210, 220), font=f_mono)
    draw.text((540, 395), "Mắt một mí hẹp dài hình thoi", fill=(255, 180, 180), font=f_mono)
    
    # Bottom Note
    draw.rectangle([40, 435, 760, 565], fill=(20, 24, 30), outline=(80, 100, 120))
    draw.text((55, 448), "TỔNG KẾT CHIẾN DỊCH PHỤC KÍCH: Cơ hội bắt giữ duy nhất kẻ cầm đầu đã bị tuột mất do sự do dự", fill=(255, 220, 90), font=f_bold)
    draw.text((55, 470), "của lãnh đạo cảnh sát tỉnh Shiga (dẫn tới bi kịch tự sát của Cảnh sát trưởng Yamamoto sau này).", fill=(255, 150, 150), font=f_sub)
    draw.text((55, 492), "Cặp tài liệu d14 và d15 chứng minh tội ác vừa mang tính thao túng cổ phiếu vừa có mạng lưới trinh sát ngầm tinh vi.", fill=(200, 220, 240), font=f_mono)
    
    save_webp(img, "d14-phuc-kich-shinkansen.webp")

# 8. d18-thu-dinh-chien.webp (700x520) - Final Truce Letter from Monster with 21 Faces
def render_d18():
    w, h = 700, 520
    img = Image.new('RGB', (w, h), (245, 243, 235))
    draw = ImageDraw.Draw(img)
    
    f_title = get_font(FONT_HELVETICA, 16)
    f_sub = get_font(FONT_HELVETICA, 12)
    f_mono = get_font(FONT_COURIER, 12)
    f_bold = get_font(FONT_HELVETICA, 13)
    
    draw.rectangle([40, 35, w - 40, h - 35], fill=(255, 255, 252), outline=(180, 170, 150), width=1)
    
    # Machine Typewritten Text (Bức thư đình chiến ngày 12/08/1985)
    draw.text((65, 55), "THƯ GỬI TOÀN THỂ TRUYỀN THÔNG & CẢNH SÁT NHẬT BẢN", fill=(30, 40, 50), font=f_bold)
    draw.text((65, 75), "Ngày 12 tháng 08 năm 1985 (Chiến dịch kết thúc)", fill=(120, 120, 120), font=f_mono)
    draw.line([(65, 95), (w - 65, 95)], fill=(200, 190, 180), width=1)
    
    letter_lines = [
        "Cảnh sát trưởng Yamamoto tỉnh Shiga đã tự thiêu vì không bắt được chúng tao.",
        "Thật là một người đàn ông đáng kính. Chúng tao gửi lời chia buồn chân thành.",
        "Chuyện trêu chọc các công ty bánh kẹo đến đây là hết.",
        "",
        "Nếu chúng tao tiếp tục tống tiền các công ty thực phẩm,",
        "chúng tao sẽ trở thành những kẻ ác đê hèn thực sự.",
        "Chúng tao là kẻ xấu, nhưng chúng tao có quy tắc của chúng tao.",
        "Từ nay trở đi, bánh kẹo tại các siêu thị sẽ an toàn.",
        "",
        "Nước Nhật có thể thở phào nhẹ nhõm rồi đấy.",
        "Chúng tao đi đây. Chúc cảnh sát may mắn lần sau!",
        "",
        "Ký tên:",
        "QUÁI VẬT 21 KHUÔN MẶT (かいじん21ぱんそう)"
    ]
    
    y = 110
    for line in letter_lines:
        color = (180, 20, 20) if "Yamamoto" in line or "QUÁI VẬT" in line else (40, 40, 40)
        draw.text((65, y), line, fill=color, font=f_mono)
        y += 24
        
    # Monster stamp / Emblem
    draw.rectangle([450, 360, w - 65, 460], fill=(255, 240, 240), outline=(200, 30, 30), width=2)
    draw.text((465, 375), "BỨC THƯ ĐÌNH CHIẾN", fill=(180, 20, 20), font=f_bold)
    draw.text((465, 400), "Dấu chấm hết cho 17 tháng", fill=(50, 50, 50), font=f_mono)
    draw.text((465, 420), "khủng hoảng Glico Morinaga", fill=(50, 50, 50), font=f_mono)
    draw.text((465, 438), "Kỳ án không lời giải thế kỷ 20", fill=(120, 20, 20), font=f_bold)
    
    save_webp(img, "d18-thu-dinh-chien.webp")

if __name__ == "__main__":
    optimize_existing()
    fix_d09_sketch()
    render_d03()
    render_d04()
    render_d10()
    render_d13()
    render_d14()
    render_d18()
    print("Optimization and rendering for Case 16 completed successfully.")
