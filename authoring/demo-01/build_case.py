"""Dựng public/cases/demo-01/case.json từ kịch bản. Chạy ở thư mục gốc: python3 authoring/demo-01/build_case.py
Builds public/cases/demo-01/case.json (Chiếc đồng hồ ở ngõ Gác Chuông, bản 2). Run from the repo root."""
import json

CA = ['Công an quận Hoàn Kiếm', 'Đội Cảnh sát hình sự']
DTV = 'Điều tra viên'
KHAI = 'Đại uý Lương Minh Khải'


def tl(name, *pairs):
    """Testimony lines: (speaker, text); speaker None = người khai (name)."""
    return [{'n': i + 1, 'speaker': s or name, 'text': t} for i, (s, t) in enumerate(pairs)]


docs = []
add = docs.append

# ───────────── Vòng 1 ─────────────
add({'id': 'd00', 'stage': 1, 'type': 'people', 'title': 'Người bị hại và những người liên quan',
     'paragraphs': ['Ảnh thẻ trích từ cơ sở dữ liệu căn cước, kèm lý do từng người được đưa vào diện xác minh ngay sáng 15/3/2024.']})

add({'id': 'd01', 'stage': 1, 'type': 'newspaper', 'title': 'Báo Phố Cũ: Trộm đột nhập nhà nhà sưu tầm đồng hồ',
     'masthead': 'Phố Cũ', 'issue': 'Số 1.204', 'date': 'Thứ Sáu, 15/3/2024 · Số chiều',
     'headline': 'Trộm đột nhập nhà sưu tầm, cuỗm đồng hồ cổ trăm năm',
     'deck': 'Cửa sổ vỡ tan, két sắt mở toang: hàng xóm ngõ Gác Chuông bàng hoàng sau một đêm mưa phùn.',
     'image': 'images/d01-window.webp', 'imageCaption': 'Ô cửa sổ phòng làm việc nhà số 17 nhìn từ sân sau, sáng 15/3.',
     'paragraphs': [
         'Sáng 15/3, ông Trần Đức Hậu (68 tuổi), nhà sưu tầm đồng hồ cổ có tiếng ở ngõ Gác Chuông, trình báo công an về việc chiếc đồng hồ bỏ túi vỏ vàng đời 1920, khắc chữ T.Đ.H, bị mất khỏi két sắt trong phòng làm việc.',
         'Theo một số hộ dân, khoảng 23 giờ đêm 14/3 họ nghe tiếng kính vỡ phía sau nhà số 17. Nhiều người cho rằng kẻ gian đã trèo tường sau, phá cửa sổ để vào nhà.',
         'Đêm đó ông Hậu đi dự tiệc mừng thọ ở Hải Phòng. Trong nhà có người giúp việc và một người cháu.',
         'Chiếc đồng hồ được giới chơi đồ cổ định giá khoảng 300 triệu đồng. Công an quận Hoàn Kiếm đề nghị các tiệm cầm đồ, cửa hàng đồ cổ báo tin nếu có người mang tới.']})

add({'id': 'd02', 'stage': 1, 'type': 'report', 'title': 'Biên bản khám nghiệm hiện trường',
     'header': CA, 'heading': 'Biên bản khám nghiệm hiện trường', 'code': '17/KNHT', 'date': '08 giờ 30 ngày 15/3/2024',
     'fields': [{'label': 'Địa điểm', 'value': 'Nhà số 17 ngõ Gác Chuông (nhà ống 3 tầng)'},
                {'label': 'Chủ nhà', 'value': 'Trần Đức Hậu, 68 tuổi'},
                {'label': 'Tài sản mất', 'value': '01 đồng hồ bỏ túi vỏ vàng đời 1920, nắp sau khắc T.Đ.H'}],
     'image': 'images/d02-so-do-nha.webp', 'imageCaption': 'Sơ đồ tầng 2 và sân sau nhà số 17 (lập lúc khám nghiệm).',
     'sections': [
         {'heading': '1. Cửa chính và cổng', 'paragraphs': ['Cửa chính khoá trong, ổ khoá nguyên vẹn. Cổng sắt cài then phía trong. Không có dấu vết cạy phá.']},
         {'heading': '2. Cửa sổ phòng làm việc (tầng 2, nhìn xuống sân sau)', 'paragraphs': [
             'Một ô kính bị vỡ. **Phần lớn mảnh kính rơi xuống sân sau**, cách chân tường 1–3 m; trong phòng chỉ có vài mảnh nhỏ trên bậu cửa.',
             'Cửa sổ cao 4,2 m so với mặt sân. Tường sau, ống thoát nước và bậu cửa không có dấu leo bám, dấu giày hay bùn. Không thấy thang.']},
         {'heading': '3. Két sắt', 'paragraphs': [
             'Két khoá số 6 chữ số đặt dưới gầm bàn làm việc. Cửa két mở, **không có dấu vết khoan, cạy hay phá khoá**: két được mở bằng đúng mã.',
             'Trong két còn nguyên sổ đỏ, 2 chiếc đồng hồ đeo tay và 15 triệu đồng tiền mặt.']},
         {'heading': '4. Sân sau và cầu thang sau', 'paragraphs': [
             'Dây phơi quần áo ở sân sau không có đồ phơi. Giỏ đồ bẩn ở chân cầu thang sau có quần áo chưa giặt.',
             'Thu trong rãnh đế đôi giày thể thao trắng cỡ 42 để ở chân cầu thang sau (của Nguyễn Quang Minh) **4 mảnh kính nhỏ** cùng loại kính cửa sổ.']},
         {'heading': '5. Ghi nhận khác', 'paragraphs': ['Sân trước có một con chó becgie (tên Mực) được xích cạnh cổng. Khám nghiệm kết thúc lúc 09 giờ 30.']}],
     'signers': [{'role': DTV, 'name': KHAI}]})

add({'id': 'd03', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của ông Trần Đức Hậu (người bị hại)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 40 ngày 15/3/2024',
     'fields': [{'label': 'Người khai', 'value': 'Trần Đức Hậu, 68 tuổi, nhà sưu tầm đồng hồ cổ'}],
     'lines': tl('Trần Đức Hậu', 
         (DTV, 'Ông kể lại sáng nay ông phát hiện mất đồng hồ thế nào?'),
         (None, 'Tôi với anh Hoà ở Hải Phòng về tới nhà lúc bảy giờ bốn lăm. Anh Hoà thả tôi ở đầu ngõ rồi về luôn.'),
         (None, 'Tôi lên phòng làm việc thì thấy cửa sổ vỡ, két mở. Bảy giờ năm mươi tôi gọi thằng Minh dậy, hai cậu cháu đứng đấy với nhau suốt tới lúc các anh đến, rồi ngồi cùng các anh tới giờ.'),
         (DTV, 'Ai biết mã két của ông?'),
         (None, 'Mã két là ngày giỗ nhà tôi, bà Lan, tính theo **âm lịch**. Tôi chưa đọc mã cho ai bao giờ, kể cả thằng Minh. Tháng trước nó cần sổ hộ khẩu, tôi tự mở két lấy đưa nó.'),
         (DTV, 'Những ai biết ngày giỗ bà nhà theo âm lịch?'),
         (None, 'Chị Tư nấu cỗ giỗ cho tôi mười hai năm nay. Anh Hoà năm nào cũng đến thắp hương. Thằng Minh tháng Giêng năm nay mới lên ở, chưa dự giỗ nào. Anh Lộc thợ đồng hồ thì chưa lên tầng hai nhà tôi bao giờ.'),
         (DTV, 'Gần đây có ai hỏi vay tiền ông không?'),
         (None, 'Hôm mùng 10 tháng Ba, chị Tư xin ứng trước sáu chục triệu lo cho đứa cháu nội ốm. Tôi bảo đi Hải Phòng về sẽ tính.'),
         (None, 'Thằng Minh thì tôi nghe anh Hoà kể nó đi vay khắp nơi. Nhưng nó là con chị gái tôi, tôi không tin nó làm chuyện này.')),
     'signature': 'Người khai: Trần Đức Hậu'})

