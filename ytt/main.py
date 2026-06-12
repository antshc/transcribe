#!/usr/bin/env python3

"""Thin CLI that uploads a local file to a GitHub repository using helpers.

The heavy lifting lives in `github.py` so this file's responsibility is CLI
argument parsing and orchestration.
"""

import pathlib

import click

from github import (
    upload_file_to_repo
)
from downloader import download_audio
from transcriber import transcribe_and_save_srt

@click.command()
@click.option("--url", required=True, help="YouTube URL")
@click.option("--lang", required=False, help="Language for transcription")
@click.option("--repo", required=True, help="Github Repository Name")
@click.option("--token", required=True, help="Github Personal Access Token")
@click.option("--cookies-file", default="cookies.txt", show_default=True, help="Path to cookies.txt for authentication")
def main(url: str, lang: str, repo: str, token: str, cookies_file: str) -> None:
    output_dir = "downloads"
    audio_path = download_audio(url, output_dir=output_dir, cookies_file=cookies_file)
    print("Audio saved to:", audio_path)

    srt_path = transcribe_and_save_srt(audio_path, model_name="turbo", output_dir=output_dir, language=lang)
    print("SRT saved to:", srt_path)

    upload_file_to_repo(repo, token, pathlib.Path(srt_path))
    print(f"Uploaded {srt_path} to repository {repo}.")

if __name__ == "__main__":
    main()
