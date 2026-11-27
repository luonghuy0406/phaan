# Nguồn âm thanh

Mọi tệp dưới đây đều dùng giấy phép **CC0 1.0** (không bắt buộc ghi công, được dùng thương mại).
Tệp gốc đã được cắt, trộn và chuyển sang MP3 mono bằng ffmpeg.

## Hiệu ứng dùng chung (`public/sfx/`)

| Tệp | Nguồn | Tệp gốc |
|---|---|---|
| `paper.mp3` | Kenney, RPG Audio (kenney.nl/assets/rpg-audio) | `bookFlip2.ogg` |
| `pin.mp3` | Kenney, RPG Audio | `metalClick.ogg` |
| `stamp.mp3` | Kenney, Impact Sounds (kenney.nl/assets/impact-sounds) | `impactWood_heavy_002.ogg` + `impactPunch_heavy_001.ogg` |
| `wrong.mp3` | Kenney, Impact Sounds + Interface Sounds (kenney.nl/assets/interface-sounds) | `impactSoft_heavy_001.ogg` + `error_006.ogg` |
| `pencil.mp3` | Kenney, Interface Sounds | `scratch_001.ogg`, `scratch_003.ogg`, `scratch_005.ogg` |
| `unseal.mp3` | Kenney, RPG Audio | `cloth3.ogg` + `bookOpen.ogg` |
| `tick.mp3` | Kenney, Interface Sounds | `tick_002.ogg` |
| `gong.mp3` | Joseph Sardin, BigSoundBank.com | "Gong sweet" (#1482) |

## Tiếng nền hồ sơ

`cases/con-nuoc-ram-thang-gieng/audio/ambient.mp3`: trộn từ BigSoundBank.com (Joseph Sardin):
"Rain on plastic tarpaulin" (#1292), "Pontoon marina" (#1444), "Song of nocturnal insect 1" (#424), "Frogs 1" (#997).

## Giọng đọc

`cases/*/audio/intro.mp3`, `beat-*.mp3`, `finale.mp3`: tạo bằng **VieNeu-TTS v3 Turbo** (Phạm Nguyễn Ngọc Bảo,
github.com/pnnbao97/VieNeu-TTS, mô hình huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo, giấy phép Apache-2.0),
chạy trên máy bằng `tools/gen-voice.mjs` + `tools/vieneu-synth.py` từ kịch bản `authoring/<id>/voice.json`.
Giọng dựng sẵn: Thiện Minh (dẫn chuyện), Minh Triết, Đức Trí, Adam, Thái Sơn.
`cases/*/audio/read/**`: giọng đọc tài liệu, cùng engine, tạo bằng `tools/gen-doc-voice.mjs`; thêm giọng Thục Đoan, Kim Thanh, Mỹ Duyên.

Additional sounds: Joseph SARDIN - BigSoundBank.com · Kenney (www.kenney.nl)