add({'id': 'd04', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của bà Phạm Thị Tư (người giúp việc)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 00 ngày 15/3/2024',
     'fields': [{'label': 'Người khai', 'value': 'Phạm Thị Tư, 59 tuổi'}, {'label': 'Quan hệ', 'value': 'Giúp việc, ở cùng nhà 12 năm'}],
     'lines': tl('Phạm Thị Tư', 
         (DTV, 'Bà kể lại tối 14/3.'),
         (None, 'Ông đi Hải Phòng từ chiều, trong nhà còn tôi với cậu Minh. Chín rưỡi cậu bảo ra quán đầu ngõ uống cà phê.'),
         (None, 'Mười giờ tôi khoá cửa chính, cài then cổng rồi lên phòng trên tầng ba nằm.'),
         (None, 'Tầm mười một giờ tôi nghe choang một cái ở tầng dưới, sợ quá không dám xuống.'),
         (None, 'Con Mực nhà này người lạ đến là sủa inh ỏi, hôm ông thợ đồng hồ tới lấy đồng hồ nó sủa suốt. Vậy mà đêm qua nó im re.'),
         (DTV, 'Ai biết mã két?'),
         (None, 'Mã két chỉ ông biết thôi. À, tháng trước tôi thấy ông đọc mã cho cậu Minh mở két lấy giấy tờ.'),
         (DTV, 'Sáng nay bà ở đâu?'),
         (None, 'Bảy rưỡi tôi đi chợ Hàng Bè như mọi ngày, tám giờ bốn mươi về thì đã thấy công an đầy nhà.'),
         (None, 'Cậu Minh về lúc nào tôi không biết. Cậu ấy dạo này hay bị người ta gọi điện đòi tiền.')),
     'signature': 'Người khai: Phạm Thị Tư'})

add({'id': 'd05', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của Nguyễn Quang Minh (cháu ông Hậu)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 45 ngày 15/3/2024',
     'fields': [{'label': 'Người khai', 'value': 'Nguyễn Quang Minh, 27 tuổi'}, {'label': 'Quan hệ', 'value': 'Cháu gọi ông Hậu là cậu, ở nhờ từ tháng 1/2024'}],
     'lines': tl('Nguyễn Quang Minh', 
         (DTV, 'Tối 14/3 anh ở đâu?'),
         (None, 'Chín rưỡi tôi ra quán cà phê Gác Nhỏ ở đầu ngõ, ngồi một mình lướt điện thoại.'),
         (DTV, 'Anh về nhà lúc mấy giờ?'),
         (None, 'Tôi ngồi ở quán tới khoảng mười một rưỡi mới về.'),
         (None, 'Cổng cài then bên trong nên tôi vòng ra ngõ sau trèo tường vào, vào bằng cửa bếp. Lúc đó tôi thấy kính rơi đầy sân, tưởng gió đánh vỡ.'),
         (DTV, 'Anh có nợ ai tiền không?'),
         (None, 'Không. Ai nói với các anh thế?'),
         (DTV, 'Anh có biết mã két không?'),
         (None, 'Tôi không biết. Cậu tôi chẳng bao giờ nói chuyện tiền nong với tôi.'),
         (None, 'Chắc chắn là trộm ở ngoài vào. Ngõ này dạo này mất xe suốt.')),
     'signature': 'Người khai: Nguyễn Quang Minh'})

add({'id': 'd06', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của ông Lâm Văn Hoà (bạn làm ăn)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '16 giờ 00 ngày 15/3/2024',
     'fields': [{'label': 'Người khai', 'value': 'Lâm Văn Hoà, 61 tuổi, kinh doanh đồ cổ'}, {'label': 'Quan hệ', 'value': 'Bạn làm ăn của ông Hậu gần 20 năm'}],
     'lines': tl('Lâm Văn Hoà', 
         (DTV, 'Ông có quan tâm tới chiếc đồng hồ bị mất không?'),
         (None, 'Có chứ. Tôi trả anh Hậu ba trăm triệu từ năm ngoái, anh ấy không chịu bán. Đồ tốt thì ai chẳng thèm.'),
         (DTV, 'Đêm 14/3 ông ở đâu?'),
         (None, 'Tôi lái xe đưa anh Hậu xuống Hải Phòng dự tiệc mừng thọ ông Bảy Lực. Tiệc tới gần nửa đêm, hai anh em ngủ khách sạn, sáng năm rưỡi lái về.'),
         (DTV, 'Ông có biết mã két nhà ông Hậu không?'),
         (None, 'Không. Mà sao tôi phải biết?'),
         (None, 'Tuần trước thằng Minh tìm tôi vay tám chục triệu, nói nợ bạn đánh bài, phải trả gấp. Tôi không cho, tôi biết tính nó.'),
         (None, 'Các anh cứ hỏi tiệm đồ cổ quanh Hàng Đào, đồ của anh Hậu ai cầm ra là người ta nhận ra ngay.')),
     'signature': 'Người khai: Lâm Văn Hoà'})

# ───────────── Vòng 2 ─────────────
add({'id': 'd07', 'stage': 2, 'type': 'receipt', 'title': 'Hoá đơn quán Cà phê Gác Nhỏ, bàn 04',
     'shop': 'Cà phê Gác Nhỏ', 'address': 'Số 2, đầu ngõ Gác Chuông',
     'fields': [{'label': 'Ngày', 'value': '14/03/2024'}, {'label': 'Bàn', 'value': '04'}, {'label': 'Giờ vào', 'value': '21:36'}, {'label': 'Giờ in', 'value': '22:41'}],
     'items': [{'name': 'Cà phê đen đá', 'qty': '1', 'price': '25.000'}, {'name': 'Hướng dương', 'qty': '1', 'price': '15.000'}],
     'total': '40.000đ', 'footer': ['Tiền mặt. Cảm ơn quý khách!', '**Quán đóng cửa lúc 22:45 hằng ngày.**']})

