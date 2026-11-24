import json, os

cases = {
    'bong-nang-hoi-an': ('q5', [
        "Xem xét đối tượng nào có nợ nần cờ bạc, có tên trên hóa đơn mua ống nhựa PVC và có vết bùn rêu giếng trên giày.",
        "Đối chiếu bức ảnh góc bóng nắng do nghi phạm chụp với phân tích quang học của chuyên gia thiên văn."
    ]),
    'dem-sung-no-tay-son': ('q5', [
        "Ai là đối tượng sở hữu khẩu súng K54 có vân tay trên bao thuốc lá Du Lịch và có lộ trình qua bến phà Đen?",
        "Đối chiếu kết quả khai quật thu hồi 108 lượng vàng tại bãi ngô sông Hồng với nơi ẩn náu của đối tượng truy nã."
    ]),
    'gac-den-hon-dau': ('q5', [
        "Ai có chuyên môn cơ điện chế tạo bẫy ngắn mạch trễ, có kìm tuốt chì, sở hữu dao găm thợ lặn và tham ô 3.200 lít dầu?",
        "Đối chiếu vết máu trên chiếc áo mưa giấu trong bầu lọc gió với mẫu ADN của nạn nhân."
    ]),
    'lua-than-tay-nguyen': ('q5', [
        "Ai là người sở hữu xà gạc dính máu, biết kỹ thuật đấu nối đui đèn điện bẫy nhiệt và giấu tượng ngọc trong bồ thóc?",
        "Đối chiếu mẫu bùn đỏ pha cát vàng dính trên gấu quần nghi phạm với vết đất chân cầu thang nhà già làng."
    ]),
    'vang-bong-cho-lon': ('q5', [
        "Ai là người biết rõ thói quen uống cà phê của ông Thành, viết mảnh giấy 24 hoán vị và tàng trữ vàng thỏi trong hộp trà?",
        "Đối chiếu mẫu bột phấn trên núm két sắt và kết quả giám định lọ thuốc ngủ cloral hydrat thu giữ tại nhà riêng."
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
print("Fixed hints for Batch 2.")
