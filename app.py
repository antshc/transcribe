import os
from yt_dlp import YoutubeDL
import whisper

url = "https://www.youtube.com/watch?v=zhCRX3B7qwY"

OUTPUT_DIR = "downloads"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ydl_opts = {
    # Best audio for transcription (no ffmpeg)
    "format": "bestaudio[acodec=opus][abr<=96]/bestaudio",

    # Encode filename: spaces & unsafe chars -> '_'
    "outtmpl": os.path.join(OUTPUT_DIR, "%(title)s.%(ext)s"),
    "restrictfilenames": True,

    "noplaylist": True,
}

def srt_timestamp(seconds: float) -> str:
    # SRT format: HH:MM:SS,mmm
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

# 1) Download audio only if it does not already exist
with YoutubeDL(ydl_opts) as ydl:
    # Extract metadata first (no download)
    info = ydl.extract_info(url, download=False)

    # Predict the expected filename
    predicted_path = ydl.prepare_filename(info)

    if os.path.exists(predicted_path):
        audio_path = predicted_path
        print("Audio already exists, skipping download:", audio_path)
    else:
        # Download and get the real saved path
        info = ydl.extract_info(url, download=True)
        audio_path = info["requested_downloads"][0]["filepath"]
        print("Audio downloaded:", audio_path)

# 2) Transcribe with Whisper (segments include timestamps)
model = whisper.load_model("base")  # tiny/base/small/medium/large
result = model.transcribe(audio_path)

# 3) Save SRT (same safe base name)
base_name, _ = os.path.splitext(os.path.basename(audio_path))
srt_path = os.path.join(OUTPUT_DIR, f"{base_name}.srt")
write_srt(result["segments"], srt_path)

print("Audio saved to:", audio_path)
print("SRT saved to:", srt_path)
