import json, os

cases = {
    'demo-01': ('q4', [
        "Xem xét đối tượng nào có mặt trong nhà, biết rõ vị trí cất đồng hồ và có mâu thuẫn giờ giấc ngoại phạm.",
        "Đối chiếu tên người cầm cố trên phiếu cầm đồ tiệm Phát Đạt với các nghi phạm."
    ]),
    'con-nuoc-ram-thang-gieng': ('q6', [
        "Xem xét ai có động cơ nợ đất hương hỏa, sở hữu kìm mở van lù và cuộn cước câu cá thu trong chòi đò.",
        "Đối chiếu thủ đoạn ngụy tạo hỏng máy đò theo con nước Rằm với diễn biến triều cường."
    ]),
    'mua-dong-binh-ty': ('q5', [
        "Ai có chuyên môn sửa chữa đồ đạc, có dấu vết dép rọ trên bậu cửa sổ ban công?",
        "Đối chiếu vị trí 12 chỉ vàng lá 9999 chôn giấu sau vườn chuối với nơi ở của nghi phạm."
    ]),
    'tieng-dan-day-pho-hien': ('q5', [
        "Ai là người biết rõ thói quen vuốt phím số 3 của cụ Cửu và có mặt ở buồng hóa trang trước giờ diễn?",
        "Đối chiếu tang vật khăn lụa tẩm độc và chứng cứ mua lá ngón tại hiệu thuốc bắc Nam Hòa Đường."
    ]),
    'suong-mu-trai-trai': ('q5', [
        "Ai có chìa khóa kho lạnh số 2, biết điều khiển máy nén khí làm đá lạnh sâu -18°C?",
        "Đối chiếu dấu vết lốp xe cút kít tại xưởng hoa và bao thuốc lá ba số 555 rơi tại cửa xả kho lạnh."
    ])
}

for cid, (qid, hints) in cases.items():
    p = f"public/cases/{cid}/case.json"
    with open(p, "r", encoding="utf-8") as f:
        c = json.load(f)
    for q in c.get("questions", []):
        if q.get("id") == qid:
            q["hints"] = hints
    with open(p, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
print("Fixed hints for Batch 1.")
