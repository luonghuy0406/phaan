# Kế hoạch nâng cấp hồ sơ lên mức "hồ sơ chủ lực"

Mục tiêu: mỗi hồ sơ đạt độ chi tiết, độ khó và lượng tài nguyên tương đương hồ sơ 01 của DOSSIER
(pha-an.netlify.app/game, phân tích ngày 27/11/2026): khoảng 30 tài liệu, khoảng 35–50 nghìn ký tự,
nhiều lớp sự thật, câu hỏi không tự lộ đáp án, có âm thanh và giọng dẫn chuyện.

Hồ sơ làm đầu tiên: **`con-nuoc-ram-thang-gieng`** (Con nước Rằm tháng Giêng). Làm xong hồ sơ này thì
dùng nó làm khuôn cho 16 hồ sơ còn lại.

---

## 1. Chuẩn "hồ sơ chủ lực"

| Hạng mục | Chuẩn | DOSSIER vụ 01 | `con-nuoc` trước nâng cấp |
|---|---|---|---|
| Số tài liệu | 30–36 | 29 | 26 |
| Chữ trong tài liệu | 35–50 nghìn ký tự | ~33 nghìn | ~34 nghìn |
| Số trọng điểm | 5 | 3 + câu mở đầu | 5 |
| Số câu hỏi | 8–12 | 4 + 3 câu đối chất | 6 (sau nâng cấp: 12) |
| Gợi ý mỗi câu | đủ 3, tăng dần | 1–3 | 2–3 |
| Lời giải mỗi câu | 3 ý `{title, body[]}` | có | chuỗi trơn (không hiện được) |
| Nghi phạm vô tội | mỗi người ≥ 1 tài liệu gỡ tội + 1 chi tiết đáng ngờ thật | có | thiếu cho Lành, Nguyệt |
| Lớp sự thật | ≥ 3 (cơ chế, người ra tay, động cơ/chuẩn bị, bi kịch) | 3 | 2 |
| Âm thanh | hiệu ứng thao tác + nền theo bối cảnh | có | không |
| Giọng đọc | lời dẫn mở đầu, chuyển cảnh mỗi vòng, kết thúc | có (1 giọng) | không |
| Đoạn chuyển cảnh giữa các vòng | có | có (`BEATS`) | không |

## 2. Nguyên tắc viết câu hỏi (rút từ DOSSIER và `docs/danh-gia-do-kho.md`)

1. Tiêu đề và đề bài chỉ **đặt vấn đề**, không nêu kết luận, không tả tài liệu đáp án.
2. Ba gợi ý tăng dần: hướng nghĩ → loại tài liệu / chi tiết cần so → gần như nói đáp án (chỉ gợi ý 3 được nêu mã tài liệu).
3. Dùng **điều kiện kép** ("có kỹ năng **và** không có ngoại phạm", "bị bác bởi tài liệu **và** mâu thuẫn về giờ") để không đoán bừa được.
4. Có ít nhất một chuỗi **đối chất**: đưa ra một câu khai, người chơi tìm tài liệu bác bỏ.
5. Các phương án của câu cuối dài ngang nhau, chỉ khác ở chi tiết suy ra từ tài liệu.
6. Mọi câu đều giải được chỉ bằng tài liệu đang mở ở vòng đó (quy tắc 4 trong `AGENTS.md`).
7. `nudges` cho các lựa chọn sai phổ biến: nói vì sao sai, không nói đáp án.

## 3. Việc cho `con-nuoc-ram-thang-gieng`

### 3.1 Sửa mâu thuẫn hiện có
- [x] Câu 1: phương án đúng ghi "then sắt cài từ bên ngoài", trái với d02/d03 (then gỗ lim cài bên trong).
- [x] Lời giải câu 2 ghi đỉnh triều 01h30, trái với bản tin thủy văn (22h40–23h30).
- [x] Lời giải câu 4 nói "dây curoa cũ bị cắt khía", "ghi sẵn từ chập tối", trái với d17, d21, d22.
- [x] Câu 5 và câu 6 ghi "kìm mỏ lết", "thuốc mê", "then ngoài", trái với tài liệu (kìm mỏ quạ, mã tiền, then trong).
- [x] Lời giải dạng chuỗi trơn không hiện trên engine: chuyển sang `{title, body[]}`.
- [x] Lời khai Nguyệt "đi đò về lúc 22h15" lệch sổ đò (chuyến về Tân Mỹ lúc 22h30).
- [x] Lời khai Hưng (d12) gần như gọi tên hung thủ ngay vòng 2: làm mềm lại.
- [x] `bible.md` lệch mã tài liệu với `case.json`: viết lại bản đồ manh mối theo mã mới.

