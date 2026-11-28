"""Dựng public/cases/tieng-dan-day-pho-hien/case.json (bản 2, độ khó vừa). Chạy ở thư mục gốc:
python3 authoring/tieng-dan-day-pho-hien/build_case.py

Lời giải: quản lý phường Đỗ Trọng Toàn tẩm mã tiền lên phím đàn sừng của cụ Cửu. Xem bible.md.
"""
import json
import os

CID = 'tieng-dan-day-pho-hien'
CA = ['Công an thị xã Hưng Yên', 'Đội Cảnh sát hình sự']
DTV = 'Điều tra viên'
DTV_NAME = 'Đại uý Trần Văn Kiên'


def tl(name, *pairs):
    return [{'n': i + 1, 'speaker': s or name, 'text': t} for i, (s, t) in enumerate(pairs)]


D = []
add = D.append

# ───────────── Vòng 1: không phải chén trà ─────────────
add({'id': 'd00', 'stage': 1, 'type': 'people', 'title': 'Nạn nhân và những người liên quan',
     'paragraphs': ['Ảnh thẻ trích từ hồ sơ hộ khẩu, kèm lý do từng người được đưa vào diện xác minh sáng 1/10/1993.']})

add({'id': 'd01', 'stage': 1, 'type': 'newspaper', 'title': 'Báo Hải Hưng: Nghệ nhân đàn đáy gục ngã giữa đêm hội',
     'masthead': 'Hải Hưng', 'issue': 'Số 2.310', 'date': 'Thứ Bảy, 2/10/1993',
     'headline': 'Đêm rằm tháng Tám: nghệ nhân đàn đáy gục ngã giữa khúc "Lạc Nhạn"',
     'deck': 'Chén trà sen đổ trên chiếu hoa, cả phường hát nghi có người bỏ độc.',
     'image': 'images/d01-bao-chi.webp', 'imageCaption': 'Đình Hoa Nguyệt bên hồ Bán Nguyệt sáng 1/10.',
     'paragraphs': [
         'Tối 30/9 (rằm tháng Tám Quý Dậu), phường ca trù Kim Nguyệt (hư cấu) tế tổ và diễn ở đình Hoa Nguyệt ven hồ Bán Nguyệt, thị xã Hưng Yên. Đang dạo khúc "Lạc Nhạn", cụ Phan Bá Cửu (68 tuổi), nghệ nhân đàn đáy, trưởng phường, co giật rồi ngã gục.',
         'Cụ được đưa đến trạm xá phường Hiến Nam nhưng mất lúc 21 giờ 10. Ngay trước khi cụ ngã, đào nương Ánh Tuyết vừa dâng chén trà sen; chén trà đổ trên chiếu.',
         'Nhiều người trong phường cho rằng chén trà có độc. Công an thị xã đã niêm phong buồng hoá trang của đình.']})

