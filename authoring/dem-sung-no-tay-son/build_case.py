"""Dựng public/cases/dem-sung-no-tay-son/case.json (bản 2: hư cấu hoá, khó, có đồng phạm). Chạy ở thư mục gốc:
python3 authoring/dem-sung-no-tay-son/build_case.py

Lời giải: tay súng Tạ Văn Cường + người báo tin là lái xe Đặng Quốc Tuấn. Xem bible.md.
"""
import json
import os

CID = 'dem-sung-no-tay-son'
CA = ['Công an thành phố Hà Nội', 'Phòng Cảnh sát hình sự']
DTV = 'Điều tra viên'
DTV_NAME = 'Thiếu tá Hoàng Minh Đức'


def tl(name, *pairs):
    return [{'n': i + 1, 'speaker': s or name, 'text': t} for i, (s, t) in enumerate(pairs)]


D = []
add = D.append

# ───────────── Vòng 1: kẻ cướp biết trước ─────────────
add({'id': 'd00', 'stage': 1, 'type': 'people', 'title': 'Nạn nhân và những người liên quan',
     'paragraphs': ['Ảnh thẻ trích từ hồ sơ hộ khẩu và hồ sơ đối tượng, kèm lý do từng người được đưa vào diện xác minh sáng 27/8/1998.']})

add({'id': 'd01', 'stage': 1, 'type': 'newspaper', 'title': 'Báo Thủ đô Chiều: Nổ súng cướp vàng trong đêm mưa',
     'masthead': 'Thủ đô Chiều', 'issue': 'Số 2.906', 'date': 'Thứ Năm, 27/8/1998',
     'headline': 'Nổ súng cướp vàng giữa đêm mưa giông ở phố Chùa Bộc',
     'deck': 'Chủ tiệm vàng Phúc Hưng tử vong ngay trước cửa nhà, kẻ cướp phóng xe máy biến mất.',
     'image': 'images/d01-bao-chi.webp', 'imageCaption': 'Ngõ bên hông tiệm vàng Phúc Hưng sáng 27/8.',
     'paragraphs': [
         'Khoảng 22 giờ 40 tối 26/8, giữa cơn mưa giông lớn, ông Lương Văn Phúc (58 tuổi), chủ tiệm vàng Phúc Hưng trên phố Chùa Bộc (quận Đống Đa), bị một đối tượng mặc áo mưa, đội mũ bảo hiểm nổ súng bắn trước cửa ngách nhà mình.',
         'Kẻ cướp giật một chiếc cặp da rồi phóng xe máy vào ngõ. Ông Phúc tử vong tại chỗ. Theo người nhà, trong cặp có khoảng 60 lượng vàng.',
         'Tiếng sấm át cả tiếng súng, nhiều nhà hàng xóm không hay biết. Công an thành phố Hà Nội đã lập chuyên án.']})

