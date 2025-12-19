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
@click.argument(
    "filepath", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path)
)
def main(repo: str, token: str, filepath: pathlib.Path) -> None:
    """Upload the file `filepath` to a GitHub repo using small helper functions."""
    
    audio_path = download_audio(url, "downloads")
    print("Audio saved to:", audio_path)
    
    srt_path = transcribe_and_save_srt(audio_path, model_name="base", output_dir=OUTPUT_DIR)
    print("SRT saved to:", srt_path)

    upload_file_to_repo(repo, token, filepath)
    print(f"Uploaded {filepath} to repository {repo}.")

if __name__ == "__main__":
    main()