### 3.2 Thêm chiều sâu (tài liệu mới)
- [x] Vòng 1: biên bản thu giữ trong phòng bà Lành (thuốc an thần, túi đồ gói sẵn, rút sổ tiết kiệm): nghi phạm giả.
- [x] Vòng 3: kết quả xét nghiệm bổ sung (không có thuốc an thần, nồng độ cồn thấp) → gỡ nghi cho bà Lành.
- [x] Vòng 2: lời khai bổ sung của Tư Lợi về van lù và người được thuê lặn kiểm tra van tháng Chạp.
- [x] Vòng 2: thêm ba thợ hút cát của Ba Thầu vào biên bản bắt sới gà (gỡ nghi cho nhóm thợ lặn khác).
- [x] Vòng 3: xác nhận của sư cô chùa Phước Quang về Nguyệt (giờ rời chùa, sợ nước).
- [x] Vòng 3: lời khai bổ sung của bà Lành (kế hoạch bỏ đi Cần Thơ, câu ông Kiên nói lúc ăn cơm tối).
- [x] Vòng 4: biên bản thực nghiệm điều tra bơi theo con nước 120 m.
- [x] Vòng 4: biên bản ghi lời khai lần 2 của Ba Thuyền (đối chất).
- [x] Vòng 5: giấy nhận lại tiền đặt cọc của Ba Thầu cát, ký chiều 12/2.
- [x] Vòng 5: mảnh thư viết dở của ông Kiên gửi Ba Thuyền, thu trong hộp thiếc ở khoang ghe.

### 3.3 Câu hỏi mới (12 câu, 5 vòng)
- [x] V1 · `choice`: tính chất cái chết (4 phương án dài ngang nhau).
- [x] V2 · `evidence` 3: nước vào từ đâu, lúc nào, vì sao nạn nhân không thoát.
- [x] V2 · `choice` nhiều đáp án: ai có ngoại phạm kín trong khung 22h40–23h30.
- [x] V3 · `line`: câu khai mâu thuẫn với quy luật con nước.
- [x] V3 · `evidence` 2: chứng minh người lái đò rời đò trong lúc "sửa máy".
- [x] V3 · `evidence` 2: hai tài liệu khách quan giải thích thuốc an thần và túi đồ của bà Lành.
- [x] V4 · đối chất 1 (`evidence` 1): "dây curoa đứt, tôi quăng xuống sông".
- [x] V4 · đối chất 2 (`evidence` 1): "rượu rễ nhàu tôi tự ngâm, lành tính".
- [x] V4 · đối chất 3 (`line`): câu khai bị biên bản thực nghiệm bác.
- [x] V5 · `choice`: kết luận toàn diện (4 phương án chỉ khác chi tiết).
- [x] V5 · `choice`: bi kịch: nếu ông Kiên sống tới sáng 16 tháng Giêng thì mảnh vườn dừa ra sao.

