#!/usr/bin/env python3
import glob
import json
import os

ai_generated_files = {
    ("bong-nang-hoi-an", "images/cover.webp"): "AI Model (Hội An Box Mockup)",
    ("bong-nang-hoi-an", "images/d03-gieng-ba-le.webp"): "AI Model (Giếng cổ Bá Lễ)",
    ("bong-nang-hoi-an", "images/d07-anh-com-ga.webp"): "AI Model (Bằng chứng quán cơm gà)",
    ("chuyen-tau-dem-muong-man", "images/cover.webp"): "AI Model (Tàu SE3 Box Mockup)",
    ("suong-mu-trai-trai", "images/cover.webp"): "AI Model (Trại Mát Box Mockup)",
    ("tieng-dan-day-pho-hien", "images/cover.webp"): "AI Model (Phố Hiến Box Mockup)",
    ("lua-than-tay-nguyen", "images/cover.webp"): "AI Model (Ea Kral Box Mockup)",
    ("gac-den-hon-dau", "images/cover.webp"): "AI Model (Hòn Dáu Box Mockup)",
    ("vang-bong-cho-lon", "images/cover.webp"): "AI Model (Chợ Lớn Box Mockup)",
    ("tieng-huan-van-don", "images/cover.webp"): "AI Model (Vân Đồn Box Mockup)",
    ("vet-muc-lang-dong-ho", "images/cover.webp"): "AI Model (Đông Hồ Box Mockup)",
    ("ly-tra-trao-doc", "images/cover.webp"): "AI Model (Ly Trà Sài Gòn Box Mockup)",
}

cases_data = []
total_images = 0
official_images = 0
demo_images = 0

for p in sorted(glob.glob("public/cases/*/case.json")):
    cid = p.split("/")[2]
    with open(p) as f:
        d = json.load(f)
    
    c_no = d.get("no", 0)
    c_title = d.get("title", "")
    items = []
    
    # 1. Cover
    cov_rel = d.get("cover", "images/cover.webp")
    cov_path = os.path.join("public/cases", cid, cov_rel)
    cov_sz = os.path.getsize(cov_path) // 1024 if os.path.exists(cov_path) else 0
    is_cov_ai = (cid, cov_rel) in ai_generated_files
    items.append({
        "type": "Ảnh bìa hộp (3:4)",
        "file": cov_rel,
        "size_kb": cov_sz,
        "status": "CHÍNH THỨC (AI Model)" if is_cov_ai else "DEMO (Cần tạo lại)",
        "note": ai_generated_files.get((cid, cov_rel), "Đồ họa mô phỏng nội bộ")
    })
    total_images += 1
    if is_cov_ai: official_images += 1
    else: demo_images += 1
    
    # 2. Documents
    for doc in d.get("documents", []):
        if "image" in doc:
            img_rel = doc["image"]
            img_p = os.path.join("public/cases", cid, img_rel)
            sz = os.path.getsize(img_p) // 1024 if os.path.exists(img_p) else 0
            is_doc_ai = (cid, img_rel) in ai_generated_files
            items.append({
                "type": f"Tư liệu {doc['id']}",
                "file": img_rel,
                "size_kb": sz,
                "status": "CHÍNH THỨC (AI Model)" if is_doc_ai else "DEMO (Cần tạo lại)",
                "note": ai_generated_files.get((cid, img_rel), doc.get("title", ""))
            })
            total_images += 1
            if is_doc_ai: official_images += 1
            else: demo_images += 1
            
    cases_data.append({
        "no": c_no,
        "id": cid,
        "title": c_title,
        "items": items
    })

