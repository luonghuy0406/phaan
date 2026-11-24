import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1050
# Vintage 2004 newsprint paper background (warm yellowed newsprint)
img = Image.new("RGB", (W, H), "#eee6d1")
draw = ImageDraw.Draw(img)

# Newsprint paper texture
for y in range(0, H, 2):
    t = random.randint(-4, 4)
    draw.line([(0, y), (W, y)], fill=(238 + t, 230 + t, 209 + t))

# Border
draw.rectangle([40, 40, W - 40, H - 40], outline="#473a27", width=2)
draw.rectangle([44, 44, W - 44, H - 44], outline="#7d6a4f", width=1)

# Fonts
font_masthead = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 54)
font_submast = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 18)
font_meta = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 15)
font_head_main = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 34)
font_head_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
font_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman.ttf", 16)
font_body_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman.ttf", 17)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13)

# 1. Masthead: BÁO HÀ TÂY
draw.text((60, 55), "TỈNH ỦY - HĐND - UBND TỈNH HÀ TÂY", fill="#5a4933", font=font_submast)
draw.text((W // 2, 85), "BÁO HÀ TÂY", fill="#8b1c14", font=font_masthead, anchor="mm")
draw.text((W // 2, 125), "TIẾNG NÓI CỦA ĐẢNG BỘ, CHÍNH QUYỀN VÀ NHÂN DÂN TỈNH HÀ TÂY", fill="#2b2116", font=font_submast, anchor="mm")

# Metadata Bar
draw.line([(60, 145), (W - 60, 145)], fill="#2b2116", width=3)
draw.text((65, 155), "XUẤT BẢN HÀNG NGÀY • SỐ 862", fill="#2b2116", font=font_meta)
draw.text((W // 2, 155), "THỨ SÁU, NGÀY 02 THÁNG 4 NĂM 2004", fill="#2b2116", font=font_meta, anchor="mt")
draw.text((W - 65, 155), "GIÁ: 1.200 ĐỒNG", fill="#2b2116", font=font_meta, anchor="rt")
draw.line([(60, 180), (W - 60, 180)], fill="#2b2116", width=2)

# 2. Headline
headline = "ÁN MẠNG BẤT THƯỜNG TRÊN ĐỈNH NÚI SÀI SƠN: SƯ TRỤ TRÌ TỊNH THẤT BỊ SÁT HẠI"
draw.text((W // 2, 215), headline, fill="#8b1c14", font=font_head_main, anchor="mm")
subhead = "Tiếng chuông trưa ngân vang lúc 11h45 và bức màn bí mật cơ học tại gác chuông chùa Cổ Sơn"
draw.text((W // 2, 250), subhead, fill="#1f1810", font=font_head_sub, anchor="mm")
draw.line([(W // 2 - 320, 275), (W // 2 + 320, 275)], fill="#8b1c14", width=2)

# 3. Two-Column Layout: Left = Documentary Photo of Sai Son Mountain Pagoda; Right = Article Text
content_top = 295
px, py = 70, content_top
pw, ph = 680, 520

# Photo Frame
draw.rectangle([px, py, px + pw, py + ph], fill="#26282b", outline="#111214", width=3)
# Scenery: Sai Son limestone mountain & Ancient Pagoda Bell Tower in midday mist
draw.rectangle([px + 10, py + 10, px + pw - 10, py + ph - 60], fill="#353b3e")

# Mountains in background
mtn1 = [(px + 40, py + 300), (px + 240, py + 120), (px + 440, py + 300)]
mtn2 = [(px + 320, py + 320), (px + 520, py + 160), (px + pw - 30, py + 320)]
draw.polygon(mtn1, fill="#1e2427")
draw.polygon(mtn2, fill="#283034")

# Misty fog layers
for y_fog in range(py + 180, py + 300, 15):
    draw.line([(px + 10, y_fog), (px + pw - 10, y_fog)], fill="#49555c", width=4)

# Ancient Pagoda Bell Tower (Gác chuông chùa Thầy)
bx, by = px + 220, py + 220
bw, bh = 240, 180
# Two tier curved curved roofs
draw.polygon([(bx - 30, by + 40), (bx + bw // 2, by - 20), (bx + bw + 30, by + 40)], fill="#1a1c1d")
draw.polygon([(bx - 50, by + 110), (bx + bw // 2, by + 50), (bx + bw + 50, by + 110)], fill="#1a1c1d")
# Columns
for cx_col in [bx + 20, bx + 70, bx + bw - 70, bx + bw - 20]:
    draw.line([(cx_col, by + 40), (cx_col, by + bh)], fill="#0f1112", width=6)
# Big bronze bell hanging silhouette
draw.ellipse([bx + bw // 2 - 25, by + 65, bx + bw // 2 + 25, by + 125], fill="#0a0b0c")

# Stone stairs going up
for i in range(12):
    sy = by + bh + i * 5
    draw.line([(px + 160 + i * 15, sy), (px + 380 - i * 15, sy)], fill="#5c6266", width=3)

# Police caution tape at base
draw.line([(px + 40, py + 410), (px + pw - 40, py + 430)], fill="#dcd78c", width=8)

# Photo Caption
draw.rectangle([px, py + ph - 55, px + pw, py + ph], fill="#1e2024")
draw.text((px + pw // 2, py + ph - 28), "Ảnh tư liệu PV Báo Hà Tây: Toàn cảnh núi Sài Sơn và gác chuông cổ chùa Cổ Sơn\nnơi xảy ra vụ án mạng chấn động chốn thiền môn, lực lượng công an phong tỏa chân núi sáng 2-4", fill="#cfd5e0", font=font_small, anchor="mm")

# 3.2 Newspaper Text Columns (Right Side)
col1_x = 790
col2_x = 1190
col_w = 370

paras_col1 = [
    ("HỒI 13H30 NGÀY 01-04,", "tại chùa Cổ Sơn tọa lạc trên đỉnh núi đá vôi Sài Sơn (huyện Quốc Oai, tỉnh Hà Tây), phật tử và nhà chùa bàng hoàng phát hiện Đại đức Thích Tâm Viên (72 tuổi, trụ trì chùa) đã viên tịch bất thường ngay trong tịnh thất am thiền."),
    ("Khám nghiệm sơ bộ của Phòng Kỹ thuật hình sự Công an tỉnh Hà Tây,", "nạn nhân tử vong do ngạt thở cơ học vì bị siết cổ bằng dây thừng gai sợi thô, thời điểm tử vong được xác định trong khoảng từ 09h30 đến 10h30 sáng."),
    ("Điều kỳ lạ là đúng 11h45 trưa,", "toàn bộ phật tử và người dân dưới chân núi Sài Sơn vẫn nghe thấy tiếng đại hồng chung trên gác chuông ngân vang 3 hồi gián đoạn như thường lệ, tạo ra một bằng chứng ngoại phạm hoàn hảo cho kẻ thủ ác.")
]

paras_col2 = [
    ("ĐIỀU TRA HIỆN TRƯỜNG GÁC CHUÔNG,", "các điều tra viên Đội Trọng án (PC14) đã phát hiện trên sàn gỗ lim dưới vành đại hồng chung có một vũng nước đọng nhỏ giọt còn ẩm ướt và dấu vết xơ dây dù xanh cọ xát trên xà gồ đỡ chuông."),
    ("Bên cạnh đó, pho tượng cổ,", "bảo vật gia truyền bằng đồng dát vàng của nhà chùa đặt tại mật thất tịnh thất cũng đã biến mất không dấu vết."),
    ("Công an tỉnh Hà Tây cùng Công an huyện Quốc Oai", "đang khẩn trương triệu tập các đối tượng liên quan, lấy lời khai của các tăng ni, người làm bếp và phân tích cơ cấu giật chuông cơ học nhằm làm sáng tỏ vụ trọng án thiền môn.")
]

y_cur = content_top
for lead, body in paras_col1:
    draw.text((col1_x, y_cur), lead, fill="#8b1c14", font=font_body_bold)
    y_cur += 24
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

# 4. Bottom Police Bulletin Banner
draw.line([(60, H - 180), (W - 60, H - 180)], fill="#2b2116", width=2)
draw.rectangle([60, H - 170, W - 60, H - 70], fill="#e4dbbe", outline="#8b1c14", width=2)

draw.text((80, H - 150), "THÔNG CÁO BÁO CHÍ CỦA CƠ QUAN CSĐT CÔNG AN TỈNH HÀ TÂY:", fill="#8b1c14", font=font_head_sub)
draw.text((80, H - 120), "• Vụ án có tính chất toan tính tinh vi, kẻ thủ ác lợi dụng cơ cấu cơ học truyền động tự động để ngụy tạo thời gian phát chuông.", fill="#1f1810", font=font_body)
draw.text((80, H - 95), "• Khuyến cáo phật tử và nhân dân cung cấp thông tin về bất kỳ dấu hiệu tàng trữ, tiêu thụ pho tượng Phật cổ dát vàng trong khu vực.", fill="#1f1810", font=font_body)

# Red official archive stamp on top right
stamp_x, stamp_y = W - 160, 230
draw.circle((stamp_x, stamp_y), 45, outline="#8b1c14", width=3)
draw.circle((stamp_x, stamp_y), 40, outline="#8b1c14", width=1)
draw.text((stamp_x, stamp_y - 18), "CÔNG AN HÀ TÂY", fill="#8b1c14", font=font_small, anchor="mm")
draw.text((stamp_x, stamp_y), "LƯU TRỮ", fill="#8b1c14", font=font_body_bold, anchor="mm")
draw.text((stamp_x, stamp_y + 18), "HỒ SƠ ÁN", fill="#8b1c14", font=font_small, anchor="mm")

# Save as WebP
out_path = "public/cases/hoi-chuong-chua-thay/images/d01-bao-chi.webp"
img.save(out_path, "WEBP", quality=88)
print(f"Generated {out_path} successfully!")
