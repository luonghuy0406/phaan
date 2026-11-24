#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path("/Users/huynguyen/Documents/game_pha_an")
CASES_DIR = ROOT / "public" / "cases"
AUTHORING_DIR = ROOT / "authoring"

# Define official AI images
OFFICIAL_AI = {
    ("bong-nang-hoi-an", "cover.webp"),
    ("bong-nang-hoi-an", "d03-gieng-ba-le.webp"),
    ("bong-nang-hoi-an", "d07-anh-com-ga.webp"),
    ("tieng-dan-day-pho-hien", "cover.webp"),
    ("suong-mu-trai-trai", "cover.webp"),
    ("chuyen-tau-dem-muong-man", "cover.webp"),
    ("lua-than-tay-nguyen", "cover.webp"),
    ("gac-den-hon-dau", "cover.webp"),
    ("vang-bong-cho-lon", "cover.webp"),
    ("tieng-huan-van-don", "cover.webp"),
    ("vet-muc-lang-dong-ho", "cover.webp"),
    ("ly-tra-trao-doc", "cover.webp"),
}

def get_case_order():
    idx_path = CASES_DIR / "index.json"
    with open(idx_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cases = []
    case_list = data.get("cases", data) if isinstance(data, dict) else data
    for c in case_list:
        cid = c.get("id")
        title = c.get("title")
        cases.append((cid, title))
    # demo-01
    return [("demo-01", "Chiếc đồng hồ ở ngõ Gác Chuông")] + [c for c in cases if c[0] != "demo-01"]

def find_prompt_line(case_id, filename):
    prompt_file = AUTHORING_DIR / case_id / "image-prompts.md"
    if not prompt_file.exists():
        prompt_file = AUTHORING_DIR / case_id / "kich-ban-va-prompts.md"
    if not prompt_file.exists():
        return None, 1
    
    # stem search
    stem = Path(filename).stem
    # e.g. cover -> Cover
    terms = [filename, stem]
    if "cover" in stem:
        terms.extend(["Cover", "Ảnh bìa", "Bìa"])
    if "d01" in stem or "bao-chi" in stem or "newspaper" in stem:
        terms.extend(["d01", "Báo", "newspaper", "bao-chi"])
    if "d02" in stem:
        terms.extend(["d02", "Sơ đồ", "Biên bản", "bản đồ"])
    if "d03" in stem:
        terms.extend(["d03", "Sơ đồ", "then cài", "giếng", "hầm"])
    if "d04" in stem:
        terms.extend(["d04", "Sơ đồ", "ghe", "tiệm", "thương tổn"])
    if "d05" in stem:
        terms.extend(["d05", "Hiện trường", "Khám nghiệm", "giải phẫu", "bức thư", "xà gồ"])
    if "d06" in stem:
        terms.extend(["d06", "chân dung", "tử thi", "ảnh thẻ"])
    if "d07" in stem:
        terms.extend(["d07", "cơm gà", "tranh", "hóa đơn", "hoa khôi"])
    if "d08" in stem:
        terms.extend(["d08", "mắt cáo", "cơ học", "đồng hồ"])
    if "d09" in stem:
        terms.extend(["d09", "vé", "cuống vé"])
    if "d11" in stem:
        terms.extend(["d11", "sợi len", "nhiệt độ", "rùi điện", "hộp kẹo"])
    if "d12" in stem:
        terms.extend(["d12", "vé phà", "cuộn cước", "kho lạnh"])
    if "d15" in stem:
        terms.extend(["d15", "cổ phiếu", "áo mưa"])
    
    with open(prompt_file, "r", encoding="utf-8") as pf:
        lines = pf.readlines()
    
    for term in terms:
        for idx, line in enumerate(lines, 1):
            if term.lower() in line.lower():
                return prompt_file, idx
                
    return prompt_file, 1

def generate_trackers():
    cases = get_case_order()
    total_imgs = 0
    official_count = 0
    demo_count = 0
    
    case_tables = []
    prompt_entries = []
    
    for case_id, title in cases:
        c_dir = CASES_DIR / case_id / "images"
        if not c_dir.exists():
            continue
        
        # Read case.json to see which images are referenced
        case_json_file = CASES_DIR / case_id / "case.json"
        ref_images = []
        if case_json_file.exists():
            with open(case_json_file, "r", encoding="utf-8") as f:
                c_json = json.load(f)
            cov = c_json.get("cover")
            if cov:
                ref_images.append((Path(cov).name, "Ảnh bìa hộp (3:4)"))
            for doc in c_json.get("documents", []):
                dimg = doc.get("image")
                if dimg:
                    dname = Path(dimg).name
                    dtitle = doc.get("title", "")
                    did = doc.get("id", "")
                    ref_images.append((dname, f"Tài liệu {did} ({dtitle[:30]}...)"))
        
        # Sort and deduplicate by filename
        seen = set()
        dedup_images = []
        for fn, desc in ref_images:
            if fn not in seen:
                seen.add(fn)
                dedup_images.append((fn, desc))
                
        # Also include any files in dir not referenced
        for fpath in sorted(c_dir.glob("*.webp")):
            if fpath.name not in seen:
                dedup_images.append((fpath.name, "Tư liệu bổ sung"))
                seen.add(fpath.name)
        
        table_rows = []
        c_prompts = []
        for idx, (fn, desc) in enumerate(dedup_images, 1):
            total_imgs += 1
            fpath = c_dir / fn
            size_kb = int(fpath.stat().st_size / 1024) if fpath.exists() else 0
            is_official = (case_id, fn) in OFFICIAL_AI
            
            p_file, p_line = find_prompt_line(case_id, fn)
            p_file_str = str(p_file) if p_file else ""
            p_link = f"[{p_file.name}#L{p_line}](file://{p_file_str}#L{p_line})" if p_file else "*(N/A)*"
            
            if is_official:
                official_count += 1
                status = "🟢 **CHÍNH THỨC (AI Model)**"
                origin = "AI Image Generator"
            else:
                demo_count += 1
                status = "🟡 *DEMO (Cần tạo lại)*"
                origin = f"Đồ họa nội bộ • Prompt: {p_link}"
                c_prompts.append((fn, desc, p_file_str, p_file.name if p_file else "", p_line))
            
            table_rows.append(f"| {idx} | {desc} | `{fn}` | {size_kb} KB | {status} | {origin} |")
        
        table_md = f"### Vụ án: {title} (`{case_id}`)\n"
        table_md += "| STT | Hạng mục ảnh | Tên file | Kích thước | Trạng thái hiện tại | Chi tiết / Nguồn gốc |\n"
        table_md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        table_md += "\n".join(table_rows) + "\n"
        case_tables.append(table_md)
        
        if c_prompts:
            prompt_entries.append((case_id, title, c_prompts))
            
    # Build tracker markdown
    tracker_md = f"""# BẢNG THEO DÕI TIẾN TRÌNH HÌNH ẢNH HỒ SƠ VỤ ÁN
## (IMAGE GENERATION AUDIT & PRODUCTION TRACKER)

> [!IMPORTANT]
> **Mục đích tài liệu:** Phân loại rõ ràng toàn bộ {total_imgs} hình ảnh trong hệ thống game phá án: đâu là hình ảnh **CHÍNH THỨC** (đã sinh bằng AI Image Model) và đâu là hình ảnh **DEMO** (đồ họa dựng tạm nội bộ đang chờ tạo lại bằng AI model). Dùng làm cơ sở dữ liệu để kích hoạt sinh ảnh tự động khi quota hồi phục.

---

## 📊 TỔNG QUAN TIẾN ĐỘ

- **Tổng số hình ảnh trong toàn bộ hệ thống:** **{total_imgs}** tệp (.webp)
- **Đã hoàn thiện CHÍNH THỨC bằng Model AI:** **{official_count} / {total_imgs}** ({int(official_count/total_imgs*100)}%)
- **Bản DEMO đồ họa nội bộ (Cần sinh lại bằng Model AI):** **{demo_count} / {total_imgs}** ({int(demo_count/total_imgs*100)}%)

```mermaid
pie title Tỉ lệ hoàn thiện hình ảnh chính thức ({total_imgs} ảnh)
    "Đã sinh bằng AI Model (Chính thức)" : {official_count}
    "Bản Demo đồ họa nội bộ (Cần sinh lại)" : {demo_count}
```

---

## 📋 CHI TIẾT THEO TỪNG VỤ ÁN (17 CASES)

""" + "\n".join(case_tables)

    with open(AUTHORING_DIR / "IMAGE_GENERATION_TRACKER.md", "w", encoding="utf-8") as f:
        f.write(tracker_md)
        
    with open("/Users/huynguyen/.gemini/antigravity/brain/a47913dd-ad08-4d25-85e6-88df6edc1929/image_generation_tracker.md", "w", encoding="utf-8") as f:
        f.write(tracker_md)

    # Build prompt links markdown
    links_md = f"""# DANH MỤC LIÊN KẾT PROMPT CHO CÁC HÌNH ẢNH CHƯA TẠO
## (PROMPT SOURCE CODES & DIRECT LINKS FOR UNGENERATED IMAGES)

> [!TIP]
> Bảng tổng hợp liên kết trực tiếp tới file kịch bản/prompt cho từng hình ảnh bản Demo (chưa sinh bằng AI Image Model). Nhấp trực tiếp vào link để mở đúng file và dòng tương ứng trong dự án.

---

## 📊 THỐNG KÊ TÀI NGUYÊN CHỜ SINH ẢNH

- **Tổng số ảnh chờ tạo chính thức:** **{demo_count}** hình ảnh.
- **Phân bổ:** 17/17 vụ án (Bao gồm 7 ảnh bìa hộp remaster và 85 ảnh tư liệu/hiện trường/sơ đồ).

---

"""
    for case_id, title, p_list in prompt_entries:
        links_md += f"### {title} (`{case_id}`)\n\n"
        links_md += "| STT | Hạng mục ảnh | Tên file đích | File Prompt nguồn | Dòng | Thao tác |\n"
        links_md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
        for idx, (fn, desc, p_path, p_name, p_line) in enumerate(p_list, 1):
            if p_path:
                link = f"[{p_name}](file://{p_path}#L{p_line})"
                action = f"[Mở Prompt](file://{p_path}#L{p_line})"
            else:
                link = "*(Đang cập nhật)*"
                action = "-"
            links_md += f"| {idx} | {desc} | `{fn}` | {link} | L{p_line} | {action} |\n"
        links_md += "\n"

    with open(AUTHORING_DIR / "PROMPT_LINKS_CHUA_TAO.md", "w", encoding="utf-8") as f:
        f.write(links_md)
        
    with open("/Users/huynguyen/.gemini/antigravity/brain/a47913dd-ad08-4d25-85e6-88df6edc1929/prompt_links_chua_tao.md", "w", encoding="utf-8") as f:
        f.write(links_md)

    print(f"Generated trackers: Total {total_imgs} images ({official_count} official, {demo_count} demo).")

if __name__ == "__main__":
    generate_trackers()