add({'id': 'd08', 'stage': 2, 'type': 'photo', 'title': 'Ảnh trích xuất camera tiệm tạp hoá đầu ngõ',
     'image': 'images/d07-camera.webp', 'label': 'Camera tiệm tạp hoá Thanh Mai · 14/3/2024',
     'caption': '22:53: một người mặc áo nỉ xám có mũ, quần sẫm, giày trắng đi bộ vào ngõ, hướng về phía nhà số 17. Từ 22:00 đến 06:00 camera không ghi được ai khác vào ngõ.'})

add({'id': 'd09', 'stage': 2, 'type': 'report', 'title': 'Biên bản xác minh tại Hải Phòng',
     'header': CA, 'heading': 'Biên bản xác minh', 'code': '22/XM', 'date': '10 giờ 00 ngày 16/3/2024',
     'fields': [{'label': 'Nội dung', 'value': 'Xác minh nơi ở đêm 14/3/2024 của ông Trần Đức Hậu và ông Lâm Văn Hoà'}],
     'sections': [
         {'heading': '1. Tiệc mừng thọ', 'paragraphs': ['Gia đình ông Đinh Văn Lực (phường Lạch Tray) cung cấp video quay tiệc: lúc 23:10 ông Lâm Văn Hoà cầm micro chúc thọ, ông Trần Đức Hậu đứng cạnh. Tiệc kết thúc khoảng 23:50.']},
         {'heading': '2. Khách sạn', 'paragraphs': ['Khách sạn Cát Bi Garden: hai ông nhận phòng 412 lúc 00:15 ngày 15/3, trả phòng 05:30. Camera hành lang tầng 4 không ghi nhận ai ra khỏi phòng 412 trong đêm.']},
         {'heading': '3. Kết luận', 'paragraphs': ['Từ 21:00 ngày 14/3 đến 05:30 ngày 15/3, ông Hậu và ông Hoà ở Hải Phòng, cách Hà Nội khoảng 120 km.']}],
     'signers': [{'role': DTV, 'name': 'Thượng uý Đỗ Văn Tâm'}]})

add({'id': 'd10', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của ông Đào Quang Lộc (thợ sửa đồng hồ)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 00 ngày 16/3/2024',
     'fields': [{'label': 'Người khai', 'value': 'Đào Quang Lộc, 52 tuổi'}, {'label': 'Nghề nghiệp', 'value': 'Thợ sửa đồng hồ, số 41 phố Hàng Đào'}],
     'lines': tl('Đào Quang Lộc', 
         (DTV, 'Ông có giữ chiếc đồng hồ của ông Hậu không?'),
         (None, 'Có. Mùng 1 tháng Ba tôi đến nhà lấy về lau dầu, mùng 4 trả. Con chó nhà ấy sủa tôi ầm cả ngõ.'),
         (DTV, 'Ngoài lau dầu ông còn làm gì với chiếc đồng hồ?'),
         (None, 'Không, lau dầu thôi. Đồ của khách tôi không đụng vào.'),
         (DTV, 'Cửa hàng ông đang nợ tiền thuê?'),
         (None, 'Ba tháng rồi, chủ nhà dọa lấy lại mặt bằng. Nhưng nghèo thì nghèo, tôi làm nghề ba chục năm chưa lấy của ai cái gì.'),
         (DTV, 'Đêm 14/3 ông ở đâu?'),
         (None, 'Vợ tôi mổ ruột thừa ở Việt Đức chiều hôm ấy. Tôi ở viện trông cả đêm, các anh hỏi điều dưỡng khoa là biết.')),
     'signature': 'Người khai: Đào Quang Lộc'})

add({'id': 'd11', 'stage': 2, 'type': 'note', 'title': 'Trích sổ nhận sửa của tiệm đồng hồ Lộc, tháng 3/2024',
     'paragraphs': [
         'Sổ bìa xanh ghi tay, thu tại tiệm số 41 Hàng Đào ngày 16/3/2024:',
         '— 01/3: Nhận của ông Hậu (ngõ Gác Chuông) 01 đồng hồ bỏ túi vỏ vàng, khắc T.Đ.H. Lau dầu, chỉnh giờ. **Số máy 31.774.**',
         '__— 02/3: Ông Hoà (bạn ông Hậu) đến, nhờ chụp ảnh máy, ghi số máy, đo đường kính vỏ chiếc T.Đ.H. Nhận 2.000.000đ. Không báo chủ.__',
         '— 03/3: Thay dây cót đồng hồ treo tường cho bà Thu, Hàng Bạc.',
         '— 04/3: Trả đồng hồ T.Đ.H cho ông Hậu. Thu 800.000đ.'],
     'signature': 'Chủ tiệm: Lộc'})

add({'id': 'd12', 'stage': 2, 'type': 'letter', 'title': 'Giấy xác nhận của điều dưỡng Bệnh viện Việt Đức',
     'date': 'Hà Nội, ngày 16 tháng 3 năm 2024',
     'greeting': 'Kính gửi: Đội Cảnh sát hình sự, Công an quận Hoàn Kiếm',
     'paragraphs': [
         'Khoa Phẫu thuật tiêu hoá xác nhận: bệnh nhân Nguyễn Thị Hằng (giường 18, phòng 305) mổ ruột thừa lúc 16 giờ ngày 14/3/2024.',
         'Người nhà ở lại chăm là ông Đào Quang Lộc, đăng ký thẻ người nhà lúc 19 giờ 40. Ông Lộc có mặt ở các lượt kiểm tra lúc 22 giờ, 0 giờ, 2 giờ và 4 giờ; 23 giờ 15 ông xuống quầy thuốc ký nhận thuốc giảm đau cho bệnh nhân.',
         'Sổ ra vào cổng khoa ghi ông Lộc rời khoa lúc 6 giờ 10 sáng 15/3.'],
     'signature': 'Điều dưỡng trưởng ca: Vũ Thị Ngân'})

# ───────────── Vòng 3 ─────────────
add({'id': 'd13', 'stage': 3, 'type': 'evidence', 'title': 'Phiếu cầm đồ thu giữ tại tiệm Phát Đạt',
     'code': 'TV-03', 'image': 'images/d08-watch.webp', 'imageCaption': 'Chiếc đồng hồ bỏ túi thu giữ tại tiệm cầm đồ Phát Đạt ngày 16/3/2024.',
     'fields': [{'label': 'Tiệm', 'value': 'Cầm đồ Phát Đạt, phố Hàng Rèn (cách chợ Hàng Bè khoảng 200 m)'},
                {'label': 'Thời gian', 'value': '08 giờ 15 ngày 15/3/2024'},
                {'label': 'Tài sản cầm', 'value': '01 đồng hồ bỏ túi vỏ vàng, nắp sau khắc T.Đ.H'},
                {'label': 'Số tiền', 'value': '60.000.000đ, tiền mặt'},
                {'label': 'Giấy tờ', 'value': 'Bản photo căn cước của Nguyễn Quang Minh; người cầm ký "Minh"'}],
     'paragraphs': [
         'Chủ tiệm khai: người cầm vào lúc tiệm vừa mở, trùm mũ áo nỉ xám, đeo khẩu trang, **tay áo trái có một vệt sơn trắng**. Dáng nhỏ, thấp hơn chủ tiệm (cao 1,68 m) gần một cái đầu, nói rất ít, giọng nhỏ.',
         'Người đó không đưa căn cước gốc, chỉ có bản photo, nói "để quên ở nhà". Chủ tiệm nhận vì món đồ có giá. Chiều 15/3 đọc báo Phố Cũ, chủ tiệm báo công an.']})

