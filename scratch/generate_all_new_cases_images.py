#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/Users/huynguyen/Documents/game_pha_an/public/cases"

cases_images = {
    "tieng-dan-day-pho-hien": [
        ("cover.webp", "TIẾNG ĐÀN ĐÁY PHỐ HIẾN", (30, 25, 20), (210, 160, 90)),
        ("d04-dan-day.webp", "VẬT CHỨNG: ĐÀN ĐÁY VÀ HỘP PHÍM SỪNG", (25, 20, 20), (200, 140, 80)),
        ("d13-khan-lua.webp", "TANG VẬT: KHĂN LỤA VÀ LỌ THẠCH TÍN", (40, 35, 30), (220, 180, 110))
    ],
    "suong-mu-trai-trai": [
        ("cover.webp", "SƯƠNG MÙ TRẠI MÁT", (20, 30, 45), (140, 180, 220)),
        ("d05-hien-truong.webp", "HIỆN TRƯỜNG DỐC THÔNG & VỆT XE RÙA", (35, 25, 20), (190, 130, 100)),
        ("d12-kho-lanh.webp", "KHO LẠNH SỐ 2 & MÁY LÀM ĐÁ VẢY", (20, 35, 50), (130, 200, 230))
    ],
    "chuyen-tau-dem-muong-man": [
        ("cover.webp", "CHUYẾN TÀU ĐÊM MƯỜNG MÁN", (25, 25, 35), (180, 170, 210)),
        ("d05-cua-truot.webp", "CỬA TRƯỢT KHOANG 4 & VẾT MA SÁT", (35, 30, 30), (210, 170, 140)),
        ("d12-cuon-cuoc.webp", "TANG VẬT: CUỘN CƯỚC & DÙI SẮT", (30, 35, 40), (150, 190, 200))
    ],
    "bong-nang-hoi-an": [
        ("cover.webp", "BÓNG NẮNG GIẾNG BÁ LỄ", (45, 35, 15), (230, 190, 80)),
        ("d03-gieng-ba-le.webp", "HIỆN TRƯỜNG GIẾNG CỔ BÁ LỄ", (30, 40, 30), (160, 210, 140)),
        ("d07-anh-com-ga.webp", "ẢNH BẰNG CHỨNG QUÁN CƠM GÀ", (50, 40, 20), (240, 200, 100))
    ],
    "lua-than-tay-nguyen": [
        ("cover.webp", "ĐÊM LỬA TÀN BUÔN EA KRAL", (45, 20, 15), (240, 140, 70)),
        ("d05-xa-gac.webp", "VẬT CHỨNG: XÀ GẠC KHẮC CHỮ B", (35, 25, 20), (210, 120, 80)),
        ("d11-rui-dien.webp", "BẪY NHIỆT: ĐUI ĐÈN & RƠ-LE MÁY ẤP TRỨNG", (40, 30, 25), (220, 160, 90))
    ],
    "gac-den-hon-dau": [
        ("cover.webp", "GÁC ĐÈN HÒN DÁU", (15, 25, 40), (120, 170, 220)),
        ("d11-may-phat.webp", "MÁY PHÁT YANMAR & THANH LƯỠNG KIM", (25, 35, 30), (140, 190, 160)),
        ("d15-ao-mua.webp", "ÁO MƯA DÍNH MÁU & TRANG NHẬT KÝ", (45, 35, 20), (230, 180, 90))
    ],
    "vang-bong-cho-lon": [
        ("cover.webp", "VÀNG BÓNG CHỢ LỚN", (40, 30, 15), (230, 180, 70)),
        ("d05-num-ket.webp", "NÚM XOAY KÉT SẮT CHUBB DÍNH PHẤN", (30, 35, 30), (170, 200, 160)),
        ("d10-manh-giay.webp", "MẢNH GIẤY GHI 24 HOÁN VỊ MẬT SỐ", (45, 40, 30), (220, 200, 150))
    ],
    "tieng-huan-van-don": [
        ("cover.webp", "TIẾNG HÚ CẢNG VÂN ĐỒN", (20, 30, 40), (130, 180, 220)),
        ("d05-nap-khoang.webp", "NẮP KHOANG LẠNH SỐ 3 THEN CÀI NGOÀI", (30, 25, 35), (180, 150, 190)),
        ("d11-da-kho.webp", "MẪU ĐÁ KHÔ CO2 & PHỄU QUẠT HÚT", (20, 35, 45), (150, 210, 240))
    ],
    "hoi-chuong-chua-thay": [
        ("cover.webp", "HỒI CHUÔNG NÚI SÀI SƠN", (35, 30, 25), (200, 170, 120)),
        ("d05-gac-chuong.webp", "GÁC CHUÔNG & CHÀY GỖ ĐẠI HỒNG CHUNG", (40, 35, 30), (210, 180, 130)),
        ("d11-ong-tre.webp", "ỐNG BƯƠNG TRE BẬP BÊNH THỦY LỰC", (35, 40, 25), (170, 210, 120))
    ],
    "vet-muc-lang-dong-ho": [
        ("cover.webp", "VẾT MỰC LÀNG ĐÔNG HỒ", (45, 20, 20), (240, 120, 100)),
        ("d03-ban-khac.webp", "BẢN KHẮC GỖ THỊ GÃY ĐÔI DÍNH PHẨM SON", (50, 25, 20), (240, 140, 110)),
        ("d10-dam-go.webp", "DĂM GỖ THỊ & DÉP TỔ ONG BÙN SÔNG ĐUỐNG", (40, 35, 30), (220, 190, 130))
    ]
}

def generate():
    for case_id, files in cases_images.items():
        case_dir = os.path.join(ROOT, case_id, "images")
        os.makedirs(case_dir, exist_ok=True)
        for filename, label, bg_color, fg_color in files:
            filepath = os.path.join(case_dir, filename)
            # Create a 800x600 image with gradient/noise styling
            img = Image.new("RGB", (800, 600), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Subtle border
            draw.rectangle([10, 10, 790, 590], outline=fg_color, width=3)
            draw.rectangle([20, 20, 780, 580], outline=(bg_color[0]+30, bg_color[1]+30, bg_color[2]+30), width=1)
            
            # Center title text
            draw.text((400, 280), label, fill=fg_color, anchor="mm")
            draw.text((400, 320), f"HỒ SƠ: {case_id.upper()}", fill=(180, 180, 180), anchor="mm")
            draw.text((400, 550), "[ HỒ SƠ PHÁ ÁN - BÀN ĐIỀU TRA ]", fill=(120, 120, 120), anchor="mm")
            
            # Save as webp with high efficiency
            img.save(filepath, "WEBP", quality=80)
            print(f"Created: {filepath} ({os.path.getsize(filepath) // 1024} KB)")

if __name__ == "__main__":
    generate()
