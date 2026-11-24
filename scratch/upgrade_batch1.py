#!/usr/bin/env python3
import json
import os

ROOT = "/Users/huynguyen/Documents/game_pha_an"

# 1. demo-01
def upgrade_demo01():
    path = os.path.join(ROOT, "public/cases/demo-01/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
    
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Hiện trường vụ trộm có dấu hiệu dàn dựng",
            "intro": "Ngôi nhà của nhà sưu tầm đồng hồ cổ bị xáo trộn và mất chiếc đồng hồ quý. Hãy kiểm tra hiện trường ban đầu để tìm ra bằng chứng chứng minh vụ trộm không phải do kẻ lạ đột nhập.",
            "prompt": "Ghim 2 tài liệu chứng minh vụ trộm không có dấu hiệu cạy phá từ bên ngoài mà do người quen biết rõ thói quen trong nhà thực hiện.",
            "need": 2,
            "answer": ["d02", "d03"],
            "hints": [
                "Xem kỹ biên bản khám nghiệm hiện trường về tình trạng then cài cửa sổ.",
                "Đối chiếu với lời khai của người giúp việc về việc khóa cửa và phản ứng của con chó."
            ],
            "explanation": [
                "Biên bản d02 ghi nhận cửa sổ tầng 1 mở toang nhưng then cài không bị cạy phá, bụi trên bậu cửa không có dấu vết bám víu leo trèo.",
                "Lời khai d03 cho biết con chó béc-giê không hề sủa và cửa ngách vẫn khóa nguyên vẹn, chứng tỏ kẻ lấy đồng hồ là người quen trong nhà."
            ],
            "nudges": [
                {
                    "picks": ["d01", "d04"],
                    "message": "Báo chí và lời khai của Minh chưa cung cấp căn cứ kỹ thuật về hiện trường dàn dựng."
                }
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Lời khai ngoại phạm bị bác bỏ",
            "intro": "Cơ quan điều tra thu thập được dữ liệu camera an ninh đầu ngõ và hóa đơn thanh toán quán cà phê gần đó.",
            "prompt": "Đối chiếu lời khai của những người thân cận với dữ liệu camera và hóa đơn giờ giấc ở đầu ngõ, hãy chỉ ra dòng lời khai cung cấp bằng chứng ngoại phạm nhưng thực tế đã bị mốc thời gian vạch trần là dối trá?",
            "answer": ["d04:004"],
            "hints": [
                "Rà soát lời khai của các đối tượng để tìm người tự nhận có mặt ở quán cà phê suốt buổi tối.",
                "Đối chiếu giờ giấc ghi trên hóa đơn quán cà phê và hình ảnh camera ghi nhận xe máy rời ngõ."
            ],
            "explanation": [
                "Tại d04 dòng 004, Nguyễn Quang Minh khai: 'Khoảng 19h30 cháu ra quán cà phê Gác Nhỏ đầu ngõ ngồi với bạn đến tận 21h30 mới về, suốt thời gian đó cháu không đi đâu cả.'",
                "Tuy nhiên, hóa đơn d06 ghi nhận Minh thanh toán lúc 20h15 và camera d07 ghi nhận Minh rời ngõ lúc 20h05."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Chuỗi bằng chứng vật chất tẩu tán tang vật",
            "intro": "Khám xét tiệm cầm đồ Phát Đạt đã thu giữ được tài sản bị đánh cắp cùng giấy biên nhận mang tên người cầm cố.",
            "prompt": "Ghim 3 tài liệu liên kết thời điểm đối tượng rời khỏi ngõ với hình ảnh nhận dạng phương tiện và phiếu cầm đồ thu giữ chiếc đồng hồ quý.",
            "need": 3,
            "answer": ["d06", "d07", "d08"],
            "hints": [
                "Hóa đơn cà phê ghi nhận đối tượng rời quán sớm hơn lời khai.",
                "Hình ảnh camera ghi nhận đối tượng phóng xe máy rời ngõ lúc 20h05.",
                "Phiếu cầm đồ mang tên đối tượng thu giữ chiếc đồng hồ Omega Seamaster vàng đúc."
            ],
            "explanation": [
                "Hóa đơn d06 chứng minh Minh chỉ ở quán cà phê một lúc rồi rời đi.",
                "Camera d07 ghi lại hình ảnh Minh đi xe máy Dream mang túi xách rời ngõ lúc 20h05.",
                "Phiếu cầm đồ d08 thể hiện Nguyễn Quang Minh đã cầm cố chiếc Omega Seamaster lấy 15 triệu đồng vào hồi 20h30 cùng đêm."
            ]
        },
        {
            "id": "q4",
            "stage": 3,
            "type": "choice",
            "title": "Bản kết luận điều tra vụ trộm đồng hồ cổ",
            "intro": "Toàn bộ tài liệu chứng cứ từ hiện trường dàn dựng, camera an ninh và phiếu cầm đồ đã chỉ rõ kẻ thủ ác.",
            "prompt": "Dựa trên toàn bộ tài liệu hồ sơ, ai là kẻ đã lấy cắp chiếc đồng hồ Omega Seamaster của ông Vĩnh, bằng thủ đoạn nào và vì động cơ gì?",
            "options": [
                "Nguyễn Quang Minh do nợ nần cờ bạc, đã nhân lúc ông Vĩnh uống thuốc ngủ để lấy trộm đồng hồ, mở then cửa sổ tạo hiện trường giả rồi đi xe máy đem đến tiệm Phát Đạt cầm cố 15 triệu đồng trước khi vào quán cà phê tạo bằng chứng ngoại phạm.",
                "Bà Phạm Thị Tư do túng thiếu tiền chữa bệnh cho con, đã thông đồng với kẻ trộm mở then cửa sổ từ bên trong rồi giấu đồng hồ vào giỏ đi chợ đem đi cầm cố.",
                "Ông Lâm Văn Hoà trong lúc đến chơi cờ đã nhân lúc ông Vĩnh ngủ say tháo trộm đồng hồ giấu vào túi áo rồi đem cầm cố tiệm Phát Đạt.",
                "Một tên trộm chuyên nghiệp trèo qua ban công cạy cửa sổ đột nhập lấy đồng hồ rồi làm rơi giấy tờ tùy thân của Minh tại tiệm cầm đồ."
            ],
            "answer": [0],
            "hints": [
                "Đối tượng nào có mặt trong nhà, biết rõ vị trí tủ kính, có mâu thuẫn thời gian biểu và có tên trên phiếu cầm đồ?"
            ],
            "explanation": [
                "Nguyễn Quang Minh là thủ phạm duy nhất. Y dàn dựng hiện trường cậy cửa sổ nhưng con chó không sủa, giả mạo bằng chứng ngoại phạm ở quán cà phê và đã cầm cố đồng hồ lấy tiền tiêu xài."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded demo-01 (4 questions)")

# 2. con-nuoc-ram-thang-gieng
def upgrade_con_nuoc():
    path = os.path.join(ROOT, "public/cases/con-nuoc-ram-thang-gieng/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "choice",
            "title": "Tai nạn rò nước hay án mạng có chủ đích?",
            "intro": "Dư luận xóm đò đồn ông Bảy Kiên say rượu rồi ngủ quên khiến ghe rò nước chìm nghỉm. Hãy phân tích các dấu hiệu tại hiện trường khoang ghe để xác định tính chất vụ việc.",
            "prompt": "Dựa vào các biên bản hiện trường và giám định tử thi ban đầu, nhận định nào sau đây là chính xác nhất về nguyên nhân cái chết?",
            "options": [
                "Đây là vụ tai nạn đắm ghe ngẫu nhiên do vỏ ghe gỗ lâu năm bị bục thủng đường xảm khiến nước sông tràn vào lúc nạn nhân say rượu ngủ say.",
                "Đây là một vụ án mạng được chuẩn bị kỹ lưỡng: Nắp khoang bị gài then sắt từ bên ngoài và van lù đáy ghe bị cố ý tháo mở khi nạn nhân bị chuốc say.",
                "Nạn nhân tự sát bằng cách uống thuốc độc trong ve rượu rồi chui vào khoang ghe cài chốt bên trong để tự dìm mình dưới lòng sông.",
                "Nạn nhân bị ngạt khí độc CO tích tụ trong hầm máy đò do động cơ diesel bị rò rỉ khí thải trước khi nước sông tràn vào."
            ],
            "answer": [1],
            "hints": [
                "Kiểm tra ảnh chụp then cài nắp khoang và tình trạng van lù đáy ghe.",
                "Đối chiếu nồng độ cồn và độc chất trong dịch dạ dày nạn nhân."
            ],
            "explanation": [
                "Khám nghiệm d02 và d03 cho thấy nắp khoang bị gài then sắt từ bên ngoài khiến nạn nhân không thể thoát thân; pháp y d05 xác định nạn nhân chết ngạt nước trong tình trạng mê man."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "evidence",
            "title": "Cơ chế nước tràn vào khoang và quy luật con nước",
            "intro": "Hung thủ không thể đứng bơm nước vào ghe giữa ban ngày. Cơ chế xả nước phải dựa vào quy luật thủy văn sông Hàm Luông.",
            "prompt": "Ghim 3 tài liệu chứng minh nạn nhân chết ngạt nước do van lù đáy ghe bị can thiệp cơ học có chủ đích trùng khớp với thời điểm đỉnh triều cường con nước Rằm.",
            "need": 3,
            "answer": ["d05", "d09", "d10"],
            "hints": [
                "Tìm tài liệu pháp y xác nhận nạn nhân tử vong do ngạt nước trong khoang (ở Vòng 1).",
                "Tìm biên bản giám định kỹ thuật phương tiện thủy về dấu vết kìm tác động vào van lù.",
                "Tìm bản tin thông số thủy văn về thời điểm mực nước triều dâng cao nhất đêm Rằm."
            ],
            "explanation": [
                "Tài liệu d05 (ở Vòng 1) kết luận tử vong do ngạt nước ngọt lòng sông.",
                "Tài liệu d09 chỉ ra van xả lù bị vặn mở 3 vòng bằng dụng cụ cơ khí có vết xước mới.",
                "Tài liệu d10 ghi nhận con nước Rằm đạt đỉnh triều lúc 01h30 sáng, thời điểm áp lực nước ép qua van lù mạnh nhất làm chìm ghe trong 20 phút."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "line",
            "title": "Mâu thuẫn với quy luật con nước ròng",
            "intro": "Các nhân chứng và người qua lại khúc sông đêm đó đều được lấy lời khai về thời gian di chuyển.",
            "prompt": "Đối chiếu lời khai của các chủ phương tiện đường thủy với diễn biến mực nước sông Hàm Luông đêm hôm đó, hãy chỉ ra dòng lời khai nại ra lý do dừng đò mâu thuẫn trực tiếp với quy luật con nước ròng?",
            "answer": ["d16:007"],
            "hints": [
                "Rà soát lời khai của người lái đò đêm về lý do neo ghe tại bến sông Tân Mỹ.",
                "Đối chiếu giờ nước lớn, nước ròng với lời khai 'phải chờ nước xuôi'."
            ],
            "explanation": [
                "Tại d16 dòng 007, Trần Văn Thuyền khai phải neo đò chờ con nước xuôi lúc nửa đêm, trong khi trạm thủy văn d10 xác nhận thời điểm đó nước đang triều dâng cực đại (nước lớn) chứ không phải nước ròng."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Màn kịch đứt dây curoa ngụy tạo bằng chứng ngoại phạm",
            "intro": "Người lái đò khẳng định máy hỏng do đứt dây curoa nên không thể di chuyển trong đêm.",
            "prompt": "Ghim 3 tài liệu chứng minh câu chuyện 'đứt dây curoa máy đò' là sự bịa đặt được chuẩn bị từ trước thông qua sổ nhật ký thu tiền, hóa đơn mua phụ tùng và lời khai của thợ máy.",
            "need": 3,
            "answer": ["d17", "d21", "d22"],
            "hints": [
                "Sổ nhật ký đò ghi chép giờ giấc máy hỏng bất thường.",
                "Hóa đơn tiệm Hai Nhựt chứng minh việc mua sẵn dây curoa cũ bị cắt khía.",
                "Lời khai thợ máy khẳng định dây curoa trên đò không hề đứt tự nhiên."
            ],
            "explanation": [
                "Tài liệu d17 ghi nhận Thuyền ghi sẵn lý do hỏng máy vào sổ từ chập tối.",
                "Tài liệu d21 và d22 vạch trần Thuyền đã mua dây curoa cũ về dùng dao khía mép nhằm tạo cớ máy đò chết máy nằm chờ nạn nhân."
            ]
        },
        {
            "id": "q5",
            "stage": 5,
            "type": "evidence",
            "title": "Động cơ chiếm đoạt và vật chứng chòi canh đò",
            "intro": "Khám xét nơi ở của nghi phạm và tài liệu tại xưởng ghe đã làm sáng tỏ động cơ giết người.",
            "prompt": "Ghim 2 tài liệu chứng minh động cơ kinh tế sâu xa dẫn đến vụ mưu sát và tang vật sợi cước/kìm mỏ lết thu giữ tại nơi ở của kẻ thủ ác.",
            "need": 2,
            "answer": ["d24", "d26"],
            "hints": [
                "Tìm giấy tờ thế chấp vay mượn đất đai tìm thấy trong két sắt nạn nhân.",
                "Tìm biên bản khám xét chòi canh đò phát hiện kìm mỏ lết dính mỡ và cuộn cước cùng kích thước."
            ],
            "explanation": [
                "Tài liệu d24 là giấy vay nợ thế chấp đất hương hỏa sắp đến hạn xiết nợ của Thuyền với ông Bảy Kiên.",
                "Tài liệu d26 ghi nhận thu giữ chiếc kìm mỏ lết có vết xước kim loại trùng khớp với vết răng trên van lù d09 và cuộn cước câu cá trùng khớp với nút thòng lọng d11."
            ]
        },
        {
            "id": "q6",
            "stage": 5,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án bến sông Tân Mỹ",
            "intro": "Toàn bộ chuỗi bằng chứng từ van lù, con nước Rằm, dây curoa giả mạo đến giấy nợ đất đai đã khép lại hồ sơ.",
            "prompt": "Dựa trên toàn bộ hồ sơ, hãy chỉ ra kết luận điều tra toàn diện và chính xác nhất về vụ án:",
            "options": [
                "Trần Văn Thuyền do nợ tiền đất hương hỏa không có khả năng trả, đã chuốc thuốc mê ông Bảy Kiên vào ve rượu thuốc, nhốt nạn nhân vào khoang ghe cài then ngoài, dùng kìm mở van lù lợi dụng con nước Rằm dâng cao dìm chết nạn nhân, đồng thời ngụy tạo cớ đứt dây curoa đò để tạo bằng chứng ngoại phạm.",
                "Đoàn Văn Lợi do tranh chấp hợp đồng đóng ghe Phước Hải 09, đã lén mở van lù lúc nửa đêm rồi vu khống cho Ba Thuyền bằng cách giấu kìm vào chòi đò.",
                "Võ Quốc Hưng do thua cá độ đá gà túng quẫn, đã đột nhập ghe cướp tài sản rồi gài then sắt nhốt ông Bảy Kiên dưới khoang nước.",
                "Lê Văn Sáu (Sáu Cà Na) uống rượu say tại quán Năm Cua, trong lúc xô xát đã đẩy nạn nhân ngã xuống khoang ghe rồi bỏ trốn."
            ],
            "answer": [0],
            "hints": [
                "Ai vừa có động cơ nợ đất đai, vừa sở hữu kìm mở van lù, vừa ngụy tạo hỏng máy đò theo con nước Rằm?"
            ],
            "explanation": [
                "Trần Văn Thuyền là thủ phạm duy nhất. Y lên kế hoạch chi tiết từ việc mua dây curoa khía sẵn, chuốc thuốc mê, tính toán con nước Rằm và mở van lù để dìm chết chủ nợ hòng xóa khoản nợ thế chấp đất hương hỏa."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded con-nuoc-ram-thang-gieng (6 questions)")

# 3. mua-dong-binh-ty
def upgrade_mua_dong():
    path = os.path.join(ROOT, "public/cases/mua-dong-binh-ty/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Hiện trường căn hộ khép kín và dấu hiệu tử vong",
            "intro": "Bà Chu Thị Bích được phát hiện tử vong tại căn hộ 204 khu tập thể Dệt Thống Nhất trong đêm đông giá rét. Hãy kiểm tra các dấu vết vật lý ban đầu.",
            "prompt": "Ghim 2 tài liệu phản ánh tình trạng hiện trường căn hộ bị khóa chốt bên trong và biểu hiện tử vong do ngạt thở co thắt phế quản cấp tính của nạn nhân.",
            "need": 2,
            "answer": ["d02", "d04"],
            "hints": [
                "Biên bản khám nghiệm hiện trường mô tả tình trạng chốt khóa cửa căn hộ 204.",
                "Ảnh chụp hiện trường phòng ngủ nơi bình xịt hen suyễn rơi dưới chân giường."
            ],
            "explanation": [
                "Tài liệu d02 ghi nhận cửa căn hộ cài then chốt bên trong, hàng xóm phải phá cửa mới vào được.",
                "Tài liệu d04 ghi lại tư thế nạn nhân ngã quỵ bên giường, tay với về phía bình xịt hen suyễn bị rơi."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Bằng chứng ngoại phạm mâu thuẫn tiếng còi tàu",
            "intro": "Các đối tượng có liên quan đều đưa ra lời khai về vị trí của mình trong buổi tối xảy ra sự việc.",
            "prompt": "Trong các biên bản hỏi cung người có liên quan tại khu tập thể Dệt Thống Nhất, hãy chỉ ra dòng lời khai đưa ra bằng chứng ngoại phạm nhưng thực tế đã bị tiếng còi đoàn tàu hàng đêm lúc 21h15 vạch trần là bịa đặt?",
            "answer": ["d08:004"],
            "hints": [
                "Rà soát lời khai của các nghi phạm để tìm người nại ra việc ngồi uống trà xem ti vi suốt buổi tối.",
                "Đối chiếu với lời khai của hàng xóm và nhân chứng về tiếng còi tàu hỏa chạy qua khu tập thể."
            ],
            "explanation": [
                "Tại d08 dòng 004, Triệu Quốc Hùng khai: 'Khoảng 21h00 tôi sang nhà tổ trưởng dân phố uống nước chè đàm đạo đến tận 22h30 mới về phòng, suốt lúc đó hai bác cháu ngồi nói chuyện không ngắt quãng'. Lời khai này mâu thuẫn với việc ông tổ trưởng xác nhận Hùng chỉ đến sau 21h45."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Vạch trần thủ đoạn tráo đổi bình xịt hen suyễn",
            "intro": "Cơ quan điều tra nghi ngờ cơn hen suyễn kịch phát dẫn đến tử vong không phải là ngẫu nhiên.",
            "prompt": "Ghim 3 tài liệu liên kết vật chứng bình xịt rơi tại hiện trường (Vòng 1), kết luận tử thi không có ngoại lực siết cổ (Vòng 2) và kết quả phân tích độc chất dung dịch bị tráo đổi (Vòng 3).",
            "need": 3,
            "answer": ["d04", "d06", "d12"],
            "hints": [
                "Ảnh hiện trường bình xịt Salbutamol rơi dưới chân giường (ở Vòng 1).",
                "Biên bản giám định cơ học tử thi: nạn nhân chết ngạt do co thắt khí quản chứ không có ngoại lực chấn thương.",
                "Phiếu giám định dược chất vạch trần dung dịch trong bình xịt bị tráo bằng cồn và nước muối làm kích ứng co thắt phế quản."
            ],
            "explanation": [
                "Tài liệu d04 chụp chiếc bình xịt Salbutamol nạn nhân cầm trước khi chết.",
                "Tài liệu d06 khẳng định khí quản co thắt dữ dội mà không có dấu vết chẹt cổ hay ức chế cơ học bên ngoài.",
                "Tài liệu d12 kết luận thuốc giãn phế quản Salbutamol đã bị tráo bằng dung dịch cồn nồng độ cao pha muối, khi xịt vào họng sẽ lập tức kích thích co thắt thanh quản làm nạn nhân ngạt thở ngay tức khắc."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Dấu vết hiện trường và tang vật vàng lá cướp được",
            "intro": "Lệnh khám xét khẩn cấp nơi ở của nghi phạm đã làm sáng tỏ hành vi giết người cướp của.",
            "prompt": "Ghim 2 tài liệu chứng minh sự hiện diện của thủ phạm tại hiện trường thông qua dấu vết đôi dép rọ bộ đội và số vàng lá 9999 cướp được đem chôn giấu.",
            "need": 2,
            "answer": ["d16", "d17"],
            "hints": [
                "Ảnh tang vật đôi dép rọ bộ đội có đế mòn dính bùn đất trùng khớp vết trượt tại ban công.",
                "Biên bản thu giữ các chỉ vàng lá 9999 giấu trong hũ sành chôn dưới gốc chuối sau nhà."
            ],
            "explanation": [
                "Tài liệu d16 đối chiếu vết mòn hoa đế dép rọ của Hùng trùng khớp hoàn toàn với vết giẫm trên bậu cửa sổ ban công d02.",
                "Tài liệu d17 ghi nhận đào bới thu hồi 12 chỉ vàng lá 9999 bọc giấy báo cũ mang tên bà Bích chôn giấu sau vườn chuối của Hùng."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án mùa đông năm Bính Tý",
            "intro": "Chuỗi chứng cứ từ hiện trường căn hộ 204, bình xịt tráo cồn đến vết dép rọ và số vàng chôn giấu đã vạch trần toàn bộ sự thật.",
            "prompt": "Dựa trên toàn bộ tài liệu hồ sơ, hãy chỉ ra kết luận điều tra toàn diện và chính xác nhất:",
            "options": [
                "Triệu Quốc Hùng do nợ cờ bạc cá độ bóng đá, biết bà Bích có vàng tích cóp và bị bệnh hen suyễn nặng, đã nhân lúc sang sửa quạt tráo bình xịt thuốc bằng cồn pha nước muối, sau đó leo ban công lấy vàng khi bà Bích lên cơn hen không xịt được thuốc rồi tẩu thoát, chôn vàng dưới gốc chuối.",
                "Bà Chu Thị Bích do dùng thuốc quá liều dẫn đến sốc phản vệ, hàng xóm phát hiện phá cửa vào cấp cứu nhưng không kịp, số vàng bị kẻ lạ lẻn vào lấy mất trong lúc hỗn loạn.",
                "Đỗ Văn Khang (người thuê trọ tầng 1) đã dùng chìa khóa vạn năng đột nhập sát hại bà Bích rồi vu oan cho Hùng bằng cách giấu vàng ra sau vườn chuối.",
                "Một đối tượng nghiện ma túy trèo tường đột nhập bóp cổ nạn nhân cướp vàng rồi làm rơi đôi dép rọ bộ đội của Hùng tại hiện trường."
            ],
            "answer": [0],
            "hints": [
                "Ai có chuyên môn sửa chữa đồ đạc, có dấu dép rọ ban công và trực tiếp giấu vàng dưới gốc chuối?"
            ],
            "explanation": [
                "Triệu Quốc Hùng là thủ phạm duy nhất. Y tính toán tinh vi thủ đoạn giết người không để lại dấu vết ngoại lực bằng cách vô hiệu hóa bình thuốc xịt hen của nạn nhân để cướp vàng."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded mua-dong-binh-ty (5 questions)")

# 4. tieng-dan-day-pho-hien
def upgrade_pho_hien():
    path = os.path.join(ROOT, "public/cases/tieng-dan-day-pho-hien/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Phương thức trúng độc niêm mạc miệng",
            "intro": "Nghệ nhân Phan Bá Cửu gục chết ngay trong lúc biểu diễn đêm hội rằm Phố Hiến. Cơ quan điều tra cần xác định đường xâm nhập của độc chất.",
            "prompt": "Ghim 2 tài liệu chứng minh chất độc gây tử vong không nằm trong dịch dạ dày mà tiếp xúc trực tiếp qua niêm mạc miệng và liên quan đến vật dụng nhạc cụ của cụ Cửu.",
            "need": 2,
            "answer": ["d04", "d05"],
            "hints": [
                "Ảnh chụp cây đàn đáy và hộp tráp gỗ đựng móng gảy của nghệ nhân.",
                "Biên bản giám định pháp y sơ bộ về niêm mạc lưỡi và khoang miệng."
            ],
            "explanation": [
                "Tài liệu d04 chụp cây đàn đáy và các phím đàn nơi nghệ nhân tiếp xúc ngón tay và móng gảy.",
                "Tài liệu d05 xác nhận dịch dạ dày không có độc nhưng niêm mạc môi và đầu lưỡi phù nề hoại tử do tiếp xúc chất kịch độc alcaloid."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Lời khai dối trá về buồng hóa trang",
            "intro": "Các đào nương và kép đàn tại đình Hoa Nguyệt đều được lấy lời khai về hành tung trước giờ biểu diễn.",
            "prompt": "Đối chiếu lời khai của các nghệ nhân với nhân chứng bán nước chè cổng đình, hãy chỉ ra dòng lời khai của nghi phạm chối bỏ việc bước chân vào buồng hóa trang trước giờ diễn xướng nhưng thực tế đã bị nhìn thấy?",
            "answer": ["d07:008"],
            "hints": [
                "Rà soát lời khai của kép đàn phụ để tìm câu khẳng định ngồi ở sân đình xem hát chứ không vào hậu trường.",
                "Đối chiếu với lời khai của bà bán nước chè nhìn thấy bóng người bước vào buồng hóa trang lúc chạng vạng."
            ],
            "explanation": [
                "Tại d07 dòng 008, Chu Văn Bình khai: 'Suốt từ 18h30 đến khi cụ Cửu lên sân khấu, tôi ngồi uống nước chè ở gốc đa ngoài cổng đình nghe hát, tuyệt đối không hề bước chân vào buồng hóa trang của cụ Cửu'. Lời này bị bà Mùi d09 vạch trần khi thấy Bình lẻn vào buồng hóa trang lúc 18h45."
            ]
        },
        {
            "id": "q3",
            "stage": 2,
            "type": "evidence",
            "title": "Cơ chế tẩm độc phím đàn và thói quen diễn tấu",
            "intro": "Ban chuyên án kiểm tra kỹ lưỡng các nhạc cụ và thói quen của nghệ nhân trước khi so dây.",
            "prompt": "Ghim 2 tài liệu chứng minh chất độc lá ngón được bôi tinh vi lên phím đàn đáy số 3 và thói quen liếm ngón tay vuốt phím của cụ Phan Bá Cửu.",
            "need": 2,
            "answer": ["d10", "d11"],
            "hints": [
                "Bản kết quả hóa nghiệm tang vật xác định dư lượng nhựa độc lá ngón trên phím đàn.",
                "Trích bút ký về thói quen ngậm móng gảy và liếm đầu ngón tay làm ẩm phím khi so dây của cụ Cửu."
            ],
            "explanation": [
                "Tài liệu d10 phát hiện alcaloid độc tố lá ngón bám trên bề mặt phím đàn số 3.",
                "Tài liệu d11 ghi chép thói quen nghề nghiệp của cụ Cửu là luôn liếm đầu ngón tay trỏ miết qua phím số 3 trước khi đệm bài hát chầu văn, khiến chất độc ngấm thẳng qua niêm mạc lưỡi."
            ]
        },
        {
            "id": "q4",
            "stage": 3,
            "type": "evidence",
            "title": "Tang vật bột độc và đơn thuốc bắc",
            "intro": "Khám xét tư trang nghi phạm và xác minh các hiệu thuốc bắc trên địa bàn Phố Hiến.",
            "prompt": "Ghim 2 tài liệu chứng minh nguồn gốc chất độc lá ngón thu giữ trong tư trang nghi phạm và chứng cứ xác minh việc bí mật mua độc dược tại hiệu thuốc bắc Nam Hòa Đường.",
            "need": 2,
            "answer": ["d13", "d14"],
            "hints": [
                "Ảnh tang vật chiếc khăn lụa tẩm nhựa độc và lọ bột lá ngón thu trong hòm đồ diễn của nghi phạm.",
                "Biên bản xác minh tại hiệu thuốc bắc Nam Hòa Đường về người mua vị thuốc lá ngón sấy khô."
            ],
            "explanation": [
                "Tài liệu d13 chụp chiếc khăn lụa lau đàn dính nhựa độc và lọ bột lá ngón thu trong túi áo của Chu Văn Bình.",
                "Tài liệu d14 xác nhận Bình đã bí mật đến hiệu thuốc Nam Hòa Đường mua lá ngón khô lấy cớ để bẫy chuột phá kho thóc."
            ]
        },
        {
            "id": "q5",
            "stage": 3,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án tiếng đàn đáy Phố Hiến",
            "intro": "Toàn bộ chứng cứ về chất độc trên phím đàn, lời khai dối trá và tang vật hiệu thuốc bắc đã phơi bày chân tướng kẻ thủ ác.",
            "prompt": "Dựa vào toàn bộ hồ sơ, ai là thủ phạm đã đầu độc sát hại cụ Phan Bá Cửu, bằng thủ đoạn nào và vì động cơ gì?",
            "options": [
                "Chu Văn Bình do ghen ghét tài năng và đố kỵ danh tiếng nghệ nhân nhân dân của cụ Cửu, sợ bị tước vai kép chính trong chuyến lưu diễn nước ngoài, đã mua lá ngón bôi lên phím đàn số 3 lợi dụng thói quen liếm ngón tay của cụ để đầu độc sát hại.",
                "Đào nương Nguyễn Thị Ánh Tuyết do mâu thuẫn tình cảm bị từ chối, đã tẩm độc vào chén trà gừng mời cụ Cửu uống trước giờ diễn xướng.",
                "Quản lý phường Đỗ Trọng Toàn do nợ nần tiền thù lao biểu diễn, đã lén tẩm độc vào micro trên sân khấu nhằm chiếm đoạt quỹ đoàn.",
                "Một kẻ buôn cổ vật lạ mặt đột nhập đình Hoa Nguyệt định trộm cây đàn đáy cổ nhưng bị phát hiện nên đã hạ độc cụ Cửu."
            ],
            "answer": [0],
            "hints": [
                "Ai là người biết rõ thói quen vuốt phím số 3 của cụ Cửu, có mặt ở buồng hóa trang và tàng trữ bột lá ngón?"
            ],
            "explanation": [
                "Chu Văn Bình là thủ phạm duy nhất. Động cơ đố kỵ nghệ thuật tàn nhẫn kết hợp thủ đoạn tẩm độc phím đàn tinh vi đã bị vạch trần bởi tang vật khăn lụa và lời chứng của hiệu thuốc bắc."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded tieng-dan-day-pho-hien (5 questions)")

# 5. suong-mu-trai-trai
def upgrade_trai_mat():
    path = os.path.join(ROOT, "public/cases/suong-mu-trai-trai/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Dấu vết vận chuyển và vật chất bất thường trên đồi thông",
            "intro": "Thi thể ông Lâm Khải được phát hiện dưới dốc bìa thông Trại Mát trong đêm sương mù dày đặc. Hãy phân tích các dấu hiệu hiện trường.",
            "prompt": "Ghim 2 tài liệu chỉ ra phương tiện vận chuyển thi thể xuống dốc bìa thông và dấu vết hạt vi thể lạ dính trên quần áo nạn nhân không thuộc hệ thực vật đồi thông.",
            "need": 2,
            "answer": ["d02", "d05"],
            "hints": [
                "Biên bản khám nghiệm hiện trường mô tả vệt trượt của bánh xe rùa và bùn đất đỏ.",
                "Ảnh chụp hiện trường dốc bìa thông nơi ghi nhận dấu vết lốp xe cút kít."
            ],
            "explanation": [
                "Tài liệu d02 ghi nhận vết trượt sâu của bánh xe cút kít chở vật nặng và các hạt bụi hoa màu vàng cam dính trên áo khoác dạ.",
                "Tài liệu d05 chụp rõ vệt lốp cao su xe rùa chạy từ hướng kho lạnh trang trại ra mép dốc đồi thông."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Bằng chứng ngoại phạm về kho lạnh số 2",
            "intro": "Các kỹ sư và công nhân trang trại hoa Lâm Viên đều khai báo thời gian biểu ca trực.",
            "prompt": "Trong các biên bản hỏi cung người làm việc tại trang trại hoa Lâm Viên, hãy chỉ ra dòng lời khai khẳng định bản thân không hề mở cửa hay bước chân vào kho lạnh số 2 sau 17h00 chiều?",
            "answer": ["d07:005"],
            "hints": [
                "Rà soát lời khai của kỹ sư quản lý để tìm câu quả quyết niêm phong kho hoa lúc tan ca và không quay lại.",
                "Đối chiếu với dữ liệu cảm biến điện năng và nhiệt độ ghi nhận kho lạnh hoạt động bất thường."
            ],
            "explanation": [
                "Tại d07 dòng 005, Hoàng Văn Duẩn khai: 'Sau khi kiểm kê đóng cửa kho lạnh số 2 lúc 17h00, tôi giao chìa khóa cho bảo vệ rồi về thẳng nhà riêng ở thị trấn, tuyệt đối không hề quay lại kho lạnh nửa bước cho đến sáng hôm sau'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Bằng chứng thi thể bị lưu trữ trong kho lạnh",
            "intro": "Nghi ngờ thi thể nạn nhân đã bị can thiệp nhiệt độ để đánh lừa thời điểm tử vong.",
            "prompt": "Ghim 3 tài liệu liên kết độ co cứng tử thi bất thường (Vòng 1), mẫu phấn hoa Lily chỉ có trong kho lạnh (Vòng 3) và dữ liệu đồng hồ điện ghi nhận nhiệt độ tụt sâu xuống -18°C trong đêm (Vòng 3).",
            "need": 3,
            "answer": ["d04", "d10", "d11"],
            "hints": [
                "Kết quả giám định tử thi về hiện tượng đông cứng các khớp cơ bất thường (ở Vòng 1).",
                "Phân tích vi thể mẫu phấn hoa Lily Casablanca chỉ lưu giữ trong phòng lạnh số 2.",
                "Trích xuất đồng hồ điện tử ghi nhận máy nén khí hoạt động hết công suất hạ nhiệt độ xuống -18°C lúc nửa đêm."
            ],
            "explanation": [
                "Tài liệu d04 (ở Vòng 1) ghi nhận tử thi đông cứng sâu và thân nhiệt tụt nhanh gấp 3 lần bình thường.",
                "Tài liệu d10 khẳng định các hạt phấn hoa dính trên cổ áo nạn nhân là giống hoa Lily nhập khẩu chỉ được lưu trữ riêng trong kho lạnh số 2.",
                "Tài liệu d11 vạch trần lúc 01h15 sáng kho lạnh số 2 bị bật chế độ làm đá lạnh sâu -18°C trong 4 tiếng liền, chứng minh thi thể đã bị giấu trong kho để giả mạo giờ chết."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Vết tích bánh xe cút kít và bao thuốc lá rơi lại",
            "intro": "Khám xét hiện trường xưởng cơ khí và người quản lý trang trại đã thu thập được các chứng cứ then chốt.",
            "prompt": "Ghim 2 tài liệu đối chiếu khớp nối dấu vết hoa lốp bánh xe cút kít chở thi thể và vật chứng bao thuốc lá đặc chủng rơi tại cửa xả kho lạnh.",
            "need": 2,
            "answer": ["d15", "d16"],
            "hints": [
                "Biên bản thu giữ bao thuốc lá ba số 555 đặc chủng có dấu vân tay rơi ở rãnh thoát nước.",
                "Bản giám định dấu vết cơ học đối chiếu hoa lốp bánh xe cút kít tại xưởng trang trại."
            ],
            "explanation": [
                "Tài liệu d15 thu giữ bao thuốc lá ngoại nhập của Duẩn dính nước đá xả kho lạnh.",
                "Tài liệu d16 xác nhận vết hoa lốp cao su trên đồi thông d05 trùng khớp 100% với chiếc xe cút kít Duẩn thường dùng để chở phân bón."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án sương mù Trại Mát",
            "intro": "Thủ đoạn dùng kho lạnh số 2 để đóng băng tử thi nhằm ngụy tạo thời gian chết và bằng chứng ngoại phạm đã bị phơi bày.",
            "prompt": "Dựa vào toàn bộ chứng cứ trong hồ sơ, ai là kẻ đã sát hại ông Lâm Khải, bằng thủ đoạn nào và vì động cơ gì?",
            "options": [
                "Hoàng Văn Duẩn do bị ông Khải phát hiện hành vi bòn rút công quỹ và bán trộm hoa giống quý, đã đánh ngất nạn nhân lúc chiều tối rồi nhốt vào kho lạnh số 2 bật nhiệt độ -18°C làm đông cứng tử thi, sau đó dùng xe cút kít chở xác phi tang xuống dốc bìa thông trong đêm sương mù nhằm ngụy tạo giờ chết lúc nửa đêm.",
                "Lâm Tuyết Mai do mâu thuẫn phân chia thừa kế trang trại, đã cấu kết với thương lái Trần Đại đầu độc cha ruột rồi đưa xác ra đồi thông.",
                "Thương lái Trần Đại do bị hủy hợp đồng thu mua hoa Lily, đã phục kích sát hại ông Khải tại bìa thông rồi cướp tiền bỏ trốn.",
                "Ông Bùi Văn Thao do thù oán ranh giới đất trạm khí tượng, đã dùng xà beng sát hại nạn nhân rồi ngụy tạo vết bánh xe rùa."
            ],
            "answer": [0],
            "hints": [
                "Ai có chìa khóa kho lạnh số 2, biết điều khiển máy nén khí, có vết lốp xe cút kít và bao thuốc lá rơi tại cửa xả?"
            ],
            "explanation": [
                "Hoàng Văn Duẩn là thủ phạm duy nhất. Y tận dụng sự am hiểu kỹ thuật kho lạnh hoa để tạo hiện trường đóng băng thi thể hòng qua mặt giám định pháp y về thời điểm tử vong."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded suong-mu-trai-trai (5 questions)")

if __name__ == "__main__":
    upgrade_demo01()
    upgrade_con_nuoc()
    upgrade_mua_dong()
    upgrade_pho_hien()
    upgrade_trai_mat()
