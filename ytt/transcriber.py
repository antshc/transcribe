import json
import os
from collections import defaultdict
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

def write_srt_chunks(
    segments: list,
    chunk_dir: str,
    base_name: str,
    chunk_seconds: int = 300,
) -> list[str]:
    buckets: dict[int, list] = defaultdict(list)
    for seg in segments:
        bucket = int(seg["start"] // chunk_seconds)
        buckets[bucket].append(seg)

    chunk_paths = []
    for n, bucket_idx in enumerate(sorted(buckets), start=1):
        chunk_path = os.path.join(chunk_dir, f"{base_name}_part_{n:02d}.srt")
        chunk_paths.append(chunk_path)
        if os.path.exists(chunk_path):
            continue
        with open(chunk_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(buckets[bucket_idx], start=1):
                start = srt_timestamp(seg["start"])
                end = srt_timestamp(seg["end"])
                text = (seg.get("text") or "").strip()
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    return chunk_paths


def merge_srt_files(chunk_paths: list[str], output_path: str) -> None:
    counter = 1
    with open(output_path, "w", encoding="utf-8") as out:
        for chunk_path in chunk_paths:
            with open(chunk_path, "r", encoding="utf-8") as f:
                content = f.read()
            blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
            for block in blocks:
                lines = block.splitlines()
                # replace the block index (first line) with the global counter
                lines[0] = str(counter)
                out.write("\n".join(lines) + "\n\n")
                counter += 1


def transcribe_and_save_srt(
    audio_path: str,
    model_name: str = "turbo",
    output_dir: str = "downloads",
    language: Optional[str] = None,
    chunk_minutes: int = 1,
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    base_name, _ = os.path.splitext(os.path.basename(audio_path))
    srt_path = os.path.join(output_dir, f"{base_name}.srt")
    if os.path.exists(srt_path):
        return srt_path

    chunk_dir = os.path.join(output_dir, f"{base_name}_chunks")
    os.makedirs(chunk_dir, exist_ok=True)
    segments_json_path = os.path.join(chunk_dir, f"{base_name}_segments.json")

    if os.path.exists(segments_json_path):
        with open(segments_json_path, "r", encoding="utf-8") as f:
            segments = json.load(f)
    else:
        model = whisper.load_model(model_name)
        transcribe_kwargs: dict[str, str] = {}
        if language is not None:
            transcribe_kwargs["language"] = language
        result = model.transcribe(audio_path, **transcribe_kwargs)
        segments = result["segments"]
        with open(segments_json_path, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False)

    chunk_paths = write_srt_chunks(segments, chunk_dir, base_name, chunk_minutes * 60)
    merge_srt_files(chunk_paths, srt_path)
    return srt_path
