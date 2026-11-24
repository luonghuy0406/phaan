#!/usr/bin/env python3
import json
import os

ROOT = "/Users/huynguyen/Documents/game_pha_an"

# 1. tieng-huan-van-don
def upgrade_van_don():
    path = os.path.join(ROOT, "public/cases/tieng-huan-van-don/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Nguyên nhân tử vong và tình trạng nắp khoang khóa kín",
            "intro": "Thuyền trưởng tàu cá xa bờ được phát hiện tử vong bí ẩn dưới khoang lạnh số 3 khi tàu cập cảng Cái Rồng. Hãy kiểm tra các dấu vết ban đầu.",
            "prompt": "Ghim 2 tài liệu chứng minh Thuyền trưởng tử vong do ngạt khí CO2 kèm tổn thương phỏng lạnh hình học và tình trạng nắp khoang lạnh số 3 bị gài then sắt từ bên ngoài.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Kết quả giám định tử thi về dấu hiệu ngạt khí cacbonic và các vết phỏng lạnh hình tròn trên da.",
                "Ảnh chụp cận cảnh nắp khoang lạnh số 3 bị gài then sắt kiên cố từ phía ngoài mặt boong."
            ],
            "explanation": [
                "Tài liệu d03 xác nhận nạn nhân chết ngạt trong môi trường yếm khí bão hòa khí CO2, trên tay có các vết bỏng nhiệt độ âm do tiếp xúc đá khô.",
                "Tài liệu d05 ghi nhận nắp khoang lạnh bằng thép bọc cao su bị gài then ngoài, người bên trong hoàn toàn không thể mở ra."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Bằng chứng ngoại phạm trên buồng lái",
            "intro": "Các thuyền viên và máy trưởng trên tàu đều được lấy lời khai về ca trực đêm xảy ra tai nạn.",
            "prompt": "Trong các biên bản hỏi cung thuyền viên tàu cá QN-9288-TS, hãy chỉ ra dòng lời khai khẳng định túc trực liên tục trên buồng lái đàm thoại vô tuyến từ 00h00 đến 03h30 sáng không rời nửa bước?",
            "answer": ["d06:003"],
            "hints": [
                "Rà soát lời khai của Thuyền phó phụ trách hoa tiêu buồng lái.",
                "Tìm câu khẳng định một mình cầm vô lăng và giữ liên lạc vô tuyến suốt ca đêm."
            ],
            "explanation": [
                "Tại d06 dòng 003, Lê Quốc Tuấn khai: 'Suốt từ 00h00 đến 03h30 sáng tôi ngồi liên tục trong cabin buồng lái cầm vô lăng điều khiển tàu và giữ đàm thoại vô tuyến với đài bờ Cái Rồng, tuyệt đối không hề rời buồng lái nửa bước'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Vết phỏng lạnh CO2, đá khô viên nén và quạt hút xả khí",
            "intro": "Cơ quan điều tra nghi ngờ hiện tượng 'tiếng hú ma ám' thực chất là một cơ chế vật lý ngụy tạo tinh vi.",
            "prompt": "Ghim 3 tài liệu liên kết thương tích phỏng lạnh do CO2 (Vòng 1) với bản phân tích kỹ thuật thăng hoa của đá khô (Vòng 3) và ảnh tang vật ống quạt hút xả khí tạo tiếng hú rùng rợn trong đêm (Vòng 3).",
            "need": 3,
            "answer": ["d03", "d10", "d11"],
            "hints": [
                "Giám định tử thi về nồng độ CO2 máu và vết phỏng lạnh hình học (ở Vòng 1).",
                "Bản phân tích kỹ thuật chứng minh đá khô CO2 thăng hoa làm tụt thân nhiệt giả mạo giờ chết sớm hơn 4 tiếng.",
                "Ảnh tang vật mẫu đá khô viên nén công nghiệp và phễu quạt hút gió tạo luồng khí áp suất cao phát ra tiếng hú."
            ],
            "explanation": [
                "Tài liệu d03 xác định nạn nhân tiếp xúc với nguồn nhiệt độ âm cực thấp.",
                "Tài liệu d10 giải mã thủ đoạn dùng đá khô thăng hoa giải phóng khí CO2 đậm đặc chiếm đoạt oxy, đồng thời làm lạnh sâu thi thể để đánh lừa giám định pháp y.",
                "Tài liệu d11 chụp phễu ống thông gió gắn ngược tạo hiệu ứng Venturi phát ra tiếng rít hú gió trong đêm bão để dọa các thủy thủ không dám lại gần hầm lạnh."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Sổ kiểm kê đá khô và ly trà gừng tẩm thuốc mê",
            "intro": "Khám xét buồng lái và phòng riêng của thuyền phó đã làm sáng tỏ hành vi giết người có kế hoạch.",
            "prompt": "Ghim 2 tài liệu chứng minh việc mua lén 50kg đá khô lạnh sâu và kết quả xét nghiệm ly trà gừng có độc chất chuốc mê nạn nhân trước khi nhốt vào khoang lạnh.",
            "need": 2,
            "answer": ["d12", "d15"],
            "hints": [
                "Sổ kiểm kê vật tư đá khô lạnh sâu ghi nhận lượng đá khô bị bớt xén dùng sai mục đích bảo quản cá.",
                "Kết quả xét nghiệm mẫu cặn ly trà gừng tìm thấy thuốc an thần liều cao seduxen."
            ],
            "explanation": [
                "Tài liệu d12 vạch trần việc Tuấn tự ý mua thêm 50kg đá khô CO2 viên nén trước ngày ra khơi.",
                "Tài liệu d15 chứng minh Thuyền trưởng Đạt đã bị đánh thuốc mê vào ly trà gừng trước khi bị đẩy xuống hầm lạnh khóa chốt."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án tàu cá Cái Rồng",
            "intro": "Tiếng hú ban đêm, vết phỏng đá khô CO2 và ly trà gừng chuốc mê đã vạch trần toàn bộ sự thật.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, ai là thủ phạm đã sát hại Thuyền trưởng Trần Văn Đạt?",
            "options": [
                "Thuyền phó Lê Quốc Tuấn do mâu thuẫn chia tiền bán hải sản và muốn đoạt quyền chỉ huy tàu cá, đã lén pha thuốc mê vào ly trà gừng của Thuyền trưởng Đạt, đẩy nạn nhân vào khoang lạnh số 3 gài then sắt ngoài rồi đổ 50kg đá khô CO2 làm ngạt thở, dùng ống quạt gió tạo tiếng hú dọa thủy thủ để ngụy tạo tai nạn ma ám.",
                "Máy trưởng Nguyễn Văn Sáu do bất cẩn trong lúc xả đá khô làm lạnh hầm cá đã để khí CO2 rò rỉ làm ngạt Thuyền trưởng, sau đó vì sợ hãi nên khóa then nắp hầm trốn tránh trách nhiệm.",
                "Thủy thủ Bùi Văn Hải do bị Thuyền trưởng khiển trách phạt trừ lương, đã lẻn vào hầm lạnh số 3 gài then sắt nhốt cấp trên rồi đổ đá khô sát hại.",
                "Tàu đánh cá bị một nhóm hải tặc lạ mặt đột nhập trong đêm bão khống chế Thuyền trưởng nhốt vào khoang lạnh rồi tẩu thoát."
            ],
            "answer": [0],
            "hints": [
                "Ai có chuyên môn hoa tiêu buồng lái, tự tay pha ly trà gừng cho nạn nhân và lén mua 50kg đá khô CO2 viên nén?",
                "Đối chiếu lời khai ngoại phạm của Tuấn với việc mất tín hiệu đàm thoại ICOM 45 phút trên biển."
            ],
            "explanation": [
                "Lê Quốc Tuấn là thủ phạm duy nhất. Kế hoạch giết người tinh vi bằng đá khô CO2 kết hợp hiệu ứng âm thanh dọa ma nhằm tạo bằng chứng ngoại phạm đã bị bóc trần hoàn toàn."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded tieng-huan-van-don (5 questions)")

# 2. hoi-chuong-chua-thay
def upgrade_chua_thay():
    path = os.path.join(ROOT, "public/cases/hoi-chuong-chua-thay/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Giờ chết thực tế của sư trụ trì và dấu vết gác chuông",
            "intro": "Đại đức Thích Tâm Viên được phát hiện viên tịch trong tịnh thất am thiền sau tiếng chuông chùa ngân vang lúc 10h15 sáng. Hãy kiểm tra các dấu vết bất thường.",
            "prompt": "Ghim 2 tài liệu chứng minh sư trụ trì đã tử vong từ trước 10h15 sáng và dấu vết dây dù cùng vũng nước bất thường trên sàn gác chuông chùa Cổ Sơn.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Kết quả giám định tử thi xác định vết hoằn siết cổ và thời điểm tử vong vào khoảng 07h00 - 08h00 sáng.",
                "Ảnh chụp gác chuông phát hiện vũng nước ướt loang và hệ thống chày gỗ giộng chuông có buộc sợi dây dù nối xuống máng nước."
            ],
            "explanation": [
                "Tài liệu d03 xác nhận nạn nhân bị siết cổ chết từ 07h30 sáng, tức là tiếng chuông ngân vang lúc 10h15 sáng không thể do nạn nhân giộng.",
                "Tài liệu d05 ghi nhận trên sàn gác chuông có vệt nước đọng và cơ chế chày giộng chuông bị buộc dây dù khác thường."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Bằng chứng ngoại phạm tiếp đón phật tử",
            "intro": "Các sư thầy và phật tử có mặt tại chùa đều giải trình hành tung trong buổi sáng xảy ra vụ án.",
            "prompt": "Trong các biên bản hỏi cung người có mặt tại chùa, hãy chỉ ra dòng lời khai khẳng định có mặt liên tục dưới nhà khách đón tiếp đoàn phật tử không hề lên gác chuông?",
            "answer": ["d06:003"],
            "hints": [
                "Rà soát lời khai của đệ tử trưởng phụ trách việc đón tiếp khách thập phương.",
                "Tìm câu khẳng định ngồi ăn cơm chay và thuyết pháp dưới chân núi suốt từ 09h00 đến 11h30."
            ],
            "explanation": [
                "Tại d06 dòng 003, Thích Quảng Chân khai: 'Suốt từ 09h00 đến 11h30 trưa tôi ngồi liên tục tại nhà khách dưới chân núi tiếp đón và ăn cơm chay cùng đoàn phật tử Hà Nội, khi nghe tiếng chuông chùa ngân lúc 10h15 tôi còn cùng mọi người chắp tay niệm Phật'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Vũng nước gác chuông, đòn bẩy máng nước và ống bương tre",
            "intro": "Ban chuyên án thực nghiệm cơ học trên gác chuông để giải mã nguồn gốc tiếng chuông lúc 10h15.",
            "prompt": "Ghim 3 tài liệu liên kết vết nước lạ trên gác chuông (Vòng 1) với bản giám định cơ học đòn bẩy máng nước (Vòng 3) và ảnh tang vật ống bương tre trục xoay tìm thấy sau tượng Hộ Pháp (Vòng 3).",
            "need": 3,
            "answer": ["d05", "d10", "d11"],
            "hints": [
                "Ảnh hiện trường gác chuông vũng nước và chày gỗ (ở Vòng 1).",
                "Bản giám định cơ học nguyên lý đòn bẩy nước giọt: Máng nước tre tích nước đủ nặng sẽ bập bênh kéo chày gỗ giộng vào chuông.",
                "Ảnh tang vật ống bương tre có đục lỗ điều tiết giọt nước và trục xoay giấu sau tượng Hộ Pháp."
            ],
            "explanation": [
                "Tài liệu d05 là hiện trường vết nước ban đầu.",
                "Tài liệu d10 giải mã cơ chế đồng hồ nước hẹn giờ: Nước từ máng tre rỉ từng giọt mất đúng 2 tiếng 45 phút để làm đầy ống bương làm nảy đòn bẩy kéo chày giộng chuông lúc 10h15.",
                "Tài liệu d11 chụp ống bương tre chuyên dụng dùng để chế tạo bẫy nước hẹn giờ phát ra tiếng chuông tự động."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Sợi dây thừng siết cổ và hòm công đức đúc chuông",
            "intro": "Khám xét phòng riêng của nghi phạm đã làm sáng tỏ động cơ và hung khí gây án.",
            "prompt": "Ghim 2 tài liệu chứng minh hung khí sợi dây thừng dù siết cổ nạn nhân và biên bản thu hồi bọc tiền công đức đúc chuông đồng giấu dưới đệm nằm.",
            "need": 2,
            "answer": ["d14", "d15"],
            "hints": [
                "Biên bản khám xét phòng riêng thu giữ bọc tiền mặt 120 triệu đồng quyên góp đúc đại hồng chung.",
                "Kết quả giám định sợi dây thừng siết cổ có dính xơ vải áo cà sa của Đại đức Thích Tâm Viên."
            ],
            "explanation": [
                "Tài liệu d14 ghi nhận thu hồi 120 triệu đồng tiền công đức đúc đại hồng chung do đệ tử trưởng biển thủ giấu dưới giát giường.",
                "Tài liệu d15 chứng minh sợi dây dù thu trong rương đồ chơi cơ khí của Quảng Chân có kích thước và vết máu trùng khớp với vết siết cổ sư trụ trì."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án Chùa Cổ Sơn",
            "intro": "Thủ đoạn bẫy nước hẹn giờ giộng chuông để tạo bằng chứng ngoại phạm trước đoàn phật tử đã bị lật tẩy.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, ai là thủ phạm đã sát hại sư trụ trì Thích Tâm Viên?",
            "options": [
                "Đệ tử trưởng Thích Quảng Chân do tham ô 120 triệu đồng tiền công đức đúc chuông bị sư trụ trì phát hiện và yêu cầu sám hối trục xuất, đã siết cổ sư phụ lúc 07h30 sáng rồi lắp đặt hệ thống ống bương tre nhỏ giọt nước tự động giộng chuông lúc 10h15, nhân lúc đó đang ngồi tiếp đoàn phật tử dưới chân núi để tạo bằng chứng ngoại phạm hoàn hảo.",
                "Thợ đúc đồng Bùi Văn Lực do tranh chấp tiền công đúc đại hồng chung, đã lẻn lên tịnh thất siết cổ sư trụ trì rồi trèo lên gác chuông giộng chuông báo động.",
                "Phật tử làm bếp Hoàng Thị Nga do bị khiển trách làm mất trộm gạo chay, đã cấu kết với kẻ gian bên ngoài đột nhập am thiền cướp hòm tiền công đức.",
                "Một tên trộm cổ vật đột nhập am thiền lấy cắp tượng Phật ngọc rồi kéo dây chuông đánh động để tẩu thoát."
            ],
            "answer": [0],
            "hints": [
                "Ai là người am hiểu cơ học chế tạo bẫy nước máng tre, có xơ tre trong túi áo và cất giấu 120 triệu tiền công đức đúc chuông?",
                "Đối chiếu lời khai ngoại phạm của Quảng Chân với thời gian hẹn giờ 2 tiếng 45 phút của ống bương tre."
            ],
            "explanation": [
                "Thích Quảng Chân là thủ phạm duy nhất. Tâm ma vụ lợi kết hợp sự xảo quyệt dùng bẫy nước cơ học hẹn giờ giộng chuông hòng tạo bằng chứng ngoại phạm đã bị khoa học hình sự vạch trần."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded hoi-chuong-chua-thay (5 questions)")

# 3. vet-muc-lang-dong-ho
def upgrade_dong_ho():
    path = os.path.join(ROOT, "public/cases/vet-muc-lang-dong-ho/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Bản khắc gỗ thị bị đập phá và vệt phẩm son gia truyền",
            "intro": "Bản khắc gỗ thị cổ 'Đám cưới chuột' độc bản nghìn năm của làng tranh Đông Hồ bị kẻ gian đập gãy tan tành trong đêm. Hãy phân tích các dấu vết ban đầu.",
            "prompt": "Ghim 2 tài liệu chỉ ra tình trạng bản khắc gỗ thị cổ bị đập gãy bằng chày đá và dấu vết phẩm màu son đỏ tươi gia truyền rơi vãi tại hiện trường.",
            "need": 2,
            "answer": ["d02", "d03"],
            "hints": [
                "Biên bản khám nghiệm hiện trường mô tả những nhát đập phá nát phiến gỗ thị cổ.",
                "Ảnh chụp bản khắc gỗ thị bị vỡ đôi và vệt phẩm màu đỏ son gia truyền rơi rớt trên thềm gạch."
            ],
            "explanation": [
                "Tài liệu d02 ghi nhận bản khắc gỗ thị quý bị chày đá đập vỡ vụn có chủ đích phá hủy hoa văn.",
                "Tài liệu d03 chụp cận cảnh bản khắc cổ bị gãy đôi, xung quanh vương vãi vệt phẩm son đỏ tươi."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Lời khai ngoại phạm xem chiếu phim sân đình",
            "intro": "Những người thợ khắc gỗ và con cháu trong phường tranh đều phải tường trình hoạt động buổi tối xảy ra vụ việc.",
            "prompt": "Đối chiếu lời khai của các nghệ nhân và người làng Đông Hồ, hãy chỉ ra dòng lời khai khẳng định ngồi xem chiếu phim liên tục tại sân đình từ 19h30 đến 22h00 không rời nửa bước?",
            "answer": ["d05:003"],
            "hints": [
                "Rà soát lời khai của người cháu thợ cả.",
                "Tìm câu quả quyết ngồi xem phim bãi ở sân đình suốt buổi tối không về xưởng."
            ],
            "explanation": [
                "Tại d05 dòng 003, Nguyễn Đăng Khiêm khai: 'Từ 19h30 tối đến tận 22h00 đêm tôi ngồi xem đội chiếu phim lưu động chiếu phim nhựa ở sân đình làng cùng thanh niên trong xóm, tuyệt đối không hề rời sân đình nửa bước'."
            ]
        },
        {
            "id": "q3",
            "stage": 2,
            "type": "evidence",
            "title": "Dấu vết chày đá và thói quen pha chế phẩm son",
            "intro": "Cơ quan điều tra tìm kiếm hung khí đã dùng để đập phá bản khắc gỗ thị.",
            "prompt": "Ghim 2 tài liệu liên kết vết đập dăm gỗ trên bản khắc với lời khai của thợ phụ Lê Văn Hùng nhìn thấy chiếc chày đá giã thuốc bắc bị mượn lén.",
            "need": 2,
            "answer": ["d06", "d07"],
            "hints": [
                "Lời khai của thợ cả khẳng định chiếc chày đá giã thuốc bắc ở chái bếp bị xê dịch.",
                "Lời khai của thợ phụ Hùng xác nhận thấy bóng người mang chày đá lẻn vào xưởng tranh lúc chập tối."
            ],
            "explanation": [
                "Tài liệu d06 và d07 xác định kẻ phá hoại đã dùng chiếc chày đá giã thuốc bắc của gia đình để đập vỡ bản khắc gỗ thị."
            ]
        },
        {
            "id": "q4",
            "stage": 3,
            "type": "evidence",
            "title": "Hợp đồng bán tranh giả và dăm gỗ thị dính mực son",
            "intro": "Khám xét tư trang nghi phạm đã làm sáng tỏ động cơ phá hủy di sản độc bản của dòng họ.",
            "prompt": "Ghim 2 tài liệu chứng minh việc khám xét thu giữ những mảnh dăm gỗ thị dính phẩm son trong túi quần nghi phạm và bản hợp đồng giao dịch tranh giả thu lời bất chính.",
            "need": 2,
            "answer": ["d10", "d11"],
            "hints": [
                "Ảnh chụp những mảnh dăm gỗ thị hình chóp lọng dính mực son đỏ thu trong túi áo nghi phạm.",
                "Biên bản xác minh bản hợp đồng bán 500 bức tranh in lưới giả mạo bản khắc cổ cho thương lái phố Hàng Trống."
            ],
            "explanation": [
                "Tài liệu d10 phát hiện các mảnh dăm gỗ thị văng vào túi áo của Khiêm khi dùng chày đập bản khắc.",
                "Tài liệu d11 vạch trần Khiêm đã ký hợp đồng bán tranh in lậu công nghiệp giả tranh Đông Hồ, nếu bản khắc gốc còn tồn tại thì tranh giả của y sẽ bị phát hiện ngay lập tức."
            ]
        },
        {
            "id": "q5",
            "stage": 3,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án làng tranh Đông Hồ",
            "intro": "Vết mực son, chày đá giã thuốc và bản hợp đồng tranh giả đã phơi bày toàn bộ sự thật.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, ai là người đã đập gãy bản khắc cổ 'Đám cưới chuột'?",
            "options": [
                "Nguyễn Đăng Khiêm do câu kết với thương lái phố cổ in hàng nghìn bản tranh giả mạo bản gốc để trục lợi, sợ bị ông nội dùng bản khắc cổ đối chiếu vạch trần hành vi lừa đảo, đã lén lấy chày đá đập nát bản khắc độc bản hòng triệt tiêu bằng chứng so sánh, rồi ra sân đình xem phim tạo bằng chứng ngoại phạm.",
                "Thợ phụ Lê Văn Hùng do bất cẩn làm rơi tảng đá nghiền mực đè gãy bản khắc, sợ bị đuổi việc nên đã bỏ trốn.",
                "Một thương lái tranh dân gian từ Hà Nội đột nhập xưởng tranh lấy cắp bản khắc không thành nên đập gãy phi tang.",
                "Nghệ nhân Nguyễn Đăng Thao trong lúc say rượu đã lỡ tay làm gãy bản khắc gia truyền rồi đổ tội cho con cháu."
            ],
            "answer": [0],
            "hints": [
                "Ai là người ký hợp đồng bán tranh in lậu công nghiệp, có dăm gỗ thị dính son trong túi quần và khai man giờ xem phim sân đình?",
                "Đối chiếu sự cố cúp điện sân đình lúc 20h15 vạch trần lời khai xem phim liên tục của Khiêm."
            ],
            "explanation": [
                "Nguyễn Đăng Khiêm là thủ phạm duy nhất. Lòng tham trục lợi làm hàng giả và tâm địa phá hủy bảo vật nghìn năm của cha ông đã bị chứng cứ khoa học lật tẩy."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded vet-muc-lang-dong-ho (5 questions)")

# 4. ly-tra-trao-doc
def upgrade_ly_tra():
    path = os.path.join(ROOT, "public/cases/ly-tra-trao-doc/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Độc chất xyanua trong ly trà và lỗ kim châm vi thể",
            "intro": "Một nữ điều dưỡng viên Bệnh viện Phổi Thái Bình tử vong đột ngột chỉ sau vài ngụm trà sữa tại phòng trực. Cơ quan điều tra cần xác định độc chất và đường xâm nhập.",
            "prompt": "Ghim 2 tài liệu chứng minh nạn nhân tử vong do chất kịch độc xyanua trong ly trà sữa và dấu vết lỗ kim châm vi thể trên màng nilon nắp cốc.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Kết quả giám định pháp y tử thi xác nhận nồng độ cực độc Natri Xyanua trong máu và niêm mạc dạ dày màu đỏ anh đào.",
                "Ảnh chụp macro lỗ châm kim vi thể đường kính 0.5mm bị dán đè tinh vi trên màng ép nắp cốc trà sữa."
            ],
            "explanation": [
                "Tài liệu d03 khẳng định nạn nhân chết do ngộ độc cấp xyanua với nồng độ gấp 5 lần liều gây chết người.",
                "Tài liệu d05 vạch trần chất độc không được pha từ quán mà được bơm lén bằng ống tiêm qua lỗ châm kim siêu nhỏ trên nắp cốc sau khi mua về."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Lời khai ngoại phạm của người gửi trà",
            "intro": "6 cốc trà sữa được gửi nặc danh đến Khoa Nội kèm mẩu giấy nhắn gửi chị Yến nhưng chị Yến đi vắng nên người khác uống phải.",
            "prompt": "Trong các biên bản ghi lời khai người thân của đối tượng tình nghi, hãy chỉ ra dòng lời khai của người có quan hệ tình cảm khẳng định bản thân chỉ coi nhau như anh em họ hàng và không hề biết gì về các cốc trà sữa?",
            "answer": ["d07:003"],
            "hints": [
                "Rà soát lời khai của người anh rể (chồng của chị Yến).",
                "Tìm câu khẳng định quan hệ giữa hai người hoàn toàn trong sáng như anh em ruột thịt trong nhà."
            ],
            "explanation": [
                "Tại d07 dòng 003, người anh rể khai: 'Mối quan hệ giữa tôi và cô Trang chỉ là anh rể em họ bình thường, hoàn toàn trong sáng không có gì khuất tất, tôi không hề biết ai gửi trà sữa đến cơ quan của vợ tôi'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Lỗ kim châm, mẩu giấy nhắn nặc danh và trích xuất điện thoại",
            "intro": "Phân tích kỹ thuật số điện thoại và chữ viết tay trên mẩu giấy gửi trà sữa đã lần ra kẻ chủ mưu.",
            "prompt": "Ghim 3 tài liệu liên kết dấu vết lỗ kim châm bơm độc (Vòng 1) với mẩu giấy nhắn kẹp ngoài túi trà (Vòng 3) và dữ liệu trích xuất điện thoại đặt mua chất kịch độc xyanua trên mạng (Vòng 3).",
            "need": 3,
            "answer": ["d05", "d09", "d10"],
            "hints": [
                "Ảnh macro lỗ châm kim vi thể trên nắp cốc trà sữa (ở Vòng 1).",
                "Mẩu giấy nhắn nặc danh viết tay bằng mực tím kẹp ngoài túi trà gửi đích danh cho chị họ Yến.",
                "Trích xuất dữ liệu điện thoại Cellebrite vạch trần lịch sử tìm kiếm 'chất độc không mùi không màu' và tin nhắn đặt mua 2kg Natri Xyanua."
            ],
            "explanation": [
                "Tài liệu d05 chứng minh thủ pháp bơm độc bằng ống tiêm y tế.",
                "Tài liệu d09 thể hiện mục tiêu thực sự của kẻ gửi trà là chị họ Yến (đồng nghiệp của nạn nhân xấu số).",
                "Tài liệu d10 vạch trần Lại Thị Kiều Trang đã tìm kiếm cách giết người bằng xyanua và liên hệ với đầu mối hóa chất để đặt mua độc chất."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Ống tiêm y tế và hóa đơn chuyển phát ViettelPost",
            "intro": "Lệnh khám xét khẩn cấp nơi ở của Lại Thị Kiều Trang đã thu giữ toàn bộ công cụ phương tiện phạm tội.",
            "prompt": "Ghim 2 tài liệu chứng minh vật chứng ống tiêm dùng bơm xyanua vào cốc trà và hóa đơn bưu cục chuyển phát hộp xyanua đến tay thủ phạm.",
            "need": 2,
            "answer": ["d11", "d12"],
            "hints": [
                "Ảnh tang vật ống tiêm y tế 5ml còn dính dung dịch xyanua thu giữ trong thùng rác phòng ngủ.",
                "Hóa đơn chuyển phát nhanh ViettelPost mang tên người nhận Lại Thị Kiều Trang bưu kiện chứa hóa chất công nghiệp."
            ],
            "explanation": [
                "Tài liệu d11 thu giữ chính chiếc ống tiêm y tế dùng để bơm xyanua qua màng nilon cốc trà.",
                "Tài liệu d12 xác nhận Trang đã ký nhận bưu kiện chứa chất kịch độc xyanua từ một cơ sở hóa chất tại Hà Nội chuyển về."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án ly trà tráo độc",
            "intro": "Mối quan hệ bất chính, lịch sử đặt mua xyanua và chiếc ống tiêm y tế đã khép lại kỳ án có thật chấn động Thái Bình.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, ai là thủ phạm của vụ án, bằng thủ đoạn nào và vì động cơ gì?",
            "options": [
                "Lại Thị Kiều Trang do có quan hệ bất chính với anh rể nhưng bị anh rể đòi chấm dứt, vì ghen tuông mù quáng muốn hạ độc người chị họ để được tự do qua lại với anh rể, đã đặt mua xyanua qua mạng, bơm độc vào 4 trong số 6 cốc trà sữa rồi gửi nặc danh đến Bệnh viện Phổi Thái Bình, khiến chị H. (nữ điều dưỡng vô tội) uống phải và tử vong oan uổng.",
                "Người anh rể do muốn ly hôn vợ để chiếm đoạt tài sản chung, đã câu kết với Trang mua xyanua bơm vào trà sữa gửi đến cơ quan vợ nhằm đầu độc vợ nhưng tính toán nhầm.",
                "Chủ tiệm trà sữa do bất cẩn trong khâu bảo quản chất tẩy rửa công nghiệp đã làm rò rỉ hóa chất vào các cốc trà sữa khiến khách hàng ngộ độc tử vong.",
                "Một đối tượng bệnh nhân tâm thần có mâu thuẫn với khoa Nội bệnh viện đã chặn xe giao hàng tráo đổi trà sữa tẩm xyanua để trả thù các bác sĩ."
            ],
            "answer": [0],
            "hints": [
                "Ai là người ngoại tình với anh rể, tự tay đặt mua xyanua qua mạng, viết mẩu giấy nhắn gửi chị họ và bị camera tiệm trà ghi lại?",
                "Đối chiếu dấu vết ống tiêm y tế thu trong phòng ngủ của Trang với lỗ châm kim trên nắp cốc."
            ],
            "explanation": [
                "Lại Thị Kiều Trang là thủ phạm duy nhất. Vụ án có thật tại Thái Bình năm 2019 với động cơ ghen tuông cuồng loạn và thủ đoạn tàn độc đầu độc bằng trà sữa xyanua đã cướp đi sinh mạng của một nữ điều dưỡng viên vô tội."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded ly-tra-trao-doc (5 questions)")

# 5. buc-thu-dem-tuyet-trang
def upgrade_ramsey():
    path = os.path.join(ROOT, "public/cases/buc-thu-dem-tuyet-trang/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Nguyên nhân tử vong kết hợp và nguồn gốc bức thư tống tiền",
            "intro": "Vụ án mạng hoa khôi nhí JonBenét Ramsey trong căn biệt thự đêm Giáng sinh gây chấn động toàn nước Mỹ. Hãy phân tích các dấu hiệu bất thường ban đầu.",
            "prompt": "Ghim 2 tài liệu chứng minh nguyên nhân tử vong do chấn thương sọ não kết hợp siết cổ và bằng chứng bức thư tống tiền dài 3 trang được xé từ cuốn sổ tay có sẵn trong nhà.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Kết quả giám định tử thi về vết nứt sọ dài 21cm và vòng dây thừng siết cổ garrote.",
                "Ảnh chụp bức thư tống tiền 3 trang đòi đúng 118.000 USD trùng khớp với tiền thưởng tết của người cha và vết giấy xé từ sổ tay trong bếp."
            ],
            "explanation": [
                "Tài liệu d03 xác nhận nạn nhân bị đánh vỡ hộp sọ trước rồi mới bị siết cổ bằng dây garrote.",
                "Tài liệu d05 vạch trần bức thư tống tiền dài lê thê bất thường được viết bằng bút dạ và giấy xé từ cuốn sổ tay Pad trên bàn bếp của gia đình."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Lời khai phát hiện bức thư trên bậc cầu thang",
            "intro": "Lời khai của các thành viên gia đình Ramsey có nhiều điểm mâu thuẫn về thời khắc rạng sáng ngày 26/12.",
            "prompt": "Trong biên bản hỏi cung người nhà nạn nhân, hãy chỉ ra dòng lời khai khẳng định nhìn thấy 3 trang thư trên bậc cầu thang và hoàn toàn không biết nguồn gốc bức thư từ trước?",
            "answer": ["d06:002"],
            "hints": [
                "Rà soát lời khai của người mẹ Patsy Ramsey về khoảnh khắc bước xuống cầu thang lúc 05h30 sáng.",
                "Tìm câu khẳng định nhìn thấy các trang giấy đặt ngay ngắn trên bậc thang xoắn ốc."
            ],
            "explanation": [
                "Tại d06 dòng 002, Patsy Ramsey khai: 'Lúc 05h30 sáng tôi bước xuống cầu thang xoắn ốc để xuống bếp pha cà phê thì nhìn thấy 3 trang giấy viết tay đặt ngay ngắn trên bậc thang thứ hai, tôi đọc lướt thấy đòi tiền chuộc nên hoảng loạn hét lên gọi chồng'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Bức thư 3 trang, giám định chữ viết tay và sợi len áo đỏ",
            "intro": "Cục Điều tra Liên bang FBI vào cuộc phân tích văn bản học và dấu vết vi thể.",
            "prompt": "Ghim 3 tài liệu liên kết bức thư tống tiền (Vòng 1) với kết quả giám định chữ viết tay trùng khớp hơn 24 đặc điểm với người mẹ (Vòng 3) và phân tích vi thể sợi len áo khoác đỏ dính trên băng dính dán miệng nạn nhân (Vòng 3).",
            "need": 3,
            "answer": ["d05", "d10", "d11"],
            "hints": [
                "Ảnh chụp bức thư tống tiền 3 trang (ở Vòng 1).",
                "Báo cáo giám định chữ viết tay của các chuyên gia FBI kết luận người mẹ Patsy Ramsey có độ tương đồng chữ viết cao nhất.",
                "Ảnh phân tích sợi dệt vi thể xác định sợi len màu đỏ dính trên mép băng keo dán miệng nạn nhân trùng khớp với sợi áo khoác len Patsy mặc đêm Giáng sinh."
            ],
            "explanation": [
                "Tài liệu d05 là vật chứng bức thư tống tiền ban đầu.",
                "Tài liệu d10 khẳng định nét chữ nắn nót, cách ngắt dòng và các chữ cái 'a', 'q', 'd' trùng khớp hoàn toàn với mẫu chữ viết tay của Patsy Ramsey.",
                "Tài liệu d11 chứng minh sợi len từ áo khoác đỏ của người mẹ đã rơi rụng và dính chặt vào lớp keo dán miệng nạn nhân trong quá trình dàn dựng hiện trường."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Cửa sổ tầng hầm nguyên tuyết và que cọ vẽ tự chế",
            "intro": "Khám nghiệm lối đột nhập tầng hầm và hung khí tự chế đã chứng minh kẻ gây án là người trong nhà.",
            "prompt": "Ghim 2 tài liệu chỉ ra sơ đồ hiện trường lớp tuyết trắng quanh cửa sổ tầng hầm hoàn toàn nguyên vẹn không có dấu chân kẻ đột nhập và hung khí dây thừng garrote tự chế từ thân que cọ vẽ của người mẹ.",
            "need": 2,
            "answer": ["d04", "d12"],
            "hints": [
                "Sơ đồ mặt bằng biệt thự và báo cáo trinh sát xác nhận tuyết bao phủ kín quanh nhà, cửa sổ tầng hầm đóng chặt không có vết chân trên tuyết.",
                "Biên bản giám định hung khí dây garrote xác nhận cán xoay được bẻ từ chiếc cọ vẽ lông thú trong hộp màu vẽ của Patsy Ramsey."
            ],
            "explanation": [
                "Tài liệu d04 bác bỏ hoàn toàn giả thuyết kẻ lạ đột nhập từ ngoài vào vì tuyết trắng quanh biệt thự nguyên vẹn không một dấu chân.",
                "Tài liệu d12 chứng minh hung khí siết cổ garrote được chế tạo ngay tại chỗ bằng que cọ vẽ lấy từ hộp họa cụ của người mẹ trong tầng hầm."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện kỳ án JonBenét Ramsey",
            "intro": "Lớp tuyết trắng nguyên vẹn, nét chữ trong bức thư và sợi len áo khoác đỏ đã hé lộ bản chất thực sự của vụ án.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, chuỗi chứng cứ nào vạch trần vụ án là một màn kịch dàn dựng bắt cóc giả mạo (Staging) từ nội bộ ngôi nhà?",
            "options": [
                "Hiện trường không hề có kẻ lạ đột nhập từ ngoài vào vì tuyết trắng nguyên vẹn; bức thư tống tiền 3 trang thực chất do người mẹ Patsy Ramsey viết bằng giấy bút trong nhà với số tiền đòi chuộc đúng bằng tiền thưởng tết của chồng; sợi len áo khoác đỏ của bà dính trên băng dính dán miệng và hung khí dây garrote làm từ chính que cọ vẽ trong tầng hầm, chứng minh gia đình đã dàn dựng màn kịch bắt cóc giả mạo để che đậy một tai nạn chấn thương sọ não nội bộ.",
                "Một kẻ ấu dâm biến thái đột nhập qua cửa sổ tầng hầm trong lúc tuyết ngừng rơi, dùng que cọ vẽ chế tạo dây garrote sát hại JonBenét rồi sao chép chữ viết của Patsy Ramsey để đánh lạc hướng cảnh sát.",
                "Nhóm khủng bố ngoại quốc cánh tả 'Small Foreign Faction' đã bắt cóc tống tiền gia đình Ramsey nhưng do nạn nhân la hét nên đã sát hại rồi để lại bức thư tống tiền đòi 118.000 USD.",
                "Người giúp việc Linda Hoffmann do túng thiếu nợ nần đã đột nhập tầng hầm ban đêm sát hại JonBenét rồi vu oan cho bà chủ bằng cách dùng que cọ vẽ và sổ tay trong bếp."
            ],
            "answer": [0],
            "hints": [
                "Tại sao kẻ bắt cóc tống tiền lại viết thư dài 3 trang bằng giấy bút trong nhà, đòi đúng 118.000 USD và để lại xác nạn nhân ngay trong tầng hầm?",
                "Đối chiếu lớp tuyết phủ nguyên vẹn không dấu chân và sợi len áo đỏ của người mẹ dính trên băng dính."
            ],
            "explanation": [
                "Phương án 1 là kết luận chính xác nhất được toàn bộ các chuyên gia hình sự và nhà phân tích FBI đồng thuận: Đây là vụ dàn dựng hiện trường (Crime Scene Staging) kinh điển nhất thế kỷ 20 nhằm bảo vệ thành viên gia đình sau một bi kịch tai nạn nội bộ."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded buc-thu-dem-tuyet-trang (5 questions)")

# 6. quai-vat-21-khuon-mat
def upgrade_quai_vat():
    path = os.path.join(ROOT, "public/cases/quai-vat-21-khuon-mat/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Chất kịch độc trong hộp kẹo và bức thư máy đánh chữ sứt mẻ",
            "intro": "Bóng ma bí ẩn 'Quái vật 21 khuôn mặt' reo rắc kinh hoàng lên toàn nước Nhật năm 1984. Hãy xác định độc chất và phương thức khiêu khích truyền thông.",
            "prompt": "Ghim 2 tài liệu chứng minh chất độc kali xyanua liều lượng gây chết người trong các hộp kẹo trẻ em và bức thư khiêu khích cảnh sát đánh máy có khuyết tật cơ học đặc thù.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Báo cáo hóa nghiệm độc chất của Viện Khoa học Hình sự Osaka phát hiện Kali Xyanua tinh khiết 98% nồng độ 80mg/viên.",
                "Ảnh chụp bức thư nặc danh đánh máy bằng máy cơ có ký tự chữ 'ka' bị mẻ khuyết độc nhất gửi tòa soạn báo Mainichi."
            ],
            "explanation": [
                "Tài liệu d03 xác nhận chất độc là Kali Xyanua cực độc có thể giết chết người lớn trong vài phút.",
                "Tài liệu d05 chụp bức thư đánh máy gửi truyền thông mang con dấu đỏ 'Kaijin 21 Mensō'."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Thiệt hại tài chính và cổ phiếu lao dốc",
            "intro": "Các tập đoàn bánh kẹo hàng đầu Nhật Bản đứng trước bờ vực phá sản vì làn sóng khủng bố độc dược.",
            "prompt": "Trong biên bản làm việc với lãnh đạo các tập đoàn bánh kẹo, hãy chỉ ra dòng lời khai mô tả thiệt hại tài chính tàn khốc khiến cổ phiếu trên sàn giao dịch Tokyo lao dốc gần 50% chỉ trong hai tuần?",
            "answer": ["d06:004"],
            "hints": [
                "Rà soát lời khai của Giám đốc điều hành tập đoàn Morinaga.",
                "Tìm câu mô tả giá cổ phiếu sụt giảm nghiêm trọng và hàng triệu hộp bánh kẹo bị thu hồi."
            ],
            "explanation": [
                "Tại d06 dòng 004, Giám đốc điều hành Morinaga mô tả: 'Giá cổ phiếu của chúng tôi trên sàn giao dịch Tokyo đã tụt dốc gần 50% chỉ trong hai tuần, thiệt hại tài chính và chi phí thu hồi sản phẩm lên tới hàng chục tỷ Yên, công ty đứng trước nguy cơ phá sản'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Vết sứt máy Panwriter, keo dán PUR-82 và danh sách nghi vấn",
            "intro": "Cảnh sát Quốc gia Nhật Bản lần theo các dấu vết kỹ thuật độc nhất của kẻ chủ mưu.",
            "prompt": "Ghim 3 tài liệu liên kết bức thư khiêu khích ban đầu (Vòng 1) với báo cáo giám định vi thể vết mẻ phím chữ 'ka' trên máy đánh chữ Panwriter (Vòng 3) và ảnh chụp vi thể keo nhiệt công nghiệp PUR-82 dán lại đáy hộp kẹo (Vòng 3).",
            "need": 3,
            "answer": ["d05", "d10", "d11"],
            "hints": [
                "Ảnh bức thư khiêu khích cảnh sát đánh máy bằng máy cơ học (ở Vòng 1).",
                "Báo cáo giám định vết mẻ 0.3mm trên phím chữ 'ka' của chiếc máy đánh chữ Panwriter đời 1978.",
                "Ảnh chụp vi thể mép dán keo nhiệt polyurethane PUR-82 dính sợi len xám chứng minh hộp kẹo bị cạy đáy tẩm độc rồi dán lại tinh vi."
            ],
            "explanation": [
                "Tài liệu d05 là vật chứng bức thư tống tiền ban đầu.",
                "Tài liệu d10 khẳng định toàn bộ các bức thư gửi cảnh sát đều được gõ ra từ đúng một chiếc máy đánh chữ Panwriter có phím 'ka' bị sứt mẻ độc nhất vô nhị.",
                "Tài liệu d11 chứng minh kẻ chủ mưu sở hữu súng bắn keo nhiệt công nghiệp PUR-82 dùng trong ngành đóng gói bao bì ở khu vực cảng Kobe."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Quang phổ âm thanh cassette, phục kích Shinkansen và cổ phiếu bán khống",
            "intro": "Các cuộc giao tiền chuộc diễn ra nghẹt thở dọc tuyến đường sắt cao tốc Shinkansen.",
            "prompt": "Ghim 3 tài liệu liên kết bản phân tích quang phổ giọng đọc trẻ con trong băng cassette (Vòng 3) với báo cáo phục kích bắt hụt Người đàn ông mắt cáo tại ga Kyoto (Vòng 4) và biểu đồ thao túng bán khống cổ phiếu thu lợi hơn 1,2 tỷ Yên (Vòng 4).",
            "need": 3,
            "answer": ["d13", "d14", "d15"],
            "hints": [
                "Phân tích quang phổ âm thanh băng cassette ghi âm giọng đọc của một bé gái chỉ dẫn địa điểm ném tiền trên tàu (ở Vòng 3).",
                "Báo cáo cuộc phục kích bắt hụt Người đàn ông mắt cáo ngồi ghế 14B toa số 7 tàu Shinkansen Hikari biến mất tại ga Kyoto.",
                "Biểu đồ tài chính của Ủy ban Giám sát Chứng khoán vạch trần các đợt bán khống gom đáy cổ phiếu thu lợi hơn 1,2 tỷ Yên."
            ],
            "explanation": [
                "Tài liệu d13 cho thấy hung thủ dùng giọng trẻ con để tránh bị máy nhận diện giọng nói phân tích.",
                "Tài liệu d14 ghi lại hình ảnh nhân dạng đối tượng then chốt 'Người đàn ông mắt cáo' trong chiến dịch phục kích.",
                "Tài liệu d15 vạch trần bản chất thật sự: Các vụ tẩm độc kẹo chỉ là đòn hỏa mù nhằm làm sụp đổ giá cổ phiếu trên sàn TSE để các tài khoản ngầm kiếm lời khổng lồ từ nghiệp vụ bán khống."
            ]
        },
        {
            "id": "q5",
            "stage": 5,
            "type": "evidence",
            "title": "Bức thư đình chiến lịch sử và bài học quy chuẩn bao bì",
            "intro": "Sau 17 tháng gieo rắc ác mộng, Quái vật 21 khuôn mặt gửi bức thư cuối cùng chấn động lịch sử tư pháp.",
            "prompt": "Ghim 2 tài liệu lưu trữ bức thư đình chiến ngày 12/08/1985 tuyên bố chấm dứt chiến dịch tống tiền và tài liệu đúc kết bài học lịch sử về quy chuẩn bao bì đóng gói chống cạy mở.",
            "need": 2,
            "answer": ["d18", "d20"],
            "hints": [
                "Bản scan bức thư đình chiến của Quái vật 21 khuôn mặt gửi lời chia buồn trước cái chết của Cảnh sát trưởng Yamamoto và tuyên bố buông tha các hãng bánh kẹo.",
                "Ghi chép bài học lịch sử về việc thay đổi toàn bộ quy chuẩn bao bì niêm phong chống cạy mở (Tamper-evident) của ngành thực phẩm toàn cầu."
            ],
            "explanation": [
                "Tài liệu d18 là bức thư chia tay lịch sử ngày 12/08/1985 chấm dứt hoàn toàn vụ án Glico Morinaga.",
                "Tài liệu d20 tổng kết tác động làm thay đổi vĩnh viễn ngành công nghiệp thực phẩm thế giới sang bao bì niêm phong khóa nhiệt không thể can thiệp."
            ]
        },
        {
            "id": "q6",
            "stage": 5,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện kỳ án Quái vật 21 khuôn mặt",
            "intro": "Vụ án thế kỷ không lời giải của Cảnh sát Nhật Bản đã để lại những bài học sâu sắc về tội phạm kinh tế công nghệ cao.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, động cơ cốt lõi thực sự của tổ chức Quái vật 21 khuôn mặt đằng sau các vụ đầu độc bánh kẹo là gì?",
            "options": [
                "Khủng bố tâm lý và thao túng thị trường tài chính: Lợi dụng sự hoảng loạn của công chúng để đánh sập giá cổ phiếu các tập đoàn bánh kẹo khổng lồ trên Sàn giao dịch chứng khoán Tokyo (TSE), từ đó các tài khoản ngầm cấu kết với thế lực Yakuza thực hiện các lệnh bán khống gom đáy thu lợi nhuận bất chính hơn 1,2 tỷ Yên.",
                "Một cựu nhân viên bị sa thải khỏi tập đoàn Glico nuôi mối thù hận cá nhân nên đã tẩm độc kẹo để trả thù ban giám đốc và phá hoại thương hiệu.",
                "Một tổ chức tội phạm quốc tế muốn tống tiền 1 tỷ Yên tiền mặt của chính phủ Nhật Bản để tài trợ cho các hoạt động chính trị cực đoan.",
                "Một nhóm thanh thiếu niên cuồng tín truyện trinh thám bắt chước nhân vật Quái vật 21 mặt của nhà văn Edogawa Ranpo để trêu ngươi cảnh sát mà không vì mục đích tiền bạc."
            ],
            "answer": [0],
            "hints": [
                "Hãy nhìn vào dòng tiền: Tại sao bọn chúng liên tục đòi tiền chuộc nhưng không bao giờ đến lấy tiền thật sự ở các điểm hẹn?",
                "Đối chiếu biểu đồ biến động giá cổ phiếu và khối lượng bán khống bất thường trên sàn chứng khoán Tokyo trong tài liệu d15."
            ],
            "explanation": [
                "Phương án 1 là kết luận chính xác nhất của Cục Cảnh sát Quốc gia Nhật Bản: Quái vật 21 khuôn mặt thực chất là một tổ chức tội phạm kinh tế cực kỳ tinh vi. Tiền tống tiền chỉ là đòn nghi binh, nguồn tiền khổng lồ thực sự chúng kiếm được là từ việc thao túng bán khống cổ phiếu trên sàn chứng khoán."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded quai-vat-21-khuon-mat (6 questions)")

if __name__ == "__main__":
    upgrade_van_don()
    upgrade_chua_thay()
    upgrade_dong_ho()
    upgrade_ly_tra()
    upgrade_ramsey()
    upgrade_quai_vat()
