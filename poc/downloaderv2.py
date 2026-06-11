import os
import re
from pathlib import Path
from typing import Iterable, List

import ffmpeg
from yt_dlp import YoutubeDL

def download_audio(url: str, output_dir: str = "downloads") -> str:
    """
    Download audio for a YouTube URL (or return existing file path).
    Returns the path to the downloaded audio file.
    """
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio[acodec=opus][abr<=96]/bestaudio",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "restrictfilenames": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        predicted_path = ydl.prepare_filename(info)
        if os.path.exists(predicted_path):
            return predicted_path
        info = ydl.extract_info(url, download=True)
        return info["requested_downloads"][0]["filepath"]
    
# Strict timestamp: HH:MM:SS.mmm
_TIMESTAMP_RE = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}$")


def download_video(url: str, output_dir: str = "downloads") -> str:
    """
    Download a video and return the local MP4 path.
    """
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "restrictfilenames": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        predicted = ydl.prepare_filename(info)
        predicted = os.path.splitext(predicted)[0] + ".mp4"

        if os.path.exists(predicted):
            return predicted

        info = ydl.extract_info(url, download=True)

        if info.get("filepath") and os.path.exists(info["filepath"]):
            return info["filepath"]

        if os.path.exists(predicted):
            return predicted

        raise FileNotFoundError("Video downloaded but final file not found.")


def _validate_timestamp(ts: str) -> None:
    """
    Enforce HH:MM:SS.mmm format only.
    """
    if not isinstance(ts, str) or not _TIMESTAMP_RE.match(ts):
        raise ValueError(
            f"Invalid timestamp '{ts}'. "
            "Only format allowed: HH:MM:SS.mmm (e.g. 00:01:23.400)"
        )


def make_screenshots(
    video_path: str,
    timestamps: Iterable[str],
    output_dir: str = "screenshots",
    image_ext: str = "jpg",
) -> List[str]:
    """
    Create screenshots at exact timestamps using ffmpeg-python.

    timestamps must be in format: HH:MM:SS.mmm
    """
    video = Path(video_path)
    if not video.exists():
        raise FileNotFoundError(f"Video not found: {video}")

    os.makedirs(output_dir, exist_ok=True)

    base = video.stem
    outputs: List[str] = []

    for index, ts in enumerate(timestamps, start=1):
        _validate_timestamp(ts)

        out_file = (
            Path(output_dir)
            / f"{base}__{index:03d}__{ts.replace(':', '-').replace('.', '-')}.{image_ext}"
        )
        outputs.append(str(out_file))

        if out_file.exists():
            continue

        try:
            (
                ffmpeg
                .input(str(video), ss=ts)
                .output(str(out_file), vframes=1)
                .global_args("-y", "-hide_banner", "-loglevel", "error")
                .run()
            )
        except ffmpeg.Error as e:
            stderr = ""
            if e.stderr:
                stderr = e.stderr.decode("utf-8", errors="replace")
            raise RuntimeError(
                f"ffmpeg failed at timestamp {ts}\n{stderr}"
            ) from e

    return outputs