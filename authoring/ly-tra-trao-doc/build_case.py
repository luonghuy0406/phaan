"""Dựng public/cases/ly-tra-trao-doc/case.json (bản 2, hư cấu, có đồng phạm). Chạy ở thư mục gốc:
python3 authoring/ly-tra-trao-doc/build_case.py"""
import json
import os

CID = 'ly-tra-trao-doc'
CA = ['Công an thị xã Hưng Thái', 'Đội Cảnh sát hình sự']
DTV = 'Điều tra viên'
DTV_NAME = 'Đại uý Nguyễn Hải Đăng'


def tl(name, *pairs):
    """Lời khai: (người nói, câu); None = người khai."""
    return [{'n': i + 1, 'speaker': s or name, 'text': t} for i, (s, t) in enumerate(pairs)]


D = []
add = D.append

# ───────────── Vòng 1: cốc trà dành cho ai ─────────────
add({'id': 'd00', 'stage': 1, 'type': 'people', 'title': 'Nạn nhân và những người liên quan',
     'paragraphs': ['Ảnh thẻ trích từ hồ sơ nhân khẩu, kèm lý do từng người được đưa vào diện xác minh sáng 20/11/2016.']})

add({'id': 'd01', 'stage': 1, 'type': 'newspaper', 'title': 'Báo Hưng Thái: Nữ kỹ thuật viên tử vong sau cốc trà sữa',
     'masthead': 'Hưng Thái', 'issue': 'Số 1.388', 'date': 'Chủ nhật, 20/11/2016',
     'headline': 'Uống trà sữa trong tủ lạnh khoa, nữ kỹ thuật viên dược tử vong',
     'deck': 'Túi trà sữa "cảm ơn" gửi tới khoa Dược chiều thứ Sáu. Sáng thứ Bảy, một người đã không qua khỏi.',
     'image': 'images/d01-benh-vien.webp', 'imageCaption': 'Cổng Bệnh viện Đa khoa thị xã Hưng Thái sáng 19/11.',
     'paragraphs': [
         'Sáng 19/11, chị Lê Thị Ngọc Hân (27 tuổi), kỹ thuật viên khoa Dược Bệnh viện Đa khoa thị xã Hưng Thái, đột ngột tê miệng, nôn và ngất sau khi uống một cốc trà sữa lấy từ tủ lạnh phòng giao ban. Chị tử vong lúc 10 giờ 15 dù được cấp cứu ngay tại chỗ.',
         'Túi trà sữa được người giao hàng mang tới khoa chiều 18/11, kèm tấm thiệp ký tên "Phòng Vật tư". Một số nhân viên khoa đã uống các cốc khác ngay chiều hôm đó mà không có biểu hiện gì.',
         'Lãnh đạo bệnh viện cho biết Phòng Vật tư không gửi quà cho khoa Dược. Công an thị xã đã niêm phong phòng giao ban và lấy mẫu xét nghiệm.',
         'Đây là ngày Nhà giáo Việt Nam; cả khoa Dược đã huỷ buổi liên hoan dự định vào chiều nay.']})

