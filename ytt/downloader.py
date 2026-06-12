import glob
import os
from pathlib import Path

from yt_dlp import YoutubeDL

def download_audio(url: str, output_dir: str = "downloads", cookies_file: str = "cookies.txt") -> str:
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
        stem = Path(predicted_path).stem
        existing = glob.glob(os.path.join(output_dir, f"{stem}.*"))
        if existing:
            print(f"Already exists, skipping download: {existing[0]}")
            return existing[0]
        info = ydl.extract_info(url, download=True)
        return info["requested_downloads"][0]["filepath"]