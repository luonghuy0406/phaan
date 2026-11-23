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
| `documents` | Document[] | mục 2 |
| `questions` | Question[] | mục 3 |
| `finale` | `{ title, paragraphs[] }` | kể lại toàn bộ sự thật sau khi phá án |
| `epilogue` | `{ title, text }[]` | tuỳ chọn, "sau khi hồ sơ khép lại": số phận từng nhân vật |

Định dạng chữ cho phép: `**đậm**`, `__gạch chân__`, `~~gạch xoá~~`. **Không dùng thẻ HTML.**
Có thể nhắc tài liệu bằng mã, ví dụ `(d12)`: người chơi sẽ thấy "(Tài liệu 12)" theo đúng số hiển thị.

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
| `scan` | `image` (bản chụp cả trang tài liệu đã dàn trang sẵn), `imageHi`, `caption` |

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
```json
{ "type": "choice", "options": ["A…", "B…"], "answer": [1], "multiple": false,
  "nudges": { "0": { "message": "Vì sao A sai…" } } }
```

Ví dụ đầy đủ: `public/cases/con-nuoc-ram-thang-gieng/case.json` (5 vòng, 26 tài liệu).
