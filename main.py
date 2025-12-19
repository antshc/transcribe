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

url = "https://www.youtube.com/watch?v=2EGzAPhz2nE"


@click.command()
@click.option("--repo", required=True, help="Github Repository Name")
@click.option("--token", required=True, help="Github Personal Access Token")
def main(repo: str, token: str) -> None:
    """Upload the file `filepath` to a GitHub repo using small helper functions."""
    output_dir = "downloads"
    audio_path = download_audio(url, output_dir)
    print("Audio saved to:", audio_path)

    srt_path = transcribe_and_save_srt(audio_path, model_name="base", output_dir=output_dir)
    print("SRT saved to:", srt_path)

    upload_file_to_repo(repo, token, audio_path)
    print(f"Uploaded {audio_path} to repository {repo}.")

if __name__ == "__main__":
    main()