### 3.4 Âm thanh và giọng đọc
- [x] Engine: module hiệu ứng `src/lib/sfx.ts` (WebAudio, mở khoá ở lần chạm đầu cho iPad).
- [x] Engine: âm thanh khi mở tài liệu, ghim, đúng (đóng dấu), sai, gợi ý, mở niêm phong, kết thúc.
- [x] Engine: nhạc / tiếng nền theo hồ sơ (`audio.ambient` trong `case.json`), tự nhỏ lại khi đang đọc giọng.
- [x] Engine: đoạn chuyển cảnh khi mở vòng mới (`beats` trong `case.json`), có nút nghe giọng dẫn.
- [x] Engine: nút nghe lời dẫn ở màn mở đầu và màn kết thúc.
- [x] Cài đặt: bật/tắt hiệu ứng, bật/tắt tiếng nền, âm lượng.
- [x] PWA: lưu đệm file `.mp3` (CacheFirst) để chơi được khi mất mạng.
- [x] Engine: hiện được lời giải viết dạng chuỗi trơn (16 hồ sơ cũ trước đây không hiện lời giải).
- [x] Công cụ `tools/gen-voice.mjs`: tạo sẵn giọng đọc từ `authoring/<id>/voice.json`, hai bộ máy: **VieNeu-TTS v3 Turbo** (mặc định cho hồ sơ này) và Supertonic 3.
- [x] Kịch bản giọng đọc `authoring/con-nuoc-ram-thang-gieng/voice.json` (dẫn chuyện + vai nhân vật).
- [x] Tạo file giọng đọc vào `public/cases/con-nuoc-ram-thang-gieng/audio/`.
- [x] Hiệu ứng dùng chung trong `public/sfx/` (Kenney, CC0) và tiếng nền sông nước (BigSoundBank, CC0).
- [x] Ghi nguồn và giấy phép trong `public/sfx/CREDITS.md`.
- [ ] Nghe lại toàn bộ giọng đọc trên iPad, sửa chữ khó đọc trong `voice.json`, chạy lại `npm run gen-voice`.
- [x] Đọc tài liệu (nút loa, "Đọc đoạn này") dùng file VieNeu tạo sẵn theo từng khối (`npm run gen-doc-voice`), lời khai đọc phân vai; trước đây đọc trực tiếp bằng Supertonic trên trình duyệt nên bị khựng.
- [x] Chuyển sang VieNeu-TTS v3 Turbo: giọng miền Nam cho nhân vật Bến Tre (Đức Trí, Minh Triết, Thái Sơn), nhịp tự nhiên hơn, 48 kHz, hỗ trợ tag `[thở dài]`.
- [ ] (Tuỳ chọn) Thử airy.so/studio cho các câu cần diễn cảm mạnh (cần tài khoản, tải tay vào `public/cases/<id>/audio/`).

### 3.5 Hình ảnh
- [x] Tờ "Hồ sơ nhân thân" (d00, loại `people`) đặt đầu bàn vòng 1: ảnh thẻ nạn nhân + 6 nghi phạm, có giọng đọc.
- [x] Ảnh thẻ 6 nghi phạm + nạn nhân (FLUX.1 Krea qua Hugging Face MCP), thẻ nghi phạm ở màn mở đầu, nút "Nghi phạm", câu 3 và câu "Chỉ mặt hung thủ" chọn bằng thẻ ảnh.
- [ ] Ảnh cho 9 tài liệu mới chưa bắt buộc (đều là giấy tờ có chữ). Nên có thêm:
  - [ ] Ảnh tang vật: vỉ thuốc an thần và túi đồ trong phòng bà Lành.
  - [ ] Ảnh mảnh thư viết dở trong hộp thiếc (dạng `scan`, chữ nhoè nước).
  - [ ] Sơ đồ thực nghiệm bơi 120 m theo con nước (vẽ bằng code như `authoring/draw_misc_images.py`).
- [ ] Prompt ảnh ghi vào `authoring/con-nuoc-ram-thang-gieng/image-prompts.md`.

