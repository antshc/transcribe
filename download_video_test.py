#!/usr/bin/env python3
from downloaderv2 import download_video, make_screenshots

url = "https://www.youtube.com/watch?v=2EGzAPhz2nE"

def main() -> None:
    video_path = download_video(url, "downloads")
    print("Video saved to:", video_path)

    screenshots = make_screenshots(
        video_path,
        [
            "00:00:05.000",
            "00:01:23.400",
            "00:10:00.000",
        ],
    )

    print(screenshots)

if __name__ == "__main__":
    main()