add({'id': 'd02', 'stage': 1, 'type': 'report', 'title': 'Biên bản khám nghiệm hiện trường đình Hoa Nguyệt',
     'header': CA, 'heading': 'Biên bản khám nghiệm hiện trường', 'code': '91/KNHT', 'date': '22 giờ 00 ngày 30/9/1993',
     'fields': [{'label': 'Địa điểm', 'value': 'Đình Hoa Nguyệt, ven hồ Bán Nguyệt, thị xã Hưng Yên'},
                {'label': 'Nạn nhân', 'value': 'Phan Bá Cửu, 68 tuổi, nghệ nhân đàn đáy, trưởng phường Kim Nguyệt'}],
     'sections': [
         {'heading': '1. Chiếu diễn (đại bái)', 'paragraphs': ['Cây đàn đáy khảm xà cừ của nạn nhân đặt nghiêng trên chiếu hoa. Chén trà sen úp, nước trà loang ra chiếu; ấm trà còn gần đầy.',
                                                               '**Phím gảy bằng sừng trâu** (hình lá, dài 6 cm) rơi cạnh đàn; mặt phím bóng, hơi dính tay.']},
         {'heading': '2. Buồng hoá trang', 'paragraphs': ['Ở góc tây nam đình, một cửa vào từ đại bái, một cửa sổ nhỏ trông ra cổng đình. Tráp gỗ đựng nhạc cụ của nạn nhân để trên án, không khoá.']},
         {'heading': '3. Thu giữ', 'paragraphs': ['Phím gảy, chén trà, ấm trà, cây đàn, tráp gỗ. Đã gửi hoá nghiệm.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd03', 'stage': 1, 'type': 'scan', 'title': 'Sơ đồ đình Hoa Nguyệt đêm 30/9',
     'image': 'images/d03-so-do-dinh.webp', 'caption': 'Sơ đồ lập khi khám nghiệm: đại bái (chiếu diễn), tiền đình (hương án), buồng hoá trang ở góc tây nam có cửa sổ nhỏ trông ra phía cổng, quán nước bà Mùi ngay góc cổng đình.'})

add({'id': 'd04', 'stage': 1, 'type': 'photo', 'title': 'Ảnh cây đàn đáy, tráp gỗ và phím gảy',
     'image': 'images/d04-dan-day.webp', 'label': 'Tang vật ảnh số 2 · 1/10/1993',
     'caption': 'Cây đàn đáy khảm xà cừ của cụ Cửu, tráp gỗ lót nhung đỏ và chiếc phím gảy bằng sừng trâu.'})

add({'id': 'd05', 'stage': 1, 'type': 'report', 'title': 'Kết quả giám định pháp y sơ bộ',
     'header': ['Trung tâm Pháp y tỉnh Hải Hưng'], 'heading': 'Kết quả giám định sơ bộ', 'code': '177/PY', 'date': 'Ngày 1 tháng 10 năm 1993',
     'sections': [
         {'heading': '1. Triệu chứng (theo trạm xá)', 'paragraphs': ['Co giật từng cơn, người uốn cong, cứng hàm, nạn nhân tỉnh táo đến gần cuối. Tử vong lúc 21:10 do ngạt vì co cứng cơ hô hấp.',
                                                                      'Triệu chứng điển hình của ngộ độc **strychnin** (hoạt chất của hạt **mã tiền**), khởi phát khoảng 15–30 phút sau khi chất độc vào cơ thể.']},
         {'heading': '2. Khám trong', 'paragraphs': ['Niêm mạc lưỡi và vòm miệng có nồng độ strychnin cao nhất. **Dạ dày không có nước trà**, chỉ có cơm và chút rượu từ bữa chiều.']}],
     'signature': 'Giám định viên: BS. Vũ Thị Lan'})

add({'id': 'd06', 'stage': 1, 'type': 'photo', 'title': 'Ảnh lưu niệm phường Kim Nguyệt năm 1991',
     'image': 'images/d06-anh-chan-dung.webp', 'label': 'Ảnh do gia đình nạn nhân cung cấp',
     'caption': 'Từ trái sang: đào nương Nguyễn Thị Ánh Tuyết, cụ Phan Bá Cửu ôm đàn đáy, kép đàn Chu Văn Bình.'})

add({'id': 'd07', 'stage': 1, 'type': 'testimony', 'title': 'Lời khai của đào nương Nguyễn Thị Ánh Tuyết',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '23 giờ 00 ngày 30/9/1993',
     'fields': [{'label': 'Người khai', 'value': 'Nguyễn Thị Ánh Tuyết, 28 tuổi, đào nương phường Kim Nguyệt'}],
     'lines': tl('Nguyễn Thị Ánh Tuyết',
         (DTV, 'Chị dâng trà cho cụ Cửu lúc nào?'),
         (None, 'Tám giờ mười, cụ đang dạo đàn thì em dâng chén trà sen như lệ. Cụ gật đầu nhưng chưa nhấp, vì đang gảy.'),
         (DTV, 'Sau đó?'),
         (None, 'Chừng mười phút sau tay cụ cứng lại, người giật lên, gạt đổ chén trà. Cụ vẫn nhìn em, nói không ra tiếng.'),
         (DTV, 'Sáng nay cụ phê bình chị?'),
         (None, 'Vâng, tổng duyệt cụ mắng em hát lạc phách trước cả phường. Em khóc, nhưng cụ dạy em mười năm nay, em không bao giờ hại cụ.')),
     'signature': 'Người khai: Nguyễn Thị Ánh Tuyết'})

# ───────────── Vòng 2: chiếc phím sừng ─────────────
add({'id': 'd08', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của kép đàn Chu Văn Bình',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '08 giờ 30 ngày 1/10/1993',
     'fields': [{'label': 'Người khai', 'value': 'Chu Văn Bình, 40 tuổi, học trò đàn đáy của cụ Cửu 15 năm'}],
     'lines': tl('Chu Văn Bình',
         (DTV, 'Tuần trước cụ Cửu truất anh khỏi đội đi hội diễn tỉnh?'),
         (None, 'Vâng. Cụ bảo tiếng đàn của tôi "còn vướng bụi trần". Tôi buồn, nhưng thầy nói thì trò nghe.'),
         (DTV, 'Từ 19:30 đến 20:00 anh ở đâu?'),
         (None, 'Tôi đứng ở tiền đình hầu hương với thầy, rồi ra sân hút thuốc.'),
         (DTV, 'Anh có vào buồng hoá trang không?'),
         (None, 'Không. Tráp đàn của thầy, không ai được đụng vào. Tôi không vào buồng ấy lần nào.')),
     'signature': 'Người khai: Chu Văn Bình'})

add({'id': 'd09', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của quản lý phường Đỗ Trọng Toàn',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '10 giờ 00 ngày 1/10/1993',
     'fields': [{'label': 'Người khai', 'value': 'Đỗ Trọng Toàn, 52 tuổi, quản lý tài chính phường Kim Nguyệt'}],
     'lines': tl('Đỗ Trọng Toàn',
         (DTV, 'Tối 30/9 ông làm gì?'),
         (None, 'Tôi lo lễ vật, đón khách. Từ bảy rưỡi đến tám giờ tôi đứng ở tiền đình thắp hương cùng cụ Cửu, không rời đi đâu.'),
         (DTV, 'Ông có vào buồng hoá trang không?'),
         (None, 'Không, buồng ấy của nghệ nhân.'),
         (DTV, 'Tiền tài trợ mua nhạc cụ năm nay thế nào?'),
         (None, 'Sở Văn hoá cấp ba triệu, tôi mua đủ một bộ nhạc cụ mới, hoá đơn đầy đủ. Cụ Cửu đã xem và hài lòng.')),
     'signature': 'Người khai: Đỗ Trọng Toàn'})

add({'id': 'd10', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của ông Phan Bá Lộc (con trai nạn nhân)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 00 ngày 1/10/1993',
     'fields': [{'label': 'Người khai', 'value': 'Phan Bá Lộc, 42 tuổi, buôn đồ cổ ở phố Hàng Bạc, Hà Nội'}],
     'lines': tl('Phan Bá Lộc',
         (DTV, 'Ông muốn bán cây đàn gia bảo của cụ Cửu?'),
         (None, 'Có người Hồng Kông trả hai mươi lượng vàng. Tôi nói với bố, bố đuổi tôi ra khỏi nhà. Bố bảo đàn này chết theo bố.'),
         (DTV, 'Tối 30/9 ông ở đâu?'),
         (None, 'Tôi về dự lễ tế tổ, ngồi chiếu khách ở tiền đình cạnh ông thủ từ từ bảy giờ đến lúc bố ngã.')),
     'signature': 'Người khai: Phan Bá Lộc'})

add({'id': 'd11', 'stage': 2, 'type': 'note', 'title': 'Trích sổ tay ghi chép của đào nương Ánh Tuyết',
     'paragraphs': ['Sổ tay học đàn hát của Ánh Tuyết, chép lời thầy dạy (1983–1993):',
                    '— "Phím sừng phải ấm, phải ẩm. Trước khi dạo, thầy ngậm phím vào miệng một lúc cho sừng mềm, tiếng mới ngọt." Cả phường đều biết thói quen này.',
                    '— Phím của thầy để trong tráp, nằm trên mặt nhung, thầy không cho ai chạm.',
                    '— Rằm tháng Tám: thầy thắp hương tổ ở tiền đình từ bảy rưỡi, tám giờ ra chiếu, dạo "Lạc Nhạn" mở hội.'],
     'signature': 'Nguyễn Thị Ánh Tuyết'})

add({'id': 'd12', 'stage': 2, 'type': 'report', 'title': 'Kết quả hoá nghiệm tang vật',
     'header': ['Phân viện Khoa học hình sự', 'Bộ Nội vụ'], 'heading': 'Kết quả hoá nghiệm', 'code': '603/HN', 'date': 'Ngày 2/10/1993',
     'sections': [
         {'heading': '1. Phím gảy sừng trâu', 'paragraphs': ['Mặt phím có một lớp **mật ong** trộn **bột hạt mã tiền** (strychnin). Lượng còn lại đủ gây ngộ độc nặng cho một người già.']},
         {'heading': '2. Chén trà, ấm trà sen', 'paragraphs': ['**Không phát hiện chất độc.**']},
         {'heading': '3. Tráp gỗ', 'paragraphs': ['Mặt nhung chỗ đặt phím có vệt mật ong. Không phát hiện bột độc ở chỗ khác trong tráp.']}],
     'signature': 'Giám định viên: Thượng uý Nguyễn Văn Hải'})

add({'id': 'd13', 'stage': 2, 'type': 'testimony', 'title': 'Lời khai của bà Lê Thị Mùi (bán nước chè ở cổng đình)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '16 giờ 00 ngày 1/10/1993',
     'fields': [{'label': 'Người khai', 'value': 'Lê Thị Mùi, 61 tuổi, bán nước chè ngay ngoài cổng đình'}],
     'lines': tl('Lê Thị Mùi',
         (DTV, 'Từ quán bà có nhìn thấy buồng hoá trang không?'),
         (None, 'Thấy cái cửa sổ nhỏ, có đèn. Bảy giờ ba lăm, trong buồng có người mặc áo the, đội khăn xếp ngồi gảy đàn đáy. Tôi lạ, vì cụ Cửu đang thắp hương ngoài tiền đình kia mà.'),
         (DTV, 'Người ấy ngồi bao lâu?'),
         (None, 'Năm phút. Tiếng đàn vụng, lạc phím mấy lần. Rồi đèn tắt một lúc.'),
         (DTV, 'Sau đó?'),
         (None, 'Tám giờ kém mười tám, có một người đeo kính, mặc sơ mi trắng, cầm cặp da vào buồng, cúi xuống cái án. Tám giờ kém mười ba thì ra, lấy khăn lau tay mãi.')),
     'signature': 'Người khai: Lê Thị Mùi'})

# ───────────── Vòng 3: năm phút ở buồng hoá trang ─────────────
add({'id': 'd14', 'stage': 3, 'type': 'testimony', 'title': 'Lời khai của ông Nguyễn Văn Thắm (thủ từ đình Hoa Nguyệt)',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '09 giờ 00 ngày 2/10/1993',
     'fields': [{'label': 'Người khai', 'value': 'Nguyễn Văn Thắm, 70 tuổi, thủ từ đình Hoa Nguyệt'}],
     'lines': tl('Nguyễn Văn Thắm',
         (DTV, 'Từ 19:30 đến 20:00 ở tiền đình có những ai?'),
         (None, 'Cụ Cửu khấn tổ, tôi đứng hầu. Anh Lộc con cụ ngồi chiếu khách cạnh tôi suốt, không đứng dậy lần nào.'),
         (DTV, 'Ông Toàn quản lý thì sao?'),
         (None, 'Anh Toàn đứng được mười phút. Bảy giờ bốn mươi thì bảo đi lấy sổ công đức, tám giờ kém mười mới quay ra, tay còn cầm cái cặp da.'),
         (DTV, 'Anh Bình?'),
         (None, 'Bình đứng ở cửa tiền đình lúc đầu, rồi lẩn đâu mất chừng bảy giờ ba mươi lăm, tám giờ mới thấy lại.')),
     'signature': 'Người khai: Nguyễn Văn Thắm'})

add({'id': 'd15', 'stage': 3, 'type': 'testimony', 'title': 'Biên bản ghi lời khai lần hai của Chu Văn Bình',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '14 giờ 00 ngày 2/10/1993',
     'fields': [{'label': 'Người khai', 'value': 'Chu Văn Bình, 40 tuổi'}],
     'lines': tl('Chu Văn Bình',
         (DTV, 'Bà Mùi thấy người mặc áo the gảy đàn trong buồng hoá trang lúc 19:35.'),
         (None, '(Cúi đầu) Là tôi. Mười lăm năm tôi chưa từng được chạm vào cây đàn của thầy. Tôi chỉ muốn gảy thử một lần trước khi bị loại khỏi hội diễn.'),
         (DTV, 'Anh gảy bằng gì?'),
         (None, 'Bằng ngón tay. Tôi không dám đụng vào phím của thầy. Lúc tôi mở tráp, cái phím nằm trên nhung, khô, xỉn như mọi ngày.'),
         (DTV, 'Anh ra lúc nào?'),
         (None, 'Bảy giờ bốn mươi. Tôi đậy tráp, tắt đèn, ra sân đứng một mình đến tám giờ. Lúc thầy ngã, tôi thấy cái phím rơi trên chiếu bóng lên, tôi đã thấy lạ.')),
     'signature': 'Người khai: Chu Văn Bình'})

add({'id': 'd16', 'stage': 3, 'type': 'report', 'title': 'Biên bản xác minh tại hiệu thuốc bắc Nam Hoà Đường',
     'header': CA, 'heading': 'Biên bản xác minh', 'code': '34/XM', 'date': 'Ngày 3/10/1993',
     'sections': [
         {'heading': 'Kết quả', 'paragraphs': ['Sổ bán hàng của hiệu Nam Hoà Đường (phố Bắc Hoà, thị xã Hưng Yên) ngày 22/9/1993: "Mã tiền chế, 20 g, ngâm rượu xoa bóp. Người mua: Toàn, phường hát Kim Nguyệt."',
                                                 'Ông lang Hoàng Văn Quý nhớ người mua đeo kính, cầm cặp da, hỏi kỹ "uống nhầm thì bao lâu mới phát".',
                                                 'Mã tiền là vị thuốc độc bảng A, chỉ bán theo yêu cầu, ghi sổ.']}],
     'signers': [{'role': DTV, 'name': DTV_NAME}]})

add({'id': 'd17', 'stage': 3, 'type': 'testimony', 'title': 'Biên bản ghi lời khai lần hai của Đỗ Trọng Toàn',
     'header': CA, 'heading': 'Biên bản ghi lời khai', 'date': '16 giờ 00 ngày 3/10/1993',
     'fields': [{'label': 'Người khai', 'value': 'Đỗ Trọng Toàn, 52 tuổi'}],
     'lines': tl('Đỗ Trọng Toàn',
         (DTV, 'Ông thủ từ nói ông rời tiền đình từ 19:40 đến 19:50.'),
         (None, 'À, tôi đi lấy sổ công đức để ghi tiền khách cúng. Quên không kể.'),
         (DTV, 'Sổ công đức để ở đâu?'),
         (None, 'Ở phòng thủ từ, sau tiền đình. Tôi không vào buồng hoá trang.'),
         (DTV, 'Ông mua mã tiền ở Nam Hoà Đường làm gì?'),
         (None, 'Ngâm rượu xoa bóp chữa đau lưng. Ai chẳng ngâm.')),
     'signature': 'Người khai: Đỗ Trọng Toàn'})

# ───────────── Vòng 4: ba triệu tiền nhạc cụ ─────────────
add({'id': 'd18', 'stage': 4, 'type': 'letter', 'title': 'Thư cụ Phan Bá Cửu gửi Sở Văn hoá Thông tin Hải Hưng (bản nháp)',
     'date': 'Phố Hiến, ngày 27 tháng 9 năm 1993', 'greeting': 'Kính gửi: Sở Văn hoá Thông tin tỉnh Hải Hưng',
     'paragraphs': [
         'Tôi là Phan Bá Cửu, trưởng phường Kim Nguyệt. Năm nay phường nhận ba triệu đồng tiền tài trợ mua nhạc cụ. Bộ nhạc cụ quản lý Đỗ Trọng Toàn mua về là đàn đáy dây nilon, phách gỗ tạp, hoá đơn ghi giá gấp ba giá chợ.',
         'Tôi đã hỏi hiệu nhạc cụ Hàng Gai: bộ ấy chỉ đáng chừng chín trăm nghìn. Anh Toàn xin tôi thư thả đến sau hội diễn tỉnh. Tôi không thể.',
         'Sau đêm tế tổ rằm tháng Tám, tôi sẽ tự mang thư và hoá đơn lên Sở. Kính mong Sở cử người kiểm tra.'],
     'signature': 'Phan Bá Cửu (thư tìm thấy trong ngăn đáy tráp đàn, dưới lớp nhung)'})

add({'id': 'd19', 'stage': 4, 'type': 'evidence', 'title': 'Biên bản khám xét cặp da của Đỗ Trọng Toàn',
     'code': 'TV-13', 'image': 'images/d13-khan-lua.webp', 'imageCaption': 'Khăn lụa vàng dính vết mật ong và túi gấm thêu chữ Thọ thu trong cặp da của Đỗ Trọng Toàn.',
     'paragraphs': ['1. Một khăn tay lụa vàng có vết mật ong khô; hoá nghiệm có strychnin.',
                    '2. Một túi gấm thêu chữ Thọ, bên trong còn khoảng 12 g bột mã tiền chế, bọc giấy của hiệu Nam Hoà Đường.',
                    '3. Hoá đơn mua bộ nhạc cụ ghi 2.950.000 đồng; hiệu Hàng Gai xác nhận chỉ bán 900.000 đồng, hoá đơn do người mua tự ghi.',
                    '4. Không có chai rượu thuốc ngâm mã tiền nào ở nhà Toàn.']})

CARDS = ['binh', 'tuyet', 'toan', 'loc']
NAMES = ['Chu Văn Bình', 'Nguyễn Thị Ánh Tuyết', 'Đỗ Trọng Toàn', 'Phan Bá Lộc']
Q = [
    {'id': 'q1', 'stage': 1, 'type': 'choice', 'title': 'Chén trà sen hay thứ khác?',
     'prompt': 'Cả phường nghi chén trà sen có độc. Theo hồ sơ đang mở, nhận định nào đứng vững?',
     'options': ['Cụ Cửu uống chén trà sen có độc do đào nương dâng, rồi co giật và gục ngã.',
                 'Cụ Cửu không uống trà; chất độc vào qua miệng bằng một đường khác, và triệu chứng là của mã tiền.',
                 'Cụ Cửu tuổi cao, xúc động khi diễn nên lên cơn đột quỵ; không có chất độc nào.'],
     'answer': [1],
     'nudges': {'0': {'message': 'Pháp y nói gì về nước trà trong dạ dày?'},
                '2': {'message': 'Pháp y mô tả triệu chứng của chất gì?'}},
     'hints': ['Đọc kết luận pháp y.', 'Dạ dày có trà không? Chất độc tập trung ở đâu?',
               'd05: strychnin (mã tiền), cao nhất ở lưỡi và vòm miệng, dạ dày không có trà.'],
     'solved': 'Không phải chén trà. Chất độc vào qua miệng, nhưng không phải bằng đường uống.',
     'explanation': [{'title': 'Chất độc', 'body': ['d05: co giật, cứng hàm, tỉnh táo: ngộ độc strychnin từ hạt mã tiền.']},
                     {'title': 'Không phải trà', 'body': ['d05: dạ dày không có nước trà.']},
                     {'title': 'Ở miệng', 'body': ['d05: nồng độ cao nhất ở niêm mạc lưỡi và vòm miệng.']}]},
    {'id': 'q2', 'stage': 1, 'type': 'evidence', 'need': 2, 'title': 'Chén trà chưa nhấp',
     'prompt': 'Ghim 2 tài liệu cho thấy chén trà sen không phải nguồn chất độc.',
     'answer': ['d05', 'd07'],
     'nudges': [{'any': ['d02'], 'near': True, 'message': 'Biên bản tả chén trà đổ. Cần tài liệu nói cụ có uống trà hay không.'}],
     'hints': ['Một kết luận pháp y, một lời khai.', 'Cụ đã nhấp trà chưa? Dạ dày có trà không?',
               'd05: dạ dày không có trà. d07: cụ gật đầu nhưng chưa nhấp vì đang gảy; chén đổ khi cụ co giật.'],
     'solved': 'Cụ Cửu chưa từng nhấp chén trà. Nó đổ vì cụ co giật, không phải ngược lại.',
     'explanation': [{'title': 'Pháp y', 'body': ['d05: dạ dày không có trà.']},
                     {'title': 'Lời đào nương', 'body': ['d07: cụ chưa nhấp vì đang gảy; mười phút sau co giật, gạt đổ chén.']},
                     {'title': 'Còn lại', 'body': ['d02: phím gảy sừng trâu bóng, hơi dính tay.']}]},
    {'id': 'q3', 'stage': 2, 'type': 'evidence', 'need': 2, 'title': 'Chiếc phím sừng',
     'prompt': 'Ghim 2 tài liệu cho thấy chất độc đã vào miệng cụ Cửu bằng đường nào.',
     'answer': ['d11', 'd12'],
     'nudges': [{'any': ['d04'], 'near': True, 'message': 'Ảnh cho thấy chiếc phím. Cần tài liệu về thói quen của cụ và kết quả hoá nghiệm.'}],
     'hints': ['Một ghi chép về thói quen, một kết quả hoá nghiệm.', 'Cụ làm gì với phím trước khi dạo đàn? Trên phím có gì?',
               'd11: cụ ngậm phím vào miệng trước khi dạo, cả phường biết. d12: mặt phím có mật ong trộn bột mã tiền; trà sạch.'],
     'solved': 'Ai đó đã tẩm mật ong trộn mã tiền lên chiếc phím mà cụ luôn ngậm trước khi dạo đàn.',
     'explanation': [{'title': 'Thói quen', 'body': ['d11: cụ ngậm phím cho sừng mềm, cả phường biết; phím để trong tráp.']},
                     {'title': 'Hoá nghiệm', 'body': ['d12: mật ong trộn bột mã tiền trên phím; vệt mật ong trên nhung tráp.']},
                     {'title': 'Khi nào', 'body': ['d11: cụ thắp hương ở tiền đình từ 19:30, tráp để trong buồng hoá trang.']}]},
    {'id': 'q4', 'stage': 2, 'type': 'line', 'title': 'Tiếng đàn vụng trong buồng hoá trang',
     'prompt': 'Chỉ ra dòng khai bị lời bà bán nước ở cổng đình bác bỏ.',
     'answer': ['d08:006'],
     'nudges': {'d08:004': {'near': True, 'message': 'Câu này mơ hồ. Tìm câu khẳng định thẳng về buồng hoá trang.'},
                'd09:004': {'message': 'Bà Mùi có nhắc tới người đeo kính, nhưng chưa nói rõ là ai. Người mặc áo the đội khăn xếp thì sao?'}},
     'hints': ['Bà Mùi thấy ai gảy đàn lúc 19:35?', 'Trong phường, ngoài cụ Cửu, ai mặc áo the đội khăn xếp gảy đàn đáy?',
               'd08 dòng 6: không vào buồng lần nào. d13: 19:35 người mặc áo the, khăn xếp gảy đàn vụng trong buồng. d06: Bình là kép đàn mặc áo the, khăn xếp.'],
     'solved': 'Bình đã vào buồng hoá trang lúc 19:35. Nhưng bà Mùi còn thấy một người khác vào sau.',
     'explanation': [{'title': 'Câu khai', 'body': ['d08 dòng 6: không vào buồng hoá trang lần nào.']},
                     {'title': 'Bị bác', 'body': ['d13: 19:35 người mặc áo the, khăn xếp gảy đàn vụng; cụ Cửu đang ở tiền đình. d06: Bình là kép đàn mặc áo the.']},
                     {'title': 'Người thứ hai', 'body': ['d13: 19:42 người đeo kính, sơ mi trắng, cầm cặp da vào, 19:47 ra, lau tay mãi.']}]},
    {'id': 'q5', 'stage': 3, 'type': 'line', 'title': 'Mười phút đi lấy sổ',
     'prompt': 'Chỉ ra dòng khai bị lời ông thủ từ bác bỏ.',
     'answer': ['d09:002'],
     'nudges': {'d10:004': {'message': 'Ông thủ từ xác nhận ông Lộc ngồi cạnh suốt.'},
                'd08:004': {'near': True, 'message': 'Lời Bình cũng bị bác, nhưng đã bị bác ở vòng trước. Tìm người khác.'}},
     'hints': ['Ông thủ từ nói ai rời tiền đình lúc 19:40?', 'Ai khai đứng ở tiền đình suốt?',
               'd09 dòng 2: đứng ở tiền đình 19:30–20:00 không rời đi. d14: 19:40 ông Toàn đi "lấy sổ công đức", 19:50 mới quay ra, tay cầm cặp da.'],
     'solved': 'Ông Toàn rời tiền đình mười phút, đúng lúc bà Mùi thấy người đeo kính cầm cặp da vào buồng hoá trang.',
     'explanation': [{'title': 'Câu khai', 'body': ['d09 dòng 2: không rời tiền đình.']},
                     {'title': 'Bị bác', 'body': ['d14: 19:40–19:50 ông Toàn rời tiền đình, quay ra tay cầm cặp da.']},
                     {'title': 'Khớp', 'body': ['d13: 19:42–19:47 người đeo kính, sơ mi trắng, cầm cặp da vào buồng hoá trang.']}]},
    {'id': 'q6', 'stage': 3, 'type': 'evidence', 'need': 2, 'title': 'Phím còn khô lúc 19:40',
     'prompt': 'Ghim 2 tài liệu cho thấy chiếc phím bị tẩm độc sau khi Bình rời buồng, và ai vào buồng sau đó.',
     'answer': ['d13', 'd15'],
     'nudges': [{'any': ['d14'], 'near': True, 'message': 'Ông thủ từ cho biết ai rời tiền đình. Cần tài liệu cho thấy ai vào buồng và chiếc phím lúc ấy thế nào.'}],
     'hints': ['Một lời khai của người ngồi ngoài cổng, một lời khai của người gảy đàn.', 'Lúc Bình mở tráp, phím thế nào? Ai vào buồng sau Bình?',
               'd15: 19:35–19:40 phím trên nhung khô, xỉn. d13: 19:42–19:47 người đeo kính cầm cặp da vào buồng, ra lau tay mãi.'],
     'solved': 'Chiếc phím còn khô lúc 19:40. Năm phút sau, người đeo kính cầm cặp da đã ở trong buồng.',
     'explanation': [{'title': 'Khô lúc 19:40', 'body': ['d15: Bình gảy bằng ngón tay, thấy phím khô, xỉn như mọi ngày.']},
                     {'title': 'Người vào sau', 'body': ['d13: 19:42–19:47 người đeo kính, sơ mi trắng, cầm cặp da; ra lau tay bằng khăn.']},
                     {'title': 'Lúc cụ ngã', 'body': ['d15: phím trên chiếu bóng lên. d12: mật ong trộn mã tiền.']}]},
    {'id': 'q7', 'stage': 4, 'type': 'evidence', 'need': 2, 'title': 'Ba triệu tiền nhạc cụ',
     'prompt': 'Ghim 2 tài liệu cho thấy vì sao ông Toàn cần cụ Cửu im lặng trước khi lên Sở, và tang vật nối ông với chiếc phím.',
     'answer': ['d18', 'd19'],
     'nudges': [{'any': ['d16'], 'near': True, 'message': 'Sổ hiệu thuốc cho biết ai mua mã tiền. Cần tài liệu về động cơ và tang vật tìm thấy.'}],
     'hints': ['Một lá thư, một biên bản khám xét.', 'Cụ Cửu định làm gì sau đêm tế tổ? Trong cặp da ông Toàn có gì?',
               'd18: hoá đơn nhạc cụ gấp ba, cụ định mang lên Sở sau đêm rằm. d19: khăn lụa dính mật ong có strychnin, túi gấm còn bột mã tiền, hoá đơn khống.'],
     'solved': 'Cụ Cửu sắp mang hoá đơn khống lên Sở. Ông Toàn chọn đêm rằm, lúc cả phường đổ dồn mắt vào chén trà.',
     'explanation': [{'title': 'Động cơ', 'body': ['d18: bộ nhạc cụ chỉ đáng 900 nghìn, hoá đơn ghi gần 3 triệu; cụ sẽ lên Sở sau đêm tế tổ.']},
                     {'title': 'Tang vật', 'body': ['d19: khăn lụa dính mật ong có strychnin, túi gấm còn mã tiền chế của Nam Hoà Đường.']},
                     {'title': 'Lời nói dối', 'body': ['d17: "ngâm rượu xoa bóp"; d19: không có chai rượu thuốc nào ở nhà.']}]},
    {'id': 'q-accuse', 'stage': 4, 'type': 'choice', 'cards': CARDS, 'title': 'Chỉ mặt thủ phạm',
     'prompt': 'Ai đã đầu độc cụ Phan Bá Cửu? Chọn một người.',
     'options': NAMES, 'answer': [2],
     'nudges': {'0': {'message': 'Bình vào buồng trước, lúc phím còn khô (d15). Người vào sau là ai (d13, d14)?'},
                '1': {'message': 'Chén trà sạch, cụ chưa nhấp (d05, d07, d12).'},
                '3': {'message': 'Ông Lộc ngồi cạnh ông thủ từ suốt từ 19:00 (d14).'}},
     'hints': ['Người làm cần: biết thói quen ngậm phím, vào buồng sau 19:40, có mã tiền và mật ong.', 'Ai đeo kính, cầm cặp da, rời tiền đình 19:40–19:50?',
               'Ông Toàn: rời tiền đình (d14), vào buồng (d13), mua mã tiền (d16), khăn và túi gấm (d19), hoá đơn khống (d18).'],
     'solved': 'Đỗ Trọng Toàn.',
     'explanation': [{'title': 'Thời điểm', 'body': ['d13, d14, d15: phím khô lúc 19:40; 19:42–19:47 ông Toàn ở trong buồng.']},
                     {'title': 'Chất độc', 'body': ['d16, d19: mua mã tiền chế ngày 22/9; còn 12 g trong túi gấm; khăn dính mật ong có strychnin.']},
                     {'title': 'Động cơ', 'body': ['d18: hoá đơn nhạc cụ khống, cụ Cửu sắp lên Sở.']}]},
    {'id': 'q8', 'stage': 4, 'type': 'choice', 'title': 'Kết luận điều tra',
     'prompt': 'Chọn bản kết luận đúng với hồ sơ ở mọi chi tiết.',
     'options': [
         'Ông Toàn ghi hoá đơn khống gấp ba tiền mua nhạc cụ, biết cụ Cửu sẽ mang hoá đơn lên Sở sau đêm rằm. Ông mua mã tiền chế ở Nam Hoà Đường, trộn với mật ong; lúc cụ thắp hương ở tiền đình, 19:42 ông vào buồng hoá trang phết lên chiếc phím sừng mà cụ luôn ngậm trước khi dạo đàn. 20:05 cụ ngậm phím, dạo "Lạc Nhạn" rồi co giật; chén trà đổ chỉ khiến mọi người nghi oan đào nương.',
         'Bình hận vì bị truất khỏi hội diễn tỉnh, lẻn vào buồng hoá trang lúc 19:35 tẩm mã tiền lên phím đàn của thầy rồi gảy thử để che tiếng động, sau đó làm đổ chén trà sen của Ánh Tuyết lúc cụ ngã để đổ tội cho đào nương; ông Toàn chỉ vào buồng lấy sổ công đức, còn túi mã tiền trong cặp da là Bình nhét vào để đổ tội.',
         'Ánh Tuyết giận vì bị cụ mắng trước cả phường trong buổi tổng duyệt, bỏ mã tiền vào chén trà sen dâng lên lúc 20:10; cụ nhấp một ngụm rồi co giật, chén trà đổ để xoá dấu vết, còn mật ong trên phím là do cụ tự bôi cho sừng mềm, và người đeo kính bà Mùi thấy chỉ vào buồng tìm khăn lau.',
         'Ông Lộc muốn bán cây đàn gia bảo cho người Hồng Kông, nhờ ông Toàn mua mã tiền rồi tự tay tẩm lên phím đàn của bố trước buổi lễ, định nhân lúc lộn xộn mang cây đàn đi; ông Toàn chỉ mua thuốc giúp mà không biết dùng làm gì, rồi sợ liên luỵ nên giấu túi thuốc và khăn lau trong cặp.'],
     'answer': [0],
     'exam': {'examiner': 'Kiểm sát viên Đỗ Thị Hằng',
              'intro': 'Trình bày kết luận trước kiểm sát viên: trả lời lần lượt từng câu hỏi bằng lời của mình. Không dùng được AI thì bấm “Trả lời bằng trắc nghiệm” để chọn bản kết luận đúng.'},
     'nudges': {'1': {'message': 'Lúc Bình ra khỏi buồng, phím vẫn khô (d15). Người vào sau là ông Toàn (d13, d14).'},
                '2': {'message': 'Chén trà sạch, cụ chưa nhấp (d05, d07, d12).'},
                '3': {'message': 'Ông Lộc ngồi cạnh thủ từ suốt (d14). Khăn và túi mã tiền nằm trong cặp ông Toàn (d19).'}},
     'hints': ['Đối chiếu: phím khô lúc 19:40 (d15), ai vào buồng sau đó (d13, d14), ai mua mã tiền (d16).', 'Chỉ một phương án có hoá đơn khống, phím sừng và thời điểm 19:42.', 'Phương án A.'],
     'solved': 'Hồ sơ khép lại với tên Đỗ Trọng Toàn.',
     'explanation': [{'title': 'Cách làm', 'body': ['d11, d12, d13: mật ong trộn mã tiền trên phím; cụ ngậm phím trước khi dạo.']},
                     {'title': 'Thời điểm', 'body': ['d14, d15: phím khô lúc 19:40; ông Toàn rời tiền đình 19:40–19:50.']},
                     {'title': 'Vì sao', 'body': ['d18, d19: hoá đơn nhạc cụ khống; cụ sắp lên Sở.']}]},
]

case = {
    'id': CID, 'no': 3, 'status': 'available',
    'title': 'Tiếng đàn đáy Phố Hiến',
    'subtitle': 'Một khúc "Lạc Nhạn" dở dang, một chén trà đổ và chiếc phím sừng',
    'tagline': 'Đêm rằm tháng Tám, nghệ nhân đàn đáy gục ngã giữa khúc dạo đầu. Cả phường nhìn vào chén trà sen. Không ai nhìn chiếc phím.',
    'difficulty': 3, 'players': '1–5', 'duration': '60–75 phút',
    'setting': 'Đình Hoa Nguyệt (hư cấu) ven hồ Bán Nguyệt, thị xã Hưng Yên', 'era': 'Tháng 9/1993',
    'tags': ['Án mạng', 'Đầu độc', 'Ca trù', 'Phố Hiến'], 'cover': 'images/cover.webp',
    'contentWarning': 'Hồ sơ có mô tả một vụ đầu độc. Phường hát, nhân vật và sự việc đều hư cấu.',
    'synopsis': ['Đêm rằm tháng Tám năm 1993, phường ca trù Kim Nguyệt tế tổ ở đình Hoa Nguyệt ven hồ Bán Nguyệt. Cụ Phan Bá Cửu, nghệ nhân đàn đáy, gục ngã khi vừa dạo khúc "Lạc Nhạn".',
                 'Chén trà sen đào nương vừa dâng đổ loang trên chiếu. Cả phường tin chén trà có độc. Pháp y nói: cụ chưa uống một ngụm nào.'],
    'intro': {'title': 'Tiếng đàn đáy Phố Hiến',
              'paragraphs': ['Thị xã Hưng Yên, đất Phố Hiến xưa, đêm rằm tháng Tám năm 1993. Phường ca trù Kim Nguyệt tế tổ ở đình Hoa Nguyệt bên hồ Bán Nguyệt.',
                             'Tám giờ, cụ Phan Bá Cửu ngồi lên chiếu hoa, ôm cây đàn đáy khảm xà cừ, dạo khúc "Lạc Nhạn". Đào nương dâng chén trà sen. Mười phút sau, tay cụ cứng lại, người giật lên, chén trà đổ.',
                             'Bạn là điều tra viên Đội Cảnh sát hình sự Công an thị xã Hưng Yên. Bốn người có lý do bị nghi. Hãy bắt đầu từ kết luận pháp y.'],
              'objective': 'Tìm ra chất độc vào người cụ Cửu bằng đường nào, ai đã đặt nó, lúc nào và vì sao.'},
    'victim': {'id': 'cuu', 'name': 'Phan Bá Cửu', 'age': 68, 'role': 'Nghệ nhân đàn đáy, trưởng phường Kim Nguyệt', 'image': 'images/id-cuu.webp',
               'note': 'Gục ngã khi dạo đàn tối 30/9/1993 (rằm tháng Tám), mất lúc 21:10 tại trạm xá.'},
    'suspects': [
        {'id': 'binh', 'name': 'Chu Văn Bình', 'age': 40, 'role': 'Kép đàn, học trò 15 năm', 'image': 'images/id-binh.webp', 'voice': 'M1',
         'suspicion': 'Tuần trước bị cụ Cửu truất khỏi đội đi hội diễn tỉnh vì tiếng đàn "còn vướng bụi trần".'},
        {'id': 'tuyet', 'name': 'Nguyễn Thị Ánh Tuyết', 'age': 28, 'role': 'Đào nương', 'image': 'images/id-tuyet.webp', 'voice': 'F1',
         'suspicion': 'Bị cụ mắng trước cả phường sáng hôm ấy; người dâng chén trà sen.'},
        {'id': 'toan', 'name': 'Đỗ Trọng Toàn', 'age': 52, 'role': 'Quản lý tài chính phường', 'image': 'images/id-toan.webp', 'voice': 'M3',
         'suspicion': 'Giữ tiền tài trợ mua nhạc cụ của Sở Văn hoá; có lời ra tiếng vào về khoản ấy.'},
        {'id': 'loc', 'name': 'Phan Bá Lộc', 'age': 42, 'role': 'Con trai nạn nhân, buôn đồ cổ', 'image': 'images/id-loc.webp', 'voice': 'M2',
         'suspicion': 'Muốn bán cây đàn gia bảo cho người Hồng Kông, bị bố đuổi khỏi nhà.'}],
    'aiInterrogation': True,
    'audio': {'intro': 'audio/intro.mp3', 'finale': 'audio/finale.mp3'},
    'documents': D,
    'questions': Q,
    'beats': [
        {'stage': 2, 'kicker': 'Ngày 1–2/10/1993 · Đình Hoa Nguyệt', 'title': 'Chiếc phím sừng', 'voice': 'audio/beat-2.mp3',
         'paragraphs': ['Chén trà sen vô tội. Chất độc đã vào miệng cụ Cửu bằng một đường khác.',
                        'Đại uý Kiên mở cuốn sổ tay học đàn của đào nương, gửi chiếc phím sừng đi hoá nghiệm, và ngồi xuống quán nước của bà Mùi ở cổng đình.',
                        'Ai đã vào buồng hoá trang khi cụ Cửu đang thắp hương?']},
        {'stage': 3, 'kicker': 'Ngày 2–3/10/1993 · Phố Bắc Hoà', 'title': 'Năm phút trong buồng hoá trang', 'voice': 'audio/beat-3.mp3',
         'paragraphs': ['Ông thủ từ nhớ rõ ai đứng ở tiền đình, ai rời đi. Người học trò mười lăm năm xin được khai lại.',
                        'Ở phố Bắc Hoà, một hiệu thuốc bắc còn giữ sổ bán hàng.',
                        'Chiếc phím còn khô lúc nào, và ai cầm nó sau đó?']},
        {'stage': 4, 'kicker': 'Ngày 4/10/1993', 'title': 'Ngăn đáy chiếc tráp', 'voice': 'audio/beat-4.mp3',
         'paragraphs': ['Dưới lớp nhung đỏ của chiếc tráp đàn, có một lá thư chưa kịp gửi.',
                        'Chỉ mặt thủ phạm. Và giải thích vì sao.']}],
    'finale': {'title': 'Tiếng đàn đáy Phố Hiến',
               'paragraphs': ['Đỗ Trọng Toàn khai nhận ngày 5/10/1993, khi túi gấm thêu chữ Thọ được đặt cạnh lá thư nháp của cụ Cửu.',
                              'Ba triệu đồng tiền tài trợ, ông mua một bộ nhạc cụ chín trăm nghìn, ghi hoá đơn gần ba triệu. Cụ Cửu chỉ cần chạm vào sợi dây nilon là biết.',
                              'Cả phường biết thói quen của cụ: ngậm phím cho sừng ấm trước khi dạo đàn. Ông Toàn mua hai mươi gam mã tiền, trộn với mật ong cho dính, cho bớt đắng.',
                              'Bảy giờ bốn mươi hai, ông nói đi lấy sổ công đức. Ông không biết, năm phút trước đó, một người học trò vừa đặt chiếc phím xuống, khô và xỉn như mọi ngày.',
                              'Ông chỉ nói một câu: "Tôi tưởng ai cũng sẽ nhìn vào chén trà."',
                              'Đêm rằm năm sau, Chu Văn Bình ngồi lên chiếu hoa ở đình Hoa Nguyệt, gảy trọn khúc "Lạc Nhạn" bằng cây đàn của thầy.']},
    'epilogue': [
        {'title': 'Đỗ Trọng Toàn', 'text': 'Bị truy tố về tội giết người và tham ô tài sản. Bộ nhạc cụ khống được trả lại hiệu Hàng Gai.'},
        {'title': 'Chu Văn Bình', 'text': 'Được phường bầu thay thầy cầm đàn chính ở hội diễn tỉnh năm 1994.'},
        {'title': 'Nguyễn Thị Ánh Tuyết', 'text': 'Vẫn hát ở phường Kim Nguyệt. Mỗi rằm tháng Tám, chị dâng một chén trà sen trước bàn thờ thầy.'},
        {'title': 'Phan Bá Lộc', 'text': 'Không bán cây đàn. Ông gửi nó lại cho phường, theo lời bố.'}],
}

for person in [case['victim'], *case['suspects']]:
    if person.get('image') and not os.path.exists(f'public/cases/{CID}/' + person['image']):
        print('chưa có ảnh:', person['image']); del person['image']
if case['cover'] and not os.path.exists(f'public/cases/{CID}/' + case['cover']):
    print('chưa có ảnh:', case['cover']); case['cover'] = None
json.dump(case, open(f'public/cases/{CID}/case.json', 'w'), ensure_ascii=False, indent=2)
open(f'public/cases/{CID}/case.json', 'a').write('\n')
print(len(D), 'docs', len(Q), 'questions')
