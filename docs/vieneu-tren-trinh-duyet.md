# Thử nghiệm: chạy VieNeu-TTS v3 Turbo trong trình duyệt (onnxruntime-web)

Ngày 28/11/2026. Máy đo: Mac (Apple GPU Metal 3, 10 nhân), Chrome, trang đã cô lập cross-origin (WebAssembly 4 luồng).
Mô hình: `pnnbao-ump/VieNeu-TTS-v3-Turbo` (onnx_update, fp32) + `OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano-ONNX`.

## Cấu trúc một lần đọc (đo bằng bản Python gốc, câu 9 giây âm thanh)

| Bước | Số lần gọi | Python/CPU | Ghi chú |
|---|---|---|---|
| `vieneu_prefill` | 1 | 43 ms | dùng chung 396 MB trọng số với `decode_step` |
| `vieneu_decode_step` (12 tầng, KV cache) | 111 (12,5 khung/giây) | 7,5 ms/lần | |
| `vieneu_acoustic_cached` (1 tầng, ~1,7 triệu tham số) | 1.792 (16 kênh × khung) | 0,17 ms/lần | phụ thuộc tuần tự: kênh sau cần mã kênh trước |
| logits + lấy mẫu (numpy, ma trận 16 × 1024 × 768) | | 0,20 s tổng | |
| `moss_audio_tokenizer_decode_full` | 1 | 379 ms | có bản `decode_step` để giải mã nối tiếp |
| **Tổng** | | **1,77 s** | RTF 0,20 |

## Đo trong trình duyệt (dữ liệu giả, đúng kích thước)

| Bước | WebAssembly ×4 | WebGPU | Tốt nhất |
|---|---|---|---|
| `decode_step` | 28 ms | 30 ms; **12,2 ms** khi giữ KV cache trên GPU (`preferredOutputLocation: 'gpu-buffer'`) | WebGPU + KV trên GPU: ~1,4 s/câu |
| `acoustic` | 2,2 ms | 6,2 ms | **WebAssembly 1 luồng trong worker riêng: 0,94 ms** → ~1,7 s/câu |
| giải mã MOSS (112 khung) | 758 ms | **249 ms** | WebGPU |
| logits bằng JS thuần | 950 ms/câu | | nên đưa vào đồ thị `acoustic` (Gather theo kênh + MatMul) |

**Ước tính tốt nhất trên Mac:** khoảng 3,5–4 s cho 9 s âm thanh (RTF ≈ 0,4). iPad có thể chậm hơn 1,5–2 lần (RTF ≈ 0,6–0,8),
chưa đo. Các bước nối tiếp nhau theo từng khung (không chạy song song được), nên phải phát dần bằng bộ giải mã nối tiếp
của MOSS để giọng bắt đầu sau khoảng 1 giây.

## Việc phải làm nếu đi tiếp

1. Viết lại vòng sinh (~600 dòng Python trong `onnx_runtime_lite.py`) bằng TypeScript: dựng prompt, nhúng (embedding) từ
   `vieneu_v3_heads.npz` (chuyển sang file nhị phân), lấy mẫu top-k/top-p, phạt lặp, chặn "nói lan man" (babble guard).
2. Sửa đồ thị `acoustic` để tự tính logits của kênh hiện tại (bớt 950 ms JS).
3. Biên dịch `sea-g2p` (Rust, Apache-2.0, github.com/pnnbao97/sea-g2p) sang WebAssembly; từ điển 63 MB.
4. Tokenizer (419 ký hiệu âm vị) và giọng dựng sẵn (`vieneu/assets/voices_v3_turbo.json`).
5. Bộ nhớ: `prefill` và `decode_step` mỗi phiên tự nạp 396 MB trọng số → bỏ `prefill`, chạy prompt bằng `decode_step`
   (thêm ~60–100 bước, ~1 s) để chỉ giữ một bản trên GPU.
6. Dung lượng tải: ~580 MB fp32 + 63 MB từ điển (có bản `onnx_int8` của bộ khung để giảm).

## Kết luận

Khả thi về kỹ thuật trên máy mạnh có WebGPU, nhưng chậm hơn Supertonic khoảng 10–15 lần (Supertonic: ~0,25 s/câu),
tải nặng gấp ~3 lần, và cần khoảng 1–2 tuần công để chuyển mã. Chưa rõ có đạt thời gian thực trên iPad.
