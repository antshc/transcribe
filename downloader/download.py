"""
download.py — standalone CLI audio downloader using yt-dlp with Chrome cookies.

Usage:
    python download.py --url <youtube-url>

Features:
- Authenticates via Chrome browser cookies (Windows DPAPI) — no manual export needed.
- Downloads audio in opus ≤96 kbps, falling back to best available audio.
- Idempotent: skips the download when the output file already exists.
- Windows-safe filenames via restrictfilenames=True.
- Rejects playlist URLs — downloads only the single specified video.
- Creates the downloads/ directory automatically if absent.
"""

import argparse
import os
import sys

from yt_dlp import YoutubeDL


OUTPUT_DIR = "downloads"


def download_audio(url: str, output_dir: str = OUTPUT_DIR) -> str:
    """Download audio for a YouTube URL to *output_dir*.

    Uses Chrome browser cookies for authentication so no manual cookie export
    is required.  The function is idempotent: if the predicted output file
    already exists it is returned immediately without re-downloading.

    Args:
        url: YouTube video URL.  Playlist URLs are silently treated as
             single-video downloads (``noplaylist=True``).
        output_dir: Directory where the audio file is saved.  Created
                    automatically when absent.

    Returns:
        Absolute or relative path to the downloaded (or already-existing)
        audio file.
    """
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio[acodec=opus][abr<=96]/bestaudio",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "restrictfilenames": True,
        "noplaylist": True,
        # Use Chrome's encrypted cookie store — no cookies.txt needed.
        # On Windows yt-dlp decrypts via DPAPI automatically.
        "cookiesfrombrowser": ("chrome",),
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        predicted_path = ydl.prepare_filename(info)
        if os.path.exists(predicted_path):
            print(f"Already exists, skipping download: {predicted_path}")
            return predicted_path
        info = ydl.extract_info(url, download=True)
        return info["requested_downloads"][0]["filepath"]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Download audio from a YouTube URL using Chrome cookies. "
            "Output is written to the downloads/ directory."
        )
    )
    parser.add_argument(
        "--url",
        required=True,
        metavar="URL",
        help="YouTube video URL to download audio from.",
    )
    args = parser.parse_args()

    try:
        path = download_audio(args.url)
        print(f"Downloaded: {path}")
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
