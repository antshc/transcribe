import os
from typing import Optional

import whisper

def srt_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000.0))
    h = ms // 3_600_000
    ms -= h * 3_600_000
    m = ms // 60_000
    ms -= m * 60_000
    s = ms // 1000
    ms -= s * 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def write_srt(segments, srt_path: str) -> None:
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start = srt_timestamp(seg["start"])
            end = srt_timestamp(seg["end"])
            text = (seg.get("text") or "").strip()
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")

def transcribe_and_save_srt(
    audio_path: str,
    model_name: str = "base",
    output_dir: str = "downloads",
    language: Optional[str] = None,
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    base_name, _ = os.path.splitext(os.path.basename(audio_path))
    transcribe_name = f"{base_name}.srt"
    srt_path = os.path.join(output_dir, transcribe_name)
    if os.path.exists(srt_path):
        return srt_path
    model = whisper.load_model(model_name)
    transcribe_kwargs: dict[str, str] = {}
    if language is not None:
        transcribe_kwargs["language"] = language
    result = model.transcribe(audio_path, **transcribe_kwargs)
    write_srt(result["segments"], srt_path)
    return srt_path
