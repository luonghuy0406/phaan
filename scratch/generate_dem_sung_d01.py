import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1050
# Aged 1999 newsprint paper background (yellowed cream with newsprint texture)
img = Image.new("RGB", (W, H), "#efe8d3")
draw = ImageDraw.Draw(img)

# Newsprint paper texture (subtle grain and fibers)
for y in range(0, H, 2):
    t = random.randint(-4, 4)
    draw.line([(0, y), (W, y)], fill=(239 + t, 232 + t, 211 + t))

# Paper border & margins
draw.rectangle([40, 40, W - 40, H - 40], outline="#4a3e2d", width=2)
draw.rectangle([44, 44, W - 44, H - 44], outline="#827159", width=1)

# Fonts
font_masthead = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 52)
font_submast = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
font_meta = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_head_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 34)
font_head_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
font_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman.ttf", 16)
font_body_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman.ttf", 17)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)

# 1. Masthead: BÁO AN NINH THỦ ĐÔ
draw.text((60, 55), "CÔNG AN THÀNH PHỐ HÀ NỘI", fill="#5a4933", font=font_submast)
draw.text((W // 2, 85), "AN NINH THỦ ĐÔ", fill="#8b1c14", font=font_masthead, anchor="mm")
draw.text((W // 2, 125), "TIẾNG NÓI CỦA LỰC LƯỢNG VŨ TRANG VÀ NHÂN DÂN THỦ ĐÔ HÀ NỘI", fill="#2b2116", font=font_submast, anchor="mm")

# Metadata Bar
draw.line([(60, 145), (W - 60, 145)], fill="#2b2116", width=3)
draw.text((65, 155), "XUẤT BẢN HÀNG NGÀY • SỐ 1248", fill="#2b2116", font=font_meta)
draw.text((W // 2, 155), "THỨ HAI, NGÀY 19 THÁNG 7 NĂM 1999", fill="#2b2116", font=font_meta, anchor="mt")
draw.text((W - 65, 155), "GIÁ: 1.500 ĐỒNG", fill="#2b2116", font=font_meta, anchor="rt")
draw.line([(60, 180), (W - 60, 180)], fill="#2b2116", width=2)

# 2. Main Headline
headline = "TRỌNG ÁN: NỔ SÚNG CƯỚP TIỆM VÀNG TRÊN PHỐ TÂY SƠN TRONG ĐÊM MƯA BÃO"
draw.text((W // 2, 215), headline, fill="#8b1c14", font=font_head_main, anchor="mm")
subhead = "Kẻ cướp dùng súng ngắn quân dụng K54 bắn bị thương chủ tiệm, cướp đi hơn 100 lượng vàng ta rồi tẩu thoát"
draw.text((W // 2, 250), subhead, fill="#1f1810", font=font_head_sub, anchor="mm")
draw.line([(W // 2 - 300, 275), (W // 2 + 300, 275)], fill="#8b1c14", width=2)

# 3. Two-Column Layout: Left Side = Gritty B&W Documentary Photo; Right Side = Article text columns
content_top = 295

# 3.1 Crime Scene Documentary Photo (Left Side)
px, py = 70, content_top
pw, ph = 680, 520
# Photo background (gritty 1999 monochrome dark room print)
draw.rectangle([px, py, px + pw, py + ph], fill="#26282b", outline="#111214", width=3)

# Inside Photo: Phố Tây Sơn tiệm vàng Kim Sinh in night rain
# Rainy street & store front
draw.rectangle([px + 10, py + 10, px + pw - 10, py + ph - 60], fill="#3a3d42")

# Store awning & sign
draw.rectangle([px + 50, py + 40, px + pw - 50, py + 110], fill="#1e2024")
draw.rectangle([px + 70, py + 55, px + pw - 70, py + 95], fill="#111214", outline="#727780")
draw.text((px + pw // 2, py + 75), "TIỆM VÀNG KIM SINH - 38 TÂY SƠN", fill="#dcdfe6", font=font_submast, anchor="mm")

# Shattered glass window display
draw.rectangle([px + 100, py + 130, px + pw - 100, py + 320], fill="#222429", outline="#5b606b", width=2)
# Spiderweb crack lines
for _ in range(12):
    cx, cy = px + pw // 2, py + 225
    ang = random.uniform(0, 2 * 3.14159)
    dist = random.uniform(50, 160)
    draw.line([(cx, cy), (cx + dist * 0.9, cy + dist * 0.7)], fill="#a1a7b3", width=2)

# Police tape diagonally across store
draw.line([(px + 40, py + 340), (px + pw - 40, py + 260)], fill="#dcd78c", width=12)
draw.text((px + pw // 2, py + 295), "DÂY PHONG TỎA BẢO VỆ HIỆN TRƯỜNG - CÔNG AN QUẬN ĐỐNG ĐA", fill="#1f1810", font=font_small, anchor="mm")

# UAZ Police Jeep silhouette parked in rain
draw.rectangle([px + 80, py + 360, px + 280, py + 430], fill="#1c1e22")
draw.circle((px + 130, py + 430), 22, fill="#111214")
draw.circle((px + 230, py + 430), 22, fill="#111214")

# Rain streaks
for _ in range(250):
    rx = random.randint(px + 10, px + pw - 10)
    ry = random.randint(py + 10, py + ph - 70)
    draw.line([(rx, ry), (rx - 4, ry + 16)], fill="#69707d", width=1)

# Photo Caption
draw.rectangle([px, py + ph - 55, px + pw, py + ph], fill="#1e2024")
draw.text((px + pw // 2, py + ph - 28), "Ảnh tư liệu phóng viên Báo ANTĐ: Hiện trường tiệm vàng Kim Sinh số 38 phố Tây Sơn\nbị kẻ cướp nổ súng tàn phá, lực lượng chức năng phong tỏa thu thập dấu vết lúc rạng sáng 19-7", fill="#cfd5e0", font=font_small, anchor="mm")


# 3.2 Newspaper Text Columns (Right Side: 2 sub-columns)
col1_x = 790
col2_x = 1190
col_w = 370

paras_col1 = [
    ("HỒI 23H00 ĐÊM QUA 18-7,", "trong lúc ngoài trời đang đổ mưa giông rất lớn, tại tiệm vàng Kim Sinh (số 38 phố Tây Sơn, phường Quang Trung, quận Đống Đa) đã xảy ra một vụ cướp tài sản có vũ trang đặc biệt nghiêm trọng."),
    ("Theo các nhân chứng có mặt tại khu vực ngõ chùa Đồng Quang,", "một đối tượng nam giới trùm kín áo mưa, đeo găng tay len đã bất ngờ xông vào gian trưng bày tiệm vàng. Y rút súng ngắn quân dụng K54 khống chế, sau đó thẳng tay nổ súng bắn trọng thương người bảo vệ và đập vỡ toàn bộ tủ kính quầy vàng."),
    ("Trước sự kháng cự của gia đình chủ tiệm,", "tên cướp hung hãn đã nổ tiếp 2 phát đạn găm vào cột gỗ và vách tường, sau đó vơ vét hàng trăm lượng vàng miếng 9999 cho vào bao tải rồi nhanh chóng tháo chạy theo lối ngõ ngách phía sau.")
]

paras_col2 = [
    ("NGAY TRONG ĐÊM,", "Đại tá Thủ trưởng Cơ quan CSĐT Công an TP Hà Nội cùng các lực lượng tinh nhuệ của Phòng CSHS (PC14) và Phòng Kỹ thuật hình sự (PC21) đã có mặt trực tiếp chỉ đạo phong tỏa hiện trường."),
    ("Khám nghiệm sơ bộ,", "cơ quan điều tra đã thu giữ được 3 vỏ đạn bằng đồng của súng ngắn quân dụng K54 dập năm sản xuất 1968 cùng một đầu đạn chì biến dạng găm trong khung bao lam gỗ."),
    ("Tại lối ngõ sau thông ra đường Đặng Tiến Đông,", "công an phát hiện một số dấu vết nghi vấn gồm vỏ bao thuốc lá Du Lịch màu xanh dẫm nát dưới bùn. Toàn bộ các bến phà, cửa ngõ ra vào Thủ đô sang phía Gia Lâm, Bắc Ninh đã được lệnh chốt chặn nghiêm ngặt.")
]

y_cur = content_top
for lead, body in paras_col1:
    draw.text((col1_x, y_cur), lead, fill="#8b1c14", font=font_body_bold)
    y_cur += 24
    # Word wrap body
    words = body.split()
    line = ""
    for w in words:
        test = line + " " + w if line else w
        if draw.textlength(test, font=font_body) < col_w:
            line = test
        else:
            draw.text((col1_x, y_cur), line, fill="#1f1810", font=font_body)
            y_cur += 22
            line = w
    if line:
        draw.text((col1_x, y_cur), line, fill="#1f1810", font=font_body)
        y_cur += 30

y_cur = content_top
for lead, body in paras_col2:
    draw.text((col2_x, y_cur), lead, fill="#8b1c14", font=font_body_bold)
    y_cur += 24
    words = body.split()
    line = ""
    for w in words:
        test = line + " " + w if line else w
        if draw.textlength(test, font=font_body) < col_w:
            line = test
        else:
            draw.text((col2_x, y_cur), line, fill="#1f1810", font=font_body)
            y_cur += 22
            line = w
    if line:
        draw.text((col2_x, y_cur), line, fill="#1f1810", font=font_body)
        y_cur += 30


# 4. Bottom Urgent Police Bulletin Banner
draw.line([(60, H - 180), (W - 60, H - 180)], fill="#2b2116", width=2)
draw.rectangle([60, H - 170, W - 60, H - 70], fill="#e5dcbf", outline="#8b1c14", width=2)

draw.text((80, H - 150), "THÔNG BÁO KHẨN CỦA CÔNG AN THÀNH PHỐ HÀ NỘI TRUY TÌM TUNG TÍCH HUNG THỦ:", fill="#8b1c14", font=font_head_sub)
draw.text((80, H - 120), "• Đặc điểm nhận dạng: Nam giới cao khoảng 1m68 - 1m72, đậm người, trên mặt có vết sẹo ngang đuôi mắt phải, đi xe máy Simson hoặc Minsk.", fill="#1f1810", font=font_body)
draw.text((80, H - 95), "• Tang vật truy tìm: Khoảng 100 lượng vàng ta dạng nhẫn tròn và vàng lá, hung khí là súng K54 có ống giảm thanh tự chế. Ai phát hiện báo ngay Đội Điều tra Trọng án.", fill="#1f1810", font=font_body)

# Red official archive stamp on top right of page
stamp_x, stamp_y = W - 160, 230
draw.circle((stamp_x, stamp_y), 45, outline="#8b1c14", width=3)
draw.circle((stamp_x, stamp_y), 40, outline="#8b1c14", width=1)
draw.text((stamp_x, stamp_y - 18), "CÔNG AN HÀ NỘI", fill="#8b1c14", font=font_small, anchor="mm")
draw.text((stamp_x, stamp_y), "LƯU TRỮ", fill="#8b1c14", font=font_body_bold, anchor="mm")
draw.text((stamp_x, stamp_y + 18), "HỒ SƠ ÁN", fill="#8b1c14", font=font_small, anchor="mm")

# Save as WebP
out_path = "public/cases/dem-sung-no-tay-son/images/d01-bao-chi.webp"
img.save(out_path, "WEBP", quality=88)
print(f"Generated {out_path} successfully!")
