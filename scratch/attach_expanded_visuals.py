#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path("/Users/huynguyen/Documents/game_pha_an")
CASES_DIR = ROOT / "public" / "cases"

ATTACHMENTS = {
    "demo-01": {
        "d02": ("images/d02-so-do-nha.webp", "Sơ đồ mặt bằng tầng 2 căn nhà cổ ngõ Gác Chuông")
    },
    "con-nuoc-ram-thang-gieng": {
        "d02": ("images/d02-ban-do-song.webp", "Sơ đồ khúc sông Hàm Luông và nhánh rạch Cây Bần"),
        "d05": ("images/d05-giai-phau.webp", "Sơ đồ phác họa hình nhân y pháp và dấu hiệu ngạt nước")
    },
    "mua-dong-binh-ty": {
        "d02": ("images/d02-so-do-can-ho.webp", "Sơ đồ mặt bằng căn hộ 204 nhà A6 tập thể Dệt Thống Nhất"),
        "d06": ("images/d06-so-do-tu-thi.webp", "Sơ đồ giải phẫu đường thở và co thắt phế quản cấp tính")
    },
    "tieng-dan-day-pho-hien": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Hải Hưng: Đình Hoa Nguyệt trong đêm hội rằm"),
        "d03": ("images/d03-so-do-dinh.webp", "Sơ đồ kiến trúc mặt bằng đình cổ Hoa Nguyệt"),
        "d06": ("images/d06-anh-chan-dung.webp", "Ảnh kỷ niệm nghệ nhân phường chèo và kép đàn Chu Văn Bình")
    },
    "suong-mu-trai-trai": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Lâm Đồng: Cổng trang trại hoa Lâm Viên trong sương sớm"),
        "d03": ("images/d03-so-do-trang-trai.webp", "Sơ đồ tổng thể các nhà kính và kho lạnh trang trại hoa Lâm Viên"),
        "d11": ("images/d11-dong-ho-nhiet-do.webp", "Biểu đồ tròn tự ghi nhiệt độ kho lạnh số 2 lúc nửa đêm")
    },
    "chuyen-tau-dem-muong-man": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Bình Thuận: Đoàn tàu SE3 dừng khẩn cấp tại ga Mường Mán"),
        "d03": ("images/d03-so-do-toa-tau.webp", "Sơ đồ mặt bằng toa 6 tàu Thống Nhất SE3"),
        "d09": ("images/d09-ve-tau-se3.webp", "Bản chụp cuống vé tàu hỏa Thống Nhất SE3")
    },
    "bong-nang-hoi-an": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Quảng Nam: Phố cổ Hội An và khu vực giếng Bá Lễ"),
        "d04": ("images/d04-so-do-tu-duong.webp", "Sơ đồ ngõ hẹp từ cổng từ đường họ Lương ra giếng Bá Lễ")
    },
    "lua-than-tay-nguyen": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Bản tin An ninh: Hiện trường đổ nát kho cà phê buôn Ea Kral"),
        "d03": ("images/d03-so-do-buon-lang.webp", "Sơ đồ mặt bằng buôn Ea Kral và đường dây tải điện tự kéo"),
        "d06": ("images/d06-anh-the.webp", "Ảnh thẻ căn cước và hồ sơ nhân chứng buôn Ea Kral")
    },
    "gac-den-hon-dau": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Hải Phòng: Tháp hải đăng cổ Hòn Dáu trong giông bão"),
        "d02": ("images/d02-ban-do-dao.webp", "Sơ đồ cao độ và các công trình trên đảo Hòn Dáu"),
        "d04": ("images/d04-giai-phau.webp", "Sơ đồ thương tổn hộp sọ giám định pháp y")
    },
    "vang-bong-cho-lon": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Sài Gòn Giải Phóng: Mặt tiền tiệm kim hoàn Vạn Thành Chợ Lớn năm 1995"),
        "d04": ("images/d04-so-do-tiem-vang.webp", "Sơ đồ mặt bằng quầy tủ kính và vị trí két sắt tiệm kim hoàn"),
        "d09": ("images/d09-cuong-ve.webp", "Bản chụp cuống vé xem ca nhạc Dạ thảo rạp Hào Huê")
    },
    "tieng-huan-van-don": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Quảng Ninh: Tàu cá QN-9288-TS cập cảng Cái Rồng"),
        "d04": ("images/d04-so-do-tau-ca.webp", "Sơ đồ mặt cắt hệ thống hầm bảo quản đá lạnh tàu cá"),
        "d03": ("images/d03-giai-phau.webp", "Sơ đồ y pháp: Dấu hiệu ngạt khí độc Carbon Dioxide (CO2)")
    },
    "hoi-chuong-chua-thay": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Bản tin Hà Tây: Toàn cảnh núi Sài Sơn và chùa Thầy"),
        "d03": ("images/d03-so-do-chua.webp", "Sơ đồ mặt bằng gác chuông và tòa chính điện chùa Thầy"),
        "d08": ("images/d08-so-do-co-hoc.webp", "Bản phác thảo sơ đồ nguyên lý đòn bẩy thủy lực nước nhỏ giọt")
    },
    "vet-muc-lang-dong-ho": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Văn hóa Bắc Ninh: Sân phơi giấy điệp làng tranh Đông Hồ"),
        "d04": ("images/d04-so-do-lang-tranh.webp", "Sơ đồ đường làng Đông Hồ, xưởng tranh và lối ra bến sông Đuống"),
        "d07": ("images/d07-tranh-dong-ho.webp", "Bản dập thử tranh khắc gỗ Đám cưới chuột trên giấy điệp")
    },
    "ly-tra-trao-doc": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Tuổi Trẻ: Hiện trường phong tỏa quán trà sữa đường Nguyễn Huệ"),
        "d03": ("images/d03-so-do-quan-tra.webp", "Sơ đồ mặt bằng quán trà sữa và khu vực máy pha chế"),
        "d07": ("images/d07-hoa-don-tra-sua.webp", "Bản scan hóa đơn thanh toán in nhiệt máy POS")
    },
    "buc-thu-dem-tuyet-trang": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Bản tin CNN: Căn biệt thự gia đình Ramsey phủ đầy tuyết trắng"),
        "d04": ("images/d04-so-do-biet-thu.webp", "Sơ đồ kiến trúc mặt bằng tầng hầm và tầng trệt biệt thự"),
        "d07": ("images/d07-anh-hoa-khoi.webp", "Ảnh hồ sơ hoa khôi nhí tóc vàng JonBenét Ramsey")
    },
    "dem-sung-no-tay-son": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo An ninh Thủ đô: Hiện trường tiệm vàng phố Tây Sơn sáng sớm"),
        "d04": ("images/d04-so-do-hien-truong.webp", "Sơ đồ hiện trường tiệm vàng, ngõ số 12 và lối thoát ra bến phà"),
        "d12": ("images/d12-ve-pha-den.webp", "Bản chụp cuống vé phà Đen đêm giông bão")
    },
    "quai-vat-21-khuon-mat": {
        "d01": ("images/d01-bao-chi.webp", "Ảnh tư liệu Báo Asahi Shimbun: Cảnh sát phong tỏa trụ sở tập đoàn bánh kẹo"),
        "d08": ("images/d08-phac-hoa-mat-cao.webp", "Bản phác họa truy nã 'Người đàn ông mắt cáo' của Cảnh sát Osaka"),
        "d15": ("images/d15-bieu-do-co-phieu.webp", "Biểu đồ biến động giá cổ phiếu tập đoàn Glico trong khủng hoảng")
    }
}

def main():
    total_attached = 0
    for case_id, doc_map in ATTACHMENTS.items():
        case_file = CASES_DIR / case_id / "case.json"
        if not case_file.exists():
            print(f"Error: {case_file} does not exist")
            continue
        
        with open(case_file, "r", encoding="utf-8") as f:
            case_data = json.load(f)
        
        docs = case_data.get("documents", [])
        modified = False
        for doc in docs:
            did = doc.get("id")
            if did in doc_map:
                img_path, caption = doc_map[did]
                target_file = CASES_DIR / case_id / img_path
                if not target_file.exists():
                    print(f"Warning: File {target_file} not found!")
                    continue
                doc["image"] = img_path
                doc["imageCaption"] = caption
                modified = True
                total_attached += 1
                print(f"✓ Attached {img_path} to {case_id} -> {did}")
        
        if modified:
            with open(case_file, "w", encoding="utf-8") as f:
                json.dump(case_data, f, ensure_ascii=False, indent=2)
                f.write("\n")
    
    print(f"\nSuccessfully attached {total_attached} visuals across all cases!")

if __name__ == "__main__":
    main()