### 3.5b Thẩm vấn bằng AI (bước 1 của tích hợp AI)
- [x] Hồ sơ thẩm vấn 6 nghi phạm (`authoring/con-nuoc-ram-thang-gieng/interrogation.json`): tính cách, điều biết, lời nói dối, điều kiện khai nhận.
- [x] Lõi dùng chung `supabase/functions/_shared/` (luật khai nhận do máy chủ quyết định, prompt, xoay vòng Gemini/Groq/OpenRouter) + 12 unit test.
- [x] Edge Function `interrogate`, migration `20261127000000_ai_interrogation.sql` (hạn mức lượt hỏi/ngày, lịch sử theo người chơi).
- [x] Màn "Phòng thẩm vấn" mở từ nút "Thẩm vấn" trong hộp Nghi phạm; đưa tài liệu đang mở lên bàn.
- [x] Bỏ chi tiết lộ hung thủ ở vòng 1 (thẻ Ba Thuyền không còn "thợ lặn"/"biếu rượu"; lời khai bà Lành không còn nêu người biếu rượu); Lành là nghi phạm 01, Ba Thuyền 03.
- [x] Áp migration, đẩy hàm, đặt 3 khoá AI trong Supabase Secrets, chạy `npm run sync-cases`.
- [x] Đăng nhập ẩn danh cho thẩm vấn (không cần email/SMTP).
- [x] Hộp Nghi phạm thiết kế lại: ảnh, tên, lý do nghi vấn trong cùng một ô; nút "Thẩm vấn" đỏ chiếm đáy ô.
- [x] Phòng thẩm vấn: cao cố định, chỉ phần chat cuộn; đặt tối đa 3 tài liệu một lần; mở sổ tay bên cạnh; bôi chọn đoạn khai để ghi vào sổ; nút "Ghi cả câu".
- [x] Giọng nghi phạm đọc ngay trên thiết bị bằng Supertonic (không dùng API đám mây): mỗi nghi phạm một giọng (`voice` trong `suspects`), 6 bước khử nhiễu, đoạn đầu ngắn để giọng bắt đầu sớm, nạp và biên dịch sẵn khi mở phòng. Edge Function `voice-line` (Gemini TTS) không còn dùng.
- [x] Tối ưu ONNX Runtime: bản fp16 cho WebGPU (200 MB, latent giữ trên GPU giữa các bước), bản int8 cho CPU (186 MB), cô lập cross-origin để WebAssembly chạy 4 luồng (`tools/optimize-supertonic.py`).
- [ ] Đăng thư mục fp16/ + int8/ lên một nơi có CORS (đề xuất Hugging Face) và đặt `VITE_TTS_MODEL_OPT_BASE` trên Vercel.
- [ ] Chơi thử thẩm vấn cả 6 nghi phạm; bộ câu hỏi "tấn công" (đòi lộ hung thủ, đổi vai) để kiểm tra rào chắn.

### 3.5c Giấu hung thủ lâu hơn (28/11/2026)

- [x] Bỏ "thợ lặn sông" và chuyện ve rượu biếu khỏi lời khai Ba Thuyền ở vòng 3 (d18).
- [x] Tư Lợi (d13) không còn nêu tên người lặn thay ron, không tự gỡ tội; Hưng (d14) không nêu tên người nợ.
- [x] Vòng 4 thêm sổ chi tháng Chạp (d36: Ba Thuyền được thuê lặn tháo van) và phiếu khám tai của Tư Lợi (d37); ve rượu có dấu vân tay Ba Thuyền (d28).
- [x] Câu hỏi mới q-loi: gỡ nghi cho Tư Lợi bằng d37. Tư Lợi là nghi phạm giả tới vòng 4.
- [x] Thẩm vấn AI chặn theo vòng: `knows`/`lies` có `stage`; máy chủ nhận vòng đang mở, bỏ điều chưa tới vòng khỏi lời dặn model, từ chối tài liệu của vòng sau (DOC_LOCKED).
- [ ] Vòng do trình duyệt gửi lên, người chơi cố tình sửa được; chấp nhận vì không có lợi gì ngoài tự làm hỏng trò chơi.

### 3.5d Báo cáo kết luận trước kiểm sát viên (AI)

- [x] Câu q11 có `exam`: kiểm sát viên hỏi lần lượt 5 ý (hung thủ và căn cứ, vì sao không thoát, nước vào bằng đường nào, vì sao đúng giờ đó, động cơ); điều tra viên gõ câu trả lời.
- [x] Đáp án `authoring/con-nuoc-ram-thang-gieng/conclusion.json` (chỉ trên máy chủ). AI chấm ý nào đã nói; máy chủ chỉ công nhận khi câu trả lời có từ khoá của ý đó, và tự chọn câu hỏi gặng. Trả lời trái hồ sơ tính như một lần sai; sai hai lần ở một ý thì hiện gợi ý.
- [x] Edge Function `conclude`, bảng `exam_state`. Đã thử thật: dụ AI "chấm đạt hết" không qua; 5 ý hoàn tất, mỗi lượt 2–4 giây.
- [x] Không đăng nhập được, hết lượt AI hoặc chơi nhóm: dùng lại phần trắc nghiệm.

