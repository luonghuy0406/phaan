# Cấu trúc dữ liệu hồ sơ vụ án (`case.json`)

Mỗi vụ án là một thư mục trong `public/cases/<case-id>/`:

```
public/cases/<case-id>/
  case.json          ← toàn bộ nội dung chơi (bắt buộc)
  images/            ← ảnh .webp (bìa, ảnh hiện trường, tang vật, bản chụp tài liệu…)
  files/             ← (tuỳ chọn) bản gốc cho người chơi tải về: PDF, ảnh khổ lớn
authoring/<case-id>/ ← tài liệu biên soạn, KHÔNG nằm trong public/ nên không lên web
  bible.md           ← kịch bản gốc: sự thật, dòng thời gian, chuỗi manh mối
  image-prompts.md   ← prompt tạo từng ảnh
```

Sau khi thêm hồ sơ, khai báo trong `public/cases/index.json` và chạy `npm run validate`
(hoặc `node tools/validate-case.mjs <case-id>`).

Tiến trình người chơi được lưu theo **cấu trúc** hồ sơ (mã tài liệu, vòng, loại câu hỏi, đáp án). Sửa chữ, sửa chính tả
thì tiến trình được giữ nguyên; thêm, bớt, đánh số lại tài liệu hoặc đổi đáp án thì người chơi bắt đầu lại hồ sơ đó.

## 0. Nhịp vòng khuyến nghị (hồ sơ 90–120 phút)

| Vòng | Tài liệu | Câu hỏi | Mục đích |
|---|---|---|---|
| 1 | 8–10 | `choice` **2 lựa chọn** (ví dụ: tai nạn hay án mạng?) | Làm quen bàn chơi, xác lập vụ án |
| 2 | 7–9 | `evidence` 2 tài liệu | Cơ chế gây án, loại trừ nghi phạm có ngoại phạm |
| 3 | 5–7 | `line` | Bắt lời khai dối |
| 4 | 3 | `evidence` 2–3 tài liệu | Lật màn kịch / chứng cứ chuẩn bị trước |
| 5 | 3 | `choice` 4 phương án | Gọi tên hung thủ, thủ đoạn, động cơ |

Số tài liệu giảm dần, nhưng mỗi vòng sau cần đối chiếu chéo nhiều tài liệu của các vòng trước hơn.
Mỗi câu hỏi có **3 gợi ý** (mơ hồ → chỉ ra chi tiết → gần như nói đáp án) và **lời giải 3 ý**.
Mỗi nghi phạm vô tội cần ít nhất một tài liệu loại trừ, thường đặt ở vòng 2–3.

## 1. Thông tin chung

| Trường | Kiểu | Ghi chú |
|---|---|---|
| `id` | chuỗi | trùng tên thư mục, chỉ `a-z 0-9 -` |
| `no` | số | số thứ tự hiển thị "Hồ sơ 01" |
| `status` | `"available"` \| `"coming-soon"` | |
| `title`, `subtitle`, `tagline` | chuỗi | `tagline` là 1 câu móc câu |
| `difficulty` | 1–5 | |
| `players`, `duration`, `setting`, `era` | chuỗi | ví dụ `"2–6"`, `"90 phút"` |
| `tags` | chuỗi[] | tối đa 3 hiển thị |
| `cover` | chuỗi \| null | `"images/cover.webp"`, tỉ lệ 4:5 |
| `contentWarning` | chuỗi | tuỳ chọn |
| `synopsis` | chuỗi[] | giới thiệu KHÔNG tiết lộ, hiện ở trang chi tiết |
| `intro` | `{ title, paragraphs[], objective }` | hiện khi mở bàn điều tra |
| `tour` | `{ title, text }[]` | tuỳ chọn, 4 bước hướng dẫn lần đầu (bỏ trống = dùng bản mặc định) |
| `beats` | `{ stage, kicker?, title?, paragraphs[], voice? }[]` | tuỳ chọn, đoạn chuyển cảnh hiện khi trọng điểm `stage` (≥ 2) mở; `voice` là clip giọng đọc |
| `suspects` | `{ id, name, alias?, age?, role?, image?, suspicion? }[]` | tuỳ chọn, thẻ ảnh nghi phạm: hiện ở màn mở đầu, nút "Nghi phạm" và câu hỏi có `cards`. `suspicion` chỉ ghi lý do bị nghi lúc mở hồ sơ, không lộ lời giải. Ảnh thẻ 3:4 (480×640 webp) |
| `victim` | như một phần tử `suspects`, thêm `note` | tuỳ chọn, thẻ nạn nhân |
| `audio` | `{ ambient?, intro?, finale? }` | tuỳ chọn, đường dẫn `.mp3` trong thư mục hồ sơ: tiếng nền lặp, lời dẫn mở đầu và kết thúc |
| `documents` | Document[] | mục 2 |
| `questions` | Question[] | mục 3 |
| `finale` | `{ title, paragraphs[] }` | kể lại toàn bộ sự thật sau khi phá án |
| `epilogue` | `{ title, text }[]` | tuỳ chọn, "sau khi hồ sơ khép lại": số phận từng nhân vật |

