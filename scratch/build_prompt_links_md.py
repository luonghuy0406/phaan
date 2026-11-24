#!/usr/bin/env python3
import glob
import json
import os

ai_generated_files = {
    ("bong-nang-hoi-an", "images/cover.webp"),
    ("bong-nang-hoi-an", "images/d03-gieng-ba-le.webp"),
    ("bong-nang-hoi-an", "images/d07-anh-com-ga.webp"),
    ("chuyen-tau-dem-muong-man", "images/cover.webp"),
    ("suong-mu-trai-trai", "images/cover.webp"),
    ("tieng-dan-day-pho-hien", "images/cover.webp"),
    ("lua-than-tay-nguyen", "images/cover.webp"),
    ("gac-den-hon-dau", "images/cover.webp"),
    ("vang-bong-cho-lon", "images/cover.webp"),
    ("tieng-huan-van-don", "images/cover.webp"),
    ("vet-muc-lang-dong-ho", "images/cover.webp"),
    ("ly-tra-trao-doc", "images/cover.webp"),
}

workspace_root = "/Users/huynguyen/Documents/game_pha_an"

cases_missing = []

for p in sorted(glob.glob("public/cases/*/case.json")):
    cid = p.split("/")[2]
    with open(p) as f:
        d = json.load(f)
    
    c_no = d.get("no", 0)
    c_title = d.get("title", "")
    missing_items = []
    
    # 1. Cover
    cov_rel = d.get("cover", "images/cover.webp")
    if (cid, cov_rel) not in ai_generated_files:
        prompt_rel = "authoring/AI_COVER_PROMPTS.md"
        prompt_abs = f"{workspace_root}/{prompt_rel}"
        line_no = 1
        with open(prompt_abs) as pf:
            for idx, line in enumerate(pf, 1):
                if cid in line:
                    line_no = idx
                    break
        missing_items.append({
            "category": "Ảnh bìa hộp (3:4)",
            "dest_file": f"public/cases/{cid}/{cov_rel}",
            "prompt_file": prompt_rel,
            "prompt_link": f"file://{prompt_abs}#L{line_no}",
            "line_no": line_no,
            "brief": f"Hộp boardgame Noir: {c_title} (Split-face Collage)"
        })
        
    # 2. Documents
    for doc in d.get("documents", []):
        if "image" in doc:
            img_rel = doc["image"]
            if (cid, img_rel) not in ai_generated_files:
                img_name = os.path.basename(img_rel)
                doc_id = doc["id"]
                prompt_rel = f"authoring/{cid}/image-prompts.md"
                prompt_abs = f"{workspace_root}/{prompt_rel}"
                line_no = 1
                if os.path.exists(prompt_abs):
                    with open(prompt_abs) as pf:
                        for idx, line in enumerate(pf, 1):
                            if img_name in line or doc_id in line:
                                line_no = idx
                                break
                else:
                    prompt_rel = "authoring/art_direction_dossier.md"
                    prompt_abs = f"{workspace_root}/{prompt_rel}"
                
                missing_items.append({
                    "category": f"Tư liệu {doc_id}",
                    "dest_file": f"public/cases/{cid}/{img_rel}",
                    "prompt_file": prompt_rel,
                    "prompt_link": f"file://{prompt_abs}#L{line_no}",
                    "line_no": line_no,
                    "brief": doc.get("title", "")
                })
                
    if missing_items:
        cases_missing.append({
            "no": c_no,
            "id": cid,
            "title": c_title,
            "items": missing_items
        })

# Total missing
total_missing = sum(len(c["items"]) for c in cases_missing)