add({'id': 'd02', 'stage': 1, 'type': 'report', 'title': 'Biên bản khám nghiệm hiện trường cửa ngách tiệm vàng Phúc Hưng',
     'header': CA, 'heading': 'Biên bản khám nghiệm hiện trường', 'code': '233/KNHT', 'date': '23 giờ 30 ngày 26/8/1998',
     'fields': [{'label': 'Địa điểm', 'value': 'Cửa ngách (ngõ bên hông) tiệm vàng Phúc Hưng, phố Chùa Bộc, quận Đống Đa'},
                {'label': 'Người chết', 'value': 'Lương Văn Phúc, 58 tuổi, chủ tiệm'}],
     'sections': [
         {'heading': '1. Hiện trường', 'paragraphs': ['Tử thi nằm ngay bậc cửa ngách. Cửa ngách mở vào trong, then đã mở. Mặt tiền tiệm (cửa sắt kéo) khoá nguyên; tủ kính bày vàng trong tiệm **nguyên vẹn, không bị đụng tới**.']},
         {'heading': '2. Dấu vết', 'paragraphs': ['Thu **2 vỏ đạn** súng ngắn cỡ 7,62 mm cách tử thi 2–3 m về phía trong ngõ.',
                                                    'Trên nền đất trong ngõ có vệt lốp xe máy bánh nhỏ, vết trượt hướng ra ngõ sau. Mưa xoá phần lớn dấu giày.']},
         {'heading': '3. Ghi nhận', 'paragraphs': ['Cửa ngách chỉ mở vào tối thứ Tư hằng tuần, theo lời gia đình. Ngày thường đóng then trong.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd03', 'stage': 1, 'type': 'report', 'title': 'Kết quả giám định pháp y sơ bộ',
     'header': ['Viện Pháp y', 'Công an thành phố Hà Nội'], 'heading': 'Kết quả giám định sơ bộ', 'code': '418/PY', 'date': 'Ngày 27 tháng 8 năm 1998',
     'sections': [
         {'heading': 'Kết luận', 'paragraphs': ['Nạn nhân trúng hai phát đạn súng ngắn ở vùng ngực, bắn ở cự ly gần (dưới 2 m). Tử vong gần như ngay lập tức, khoảng 22:40–22:45 ngày 26/8/1998.',
                                                 'Không có dấu hiệu vật lộn. Đầu đạn đã thu gửi giám định đạn đạo.']}],
     'signature': 'Giám định viên: BS. Ngô Văn Thịnh'})

add({'id': 'd04', 'stage': 1, 'type': 'scan', 'title': 'Sơ đồ hiện trường tiệm vàng Phúc Hưng',
     'image': 'images/d04-so-do-hien-truong.webp', 'caption': 'Sơ đồ lập khi khám nghiệm: mặt tiền, cửa ngách, ngõ bên hông, ngõ sau và nhà gửi xe.'})

add({'id': 'd05', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của bà Trần Thị Hạnh (vợ nạn nhân)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '08 giờ 00 ngày 27/8/1998',
     'fields': [{'label': 'Người khai', 'value': 'Trần Thị Hạnh, 54 tuổi, vợ ông Phúc, đồng chủ tiệm'}],
     'lines': tl('Trần Thị Hạnh',
         (DTV, 'Những ai biết tối thứ Tư ông Phúc mang vàng về?'),
         (None, 'Thứ Tư nào ông nhà tôi cũng lên chi nhánh Hàng Bạc lấy vàng về cất két nhà, đi cửa ngách cho kín. Biết chuyện ấy chỉ có tôi, cậu Tuấn lái xe, cô Lan kế toán chi nhánh, và thằng Đông, thợ cũ, làm ở đây ba năm.'),
         (DTV, 'Bà kể lại lúc 22:40.'),
         (None, 'Nghe tiếng xe đỗ ở miệng ngõ, tôi xuống mở then cửa ngách. Ông nhà tôi đi vào ngõ, vừa bước lên bậc thì xe đã chạy đi gửi như mọi khi. Một người mặc áo mưa quân dụng, đội mũ bảo hiểm kín mặt từ trong ngõ lao ra.'),
         (None, 'Hắn bắn hai phát, giật ngay cái cặp da đen trên tay ông nhà tôi rồi chạy vào ngõ. Hắn không nhìn vào tiệm, tủ kính đầy vàng ngay sau lưng tôi hắn không đụng.'),
         (DTV, 'Hắn có nói gì không?'),
         (None, 'Không một câu. Như thể hắn biết trước cái cặp ấy có gì.')),
     'signature': 'Người khai: Trần Thị Hạnh'})

add({'id': 'd06', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của anh Đặng Quốc Tuấn (lái xe của ông Phúc)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 30 ngày 27/8/1998',
     'fields': [{'label': 'Người khai', 'value': 'Đặng Quốc Tuấn, 29 tuổi, lái xe riêng cho ông Phúc ba năm'}],
     'lines': tl('Đặng Quốc Tuấn',
         (DTV, 'Tối 26/8 anh làm gì?'),
         (None, 'Chín rưỡi tôi chở ông chủ lên chi nhánh Hàng Bạc. Ông đếm vàng với cô Lan, tôi ngồi cạnh ông suốt, không rời đi đâu.'),
         (DTV, 'Lúc 22:40 thì sao?'),
         (None, 'Tôi thả ông ở cửa ngách rồi đưa xe đi gửi như mọi lần. Mưa to, sấm nổ liên tục, tôi không nghe gì. Gửi xe xong chạy về thì thấy ông nằm đó.'),
         (DTV, 'Anh có nợ nần ai không?'),
         (None, 'Không. Ông chủ trả lương đủ, tôi không nợ ai.')),
     'signature': 'Người khai: Đặng Quốc Tuấn'})

add({'id': 'd07', 'stage': 1, 'type': 'evidence', 'title': 'Vỏ đạn và đầu đạn thu tại hiện trường',
     'code': 'TV-01', 'image': 'images/d07-vo-dan.webp', 'imageCaption': 'Hai vỏ đạn và hai đầu đạn thu tại hiện trường (thước tỷ lệ cm).',
     'fields': [{'label': 'Loại', 'value': 'Đạn súng ngắn 7,62 × 25 mm (dùng cho súng K54)'},
                {'label': 'Đáy vỏ đạn', 'value': 'Dập số lô sản xuất cũ, năm 1968'}],
     'paragraphs': ['Súng K54 không được bán cho dân thường. Đạn lô cũ thường là vũ khí trôi nổi.',
                    'Đã gửi giám định dấu kim hoả, dấu móc đạn và rãnh xoắn để đối chiếu với các vụ án trước.']})

# ───────────── Vòng 2: tay súng ─────────────
add({'id': 'd08', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của Nguyễn Văn Đông (thợ kim hoàn cũ)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 00 ngày 27/8/1998',
     'fields': [{'label': 'Người khai', 'value': 'Nguyễn Văn Đông, 30 tuổi, thợ kim hoàn tiệm Phúc Hưng 1995–7/1998'}],
     'lines': tl('Nguyễn Văn Đông',
         (DTV, 'Vì sao anh nghỉ việc ở tiệm Phúc Hưng?'),
         (None, 'Tháng Bảy ông Phúc cho tôi nghỉ vì nghi tôi pha tuổi vàng. Tôi oan, tôi có chửi ông ấy mấy câu ngoài phố.'),
         (DTV, 'Anh có biết lịch ông Phúc đi lấy vàng?'),
         (None, 'Tôi không biết ông ấy đi lấy vàng ngày nào. Thợ chỉ ngồi bàn chế tác, chuyện két bạc là việc nhà ông ấy.'),
         (DTV, 'Tối 26/8 anh ở đâu?'),
         (None, 'Tôi trực đêm cho mẹ ở bệnh viện Bạch Mai, mẹ tôi mổ sỏi mật hôm 25.')),
     'signature': 'Người khai: Nguyễn Văn Đông'})

add({'id': 'd09', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của Trần Khắc Hùng (chủ tiệm cầm đồ bến xe Giáp Bát)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '16 giờ 00 ngày 27/8/1998',
     'fields': [{'label': 'Người khai', 'value': 'Trần Khắc Hùng, 45 tuổi, chủ tiệm cầm đồ cạnh bến xe Giáp Bát'}],
     'lines': tl('Trần Khắc Hùng',
         (DTV, 'Anh có mua bán vàng không giấy tờ không?'),
         (None, 'Tôi cầm đồ, mua bán vàng có giấy tờ đàng hoàng, đăng ký kinh doanh treo trên tường.'),
         (DTV, 'Từ 26/8 có ai mang vàng tới bán không?'),
         (None, 'Không. Từ hôm ấy đến giờ tôi không mua lượng vàng nào không giấy tờ, không ai mang vàng Phúc Hưng tới.'),
         (DTV, 'Tối 26/8 anh ở đâu?'),
         (None, 'Tôi đánh tá lả ở tiệm với mấy ông bạn đến gần nửa đêm.')),
     'signature': 'Người khai: Trần Khắc Hùng'})

add({'id': 'd10', 'stage': 2, 'type': 'report', 'title': 'Kết luận giám định đạn đạo',
     'header': ['Phân viện Khoa học hình sự', 'Bộ Công an'], 'heading': 'Kết luận giám định', 'code': '1127/GĐ', 'date': 'Ngày 29/8/1998',
     'sections': [
         {'heading': '1. Đối chiếu', 'paragraphs': ['Dấu kim hoả và dấu móc đạn trên 2 vỏ đạn thu tại phố Chùa Bộc **trùng khớp** với vỏ đạn thu trong vụ cướp tiệm vàng ở thị xã Bắc Giang ngày 14/12/1997.',
                                                     'Hai vụ do **cùng một khẩu súng K54** bắn ra.']},
         {'heading': '2. Vụ Bắc Giang', 'paragraphs': ['Đối tượng bị xác định trong vụ Bắc Giang: **Tạ Văn Cường** ("Cường sẹo"), hiện đang bị truy nã (xem hồ sơ đối tượng).']}],
     'signature': 'Giám định viên: Thượng tá Lê Hữu Nghĩa'})

add({'id': 'd11', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của ông Vũ Văn Bảy (trông nhà gửi xe đầu ngõ)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '10 giờ 00 ngày 28/8/1998',
     'fields': [{'label': 'Người khai', 'value': 'Vũ Văn Bảy, 63 tuổi, trông nhà gửi xe cách tiệm vàng khoảng 150 m'}],
     'lines': tl('Vũ Văn Bảy',
         (DTV, 'Tối 26/8 xe ông Phúc gửi lúc mấy giờ?'),
         (None, 'Sổ tôi ghi 22 giờ 44, xe Toyota đen của ông Phúc, cậu Tuấn lái. Thứ Tư nào cũng vậy.'),
         (DTV, 'Gửi xong cậu Tuấn làm gì?'),
         (None, 'Lạ cái là hôm ấy cậu ấy không chạy về ngay như mọi khi. Cậu đứng dưới mái hiên nhà xe, nhìn đồng hồ, châm điếu thuốc, phải đến 22 giờ 47 mới chạy về phía tiệm.'),
         (DTV, 'Ông có nghe tiếng súng không?'),
         (None, 'Sấm to quá, tôi không phân biệt được.')),
     'signature': 'Người khai: Vũ Văn Bảy'})

add({'id': 'd12', 'stage': 2, 'type': 'report', 'title': 'Biên bản xác minh nơi ở tối 26/8 của Đông và Hùng',
     'header': CA, 'heading': 'Biên bản xác minh', 'code': '88/XM', 'date': 'Ngày 28/8/1998',
     'sections': [
         {'heading': '1. Nguyễn Văn Đông', 'paragraphs': ['Sổ trực khoa Ngoại bệnh viện Bạch Mai ghi người nhà bệnh nhân Nguyễn Thị Mơ là Đông, có mặt từ 19:00 ngày 26/8 đến 6:00 ngày 27/8. Y tá trực xác nhận Đông giúp đẩy giường bệnh nhân lúc khoảng 22:30 và 23:00.']},
         {'heading': '2. Trần Khắc Hùng', 'paragraphs': ['Ba người cùng chơi bài xác nhận Hùng ngồi ở tiệm cầm đồ Giáp Bát từ 20:00 đến gần 24:00. Giáp Bát cách phố Chùa Bộc khoảng 7 km.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd13', 'stage': 2, 'type': 'report', 'title': 'Trích hồ sơ đối tượng truy nã Tạ Văn Cường',
     'header': CA, 'heading': 'Trích hồ sơ đối tượng', 'code': 'TN-97/341', 'date': 'Ngày 29/8/1998',
     'fields': [{'label': 'Họ tên', 'value': 'Tạ Văn Cường ("Cường sẹo"), 34 tuổi'}, {'label': 'Đặc điểm', 'value': 'Sẹo dài ở cằm trái, cao khoảng 1,70 m'}],
     'sections': [
         {'heading': 'Tiền án, truy nã', 'paragraphs': ['Năm 1990: cướp tài sản, 6 năm tù. Tháng 12/1997: nghi phạm vụ cướp tiệm vàng Bắc Giang có dùng súng K54; bị truy nã từ tháng 1/1998.',
                                                        'Theo trinh sát, Cường hay đi một xe máy Simson màu đỏ mận đứng tên người tình; thời gian gần đây làm "đòi nợ thuê" cho một ổ cá độ bóng đá ở Hà Nội mùa World Cup 1998.']},
         {'heading': 'Ghi chú', 'paragraphs': ['Chưa rõ Cường lấy thông tin về tiệm Phúc Hưng từ đâu. Cường không quen ai trong gia đình ông Phúc.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

# ───────────── Vòng 3: người báo tin ─────────────
add({'id': 'd14', 'stage': 3, 'type': 'testimony', 'title': 'Lời khai của chị Phí Thị Lan (kế toán chi nhánh Hàng Bạc)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 00 ngày 30/8/1998',
     'fields': [{'label': 'Người khai', 'value': 'Phí Thị Lan, 33 tuổi, kế toán chi nhánh tiệm Phúc Hưng ở phố Hàng Bạc'}],
     'lines': tl('Phí Thị Lan',
         (DTV, 'Tối 26/8 ở chi nhánh có những ai?'),
         (None, 'Ông Phúc, tôi và cậu Tuấn. Ông với tôi đếm vàng từ chín rưỡi, cho vào cặp da đen sáu mươi lượng.'),
         (DTV, 'Cậu Tuấn ngồi đâu?'),
         (None, 'Mười giờ mười lăm cậu ấy nói ra đầu phố mua bao thuốc lá. Mười phút sau mới vào, bảo hết Vinataba phải đi xa. Lúc đó ông Phúc vừa khoá cặp.'),
         (DTV, 'Mấy giờ hai người về?'),
         (None, 'Mười giờ hai lăm. Ông Phúc gọi về nhà dặn bà Hạnh: "Khoảng mười một giờ kém hai mươi tôi về đến, mở cửa ngách."')),
     'signature': 'Người khai: Phí Thị Lan'})

add({'id': 'd15', 'stage': 3, 'type': 'report', 'title': 'Trích sổ tổng đài dịch vụ nhắn tin đêm 26/8/1998',
     'header': ['Công ty dịch vụ nhắn tin (bưu điện Hà Nội)', 'Tổng đài trung tâm'], 'heading': 'Trích sổ tổng đài', 'code': '17/NT', 'date': 'Ngày 30/8/1998',
     'sections': [
         {'heading': '1. Cuộc gọi', 'paragraphs': ['22:16, số gọi đến: **bốt điện thoại thẻ ở đầu phố Hàng Bạc**. Người gọi (giọng nam) nhờ nhắn vào máy nhắn tin số 107-5523.',
                                                    'Nội dung tổng đài viên nhập: **"22H40 CAP DEN CUA NGACH"**.']},
         {'heading': '2. Thuê bao 107-5523', 'paragraphs': ['Đăng ký ngày 2/8/1998, tên "Nguyễn Văn Ba", số chứng minh không có thật. Nhân viên đăng ký nhận diện ảnh: người đến làm thủ tục có **sẹo dài ở cằm trái**.']}],
     'signature': 'Trưởng tổng đài: Đỗ Thị Hoà'})

add({'id': 'd16', 'stage': 3, 'type': 'report', 'title': 'Xác minh của bưu điện về bốt điện thoại thẻ phố Hàng Bạc',
     'header': ['Bưu điện thành phố Hà Nội', 'Trung tâm điện thoại công cộng'], 'heading': 'Văn bản xác minh', 'code': '231/ĐT', 'date': 'Ngày 31/8/1998',
     'sections': [
         {'heading': 'Kết quả', 'paragraphs': ['Bốt điện thoại thẻ số HB-04 (đầu phố Hàng Bạc) ghi nhận cuộc gọi 22:15:52 đến tổng đài nhắn tin, dài 1 phút 40 giây.',
                                                'Thẻ sử dụng: thẻ 30 đơn vị, **số sê-ri 0812774**. Trước đó, cùng thẻ này đã gọi tới tổng đài nhắn tin vào các ngày 5/8, 12/8, 19/8 (đều là thứ Tư), khoảng 22 giờ.']}],
     'signature': 'Giám đốc trung tâm: Trịnh Văn Hải'})

add({'id': 'd17', 'stage': 3, 'type': 'testimony', 'title': 'Biên bản ghi lời khai lần hai của anh Đặng Quốc Tuấn',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '15 giờ 00 ngày 31/8/1998',
     'fields': [{'label': 'Người khai', 'value': 'Đặng Quốc Tuấn, 29 tuổi'}],
     'lines': tl('Đặng Quốc Tuấn',
         (DTV, 'Chị Lan nói 22:15 anh rời chi nhánh mười phút.'),
         (None, 'À, tôi ra mua bao thuốc lá, quên không kể. Có mười phút thôi.'),
         (DTV, 'Anh có gọi điện cho ai không?'),
         (None, 'Không. Tôi mua bao thuốc rồi quay lại, không gọi điện cho ai.'),
         (DTV, 'Anh có biết ai tên Cường sẹo?'),
         (None, 'Tôi không quen ai như thế.')),
     'signature': 'Người khai: Đặng Quốc Tuấn'})

add({'id': 'd18', 'stage': 3, 'type': 'testimony', 'title': 'Lời khai của bà Nguyễn Thị Vân (bán nước chè cạnh bốt điện thoại Hàng Bạc)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 00 ngày 1/9/1998',
     'fields': [{'label': 'Người khai', 'value': 'Nguyễn Thị Vân, 60 tuổi, bán nước chè, thuốc lá cạnh bốt điện thoại đầu phố Hàng Bạc'}],
     'lines': tl('Nguyễn Thị Vân',
         (DTV, 'Tối thứ Tư 26/8 bà có thấy ai gọi điện ở bốt không?'),
         (None, 'Có cậu lái xe ô tô đen hay đỗ ở cửa tiệm vàng trong phố. Mười giờ hơn, cậu ấy vào bốt, đọc chậm từng chữ như đọc cho ai chép.'),
         (DTV, 'Bà nghe được gì?'),
         (None, 'Tôi nghe được "cửa ngách". Gọi xong cậu ấy mua của tôi bao Vinataba. Thứ Tư nào cậu ấy cũng gọi vào giờ ấy, tháng này rồi.')),
     'signature': 'Người khai: Nguyễn Thị Vân'})

# ───────────── Vòng 4: nợ World Cup ─────────────
add({'id': 'd19', 'stage': 4, 'type': 'note', 'title': 'Trích sổ ghi nợ thu giữ ở ổ cá độ bóng đá phố Khâm Thiên',
     'paragraphs': ['Sổ ghi tay, thu giữ ngày 1/9/1998 khi triệt phá ổ cá độ World Cup 1998:',
                    '— Pháp – Brazil (12/7): Tuấn "lái xe" thua 22 tr.',
                    '— Cộng dồn nợ của Tuấn "lái xe" đến 20/7: **60 tr**. Hạn trả 15/8. Giao "C. sẹo" đòi.',
                    '__— 20/8: Tuấn "lái xe" – xoá nợ. Ghi chú: "C. sẹo nhận trừ, việc thứ Tư".__'],
     'signature': 'Sổ của chủ ổ cá độ'})

add({'id': 'd20', 'stage': 4, 'type': 'report', 'title': 'Biên bản khám xét tiệm cầm đồ của Trần Khắc Hùng',
     'header': CA, 'heading': 'Biên bản khám xét', 'code': '41/KX', 'date': 'Ngày 1/9/1998',
     'sections': [
         {'heading': 'Thu giữ', 'paragraphs': ['Trong két: 20 lượng vàng đã nung chảy thành thỏi thô, chưa dập dấu.',
                                                'Sổ mua bán (chữ Hùng): "28/8 – mua 20 lượng vàng nung của anh Sẹo, 70 tr, không giấy."']},
         {'heading': 'Ghi nhận', 'paragraphs': ['Giám định thành phần cho thấy vàng 9999, phù hợp với loại vàng miếng tiệm Phúc Hưng nhập về chi nhánh tháng 8.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd21', 'stage': 4, 'type': 'report', 'title': 'Biên bản xác minh chi tiêu của Đặng Quốc Tuấn sau ngày 26/8',
     'header': CA, 'heading': 'Biên bản xác minh', 'code': '93/XM', 'date': 'Ngày 2/9/1998',
     'sections': [
         {'heading': 'Kết quả', 'paragraphs': ['Ngày 30/8: Tuấn mua một xe máy Honda Dream II tại cửa hàng phố Bà Triệu, trả **25 triệu đồng tiền mặt**.',
                                                'Lương lái xe của Tuấn là 900.000 đồng/tháng. Gia đình Tuấn ở Hà Đông không có thu nhập lớn.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd22', 'stage': 4, 'type': 'testimony', 'title': 'Lời khai của chủ quán bia hơi ngõ chợ Khâm Thiên',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 00 ngày 2/9/1998',
     'fields': [{'label': 'Người khai', 'value': 'Lê Văn Toàn, 47 tuổi, chủ quán bia hơi'}],
     'lines': tl('Lê Văn Toàn',
         (DTV, 'Ông có nhận ra hai người trong ảnh không?'),
         (None, 'Thằng có sẹo ở cằm là khách quen, đi con Simson đỏ. Còn cậu kia là lái xe, hay đỗ ô tô đen ngoài đầu ngõ.'),
         (DTV, 'Họ ngồi với nhau lúc nào?'),
         (None, 'Mấy tối tháng Tám, xem bóng đá xong. Hôm hai mươi, cậu lái xe vẽ cái gì lên vỏ bao thuốc, đưa thằng sẹo xem, thằng sẹo gật gù rồi đốt luôn.')),
     'signature': 'Người khai: Lê Văn Toàn'})

# ───────────── Vòng 5: vây bắt ─────────────
add({'id': 'd23', 'stage': 5, 'type': 'report', 'title': 'Biên bản bắt và khám xét Tạ Văn Cường tại nhà trọ bãi sông Hồng',
     'header': CA, 'heading': 'Biên bản bắt người bị truy nã', 'code': '12/BTN', 'date': '04 giờ 30 ngày 3/9/1998',
     'sections': [
         {'heading': 'Thu giữ', 'paragraphs': ['— Một súng ngắn K54 và 5 viên đạn lô 1968.',
                                                '— Một áo mưa quân dụng màu xanh, một mũ bảo hiểm kín mặt, một xe Simson màu đỏ mận.',
                                                '— 30 lượng vàng nung thỏi, một cặp da đen bị rạch khoá.',
                                                '— Một máy nhắn tin số 107-5523; tin cuối còn lưu: "22H40 CAP DEN CUA NGACH".']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd24', 'stage': 5, 'type': 'report', 'title': 'Biên bản khám xét chỗ ở của Đặng Quốc Tuấn',
     'header': CA, 'heading': 'Biên bản khám xét', 'code': '47/KX', 'date': '05 giờ 00 ngày 3/9/1998',
     'sections': [
         {'heading': 'Thu giữ', 'paragraphs': ['— Trong ví: một thẻ điện thoại 30 đơn vị đã gần hết, **số sê-ri 0812774**.',
                                                '— Trong hộc ô tô: một mẩu giấy ghi "107-5523".',
                                                '— Trong tủ: 8 triệu đồng tiền mặt, hoá đơn mua xe Dream II ngày 30/8.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd25', 'stage': 5, 'type': 'report', 'title': 'Kết luận giám định tổng hợp',
     'header': ['Phân viện Khoa học hình sự', 'Bộ Công an'], 'heading': 'Kết luận giám định', 'code': '1188/GĐ', 'date': 'Ngày 5/9/1998',
     'sections': [
         {'heading': '1. Súng', 'paragraphs': ['Khẩu K54 thu của Tạ Văn Cường là khẩu súng đã bắn 2 vỏ đạn ở phố Chùa Bộc và vụ Bắc Giang.']},
         {'heading': '2. Thẻ điện thoại', 'paragraphs': ['Vân tay trên thẻ sê-ri 0812774 là của Đặng Quốc Tuấn. Chữ viết "107-5523" trên mẩu giấy trùng chữ Tuấn.']},
         {'heading': '3. Xe', 'paragraphs': ['Hoa văn lốp xe Simson của Cường trùng vệt lốp trong ngõ bên hông tiệm Phúc Hưng.']}],
     'signature': 'Giám định viên: Thượng tá Lê Hữu Nghĩa'})

CARDS = ['cuong', 'dong', 'tuan', 'hung']
NAMES = ['Tạ Văn Cường', 'Nguyễn Văn Đông', 'Đặng Quốc Tuấn', 'Trần Khắc Hùng']
Q = [
    {'id': 'q1', 'stage': 1, 'type': 'choice', 'title': 'Cướp ngẫu nhiên hay biết trước?',
     'prompt': 'Báo chí gọi đây là một vụ cướp giữa đêm mưa. Theo hồ sơ đang mở, nhận định nào đứng vững?',
     'options': ['Một kẻ cướp liều lĩnh lảng vảng quanh các tiệm vàng, tình cờ gặp ông Phúc mở cửa, bắn hoảng rồi giật được chiếc cặp.',
                 'Kẻ cướp đã biết trước giờ, cửa và chiếc cặp: hắn chờ ở ngõ bên hông đúng tối thứ Tư, chỉ lấy chiếc cặp và bỏ qua tủ kính đầy vàng.',
                 'Kẻ cướp nhắm vào tủ kính trong tiệm, nhưng bị ông Phúc phát hiện ở cửa ngách nên bắn rồi bỏ chạy, tiện tay giật chiếc cặp.'],
     'answer': [1],
     'nudges': {'0': {'message': 'Cửa ngách mở vào hôm nào? Kẻ cướp lấy gì, bỏ qua gì?'},
                '2': {'message': 'Bà Hạnh nói hắn không nhìn vào tiệm. Tủ kính có bị đụng tới không?'}},
     'hints': ['Đọc biên bản khám nghiệm và lời bà Hạnh.', 'Cửa ngách mở khi nào? Hắn lấy gì?',
               'd02: cửa ngách chỉ mở tối thứ Tư, tủ kính nguyên vẹn. d05: hắn chờ trong ngõ, giật ngay chiếc cặp, không nhìn vào tiệm.'],
     'solved': 'Kẻ cướp biết trước. Có người đã cho hắn biết giờ, cửa và chiếc cặp.',
     'explanation': [{'title': 'Cửa ngách', 'body': ['d02: chỉ mở tối thứ Tư. d05: ông Phúc mang vàng từ Hàng Bạc về cất két nhà.']},
                     {'title': 'Chiếc cặp', 'body': ['d05: hắn giật ngay cặp da đen, không nói một câu.']},
                     {'title': 'Tủ kính', 'body': ['d02, d05: tủ kính đầy vàng ngay sau lưng bà Hạnh không bị đụng tới.']}]},
    {'id': 'q2', 'stage': 1, 'type': 'choice', 'multiple': True, 'cards': CARDS, 'title': 'Ai biết lịch tối thứ Tư?',
     'prompt': 'Chọn **tất cả** những người trong danh sách được hồ sơ cho thấy biết chuyện ông Phúc mang vàng về qua cửa ngách tối thứ Tư.',
     'options': NAMES, 'answer': [1, 2],
     'nudges': {'0': {'message': 'Ở vòng này chưa có tài liệu nào nói Cường biết gì về gia đình ông Phúc.'},
                '3': {'message': 'Có tài liệu nào ở vòng này nói chủ tiệm cầm đồ biết lịch của ông Phúc không?'}},
     'hints': ['Bà Hạnh kể những ai biết.', 'Trong danh sách thẻ, ai có tên trong lời bà Hạnh?',
               'd05 dòng 2: biết lịch có bà Hạnh, cậu Tuấn lái xe, cô Lan kế toán và Đông thợ cũ.'],
     'solved': 'Trong bốn người bị nghi, hai người biết lịch: anh Tuấn và anh Đông.',
     'explanation': [{'title': 'Tuấn', 'body': ['d05, d06: lái xe chở ông Phúc mỗi tối thứ Tư.']},
                     {'title': 'Đông', 'body': ['d05: làm ở tiệm ba năm, biết lịch; bị cho nghỉ tháng 7.']},
                     {'title': 'Chưa đủ', 'body': ['Biết lịch chưa phải là cầm súng. Ai là người bóp cò?']}]},
    {'id': 'q3', 'stage': 2, 'type': 'line', 'title': 'Người thợ cũ',
     'prompt': 'Một người mới được hỏi chối biết chuyện mà tài liệu ở vòng trước khẳng định. Chỉ ra dòng khai đó.',
     'answer': ['d08:004'],
     'nudges': {'d08:006': {'message': 'Câu về bệnh viện Bạch Mai cần kiểm tra bằng giấy tờ khác. Tìm câu bị lời bà Hạnh bác.'}},
     'hints': ['Bà Hạnh nói ai biết lịch?', 'Đông nói gì về lịch lấy vàng?', 'd08 dòng 4: không biết ông Phúc lấy vàng ngày nào. d05 dòng 2: Đông làm ba năm, biết chuyện thứ Tư.'],
     'solved': 'Đông nói dối là không biết lịch. Nhưng tối hôm ấy anh ở đâu?',
     'explanation': [{'title': 'Câu khai', 'body': ['d08 dòng 4: không biết ông Phúc đi lấy vàng ngày nào.']},
                     {'title': 'Bị bác', 'body': ['d05 dòng 2: bà Hạnh kể Đông là một trong bốn người biết.']},
                     {'title': 'Còn phải xét', 'body': ['d08 dòng 6: Đông nói trực đêm cho mẹ ở Bạch Mai.']}]},
    {'id': 'q4', 'stage': 2, 'type': 'evidence', 'need': 2, 'title': 'Khẩu K54 từ Bắc Giang',
     'prompt': 'Ghim 2 tài liệu cho thấy ai là người cầm súng đêm 26/8.',
     'answer': ['d10', 'd13'],
     'nudges': [{'any': ['d07'], 'near': True, 'message': 'Vỏ đạn cho biết loại súng. Cần kết quả đối chiếu và hồ sơ người dùng khẩu súng đó.'}],
     'hints': ['Một kết luận giám định, một hồ sơ đối tượng.', 'Vỏ đạn khớp với vụ án nào? Ai là nghi phạm vụ đó?',
               'd10: cùng một khẩu K54 với vụ Bắc Giang 12/1997, nghi phạm Tạ Văn Cường. d13: Cường truy nã, sẹo cằm, Simson đỏ, đòi nợ cá độ.'],
     'solved': 'Tay súng là Cường sẹo. Nhưng hồ sơ ghi rõ: Cường không quen ai trong nhà ông Phúc.',
     'explanation': [{'title': 'Đạn đạo', 'body': ['d10: dấu kim hoả, móc đạn trùng vụ Bắc Giang; cùng một khẩu K54.']},
                     {'title': 'Đối tượng', 'body': ['d13: Tạ Văn Cường, truy nã vì vụ Bắc Giang; đi Simson đỏ; đòi nợ cho ổ cá độ.']},
                     {'title': 'Câu hỏi', 'body': ['d13: Cường không quen ai trong gia đình ông Phúc. Ai đã báo tin?']}]},
    {'id': 'q5', 'stage': 2, 'type': 'choice', 'multiple': True, 'cards': CARDS, 'title': 'Ai không thể cầm súng?',
     'prompt': 'Chọn **tất cả** những người mà hồ sơ đang mở cho thấy không thể là người nổ súng ở cửa ngách lúc 22:40.',
     'options': NAMES, 'answer': [1, 2, 3],
     'nudges': {'0': {'message': 'Khẩu súng nổ ở phố Chùa Bộc là khẩu của vụ Bắc Giang (d10).'}},
     'hints': ['Đọc biên bản xác minh, lời bà Hạnh và lời ông trông xe.', 'Lúc súng nổ, chiếc xe ở đâu? Đông và Hùng ở đâu?',
               'd12: Đông ở Bạch Mai, Hùng ở Giáp Bát. d05: xe đã chạy đi gửi khi tay súng lao ra; d11: Tuấn gửi xe 22:44 ở nhà xe 150 m.'],
     'solved': 'Ba người đều không cầm súng. Nhưng không cầm súng chưa có nghĩa là vô can.',
     'explanation': [{'title': 'Đông, Hùng', 'body': ['d12: Đông ở bệnh viện Bạch Mai, Hùng ở tiệm cầm đồ Giáp Bát, đều có người xác nhận.']},
                     {'title': 'Tuấn', 'body': ['d05: xe chạy đi trước khi tay súng lao ra; d11: Tuấn gửi xe lúc 22:44.']},
                     {'title': 'Nhưng', 'body': ['d11: Tuấn đứng dưới mái hiên nhìn đồng hồ, 22:47 mới chạy về.']}]},
    {'id': 'q6', 'stage': 3, 'type': 'line', 'title': 'Mười phút ở Hàng Bạc',
     'prompt': 'Chỉ ra dòng khai bị lời chị kế toán chi nhánh bác bỏ.',
     'answer': ['d06:002'],
     'nudges': {'d06:004': {'near': True, 'message': 'Câu về lúc 22:40 bị ông trông xe làm lung lay, nhưng chị Lan nói về chuyện ở Hàng Bạc.'}},
     'hints': ['Chị Lan nói gì về lúc 22:15?', 'Ai khai ngồi cạnh ông Phúc suốt?', 'd06 dòng 2: ngồi cạnh ông suốt, không rời đi đâu. d14: 22:15 Tuấn ra ngoài mười phút "mua thuốc lá".'],
     'solved': 'Tuấn đã rời chi nhánh đúng lúc ông Phúc khoá chiếc cặp.',
     'explanation': [{'title': 'Câu khai', 'body': ['d06 dòng 2: ngồi cạnh ông chủ suốt, không rời đi đâu.']},
                     {'title': 'Bị bác', 'body': ['d14: 22:15 Tuấn ra đầu phố mười phút, lúc ông Phúc vừa khoá cặp.']},
                     {'title': 'Giờ về', 'body': ['d14: ông Phúc gọi về dặn "khoảng mười một giờ kém hai mươi" mở cửa ngách.']}]},
    {'id': 'q7', 'stage': 3, 'type': 'evidence', 'need': 2, 'title': 'Tin nhắn lúc 22:16',
     'prompt': 'Ghim 2 tài liệu cho thấy tay súng nhận được tin báo giờ, cửa và chiếc cặp từ đâu.',
     'answer': ['d15', 'd16'],
     'nudges': [{'any': ['d18'], 'near': True, 'message': 'Bà bán chè thấy ai gọi. Cần giấy tờ của tổng đài và bưu điện.'}],
     'hints': ['Một sổ tổng đài nhắn tin, một văn bản bưu điện.', 'Tin nhắn nội dung gì, gửi tới máy của ai, từ bốt nào, bằng thẻ nào?',
               'd15: 22:16 từ bốt thẻ đầu phố Hàng Bạc, "22H40 CAP DEN CUA NGACH", máy nhắn tin do người có sẹo cằm đăng ký. d16: thẻ sê-ri 0812774, đã gọi tổng đài nhắn tin các tối thứ Tư 5/8, 12/8, 19/8.'],
     'solved': 'Từ Hàng Bạc, có người nhắn cho Cường giờ ông Phúc về. Người đó đã nhắn như thế suốt ba tối thứ Tư trước.',
     'explanation': [{'title': 'Tin nhắn', 'body': ['d15: 22:16 "22H40 CAP DEN CUA NGACH" vào máy nhắn tin của người có sẹo cằm.']},
                     {'title': 'Bốt và thẻ', 'body': ['d16: bốt thẻ đầu phố Hàng Bạc, thẻ sê-ri 0812774; cùng thẻ gọi tổng đài nhắn tin ba tối thứ Tư trước.']},
                     {'title': 'Ai ở đó', 'body': ['d14: 22:15 Tuấn ra đầu phố Hàng Bạc mười phút.']}]},
    {'id': 'q8', 'stage': 3, 'type': 'line', 'title': 'Bao Vinataba',
     'prompt': 'Chỉ ra dòng khai bị lời bà bán nước chè bác bỏ.',
     'answer': ['d17:004'],
     'nudges': {'d17:002': {'near': True, 'message': 'Câu này Tuấn đã nhận có ra ngoài. Tìm câu về cuộc gọi.'}},
     'hints': ['Bà Vân thấy cậu lái xe làm gì trong bốt?', 'Tuấn nói gì về việc gọi điện?', 'd17 dòng 4: không gọi điện cho ai. d18: cậu lái xe ô tô đen vào bốt, đọc chậm từng chữ, có chữ "cửa ngách", rồi mua bao Vinataba.'],
     'solved': 'Người đọc tin nhắn ở bốt Hàng Bạc là Tuấn.',
     'explanation': [{'title': 'Câu khai', 'body': ['d17 dòng 4: chỉ mua bao thuốc, không gọi điện cho ai.']},
                     {'title': 'Bị bác', 'body': ['d18: cậu lái xe ô tô đen đọc chậm từng chữ trong bốt, bà nghe được "cửa ngách", rồi mua bao Vinataba.']},
                     {'title': 'Lặp lại', 'body': ['d18: thứ Tư nào cũng gọi vào giờ ấy; d16: thẻ đã gọi ba tối thứ Tư trước.']}]},
    {'id': 'q9', 'stage': 4, 'type': 'line', 'title': 'Vàng nung',
     'prompt': 'Chỉ ra dòng khai bị biên bản khám xét tiệm cầm đồ bác bỏ.',
     'answer': ['d09:004'],
     'nudges': {'d09:002': {'near': True, 'message': 'Câu về giấy phép kinh doanh chưa bị bác thẳng. Tìm câu về vàng mua sau 26/8.'}},
     'hints': ['Trong két tiệm cầm đồ có gì?', 'Hùng nói gì về vàng mua sau 26/8?', 'd09 dòng 4: không mua lượng vàng nào không giấy tờ. d20: 28/8 mua 20 lượng vàng nung của "anh Sẹo", không giấy.'],
     'solved': 'Hùng không cầm súng, nhưng đã tiêu thụ một phần số vàng cho Cường.',
     'explanation': [{'title': 'Câu khai', 'body': ['d09 dòng 4: không mua vàng không giấy tờ, không ai mang vàng Phúc Hưng tới.']},
                     {'title': 'Bị bác', 'body': ['d20: két có 20 lượng vàng nung; sổ ghi "28/8 – mua của anh Sẹo, 70 tr, không giấy".']},
                     {'title': 'Vai trò', 'body': ['d12: tối 26/8 Hùng ở Giáp Bát. Hùng là người mua lại, không phải người gây án.']}]},
    {'id': 'q10', 'stage': 4, 'type': 'evidence', 'need': 2, 'title': 'Sáu mươi triệu nợ bóng đá',
     'prompt': 'Ghim 2 tài liệu cho thấy vì sao người lái xe ba năm của ông Phúc lại báo tin cho tay súng.',
     'answer': ['d19', 'd21'],
     'nudges': [{'any': ['d22'], 'near': True, 'message': 'Chủ quán bia cho thấy hai người quen nhau. Cần tài liệu về nợ và về tiền sau vụ án.'}],
     'hints': ['Một sổ ghi nợ, một biên bản về chi tiêu.', 'Tuấn nợ ai bao nhiêu? Món nợ ấy được xoá thế nào? Sau vụ án Tuấn tiêu gì?',
               'd19: Tuấn nợ cá độ World Cup 60 tr, giao Cường sẹo đòi; 20/8 xoá nợ "việc thứ Tư". d21: 30/8 mua Dream II 25 tr tiền mặt, lương 900 nghìn.'],
     'solved': 'Tuấn trả món nợ World Cup bằng lịch tối thứ Tư của ông chủ.',
     'explanation': [{'title': 'Nợ', 'body': ['d19: nợ cá độ 60 tr, Cường sẹo được giao đi đòi.']},
                     {'title': 'Xoá nợ', 'body': ['d19: 20/8 xoá nợ, ghi chú "C. sẹo nhận trừ, việc thứ Tư".']},
                     {'title': 'Tiền', 'body': ['d21: 30/8 mua Dream II 25 tr tiền mặt, trong khi lương 900 nghìn/tháng.']}]},
    {'id': 'q-accuse', 'stage': 5, 'type': 'choice', 'multiple': True, 'cards': CARDS, 'title': 'Chỉ mặt hung thủ và đồng phạm',
     'prompt': 'Cái chết của ông Phúc là việc của hơn một người. Chọn **đúng hai** người đã cùng chuẩn bị và thực hiện vụ cướp.',
     'options': NAMES, 'answer': [0, 2],
     'nudges': {'1': {'message': 'Đông nói dối chuyện biết lịch, nhưng ở Bạch Mai suốt đêm (d12).'},
                '3': {'message': 'Hùng chỉ mua lại vàng nung hai ngày sau (d20); tối 26/8 ở Giáp Bát (d12).'}},
     'hints': ['Một người cầm súng. Một người báo tin giờ, cửa, chiếc cặp.', 'Thẻ điện thoại sê-ri 0812774 ở trong ví ai?',
               'Cường: súng, áo mưa, Simson, máy nhắn tin còn tin cuối (d23, d25). Tuấn: thẻ điện thoại, mẩu giấy số máy nhắn tin, vân tay (d24, d25).'],
     'solved': 'Tạ Văn Cường và Đặng Quốc Tuấn.',
     'explanation': [{'title': 'Cường', 'body': ['Khẩu K54 (d10, d25), áo mưa quân dụng, Simson đỏ, máy nhắn tin còn tin "22H40 CAP DEN CUA NGACH" (d23).']},
                     {'title': 'Tuấn', 'body': ['Rời chi nhánh 22:15 (d14), gọi từ bốt Hàng Bạc (d15, d16, d18), thẻ sê-ri 0812774 có vân tay và mẩu giấy số máy nhắn tin (d24, d25).']},
                     {'title': 'Vì sao', 'body': ['Nợ cá độ 60 tr do Cường đòi, xoá nợ "việc thứ Tư" (d19); mua xe 25 tr tiền mặt (d21).']}]},
    {'id': 'q11', 'stage': 5, 'type': 'choice', 'title': 'Kết luận điều tra',
     'prompt': 'Chọn bản kết luận đúng với hồ sơ ở mọi chi tiết: ai, bằng cách nào, và vì sao.',
     'options': [
         'Tuấn nợ cá độ World Cup 60 triệu, được Cường sẹo xoá nợ để đổi lấy lịch tối thứ Tư của ông Phúc. Tối 26/8, khi ông Phúc khoá cặp vàng ở Hàng Bạc, Tuấn ra bốt điện thoại thẻ nhắn vào máy nhắn tin của Cường "22H40 CAP DEN CUA NGACH". Cường mặc áo mưa quân dụng chờ trong ngõ, bắn ông Phúc bằng khẩu K54 của vụ Bắc Giang, giật cặp, chạy xe Simson; Tuấn đưa xe đi gửi để có mặt ở nơi khác lúc súng nổ.',
         'Đông bị đuổi việc vì nghi pha tuổi vàng nên thù ông Phúc, bán lịch tối thứ Tư cho Cường sẹo qua một người quen ở quán bia hơi; tối 26/8 Đông nhờ người gọi điện báo giờ từ Hàng Bạc trong khi mình trực ở bệnh viện để có ngoại phạm, còn Tuấn chỉ là lái xe tình cờ đưa xe đi gửi đúng lúc, và chiếc xe Dream mua bằng tiền vay của gia đình ở Hà Đông.',
         'Hùng đặt hàng vàng với Cường sẹo, cử người theo dõi tiệm Phúc Hưng nhiều tuần để nắm lịch tối thứ Tư, rồi cho Cường mượn khẩu K54 và tiền thuê máy nhắn tin; sau vụ cướp Hùng nhận nung chảy vàng, chia cho Cường một nửa, còn Tuấn mua xe bằng tiền thưởng cuối năm và chỉ tình cờ quen Cường ở quán bia hơi xem bóng đá.',
         'Cường sẹo tự theo dõi tiệm nhiều tuần, đoán được lịch tối thứ Tư, nằm chờ trong ngõ suốt mấy tiếng giữa mưa, bắn ông Phúc rồi giật cặp; tin nhắn trong máy nhắn tin là của ổ cá độ gửi Cường đòi nợ một người khác, còn Tuấn chỉ nói dối chuyện ra ngoài vì sợ lộ việc đánh bóng đá, và tấm thẻ điện thoại trong ví là do nhặt được.'],
     'answer': [0],
     'exam': {'examiner': 'Kiểm sát viên Phạm Thị Thu Hà',
              'intro': 'Trình bày kết luận trước kiểm sát viên: trả lời lần lượt từng câu hỏi bằng lời của mình. Không dùng được AI thì bấm “Trả lời bằng trắc nghiệm” để chọn bản kết luận đúng.'},
     'nudges': {'1': {'message': 'Người đọc tin nhắn ở bốt là cậu lái xe ô tô đen (d18), thẻ trong ví Tuấn (d24).'},
                '2': {'message': 'Hùng ở Giáp Bát tối 26/8 (d12) và chỉ mua lại vàng nung hai ngày sau (d20).'},
                '3': {'message': 'Tin nhắn ghi đúng "CUA NGACH" và gửi từ thẻ trong ví Tuấn (d15, d16, d24).'}},
     'hints': ['Đối chiếu: ai gửi tin nhắn (d15, d16, d18, d24), ai cầm súng (d10, d23).', 'Chỉ một phương án có tin nhắn 22:16, thẻ điện thoại và nợ World Cup.', 'Phương án A.'],
     'solved': 'Hồ sơ khép lại với tên Tạ Văn Cường và Đặng Quốc Tuấn.',
     'explanation': [{'title': 'Báo tin', 'body': ['d14, d15, d16, d18, d24: 22:15 Tuấn ra bốt Hàng Bạc, nhắn "22H40 CAP DEN CUA NGACH" bằng thẻ sê-ri 0812774.']},
                     {'title': 'Nổ súng', 'body': ['d10, d23, d25: Cường dùng khẩu K54 của vụ Bắc Giang, áo mưa quân dụng, Simson đỏ.']},
                     {'title': 'Vì sao', 'body': ['d19, d21: nợ cá độ 60 tr xoá vì "việc thứ Tư"; mua xe 25 tr tiền mặt.']}]},
]

case = {
    'id': CID, 'no': 15, 'status': 'available',
    'title': 'Chiếc cặp da đêm thứ Tư',
    'subtitle': 'Một đêm mưa giông, hai tiếng súng và người duy nhất biết giờ ông chủ về',
    'tagline': 'Giữa đêm mưa giông, chủ tiệm vàng bị bắn ngay cửa ngách nhà mình. Kẻ cướp chỉ lấy đúng một chiếc cặp da.',
    'difficulty': 4, 'players': '2–6', 'duration': '90–120 phút',
    'setting': 'Tiệm vàng Phúc Hưng (hư cấu), phố Chùa Bộc, Đống Đa, Hà Nội', 'era': 'Tháng 8/1998',
    'tags': ['Án mạng', 'Cướp có vũ trang', 'Hà Nội 1998', 'Có đồng phạm'], 'cover': 'images/cover.webp',
    'contentWarning': 'Hồ sơ có mô tả một vụ nổ súng cướp tài sản. Tiệm vàng, nhân vật và sự việc đều hư cấu.',
    'synopsis': ['Đêm thứ Tư 26/8/1998, giữa cơn mưa giông, ông Lương Văn Phúc, chủ tiệm vàng Phúc Hưng trên phố Chùa Bộc, bị bắn ngay bậc cửa ngách nhà mình.',
                 'Kẻ cướp không đụng tới tủ kính đầy vàng. Hắn chỉ giật đúng chiếc cặp da đen ông Phúc vừa mang về.'],
    'intro': {'title': 'Chiếc cặp da đêm thứ Tư',
              'paragraphs': ['Đêm thứ Tư 26/8/1998, Hà Nội mưa giông suốt từ chiều. Khoảng 22 giờ 40, chiếc Toyota đen dừng trước cửa ngách tiệm vàng Phúc Hưng trên phố Chùa Bộc. Ông chủ Lương Văn Phúc bước xuống, tay xách một chiếc cặp da đen.',
                             'Một người mặc áo mưa quân dụng từ trong ngõ lao ra. Hai tiếng súng lẫn trong tiếng sấm. Ông Phúc gục xuống, chiếc cặp biến mất cùng tiếng xe máy.',
                             'Bạn là điều tra viên Phòng Cảnh sát hình sự Công an thành phố Hà Nội. Tay súng không nói một câu nào, như thể đã biết trước tất cả. Hãy bắt đầu từ câu hỏi: ai đã cho hắn biết?'],
              'objective': 'Tìm ra ai cầm súng, ai đã báo tin giờ về, cửa ngách và chiếc cặp, và vì sao.'},
    'victim': {'id': 'phuc', 'name': 'Lương Văn Phúc', 'age': 58, 'role': 'Chủ tiệm vàng Phúc Hưng', 'image': 'images/id-phuc.webp',
               'note': 'Bị bắn chết trước cửa ngách nhà mình khoảng 22:40 đêm 26/8/1998; mất chiếc cặp đựng khoảng 60 lượng vàng.'},
    'suspects': [
        {'id': 'cuong', 'name': 'Tạ Văn Cường ("Cường sẹo")', 'age': 34, 'role': 'Đối tượng bị truy nã', 'image': 'images/id-cuong.webp', 'voice': 'M3',
         'suspicion': 'Có tiền án cướp tài sản, đang bị truy nã vì một vụ cướp tiệm vàng có súng ở Bắc Giang.'},
        {'id': 'dong', 'name': 'Nguyễn Văn Đông', 'age': 30, 'role': 'Thợ kim hoàn cũ của tiệm', 'image': 'images/id-dong.webp', 'voice': 'M1',
         'suspicion': 'Bị ông Phúc cho nghỉ tháng 7 vì nghi pha tuổi vàng; từng chửi ông Phúc ngoài phố.'},
        {'id': 'tuan', 'name': 'Đặng Quốc Tuấn', 'age': 29, 'role': 'Lái xe riêng của ông Phúc', 'image': 'images/id-tuan.webp', 'voice': 'M2',
         'suspicion': 'Người chở ông Phúc về đến cửa ngách, rồi đưa xe đi gửi đúng lúc súng nổ.'},
        {'id': 'hung', 'name': 'Trần Khắc Hùng', 'age': 45, 'role': 'Chủ tiệm cầm đồ bến xe Giáp Bát', 'image': 'images/id-hung.webp', 'voice': 'M4',
         'suspicion': 'Bị nghi chuyên tiêu thụ vàng không giấy tờ cho các nhóm trộm cướp.'}],
    'aiInterrogation': True,
    'audio': {'intro': 'audio/intro.mp3', 'finale': 'audio/finale.mp3'},
    'documents': D,
    'questions': Q,
    'beats': [
        {'stage': 2, 'kicker': 'Ngày 27–29/8/1998 · Hà Nội', 'title': 'Khẩu súng có lý lịch', 'voice': 'audio/beat-2.mp3',
         'paragraphs': ['Kẻ cướp biết giờ, biết cửa, biết chiếc cặp. Hắn chỉ cần đứng chờ.',
                        'Hai vỏ đạn lô 1968 được gửi lên Phân viện Khoa học hình sự. Trong lúc chờ, Thiếu tá Đức hỏi chuyện người thợ cũ, ông chủ tiệm cầm đồ và ông cụ trông xe đầu ngõ.',
                        'Khẩu súng ấy đã từng nổ ở đâu?']},
        {'stage': 3, 'kicker': 'Ngày 30–31/8/1998 · Phố Hàng Bạc', 'title': 'Mười phút mua bao thuốc lá', 'voice': 'audio/beat-3.mp3',
         'paragraphs': ['Tay súng có tên, có ảnh, nhưng không quen ai trong nhà ông Phúc. Vậy ai đã báo tin cho hắn?',
                        'Ở chi nhánh Hàng Bạc, chị kế toán nhớ lại một chi tiết nhỏ. Ở đầu phố, có một bốt điện thoại thẻ và một hàng nước chè.',
                        'Lúc 22:16, ai đã nhấc máy?']},
        {'stage': 4, 'kicker': 'Ngày 1–2/9/1998 · Phố Khâm Thiên', 'title': 'Mùa World Cup', 'voice': 'audio/beat-4.mp3',
         'paragraphs': ['Một ổ cá độ bóng đá bị triệt phá. Trong cuốn sổ ghi nợ có một cái tên quen.',
                        'Ở bến xe Giáp Bát, chiếc két của tiệm cầm đồ mở ra.',
                        'Vì sao một người lái xe ba năm lại bán lịch tối thứ Tư của ông chủ?']},
        {'stage': 5, 'kicker': 'Ngày 3/9/1998 · Rạng sáng', 'title': 'Bãi sông Hồng', 'voice': 'audio/beat-5.mp3',
         'paragraphs': ['Bốn giờ sáng, một tổ trinh sát áp sát căn nhà trọ ở bãi sông Hồng. Cùng lúc, một tổ khác gõ cửa một căn hộ ở Hà Đông.',
                        'Chỉ mặt những người đã gây ra đêm súng nổ. Và giải thích vì sao.']}],
    'finale': {'title': 'Chiếc cặp da đêm thứ Tư',
               'paragraphs': ['Đặng Quốc Tuấn khai nhận khi chiếc thẻ điện thoại sê-ri 0812774 được đặt lên bàn, cạnh máy nhắn tin còn lưu dòng chữ cuối cùng.',
                              'Mùa World Cup năm ấy, Tuấn thua sáu mươi triệu. Người đến đòi là Cường sẹo. Cường không cần tiền ngay. Cường chỉ cần biết tối thứ Tư ông chủ đi đâu, về lúc nào, xách cái gì.',
                              'Ba tối thứ Tư liền, Tuấn ra bốt điện thoại đầu phố Hàng Bạc, đọc chậm từng chữ cho tổng đài viên. Đến tối thứ Tư thứ tư, cơn mưa giông kéo về.',
                              'Tuấn thả ông chủ ở cửa ngách như mọi lần, rồi đưa xe đi gửi. Anh đứng dưới mái hiên nhà xe, nhìn đồng hồ, châm một điếu Vinataba, đợi đủ ba phút mới chạy về.',
                              'Tạ Văn Cường bị bắt ở bãi sông Hồng, khẩu K54 vẫn nằm dưới gối. Hắn chỉ nói: "Thằng lái xe bảo ông ấy không bao giờ chống cự."',
                              'Bà Hạnh không dự phiên toà. Bà chỉ nhờ người nhắn lại một câu: "Ba năm, ông nhà tôi chưa từng đi đâu mà không có cậu ấy."']},
    'epilogue': [
        {'title': 'Tạ Văn Cường', 'text': 'Bị truy tố về tội giết người và cướp tài sản trong cả hai vụ Chùa Bộc và Bắc Giang.'},
        {'title': 'Đặng Quốc Tuấn', 'text': 'Bị truy tố với vai trò đồng phạm giúp sức. Chiếc Dream II và tám triệu đồng bị thu làm tang vật.'},
        {'title': 'Trần Khắc Hùng', 'text': 'Bị truy tố về tội tiêu thụ tài sản do người khác phạm tội mà có. 20 lượng vàng được trả lại gia đình ông Phúc.'},
        {'title': 'Nguyễn Văn Đông', 'text': 'Bà Hạnh mời anh về làm thợ chính. Ở phiên toà, anh ngồi hàng ghế đầu, cạnh bà.'}],
}

# biên bản kèm ảnh tang vật: chuyển sang kiểu "evidence" (ảnh + các đoạn)
PHOTOS = {
    'd16': ('images/d16-bot-dien-thoai.webp', 'Bốt điện thoại thẻ HB-04 và hàng nước chè bên cạnh, đầu phố Hàng Bạc (ảnh chụp lại đêm 31/8).'),
    'd20': ('images/d20-vang-nung.webp', 'Vàng nung thỏi thô trong két tiệm cầm đồ của Trần Khắc Hùng.'),
    'd23': ('images/d23-tang-vat.webp', 'Một phần tang vật thu ở nhà trọ bãi sông Hồng: cặp da đen bị rạch khoá, áo mưa quân dụng, máy nhắn tin 107-5523 còn hiện tin cuối.'),
    'd24': ('images/d24-the-dien-thoai.webp', 'Thẻ điện thoại sê-ri 0812774 và mẩu giấy thu trong ví và hộc ô tô của Đặng Quốc Tuấn.'),
}
for doc in D:
    if doc['id'] in PHOTOS and os.path.exists(f'public/cases/{CID}/' + PHOTOS[doc['id']][0]):
        paras = []
        for sec in doc.pop('sections', []):
            for k, p in enumerate(sec['paragraphs']):
                paras.append((f"**{sec['heading']}.** " if k == 0 else '') + p)
        for k in ('header', 'heading', 'date', 'signers', 'signature'):
            doc.pop(k, None)
        doc.update({'type': 'evidence', 'image': PHOTOS[doc['id']][0], 'imageCaption': PHOTOS[doc['id']][1], 'paragraphs': paras})

for person in [case['victim'], *case['suspects']]:
    if person.get('image') and not os.path.exists(f'public/cases/{CID}/' + person['image']):
        print('chưa có ảnh:', person['image']); del person['image']
for doc in D:
    if doc.get('image') and not os.path.exists(f'public/cases/{CID}/' + doc['image']):
        print('chưa có ảnh:', doc['image']); del doc['image']
        if doc['type'] in ('photo', 'scan'): doc['type'] = 'note'; doc['paragraphs'] = [doc.pop('caption', '')]
if case['cover'] and not os.path.exists(f'public/cases/{CID}/' + case['cover']):
    print('chưa có ảnh:', case['cover']); case['cover'] = None
json.dump(case, open(f'public/cases/{CID}/case.json', 'w'), ensure_ascii=False, indent=2)
open(f'public/cases/{CID}/case.json', 'a').write('\n')
print(len(D), 'docs', len(Q), 'questions')
