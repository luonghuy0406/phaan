"""Dựng public/cases/mua-dong-binh-ty/case.json (bản 2, độ khó vừa). Chạy ở thư mục gốc:
python3 authoring/mua-dong-binh-ty/build_case.py

Lời giải: Lê Khắc Toàn, trưởng ban đại diện cư dân kiêm thủ kho thanh lý trạm xá. Xem bible.md.
"""
import json
import os

CID = 'mua-dong-binh-ty'
CA = ['Công an quận Hai Bà Trưng', 'Đội Điều tra hình sự']
DTV = 'Điều tra viên'
DTV_NAME = 'Đại uý Phạm Quang Huy'


def tl(name, *pairs):
    return [{'n': i + 1, 'speaker': s or name, 'text': t} for i, (s, t) in enumerate(pairs)]


D = []
add = D.append

# ───────────── Vòng 1: không phải trộm, không phải thuốc độc ─────────────
add({'id': 'd00', 'stage': 1, 'type': 'people', 'title': 'Nạn nhân và những người liên quan',
     'paragraphs': ['Ảnh thẻ trích từ sổ hộ khẩu khu tập thể, kèm lý do từng người được đưa vào diện xác minh sáng 30 Tết.']})

add({'id': 'd01', 'stage': 1, 'type': 'newspaper', 'title': 'Báo Thủ đô Cuối tuần: Án mạng sáng 30 Tết ở khu tập thể Dệt',
     'masthead': 'Thủ đô Cuối tuần', 'issue': 'Số 7 (Xuân Bính Tý)', 'date': 'Chủ nhật, 18/2/1996 (30 Tết)',
     'headline': 'Bà giáo về hưu chết trong căn hộ tập thể, 12 cây vàng biến mất',
     'deck': 'Cửa sổ hành lang bung chốt, ấm trà hoa cúc nổi váng trắng. Hàng xóm nghi có trộm đột nhập.',
     'image': 'images/d01-newspaper.webp', 'imageCaption': 'Sân nhà A6 khu tập thể Dệt Thống Nhất sáng 30 Tết.',
     'paragraphs': [
         'Sáng 30 Tết Bính Tý, bà Chu Thị Bích (68 tuổi, giáo viên cấp hai về hưu, sống một mình) được phát hiện đã mất trên ghế bành ở phòng 204 nhà A6 khu tập thể Nhà máy Dệt Thống Nhất (hư cấu).',
         'Trên bàn có ấm trà hoa cúc nổi váng trắng đục. Hộp bánh quy sắt đựng 12 cây vàng lá bà dành dụm cả đời bị cạy trống. Cửa sổ trông ra hành lang bung chốt, kính vỡ.',
         'Năm nay là cái Tết thứ hai Hà Nội không có tiếng pháo. Đêm giao thừa sắp tới, cả khu tập thể quây quần luộc bánh chưng ở sân, không ai nghe thấy gì. Công an quận Hai Bà Trưng đã vào cuộc.']})