Định dạng chữ cho phép: `**đậm**`, `__gạch chân__`, `~~gạch xoá~~`. **Không dùng thẻ HTML.**
Có thể nhắc tài liệu bằng mã, ví dụ `(d12)`: người chơi sẽ thấy "(Tài liệu 12)" theo đúng số hiển thị.

**Thể loại (`kind` trong `public/cases/index.json`):** `"fiction"` cho hồ sơ hư cấu, `"true-crime"` cho hồ sơ dựng lại từ vụ án có thật. Trang chủ chia kho hồ sơ theo trường này. Hồ sơ cũ chưa có `kind` được coi là có thật nếu có thẻ "Vụ án có thật".

**Chưa hoàn thiện (`draft` trong `public/cases/index.json`):** đặt `"draft": true` cho hồ sơ đã chơi được nhưng còn thiếu hình ảnh. Thẻ hồ sơ và trang chi tiết sẽ hiện nhãn "Chưa hoàn thiện". Xoá dòng này khi đã đủ ảnh.

## 1b. Âm thanh và giọng đọc

```json
"audio": { "ambient": "audio/ambient.mp3", "intro": "audio/intro.mp3", "finale": "audio/finale.mp3" },
"beats": [
  { "stage": 2, "kicker": "Sáng 14/2/2006 · Công an huyện", "title": "Thứ làm ông nằm yên",
    "paragraphs": ["…", "…", "Câu hỏi treo cho vòng mới (in nghiêng)."], "voice": "audio/beat-2.mp3" }
]
```

- Hiệu ứng thao tác (lật giấy, ghim, đóng dấu đúng/sai, gợi ý, mở niêm phong, kết thúc) có sẵn cho mọi hồ sơ trong `public/sfx/`.
- Tiếng nền nên dài 60–90 giây, lặp liền (đầu và cuối trộn chéo), âm lượng thấp; dưới 1 MB.
- Giọng đọc tạo sẵn bằng `npm run gen-voice -- <case-id>` từ `authoring/<case-id>/voice.json`, chạy trên máy.
  `"engine": "vieneu"` (khuyên dùng, VieNeu-TTS v3 Turbo, giọng dựng sẵn như "Thiện Minh", "Đức Trí"; cài theo đầu `tools/gen-voice.mjs`)
  hoặc `"supertonic"` (giọng F1–F5, M1–M5).
  **Mỗi clip nên lấy chữ thẳng từ `case.json`** để giọng luôn khớp chữ hiển thị:
  `{ "id": "beat-3", "source": "beat:3", "quotes": ["thuyen"] }` (`source`: `intro`, `beat:N`, `finale`).
  Mỗi lời thoại trong ngoặc kép đọc bằng vai kế tiếp trong `quotes` (vai trùng người dẫn thì đọc liền câu);
  phần còn lại do `narrator` (mặc định `dan`) đọc. Sửa chữ trong `case.json` rồi chạy lại lệnh: clip nào đổi chữ sẽ tự tạo lại.
  `npm run gen-voice -- <case-id> --dry` in ra đúng các câu sẽ đọc để đối chiếu.
- **Đọc tài liệu** (nút loa trên tờ giấy, "Đọc đoạn này"): `npm run gen-doc-voice -- <case-id>` tạo sẵn mỗi khối chữ thành
  `audio/read/<doc>/<khoá>.mp3` (cùng khoá với khối trên giấy) và `audio/read/index.json`. Lời khai đọc phân vai theo
  mục `docs` trong `voice.json`: `{ "narrator": "dan", "asker": "danh", "speakers": { "Trần Văn Thuyền": "thuyen" } }`.
  Chỉ khối có chữ thay đổi mới được tạo lại; `--dry` in ra danh sách khối. Thiếu file thì bàn điều tra đọc trực tiếp như cũ
  (Supertonic trên máy, chậm hơn). Tài liệu viết bằng `content` chưa được tạo sẵn.
  Với VieNeu có thể chèn `[thở dài]`, `[cười]`, `[hắng giọng]`.
  Viết số và ký hiệu thành chữ khi dễ đọc sai ("Phước Hải không chín", "một mét tám lăm").
- Mọi nguồn âm thanh phải là CC0 hoặc tự tạo; ghi vào `public/sfx/CREDITS.md`.

## 2. Tài liệu (`documents[]`)

Trường chung: `id` (`"d01"`… theo thứ tự đọc), `stage` (vòng, từ 1), `type`, `title`,
tuỳ chọn `x`, `y`, `width`, `rotate` (0–3), `file` (bản gốc để tải, ví dụ `"files/d01.pdf"`), `imageHi` (ảnh nét hơn, tải khi phóng to).

| `type` | Trường riêng |
|---|---|
| `newspaper` | `masthead`, `issue`, `date`, `headline`, `deck`, `image`, `imageCaption`, `paragraphs[]` |
| `report` | `header[]`, `heading`, `code`, `date`, `fields[{label,value}]`, `sections[{heading, paragraphs[]}]`, `signature` |
| `testimony` | `header[]`, `heading`, `date`, `fields[]`, `lines[{n, text, speaker?}]`, `signature` |
| `photo` | `image`, `caption`, `label` |
| `letter` | `date`, `greeting`, `paragraphs[]`, `signature` |
| `receipt` | `shop`, `address`, `fields[]`, `items[{name, qty, price}]`, `total`, `footer[]` |
| `evidence` | `code`, `image`, `imageCaption`, `fields[]`, `paragraphs[]` |
| `note` | `paragraphs[]`, `signature` (trang sổ tay viết tay) |