add({'id': 'd14', 'stage': 3, 'type': 'testimony', 'title': 'Biên bản ghi lời khai lần hai của Nguyễn Quang Minh',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '16 giờ 30 ngày 16/3/2024',
     'fields': [{'label': 'Người khai', 'value': 'Nguyễn Quang Minh, 27 tuổi (cao 1,78 m)'}],
     'lines': tl('Nguyễn Quang Minh', 
         (DTV, 'Quán đóng cửa lúc 22 giờ 45, camera ghi anh vào ngõ lúc 22 giờ 53. Anh giải thích sao?'),
         (None, 'Tôi xin lỗi. Tôi về lúc đấy thật. Cổng cài nên tôi trèo tường sau, vừa đặt chân xuống sân thì choang một cái, kính rơi lả tả lên đầu.'),
         (None, 'Tôi nép vào góc tường, nhìn lên thì thấy đèn phòng cậu tôi tắt phụt. Tôi sợ quá, vào bếp rồi lên phòng nằm im.'),
         (DTV, 'Sao anh không báo ai?'),
         (None, 'Tôi đang nợ tám chục triệu tiền bài, người ta đòi ráo riết. Tôi biết kiểu gì cũng bị nghi đầu tiên.'),
         (DTV, 'Chiếc áo nỉ xám của anh có đặc điểm gì?'),
         (None, 'Tay trái dính vệt sơn trắng hồi Tết tôi sơn cổng. Đêm đó áo ướt mưa, tôi cởi ra ném vào giỏ đồ bẩn ở chân cầu thang sau. Sáng nay không thấy đâu nữa.'),
         (DTV, 'Bản photo căn cước của anh ở đâu?'),
         (None, 'Tháng Giêng tôi đưa bà Tư một bản để bà nộp tạm trú cho tổ dân phố. Bà vẫn giữ túi giấy tờ trong nhà.'),
         (None, 'Sáng 15 cậu tôi gọi tôi dậy lúc gần tám giờ, tôi ở cạnh cậu suốt. Tôi chưa bao giờ bước chân vào tiệm Phát Đạt.')),
     'signature': 'Người khai: Nguyễn Quang Minh'})

add({'id': 'd15', 'stage': 3, 'type': 'report', 'title': 'Kết luận giám định đồng hồ, chữ ký và mảnh kính',
     'header': ['Công an thành phố Hà Nội', 'Phòng Kỹ thuật hình sự'], 'heading': 'Kết luận giám định', 'code': '318/GĐ', 'date': 'Ngày 17 tháng 3 năm 2024',
     'fields': [{'label': 'Đối tượng giám định', 'value': 'Đồng hồ thu tại tiệm Phát Đạt; phiếu cầm đồ; mảnh kính thu ở đế giày'}],
     'sections': [
         {'heading': '1. Đồng hồ', 'paragraphs': ['Đồng hồ thu giữ là **đồ thật**: vỏ vàng 18K, máy Thuỵ Sĩ đời 1920, **số máy 31.774**, nắp sau khắc T.Đ.H. Không có dấu hiệu thay máy, thay vỏ.']},
         {'heading': '2. Chữ ký trên phiếu cầm đồ', 'paragraphs': ['So với chữ ký mẫu của Nguyễn Quang Minh (hồ sơ căn cước, các biên bản ghi lời khai): chữ "Minh" trên phiếu cầm đồ viết chậm, nét run, chữ M viết kiểu chữ thường. **Không phải do Nguyễn Quang Minh viết.**']},
         {'heading': '3. Mảnh kính', 'paragraphs': ['4 mảnh kính trong đế giày cùng loại với kính cửa sổ phòng làm việc. Mảnh kính chỉ bám vào đế giày khi người đi giày giẫm lên kính đã rơi xuống nền.']}],
     'signature': 'Giám định viên: Thiếu tá Hà Thị Phương'})

add({'id': 'd16', 'stage': 3, 'type': 'receipt', 'title': 'Phiếu thu tạm ứng viện phí, Bệnh viện Nhi Trung ương',
     'shop': 'Bệnh viện Nhi Trung ương · Phòng Tài chính kế toán', 'address': '18/879 La Thành, Đống Đa, Hà Nội',
     'fields': [{'label': 'Ngày', 'value': '15/03/2024'}, {'label': 'Giờ thu', 'value': '10:20'},
                {'label': 'Bệnh nhân', 'value': 'Phạm Gia Bảo, 9 tuổi, Trung tâm Tim mạch'},
                {'label': 'Người nộp', 'value': 'Phạm Thị Tư (bà nội)'}],
     'items': [{'name': 'Tạm ứng phẫu thuật van tim (lịch mổ 18/3/2024)', 'qty': '1', 'price': '55.000.000'}],
     'total': '55.000.000đ', 'footer': ['Hình thức: **tiền mặt**.', 'Hạn nộp tạm ứng để giữ lịch mổ: 12 giờ ngày 15/3/2024.']})

add({'id': 'd17', 'stage': 3, 'type': 'testimony', 'title': 'Biên bản ghi lời khai bổ sung của bà Phạm Thị Tư',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 00 ngày 17/3/2024',
     'fields': [{'label': 'Người khai', 'value': 'Phạm Thị Tư, 59 tuổi (cao 1,50 m)'}],
     'lines': tl('Phạm Thị Tư', 
         (DTV, 'Sáng 15/3 bà nộp năm mươi lăm triệu tiền mặt cho bệnh viện. Tiền ở đâu ra?'),
         (None, 'Họ hàng dưới Nam Định góp gửi lên cho tôi.'),
         (DTV, 'Sáng hôm ấy bà đi những đâu?'),
         (None, 'Tôi đi chợ Hàng Bè từ bảy rưỡi, mua mớ rau, cân thịt rồi về thẳng.'),
         (DTV, 'Chiếc áo nỉ xám của anh Minh trong giỏ đồ bẩn, bà có thấy không?'),
         (None, 'Có, sáng sớm năm rưỡi tôi giặt luôn rồi phơi ở sân sau, tới trưa vẫn còn ướt.'),
         (DTV, 'Bà có giữ bản photo căn cước của anh Minh không?'),
         (None, 'Tôi giữ túi giấy tờ trong nhà, có hay không thì tôi không nhớ.'),
         (None, '(Im lặng) Thằng cháu tôi mổ ngày 18. Các anh cho tôi vào viện với nó.')),
     'signature': 'Người khai: Phạm Thị Tư'})

