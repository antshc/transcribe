"""Small helpers for uploading files to GitHub using the Contents API.

This module follows single-responsibility principles: each function does one
thing and can be composed by a thin CLI or other callers.
"""

from typing import Any, Dict, Optional, Tuple

import hashlib
import httpx
import base64
import logging
import pathlib

def hash_blob_sha1(file_content: bytes) -> str:
    """Compute the SHA1 of file contents like git would.

    This mirrors how Git computes the blob SHA-1: prefix with "blob {size}\0"
    and hash the resulting bytes.
    """
    size = len(file_content)
    header = f"blob {size}\0".encode("utf-8")
    store = header + file_content
    return hashlib.sha1(store).hexdigest()

def parse_github_path(path: str) -> Tuple[str, str, Optional[str]]:
    """Parse 'owner/repo[/folder/...'] -> (owner, repo, folder_or_None)."""
    parts = path.strip("/").split("/")
    if len(parts) < 2:
        raise ValueError("Path must be at least 'owner/repo'")
    owner = parts[0]
    repo = parts[1]
    folder = "/".join(parts[2:]) if len(parts) > 2 else None
    return owner, repo, folder

def build_api_url(owner: str, repo: str, path: str) -> str:
    return f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"


def make_headers(token: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


def prepare_payload(message: str, encoded_content: str, sha: Optional[str] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"message": message, "content": encoded_content}
    if sha:
        payload["sha"] = sha
    return payload


def get_remote_file(api_url: str, headers: Dict[str, str]) -> Tuple[int, Optional[Dict[str, Any]]]:
    """Return (status_code, json) for a GET on `api_url`.

    If the request fails (network error), the function raises httpx.RequestError.
    """
    response = httpx.get(api_url, headers=headers)
    try:
        data = response.json()
    except ValueError:
        data = None
    return response.status_code, data


def upload_file(api_url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> httpx.Response:
    """Create or update a file at `api_url` using the Contents API."""
    return httpx.put(api_url, headers=headers, json=payload)


def file_contents_identical(local_bytes: bytes, remote_json: Dict[str, Any]) -> bool:
    """Compare local bytes against a remote file JSON (which contains a `sha`)."""
    if not remote_json or "sha" not in remote_json:
        return False
    local_sha = hash_blob_sha1(local_bytes)
    return local_sha == remote_json["sha"]


def upload_file_to_repo(repopath: str, token: str, filepath: pathlib.Path) -> None:
    """Upload the file `filepath` to a GitHub repo using small helper functions."""
    print(f"Uploading {filepath} to GitHub repository {repopath}...")
    file_content = filepath.read_bytes()
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    owner, repo, folder = parse_github_path(repopath)
    path = f"{folder}/{filepath.name}" if folder else filepath.name
    print("Parsed repo path:", owner, repo, path)

    api_url = build_api_url(owner, repo, path)

    headers = make_headers(token)

    logging.debug("Checking if remote file exists")
    try:
        status, remote_json = get_remote_file(api_url, headers)
    except Exception as exc:  # httpx.RequestError or similar
        print(f"Error connecting to Github: {exc}")
        return

    if status == 200 and file_contents_identical(file_content, remote_json):
        print(f"File '{filepath.name}' already exists and content is identical.")
        return

    sha = remote_json.get("sha") if remote_json and isinstance(remote_json, dict) else None
    payload = prepare_payload(f"Add new blog post: {filepath.name}", encoded_content, sha=sha)

    logging.debug("Uploading file")
    response = upload_file(api_url, headers, payload)
    try:
        data = response.json()
    except ValueError:
        data = None

    if response.status_code in {200, 201}:
        if data and "content" in data:
            print(f"Successfully uploaded file. View at {data['content']['html_url']}")
        else:
            print("Successfully uploaded file.")
    else:
        print(f"Error uploading file: {data}")