**Trình bày giấy tờ.** `report` và `testimony` được in như giấy tờ hành chính:
- đầu trang có cơ quan (`header[]`, kèm `code` thành dòng "Số: …") và quốc hiệu, tiêu ngữ;
- `form` (vd. `"Mẫu số 138"`) in nghiêng ở góc phải;
- `date` bắt đầu bằng chữ số thành dòng "Vào hồi …";
- `fields[]` thành các dòng chấm điền tay bằng mực xanh.

Chữ ký ở cuối trang:
- lấy từ `signers: [{ "role": "Điều tra viên", "name": "Đại uý Lương Minh Khải" }]` (1 hoặc 2 người); nếu không có thì đọc `signature` dạng `"Vai trò: Họ tên"`;
- biên bản có `header` được đóng dấu tròn mang tên cơ quan;
- trong lời khai, `speaker` là người hỏi (Điều tra viên, Cán bộ, Thanh tra…) in thành **Câu hỏi:**, người đáp in thành **Trả lời:**; dòng nằm trọn trong ngoặc đơn in nghiêng như ghi chú.

Hồ sơ diễn ra ở nước ngoài đặt `"nationalHeader": false` ở cấp hồ sơ để không in quốc hiệu Việt Nam.

**Cách viết nhanh: `content`.** Mọi loại tài liệu (trừ `scan`) đều có thể dùng một chuỗi `content` thay cho các trường cấu trúc ở trên:
- dòng trống ngăn đoạn;
- dòng bắt đầu bằng `- ` hoặc `1. ` thành danh sách (thụt ≥ 2 dấu cách là mục con);
- `**...**` in đậm.

Nếu dòng đầu tiên chỉ gồm chữ đậm (`**BIÊN BẢN KHÁM NGHIỆM**`), dòng đó thành tiêu đề của tờ giấy. Với `newspaper`, `report`, `testimony` và `receipt`, tiêu đề này chỉ được dùng khi chưa đặt `headline`, `heading` hoặc `shop`.

Nên ưu tiên các trường cấu trúc. Lời khai vẫn phải dùng `lines[]` để câu hỏi loại `line` trỏ được tới số dòng.
| `scan` | `image` (bản chụp cả trang tài liệu đã dàn trang sẵn), `imageHi`, `caption` |
| `people` | `paragraphs[]` tuỳ chọn. Tờ "Hồ sơ nhân thân": tự lấy ảnh thẻ, tên, tuổi, vai trò và lý do bị nghi từ `victim` + `suspects`; mỗi người là một khối `pp0`, `pp1`… (tô, nối dây, đọc được) |

- Ưu tiên các loại có chữ (report, testimony…): người chơi tô, trích dẫn, nối dây được từng đoạn. Chỉ dùng `scan` cho tài liệu
  đã được thiết kế sẵn thành ảnh (bản đồ, sơ đồ, giấy tờ viết tay phức tạp). Trên `scan` người chơi vẫn viết tay bằng bút được.
- Ảnh `scan`: rộng 1400px, `imageHi` rộng 2400px, cùng tỉ lệ.
- Dòng lời khai tham chiếu dạng `"<docId>:<NNN>"`, ví dụ `"d16:007"`.

## 3. Câu hỏi (`questions[]`)

Câu hỏi được giải **theo thứ tự**. Tài liệu vòng N chỉ hiện khi mọi câu hỏi có `stage < N` đã giải.

Trường chung: `id`, `stage`, `type`, `title`, `prompt`, `answer`, `hints[]` (3 gợi ý), `solved`, `wrong` (tuỳ chọn),
`explanation[{title, body[]}]` (3 ý).

### `evidence`
```json
{ "type": "evidence", "need": 2, "answer": ["d09", "d10"],
  "nudges": [
    { "picks": ["d09", "d11"], "near": true, "message": "Gần đúng…" },
    { "any": ["d13", "d15"], "message": "Tài liệu này là chứng cứ ngoại phạm…" } ] }
```

### `line`
```json
{ "type": "line", "answer": ["d16:007"], "nudges": { "d16:006": { "near": true, "message": "…" } } }
```

### `choice`
Thêm `"cards": ["lanh", "hung", …]` (id trong `suspects`, cùng thứ tự `options`) để người chơi chọn bằng thẻ ảnh thay vì chữ.
```json
{ "type": "choice", "options": ["A…", "B…"], "answer": [1], "multiple": false,
  "nudges": { "0": { "message": "Vì sao A sai…" } } }
```

Ví dụ đầy đủ: `public/cases/con-nuoc-ram-thang-gieng/case.json` (5 vòng, 35 tài liệu, 12 câu hỏi, có `beats` và `audio`).
