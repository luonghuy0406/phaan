#!/usr/bin/env python3
"""Backend VieNeu-TTS cho tools/gen-voice.mjs (https://github.com/pnnbao97/VieNeu-TTS, Apache-2.0).

Đọc từ stdin một JSON: {"out_dir": "...", "segments": [{"voice": "Thái Sơn", "text": "..."}, ...]}
Ghi mỗi đoạn thành <out_dir>/<i>.wav (mono, 48 kHz) và in ra JSON {"sample_rate": 48000, "files": [...]}.

Cài (một lần, môi trường riêng, không đụng tới dự án):
    python3 -m venv ~/.venvs/vieneu && ~/.venvs/vieneu/bin/pip install vieneu
rồi đặt VIENEU_PYTHON=~/.venvs/vieneu/bin/python khi chạy npm run gen-voice.
Lần đầu chạy, SDK tự tải mô hình VieNeu-TTS v3 Turbo vào ~/.cache/huggingface.
"""
import json
import os
import sys

try:
    from vieneu import Vieneu
except ImportError:
    sys.stderr.write("Thiếu gói vieneu. Cài: python3 -m venv ~/.venvs/vieneu && ~/.venvs/vieneu/bin/pip install vieneu\n")
    sys.exit(3)


def main() -> None:
    job = json.load(sys.stdin)
    out_dir = job["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    tts = Vieneu()
    known = {vid for _label, vid in tts.list_preset_voices()}
    files = []
    for i, seg in enumerate(job["segments"]):
        voice = seg.get("voice") or "Hải Đăng"
        if voice not in known:
            sys.stderr.write(f"Không có giọng '{voice}'. Các giọng có sẵn: {', '.join(sorted(known))}\n")
            sys.exit(4)
        audio = tts.infer(seg["text"], voice=voice, temperature=float(seg.get("temperature", 0.8)))
        path = os.path.join(out_dir, f"{i}.wav")
        tts.save(audio, path)
        files.append(path)
        sys.stderr.write(f"  · {voice}: {seg['text'][:60]}…\n")
    print(json.dumps({"sample_rate": 48000, "files": files}))


if __name__ == "__main__":
    main()
