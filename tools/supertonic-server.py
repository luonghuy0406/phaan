#!/usr/bin/env python3
"""
Local TTS Server using Supertonic 3 (https://huggingface.co/supertone-oss-archive/supertonic-3)
OpenAI-compatible POST /v1/audio/speech endpoint with Vietnamese ('vi') support.

Requirements:
    pip install supertonic fastapi uvicorn numpy soundfile

Run:
    python3 tools/supertonic-server.py
    # Or: npm run tts-server
"""

import sys
import io
import wave

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import Response
    from pydantic import BaseModel
    import uvicorn
    import numpy as np
except ImportError:
    print("[Supertonic Server] Thiếu thư viện cần thiết!")
    print("Vui lòng cài đặt bằng lệnh:")
    print("    pip install supertonic fastapi uvicorn numpy soundfile")
    sys.exit(1)

app = FastAPI(title="Supertonic-3 Vietnamese TTS Server")

# Allow requests from web app (localhost, iPad on LAN, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tts_engine = None

def get_engine():
    global tts_engine
    if tts_engine is None:
        try:
            from supertonic import TTS
            print("[Supertonic] Đang khởi tạo mô hình Supertonic-3 (tự động tải nếu chưa có)...")
            tts_engine = TTS(auto_download=True)
            print("[Supertonic] Đã tải xong mô hình!")
        except Exception as e:
            print(f"[Supertonic] Lỗi khởi tạo TTS: {e}")
            raise
    return tts_engine

class SpeechRequest(BaseModel):
    input: str
    model: str = "supertonic-3"
    voice: str = "F1"         # F1..F5 (nữ), M1..M5 (nam)
    lang: str = "vi"          # 'vi' = Tiếng Việt
    speed: float = 1.0
    total_steps: int = 8

@app.get("/health")
def health():
    return {"status": "ok", "model": "supertonic-3", "languages": ["vi", "en", "ko", "ja", "..."]}

@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "supertonic-3", "object": "model", "owned_by": "supertone-oss-archive"}
        ]
    }

@app.post("/v1/audio/speech")
def speech(req: SpeechRequest):
    text = req.input.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    engine = get_engine()

    voice = req.voice.upper()
    valid_voices = {"F1", "F2", "F3", "F4", "F5", "M1", "M2", "M3", "M4", "M5"}
    if voice not in valid_voices:
        voice = "F1"

    try:
        style = engine.get_voice_style(voice_name=voice)
    except Exception:
        style = engine.get_voice_style(voice_name="F1")

    lang = req.lang.lower() if req.lang else "vi"

    try:
        wav, _duration = engine.synthesize(
            text=text,
            voice_style=style,
            lang=lang,
            total_steps=req.total_steps,
            speed=req.speed,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synthesis error: {str(e)}")

    # Convert float32 [-1.0, 1.0] numpy array to 16-bit PCM WAV in memory
    audio_data = np.clip(wav.squeeze(), -1.0, 1.0)
    audio_int16 = (audio_data * 32767).astype(np.int16)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)      # mono
        wf.setsampwidth(2)      # 16-bit
        wf.setframerate(44100)  # 44.1 kHz
        wf.writeframes(audio_int16.tobytes())

    wav_bytes = buf.getvalue()
    return Response(content=wav_bytes, media_type="audio/wav")

if __name__ == "__main__":
    port = 8000
    print(f"=== Supertonic-3 TTS Server đang chạy trên http://0.0.0.0:{port} ===")
    print(f"Endpoint: http://localhost:{port}/v1/audio/speech")
    uvicorn.run(app, host="0.0.0.0", port=port)
