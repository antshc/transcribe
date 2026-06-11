"""
download.py — standalone CLI audio downloader using yt-dlp with cookies.txt authentication.

Usage:
    python download.py --url <youtube-url> [--cookies-file cookies.txt]

Features:
- Authenticates via a cookies.txt file — export once from your browser using a browser extension.
- Downloads audio in opus ≤96 kbps, falling back to best available audio or combined format.
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


def download_audio(url: str, output_dir: str = OUTPUT_DIR, cookies_file: str = "cookies.txt") -> str:
    """Download audio for a YouTube URL to *output_dir*.

    Reads authentication cookies from *cookies_file* (Netscape/cookies.txt
    format).  The function is idempotent: if the predicted output file
    already exists it is returned immediately without re-downloading.

    Args:
        url: YouTube video URL.  Playlist URLs are silently treated as
             single-video downloads (``noplaylist=True``).
        output_dir: Directory where the audio file is saved.  Created
                    automatically when absent.
        cookies_file: Path to a cookies.txt file used for authentication.
                      Resolved relative to the current working directory.

    Returns:
        Absolute or relative path to the downloaded (or already-existing)
        audio file.
    """
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio[acodec=opus][abr<=96]/bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "restrictfilenames": True,
        "noplaylist": True,
        # Authenticate using a cookies.txt file (Netscape format).
        "cookiefile": cookies_file,
        # Force the standard web client — cookies can otherwise trigger
        # the web_creator client which exposes no audio/video formats.
        "extractor_args": {"youtube": {"player_client": ["web"]}},
        # Enable Node.js for YouTube's n-parameter JS challenge.
        "js_runtimes": {"node": {}},
        # Allow yt-dlp to fetch the challenge solver script from GitHub.
        "remote_components": {"ejs:github"},
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
            "Download audio from a YouTube URL using a cookies.txt file for authentication. "
            "Output is written to the downloads/ directory."
        )
    )
    parser.add_argument(
        "--url",
        required=True,
        metavar="URL",
        help="YouTube video URL to download audio from.",
    )
    parser.add_argument(
        "--cookies-file",
        default="cookies.txt",
        metavar="PATH",
        help="Path to a cookies.txt file for authentication (default: cookies.txt).",
    )
    args = parser.parse_args()

    try:
        path = download_audio(args.url, cookies_file=args.cookies_file)
        print(f"Downloaded: {path}")
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
