#!/usr/bin/env python3
import os
import glob
from PIL import Image

BRAIN_DIR = "/Users/huynguyen/.gemini/antigravity/brain/a47913dd-ad08-4d25-85e6-88df6edc1929"
CASES_DIR = "/Users/huynguyen/Documents/game_pha_an/public/cases"

# Mapping prefix in ImageName to (case_id, dest_filename)
MAPPING = {
    # Hoi An (done)
    "test_cover_hoi_an": ("bong-nang-hoi-an", "cover.webp"),
    "test_evidence_well": ("bong-nang-hoi-an", "d03-gieng-ba-le.webp"),
    "hoi_an_d07_com_ga": ("bong-nang-hoi-an", "d07-anh-com-ga.webp"),

    # chuyen-tau-dem-muong-man
    "muong_man_cover": ("chuyen-tau-dem-muong-man", "cover.webp"),
    "muong_man_d05_cua_truot": ("chuyen-tau-dem-muong-man", "d05-cua-truot.webp"),
    "muong_man_d12_cuon_cuoc": ("chuyen-tau-dem-muong-man", "d12-cuon-cuoc.webp"),

    # suong-mu-trai-trai
    "trai_mat_cover": ("suong-mu-trai-trai", "cover.webp"),
    "trai_mat_d05_hien_truong": ("suong-mu-trai-trai", "d05-hien-truong.webp"),
    "trai_mat_d12_kho_lanh": ("suong-mu-trai-trai", "d12-kho-lanh.webp"),

    # tieng-dan-day-pho-hien
    "pho_hien_cover": ("tieng-dan-day-pho-hien", "cover.webp"),
    "pho_hien_d04_dan_day": ("tieng-dan-day-pho-hien", "d04-dan-day.webp"),
    "pho_hien_d13_khan_lua": ("tieng-dan-day-pho-hien", "d13-khan-lua.webp"),

    # lua-than-tay-nguyen
    "tay_nguyen_cover": ("lua-than-tay-nguyen", "cover.webp"),
    "tay_nguyen_d05_xa_gac": ("lua-than-tay-nguyen", "d05-xa-gac.webp"),
    "tay_nguyen_d11_rui_dien": ("lua-than-tay-nguyen", "d11-rui-dien.webp"),

    # gac-den-hon-dau
    "hon_dau_cover": ("gac-den-hon-dau", "cover.webp"),
    "hon_dau_d11_may_phat": ("gac-den-hon-dau", "d11-may-phat.webp"),
    "hon_dau_d15_ao_mua": ("gac-den-hon-dau", "d15-ao-mua.webp"),

    # vang-bong-cho-lon
    "cho_lon_cover": ("vang-bong-cho-lon", "cover.webp"),
    "cho_lon_d05_num_ket": ("vang-bong-cho-lon", "d05-num-ket.webp"),
    "cho_lon_d10_manh_giay": ("vang-bong-cho-lon", "d10-manh-giay.webp"),

    # tieng-huan-van-don
    "van_don_cover": ("tieng-huan-van-don", "cover.webp"),
    "van_don_d05_nap_khoang": ("tieng-huan-van-don", "d05-nap-khoang.webp"),
    "van_don_d11_da_kho": ("tieng-huan-van-don", "d11-da-kho.webp"),

    # hoi-chuong-chua-thay
    "chua_thay_cover": ("hoi-chuong-chua-thay", "cover.webp"),
    "chua_thay_d05_gac_chuong": ("hoi-chuong-chua-thay", "d05-gac-chuong.webp"),
    "chua_thay_d11_ong_tre": ("hoi-chuong-chua-thay", "d11-ong-tre.webp"),

    # vet-muc-lang-dong-ho
    "dong_ho_cover": ("vet-muc-lang-dong-ho", "cover.webp"),
    "dong_ho_d03_ban_khac": ("vet-muc-lang-dong-ho", "d03-ban-khac.webp"),
    "dong_ho_d10_dam_go": ("vet-muc-lang-dong-ho", "d10-dam-go.webp"),

    # ly-tra-trao-doc
    "ly_tra_cover": ("ly-tra-trao-doc", "cover.webp"),
    "ly_tra_d05_nap_coc": ("ly-tra-trao-doc", "d05-nap-coc.webp"),
    "ly_tra_d11_ong_tiem": ("ly-tra-trao-doc", "d11-ong-tiem.webp"),

    # buc-thu-dem-tuyet-trang
    "tuyet_trang_cover": ("buc-thu-dem-tuyet-trang", "cover.webp"),
    "tuyet_trang_d05_buc_thu": ("buc-thu-dem-tuyet-trang", "d05-buc-thu.webp"),
    "tuyet_trang_d11_soi_len": ("buc-thu-dem-tuyet-trang", "d11-soi-len.webp"),

    # dem-sung-no-tay-son
    "tay_son_cover": ("dem-sung-no-tay-son", "cover.webp"),
    "tay_son_d05_vo_dan": ("dem-sung-no-tay-son", "d05-vo-dan.webp"),
    "tay_son_d11_bao_thuoc": ("dem-sung-no-tay-son", "d11-bao-thuoc.webp"),

    # quai-vat-21-khuon-mat
    "quai_vat_cover": ("quai-vat-21-khuon-mat", "cover.webp"),
    "quai_vat_d05_buc_thu": ("quai-vat-21-khuon-mat", "d05-buc-thu.webp"),
    "quai_vat_d11_hop_keo": ("quai-vat-21-khuon-mat", "d11-hop-keo.webp"),
}

def sync():
    jpg_files = glob.glob(os.path.join(BRAIN_DIR, "*.jpg"))
    converted = 0
    for jpg in jpg_files:
        base = os.path.basename(jpg)
        for key, (case_id, dest_file) in MAPPING.items():
            if base.startswith(key):
                target_path = os.path.join(CASES_DIR, case_id, "images", dest_file)
                try:
                    im = Image.open(jpg)
                    im.save(target_path, "WEBP", quality=85)
                    size_kb = os.path.getsize(target_path) // 1024
                    print(f"✓ Converted: {base} -> {case_id}/images/{dest_file} ({size_kb} KB)")
                    converted += 1
                except Exception as e:
                    print(f"✗ Failed {base}: {e}")
                break
    print(f"Total synced: {converted} files.")

if __name__ == "__main__":
    sync()