S = lambda i: [k for k in ['tu', 'minh', 'hoa', 'loc']].index(i)
questions = [
    {'id': 'q1', 'stage': 1, 'type': 'choice', 'title': 'Trộm vào nhà, hay ai đó dựng cảnh?',
     'prompt': 'Báo chí đưa tin kẻ trộm trèo tường sau, phá cửa sổ vào nhà. Dựa vào hồ sơ đang mở, nhận định nào đứng vững?',
     'options': ['Kẻ trộm từ ngoài vào: trèo tường sau, đập cửa sổ tầng 2 để vào phòng làm việc, rồi bẻ khoá két sắt lấy đồng hồ.',
                 'Cửa sổ bị đập từ bên trong để dựng cảnh trộm; người lấy đồng hồ đã ở trong nhà, mở két bằng đúng mã và không làm chó sủa.'],
     'answer': [1],
     'nudges': {'0': {'message': 'Kính rơi về phía nào? Két có dấu cạy phá không? Và chó becgie ở sân trước đã làm gì đêm đó?'}},
     'hints': ['Xem biên bản khám nghiệm: mảnh kính rơi ở đâu, cửa sổ cao bao nhiêu, két được mở thế nào.',
               'Kính rơi xuống sân sau nhiều hơn rơi vào phòng: lực đập đi từ trong ra. Không có thang, không có dấu leo.',
               'd02: kính văng ra sân sau, không dấu leo, két mở đúng mã, cổng cài trong. d04: con Mực không sủa. Người trong cuộc đã dựng cảnh.'],
     'solved': 'Không có tên trộm nào trèo vào. Chiếc đồng hồ được lấy từ bên trong ngôi nhà.',
     'explanation': [{'title': 'Kính vỡ từ bên trong', 'body': ['d02: phần lớn mảnh kính rơi xuống sân sau, cách chân tường 1–3 m; trong phòng chỉ vài mảnh. Cửa sổ cao 4,2 m, không thang, không dấu leo.']},
                     {'title': 'Két mở đúng mã', 'body': ['d02: không khoan, không cạy; trong két còn tiền mặt và sổ đỏ. Người mở biết mã và chỉ nhắm vào chiếc đồng hồ.']},
                     {'title': 'Chó không sủa', 'body': ['d04: con Mực sủa người lạ, kể cả ông thợ đồng hồ, nhưng đêm 14/3 im lặng. Cổng và cửa chính đều cài từ bên trong (d02).']}]},
    {'id': 'q2', 'stage': 1, 'type': 'choice', 'multiple': True, 'cards': ['tu', 'minh', 'hoa', 'loc'], 'title': 'Ai biết được mã két?',
     'prompt': 'Két được mở bằng đúng mã. Theo lời người duy nhất chắc chắn biết mã, chọn **tất cả** những người có thể biết được mã két.',
     'options': ['Phạm Thị Tư', 'Nguyễn Quang Minh', 'Lâm Văn Hoà', 'Đào Quang Lộc'], 'answer': [0, 2],
     'nudges': {'1': {'message': 'Có người khai ông Hậu từng đọc mã cho Minh. Chính ông Hậu nói gì về chuyện đó?'},
                '3': {'message': 'Ông Lộc từng lên phòng làm việc tầng 2 chưa? Ông có biết ngày giỗ bà Lan không?'}},
     'hints': ['Ông Hậu cho biết mã két được đặt theo một ngày đặc biệt.',
               'Mã là ngày giỗ bà Lan tính theo âm lịch. Ai biết ngày đó?',
               'd03: bà Tư nấu cỗ giỗ 12 năm, ông Hoà năm nào cũng đến thắp hương; Minh mới lên từ tháng Giêng, chưa dự giỗ nào; ông Lộc chưa lên tầng 2.'],
     'solved': 'Mã két là ngày giỗ bà Lan theo âm lịch: chỉ người làm giỗ cùng ông Hậu mới biết.',
     'explanation': [{'title': 'Mã két', 'body': ['d03: mã là ngày giỗ bà Lan tính theo âm lịch; ông Hậu chưa đọc mã cho ai.']},
                     {'title': 'Ai biết ngày giỗ', 'body': ['Bà Tư nấu cỗ giỗ 12 năm; ông Hoà năm nào cũng thắp hương. Minh lên ở từ tháng Giêng, chưa dự giỗ nào; ông Lộc chưa lên tầng 2.']},
                     {'title': 'Một lời khai lệch', 'body': ['d04 dòng 7: bà Tư nói thấy ông Hậu đọc mã cho Minh. d03 dòng 5: tháng trước ông tự mở két lấy sổ hộ khẩu đưa Minh. Hãy ghi nhớ chi tiết này.']}]},
    {'id': 'q3', 'stage': 2, 'type': 'line', 'title': 'Câu khai về giờ về nhà',
     'prompt': 'Một người khai giờ giấc của mình đêm 14/3, nhưng giờ đó bị hai tài liệu mới mở ở vòng này bác bỏ. Chỉ ra dòng khai đó.',
     'answer': ['d05:004'],
     'nudges': {'d05:002': {'near': True, 'message': 'Câu này nói giờ đi, khớp với hoá đơn (giờ vào 21:36). Tìm câu nói giờ về.'},
                'd04:004': {'message': 'Bà Tư nghe tiếng kính vỡ lúc 23 giờ: các tài liệu mới không bác câu này.'}},
     'hints': ['So hoá đơn quán và ảnh camera với lời khai của người ra quán tối hôm đó.',
               'Quán đóng cửa lúc mấy giờ? Camera ghi ai vào ngõ lúc 22:53?',
               'd05 dòng 4: Minh khai ngồi quán tới 23 giờ 30. d07: quán in hoá đơn 22:41, đóng cửa 22:45. d08: 22:53 người mặc áo nỉ xám vào ngõ.'],
     'solved': 'Minh đã về ngõ lúc 22 giờ 53, bảy phút trước khi kính vỡ, chứ không phải 23 giờ 30.',
     'explanation': [{'title': 'Câu khai', 'body': ['d05 dòng 4: ngồi quán tới khoảng 23 giờ 30 mới về.']},
                     {'title': 'Bị bác', 'body': ['d07: hoá đơn in 22:41, quán đóng 22:45. d08: 22:53 người mặc áo nỉ xám vào ngõ; cả đêm không ai khác vào ngõ.']},
                     {'title': 'Ý nghĩa', 'body': ['Minh có mặt ở nhà quanh 23 giờ, lúc kính vỡ (d04, d01). Mảnh kính trong đế giày Minh (d02) khiến anh càng đáng ngờ.']}]},
    {'id': 'q4', 'stage': 2, 'type': 'evidence', 'need': 2, 'title': 'Hai người ở xa đêm hôm ấy',
     'prompt': 'Ông Hoà biết ngày giỗ và từ lâu muốn có chiếc đồng hồ; ông Lộc từng giữ nó ba ngày và đang túng tiền. Ghim 2 tài liệu chứng minh cả hai không thể có mặt ở ngõ Gác Chuông đêm 14/3.',
     'answer': ['d09', 'd12'],
     'nudges': [{'any': ['d11'], 'near': True, 'message': 'Sổ sửa chữa là lý do để nghi ông Hoà và ông Lộc, chưa phải chứng cứ ngoại phạm. Họ ở đâu đêm 14/3?'},
                {'any': ['d06', 'd10'], 'message': 'Đó là lời tự khai. Tìm giấy tờ do người khác lập.'}],
     'hints': ['Mỗi người cần một tài liệu do bên thứ ba xác lập.',
               'Một tài liệu từ Hải Phòng, một tài liệu từ một bệnh viện.',
               'd09: ông Hoà (và ông Hậu) ở tiệc rồi khách sạn ở Hải Phòng cả đêm. d12: ông Lộc ở khoa phẫu thuật Bệnh viện Việt Đức, 23 giờ 15 còn ký nhận thuốc.'],
     'solved': 'Ông Hoà ở Hải Phòng, ông Lộc ở bệnh viện. Còn lại hai người trong ngôi nhà đêm ấy.',
     'explanation': [{'title': 'Ông Hoà', 'body': ['d09: 23:10 cầm micro chúc thọ ở Hải Phòng; nhận phòng khách sạn 00:15, không ra khỏi phòng tới 05:30.']},
                     {'title': 'Ông Lộc', 'body': ['d12: có mặt ở các lượt kiểm tra 22h, 0h, 2h, 4h; 23 giờ 15 ký nhận thuốc; rời khoa 6 giờ 10.']},
                     {'title': 'Sổ sửa chữa', 'body': ['d11: ông Hoà lén nhờ chụp ảnh máy, đo vỏ. Đáng ngờ, nhưng chưa chứng minh có đánh tráo. Còn phải kiểm tra chính chiếc đồng hồ.']}]},
    {'id': 'q5', 'stage': 3, 'type': 'evidence', 'need': 2, 'title': 'Người cầm đồ lúc 8 giờ 15',
     'prompt': 'Phiếu cầm đồ mang tên Minh, kèm bản photo căn cước của Minh, người cầm mặc áo nỉ xám. Ghim 2 tài liệu chứng minh người đem đồng hồ đi cầm **không phải** Minh.',
     'answer': ['d03', 'd15'],
     'nudges': [{'any': ['d14'], 'near': True, 'message': 'Đó là lời Minh tự khai. Ai khác xác nhận Minh ở đâu lúc 8 giờ 15?'},
                {'any': ['d13'], 'message': 'Phiếu cầm đồ là thứ cần bác bỏ. Tìm tài liệu cho thấy người ký không phải Minh, và Minh đang ở chỗ khác.'}],
     'hints': ['Một tài liệu nói Minh ở đâu sáng 15/3; một tài liệu nói về chữ ký.',
               'Ông Hậu về nhà lúc 7 giờ 45 và đã làm gì với Minh?',
               'd03 dòng 3: từ 7 giờ 50 Minh ở cạnh ông Hậu tới khi công an tới và suốt buổi khám nghiệm. d15: chữ "Minh" trên phiếu không do Minh viết.'],
     'solved': 'Lúc 8 giờ 15, Minh đứng cạnh cậu mình trong phòng làm việc. Ai đó đã mặc áo và mang giấy tờ của Minh đi cầm đồ.',
     'explanation': [{'title': 'Minh ở đâu', 'body': ['d03: ông Hậu gọi Minh dậy lúc 7 giờ 50, hai cậu cháu ở cùng nhau tới khi công an đến (8 giờ 30, d02) và suốt buổi khám nghiệm.']},
                     {'title': 'Chữ ký', 'body': ['d15: chữ "Minh" trên phiếu viết chậm, nét run, không phải chữ của Minh.']},
                     {'title': 'Dáng người', 'body': ['d13: người cầm thấp hơn chủ tiệm (1,68 m) gần một cái đầu. d14: Minh cao 1,78 m.']}]},
    {'id': 'q6', 'stage': 3, 'type': 'line', 'title': 'Chiếc áo nỉ xám',
     'prompt': 'Người cầm đồ mặc chiếc áo nỉ có vệt sơn trắng của Minh. Một người đã khai sai về chiếc áo đó vào sáng 15/3. Chỉ ra dòng khai, và nghĩ xem tài liệu nào ở vòng 1 đã bác nó.',
     'answer': ['d17:006'],
     'nudges': {'d17:004': {'near': True, 'message': 'Câu này đáng ngờ (chợ Hàng Bè sát phố Hàng Rèn), nhưng chưa có gì bác trực tiếp. Tìm câu nói về chiếc áo.'},
                'd17:002': {'near': True, 'message': 'Câu về tiền viện phí rất đáng ngờ. Nhưng câu hỏi này là về chiếc áo nỉ.'},
                'd14:007': {'message': 'Minh nói áo bị ném vào giỏ đồ bẩn và sáng ra không thấy. Ai đã đụng vào giỏ đồ bẩn?'}},
     'hints': ['Ai giặt giũ trong nhà? Người đó nói gì về chiếc áo nỉ?',
               'Lúc công an khám nghiệm sân sau (8 giờ 30–9 giờ 30), trên dây phơi có gì?',
               'd17 dòng 6: bà Tư nói giặt áo lúc 5 giờ 30, phơi ở sân sau tới trưa. d02: dây phơi sân sau không có đồ phơi. d13: 8 giờ 15 chiếc áo đang ở tiệm cầm đồ.'],
     'solved': 'Chiếc áo không nằm trên dây phơi buổi sáng hôm đó. Nó đang ở tiệm cầm đồ Hàng Rèn, trên người khác.',
     'explanation': [{'title': 'Câu khai', 'body': ['d17 dòng 6: giặt áo nỉ lúc 5 giờ 30, phơi ở sân sau, tới trưa còn ướt.']},
                     {'title': 'Bị bác', 'body': ['d02 (khám nghiệm 8 giờ 30–9 giờ 30): dây phơi sân sau không có đồ phơi. d13: 8 giờ 15 người cầm đồ mặc áo nỉ xám có vệt sơn trắng tay trái, đúng chiếc áo của Minh (d14).']},
                     {'title': 'Ai có áo và giấy tờ', 'body': ['d14: Minh ném áo vào giỏ đồ bẩn đêm 14/3, và đưa bản photo căn cước cho bà Tư nộp tạm trú.']}]},
    {'id': 'q-accuse', 'stage': 3, 'type': 'choice', 'cards': ['tu', 'minh', 'hoa', 'loc'], 'title': 'Chỉ mặt người lấy đồng hồ',
     'prompt': 'Ai đã mở két lấy chiếc đồng hồ của ông Trần Đức Hậu? Chọn một người.',
     'options': ['Phạm Thị Tư', 'Nguyễn Quang Minh', 'Lâm Văn Hoà', 'Đào Quang Lộc'], 'answer': [0],
     'nudges': {'1': {'message': 'Minh không biết mã két (d03), và lúc đồng hồ bị đem cầm thì Minh ở cạnh ông Hậu (d03, d15).'},
                '2': {'message': 'Ông Hoà ở Hải Phòng cả đêm (d09).'},
                '3': {'message': 'Ông Lộc ở Bệnh viện Việt Đức cả đêm (d12) và không biết mã két.'}},
     'hints': ['Người lấy phải biết mã két, ở trong nhà đêm 14/3, và có thể ra phố Hàng Rèn lúc 8 giờ 15 sáng 15/3.',
               'Ai giữ giỏ đồ bẩn và túi giấy tờ trong nhà? Ai cần tiền gấp trước trưa 15/3?',
               'Bà Tư: biết ngày giỗ (d03), ở nhà một mình 22h–22h53, đi chợ Hàng Bè 7h30–8h40 (d04), nói dối về chiếc áo (d17), nộp 55 triệu tiền mặt lúc 10h20 (d16).'],
     'solved': 'Phạm Thị Tư. Người giúp việc mười hai năm của ông Hậu.',
     'explanation': [{'title': 'Biết mã, ở trong nhà', 'body': ['d03: bà nấu cỗ giỗ bà Lan 12 năm. Từ 21h30 tới 22h53 bà ở nhà một mình (d04, d07, d08).']},
                     {'title': 'Đem đi cầm', 'body': ['d04, d17: đi chợ Hàng Bè 7h30–8h40, cách tiệm Phát Đạt 200 m (d13). Người cầm dáng nhỏ; bà cao 1,50 m.']},
                     {'title': 'Tiền', 'body': ['d16: 10h20 nộp 55 triệu tiền mặt viện phí cho cháu nội, hạn chót trưa 15/3. Tiệm cầm đồ chi 60 triệu tiền mặt lúc 8h15 (d13).']}]},
    {'id': 'q7', 'stage': 3, 'type': 'choice', 'title': 'Kết luận điều tra',
     'prompt': 'Chọn bản kết luận đúng với hồ sơ ở mọi chi tiết: người lấy, cách mở két, cách dựng cảnh, người đem cầm và động cơ.',
     'options': [
         'Bà Tư mở két bằng mã là ngày giỗ bà Lan theo âm lịch lúc Minh ra quán, khoảng 23 giờ đập kính từ bên trong cho giống trộm vào; sáng 15/3 mặc áo nỉ của Minh, dùng bản photo căn cước của Minh đem đồng hồ cầm 60 triệu để nộp viện phí cho cháu nội.',
         'Minh về lúc 22 giờ 53, trèo tường sau, mở két bằng mã được ông Hậu đọc cho từ tháng trước, đập kính từ bên trong; sáng 15/3 mặc chính áo nỉ của mình, mang căn cước đem đồng hồ cầm 60 triệu để trả khoản nợ đánh bài.',
         'Ông Hoà nhờ thợ Lộc chụp ảnh máy và đo vỏ để làm một chiếc đồng hồ giả, đêm 14/3 thuê người lẻn vào nhà đánh tráo; chiếc đồng hồ ở tiệm cầm đồ chỉ là bản giả do ông Lộc làm.',
         'Bà Tư và Minh thông đồng: Minh đọc mã két qua điện thoại cho bà mở, bà đập kính lúc Minh còn ở quán; sáng 15/3 Minh tự mang đồng hồ đi cầm rồi hai người chia nhau tiền trả nợ và viện phí.'],
     'answer': [0],
     'exam': {'examiner': 'Kiểm sát viên Nguyễn Thanh Bình',
              'intro': 'Trình bày kết luận trước kiểm sát viên: trả lời lần lượt từng câu hỏi bằng lời của mình. Không dùng được AI thì bấm “Trả lời bằng trắc nghiệm” để chọn bản kết luận đúng.'},
     'nudges': {'1': {'message': 'Ông Hậu chưa đọc mã cho Minh (d03), và lúc 8 giờ 15 Minh ở cạnh ông Hậu (d03, d15).'},
                '2': {'message': 'Đồng hồ thu giữ là đồ thật, số máy khớp sổ sửa chữa (d15, d11); ông Hoà ở Hải Phòng (d09).'},
                '3': {'message': 'Minh không biết mã két, và không phải người ký phiếu cầm đồ (d15).'}},
     'hints': ['So từng phương án với: ai biết mã, kính vỡ lúc nào, ai ký phiếu cầm đồ, đồng hồ thật hay giả.',
               'Chỉ một phương án khớp cả mã két (d03), chữ ký (d15) và đồng hồ thật (d15).',
               'Phương án A: bà Tư, mã ngày giỗ âm lịch, đập kính từ trong lúc 23 giờ, áo nỉ và bản photo căn cước của Minh, 60 triệu nộp viện phí.'],
     'solved': 'Hồ sơ khép lại với tên Phạm Thị Tư.',
     'explanation': [{'title': 'Mở két và dựng cảnh', 'body': ['Mã két là ngày giỗ bà Lan theo âm lịch (d03), bà Tư nấu cỗ giỗ 12 năm. Kính văng ra sân sau (d02): cửa sổ bị đập từ bên trong lúc 23 giờ (d04, d14).']},
                     {'title': 'Đem cầm', 'body': ['8 giờ 15: người dáng nhỏ mặc áo nỉ có vệt sơn của Minh, dùng bản photo căn cước của Minh (d13, d14). Minh ở cạnh ông Hậu (d03); chữ ký không phải của Minh (d15).']},
                     {'title': 'Động cơ', 'body': ['d16: 10 giờ 20 nộp 55 triệu tiền mặt giữ lịch mổ tim cho cháu nội, hạn trưa 15/3. d03: bà xin ứng 60 triệu, ông Hậu hẹn để sau.']}]},
]