### 3.6 Kiểm định
- [x] `npm run validate` không lỗi.
- [x] `npm test`, `npm run build` qua.
- [x] Chạy thử trên Chrome: nút nghe ở màn mở đầu, màn chuyển cảnh vòng 2 tự đọc, mục Âm thanh trong Cài đặt.
- [ ] Nén ảnh cũ của hồ sơ (cover, d01, d02, d04, d05 đang 2,5–3,8 MB, nên < 400 KB).
- [ ] Chạy `npm run sync-cases` để nạp đáp án mới lên Supabase (cần `SUPABASE_SECRET_KEY`, bạn tự chạy).
- [ ] Chơi thử từ đầu đến cuối trên iPad, bấm giờ (mục tiêu 90–120 phút), ghi lại chỗ kẹt.
- [ ] Nhờ một người chưa biết đáp án chơi thử; với mỗi vòng, kiểm tra giải được chỉ bằng tài liệu đang mở.
- [ ] Lưu ý: đổi cấu trúc nên người đang chơi dở hồ sơ này sẽ phải bắt đầu lại (quy tắc 8).

## 4. Quy trình cho các hồ sơ tiếp theo

Thứ tự đề xuất (theo `docs/danh-gia-do-kho.md` và độ dày hiện có): `mua-dong-binh-ty` → `quai-vat-21-khuon-mat`
→ `gac-den-hon-dau` → `chuyen-tau-dem-muong-man` → các hồ sơ 15–17 tài liệu.

Với mỗi hồ sơ:
- [ ] Đọc `bible.md` và `case.json`, lập bảng mâu thuẫn giữa câu hỏi, lời giải và tài liệu.
- [ ] Viết lại dòng thời gian theo phút; mỗi nghi phạm có động cơ, cơ hội, một lời khai và một tài liệu gỡ tội.
- [ ] Thêm 8–12 tài liệu để đạt 30–36; thêm ít nhất 1 lớp sự thật (chuẩn bị trước, người giúp sức hoặc bi kịch).
- [ ] Viết lại câu hỏi theo mục 2; đủ 3 gợi ý và lời giải 3 ý.
- [ ] Viết `beats` (1 đoạn chuyển cảnh mỗi vòng) và `audio` trong `case.json`.
- [ ] Viết `authoring/<id>/voice.json`, chạy `npm run gen-voice -- <id>`.
- [ ] Chọn tiếng nền hợp bối cảnh (phố, mưa, tàu đêm, gió núi…), ghi nguồn vào `public/sfx/CREDITS.md`.
- [ ] `npm run validate`, `npm test`, `npm run build`, `npm run sync-cases`, chơi thử.

## 5. Tài nguyên âm thanh

| Nguồn | Giấy phép | Dùng cho |
|---|---|---|
| Kenney: RPG Audio, Interface Sounds, Impact Sounds (kenney.nl) | CC0 | lật giấy, đóng dấu, báo sai, cào bút, mở phong bì |
| BigSoundBank (bigsoundbank.com) | CC0 | mưa, côn trùng đêm, ếch nhái, sóng vỗ, máy dầu, chuông chùa, dưới nước, tim đập |
| VieNeu-TTS v3 Turbo (pnnbao97, chạy trên máy) | Apache-2.0 | giọng dẫn chuyện và vai nhân vật (mặc định) |
| Supertonic 3 (Supertone, chạy trên máy) | OpenRAIL-M (xem `~/.cache/supertonic3/LICENSE`) | bộ máy dự phòng |

Tìm thêm khi cần: Kenney (gói Audio), BigSoundBank (mục Atmosphere), Wikimedia Commons (chỉ lấy file CC0 / public domain),
OpenGameArt (lọc CC0). Không dùng Freesound file CC-BY-NC.

## 6. Lệnh

```bash
python3 -m venv ~/.venvs/vieneu && ~/.venvs/vieneu/bin/pip install vieneu   # một lần, cho VieNeu
npm i --no-save onnxruntime-node@1.22.0     # chỉ khi dùng engine supertonic
npm run gen-voice -- con-nuoc-ram-thang-gieng          # tạo clip mới hoặc đã đổi chữ
npm run gen-voice -- con-nuoc-ram-thang-gieng beat-3 --force   # tạo lại một clip
npm run validate && npm test && npm run build
npm run sync-cases                           # sau khi đổi câu hỏi / đáp án
```