add({'id': 'd02', 'stage': 1, 'type': 'report', 'title': 'Biên bản khám nghiệm phòng giao ban khoa Dược',
     'header': CA, 'heading': 'Biên bản khám nghiệm hiện trường', 'code': '41/KNHT', 'date': '14 giờ 00 ngày 19/11/2016',
     'fields': [{'label': 'Địa điểm', 'value': 'Phòng giao ban khoa Dược, tầng 2 nhà C, Bệnh viện Đa khoa thị xã Hưng Thái'},
                {'label': 'Người chết', 'value': 'Lê Thị Ngọc Hân, 27 tuổi, kỹ thuật viên dược'}],
     'sections': [
         {'heading': '1. Tủ lạnh chung', 'paragraphs': [
             'Ngăn trên còn **một cốc trà sữa ô long kem** (nắp nguyên, tem decal quán Mộc dán trên nắp) và **một cốc trà đào**. Ngăn dưới có hộp cơm, sữa chua của nhân viên.',
             'Trên bàn giao ban có một cốc ô long kem đã uống khoảng một phần ba, nắp bị chọc ống hút. Theo nhân viên khoa, đây là cốc chị Hân uống lúc 8 giờ 20.']},
         {'heading': '2. Túi đựng và thiệp', 'paragraphs': [
             'Trong thùng rác có túi giấy của quán Mộc, quai còn băng dính trong dán kín đã bị xé, và hoá đơn ghi 6 cốc: 2 ô long kem, 2 trà đào, 2 trân châu đường đen.',
             'Thiệp in vi tính: "**Gửi anh Minh và các em khoa Dược. Cảm ơn cả khoa! Phòng Vật tư**". Không có chữ ký tay.']},
         {'heading': '3. Ghi nhận khác', 'paragraphs': ['Không có dấu hiệu xô xát, không có thuốc lạ trong phòng. Đã thu giữ toàn bộ cốc, nắp, túi, thiệp để giám định.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd03', 'stage': 1, 'type': 'report', 'title': 'Kết quả giám định pháp y sơ bộ',
     'header': ['Trung tâm Pháp y tỉnh', 'Phòng Giám định'], 'heading': 'Kết quả giám định sơ bộ', 'code': '212/PY', 'date': 'Ngày 19 tháng 11 năm 2016',
     'fields': [{'label': 'Người chết', 'value': 'Lê Thị Ngọc Hân, 27 tuổi'}],
     'sections': [
         {'heading': '1. Diễn biến theo bệnh án cấp cứu', 'paragraphs': ['Khoảng 15 phút sau khi uống: tê bỏng lưỡi và môi, buồn nôn, vã mồ hôi; sau đó tụt huyết áp, **rối loạn nhịp tim** nặng. Tử vong 10 giờ 15 ngày 19/11.']},
         {'heading': '2. Nhận định', 'paragraphs': ['Không có thương tích. Triệu chứng phù hợp ngộ độc một **alkaloid tác động lên tim và thần kinh**, đi vào qua đường uống. Không phù hợp ngộ độc thực phẩm do vi khuẩn (khởi phát quá nhanh).',
                                                    'Đã lấy máu, dịch dạ dày và gửi kèm hai cốc ô long kem để xét nghiệm độc chất.']}],
     'signature': 'Giám định viên: BS. Trần Quang Lợi'})

add({'id': 'd04', 'stage': 1, 'type': 'scan', 'title': 'Sơ đồ khoa Dược và lối vào nhà C',
     'image': 'images/d04-so-do-khoa-duoc.webp', 'caption': 'Sơ đồ tầng 2 nhà C (khoa Dược) và bãi xe phía sau, lập lúc khám nghiệm.'})

add({'id': 'd05', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của Phạm Thu Trang (dược sĩ khoa Dược)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '15 giờ 30 ngày 19/11/2016',
     'fields': [{'label': 'Người khai', 'value': 'Phạm Thu Trang, 30 tuổi, dược sĩ khoa Dược'}],
     'lines': tl('Phạm Thu Trang',
         (DTV, 'Túi trà sữa đến khoa thế nào?'),
         (None, 'Khoảng ba rưỡi chiều thứ Sáu, anh giao hàng mang lên, Hân ký nhận. Túi giấy quán Mộc, quai dán băng dính kín, kèm tấm thiệp ghi Phòng Vật tư.'),
         (None, 'Tôi, Hân với chị Ngân uống luôn hai cốc trân châu với một cốc trà đào. Không ai làm sao cả.'),
         (DTV, 'Sao hai cốc ô long kem còn lại?'),
         (None, 'Ô long kem là món anh Minh trưởng khoa uống chiều thứ Sáu nào cũng uống, cả khoa biết. Thiệp lại ghi gửi anh Minh, nên chúng tôi để phần anh ấy vào tủ lạnh.'),
         (None, 'Chiều đó anh Minh đi họp ở Sở rồi về thẳng nhà. Sáng thứ Bảy Hân trực, chắc em nghĩ để lâu hỏng, nên lấy một cốc uống.'),
         (DTV, 'Phòng Vật tư có hay gửi quà không?'),
         (None, 'Chưa bao giờ. Sáng nay tôi gọi chị trưởng phòng Vật tư, chị ấy bảo không biết gì về túi trà.'),
         (None, 'Hân hiền lắm, em chẳng thù oán ai. Cốc trà đó đâu phải của em.')),
     'signature': 'Người khai: Phạm Thu Trang'})

add({'id': 'd06', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của DS. Phạm Đức Minh (trưởng khoa Dược)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '17 giờ 00 ngày 19/11/2016',
     'fields': [{'label': 'Người khai', 'value': 'Phạm Đức Minh, 52 tuổi, trưởng khoa Dược'}],
     'lines': tl('Phạm Đức Minh',
         (DTV, 'Ai biết ông hay uống trà sữa ô long kem?'),
         (None, 'Người trong khoa ai cũng biết, thường Bảo phó khoa đặt hộ tôi. Tháng Chín bà Nhung giám đốc Công ty Phúc An đến làm việc còn mang đúng hai cốc ô long kem, nói "nghe nói anh thích món này".'),
         (DTV, 'Gần đây ông có mâu thuẫn với ai?'),
         (None, 'Tôi không ký biên bản nghiệm thu gói vật tư tiêu hao 3,2 tỷ của Phúc An vì hàng giao thiếu gần một nửa. Bà Nhung đến năn nỉ hai lần, lần sau lớn tiếng.'),
         (None, 'Tôi đã soạn đơn báo cáo Sở Y tế, định gửi sáng thứ Hai. Trong khoa chỉ Bảo biết chuyện này, vì Bảo phụ trách hồ sơ thầu.'),
         (DTV, 'Còn ai khác?'),
         (None, 'Tháng Mười có anh Hoàng Văn Sơn, con trai một bệnh nhân mất ở khoa Nội, cho rằng khoa Dược cấp nhầm thuốc. Anh ta nhắn tin cho tôi: "Ông sẽ phải trả giá". Tôi còn giữ tin nhắn.'),
         (DTV, 'Chiều thứ Sáu ông ở đâu?'),
         (None, 'Họp ở Sở Y tế từ hai giờ tới năm giờ bốn mươi, rồi về thẳng nhà. Nếu tôi về khoa, người nằm đó là tôi.')),
     'signature': 'Người khai: Phạm Đức Minh'})

add({'id': 'd07', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của DS. Vũ Quốc Bảo (phó khoa Dược)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '18 giờ 00 ngày 19/11/2016',
     'fields': [{'label': 'Người khai', 'value': 'Vũ Quốc Bảo, 33 tuổi, phó trưởng khoa Dược'}],
     'lines': tl('Vũ Quốc Bảo',
         (DTV, 'Chiều thứ Sáu anh ở đâu?'),
         (None, 'Tôi ở kho cấp phát kiểm kê cuối tháng suốt buổi chiều, ba rưỡi lên phòng giao ban thì thấy túi trà rồi, mọi người đang uống.'),
         (DTV, 'Anh có uống không?'),
         (None, 'Không, tôi không uống đồ ngọt. Tôi bảo các em để phần anh Minh.'),
         (DTV, 'Anh có biết ai muốn hại ông Minh?'),
         (None, 'Anh Sơn người nhà bệnh nhân từng dọa anh Minh, cả khoa biết. Hôm đó anh ta còn lên làm loạn ở khoa.'),
         (DTV, 'Còn Công ty Phúc An?'),
         (None, 'Chuyện nghiệm thu là chuyện hành chính, bên nào cũng có lý. Tôi chỉ lo hồ sơ thầu, không đứng về ai.')),
     'signature': 'Người khai: Vũ Quốc Bảo'})

# ───────────── Vòng 2: người đặt trà ─────────────
add({'id': 'd08', 'stage': 2, 'type': 'report', 'title': 'Kết quả xét nghiệm độc chất',
     'header': ['Viện Khoa học hình sự', 'Bộ Công an'], 'heading': 'Kết quả xét nghiệm', 'code': '1931/XN', 'date': 'Ngày 21 tháng 11 năm 2016',
     'fields': [{'label': 'Mẫu', 'value': 'Máu, dịch dạ dày nạn nhân; cốc ô long kem đã uống; cốc ô long kem còn nguyên; cốc trà đào; cặn các cốc đã uống chiều 18/11'}],
     'sections': [
         {'heading': '1. Kết quả', 'paragraphs': ['Phát hiện **aconitine** (alkaloid của cây ô đầu) trong máu, dịch dạ dày nạn nhân, trong **cả hai cốc ô long kem**. Cốc ô long kem còn nguyên chứa lượng đủ gây tử vong cho nhiều người lớn.',
                                                  'Cốc trà đào còn nguyên và cặn các cốc trân châu, trà đào đã uống chiều 18/11: **không có** aconitine.']},
         {'heading': '2. Nhận xét', 'paragraphs': ['Aconitine không có trong nguyên liệu pha chế trà sữa. Ô đầu chế được dùng trong đông dược (chủ yếu ngâm rượu xoa bóp); dịch chiết đặc phải được người có hiểu biết chuẩn bị.']}],
     'signature': 'Giám định viên: TS. Nguyễn Thị Bích'})

add({'id': 'd09', 'stage': 2, 'type': 'report', 'title': 'Trích nhật ký đơn giao hàng ngày 18/11/2016',
     'header': ['Công ty Giao hàng nhanh Tốc Hành', 'Chi nhánh Hưng Thái'], 'heading': 'Trích xuất dữ liệu theo yêu cầu cơ quan điều tra', 'code': 'TH-2016-11-18-0457', 'date': 'Ngày 21 tháng 11 năm 2016',
     'fields': [{'label': 'Người đặt', 'value': 'Tài khoản "Hoa", số 09xx xxx 418, tạo lúc 15:06 ngày 18/11'},
                {'label': 'Điểm nhận', 'value': 'Quán cà phê Lá Me, đối diện cổng sau bệnh viện'},
                {'label': 'Điểm giao', 'value': 'Khoa Dược, tầng 2 nhà C, Bệnh viện Đa khoa thị xã Hưng Thái'},
                {'label': 'Tài xế', 'value': 'Lý Văn Tài'}],
     'sections': [{'heading': 'Hành trình', 'paragraphs': [
         '— 15:08 đặt đơn, ghi chú "túi trà đã dán kín, giao tận tay khoa Dược".',
         '— 15:15 tài xế nhận hàng (định vị tại quán Lá Me).',
         '— 15:15–15:24 di chuyển liên tục, không dừng (định vị cập nhật mỗi 15 giây).',
         '— 15:27 giao xong, ảnh xác nhận: túi giấy quán Mộc, quai dán băng dính, người nhận ký "Hân".',
         'Tài khoản "Hoa" chỉ đặt một đơn này rồi không dùng lại. Thanh toán tiền mặt.']}],
     'signature': 'Trưởng chi nhánh: Đỗ Văn Khánh'})

add({'id': 'd10', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của Lý Văn Tài (tài xế giao hàng)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 00 ngày 21/11/2016',
     'fields': [{'label': 'Người khai', 'value': 'Lý Văn Tài, 24 tuổi, tài xế giao hàng'}],
     'lines': tl('Lý Văn Tài',
         (DTV, 'Ai giao túi trà cho anh?'),
         (None, 'Một chị khoảng bốn mươi, mặc áo chống nắng màu hồng trùm kín, đeo khẩu trang với kính râm, đứng ở cửa quán Lá Me. Chị ấy đưa túi, dặn đừng mở, giao tận tay khoa Dược.'),
         (None, 'Túi dán băng dính kín cả quai. Tôi treo lên móc xe đi thẳng, không dừng chỗ nào.'),
         (DTV, 'Chị ấy đi bằng gì?'),
         (None, 'Xe Lead trắng dựng ở lề, biển số bị dán băng dính đen. Tôi thấy lạ nhưng khách trả tiền mặt nên thôi.'),
         (DTV, 'Anh có quen ai ở khoa Dược không?'),
         (None, 'Không ạ. Hôm đó tôi còn nhận thêm hai cuốc ngoài ứng dụng cho đủ tiền xăng, các anh đừng báo công ty giúp tôi.')),
     'signature': 'Người khai: Lý Văn Tài'})

add({'id': 'd11', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của Hoàng Văn Sơn (người nhà bệnh nhân)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 00 ngày 21/11/2016',
     'fields': [{'label': 'Người khai', 'value': 'Hoàng Văn Sơn, 45 tuổi, công nhân bốc xếp cảng Hưng Thái'}],
     'lines': tl('Hoàng Văn Sơn',
         (DTV, 'Anh có mâu thuẫn gì với ông Minh?'),
         (None, 'Bố tôi mất ở khoa Nội tháng Mười. Tôi nghĩ khoa Dược cấp nhầm thuốc, tôi có lên khoa to tiếng.'),
         (DTV, 'Anh có nhắn tin cho ông Minh không?'),
         (None, 'Không. Tôi chưa bao giờ nhắn tin gì cho ông ấy, tôi còn chẳng có số.'),
         (DTV, 'Chiều 18/11 anh ở đâu?'),
         (None, 'Tôi làm ca chiều ở cảng, hai giờ tới mười giờ đêm. Cả tổ bốc xếp làm chứng.'),
         (None, 'Tôi giận thật, nhưng tôi không giết ai. Con bé đó tôi còn chẳng biết mặt.')),
     'signature': 'Người khai: Hoàng Văn Sơn'})

add({'id': 'd12', 'stage': 2, 'type': 'report', 'title': 'Biên bản xác minh nơi làm việc của Hoàng Văn Sơn',
     'header': CA, 'heading': 'Biên bản xác minh', 'code': '52/XM', 'date': 'Ngày 21 tháng 11 năm 2016',
     'sections': [{'heading': 'Kết quả', 'paragraphs': [
         'Bảng chấm công thẻ từ cảng Hưng Thái: Hoàng Văn Sơn quẹt thẻ vào 13:52, ra 22:07 ngày 18/11.',
         'Camera bến 3 ghi Sơn làm việc liên tục cùng tổ bốc xếp số 4, nghỉ giải lao tại chỗ 17:30–18:00. Cảng cách bệnh viện 9 km.',
         'Tổ trưởng Nguyễn Văn Tuyến xác nhận Sơn không rời bến trong ca.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd13', 'stage': 2, 'type': 'receipt', 'title': 'Hoá đơn và trích camera quán trà sữa Mộc',
     'shop': 'Trà sữa Mộc', 'address': 'Số 12 phố Lê Lai, cách cổng sau bệnh viện 300 m',
     'fields': [{'label': 'Ngày', 'value': '18/11/2016'}, {'label': 'Đặt qua điện thoại', 'value': '14:05, số 09xx xxx 418'},
                {'label': 'Nhận tại quầy', 'value': '14:30'}],
     'items': [{'name': 'Trà sữa ô long kem', 'qty': '2', 'price': '70.000'}, {'name': 'Trà đào', 'qty': '2', 'price': '60.000'},
               {'name': 'Trân châu đường đen', 'qty': '2', 'price': '64.000'}],
     'total': '194.000đ (tiền mặt)',
     'footer': ['Camera quầy 14:30: người nhận là phụ nữ khoảng 40 tuổi, áo chống nắng hồng trùm đầu, khẩu trang, kính râm; dặn "**dán tem kỹ giùm chị**". Đi xe Lead trắng, biển số dán băng dính.',
                'Mọi cốc của quán đều dán tem decal tròn in logo lên nắp sau khi ép.']})

add({'id': 'd14', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của Đinh Thị Hồng Nhung (Công ty Phúc An)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '15 giờ 30 ngày 21/11/2016',
     'fields': [{'label': 'Người khai', 'value': 'Đinh Thị Hồng Nhung, 41 tuổi, giám đốc Công ty TNHH Thiết bị y tế Phúc An (TP Nam Định)'}],
     'lines': tl('Đinh Thị Hồng Nhung',
         (DTV, 'Quan hệ giữa công ty chị và khoa Dược?'),
         (None, 'Phúc An cung ứng vật tư tiêu hao cho bệnh viện ba năm nay. Gói 3,2 tỷ đang vướng nghiệm thu, chuyện thường của ngành, rồi cũng xong.'),
         (DTV, 'Chiều thứ Sáu 18/11 chị ở đâu?'),
         (None, 'Tôi ở văn phòng công ty tại Nam Định cả buổi chiều, họp với kế toán chuẩn bị quyết toán cuối năm.'),
         (DTV, 'Chị có biết ông Minh thích uống gì không?'),
         (None, 'Làm sao tôi biết được. Tôi gặp anh Minh có vài lần, toàn ở phòng họp.'),
         (None, 'Các anh nghi tôi vì chuyện tiền nong thì cứ kiểm tra. Phúc An làm ăn đàng hoàng.')),
     'signature': 'Người khai: Đinh Thị Hồng Nhung'})

# ───────────── Vòng 3: chiếc ô tô màu đỏ ─────────────
add({'id': 'd15', 'stage': 3, 'type': 'report', 'title': 'Trích camera cổng nhà C và bãi xe bệnh viện chiều 18/11',
     'header': CA, 'heading': 'Biên bản trích xuất dữ liệu camera', 'code': '57/TX', 'date': 'Ngày 22 tháng 11 năm 2016',
     'image': 'images/d15-camera-bai-xe.webp', 'imageCaption': 'Camera bãi xe sau nhà C, 14:44 ngày 18/11: người phụ nữ áo chống nắng hồng mở cửa ghế phụ chiếc Mazda 3 đỏ.',
     'sections': [{'heading': 'Diễn biến', 'paragraphs': [
         '— 14:42 camera cửa nhà C: DS. Vũ Quốc Bảo (áo blouse) đi ra phía bãi xe sau.',
         '— 14:44 camera bãi xe: xe Lead trắng biển dán băng dính đen vào bãi, dừng cạnh ô tô Mazda 3 màu đỏ biển 18A-2xx.xx.',
         '— 14:44 người phụ nữ áo chống nắng hồng xách một túi giấy, mở cửa, **ngồi vào ghế phụ** chiếc Mazda; Bảo đã ngồi ở ghế lái.',
         '— 14:52 người phụ nữ xuống xe, xách túi giấy, đi Lead ra cổng sau. 14:55 Bảo vào lại nhà C.',
         'Ô tô Mazda 3 đỏ biển 18A-2xx.xx đăng ký tên Vũ Quốc Bảo.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd16', 'stage': 3, 'type': 'note', 'title': 'Trích sổ xuất kho đông dược khoa Dược, tháng 11/2016',
     'paragraphs': ['Sổ ghi tay kho đông dược (chìa kho do trưởng, phó khoa giữ):',
                    '— 02/11 Xuất 1 kg đương quy cho khoa Y học cổ truyền (phiếu số 118).',
                    '— 09/11 Xuất 500 g hoàng kỳ cho khoa Y học cổ truyền (phiếu số 121).',
                    '__— 16/11 Xuất 200 g ô đầu chế "làm mẫu kiểm nghiệm". Không có số phiếu. Người xuất: Bảo.__',
                    '— 18/11 Kiểm kê: không ghi.',
                    'Ghi chú của điều tra viên: ô đầu chế còn trong kho 1,3 kg, khớp với việc đã xuất 200 g.'],
     'signature': 'Người giữ sổ: Trang'})

add({'id': 'd17', 'stage': 3, 'type': 'letter', 'title': 'Văn bản của khoa Y học cổ truyền và phòng Kiểm nghiệm',
     'date': 'Hưng Thái, ngày 22 tháng 11 năm 2016', 'greeting': 'Kính gửi: Đội Cảnh sát hình sự, Công an thị xã Hưng Thái',
     'paragraphs': ['Khoa Y học cổ truyền xác nhận: tháng 11/2016 khoa không đề nghị, không nhận ô đầu chế. Khoa chỉ dùng ô đầu trong rượu xoa bóp, đã có đủ từ tháng 6.',
                    'Phòng Kiểm nghiệm xác nhận: không nhận mẫu ô đầu nào trong năm 2016; mọi mẫu gửi kiểm nghiệm đều phải có phiếu.',
                    'Theo dược điển, ô đầu là vị thuốc độc bảng A; dịch chiết đặc chỉ cần vài mililit đã đủ gây tử vong.'],
     'signature': 'BS. Đào Thị Hiền, trưởng khoa Y học cổ truyền'})

add({'id': 'd18', 'stage': 3, 'type': 'evidence', 'title': 'Giám định nắp và tem decal cốc ô long kem còn nguyên',
     'code': 'TV-09', 'image': 'images/d05-nap-coc.webp', 'imageCaption': 'Lỗ kim ở mép nắp ép, nằm ngay dưới vị trí tem decal (phóng đại).',
     'fields': [{'label': 'Vật giám định', 'value': 'Cốc ô long kem còn nguyên thu trong tủ lạnh khoa Dược'},
                {'label': 'Cơ quan giám định', 'value': 'Phòng Kỹ thuật hình sự Công an tỉnh'}],
     'paragraphs': ['1. Màng nắp ép có **một lỗ kim** đường kính khoảng 0,4 mm ở mép, **nằm dưới tem decal** của quán. Tem đã bị **bóc ra rồi dán lại**: mặt keo có nếp gấp và bụi vải.',
                    '2. Trên mặt keo của tem thu được một dấu vân tay ngón cái phải rõ nét, **trùng khớp với vân tay mẫu của Vũ Quốc Bảo**.',
                    '3. Muốn bơm dưới tem phải bóc tem, tức là làm việc với từng cốc trước khi túi được dán kín. Túi giấy giao tới khoa còn nguyên băng dính (ảnh xác nhận giao hàng).']})

add({'id': 'd19', 'stage': 3, 'type': 'testimony', 'title': 'Biên bản ghi lời khai lần hai của Vũ Quốc Bảo',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '15 giờ 00 ngày 22/11/2016',
     'fields': [{'label': 'Người khai', 'value': 'Vũ Quốc Bảo, 33 tuổi'}],
     'lines': tl('Vũ Quốc Bảo',
         (DTV, 'Lúc 14 giờ 42 anh ra bãi xe làm gì?'),
         (None, 'Tôi ra ô tô lấy tập hồ sơ kiểm kê để quên.'),
         (DTV, 'Anh ở trên xe tám phút. Anh gặp ai?'),
         (None, 'Tôi ngồi một mình xem lại giấy tờ, không gặp ai cả.'),
         (DTV, 'Hai trăm gam ô đầu anh xuất ngày 16/11 đi đâu?'),
         (None, 'Tôi xuất cho khoa Y học cổ truyền ngâm rượu xoa bóp. Quên viết phiếu thôi.'),
         (DTV, 'Vân tay anh có trên mặt keo tem cốc ô long kem.'),
         (None, '(Im lặng một lúc) Chắc lúc tôi lên phòng giao ban có cầm cốc lên xem.'),
         (None, 'Tôi không có lý do gì hại anh Minh. Anh ấy đỡ đầu tôi lên phó khoa.')),
     'signature': 'Người khai: Vũ Quốc Bảo'})

add({'id': 'd20', 'stage': 3, 'type': 'report', 'title': 'Biên bản xác minh tại Công ty Phúc An chiều 18/11',
     'header': CA, 'heading': 'Biên bản xác minh', 'code': '58/XM', 'date': 'Ngày 22 tháng 11 năm 2016',
     'sections': [
         {'heading': '1. Lời nhân viên', 'paragraphs': ['Kế toán trưởng Lương Thị Mai: chiều 18/11 công ty không có cuộc họp quyết toán nào. Giám đốc Nhung rời văn phòng khoảng **13:20**, tự lái **chiếc Lead trắng của công ty**, khoảng 16:30 mới về.']},
         {'heading': '2. Camera toà nhà', 'paragraphs': ['Camera hầm xe ghi Nhung dắt xe Lead trắng ra lúc 13:21, đội mũ bảo hiểm, mang theo một túi vải; trở về 16:34. Xe Lead công ty khi về có vết băng dính còn dính ở biển số.']},
         {'heading': '3. Quãng đường', 'paragraphs': ['Từ văn phòng Phúc An tới Bệnh viện Hưng Thái khoảng 45 phút xe máy.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

# ───────────── Vòng 4: chiếc sim rác ─────────────
add({'id': 'd21', 'stage': 4, 'type': 'report', 'title': 'Trích kê thuê bao 09xx xxx 418 và thiết bị sử dụng',
     'header': ['Tổng công ty Viễn thông', 'Chi nhánh tỉnh'], 'heading': 'Trích kê theo yêu cầu cơ quan điều tra', 'code': '0711/VT', 'date': 'Ngày 23 tháng 11 năm 2016',
     'sections': [
         {'heading': '1. Thuê bao', 'paragraphs': ['Sim 09xx xxx 418 kích hoạt ngày 10/11/2016 tại một đại lý ở TP Nam Định, thông tin chủ thuê bao không có thật. Chỉ dùng từ 10/11 đến 18/11.']},
         {'heading': '2. Thiết bị', 'paragraphs': ['Sim 418 chỉ được lắp trong một máy có số **IMEI ...572**. Từ tháng 1 đến tháng 10/2016, chiếc máy IMEI ...572 này dùng sim **chính của Đinh Thị Hồng Nhung**.']},
         {'heading': '3. Liên lạc', 'paragraphs': ['— 16/11 đến 18/11: sim 418 gọi số của Vũ Quốc Bảo 5 lần (lần cuối 14:40 ngày 18/11, 32 giây).',
                                                  '— 18/11, 14:05: gọi quán trà sữa Mộc. 15:06–15:08: tạo tài khoản và đặt đơn giao hàng.',
                                                  '— Sau 15:10 ngày 18/11 sim 418 không còn hoạt động.']}],
     'signature': 'Phòng kỹ thuật: Trương Minh Đức'})

add({'id': 'd22', 'stage': 4, 'type': 'report', 'title': 'Sao kê chuyển tiền giữa Công ty Phúc An và gia đình Vũ Quốc Bảo',
     'header': ['Ngân hàng TMCP Hưng Long', 'Chi nhánh Nam Định'], 'heading': 'Sao kê theo yêu cầu cơ quan điều tra', 'code': 'HL-2216', 'date': 'Ngày 23 tháng 11 năm 2016',
     'sections': [{'heading': 'Tổng hợp', 'paragraphs': [
         'Từ tháng 11/2014 đến tháng 10/2016, tài khoản cá nhân Đinh Thị Hồng Nhung chuyển **16 lần, tổng 400.000.000đ** vào tài khoản của bà Trần Thị Hà (vợ Vũ Quốc Bảo), nội dung "tra no", "gop von".',
         'Mỗi lần chuyển đều trong vòng 5 ngày sau khi bệnh viện thanh toán một hợp đồng cho Phúc An.',
         'Ngày 19/11/2016 (thứ Bảy), tài khoản Nhung chuyển thêm 50.000.000đ, nội dung "gop von dot 17". Giao dịch bị ngân hàng giữ lại do tài khoản nhận đang bị phong toả theo yêu cầu cơ quan điều tra từ ngày 22/11.']}],
     'signature': 'Kiểm soát viên: Hoàng Thu Phương'})

add({'id': 'd23', 'stage': 4, 'type': 'report', 'title': 'Hồ sơ nghiệm thu gói vật tư 3,2 tỷ và đơn tố cáo nháp',
     'header': ['Bệnh viện Đa khoa thị xã Hưng Thái', 'Khoa Dược'], 'heading': 'Trích hồ sơ', 'code': 'KD-112', 'date': 'Ngày 23 tháng 11 năm 2016',
     'sections': [
         {'heading': '1. Biên bản nghiệm thu (chưa ký)', 'paragraphs': ['Gói vật tư tiêu hao 3,2 tỷ: hồ sơ ghi giao đủ 100%; kiểm đếm thực tế của khoa Dược chỉ đạt **54%**. Ô ký của trưởng khoa Dược để trống. Phó khoa Vũ Quốc Bảo **đã ký** ô "người kiểm đếm".']},
         {'heading': '2. Đơn báo cáo Sở Y tế (bản nháp trong máy tính ông Minh, sửa lần cuối 17/11)', 'paragraphs': ['Đề nghị thanh tra gói thầu; nêu tên Công ty Phúc An; ghi "đề nghị làm rõ trách nhiệm người đã ký kiểm đếm không đúng thực tế". Dự định gửi ngày 21/11.']},
         {'heading': '3. Ai biết đơn này', 'paragraphs': ['Lịch sử máy in khoa Dược: bản nháp được in một lần lúc 16:12 ngày 17/11 từ tài khoản "baovq".']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd24', 'stage': 4, 'type': 'testimony', 'title': 'Biên bản ghi lời khai lần hai của Đinh Thị Hồng Nhung',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 00 ngày 24/11/2016',
     'fields': [{'label': 'Người khai', 'value': 'Đinh Thị Hồng Nhung, 41 tuổi'}],
     'lines': tl('Đinh Thị Hồng Nhung',
         (DTV, 'Chị quan hệ thế nào với anh Vũ Quốc Bảo?'),
         (None, 'Anh Bảo là cán bộ phụ trách hồ sơ thầu, tôi làm việc với anh ấy ở phòng họp như mọi nhà cung cấp.'),
         (DTV, 'Ngoài công việc thì sao?'),
         (None, 'Không. Tôi không quen biết riêng gì anh Bảo, không có số điện thoại riêng của anh ấy.'),
         (DTV, 'Chiều 18/11 chị đi đâu bằng xe Lead của công ty?'),
         (None, 'Tôi đi gặp khách hàng ở ngoại thành. Khách nào thì tôi không tiện nói.'),
         (DTV, 'Chiếc điện thoại cũ IMEI đuôi 572 của chị đâu?'),
         (None, '(Im lặng) Tôi làm mất từ lâu rồi.'),
         (None, 'Tôi cần gặp luật sư.')),
     'signature': 'Người khai: Đinh Thị Hồng Nhung'})

# ───────────── Vòng 5: hai người, một ly trà ─────────────
add({'id': 'd25', 'stage': 5, 'type': 'report', 'title': 'Biên bản khám xét nơi ở của Vũ Quốc Bảo',
     'header': CA, 'heading': 'Biên bản khám xét', 'code': '61/KX', 'date': '07 giờ 00 ngày 25/11/2016',
     'image': 'images/d25-tang-vat-nha-bao.webp', 'imageCaption': 'Tang vật số 1: lọ dịch chiết, hai xi lanh 1 ml và mẩu tem decal rách góc.',
     'sections': [
         {'heading': 'Đồ vật thu giữ', 'paragraphs': [
             '— Trong ngăn dưới tủ giày: một lọ thuỷ tinh nâu 30 ml còn khoảng 8 ml **dịch màu nâu sẫm**; giám định sơ bộ: dịch chiết ô đầu, hàm lượng aconitine rất cao.',
             '— Cùng ngăn: hai xi lanh 1 ml kim 30G, trong ống còn dính dịch nâu.',
             '— Trong xe Mazda 3 đỏ, khe ghế phụ: **một mẩu tem decal tròn in logo quán Mộc** bị rách góc.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd26', 'stage': 5, 'type': 'report', 'title': 'Biên bản khám xét xe Lead và văn phòng Công ty Phúc An',
     'header': CA, 'heading': 'Biên bản khám xét', 'code': '62/KX', 'date': '07 giờ 30 ngày 25/11/2016',
     'image': 'images/d26-tang-vat-xe-lead.webp', 'imageCaption': 'Tang vật thu trong cốp xe Lead và ngăn kéo giám đốc Phúc An.',
     'sections': [
         {'heading': 'Đồ vật thu giữ', 'paragraphs': [
             '— Cốp xe Lead trắng của công ty: một áo chống nắng màu hồng có mũ trùm, một kính râm, một cuộn băng dính đen đã dùng một phần.',
             '— Ngăn kéo khoá của giám đốc: một điện thoại cũ IMEI ...572, không có sim; khe sim còn vết xước mới.',
             '— Máy tính giám đốc: file "thiep.docx" sửa lần cuối 17/11 lúc 21:40, nội dung "Gửi anh Minh và các em khoa Dược. Cảm ơn cả khoa! Phòng Vật tư".']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd27', 'stage': 5, 'type': 'report', 'title': 'Trích tin nhắn khôi phục từ điện thoại của Vũ Quốc Bảo',
     'header': ['Phòng Kỹ thuật hình sự', 'Công an tỉnh'], 'heading': 'Kết quả khôi phục dữ liệu', 'code': '64/KP', 'date': 'Ngày 26 tháng 11 năm 2016',
     'sections': [{'heading': 'Tin nhắn với số 09xx xxx 418 (đã bị xoá, khôi phục được)', 'paragraphs': [
         '— 16/11, 21:02, 418: "Đơn đó mà lên Sở thì em cũng không thoát đâu."',
         '— 16/11, 21:10, Bảo: "Em biết. Thứ Sáu anh ấy uống ô long kem."',
         '— 17/11, 22:15, 418: "Thiệp chị in rồi. Em chuẩn bị đồ đi."',
         '— 18/11, 14:40, 418: "Chị tới bãi xe rồi. Chỉ hai cốc ô long thôi."',
         '— 18/11, 16:20, Bảo: "Anh ấy họp chưa về. Để tủ lạnh rồi."',
         '— 19/11, 11:02, Bảo: "Con Hân uống rồi. Không phải anh ấy."']}],
     'signature': 'Kỹ thuật viên: Thượng uý Phan Văn Hưng'})

CARDS = ['nhung', 'bao', 'son', 'tai']
Q = [
    {'id': 'q1', 'stage': 1, 'type': 'choice', 'title': 'Cốc trà dành cho ai?',
     'prompt': 'Chị Hân chết sau khi uống cốc trà sữa trong tủ lạnh. Dựa vào hồ sơ đang mở, nhận định nào đứng vững?',
     'options': ['Chị Hân là mục tiêu: ai đó biết chị trực sáng thứ Bảy và sẽ uống trà để lại trong tủ lạnh.',
                 'Mục tiêu là DS. Phạm Đức Minh: thiệp gửi đích danh ông, cốc ô long kem là món của riêng ông, và những người uống các vị khác không ai sao.'],
     'answer': [1],
     'nudges': {'0': {'message': 'Thiệp ghi gửi ai? Cốc ô long kem là món của ai? Ai uống các cốc khác chiều thứ Sáu?'}},
     'hints': ['Đọc tấm thiệp và lời khai của đồng nghiệp chị Hân.', 'Những ai đã uống trà chiều thứ Sáu, uống vị gì?',
               'd02: thiệp "Gửi anh Minh…". d05: ô long kem là món ông Minh uống mỗi thứ Sáu, các vị khác ba người uống không sao. d06: ông Minh không về khoa chiều đó.'],
     'solved': 'Cốc trà nhắm vào trưởng khoa Dược. Chị Hân chết thay ông.',
     'explanation': [{'title': 'Thiệp', 'body': ['d02: "Gửi anh Minh và các em khoa Dược".']},
                     {'title': 'Món của ông Minh', 'body': ['d05, d06: ô long kem là món ông Minh uống chiều thứ Sáu; ba người uống trân châu, trà đào không sao.']},
                     {'title': 'Ngẫu nhiên', 'body': ['d06: ông Minh họp ở Sở tới 17:40 rồi về thẳng nhà; d05: sáng thứ Bảy chị Hân trực nên lấy một cốc ô long kem.']}]},
    {'id': 'q2', 'stage': 1, 'type': 'choice', 'multiple': True, 'cards': CARDS, 'title': 'Ai biết thói quen của trưởng khoa?',
     'prompt': 'Người gửi trà biết chính xác món ông Minh uống. Chọn **tất cả** những người trong danh sách được hồ sơ cho thấy là biết thói quen ô long kem của ông.',
     'options': ['Đinh Thị Hồng Nhung', 'Vũ Quốc Bảo', 'Hoàng Văn Sơn', 'Lý Văn Tài'], 'answer': [0, 1],
     'nudges': {'2': {'message': 'Anh Sơn từng lên khoa to tiếng. Có tài liệu nào cho thấy anh biết ông Minh uống gì không?'},
                '3': {'message': 'Tài xế không quen ai ở khoa Dược (d10, vòng sau). Ở vòng này, có tài liệu nào nói anh biết?'}},
     'hints': ['Chính ông Minh nói ai biết.', 'Đọc lời khai ông Minh: ai đặt trà hộ, ai từng mang đúng món đó tới.',
               'd06 dòng 2: Bảo thường đặt hộ; bà Nhung tháng Chín mang đúng hai cốc ô long kem tới, nói "nghe nói anh thích món này".'],
     'solved': 'Một người trong khoa và một người ngoài khoa biết món trà của ông Minh.',
     'explanation': [{'title': 'Bảo', 'body': ['d06: phó khoa thường đặt trà hộ trưởng khoa.']},
                     {'title': 'Nhung', 'body': ['d06: tháng Chín mang tới đúng ô long kem. Bà còn đang vướng nghiệm thu 3,2 tỷ mà ông Minh không ký.']},
                     {'title': 'Chưa đủ', 'body': ['Biết thói quen chưa phải là bằng chứng. Ai đặt túi trà?']}]},
    {'id': 'q3', 'stage': 2, 'type': 'line', 'title': 'Tin nhắn "Ông sẽ phải trả giá"',
     'prompt': 'Một người mới được hỏi đã chối một việc mà tài liệu ở vòng trước xác nhận. Chỉ ra dòng khai đó.',
     'answer': ['d11:004'],
     'nudges': {'d11:006': {'message': 'Ca làm ở cảng sẽ được kiểm tra riêng. Tìm câu chối một việc đã có người xác nhận.'},
                'd14:004': {'near': True, 'message': 'Câu này của bà Nhung cũng đáng ngờ, nhưng chưa có tài liệu nào bác nó ở vòng này.'}},
     'hints': ['So lời khai anh Sơn với lời ông Minh.', 'Ông Minh nói ông còn giữ thứ gì của anh Sơn?',
               'd11 dòng 4: "chưa bao giờ nhắn tin". d06 dòng 7: ông Minh còn giữ tin nhắn "Ông sẽ phải trả giá".'],
     'solved': 'Anh Sơn đã nhắn tin dọa, rồi chối. Nhưng dọa và giết là hai chuyện khác nhau.',
     'explanation': [{'title': 'Câu khai', 'body': ['d11 dòng 4: chưa bao giờ nhắn tin cho ông Minh, không có số.']},
                     {'title': 'Bị bác', 'body': ['d06 dòng 7: ông Minh còn giữ tin nhắn "Ông sẽ phải trả giá".']},
                     {'title': 'Nhưng', 'body': ['Anh Sơn biết ông Minh uống gì không? Chiều 18/11 anh ở đâu?']}]},
    {'id': 'q4', 'stage': 2, 'type': 'evidence', 'need': 2, 'title': 'Người dọa và người giao',
     'prompt': 'Ghim 2 tài liệu khách quan loại trừ anh Sơn và anh Tài khỏi việc đầu độc túi trà.',
     'answer': ['d09', 'd12'],
     'nudges': [{'any': ['d10', 'd11'], 'message': 'Đó là lời tự khai. Tìm tài liệu do bên thứ ba lập.'},
                {'any': ['d13'], 'near': True, 'message': 'Hoá đơn quán cho thấy ai nhận trà. Còn cần chứng minh anh Tài không mở túi, và anh Sơn ở đâu.'}],
     'hints': ['Một tài liệu về hành trình chiếc túi, một tài liệu về nơi anh Sơn làm việc.', 'Túi có dừng ở đâu, có bị mở không? Anh Sơn quẹt thẻ ở đâu?',
               'd09: tài xế đi liên tục 15:15–15:24, túi dán kín khi giao. d12: Sơn quẹt thẻ ở cảng 13:52–22:07, cách bệnh viện 9 km.'],
     'solved': 'Anh Tài chỉ mang một túi đã dán kín. Anh Sơn ở cảng suốt chiều.',
     'explanation': [{'title': 'Anh Tài', 'body': ['d09: nhận 15:15, di chuyển không dừng, giao 15:27; ảnh xác nhận túi còn băng dính.']},
                     {'title': 'Anh Sơn', 'body': ['d12: chấm công và camera cảng 13:52–22:07.']},
                     {'title': 'Người thật sự', 'body': ['d10, d13: người phụ nữ áo chống nắng hồng, đi Lead trắng che biển.']}]},
    {'id': 'q5', 'stage': 2, 'type': 'evidence', 'need': 2, 'title': 'Một số máy, hai cuộc gọi',
     'prompt': 'Ghim 2 tài liệu cho thấy người đặt trà ở quán và người đặt giao hàng là một.',
     'answer': ['d09', 'd13'],
     'nudges': [{'any': ['d10'], 'near': True, 'message': 'Lời anh Tài tả người phụ nữ. Cần tài liệu ghi số máy đặt hàng.'}],
     'hints': ['Hai việc: đặt trà ở quán, đặt người giao. Mỗi việc dùng số máy nào?', 'So số điện thoại trên hoá đơn quán và trên đơn giao hàng.',
               'd13: đặt trà 14:05 từ số 09xx xxx 418. d09: tài khoản "Hoa" số 09xx xxx 418 đặt giao 15:08. Cùng một số, cùng một người áo hồng.'],
     'solved': 'Một số máy duy nhất vừa đặt trà vừa đặt giao. Giữa 14:30 và 15:08, túi trà đã ở đâu?',
     'explanation': [{'title': 'Đặt trà', 'body': ['d13: số 09xx xxx 418 gọi đặt lúc 14:05; 14:30 phụ nữ áo hồng nhận, dặn "dán tem kỹ".']},
                     {'title': 'Đặt giao', 'body': ['d09: cùng số 418 tạo tài khoản "Hoa" lúc 15:06, đặt giao từ quán Lá Me lúc 15:08.']},
                     {'title': 'Khoảng trống', 'body': ['Quán Mộc cách bệnh viện 300 m. 38 phút giữa 14:30 và 15:08 túi trà ở đâu?']}]},
    {'id': 'q6', 'stage': 3, 'type': 'evidence', 'need': 2, 'title': 'Người cầm kim',
     'prompt': 'Ghim 2 tài liệu cho thấy ai đã lấy chất độc và trực tiếp bơm vào cốc ô long kem.',
     'answer': ['d16', 'd18'],
     'nudges': [{'any': ['d15'], 'near': True, 'message': 'Camera cho thấy hai người gặp nhau. Cần tài liệu về chất độc và về chiếc cốc.'},
                {'any': ['d17'], 'near': True, 'message': 'Văn bản này bác lời giải thích về ô đầu. Tài liệu nào cho thấy ai đã lấy nó ra khỏi kho?'}],
     'hints': ['Một tài liệu về nguồn chất độc, một tài liệu về chiếc cốc.', 'Ai xuất ô đầu khỏi kho? Ai để lại dấu vết dưới tem?',
               'd16: Bảo xuất 200 g ô đầu ngày 16/11, không phiếu. d18: lỗ kim dưới tem, tem bóc ra dán lại, vân tay Bảo trên mặt keo.'],
     'solved': 'Vũ Quốc Bảo lấy ô đầu từ kho và bơm vào hai cốc ô long kem.',
     'explanation': [{'title': 'Nguồn độc', 'body': ['d16: 16/11 Bảo xuất 200 g ô đầu chế không phiếu; d17: không khoa nào nhận.']},
                     {'title': 'Chiếc cốc', 'body': ['d18: lỗ kim dưới tem, tem bóc ra dán lại, vân tay ngón cái của Bảo trên mặt keo.']},
                     {'title': 'Ở đâu', 'body': ['d15: 14:44–14:52 người phụ nữ áo hồng ngồi trên ô tô của Bảo với túi trà.']}]},
    {'id': 'q7', 'stage': 3, 'type': 'line', 'title': 'Tám phút trên chiếc Mazda',
     'prompt': 'Chỉ ra dòng khai của Bảo bị camera bãi xe bác bỏ.',
     'answer': ['d19:004'],
     'nudges': {'d19:002': {'near': True, 'message': 'Câu này về lý do ra xe. Tìm câu nói về việc gặp ai.'},
                'd19:006': {'near': True, 'message': 'Câu về ô đầu bị khoa Y học cổ truyền bác. Câu hỏi này về camera.'}},
     'hints': ['Camera ghi gì trong 8 phút Bảo ngồi trên xe?', 'Ai ngồi vào ghế phụ?', 'd19 dòng 4: "không gặp ai cả". d15: người phụ nữ áo hồng ngồi ghế phụ 14:44–14:52.'],
     'solved': 'Bảo không ngồi một mình. Người phụ nữ áo hồng đã mang túi trà lên xe anh.',
     'explanation': [{'title': 'Câu khai', 'body': ['d19 dòng 4: ngồi một mình, không gặp ai.']},
                     {'title': 'Bị bác', 'body': ['d15: 14:44 phụ nữ áo hồng xách túi giấy ngồi vào ghế phụ; 14:52 xuống xe.']},
                     {'title': 'Liên hệ', 'body': ['d21 (vòng sau) sẽ cho biết ai gọi Bảo lúc 14:40.']}]},
    {'id': 'q8', 'stage': 3, 'type': 'line', 'title': 'Buổi chiều ở văn phòng',
     'prompt': 'Một người khác cũng nói dối về nơi mình ở chiều 18/11. Chỉ ra dòng khai đó.',
     'answer': ['d14:004'],
     'nudges': {'d14:006': {'near': True, 'message': 'Câu này cũng sai (d06), nhưng câu hỏi này về nơi ở chiều 18/11.'}},
     'hints': ['Ai khai ở văn phòng cả chiều?', 'Kế toán và camera hầm xe Phúc An nói gì?',
               'd14 dòng 4: ở văn phòng Nam Định cả chiều, họp kế toán. d20: không có cuộc họp; Nhung đi Lead trắng của công ty từ 13:21 tới 16:34, biển số dính băng dính.'],
     'solved': 'Bà Nhung rời văn phòng bằng chiếc Lead trắng đúng khung giờ người phụ nữ áo hồng xuất hiện ở Hưng Thái.',
     'explanation': [{'title': 'Câu khai', 'body': ['d14 dòng 4: ở văn phòng Nam Định cả buổi chiều, họp với kế toán.']},
                     {'title': 'Bị bác', 'body': ['d20: không có cuộc họp; 13:21–16:34 bà đi Lead trắng của công ty; biển số có vết băng dính.']},
                     {'title': 'Khớp giờ', 'body': ['45 phút đường: 14:05 gọi quán, 14:30 nhận trà, 14:44 tới bãi xe, 15:08 đặt giao, rồi về Nam Định 16:34.']}]},
    {'id': 'q9', 'stage': 4, 'type': 'evidence', 'need': 2, 'title': 'Chủ nhân sim rác',
     'prompt': 'Ghim 2 tài liệu chứng minh sim 09xx xxx 418 là của bà Nhung.',
     'answer': ['d21', 'd20'],
     'nudges': [{'any': ['d22'], 'near': True, 'message': 'Sao kê cho thấy tiền đi đâu. Cần tài liệu nối chiếc sim với người dùng nó.'},
                {'any': ['d13', 'd09'], 'message': 'Tài liệu này dùng số 418, nhưng không nói ai cầm máy.'}],
     'hints': ['Sim được lắp trong máy nào? Máy đó trước đây dùng sim của ai?', 'Một tài liệu về thiết bị, một tài liệu về hành tung chủ thiết bị đúng giờ sim hoạt động.',
               'd21: sim 418 chỉ lắp trong máy IMEI ...572, máy này trước dùng sim chính của Nhung. d20: Nhung vắng mặt 13:21–16:34, đúng giờ sim 418 gọi quán và đặt giao.'],
     'solved': 'Chiếc sim rác nằm trong điện thoại cũ của bà Nhung.',
     'explanation': [{'title': 'Thiết bị', 'body': ['d21: sim 418 chỉ chạy trên máy IMEI ...572, máy dùng sim chính của Nhung tới tháng 10.']},
                     {'title': 'Thời gian', 'body': ['d21: 14:05, 15:06–15:08, 14:40 gọi Bảo. d20: Nhung vắng văn phòng 13:21–16:34.']},
                     {'title': 'Liên lạc', 'body': ['d21: sim 418 gọi Bảo 5 lần từ 16/11, lần cuối 14:40 ngày 18/11.']}]},
    {'id': 'q10', 'stage': 4, 'type': 'line', 'title': 'Người lạ ở phòng họp',
     'prompt': 'Chỉ ra dòng khai của bà Nhung bị tài liệu ở vòng này bác bỏ về quan hệ với Bảo.',
     'answer': ['d24:004'],
     'nudges': {'d24:002': {'near': True, 'message': 'Câu này mới chỉ mô tả công việc. Tìm câu phủ nhận dứt khoát.'},
                'd24:006': {'near': True, 'message': 'Câu về chuyến đi chiều 18/11. Câu hỏi này về quan hệ với Bảo.'}},
     'hints': ['Hai năm qua tiền từ tài khoản bà Nhung đi đâu?', 'Sim của bà gọi ai 5 lần?',
               'd24 dòng 4: "không quen biết riêng, không có số". d22: 16 lần chuyển 400 triệu vào tài khoản vợ Bảo. d21: sim 418 gọi Bảo 5 lần.'],
     'solved': 'Bốn trăm triệu trong hai năm, năm cuộc gọi trong ba ngày. Bà Nhung và Bảo không phải người lạ.',
     'explanation': [{'title': 'Câu khai', 'body': ['d24 dòng 4: không quen riêng Bảo, không có số điện thoại riêng.']},
                     {'title': 'Tiền', 'body': ['d22: 16 lần, 400 triệu vào tài khoản vợ Bảo, luôn sau khi bệnh viện thanh toán cho Phúc An.']},
                     {'title': 'Động cơ chung', 'body': ['d23: Bảo ký kiểm đếm khống; đơn tố cáo của ông Minh đòi làm rõ người ký kiểm đếm; Bảo in đơn nháp ngày 17/11.']}]},
    {'id': 'q-accuse', 'stage': 5, 'type': 'choice', 'multiple': True, 'cards': CARDS, 'title': 'Chỉ mặt hung thủ và đồng phạm',
     'prompt': 'Cái chết của chị Hân là việc của hơn một người. Chọn **đúng hai** người đã cùng chuẩn bị ly trà độc.',
     'options': ['Đinh Thị Hồng Nhung', 'Vũ Quốc Bảo', 'Hoàng Văn Sơn', 'Lý Văn Tài'], 'answer': [0, 1],
     'nudges': {'2': {'message': 'Anh Sơn ở cảng suốt chiều 18/11 (d12).'},
                '3': {'message': 'Anh Tài chỉ mang một túi đã dán kín; độc nằm dưới tem quán (d09, d18).'}},
     'hints': ['Một người cần biết thói quen, có chất độc, có kim; một người cần đặt trà, có sim rác, có tiền.',
               'Ai ngồi cùng nhau trên chiếc Mazda lúc 14:44?', 'Nhung: sim 418, xe Lead, áo hồng, thiệp (d20, d21, d26). Bảo: ô đầu, vân tay, xi lanh, tin nhắn (d16, d18, d25, d27).'],
     'solved': 'Đinh Thị Hồng Nhung và Vũ Quốc Bảo.',
     'explanation': [{'title': 'Nhung', 'body': ['Sim rác trong máy cũ của bà (d21), đặt trà và đặt giao (d13, d09), áo hồng và thiệp trong máy tính (d26).']},
                     {'title': 'Bảo', 'body': ['Lấy ô đầu (d16), vân tay dưới tem (d18), dịch chiết và xi lanh ở nhà (d25), tin nhắn khôi phục (d27).']},
                     {'title': 'Vì sao', 'body': ['Đơn tố cáo của ông Minh (d23) sẽ làm lộ gói thầu khống và 400 triệu hoa hồng (d22).']}]},
    {'id': 'q11', 'stage': 5, 'type': 'choice', 'title': 'Kết luận điều tra',
     'prompt': 'Chọn bản kết luận đúng với hồ sơ ở mọi chi tiết: ai, bằng cách nào, đã nhắm vào ai và vì sao.',
     'options': [
         'Bà Nhung dùng sim rác đặt sáu cốc trà, mang lên ô tô của Bảo ở bãi xe bệnh viện; Bảo bóc tem hai cốc ô long kem, bơm dịch ô đầu lấy từ kho khoa Dược rồi dán lại; bà Nhung thuê người giao tới khoa kèm thiệp giả danh Phòng Vật tư. Mục tiêu là ông Minh, người sắp tố cáo gói thầu khống; chị Hân uống nhầm.',
         'Bảo một mình mua sáu cốc trà, bơm dịch ô đầu vào cả sáu cốc ngay tại phòng giao ban lúc 15 giờ 30 chiều thứ Sáu để hại ông Minh, rồi in thiệp giả danh Phòng Vật tư; ba người uống chiều hôm đó may mắn uống phải cốc ít độc; bà Nhung không liên quan, chỉ bị Bảo lợi dụng tên công ty để đánh lạc hướng.',
         'Anh Sơn thuê một người phụ nữ mặc áo chống nắng hồng đặt trà bằng sim rác, rồi trả tiền cho tài xế Tài mở túi, bơm thuốc trừ sâu vào hai cốc ô long kem trên đường giao để trả thù ông Minh về cái chết của bố tháng Mười; Bảo và bà Nhung bị nghi oan chỉ vì chuyện nghiệm thu gói thầu.',
         'Bà Nhung tự tay bơm dịch ô đầu mua ngoài chợ vào hai cốc ô long kem khi ngồi ở quán Lá Me, dán lại tem rồi thuê người giao tới khoa kèm thiệp giả danh Phòng Vật tư để hại ông Minh; Bảo không biết gì, chỉ tình cờ gặp bà ở bãi xe để bàn chuyện nghiệm thu gói thầu.'],
     'answer': [0],
     'exam': {'examiner': 'Kiểm sát viên Đỗ Thị Thanh Hương',
              'intro': 'Trình bày kết luận trước kiểm sát viên: trả lời lần lượt từng câu hỏi bằng lời của mình. Không dùng được AI thì bấm “Trả lời bằng trắc nghiệm” để chọn bản kết luận đúng.'},
     'nudges': {'1': {'message': 'Chỉ hai cốc ô long kem có độc (d08), và túi giao tới còn dán kín (d09).'},
                '2': {'message': 'Anh Sơn ở cảng (d12); độc nằm dưới tem quán, túi còn băng dính (d18, d09).'},
                '3': {'message': 'Vân tay dưới tem là của Bảo (d18), Bảo lấy ô đầu (d16), tin nhắn (d27).'}},
     'hints': ['Đối chiếu từng phương án với: cốc nào có độc (d08), ai bơm (d18), túi ở đâu lúc 14:44 (d15).',
               'Chỉ một phương án có hai người cùng hành động và đúng hai cốc.', 'Phương án A.'],
     'solved': 'Hồ sơ khép lại với hai cái tên: Đinh Thị Hồng Nhung và Vũ Quốc Bảo.',
     'explanation': [{'title': 'Cách làm', 'body': ['Nhung đặt trà và đặt giao bằng sim rác (d13, d09, d21); Bảo bơm ô đầu dưới tem hai cốc ô long kem trên ô tô (d15, d16, d18).']},
                     {'title': 'Nhắm vào ai', 'body': ['Thiệp gửi ông Minh, ô long kem là món của ông (d02, d05, d06); tin nhắn "Chỉ hai cốc ô long thôi" (d27).']},
                     {'title': 'Vì sao', 'body': ['Đơn tố cáo gói thầu khống 3,2 tỷ, đòi làm rõ người ký kiểm đếm (d23); 400 triệu hoa hồng (d22).']}]},
]

case = {
    'id': CID, 'no': 13, 'status': 'available',
    'title': 'Ly trà tráo độc',
    'subtitle': 'Một túi trà sữa "cảm ơn", hai cốc ô long kem, và người uống nhầm',
    'tagline': 'Túi trà sữa gửi trưởng khoa Dược chiều thứ Sáu. Sáng thứ Bảy, người uống nó là một cô gái không liên quan.',
    'difficulty': 5, 'players': '2–6', 'duration': '120–150 phút',
    'setting': 'Bệnh viện Đa khoa thị xã Hưng Thái (hư cấu)', 'era': 'Tháng 11/2016',
    'tags': ['Án mạng', 'Đầu độc', 'Đồng phạm', 'Bệnh viện'], 'cover': 'images/cover.webp',
    'contentWarning': 'Hồ sơ có mô tả cái chết do ngộ độc. Mọi nhân vật, cơ quan, địa danh và tình tiết đều hư cấu.',
    'synopsis': ['Chiều thứ Sáu 18/11/2016, một túi sáu cốc trà sữa được giao tới khoa Dược Bệnh viện Đa khoa thị xã Hưng Thái, kèm tấm thiệp "cảm ơn" gửi trưởng khoa.',
                 'Sáng hôm sau, kỹ thuật viên Lê Thị Ngọc Hân lấy một cốc trong tủ lạnh ra uống. Hai tiếng sau chị qua đời. Cốc trà đó chưa bao giờ dành cho chị.'],
    'intro': {'title': 'Ly trà tráo độc',
              'paragraphs': ['Sáng 19/11/2016, chị Lê Thị Ngọc Hân (27 tuổi), kỹ thuật viên khoa Dược Bệnh viện Đa khoa thị xã Hưng Thái, uống một cốc trà sữa ô long kem lấy từ tủ lạnh phòng giao ban. Mười lăm phút sau chị tê lưỡi, nôn, ngất. Chị mất lúc 10 giờ 15.',
                             'Túi trà sữa được giao tới khoa chiều hôm trước, kèm tấm thiệp ký tên Phòng Vật tư. Ba người đã uống các cốc khác mà không sao. Phòng Vật tư nói chưa từng gửi gì.',
                             'Bạn là điều tra viên Đội Cảnh sát hình sự Công an thị xã Hưng Thái. Hãy tìm ra cốc trà dành cho ai, ai đã chuẩn bị nó, và vì sao.'],
              'objective': 'Tìm ra ai đã tẩm độc cốc trà, bằng cách nào túi trà tới được khoa Dược, người bị nhắm tới là ai, và vì sao.'},
    'victim': {'id': 'han', 'name': 'Lê Thị Ngọc Hân', 'age': 27, 'role': 'Kỹ thuật viên khoa Dược', 'image': 'images/id-han.webp',
               'note': 'Tử vong sáng 19/11/2016 sau khi uống một cốc trà sữa ô long kem trong tủ lạnh phòng giao ban khoa Dược.'},
    'suspects': [
        {'id': 'nhung', 'name': 'Đinh Thị Hồng Nhung', 'age': 41, 'role': 'Giám đốc Công ty Thiết bị y tế Phúc An', 'image': 'images/id-nhung.webp', 'voice': 'F3',
         'suspicion': 'Đang vướng nghiệm thu gói vật tư 3,2 tỷ mà trưởng khoa Dược không chịu ký.'},
        {'id': 'bao', 'name': 'Vũ Quốc Bảo', 'age': 33, 'role': 'Phó trưởng khoa Dược', 'image': 'images/id-bao.webp', 'voice': 'M2',
         'suspicion': 'Thường đặt trà hộ trưởng khoa, biết rõ thói quen của ông. Ở bệnh viện suốt chiều thứ Sáu.'},
        {'id': 'son', 'name': 'Hoàng Văn Sơn', 'age': 45, 'role': 'Người nhà bệnh nhân', 'image': 'images/id-son.webp', 'voice': 'M5',
         'suspicion': 'Bố mất ở bệnh viện tháng Mười; từng lên khoa Dược to tiếng và dọa trưởng khoa.'},
        {'id': 'tai', 'name': 'Lý Văn Tài', 'age': 24, 'role': 'Tài xế giao hàng', 'image': 'images/id-tai.webp', 'voice': 'M1',
         'suspicion': 'Người mang túi trà vào khoa Dược chiều 18/11.'}],
    'aiInterrogation': True,
    'audio': {'intro': 'audio/intro.mp3', 'finale': 'audio/finale.mp3'},
    'documents': D,
    'questions': Q,
    'beats': [
        {'stage': 2, 'kicker': 'Ngày 21/11/2016 · Công an thị xã Hưng Thái', 'title': 'Người phụ nữ áo hồng', 'voice': 'audio/beat-2.mp3',
         'paragraphs': ['Cốc trà dành cho trưởng khoa Dược. Và chỉ hai người được biết là biết món trà của ông.',
                        'Đại uý Đăng cho người tới quán trà sữa Mộc, công ty giao hàng và cảng Hưng Thái. Viện Khoa học hình sự gửi kết quả xét nghiệm về lúc chiều.',
                        'Ai đã gọi điện đặt sáu cốc trà? Và ai cầm chúng trong tay trước khi túi được dán kín?']},
        {'stage': 3, 'kicker': 'Ngày 22/11/2016 · Phòng camera Bệnh viện Hưng Thái', 'title': 'Tám phút trong bãi xe', 'voice': 'audio/beat-3.mp3',
         'paragraphs': ['Từ quán Mộc tới bệnh viện chỉ ba trăm mét. Vậy mà túi trà mất ba mươi tám phút mới tới tay người giao hàng.',
                        'Nhân viên bảo vệ tua lại camera bãi xe phía sau nhà C. "Chiếc Lead trắng kia, biển dán băng dính đen."',
                        'Chiếc ô tô màu đỏ bên cạnh là của ai?']},
        {'stage': 4, 'kicker': 'Ngày 23/11/2016 · Công an thị xã Hưng Thái', 'title': 'Chiếc sim rác', 'voice': 'audio/beat-4.mp3',
         'paragraphs': ['Một số điện thoại chỉ sống tám ngày, gọi đúng ba nơi: quán trà, công ty giao hàng, và một dược sĩ.',
                        'Nhà mạng gửi về một dãy số IMEI. Ngân hàng gửi về một bản sao kê dài hai năm.',
                        'Người phụ nữ áo hồng là ai, và bà đã trả cho Bảo bao nhiêu?']},
        {'stage': 5, 'kicker': 'Ngày 25/11/2016 · Khám xét khẩn cấp', 'title': 'Hai người, một ly trà', 'voice': 'audio/beat-5.mp3',
         'paragraphs': ['Lệnh khám xét được ký lúc sáu giờ sáng. Hai tổ công tác đi hai hướng: một tới căn hộ của Vũ Quốc Bảo, một tới Công ty Phúc An ở Nam Định.',
                        '"Tôi cần gặp luật sư." Đó là câu cuối cùng bà Nhung nói hôm trước.',
                        'Chỉ mặt cả hai người. Và giải thích vì sao.']}],
    'finale': {'title': 'Ly trà tráo độc',
               'paragraphs': ['Ngày 26/11/2016, Vũ Quốc Bảo khai trước. Anh ngồi rất lâu nhìn mẩu tem decal rách góc tìm thấy trong xe mình, rồi nói: "Tôi chỉ định để anh ấy nằm viện vài hôm, không kịp gửi đơn."',
                              'Hai năm, bốn trăm triệu. Mỗi lần bệnh viện thanh toán cho Phúc An, tài khoản vợ Bảo lại nhận một khoản "góp vốn". Khi ông Minh không chịu ký nghiệm thu gói vật tư giao thiếu gần một nửa, Bảo là người in tờ đơn tố cáo nháp đưa cho bà Nhung xem.',
                              'Bà Nhung mua sim rác, in tấm thiệp giả danh Phòng Vật tư. Chiều thứ Sáu, bà mặc áo chống nắng hồng, đi chiếc Lead của công ty, đặt sáu cốc trà và mang lên ô tô của Bảo. Bảo bóc tem hai cốc ô long kem, bơm dịch ô đầu chiết từ kho đông dược, dán tem lại.',
                              'Ông Minh họp ở Sở Y tế tới gần sáu giờ và về thẳng nhà. Hai cốc trà nằm trong tủ lạnh suốt đêm. Sáng thứ Bảy, Hân trực một mình.',
                              'Tin nhắn cuối cùng Bảo gửi cho chiếc sim rác chỉ có một dòng: "Con Hân uống rồi. Không phải anh ấy."',
                              'Bà Nhung nghe kết luận, hỏi luật sư một câu duy nhất: "Gói thầu đó có bị huỷ không?"']},
    'epilogue': [
        {'title': 'Đinh Thị Hồng Nhung', 'text': 'Bị truy tố về tội giết người với vai trò chủ mưu và tội đưa hối lộ. Công ty Phúc An bị cấm tham gia đấu thầu ngành y tế.'},
        {'title': 'Vũ Quốc Bảo', 'text': 'Bị truy tố về tội giết người và nhận hối lộ. Bộ Y tế thu hồi chứng chỉ hành nghề dược.'},
        {'title': 'Phạm Đức Minh', 'text': 'Gửi đơn tố cáo đúng hẹn. Gói thầu 3,2 tỷ bị huỷ. Ông xin thôi chức trưởng khoa sau đám tang của Hân.'},
        {'title': 'Hoàng Văn Sơn', 'text': 'Đến thắp hương cho Hân, gửi lời xin lỗi tới ông Minh về những tin nhắn tháng Mười.'}],
}

for person in [case['victim'], *case['suspects']]:  # ảnh thẻ chưa có thì để khung trống
    if person.get('image') and not os.path.exists(f'public/cases/{CID}/' + person['image']):
        print('chưa có ảnh:', person['image']); del person['image']
for d in D:  # ảnh tư liệu chưa vẽ thì bỏ trường ảnh
    if d.get('image') and not os.path.exists(f'public/cases/{CID}/' + d['image']):
        print('chưa có ảnh:', d['image']); del d['image']
        if d['type'] == 'scan': d['type'] = 'note'; d['paragraphs'] = [d.pop('caption')]
json.dump(case, open(f'public/cases/{CID}/case.json', 'w'), ensure_ascii=False, indent=2)
open(f'public/cases/{CID}/case.json', 'a').write('\n')
print(len(D), 'docs', len(Q), 'questions')