lines = []
lines.append("# DANH SÁCH 46 HÌNH ẢNH CẦN TẠO LẠI BẰNG AI MODEL & LIÊN KẾT PROMPT")
lines.append("## (AI IMAGE GENERATION PIPELINE & SOURCE PROMPT INDEX)")
lines.append("")
lines.append("> [!IMPORTANT]")
lines.append("> **Mục đích tài liệu:** Bảng điều phối dành riêng cho việc sinh lại ảnh chính thức bằng Model AI tạo ảnh (Midjourney v6, Google Gemini Image, DALL-E 3 hoặc Flux). Mỗi tệp ảnh demo đang chờ thay thế đều được gắn **đường link trực tiếp đến file prompt và số dòng cụ thể**.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 📌 TÓM TẮT TIẾN ĐỘ THỊ GIÁC")
lines.append("")
lines.append(f"- **Tổng số hình ảnh cần quản lý:** 58 tệp (.webp)")
lines.append(f"- 🟢 **Đã có ảnh chính thức bằng AI Model:** 12 tệp (Case 06 đầy đủ 3 ảnh + 9 ảnh bìa các case 03, 04, 05, 07, 08, 09, 10, 12, 13)")
lines.append(f"- 🟡 **Cần tạo lại bằng AI Model (Liệt kê bên dưới):** **{total_missing} tệp** (7 ảnh bìa + 39 ảnh vật chứng hiện trường)")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 📋 DANH SÁCH 46 HÌNH ẢNH CHƯA TẠO & LINK TỚI FILE PROMPT")
lines.append("")

for c in cases_missing:
    lines.append(f"### Case {c['no']:02d}: {c['title']} (`{c['id']}`)")
    lines.append(f"- **Thư mục case:** [`public/cases/{c['id']}/`](file://{workspace_root}/public/cases/{c['id']}/)")
    lines.append(f"- **File prompt toàn vụ án:** [`authoring/{c['id']}/image-prompts.md`](file://{workspace_root}/authoring/{c['id']}/image-prompts.md)")
    lines.append("")
    lines.append("| STT | Hạng mục | Tệp đích (`public/`) | File Prompt gốc (Click để mở) | Dòng | Tóm tắt mô tả |")
    lines.append("| :--- | :--- | :--- | :--- | :---: | :--- |")
    for idx, it in enumerate(c["items"], 1):
        prompt_basename = os.path.basename(it['prompt_file'])
        link_md = f"[{prompt_basename}#L{it['line_no']}]({it['prompt_link']})"
        lines.append(f"| {idx} | {it['category']} | `{it['dest_file']}` | {link_md} | L{it['line_no']} | {it['brief'][:45]} |")
    lines.append("")

lines.append("---")
lines.append("")
lines.append("## 🛠️ HƯỚNG DẪN THỰC THI NHANH")
lines.append("")
lines.append("1. **Khi hạn ngạch model AI được hồi phục:**")
lines.append("   - Yêu cầu subagent tạo ảnh `image-generator` đọc trực tiếp file prompt theo các link trên.")
lines.append("   - Sau khi model tạo xong file ảnh vào thư mục brain, chạy lệnh đồng bộ:")
lines.append("     ```bash")
lines.append("     python3 scratch/convert_generated_images.py")
lines.append("     ```")
lines.append("2. **Nếu tạo thủ công qua Midjourney / Bing / Flux:**")
lines.append("   - Mở từng link prompt ở cột thứ 4 để copy câu prompt tiếng Anh.")
lines.append("   - Đặt tỉ lệ khung hình: `--ar 3:4` đối với ảnh bìa, `--ar 4:3` đối với ảnh vật chứng/hiện trường.")
lines.append("   - Xuất file `.webp` chất lượng 85% và lưu đè vào cột **Tệp đích**.")
lines.append("3. **Kiểm định sau khi tạo:**")
lines.append("   ```bash")
lines.append("   npm run validate")
lines.append("   ```")

content = "\n".join(lines)

target_file = f"{workspace_root}/authoring/PROMPT_LINKS_CHUA_TAO.md"
with open(target_file, "w") as f:
    f.write(content)

print(f"Created {target_file} with {total_missing} linked items!")
