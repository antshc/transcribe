import os
from yt_dlp import YoutubeDL

def download_audio(url: str, username: str, password: str, output_dir: str = "downloads") -> str:
    """
    Download audio for a YouTube URL (or return existing file path).
    Returns the path to the downloaded audio file.
    """
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        "username": username,
        "password": password,
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