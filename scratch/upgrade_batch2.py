#!/usr/bin/env python3
import json
import os

ROOT = "/Users/huynguyen/Documents/game_pha_an"

# 1. bong-nang-hoi-an
def upgrade_hoi_an():
    path = os.path.join(ROOT, "public/cases/bong-nang-hoi-an/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Dấu vết tại hiện trường và lối thoát ra giếng Bá Lễ",
            "intro": "Bức tranh lụa cổ 'Thập mục ngưu đồ' bị mất trộm giữa ban ngày tại từ đường họ Lương. Hãy phân tích các dấu vết vật lý ban đầu.",
            "prompt": "Ghim 2 tài liệu chỉ ra lối thoát hiểm phía sau từ đường và dấu vết khả nghi dính bùn rêu bên bờ giếng cổ Bá Lễ.",
            "need": 2,
            "answer": ["d02", "d03"],
            "hints": [
                "Biên bản khám nghiệm hiện trường mô tả cánh cửa hậu từ đường dẫn ra ngõ giếng Bá Lễ.",
                "Ảnh chụp miệng giếng cổ ghi lại vết trượt bùn rêu và dấu dây thừng cọ sát."
            ],
            "explanation": [
                "Tài liệu d02 ghi nhận cửa hậu từ đường mở hé, có dấu chân dính rêu ướt.",
                "Tài liệu d03 phát hiện thành giếng cổ Bá Lễ có vết ma sát dây thừng mới và vết rêu bị gạt trầy."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Bằng chứng ngoại phạm của người thân cận",
            "intro": "Các đối tượng có khả năng tiếp cận từ đường đều được lấy lời khai về lịch trình trưa ngày rằm.",
            "prompt": "Đối chiếu lời khai của các đối tượng liên quan với thời gian biểu trong ngày rằm, hãy chỉ ra dòng lời khai khẳng định có mặt liên tục tại quán cơm gà từ 11h30 đến 13h30 chiều nhằm tạo bằng chứng ngoại phạm?",
            "answer": ["d06:003"],
            "hints": [
                "Rà soát lời khai của người cháu đích tôn về địa điểm ăn trưa.",
                "Tìm câu khẳng định ngồi ăn cơm gà và uống bia suốt 2 tiếng không rời quán."
            ],
            "explanation": [
                "Tại d06 dòng 003, Lương Gia Bảo khai: 'Từ đúng 11h30 đến tận 13h30 chiều tôi ngồi ăn cơm gà và uống bia một mình tại quán bà Buội phố Phan Chu Trinh, suốt thời gian đó tôi không rời quán nửa bước'."
            ]
        },
        {
            "id": "q3",
            "stage": 2,
            "type": "evidence",
            "title": "Bức ảnh chụp ngoại phạm và cấu trúc bức tranh cổ",
            "intro": "Nghi phạm đưa ra một bức ảnh chụp đĩa cơm gà trên bàn ăn có ánh nắng chiếu xiên để làm bằng chứng ngoại phạm.",
            "prompt": "Ghim 2 tài liệu liên kết bức ảnh chụp bữa ăn cơm gà của nghi phạm với bản mô tả cấu trúc bức tranh cổ bị đánh cắp.",
            "need": 2,
            "answer": ["d05", "d07"],
            "hints": [
                "Biên bản định giá và mô tả bức tranh cổ 'Thập mục ngưu đồ' vẽ trên lụa tơ tằm cổ.",
                "Bức ảnh ngoại phạm chụp đĩa cơm gà và cốc bia có bóng nắng chiếu xiên qua khung cửa sổ."
            ],
            "explanation": [
                "Tài liệu d05 mô tả bức tranh lụa có kích thước 1.2m cuộn tròn trong ống đồng bảo quản.",
                "Tài liệu d07 là bức ảnh ngoại phạm mà Bảo dùng điện thoại chụp lại để chứng minh thời gian ngồi ở quán."
            ]
        },
        {
            "id": "q4",
            "stage": 3,
            "type": "evidence",
            "title": "Vạch trần góc bóng nắng và vật chứng giếng Bá Lễ",
            "intro": "Phân tích khoa học hình sự về góc bóng nắng và việc trục vớt lòng giếng đã lật tẩy toàn bộ màn kịch.",
            "prompt": "Ghim 3 tài liệu liên kết kết quả phân tích quang học góc bóng nắng giả mạo thời gian ngoại phạm, hóa đơn mua ống nhựa PVC bọc tranh và biên bản trục vớt vật chứng dưới lòng giếng Bá Lễ.",
            "need": 3,
            "answer": ["d10", "d11", "d12"],
            "hints": [
                "Bản phân tích thiên văn học chứng minh góc bóng nắng 65 độ trong ảnh thuộc về khung giờ 14h15 chứ không phải 12h00 trưa.",
                "Hóa đơn tiệm điện nước phố Lê Lợi ghi nhận việc mua ống nhựa PVC fi-90 có nắp bịt chống nước.",
                "Biên bản thợ lặn trục vớt ống nhựa chứa bức tranh cổ nguyên vẹn giấu dưới đáy giếng Bá Lễ."
            ],
            "explanation": [
                "Tài liệu d10 khẳng định bức ảnh d07 được chụp lúc 14h15 chiều, vạch trần Bảo đã nói dối giờ ăn cơm gà.",
                "Tài liệu d11 thể hiện Bảo đã mua ống nhựa chống nước từ sáng hôm trước để chuẩn bị giấu tranh.",
                "Tài liệu d12 ghi nhận trục vớt ống nhựa chứa bức tranh 'Thập mục ngưu đồ' thả chìm dưới giếng Bá Lễ."
            ]
        },
        {
            "id": "q5",
            "stage": 3,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án giếng Bá Lễ Hội An",
            "intro": "Toàn bộ chuỗi chứng cứ từ vết rêu thành giếng, góc bóng nắng thiên văn đến biên bản trục vớt đã khép lại vụ án.",
            "prompt": "Dựa trên toàn bộ hồ sơ vụ án, ai là kẻ đã lấy cắp bức tranh cổ 'Thập mục ngưu đồ', bằng thủ đoạn nào và vì động cơ gì?",
            "options": [
                "Lương Gia Bảo do nợ cờ bạc cá độ hơn 300 triệu đồng bị giang hồ đe dọa, đã lợi dụng lúc gia tộc bận rộn cúng rằm để trộm bức tranh lụa cổ, cuộn vào ống nhựa PVC mua sẵn thả giấu dưới lòng giếng Bá Lễ, rồi ra quán cơm gà chụp ảnh dàn dựng góc bóng nắng tạo bằng chứng ngoại phạm.",
                "Thợ mộc Nguyễn Văn Trực trong lúc sửa chữa bao lơn từ đường đã phát hiện giá trị bức tranh cổ, lén tháo trộm rồi thả xuống giếng Bá Lễ chờ cơ hội đem bán cho thương lái Định.",
                "Thương lái đồ cổ Trần Khắc Định đã thuê nhóm trộm chuyên nghiệp từ Đà Nẵng đột nhập cửa hậu lấy tranh, sau đó vứt ống nhựa xuống giếng nhằm vu oan cho Bảo.",
                "Bà chủ quán cơm gà Buội đã thông đồng với Bảo để khai man giờ giấc nhằm chia tiền bán bức tranh cổ sau khi bán sang nước ngoài."
            ],
            "answer": [0],
            "hints": [
                "Ai có nợ nần cờ bạc, có tên trên hóa đơn mua ống nhựa PVC, có vết bùn rêu giếng trên giày và tự chụp bức ảnh góc bóng nắng?"
            ],
            "explanation": [
                "Lương Gia Bảo là thủ phạm duy nhất. Y lên kế hoạch tinh vi dùng ống nhựa bảo quản tranh dưới nước và lợi dụng góc bóng nắng để ngụy tạo ngoại phạm nhưng đã bị khoa học hình sự lật tẩy."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded bong-nang-hoi-an (5 questions)")

# 2. dem-sung-no-tay-son
def upgrade_tay_son():
    path = os.path.join(ROOT, "public/cases/dem-sung-no-tay-son/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Hung khí quân dụng và dấu vết đạn đạo",
            "intro": "Vụ cướp tiệm vàng Kim Sinh đêm giao thừa gây chấn động dư luận Thủ đô. Cơ quan điều tra cần xác định vũ khí gây án.",
            "prompt": "Ghim 2 tài liệu chứng minh hung khí gây án là súng ngắn quân dụng K54 cỡ 7.62mm thông qua thương tích tử thi và dấu vết vỏ đạn thu tại hiện trường.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Kết quả giám định tử thi nạn nhân chủ tiệm vàng về đường đạn xuyên phá.",
                "Ảnh chụp 3 vỏ đạn dập năm 1968 và đầu đạn thu gom tại quầy vàng."
            ],
            "explanation": [
                "Tài liệu d03 xác nhận nạn nhân bị bắn bởi đạn súng ngắn quân dụng cỡ 7.62x25mm Tokarev xuyên phá tim phổi.",
                "Tài liệu d05 chụp 3 vỏ đạn đồng dập số hiệu 71-68 (nhà máy 71 sản xuất năm 1968) đặc trưng của súng K54."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Bằng chứng ngoại phạm của người làm cũ",
            "intro": "Các thợ kim hoàn và người quen biết quy luật hoạt động của tiệm vàng đều nằm trong diện rà soát.",
            "prompt": "Trong các biên bản hỏi cung người có liên quan tại khu vực phố Tây Sơn, hãy chỉ ra dòng lời khai nại ra lý do ở lì bên Gia Lâm suốt đêm giao thừa nhưng thực chất đã bị bác bỏ?",
            "answer": ["d06:003"],
            "hints": [
                "Rà soát lời khai của thợ kim hoàn cũ để tìm người khẳng định ở nhà bố mẹ đẻ không sang nội thành.",
                "Tìm câu quả quyết ở trong nhà nghe pháo giao thừa từ 20h00 đến sáng hôm sau."
            ],
            "explanation": [
                "Tại d06 dòng 003, Nguyễn Văn Đông khai: 'Từ 20h00 đêm 30 Tết tôi ở lì tại nhà bố mẹ đẻ bên Bồ Đề, Gia Lâm ăn tất niên và đón giao thừa, không hề bước chân qua cầu Long Biên sang nội thành nửa bước cho tới tận trưa mùng 1 Tết'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Vỏ đạn K54, rãnh xoắn nòng súng và dấu vân tay then chốt",
            "intro": "Ban chuyên án đối chiếu hồ sơ tàng thư căn cước và kỹ thuật đạn đạo hình sự.",
            "prompt": "Ghim 3 tài liệu liên kết 3 vỏ đạn K54 thu tại hiện trường (Vòng 1) với báo cáo giám định rãnh xoắn nòng súng của đối tượng truy nã (Vòng 3) và dấu vân tay trên vỏ bao thuốc lá rơi lại ngõ thoát hiểm (Vòng 3).",
            "need": 3,
            "answer": ["d05", "d10", "d11"],
            "hints": [
                "Ảnh chụp 3 vỏ đạn K54 dập năm 1968 thu tại quầy vàng (ở Vòng 1).",
                "Báo cáo đạn đạo xác định 4 rãnh xoắn nghiêng phải có vết xước khuyết tật của khẩu K54 số hiệu 140228.",
                "Ảnh dấu vân tay ngón trỏ phải trên vỏ bao thuốc lá Du Lịch trùng khớp với tàng thư chỉ bản của Phạm Đức Thắng."
            ],
            "explanation": [
                "Tài liệu d05 là vật chứng vỏ đạn ban đầu tại hiện trường.",
                "Tài liệu d10 khẳng định cả 3 viên đạn đều bắn ra từ khẩu súng K54 số hiệu 140228 do đối tượng đặc biệt nguy hiểm Phạm Đức Thắng cướp khi trốn trại giam.",
                "Tài liệu d11 chứng minh dấu vân tay trên bao thuốc lá d09 vứt lại ở ngõ thoát hiểm chính là của Phạm Đức Thắng."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Lộ trình đào tẩu qua bến phà và tang vật vàng cướp được",
            "intro": "Lần theo dấu vết vượt sông Hồng và tiến hành vây bắt khẩn cấp hang ổ của kẻ thủ ác.",
            "prompt": "Ghim 2 tài liệu chứng minh lộ trình tẩu thoát qua sông Hồng trong đêm giao thừa và biên bản khai quật thu hồi hơn 100 lượng vàng chôn giấu tại bãi bồi ven sông.",
            "need": 2,
            "answer": ["d12", "d15"],
            "hints": [
                "Biên bản xác minh bến phà Đen ghi nhận đối tượng đi xe máy qua phà lúc 01h15 sáng mùng 1 Tết.",
                "Biên bản đào bới thu hồi các bọc vàng miếng SJC và vàng trang sức chôn giấu dưới bãi ngô sông Hồng."
            ],
            "explanation": [
                "Tài liệu d12 ghi nhận lời khai người lái phà Đen chở một đối tượng có nhân dạng giống Thắng mang túi nặng qua sông trong đêm.",
                "Tài liệu d15 thể hiện lực lượng công an đã đào bới thu hồi 108 lượng vàng ta và vàng tây cùng số tiền mặt cướp được chôn dưới bãi cát ven sông Hồng."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện chuyên án phố Tây Sơn",
            "intro": "Khẩu súng ngắn K54, dấu vân tay trên bao thuốc lá và kho vàng chôn giấu đã vạch trần toàn bộ sự thật.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, ai là kẻ đã mang vũ khí nóng bắn gục gia đình chủ tiệm vàng Kim Sinh cướp tài sản?",
            "options": [
                "Phạm Đức Thắng (đối tượng trốn trại đang bị truy nã đặc biệt) đã mang theo súng K54 cướp được, rình rập thời khắc giao thừa tiếng pháo nổ rộ để nổ súng sát hại vợ chồng chủ tiệm vàng, cướp hơn 100 lượng vàng rồi qua bến phà Đen tẩu thoát sang bãi sông Hồng chôn giấu.",
                "Nguyễn Văn Đông do bị đuổi việc uất ức, đã mua súng K54 bắn chết chủ tiệm vàng rồi đem vàng sang Gia Lâm chôn giấu trong vườn nhà bố mẹ đẻ.",
                "Trần Khắc Tuấn (chủ tiệm cầm đồ Giáp Bát) đã thuê một nhóm giang hồ cộm cán mang súng quân dụng cướp tiệm vàng Kim Sinh để trừ nợ lô đề.",
                "Nhân viên bảo vệ chùa Đồng Quang thông đồng với kẻ cướp mở cửa ngõ chùa cho đối tượng tẩu thoát sau khi nổ súng cướp tiệm vàng."
            ],
            "answer": [0],
            "hints": [
                "Ai là đối tượng sở hữu khẩu súng K54 có vân tay trên bao thuốc lá Du Lịch và bị bắt giữ tại bãi ngô sông Hồng?"
            ],
            "explanation": [
                "Phạm Đức Thắng là thủ phạm duy nhất. Bản chất tàn bạo của tên tội phạm trốn trại đã lên kế hoạch dùng tiếng pháo giao thừa át tiếng súng để cướp vàng và bị bắt cùng toàn bộ tang vật."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded dem-sung-no-tay-son (5 questions)")

# 3. lua-than-tay-nguyen
def upgrade_tay_nguyen():
    path = os.path.join(ROOT, "public/cases/lua-than-tay-nguyen/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Dấu vết sát hại trước hỏa hoạn và hung khí xà gạc",
            "intro": "Nhà sàn của già làng Y Krông rực cháy trong đêm giông sét Buôn Ea Kral. Khám nghiệm tử thi cho thấy dấu hiệu của một vụ án mạng che giấu bằng biển lửa.",
            "prompt": "Ghim 2 tài liệu chứng minh già làng đã bị sát hại bằng nhát chém hung khí sắc nhọn trước khi nhà sàn bốc cháy và hung khí xà gạc dính máu bị giấu ở bụi le.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Kết quả giám định tử thi xác nhận hộp sọ bị vỡ do vật sắc nặng chém từ trước khi cháy, phổi không có muội than.",
                "Ảnh chụp chiếc xà gạc đi rẫy dính máu khô thu giữ trong bụi le sau nhà sàn."
            ],
            "explanation": [
                "Tài liệu d03 chứng minh nạn nhân chết do vết chém sắc ngọt vào vùng thái dương, khí quản không có muội khói chứng tỏ đã chết trước khi đám cháy bùng lên.",
                "Tài liệu d05 chụp chiếc xà gạc dính máu nạn nhân bị hung thủ lau chùi vội vã vứt giấu ở bờ rào bụi le."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Lời khai ngoại phạm cúng thần rừng",
            "intro": "Những người thân trong buôn làng đều đưa ra lời giải trình về vị trí của mình trong đêm giông bão.",
            "prompt": "Trong các biên bản hỏi cung người trong buôn làng, hãy chỉ ra dòng lời khai khẳng định ở lại suốt đêm trong rừng già cúng thần rừng nhưng thực tế mâu thuẫn với dấu vết di chuyển?",
            "answer": ["d06:003"],
            "hints": [
                "Rà soát lời khai của con nuôi già làng về địa điểm cúng rừng.",
                "Tìm câu khẳng định ngủ lại chòi rẫy sâu trong rừng Ea Kral suốt đêm không về buôn."
            ],
            "explanation": [
                "Tại d06 dòng 003, Y Bang khai: 'Từ chiều tối tôi đã ở lại chòi rẫy trên đỉnh đồi cúng thần rừng theo tục lệ, suốt đêm mưa giông sấm sét tôi ngủ say trong chòi rẫy cách buôn hơn 5 cây số, hoàn toàn không hề về buôn'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Vết chém xà gạc, bẫy nhiệt rơ-le và nguồn phóng hỏa",
            "intro": "Đội Kỹ thuật hình sự khám nghiệm tàn tro nhà sàn để tìm ra nguồn phát lửa thực sự.",
            "prompt": "Ghim 3 tài liệu liên kết hung khí xà gạc phát rẫy (Vòng 1) với kết quả khám nghiệm tàn tro phát hiện bẫy nhiệt rơ-le điện (Vòng 3) và ảnh tang vật đui đèn bẫy dây mai-so dây điện cháy dở (Vòng 3).",
            "need": 3,
            "answer": ["d05", "d10", "d11"],
            "hints": [
                "Ảnh chiếc xà gạc dính máu thu tại bụi le sau nhà (ở Vòng 1).",
                "Biên bản giám định nguyên nhân hỏa hoạn loại trừ sét đánh và phát hiện dấu vết dầu hỏa cùng dây đồng nối tắt.",
                "Ảnh tang vật đui đèn bẫy nhiệt đấu nối dây mai-so bếp điện chập cháy tạo nguồn phát lửa trễ."
            ],
            "explanation": [
                "Tài liệu d05 là hung khí sát hại trực tiếp nạn nhân.",
                "Tài liệu d10 khẳng định đám cháy không phải do sét đánh tự nhiên mà do bẫy nhiệt phóng hỏa có chuẩn bị trước.",
                "Tài liệu d11 chụp đui đèn vỡ dính dây điện bọc nhựa nhiệt dẻo và mảnh vụn mai-so chập mạch để kích cháy đống củi tẩm dầu sau khi hung thủ đã rời khỏi buôn."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Mẫu bùn suối Ea Kral và pho tượng ngọc bích",
            "intro": "Khám xét khẩn cấp chòi rẫy của nghi phạm đã tìm thấy tang vật của vụ án mạng cướp của.",
            "prompt": "Ghim 2 tài liệu chứng minh sự hiện diện của thủ phạm tại hiện trường qua mẫu bùn suối Ea Kral và việc thu giữ pho tượng ngọc bích cổ giấu trong bồ thóc.",
            "need": 2,
            "answer": ["d14", "d15"],
            "hints": [
                "Kết quả phân tích mẫu bùn đỏ pha cát vàng trên gấu quần nghi phạm trùng khớp tuyệt đối với bùn rãnh nước sau nhà già làng.",
                "Biên bản thu giữ pho tượng ngọc bích thần lửa gia truyền của buôn làng bị giấu đáy bồ thóc."
            ],
            "explanation": [
                "Tài liệu d14 chứng minh chất đất bùn dính trên quần áo của Y Bang chỉ có tại chân cầu thang nhà sàn nạn nhân, bác bỏ lời khai ngủ ở chòi rẫy.",
                "Tài liệu d15 ghi nhận thu hồi nguyên vẹn pho tượng ngọc bích gia bảo nghìn năm của Buôn Ea Kral mà già làng cất giữ trong rương gỗ."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án Buôn Ea Kral",
            "intro": "Toàn bộ chuỗi chứng cứ từ vết chém xà gạc, bẫy nhiệt phóng hỏa đến pho tượng ngọc bích giấu bồ thóc đã sáng tỏ.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, ai là thủ phạm đã sát hại già làng Y Krông và phóng hỏa đốt nhà sàn?",
            "options": [
                "Y Bang (con nuôi già làng) do nợ nần cờ bạc và biết giá trị liên thành của pho tượng ngọc bích thần lửa, đã dùng xà gạc chém chết cha nuôi, cướp tượng ngọc đem giấu vào bồ thóc chòi rẫy, rồi cài bẫy nhiệt đui đèn mai-so kích cháy nhà sàn nhân lúc trời mưa giông để ngụy tạo tai nạn do sét đánh.",
                "Y Thuật (cháu họ già làng) do tranh chấp quyền kế vị già làng buôn Ea Kral, đã phóng hỏa đốt nhà sàn hòng tiêu hủy di chúc rồi lấy cắp tượng ngọc.",
                "Thương lái buôn đồ cổ người Kinh từ Buôn Ma Thuột cấu kết với đám thợ rừng lẻn vào buôn chém chết già làng cướp tượng ngọc.",
                "Một tia sét đánh trúng cột nhà sàn làm đổ bếp lửa gây cháy, già làng trong lúc chạy thoát đã bị xà gồ rớt trúng đầu tử vong."
            ],
            "answer": [0],
            "hints": [
                "Ai là người sở hữu xà gạc dính máu, biết kỹ thuật đấu nối đui đèn điện bẫy nhiệt và giấu tượng ngọc trong bồ thóc của mình?"
            ],
            "explanation": [
                "Y Bang là thủ phạm duy nhất. Lòng tham chiếm đoạt bảo vật cổ của buôn làng kết hợp thủ đoạn tạo bẫy nhiệt phóng hỏa che giấu tội ác đã bị bóc trần hoàn toàn."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded lua-than-tay-nguyen (5 questions)")

# 4. gac-den-hon-dau
def upgrade_hon_dau():
    path = os.path.join(ROOT, "public/cases/gac-den-hon-dau/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Vết đâm dao găm và sự cố ngắt điện hải đăng",
            "intro": "Trạm trưởng hải đăng Hòn Dáu tử vong dưới vực đá trong đêm bão biển. Hãy kiểm tra các dấu hiệu ban đầu chứng minh vụ án mạng.",
            "prompt": "Ghim 2 tài liệu chứng minh Trạm trưởng bị đâm từ phía sau bằng dao găm thợ lặn trước khi rơi xuống vực và thời gian ngọn đèn biển bị tắt gián đoạn 17 phút.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Kết quả giám định tử thi xác nhận vết đâm thấu ngực lưng bằng dao găm thợ lặn trước khi va đập đá.",
                "Trích sao sổ nhật ký vận hành hải đăng ghi nhận đèn vụt tắt 17 phút bất thường lúc 01h15 sáng."
            ],
            "explanation": [
                "Tài liệu d03 xác nhận vết thương chí mạng do lưỡi dao găm thợ lặn đâm từ sau lưng vào khoang màng phổi gây tử vong trước khi rơi.",
                "Tài liệu d05 ghi nhận ngọn hải đăng cấp quốc gia bị mất điện hoàn toàn từ 01h15 đến 01h32 sáng giữa đêm mưa bão."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Lời khai túc trực tầng hầm máy nổ",
            "intro": "Các nhân viên gác đèn trên đảo biệt lập đều phải tường trình chi tiết ca trực đêm.",
            "prompt": "Trong các biên bản hỏi cung nhân viên trạm đèn Hòn Dáu, hãy chỉ ra dòng lời khai quả quyết túc trực liên tục dưới tầng hầm máy phát từ 23h00 không hề bước lên các tầng tháp cho tới sáng?",
            "answer": ["d06:003"],
            "hints": [
                "Rà soát lời khai của Phó trạm trưởng phụ trách cơ điện.",
                "Tìm câu khẳng định ở lì dưới hầm máy nổ canh áp lực dầu suốt cả đêm."
            ],
            "explanation": [
                "Tại d06 dòng 003, Vũ Văn Thắng khai: 'Từ 23h00 đêm tôi xuống tầng hầm túc trực máy nổ chính và theo dõi bảng điều áp, suốt đêm tôi ở lì dưới hầm máy không hề bước chân lên các tầng tháp đèn cho tới sáng hôm sau'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Nhật ký tắt đèn, cầu chì gọt mỏng và bẫy nhiệt đoản mạch",
            "intro": "Cơ quan điều tra nghi ngờ sự cố mất điện hải đăng là một màn kịch kỹ thuật có chủ đích.",
            "prompt": "Ghim 3 tài liệu liên kết thời gian mất điện 17 phút (Vòng 1) với kết luận giám định sợi chì bị gọt mỏng (Vòng 3) và bản vẽ sơ đồ nguyên lý ngắn mạch nhiệt trễ gắn vào máy nổ (Vòng 3).",
            "need": 3,
            "answer": ["d05", "d10", "d13"],
            "hints": [
                "Nhật ký hải đăng ghi nhận thời điểm tắt đèn lúc 01h15 (ở Vòng 1).",
                "Bản giám định nguyên nhân nổ cầu chì tổng do sợi chì bị dùng dao gọt mỏng chỉ còn 0.8mm.",
                "Bản vẽ sơ đồ nguyên lý ngắn mạch trễ sử dụng thanh lưỡng kim nhiệt gài vào cuộn stato máy phát."
            ],
            "explanation": [
                "Tài liệu d05 xác định chính xác khung giờ đèn vụt tắt 17 phút.",
                "Tài liệu d10 vạch trần cầu chì tổng không đứt tự nhiên mà do bị gọt mỏng tiết diện để chịu tải yếu.",
                "Tài liệu d13 giải mã cơ chế bẫy nhiệt trễ: Khi máy nổ chạy nóng đến 75°C sau 2 tiếng, thanh lưỡng kim uốn cong chạm mạch làm nổ cầu chì, tạo cớ kéo Trạm trưởng xuống sửa chữa hoặc ngắt đèn đón tàu buôn lậu."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Áo mưa dính máu và trang nhật ký tố cáo tham ô dầu",
            "intro": "Khám xét các ngóc ngách của tháp đèn hải đăng đã phát hiện nơi cất giấu chứng cứ phạm tội.",
            "prompt": "Ghim 2 tài liệu chỉ ra chiếc áo mưa dính máu nạn nhân giấu trong bầu lọc gió và trang nhật ký tố cáo hành vi tuồn bán hơn 3.200 lít dầu diesel của thủ phạm.",
            "need": 2,
            "answer": ["d15", "d16"],
            "hints": [
                "Ảnh chụp chiếc áo mưa bảo hộ dính máu giấu trong bầu lọc gió máy nổ phụ.",
                "Bản khôi phục trang nhật ký bị xé của Trạm trưởng ghi rõ việc phát hiện hao hụt 3.200 lít dầu diesel phục vụ hải đăng."
            ],
            "explanation": [
                "Tài liệu d15 ghi nhận thu giữ chiếc áo mưa dính máu nạn nhân bị nhét sâu trong bầu lọc gió máy phát điện.",
                "Tài liệu d16 là trang nhật ký Trạm trưởng Quyết ghi lại chứng cứ Vũ Văn Thắng rút ruột 3.200 lít dầu diesel bán cho tàu cá ngoài khơi, động cơ trực tiếp dẫn đến án mạng."
            ]
        },
        {
            "id": "q5",
            "stage": 5,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án gác đèn Hòn Dáu",
            "intro": "Toàn bộ chuỗi chứng cứ từ dao găm thợ lặn, bẫy đoản mạch nhiệt trễ đến chiếc áo mưa và trang nhật ký xé rời đã vạch trần kẻ thủ ác.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, ai là thủ phạm đã sát hại Trạm trưởng Đỗ Đình Quyết?",
            "options": [
                "Phó trạm trưởng Vũ Văn Thắng do bị Trạm trưởng Quyết phát hiện hành vi bòn rút 3.200 lít dầu diesel bán cho tàu buôn lậu, đã gài bẫy ngắn mạch nhiệt làm tắt đèn lúc nửa đêm, nhân lúc ông Quyết lên tháp quan sát đã dùng dao găm thợ lặn đâm chết rồi đẩy xác xuống vực, sau đó giấu áo mưa và xé trang nhật ký để phi tang.",
                "Thợ máy Bùi Xuân Tùng do bất cẩn làm chập điện tủ sấy quần áo gây nổ cầu chì, sợ bị kỷ luật nên đã xô xát đẩy ông Quyết ngã xuống vực đá.",
                "Nhân viên gác đèn Đỗ Văn Lượng do ngủ gật để tàu cá đâm vào rạn san hô, đã dựng hiện trường giả mất điện rồi sát hại cấp trên.",
                "Nhóm cướp biển ngoại quốc lẻn lên đảo Hòn Dáu cắt điện hải đăng để đón tàu chở hàng lậu rồi đâm chết trạm trưởng."
            ],
            "answer": [0],
            "hints": [
                "Ai có chuyên môn cơ điện chế tạo bẫy ngắn mạch trễ, có kìm tuốt chì, sở hữu dao găm thợ lặn và trực tiếp tham ô 3.200 lít dầu diesel?"
            ],
            "explanation": [
                "Vũ Văn Thắng là thủ phạm duy nhất. Động cơ che giấu đường dây buôn lậu dầu diesel kết hợp thủ đoạn tạo sự cố kỹ thuật hòng tạo bằng chứng ngoại phạm đã bị bóc trần hoàn toàn."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded gac-den-hon-dau (5 questions)")

# 5. vang-bong-cho-lon
def upgrade_cho_lon():
    path = os.path.join(ROOT, "public/cases/vang-bong-cho-lon/case.json")
    with open(path, "r", encoding="utf-8") as f:
        c = json.load(f)
        
    c["questions"] = [
        {
            "id": "q1",
            "stage": 1,
            "type": "evidence",
            "title": "Độc chất tách cà phê và dấu vết bột phấn trên núm két sắt",
            "intro": "Chủ tiệm vàng Vạn Thành gục chết trên bàn làm việc trong căn phòng kín khóa chốt. Hãy kiểm tra các dấu vết vật lý ban đầu.",
            "prompt": "Ghim 2 tài liệu chứng minh nạn nhân bị đầu độc bằng thuốc ức chế thần kinh trong tách cà phê và dấu vết bột phấn lạ vạch trần 4 con số mật mã két sắt.",
            "need": 2,
            "answer": ["d03", "d05"],
            "hints": [
                "Kết quả giám định pháp y tử thi xác nhận nồng độ cao thuốc mê cloral hydrat trong dạ dày.",
                "Ảnh chụp cận cảnh núm xoay két sắt dính bột phấn phản quang trên các con số mật mã."
            ],
            "explanation": [
                "Tài liệu d03 xác nhận ông Lâm Vạn Thành bị hôn mê sâu dẫn đến ngừng thở do uống phải thuốc mê cực mạnh cloral hydrat pha trong tách cà phê.",
                "Tài liệu d05 phát hiện trên núm xoay két sắt có bám dính bột phấn màu trắng giúp kẻ gian nhận biết 4 con số thường xuyên được bấm."
            ]
        },
        {
            "id": "q2",
            "stage": 2,
            "type": "line",
            "title": "Bằng chứng ngoại phạm rạp ca nhạc",
            "intro": "Những người thân cận và thợ kim hoàn làm việc tại tiệm vàng đều phải giải trình lịch trình buổi tối xảy ra án mạng.",
            "prompt": "Trong các biên bản hỏi cung người thân cận tiệm vàng Vạn Thành, hãy chỉ ra dòng lời khai khẳng định ngồi xem ca nhạc liên tục từ 21h00 đến 23h30 không hề rời rạp nửa bước?",
            "answer": ["d06:003"],
            "hints": [
                "Rà soát lời khai của người thợ kim hoàn chính để tìm bằng chứng ngoại phạm xem ca nhạc.",
                "Tìm câu khẳng định ngồi xem từ đầu đến cuối không ra ngoài nửa bước."
            ],
            "explanation": [
                "Tại d06 dòng 003, Trương Chấn Hào khai: 'Từ 21h00 đến 23h30 đêm qua tôi ngồi liên tục tại hàng ghế F12 rạp Hào Huê xem ca nhạc tạp kỹ, suốt buổi diễn tôi ngồi im thưởng thức không hề rời rạp nửa bước cho tới khi tan màn'."
            ]
        },
        {
            "id": "q3",
            "stage": 3,
            "type": "evidence",
            "title": "Núm xoay két sắt, mảnh giấy 24 hoán vị và chữ viết tay",
            "intro": "Khám nghiệm tỉ mỉ phòng làm việc đã thu thập được manh mối về cách thức mở két sắt cơ học.",
            "prompt": "Ghim 3 tài liệu liên kết dấu vết bột phấn trên núm két sắt (Vòng 1) với mảnh giấy ghi 24 hoán vị mật số (Vòng 3) và kết luận giám định chữ viết tay của nghi phạm (Vòng 3).",
            "need": 3,
            "answer": ["d05", "d10", "d11"],
            "hints": [
                "Ảnh chụp cận cảnh núm xoay két sắt dính bột phấn (ở Vòng 1).",
                "Ảnh mảnh giấy ghi 24 dãy số hoán vị của 4 con số tìm thấy dưới gầm bàn trà.",
                "Báo cáo giám định chữ viết tay xác nhận các con số hoán vị do chính thợ kim hoàn Trương Chấn Hào viết."
            ],
            "explanation": [
                "Tài liệu d05 phát hiện 4 con số dính phấn gồm 2, 5, 7, 9.",
                "Tài liệu d10 là mảnh giấy kẻ gian tính toán sẵn 24 tổ hợp hoán vị để thử mở két sắt sau khi đánh thuốc mê nạn nhân.",
                "Tài liệu d11 khẳng định nét chữ trên mảnh giấy d10 trùng khớp hoàn toàn với chữ viết tay của Trương Chấn Hào."
            ]
        },
        {
            "id": "q4",
            "stage": 4,
            "type": "evidence",
            "title": "Lọ thuốc ngủ cloral hydrat và số vàng thỏi cướp được",
            "intro": "Lệnh khám xét khẩn cấp nơi ở của thủ phạm tại Quận 11 đã thu giữ trọn vẹn tang vật vụ cướp giết.",
            "prompt": "Ghim 2 tài liệu chứng minh việc khám xét thu giữ độc chất cloral hydrat đầu độc nạn nhân và số vàng thỏi cướp được giấu trong hộp trà Thiết Quan Âm.",
            "need": 2,
            "answer": ["d14", "d15"],
            "hints": [
                "Biên bản khám xét nhà thu hồi 30 lượng vàng thỏi và ngoại tệ giấu dưới đáy hộp trà Thiết Quan Âm.",
                "Kết quả giám định lọ thuốc ngủ cloral hydrat dạng lỏng giấu trong túi áo blu của nghi phạm."
            ],
            "explanation": [
                "Tài liệu d14 ghi nhận thu hồi toàn bộ số vàng thỏi và tiền mặt bị cướp giấu tinh vi trong hộp trà Thiết Quan Âm.",
                "Tài liệu d15 xác nhận hoạt chất trong lọ thuốc ngủ thu được ở nhà Hào trùng khớp 100% với độc chất trong tách cà phê của nạn nhân d03."
            ]
        },
        {
            "id": "q5",
            "stage": 4,
            "type": "choice",
            "title": "Bản kết luận điều tra toàn diện vụ án tiệm vàng Vạn Thành",
            "intro": "Bột phấn núm két sắt, mảnh giấy hoán vị mật mã và số vàng thỏi giấu trong hộp trà đã vạch trần chân tướng kẻ thủ ác.",
            "prompt": "Dựa vào toàn bộ tài liệu hồ sơ, ai là thủ phạm đã sát hại ông Lâm Vạn Thành và trộm két sắt?",
            "options": [
                "Trương Chấn Hào do thua cá độ bóng đá và nợ nặng lãi, đã bôi bột phấn lên núm két sắt để tìm ra 4 con số mật mã, pha thuốc ngủ cloral hydrat vào cà phê cho ông Thành uống rồi lẻn về mở két cướp 30 lượng vàng, sau đó đến rạp Hào Huê mua vé nhờ người ngồi thế chỗ để tạo bằng chứng ngoại phạm.",
                "Bà vợ bé Lý Diễm My do bị ông Thành cắt tiền chu cấp, đã câu kết với nhân viên bảo vệ Quách Bửu đầu độc chồng rồi mở két lấy vàng bỏ trốn.",
                "Bảo vệ Quách Bửu nhân lúc ông Thành ngủ say đã mở cửa cho nhóm giang hồ Chợ Lớn đột nhập dùng xà beng cạy két sắt cướp tài sản.",
                "Một đối tượng khách hàng quen của tiệm vàng đã đánh thuốc mê nạn nhân rồi ép buộc Trương Chấn Hào phải viết giấy hoán vị mở két sắt."
            ],
            "answer": [0],
            "hints": [
                "Ai là người biết rõ thói quen uống cà phê của ông Thành, viết mảnh giấy 24 hoán vị và tàng trữ vàng thỏi trong hộp trà Thiết Quan Âm?"
            ],
            "explanation": [
                "Trương Chấn Hào là thủ phạm duy nhất. Kế hoạch trộm két sắt tinh vi bằng bột phấn và hoán vị số học kết hợp màn kịch vé rạp ca nhạc đã bị bóc trần hoàn toàn."
            ]
        }
    ]
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print("✓ Upgraded vang-bong-cho-lon (5 questions)")

if __name__ == "__main__":
    upgrade_hoi_an()
    upgrade_tay_son()
    upgrade_tay_nguyen()
    upgrade_hon_dau()
    upgrade_cho_lon()