add({'id': 'd02', 'stage': 1, 'type': 'report', 'title': 'Biên bản khám nghiệm hiện trường phòng 204 nhà A6',
     'header': CA, 'heading': 'Biên bản khám nghiệm hiện trường', 'code': '18/KNHT', 'date': '08 giờ 30 ngày 18/2/1996',
     'fields': [{'label': 'Địa điểm', 'value': 'Phòng 204, nhà A6, khu tập thể Dệt Thống Nhất, quận Hai Bà Trưng'},
                {'label': 'Người chết', 'value': 'Chu Thị Bích, 68 tuổi'}],
     'sections': [
         {'heading': '1. Cửa', 'paragraphs': ['Cửa ra vào khép, ổ khoá không hỏng, không dấu cạy. Cửa sổ trông ra hành lang chung: then cài bị cắt gãy, **mảnh kính vỡ văng ra phía hành lang**, bậu cửa phía trong không có mảnh kính nào.']},
         {'heading': '2. Tử thi và bàn trà', 'paragraphs': ['Nạn nhân ngồi ngả trên ghế bành, tay phải còn nắm một bình xịt hen Ventolin. Trên bàn: ấm trà hoa cúc nổi váng trắng, một chén uống dở, **hộp mứt gừng ngào hạt điều** đã mở, ăn mất hai miếng; tivi còn bật.']},
         {'heading': '3. Hộp bánh quy', 'paragraphs': ['Hộp bánh quy sắt dưới gầm giường bị cạy nắp, trống. Trên sàn hành lang trước cửa có vết bùn đế dép đan ô ca-rô, mưa phùn chưa xoá hết.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd03', 'stage': 1, 'type': 'scan', 'title': 'Sơ đồ hiện trường căn hộ 204',
     'image': 'images/d02-so-do-can-ho.webp', 'caption': 'Sơ đồ lập khi khám nghiệm: (1) vị trí nạn nhân, (2) bàn trà, (3) hộp bánh quy dưới gầm giường. Ghi chú ở góc: cửa sổ hành lang bị bẻ chốt từ bên trong, mảnh kính văng ra ngoài.'})

add({'id': 'd04', 'stage': 1, 'type': 'photo', 'title': 'Ảnh hiện trường phòng 204 sáng 30 Tết',
     'image': 'images/d04-room.webp', 'label': 'Ảnh hiện trường số 2 · 18/2/1996',
     'caption': 'Ghế bành, ấm trà hoa cúc, đĩa mứt gừng và hộp bánh quy sắt dưới gầm giường.'})

add({'id': 'd05', 'stage': 1, 'type': 'evidence', 'title': 'Kết luận giám định pháp y',
     'code': '27/96-KL', 'image': 'images/d06-so-do-tu-thi.webp', 'imageCaption': 'Sơ đồ giải phẫu đường hô hấp kèm kết luận của Viện Khoa học hình sự.',
     'fields': [{'label': 'Thời gian tử vong', 'value': 'Khoảng 21:00 đến 22:00 ngày 17/2/1996 (29 Tết)'}],
     'paragraphs': ['1. Nguyên nhân: **sốc phản vệ do dị ứng protein hạt điều**, gây phù nề thanh quản và co thắt phế quản, suy hô hấp cấp.',
                    '2. Không phát hiện chất độc hoá học trong máu, dạ dày và ấm trà. Váng trắng trong ấm trà là **bột sắn dây**, vô hại; bột nổi trên mặt nước nguội, chưa kịp hoà tan như khi pha lúc nước còn nóng.',
                    '3. Bình xịt Ventolin trong tay nạn nhân không còn thuốc. Đã gửi giám định riêng.']})

add({'id': 'd06', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của chị Đỗ Thị Nga (bán chè chân cầu thang)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 30 ngày 18/2/1996',
     'fields': [{'label': 'Người khai', 'value': 'Đỗ Thị Nga, 36 tuổi, bán chè, xôi ở chân cầu thang nhà A6'}],
     'lines': tl('Đỗ Thị Nga',
         (DTV, 'Chị phát hiện bà Bích lúc nào?'),
         (None, 'Bảy giờ sáng em mang đĩa xôi gấc lên biếu Tết, cửa khép hờ, bà ngồi trên ghế, người lạnh ngắt. Em kêu ầm lên.'),
         (DTV, 'Hôm qua chị có gặp bà Bích không?'),
         (None, 'Trưa 29 em với bà cãi nhau ở bể nước vì em vay bà ba chỉ vàng chưa trả. Em nói nặng, em hối hận lắm.'),
         (DTV, 'Chị còn thấy ai lên phòng bà hôm 29?'),
         (None, 'Hai giờ chiều thằng Cường cháu bà lên xin tiền, bị bà cầm chổi đuổi xuống. Bốn rưỡi ông Toàn trưởng ban xách giỏ quà Tết lên phát.'),
         (DTV, 'Tối 29 chị ở đâu?'),
         (None, 'Em ngồi canh nồi bánh chưng ở góc sân với mấy nhà từ tám giờ tối đến hai giờ sáng.')),
     'signature': 'Người khai: Đỗ Thị Nga'})

# ───────────── Vòng 2: ai lên tầng hai ─────────────
add({'id': 'd07', 'stage': 2, 'type': 'note', 'title': 'Trích sổ y bạ gia đình của bà Chu Thị Bích',
     'paragraphs': ['Sổ y bạ do trạm y tế xí nghiệp cấp, chữ của y sĩ Trịnh Văn Hưng:',
                    '— Hen phế quản mạn. Dùng bình xịt Ventolin khi lên cơn. Bệnh nhân luôn để một bình trên kệ cạnh ghế bành.',
                    '__— Dị ứng nặng với các loại hạt có dầu (lạc, hạt điều). Đã một lần sốc phản vệ năm 1990. Dặn tuyệt đối tránh.__',
                    '— 12/1995: kê đơn bình Ventolin mới, mua ở hiệu thuốc Bạch Mai, lô số 95-11.',
                    'Ghi chú: danh sách người già có bệnh nền của khu tập thể (kèm dị ứng) được gửi ban đại diện cư dân để chia quà Tết cho phù hợp.'],
     'signature': 'Y sĩ Trịnh Văn Hưng'})

add({'id': 'd08', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của Nguyễn Quốc Cường (cháu ruột)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 00 ngày 18/2/1996',
     'fields': [{'label': 'Người khai', 'value': 'Nguyễn Quốc Cường, 27 tuổi, lái xe tải, cháu ruột bà Bích (bắt được ở ga Đồng Hới)'}],
     'lines': tl('Nguyễn Quốc Cường',
         (DTV, 'Chiều 29 anh có đến nhà bà Bích?'),
         (None, 'Không. Cả ngày 29 tôi ở phòng trọ bạn gái dọn đồ, không qua cô tôi.'),
         (DTV, 'Anh nợ ai?'),
         (None, 'Nợ cá độ bóng đá, mấy thằng chủ nợ doạ chặt chân. Tôi định trốn vào Sài Gòn ăn Tết.'),
         (DTV, 'Tối 29 anh ở đâu?'),
         (None, 'Mười giờ tối tôi đi xích lô ra ga Hàng Cỏ, lên tàu Thống Nhất đi Sài Gòn.')),
     'signature': 'Người khai: Nguyễn Quốc Cường'})

add({'id': 'd09', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của y sĩ Trịnh Văn Hưng (trạm y tế xí nghiệp)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '15 giờ 30 ngày 18/2/1996',
     'fields': [{'label': 'Người khai', 'value': 'Trịnh Văn Hưng, 49 tuổi, y sĩ, trạm phó trạm y tế xí nghiệp dệt'}],
     'lines': tl('Trịnh Văn Hưng',
         (DTV, 'Anh có biết bà Bích dị ứng hạt điều?'),
         (None, 'Biết. Tôi ghi trong sổ y bạ và gửi danh sách người có bệnh nền cho ban đại diện cư dân để chia quà Tết.'),
         (DTV, 'Tối 29 anh ở đâu?'),
         (None, 'Tôi trực trạm đến tám giờ, rồi về nhà đón giao thừa với vợ con ở Minh Khai.'),
         (DTV, 'Kho thuốc thanh lý của trạm ai giữ chìa?'),
         (None, 'Kho ấy niêm phong từ năm 1994, chìa giao cho thủ kho thanh lý của xí nghiệp. Tôi không giữ.')),
     'signature': 'Người khai: Trịnh Văn Hưng'})

add({'id': 'd10', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của ông Lê Khắc Toàn (trưởng ban đại diện cư dân)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '16 giờ 30 ngày 18/2/1996',
     'fields': [{'label': 'Người khai', 'value': 'Lê Khắc Toàn, 56 tuổi, trưởng ban đại diện cư dân nhà A6, bảo vệ xí nghiệp'}],
     'lines': tl('Lê Khắc Toàn',
         (DTV, 'Ngày 29 Tết ông có lên phòng 204 không?'),
         (None, 'Không. Cả ngày tôi lo việc tổ, quà Tết thì các cháu đoàn viên mang lên từng nhà.'),
         (DTV, 'Tối 29 ông ở đâu?'),
         (None, 'Tôi trực một mình ở chòi bảo vệ cổng khu tập thể đến sáng, nghe đài, giữ trật tự.'),
         (DTV, 'Giỏ quà Tết chia thế nào?'),
         (None, 'Theo danh sách phường gửi xuống, nhà nào giỏ nào là đúng như thế, tôi không sửa gì.')),
     'signature': 'Người khai: Lê Khắc Toàn'})

add({'id': 'd11', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai tập thể các hộ luộc bánh chưng ở sân nhà A6',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '10 giờ 00 ngày 19/2/1996',
     'fields': [{'label': 'Người khai', 'value': 'Bà Lương Thị Mận (phòng 102), ông Vũ Văn Lộc (phòng 105), chị Hà Thu Trang (phòng 108)'}],
     'lines': tl('Bà Lương Thị Mận',
         (DTV, 'Tối 29 các ông bà ngồi đâu?'),
         (None, 'Năm nhà góp củi luộc bánh chưng ở góc sân cạnh bể nước, từ tám giờ tối đến hai giờ sáng. Cái Nga ngồi canh nồi suốt, không đi đâu.'),
         ('Ông Vũ Văn Lộc', 'Bốn rưỡi chiều tôi thấy ông Toàn tự xách giỏ quà có buộc nơ đỏ lên tầng hai, nói "giỏ này đặc biệt, phần bà giáo".'),
         (DTV, 'Đêm có ai lên cầu thang không?'),
         ('Chị Hà Thu Trang', 'Khoảng mười một rưỡi đêm có người đi lên cầu thang, tiếng dép nhựa lép bép, đài đang phát ca nhạc chào xuân nên không ai để ý. Mười hai giờ kém mười tiếng dép đi xuống.')),
     'signature': 'Người khai: Lương Thị Mận, Vũ Văn Lộc, Hà Thu Trang'})

add({'id': 'd12', 'stage': 2, 'type': 'receipt', 'title': 'Vé tàu và xác nhận kiểm soát vé ga Hàng Cỏ',
     'shop': 'Ga Hàng Cỏ (Ga Hà Nội)', 'address': 'Đường Lê Duẩn, Hà Nội',
     'fields': [{'label': 'Tàu', 'value': 'Thống Nhất TN1, Hà Nội – Sài Gòn'}, {'label': 'Ngày', 'value': '17/02/1996'}, {'label': 'Hành khách', 'value': 'Nguyễn Quốc Cường'}],
     'items': [{'name': 'Vé ghế cứng', 'qty': '1', 'price': '298.000'}],
     'total': '298.000đ',
     'footer': ['Xác nhận của nhân viên kiểm soát vé: hành khách qua cửa soát vé 22:45, tàu chạy 23:00 đúng giờ.',
                'Công an đường sắt xác nhận Cường có mặt trên toa 6 khi tàu qua ga Phủ Lý lúc 0:40 ngày 18/2.']})

# ───────────── Vòng 3: bình xịt và giỏ quà ─────────────
add({'id': 'd13', 'stage': 3, 'type': 'evidence', 'title': 'Phiếu giám định bình xịt Ventolin trong tay nạn nhân',
     'code': '31/96-GĐ', 'image': 'images/d12-inhaler.webp', 'imageCaption': 'Bình xịt thu trong tay nạn nhân (lô in trên thân: 91-04) và các giọt chất lỏng bơm ra để thử.',
     'fields': [{'label': 'Số lô in trên thân bình', 'value': '91-04 (hết hạn năm 1991)'}],
     'paragraphs': ['1. Chất lỏng trong bình là **nước cất**, không có hoạt chất salbutamol.',
                    '2. Van bình có vết cạy mở rồi ép lại.',
                    '3. Số lô **không khớp** với bình bà Bích mua tháng 12/1995 (lô 95-11, theo sổ y bạ). Bình lô 95-11 không có trong căn hộ.']})

add({'id': 'd14', 'stage': 3, 'type': 'report', 'title': 'Biên bản kiểm tra kho thuốc thanh lý trạm y tế xí nghiệp',
     'header': CA, 'heading': 'Biên bản kiểm tra', 'code': '22/KT', 'date': 'Ngày 20/2/1996',
     'sections': [
         {'heading': '1. Kho', 'paragraphs': ['Kho niêm phong từ tháng 6/1994. Giấy niêm phong ở cửa còn nhưng bị bóc một góc rồi dán lại bằng hồ.',
                                               'Chìa kho do **thủ kho thanh lý Lê Khắc Toàn** giữ (theo quyết định của giám đốc xí nghiệp ngày 2/6/1994).']},
         {'heading': '2. Kiểm đếm', 'paragraphs': ['Sổ thanh lý ghi 6 vỏ bình Ventolin **lô 91-04** hết hạn. Kiểm đếm thực tế còn **5**.',
                                                   'Trên kệ có vết bụi mới bị quệt, một chai nước cất 500 ml đã vơi.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd15', 'stage': 3, 'type': 'receipt', 'title': 'Phiếu phân phối quà Tết công đoàn nhà A6 năm 1996',
     'shop': 'Công đoàn Nhà máy Dệt Thống Nhất – Ban đại diện cư dân nhà A6', 'address': 'Phiếu lập ngày 16/2/1996 (28 Tết)',
     'fields': [{'label': 'Người lập', 'value': 'Lê Khắc Toàn'}],
     'items': [{'name': 'Giỏ A (mứt gừng ngào hạt điều, chè, bánh)', 'qty': '12', 'price': '—'},
               {'name': 'Giỏ B (mứt sen, chè, bánh — dành cho người có bệnh nền)', 'qty': '18', 'price': '—'}],
     'total': '30 suất',
     'footer': ['Dòng phòng 204 – Chu Thị Bích: chữ "B" in sẵn bị gạch bằng **mực tím**, viết đè chữ **"A"**.',
                'Trong cả phiếu chỉ có dòng này bị sửa.']})

add({'id': 'd16', 'stage': 3, 'type': 'testimony', 'title': 'Lời khai của chị Bùi Thị Hà (thủ quỹ công đoàn xí nghiệp)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 00 ngày 21/2/1996',
     'fields': [{'label': 'Người khai', 'value': 'Bùi Thị Hà, 41 tuổi, thủ quỹ công đoàn'}],
     'lines': tl('Bùi Thị Hà',
         (DTV, 'Ai chia giỏ quà cho nhà A6?'),
         (None, 'Ông Toàn nhận cả 30 suất chiều 28, tự tay chia theo danh sách bệnh nền của y sĩ Hưng.'),
         (DTV, 'Chị có thấy ông ấy sửa phiếu không?'),
         (None, 'Tôi thấy ông ấy cầm cây bút bi mực tím vẫn cài túi áo gạch gạch trên phiếu, bảo "sửa lại cho đúng". Cả xí nghiệp chỉ ông ấy dùng mực tím.')),
     'signature': 'Người khai: Bùi Thị Hà'})

# ───────────── Vòng 4: 42 triệu quỹ sửa nhà ─────────────
add({'id': 'd17', 'stage': 4, 'type': 'report', 'title': 'Biên bản làm việc về quỹ sửa mái nhà A6 và lô đường lậu',
     'header': CA, 'heading': 'Biên bản làm việc', 'code': '29/LV', 'date': 'Ngày 22/2/1996',
     'sections': [
         {'heading': '1. Quỹ sửa mái', 'paragraphs': ['Quỹ cư dân góp sửa mái nhà A6 (ông Toàn giữ) theo sổ phải còn 42 triệu đồng; két quỹ chỉ còn 300 nghìn. Đoàn thanh tra công đoàn hẹn kiểm quỹ **mùng 6 Tết**.']},
         {'heading': '2. Lô đường', 'paragraphs': ['Ngày 14/2/1996 (26 Tết), Quản lý thị trường thu giữ 6 tấn đường kính nhập lậu ở bãi xe Giáp Bát. Trên giấy góp vốn thu ở bãi xe có tên "Toàn A6 – 42 tr" và chữ ký của Lê Khắc Toàn.']},
         {'heading': '3. Thư thu giữ', 'paragraphs': ['Một thư tay gửi ông Toàn ngày 15/2: "Hàng mất là việc của anh. Vốn của anh mất thì thôi, nhưng ra Tết đừng để người ta hỏi đến tôi."']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd18', 'stage': 4, 'type': 'evidence', 'title': 'Đôi dép rọ và bút bi mực tím thu ở chòi bảo vệ',
     'code': 'TV-16', 'image': 'images/d16-shoes.webp', 'imageCaption': 'Dép rọ nhựa (1) và bút bi mực tím (2) thu ở chòi bảo vệ cổng khu tập thể ngày 22/2.',
     'paragraphs': ['1. Đế dép đan ô ca-rô, cỡ 41, của Lê Khắc Toàn. Vân đế **trùng khớp** với vết bùn trên hành lang tầng hai trước phòng 204.',
                    '2. Mực bút bi tím **cùng loại** với nét gạch sửa "B" thành "A" trên phiếu phân phối quà Tết.']})

add({'id': 'd19', 'stage': 4, 'type': 'evidence', 'title': 'Biên bản thu giữ 12 cây vàng lá',
     'code': 'TV-17', 'image': 'images/d17-gold.webp', 'imageCaption': '12 cây vàng lá thu trong ống thông gió nhà vệ sinh bỏ hoang cạnh chòi bảo vệ.',
     'paragraphs': ['1. 12 miếng vàng lá bọc túi ni lông xanh, giấu trong ống thông gió của nhà vệ sinh bỏ hoang cạnh chòi bảo vệ. Chỉ người trực chòi giữ chìa cánh cửa này.',
                    '2. Mặt sau hộp bánh quy sắt có ghi chép của bà Bích: "12 cây – để dành chữa mắt và lo hậu sự". Số lượng khớp.',
                    '3. Cũng trong ống thông gió: một bình xịt Ventolin **lô 95-11**, còn đầy thuốc.']})

CARDS = ['toan', 'cuong', 'nga', 'hung']
NAMES = ['Lê Khắc Toàn', 'Nguyễn Quốc Cường', 'Đỗ Thị Nga', 'Trịnh Văn Hưng']
Q = [
    {'id': 'q1', 'stage': 1, 'type': 'choice', 'title': 'Trộm đột nhập hạ độc?',
     'prompt': 'Báo chí nghi kẻ trộm đột nhập, hạ độc bà Bích bằng ấm trà rồi lấy vàng. Theo hồ sơ đang mở, nhận định nào đứng vững?',
     'options': ['Kẻ trộm phá cửa sổ trèo vào, bỏ thuốc độc vào ấm trà, chờ bà Bích uống rồi lấy vàng.',
                 'Bà Bích chết vì sốc phản vệ do hạt điều, không có thuốc độc; cửa sổ bị phá từ bên trong và váng trong ấm trà được đổ vào sau, để dựng cảnh trộm hạ độc.',
                 'Bà Bích lên cơn hen tự nhiên rồi mất; kẻ trộm tình cờ đột nhập sau đó, thấy bà đã chết nên lấy vàng.'],
     'answer': [1],
     'nudges': {'0': {'message': 'Pháp y có thấy chất độc không? Mảnh kính văng về phía nào?'},
                '2': {'message': 'Pháp y nói nguyên nhân là gì, do ăn thứ gì? Và cửa sổ bị phá từ phía nào?'}},
     'hints': ['Đọc kết luận pháp y và biên bản khám nghiệm.', 'Váng trắng là gì? Kính vỡ văng về đâu?',
               'd05: sốc phản vệ do hạt điều, không chất độc, váng là bột sắn dây đổ vào nước nguội. d02: kính văng ra hành lang, bậu trong không có mảnh nào.'],
     'solved': 'Không có kẻ trộm hạ độc. Có người đã dựng cảnh ấy sau khi bà Bích chết.',
     'explanation': [{'title': 'Nguyên nhân', 'body': ['d05: sốc phản vệ do protein hạt điều; d02: hộp mứt gừng ngào hạt điều đã mở.']},
                     {'title': 'Ấm trà', 'body': ['d05: váng là bột sắn dây, nổi trên nước nguội, tức đổ vào khi trà đã nguội.']},
                     {'title': 'Cửa sổ', 'body': ['d02, d03: kính văng ra hành lang, tức bị phá từ bên trong phòng.']}]},
    {'id': 'q2', 'stage': 1, 'type': 'evidence', 'need': 2, 'title': 'Hộp mứt gừng và bình xịt',
     'prompt': 'Ghim 2 tài liệu cho thấy bà Bích đã không thể tự cứu mình khi lên cơn.',
     'answer': ['d02', 'd05'],
     'nudges': [{'any': ['d04'], 'near': True, 'message': 'Ảnh cho thấy bàn trà. Cần biên bản tả thứ trong tay bà và kết luận về chiếc bình xịt.'}],
     'hints': ['Một biên bản khám nghiệm, một kết luận pháp y.', 'Trong tay bà Bích cầm gì? Thứ ấy còn thuốc không?',
               'd02: tay phải nắm bình xịt Ventolin, hộp mứt hạt điều đã ăn hai miếng. d05: bình xịt không còn thuốc.'],
     'solved': 'Bà Bích đã kịp với lấy bình xịt, nhưng bình không còn thuốc.',
     'explanation': [{'title': 'Bình xịt', 'body': ['d02: tay phải còn nắm bình Ventolin; d05: bình không còn thuốc.']},
                     {'title': 'Mứt', 'body': ['d02: hộp mứt gừng ngào hạt điều đã mở, ăn hai miếng.']},
                     {'title': 'Câu hỏi', 'body': ['Ai đưa hộp mứt ấy tới, và bình thuốc của bà vì sao lại rỗng?']}]},
    {'id': 'q3', 'stage': 2, 'type': 'line', 'title': 'Giỏ quà buộc nơ đỏ',
     'prompt': 'Một người khai không lên phòng 204 ngày 29 Tết. Chỉ ra dòng khai bị nhiều người khác bác bỏ.',
     'answer': ['d10:002'],
     'nudges': {'d08:002': {'near': True, 'message': 'Lời Cường cũng bị bác (d06), nhưng câu hỏi nói về người bị nhiều người bác.'},
                'd10:004': {'message': 'Câu về chòi bảo vệ chưa bị bác thẳng. Tìm câu về ngày 29.'}},
     'hints': ['Ai thấy ông Toàn lúc 16:30?', 'Ông Toàn nói quà do ai mang lên?', 'd10 dòng 2: không lên phòng 204, quà do đoàn viên mang. d06: 16:30 ông Toàn xách giỏ quà lên. d11: ông Toàn tự xách giỏ nơ đỏ lên tầng hai, "phần bà giáo".'],
     'solved': 'Ông Toàn tự mang giỏ quà "đặc biệt" lên phòng 204 chiều 29 Tết.',
     'explanation': [{'title': 'Câu khai', 'body': ['d10 dòng 2: không lên phòng 204, quà do các cháu đoàn viên mang.']},
                     {'title': 'Bị bác', 'body': ['d06: 16:30 ông Toàn xách giỏ quà lên. d11: ông tự xách giỏ nơ đỏ, nói "giỏ này đặc biệt, phần bà giáo".']},
                     {'title': 'Khớp', 'body': ['d07: danh sách dị ứng được gửi cho ban đại diện cư dân để chia quà.']}]},
    {'id': 'q4', 'stage': 2, 'type': 'evidence', 'need': 2, 'title': 'Đêm giao thừa sắp tới',
     'prompt': 'Ghim 2 tài liệu loại trừ Cường và chị Nga khỏi việc lên phòng 204 lúc 23:30.',
     'answer': ['d11', 'd12'],
     'nudges': [{'any': ['d08', 'd06'], 'message': 'Đó là lời tự khai. Cần tài liệu do người khác lập.'}],
     'hints': ['Một lời khai tập thể, một tờ vé tàu.', 'Lúc 23:30 Cường ở đâu? Chị Nga ở đâu?',
               'd11: Nga canh nồi bánh chưng ở sân 20:00–2:00, có năm nhà làm chứng; 23:30 có tiếng dép nhựa lên cầu thang. d12: Cường qua cửa soát vé 22:45, trên tàu qua Phủ Lý 0:40.'],
     'solved': 'Người đi dép nhựa lên cầu thang lúc 23:30 không phải Cường, cũng không phải chị Nga.',
     'explanation': [{'title': 'Nga', 'body': ['d11: ngồi canh nồi bánh suốt 20:00–2:00 giữa năm nhà.']},
                     {'title': 'Cường', 'body': ['d12: soát vé 22:45, tàu chạy 23:00, qua Phủ Lý 0:40 vẫn có mặt.']},
                     {'title': 'Ai lên', 'body': ['d11: 23:30 tiếng dép nhựa lên, 23:50 xuống. d02: vết bùn đế ca-rô trước cửa 204.']}]},
    {'id': 'q5', 'stage': 3, 'type': 'evidence', 'need': 2, 'title': 'Lô 91-04',
     'prompt': 'Ghim 2 tài liệu cho thấy bình xịt của bà Bích đã bị tráo, và bình giả lấy từ đâu, ai giữ chìa.',
     'answer': ['d13', 'd14'],
     'nudges': [{'any': ['d07'], 'near': True, 'message': 'Sổ y bạ cho biết lô bình thật. Cần giám định bình trong tay bà và kiểm tra nơi có lô cũ.'}],
     'hints': ['Một phiếu giám định, một biên bản kiểm tra kho.', 'Bình trong tay bà thuộc lô nào? Lô ấy ở đâu?',
               'd13: bình lô 91-04 hết hạn, nước cất, không khớp lô 95-11 bà mua. d14: kho thanh lý ghi 6 vỏ lô 91-04, còn 5, niêm phong bị bóc dán lại; chìa do Lê Khắc Toàn giữ.'],
     'solved': 'Bình xịt cứu mạng của bà Bích đã bị thay bằng một vỏ hết hạn bơm nước cất, lấy từ kho mà chỉ ông Toàn giữ chìa.',
     'explanation': [{'title': 'Bình giả', 'body': ['d13: lô 91-04 hết hạn, nước cất, van bị cạy; bình lô 95-11 biến mất.']},
                     {'title': 'Nguồn', 'body': ['d14: kho thanh lý thiếu đúng 1 vỏ lô 91-04, chai nước cất vơi.']},
                     {'title': 'Chìa', 'body': ['d14: thủ kho thanh lý Lê Khắc Toàn; d09: y sĩ Hưng không giữ chìa.']}]},
    {'id': 'q6', 'stage': 3, 'type': 'line', 'title': 'Mực tím',
     'prompt': 'Chỉ ra dòng khai bị phiếu phân phối quà Tết và lời chị thủ quỹ bác bỏ.',
     'answer': ['d10:006'],
     'nudges': {'d10:002': {'near': True, 'message': 'Câu này đã bị bác ở vòng trước. Tìm câu về giỏ quà.'}},
     'hints': ['Dòng phòng 204 trên phiếu bị sửa thế nào?', 'Ông Toàn nói gì về danh sách giỏ quà?',
               'd10 dòng 6: theo danh sách phường, không sửa gì. d15: dòng phòng 204 "B" bị gạch mực tím, viết "A". d16: ông Toàn cầm bút mực tím gạch trên phiếu.'],
     'solved': 'Ông Toàn đã đổi giỏ quà của bà Bích sang giỏ có mứt hạt điều, dù danh sách dị ứng nằm trong tay ông.',
     'explanation': [{'title': 'Câu khai', 'body': ['d10 dòng 6: giỏ quà đúng danh sách, không sửa gì.']},
                     {'title': 'Bị bác', 'body': ['d15: dòng phòng 204 duy nhất bị sửa "B" thành "A" bằng mực tím. d16: ông Toàn tự tay sửa bằng bút mực tím.']},
                     {'title': 'Biết rõ', 'body': ['d07, d09: danh sách dị ứng được gửi cho ban đại diện cư dân.']}]},
    {'id': 'q7', 'stage': 4, 'type': 'evidence', 'need': 2, 'title': 'Trước mùng 6 Tết',
     'prompt': 'Ghim 2 tài liệu cho thấy vì sao ông Toàn cần 12 cây vàng trước mùng 6 Tết, và số vàng ở đâu.',
     'answer': ['d17', 'd19'],
     'nudges': [{'any': ['d18'], 'near': True, 'message': 'Đôi dép và cây bút nối ông Toàn với hiện trường. Cần tài liệu về động cơ và số vàng.'}],
     'hints': ['Một biên bản làm việc, một biên bản thu giữ vàng.', 'Quỹ sửa mái còn bao nhiêu? Ai kiểm quỹ lúc nào? Vàng giấu ở đâu?',
               'd17: quỹ sửa mái thiếu 42 triệu, thanh tra mùng 6, ông Toàn góp 42 triệu vào lô đường lậu bị thu 26 Tết. d19: 12 cây vàng và bình Ventolin lô 95-11 trong ống thông gió cạnh chòi bảo vệ.'],
     'solved': 'Ông Toàn cần lấp 42 triệu quỹ cư dân trước khi thanh tra đến mùng 6 Tết.',
     'explanation': [{'title': 'Lỗ quỹ', 'body': ['d17: 42 triệu quỹ sửa mái mất trong lô đường lậu bị thu giữ 26 Tết; thanh tra mùng 6.']},
                     {'title': 'Vàng', 'body': ['d19: 12 cây vàng trong ống thông gió cạnh chòi bảo vệ, khớp ghi chép của bà Bích.']},
                     {'title': 'Bình thật', 'body': ['d19: bình Ventolin lô 95-11 còn đầy thuốc giấu cùng chỗ.']}]},
    {'id': 'q-accuse', 'stage': 4, 'type': 'choice', 'cards': CARDS, 'title': 'Chỉ mặt thủ phạm',
     'prompt': 'Ai đã gây ra cái chết của bà Chu Thị Bích? Chọn một người.',
     'options': NAMES, 'answer': [0],
     'nudges': {'1': {'message': 'Cường qua cửa soát vé ga Hàng Cỏ 22:45 (d12). Anh không có chìa kho thuốc, không chia quà.'},
                '2': {'message': 'Chị Nga canh nồi bánh chưng ở sân cả đêm (d11).'},
                '3': {'message': 'Y sĩ Hưng không giữ chìa kho thanh lý (d09, d14), không chia giỏ quà (d16).'}},
     'hints': ['Người làm cần: biết bệnh án, giữ chìa kho thanh lý, chia giỏ quà, lên tầng hai lúc 23:30.', 'Ai dùng bút mực tím và đi dép rọ đế ca-rô?',
               'Ông Toàn: giỏ quà (d06, d11, d15, d16), kho thuốc (d14), dép và bút (d18), vàng và bình thật (d19), quỹ 42 triệu (d17).'],
     'solved': 'Lê Khắc Toàn.',
     'explanation': [{'title': 'Bẫy', 'body': ['d15, d16: đổi giỏ quà sang giỏ có hạt điều; d13, d14: tráo bình xịt bằng vỏ hết hạn bơm nước cất.']},
                     {'title': 'Dựng cảnh', 'body': ['d02, d05, d11, d18: 23:30 lên phòng, lấy vàng, đổ bột sắn dây, phá cửa sổ từ bên trong; vết dép trùng.']},
                     {'title': 'Động cơ', 'body': ['d17, d19: lỗ 42 triệu quỹ cư dân, thanh tra mùng 6; vàng giấu cạnh chòi bảo vệ.']}]},
    {'id': 'q8', 'stage': 4, 'type': 'choice', 'title': 'Kết luận điều tra',
     'prompt': 'Chọn bản kết luận đúng với hồ sơ ở mọi chi tiết.',
     'options': [
         'Ông Toàn mất 42 triệu quỹ sửa mái vào lô đường lậu, sợ thanh tra mùng 6 Tết. Biết bà Bích dị ứng hạt điều, ông sửa phiếu đổi giỏ quà của bà sang giỏ có mứt gừng hạt điều, lấy vỏ Ventolin hết hạn trong kho thanh lý bơm nước cất rồi tráo bình xịt khi mang quà lên chiều 29. Tối đó bà ăn mứt, lên cơn mà bình không có thuốc. 23:30 ông lên lấy 12 cây vàng, đổ bột sắn dây vào ấm trà và phá cửa sổ từ bên trong để dựng cảnh trộm hạ độc.',
         'Cường nợ cá độ, chiều 29 lên xin tiền bị đuổi nên tối quay lại bỏ hạt điều vào ấm trà của bà Bích rồi lấy 12 cây vàng, phá cửa sổ để giả trộm, sau đó ra ga Hàng Cỏ lên tàu đi Sài Gòn với số vàng giấu trong ba lô; ông Toàn chỉ vô tình nhầm giỏ quà khi chia, còn bình xịt của bà Bích tự hết thuốc vì bà dùng nhiều trong mùa rét.',
         'Chị Nga nợ bà Bích ba chỉ vàng, cãi nhau trưa 29, tối nhân lúc canh nồi bánh chưng lẻn lên tầng hai đổ thuốc độc vào ấm trà rồi lấy vàng trả nợ; y sĩ Hưng giúp chị bằng cách tráo bình xịt của bà Bích lấy từ trạm y tế, đổi lại một phần số vàng để lo cho con đi Ba Lan.',
         'Y sĩ Hưng cần tiền cho con đi Ba Lan, tráo bình xịt của bà Bích bằng bình hết hạn khi khám định kỳ, rồi đêm 29 lên lấy vàng; ông Toàn chỉ sửa phiếu quà vì nghĩ bà Bích thích mứt gừng, và đôi dép của ông bị người khác lấy trộm mang đi, còn số vàng trong ống thông gió là do y sĩ Hưng giấu để đổ tội cho ông.'],
     'answer': [0],
     'exam': {'examiner': 'Kiểm sát viên Nguyễn Thị Thanh',
              'intro': 'Trình bày kết luận trước kiểm sát viên: trả lời lần lượt từng câu hỏi bằng lời của mình. Không dùng được AI thì bấm “Trả lời bằng trắc nghiệm” để chọn bản kết luận đúng.'},
     'nudges': {'1': {'message': 'Không có chất độc trong ấm trà (d05); Cường qua soát vé 22:45 (d12) và vàng nằm cạnh chòi bảo vệ (d19).'},
                '2': {'message': 'Không có thuốc độc (d05); chị Nga canh nồi suốt đêm (d11); kho thanh lý không phải do y sĩ Hưng giữ chìa (d14).'},
                '3': {'message': 'Y sĩ Hưng không có chìa kho thanh lý (d14); dép và bút mực tím thu ở chòi bảo vệ (d18).'}},
     'hints': ['Đối chiếu: ai sửa phiếu quà (d15, d16), ai giữ chìa kho (d14), vàng ở đâu (d19).', 'Chỉ một phương án có giỏ quà, bình xịt nước cất và quỹ 42 triệu.', 'Phương án A.'],
     'solved': 'Hồ sơ khép lại với tên Lê Khắc Toàn.',
     'explanation': [{'title': 'Cách làm', 'body': ['d13, d14, d15, d16: tráo bình xịt và đổi giỏ quà.']},
                     {'title': 'Dựng cảnh', 'body': ['d02, d05, d11, d18: bột sắn dây, cửa sổ phá từ trong, dép đế ca-rô lúc 23:30.']},
                     {'title': 'Vì sao', 'body': ['d17, d19: 42 triệu quỹ cư dân mất trong lô đường lậu; thanh tra mùng 6 Tết.']}]},
]

case = {
    'id': CID, 'no': 2, 'status': 'available',
    'title': 'Mùa đông năm Bính Tý',
    'subtitle': 'Một giỏ quà Tết, một bình xịt hen và đêm 29 Tết ở khu tập thể',
    'tagline': 'Đêm 29 Tết Bính Tý, bà giáo về hưu chết trên ghế bành, tay còn nắm bình xịt hen. Bình không có một giọt thuốc.',
    'difficulty': 3, 'players': '1–5', 'duration': '60–75 phút',
    'setting': 'Khu tập thể Dệt Thống Nhất (hư cấu), quận Hai Bà Trưng, Hà Nội', 'era': 'Tháng 2/1996',
    'tags': ['Án mạng', 'Tết', 'Khu tập thể', 'Hà Nội 1996'], 'cover': 'images/cover.webp',
    'contentWarning': 'Hồ sơ có mô tả một cái chết do dị ứng. Khu tập thể, nhân vật và sự việc đều hư cấu.',
    'synopsis': ['Sáng 30 Tết Bính Tý (18/2/1996), bà giáo về hưu Chu Thị Bích được phát hiện đã mất trên ghế bành ở phòng 204 nhà A6 khu tập thể Dệt Thống Nhất.',
                 'Ấm trà nổi váng trắng, hộp vàng dưới gầm giường bị cạy, cửa sổ hành lang vỡ kính. Mọi thứ trông như một vụ trộm hạ độc. Có lẽ quá giống.'],
    'intro': {'title': 'Mùa đông năm Bính Tý',
              'paragraphs': ['Hà Nội, sáng 30 Tết Bính Tý, tháng 2 năm 1996. Năm thứ hai không có tiếng pháo, cả khu tập thể Dệt Thống Nhất thức trắng luộc bánh chưng dưới mưa phùn.',
                             'Bảy giờ sáng, chị Nga bán chè mang đĩa xôi gấc lên biếu bà giáo Bích ở phòng 204, thấy bà ngồi trên ghế bành, tay còn nắm bình xịt hen. Trên bàn, ấm trà hoa cúc nổi váng trắng. Dưới gầm giường, hộp bánh quy đựng 12 cây vàng đã trống.',
                             'Bạn là điều tra viên Đội Điều tra hình sự Công an quận Hai Bà Trưng. Bốn người có lý do bị nghi. Hãy bắt đầu từ kết luận pháp y.'],
              'objective': 'Tìm ra bà Bích chết vì gì, ai đã chuẩn bị cái chết ấy từ trước, ai dựng cảnh trộm hạ độc và vì sao.'},
    'victim': {'id': 'bich', 'name': 'Chu Thị Bích', 'age': 68, 'role': 'Giáo viên cấp hai về hưu', 'image': 'images/id-bich.webp',
               'note': 'Mất tối 29 Tết Bính Tý (17/2/1996) tại phòng 204 nhà A6. Mất 12 cây vàng lá dành dụm cả đời.'},
    'suspects': [
        {'id': 'toan', 'name': 'Lê Khắc Toàn', 'age': 56, 'role': 'Trưởng ban đại diện cư dân, bảo vệ xí nghiệp', 'image': 'images/id-toan.webp', 'voice': 'M3',
         'suspicion': 'Người quản lý quỹ và quà Tết của nhà A6; trực chòi bảo vệ một mình đêm 29.'},
        {'id': 'cuong', 'name': 'Nguyễn Quốc Cường', 'age': 27, 'role': 'Cháu ruột, lái xe tải', 'image': 'images/id-cuong.webp', 'voice': 'M1',
         'suspicion': 'Nợ cá độ, chiều 29 lên xin tiền bị bà Bích đuổi; đêm đó bỏ trốn vào Nam.'},
        {'id': 'nga', 'name': 'Đỗ Thị Nga', 'age': 36, 'role': 'Bán chè, hàng xóm tầng một', 'image': 'images/id-nga.webp', 'voice': 'F1',
         'suspicion': 'Nợ bà Bích ba chỉ vàng, cãi nhau to ở bể nước trưa 29; người phát hiện thi thể.'},
        {'id': 'hung', 'name': 'Trịnh Văn Hưng', 'age': 49, 'role': 'Y sĩ trạm y tế xí nghiệp', 'image': 'images/id-hung.webp', 'voice': 'M2',
         'suspicion': 'Người khám bệnh cho bà Bích, biết rõ bệnh án; đang cần tiền cho con đi lao động ở Ba Lan.'}],
    'aiInterrogation': True,
    'audio': {'intro': 'audio/intro.mp3', 'finale': 'audio/finale.mp3'},
    'documents': D,
    'questions': Q,
    'beats': [
        {'stage': 2, 'kicker': 'Ngày 18–19/2/1996 · Nhà A6', 'title': 'Những bậc cầu thang ẩm ướt', 'voice': 'audio/beat-2.mp3',
         'paragraphs': ['Không có kẻ trộm hạ độc. Bà Bích chết vì một miếng mứt, và chiếc bình xịt trong tay bà rỗng thuốc.',
                        'Đại uý Huy ngồi với từng nhà quanh nồi bánh chưng còn ấm, và mở cuốn sổ y bạ của bà giáo.',
                        'Ai biết bà Bích dị ứng hạt điều? Và ai đã lên tầng hai đêm 29?']},
        {'stage': 3, 'kicker': 'Ngày 20–21/2/1996 · Trạm y tế xí nghiệp', 'title': 'Lô thuốc năm 1991', 'voice': 'audio/beat-3.mp3',
         'paragraphs': ['Số lô in trên chiếc bình xịt dẫn điều tra viên tới một căn kho đã niêm phong hai năm.',
                        'Ở phòng công đoàn, tờ phiếu chia quà Tết còn một nét mực tím.',
                        'Ai đã tráo bình thuốc, và ai đã đổi giỏ quà?']},
        {'stage': 4, 'kicker': 'Ngày 22/2/1996 · Mùng 4 Tết', 'title': 'Trước ngày thanh tra', 'voice': 'audio/beat-4.mp3',
         'paragraphs': ['Còn hai ngày nữa là đoàn thanh tra công đoàn đến kiểm quỹ sửa mái nhà A6.',
                        'Một bức thư tay, một tờ giấy góp vốn ở bãi xe Giáp Bát, và cánh cửa nhà vệ sinh bỏ hoang cạnh chòi bảo vệ.',
                        'Chỉ mặt thủ phạm. Và giải thích vì sao.']}],
    'finale': {'title': 'Mùa đông năm Bính Tý',
               'paragraphs': ['Lê Khắc Toàn khai nhận chiều mùng 4 Tết, khi chiếc bình xịt lô 95-11 còn đầy thuốc được đặt cạnh tờ phiếu chia quà có nét mực tím.',
                              'Ông góp bốn mươi hai triệu tiền sửa mái của cả nhà A6 vào một chuyến đường lậu. Hai mươi sáu Tết, chuyến hàng bị thu ở Giáp Bát. Mùng sáu, thanh tra sẽ đến.',
                              'Danh sách người dị ứng do y sĩ Hưng gửi nằm trên bàn ông. Ông chỉ gạch một chữ B, viết đè một chữ A.',
                              'Chiều 29, ông xách giỏ quà buộc nơ đỏ lên phòng 204, khen bà giáo dạy dỗ con cháu cả khu. Lúc bà vào bếp rót nước, ông đổi chiếc bình trên kệ.',
                              'Mười một rưỡi đêm, đài đang phát ca nhạc chào xuân, ông đi dép rọ lên tầng hai. Ông lấy vàng, đổ bột sắn dây vào ấm trà đã nguội, rồi bẻ chốt cửa sổ từ bên trong, không nghĩ mảnh kính sẽ văng ra ngoài.',
                              'Ông chỉ nói một câu: "Tôi tính ra Tết sẽ chuộc lại. Mái nhà ấy dột mười năm rồi."']},
    'epilogue': [
        {'title': 'Lê Khắc Toàn', 'text': 'Bị truy tố về tội giết người, cướp tài sản và tham ô quỹ cư dân. 12 cây vàng được trả lại gia đình bà Bích.'},
        {'title': 'Nguyễn Quốc Cường', 'text': 'Được thả ở ga Đồng Hới. Anh dùng một phần số vàng của cô để trả nợ, phần còn lại góp sửa mái nhà A6 như lời bà dặn.'},
        {'title': 'Đỗ Thị Nga', 'text': 'Trả nốt ba chỉ vàng vào hòm công đức chùa gần khu tập thể, đứng tên bà giáo Bích.'},
        {'title': 'Trịnh Văn Hưng', 'text': 'Bị kỷ luật vì bán thuốc cảm trôi nổi ở chợ trời. Trạm y tế mở lại kho thanh lý và tiêu huỷ toàn bộ thuốc hết hạn.'}],
}

for person in [case['victim'], *case['suspects']]:
    if person.get('image') and not os.path.exists(f'public/cases/{CID}/' + person['image']):
        print('chưa có ảnh:', person['image']); del person['image']
if case['cover'] and not os.path.exists(f'public/cases/{CID}/' + case['cover']):
    print('chưa có ảnh:', case['cover']); case['cover'] = None
json.dump(case, open(f'public/cases/{CID}/case.json', 'w'), ensure_ascii=False, indent=2)
open(f'public/cases/{CID}/case.json', 'a').write('\n')
print(len(D), 'docs', len(Q), 'questions')