# Build markdown
md = []
md.append("# BẢNG THEO DÕI TIẾN TRÌNH HÌNH ẢNH HỒ SƠ VỤ ÁN")
md.append("## (IMAGE GENERATION AUDIT & PRODUCTION TRACKER)")
md.append("")
md.append("> [!IMPORTANT]")
md.append("> **Mục đích tài liệu:** Phân loại rõ ràng toàn bộ 58 hình ảnh trong hệ thống game phá án: đâu là hình ảnh **CHÍNH THỨC** (đã sinh bằng AI Image Model) và đâu là hình ảnh **DEMO** (đồ họa dựng tạm nội bộ đang chờ tạo lại bằng AI model). Dùng làm cơ sở dữ liệu để kích hoạt sinh ảnh tự động khi quota hồi phục.")
md.append("")
md.append("---")
md.append("")
md.append("## 📊 TỔNG QUAN TIẾN ĐỘ")
md.append("")
md.append(f"- **Tổng số hình ảnh trong toàn bộ hệ thống:** **{total_images}** tệp (.webp)")
md.append(f"- **Đã hoàn thiện CHÍNH THỨC bằng Model AI:** **{official_images} / {total_images}** ({official_images*100//total_images}%)")
md.append(f"- **Bản DEMO đồ họa nội bộ (Cần sinh lại bằng Model AI):** **{demo_images} / {total_images}** ({demo_images*100//total_images}%)")
md.append("")
md.append("```mermaid")
md.append("pie title Tỉ lệ hoàn thiện hình ảnh chính thức")
md.append(f'    "Đã sinh bằng AI Model (Chính thức)" : {official_images}')
md.append(f'    "Bản Demo đồ họa nội bộ (Cần sinh lại)" : {demo_images}')
md.append("```")
md.append("")
md.append("---")
md.append("")
md.append("## 📋 CHI TIẾT THEO TỪNG VỤ ÁN (17 CASES)")
md.append("")

for c in cases_data:
    md.append(f"### Case {c['no']:02d}: {c['title']} (`{c['id']}`)")
    md.append("| STT | Hạng mục ảnh | Tên file | Kích thước | Trạng thái hiện tại | Chi tiết / Nguồn gốc |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    for idx, it in enumerate(c["items"], 1):
        status_badge = "🟢 **CHÍNH THỨC (AI Model)**" if "CHÍNH THỨC" in it["status"] else "🟡 *DEMO (Cần tạo lại)*"
        md.append(f"| {idx} | {it['type']} | `{it['file']}` | {it['size_kb']} KB | {status_badge} | {it['note']} |")
    md.append("")

md.append("---")
md.append("")
md.append("## 🎯 HƯỚNG DẪN TÁI SINH ẢNH CHÍNH THỨC (NEXT STEPS)")
md.append("")
md.append("1. **Danh sách ưu tiên sinh lại bằng AI Model:**")
md.append("   - **Đợt 1 (7 ảnh bìa còn thiếu):** `demo-01/cover.webp`, `con-nuoc-ram-thang-gieng/cover.webp`, `mua-dong-binh-ty/cover.webp`, `hoi-chuong-chua-thay/cover.webp`, `buc-thu-dem-tuyet-trang/cover.webp`, `dem-sung-no-tay-son/cover.webp`, `quai-vat-21-khuon-mat/cover.webp`.")
md.append("   - **Đợt 2 (39 ảnh vật chứng hiện trường):** Sử dụng toàn bộ prompt chi tiết đã được chuẩn hóa trong `authoring/<case_id>/image-prompts.md` và `art_direction_dossier.md`.")
md.append("")
md.append("2. **Quy trình kích hoạt khi quota sẵn sàng:**")
md.append("   - Kiểm tra hạn ngạch Gemini Image API hoặc cấu hình `GEMINI_API_KEY` trả phí.")
md.append("   - Chạy script chuyển đổi tự động: `python3 scratch/convert_generated_images.py`.")
md.append("   - Kiểm định tính toàn vẹn bằng lệnh: `npm run validate`.")

with open("authoring/IMAGE_GENERATION_TRACKER.md", "w") as f:
    f.write("\n".join(md))

print("Created authoring/IMAGE_GENERATION_TRACKER.md successfully!")