case = {
    'id': 'demo-01', 'no': 0, 'status': 'available',
    'title': 'Chiếc đồng hồ ở ngõ Gác Chuông',
    'subtitle': 'Hồ sơ nhập môn: một đêm mất trộm, bốn người bị nghi',
    'tagline': 'Cửa sổ vỡ, két sắt mở đúng mã, con chó becgie không sủa một tiếng.',
    'difficulty': 2, 'players': '1–4', 'duration': '45–60 phút',
    'setting': 'Phố cổ, Hà Nội (hư cấu)', 'era': 'Tháng 3/2024',
    'tags': ['Trộm cắp', 'Nhập môn', 'Phố cổ'], 'cover': 'images/cover.webp',
    'synopsis': ['Đêm 14/3/2024, trong lúc nhà sưu tầm Trần Đức Hậu dự tiệc ở Hải Phòng, chiếc đồng hồ bỏ túi vỏ vàng quý nhất của ông biến mất khỏi két sắt.',
                 'Cửa sổ phòng làm việc bị đập vỡ, báo chí đồn có trộm trèo tường vào. Nhưng két được mở đúng mã, và trong căn nhà ngõ Gác Chuông đêm ấy vẫn còn người.'],
    'intro': {'title': 'Chiếc đồng hồ ở ngõ Gác Chuông',
              'paragraphs': ['Sáng 15/3/2024, ông Trần Đức Hậu (68 tuổi) từ Hải Phòng trở về căn nhà số 17 ngõ Gác Chuông và phát hiện chiếc đồng hồ bỏ túi vỏ vàng đời 1920, khắc chữ T.Đ.H, đã biến mất khỏi két sắt trong phòng làm việc.',
                             'Một ô kính cửa sổ bị đập vỡ. Hàng xóm kể nghe tiếng kính vỡ lúc gần nửa đêm. Ai cũng nghĩ đến một tên trộm trèo tường.',
                             'Bạn là điều tra viên được giao hồ sơ. Đọc kỹ, đối chiếu từng giờ giấc và từng lời khai: bốn người có lý do để bị nghi, nhưng chỉ một người đã mở chiếc két đó.'],
              'objective': 'Tìm ra ai đã lấy chiếc đồng hồ, bằng cách nào, đã đem nó đi đâu và vì sao.'},
    'victim': {'id': 'hau', 'name': 'Trần Đức Hậu', 'age': 68, 'role': 'Người bị hại, nhà sưu tầm đồng hồ cổ', 'image': 'images/id-hau.webp',
               'note': 'Sống ở nhà số 17 ngõ Gác Chuông. Vợ mất năm 1998. Mất chiếc đồng hồ bỏ túi vỏ vàng đời 1920 (định giá khoảng 300 triệu đồng) khỏi két sắt đêm 14/3/2024.'},
    'suspects': [
        {'id': 'tu', 'name': 'Phạm Thị Tư', 'age': 59, 'role': 'Giúp việc 12 năm', 'image': 'images/id-tu.webp', 'voice': 'F3',
         'suspicion': 'Giữ chìa khoá và lo việc nhà. Cháu nội đang nằm viện, gia đình cần tiền gấp. Đêm 14/3 ở nhà.'},
        {'id': 'minh', 'name': 'Nguyễn Quang Minh', 'age': 27, 'role': 'Cháu ông Hậu, ở nhờ', 'image': 'images/id-minh.webp', 'voice': 'M2',
         'suspicion': 'Thất nghiệp, lên ở nhờ từ tháng Giêng. Có tin đồn nợ nần. Đêm 14/3 ra quán, không ai rõ về lúc nào.'},
        {'id': 'hoa', 'name': 'Lâm Văn Hoà', 'age': 61, 'role': 'Bạn buôn đồ cổ', 'image': 'images/id-hoa.webp', 'voice': 'M4',
         'suspicion': 'Nhiều lần trả 300 triệu cho chiếc đồng hồ mà ông Hậu không bán. Thân thiết, hay lên nhà chơi.'},
        {'id': 'loc', 'name': 'Đào Quang Lộc', 'age': 52, 'role': 'Thợ sửa đồng hồ phố Hàng Đào', 'image': 'images/id-loc.webp', 'voice': 'M5',
         'suspicion': 'Giữ chiếc đồng hồ ba ngày đầu tháng Ba để lau dầu. Cửa hàng đang nợ ba tháng tiền thuê.'}],
    'aiInterrogation': True,
    'audio': {'intro': 'audio/intro.mp3', 'finale': 'audio/finale.mp3'},
    'documents': docs,
    'questions': questions,
    'beats': [
        {'stage': 2, 'kicker': 'Sáng 16/3/2024 · Công an quận Hoàn Kiếm', 'title': 'Những người ở xa',
         'voice': 'audio/beat-2.mp3', 'paragraphs': ['Không có tên trộm nào trèo tường. Ai đó đã mở két bằng đúng mã, rồi đập cửa sổ từ bên trong.',
                        'Đại uý Khải cho người đi Hải Phòng, ghé tiệm đồng hồ phố Hàng Đào và xin trích xuất camera đầu ngõ. Chủ quán Gác Nhỏ lục lại xấp hoá đơn tối 14/3.',
                        'Ai thật sự ở xa đêm hôm ấy? Và người cháu đã về nhà lúc nào?']},
        {'stage': 3, 'kicker': 'Chiều 16/3/2024 · Tiệm cầm đồ Phát Đạt, phố Hàng Rèn', 'title': 'Tờ phiếu mang tên người khác',
         'voice': 'audio/beat-3.mp3', 'paragraphs': ['Chủ tiệm Phát Đạt đọc báo chiều, gọi điện cho công an. Chiếc đồng hồ khắc T.Đ.H nằm trong tủ kính của tiệm từ 8 giờ 15 sáng hôm qua.',
                        'Tờ phiếu ghi tên Nguyễn Quang Minh. Minh được mời lên lần hai, mặt tái đi khi nhìn thấy chữ ký. "Đây không phải chữ của tôi."',
                        'Ai đã mặc chiếc áo của Minh, cầm giấy tờ của Minh, đi qua phố Hàng Rèn sáng hôm ấy?']}],
    'finale': {'title': 'Chiếc đồng hồ ở ngõ Gác Chuông',
               'paragraphs': ['Sáng 17/3/2024, Đại uý Khải đặt lên bàn phiếu thu viện phí 55 triệu đồng và tờ phiếu cầm đồ ký chữ "Minh". Bà Tư nhìn hai tờ giấy rất lâu rồi bật khóc.',
                              '"Thằng Bảo mổ tim ngày 18. Bệnh viện bảo trưa 15 không nộp đủ tiền thì mất lịch. Tôi xin ông, ông bảo đi Hải Phòng về rồi tính. Tôi không đợi được nữa."',
                              'Tối 14/3, khi Minh vừa ra quán, bà Tư lên tầng 2, mở két bằng ngày giỗ bà Lan, ngày bà đã nấu cỗ suốt mười hai năm. Gần 23 giờ, bà đập ô kính từ bên trong cho giống trộm vào, không biết Minh đang đứng ngay dưới sân.',
                              'Sáng hôm sau, bà lấy chiếc áo nỉ còn trong giỏ đồ bẩn và bản photo căn cước Minh gửi làm tạm trú, đi chợ Hàng Bè như mọi ngày rồi rẽ sang phố Hàng Rèn. Bà không định đổ tội cho Minh, nhưng khi bị hỏi, bà đã nói ông Hậu từng đọc mã két cho cậu.',
                              'Ông Hậu đến đồn chiều hôm ấy. Ông nhận lại chiếc đồng hồ, ngồi im rất lâu, rồi hỏi: "Ca mổ của thằng bé có kịp không?"']},
    'epilogue': [
        {'title': 'Phạm Thị Tư', 'text': 'Ông Hậu làm đơn xin giảm nhẹ và tự trả nốt tiền viện phí. Bà Tư bị xử án treo, không quay lại ngõ Gác Chuông nữa.'},
        {'title': 'Phạm Gia Bảo', 'text': 'Ca mổ van tim diễn ra đúng ngày 18/3. Một tháng sau cậu bé được về quê Nam Định.'},
        {'title': 'Nguyễn Quang Minh', 'text': 'Bị phạt hành chính vì đánh bạc trực tuyến. Minh xin vào làm thợ phụ ở tiệm đồng hồ của ông Lộc.'},
        {'title': 'Lâm Văn Hoà', 'text': 'Thôi trả giá chiếc đồng hồ. Ông Hậu vẫn mời ông đến thắp hương bà Lan mỗi năm.'}],
}

import os
for person in [case['victim'], *case['suspects']]:  # portraits not generated yet: leave the blank ID frame
    if person.get('image') and not os.path.exists('public/cases/demo-01/' + person['image']):
        print('chưa có ảnh:', person['image']); del person['image']
json.dump(case, open('public/cases/demo-01/case.json', 'w'), ensure_ascii=False, indent=2)
open('public/cases/demo-01/case.json', 'a').write('\n')
print(len(docs), 'docs', len(questions), 'questions')
