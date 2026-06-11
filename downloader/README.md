# downloader

Standalone CLI tool that downloads audio from a YouTube URL using **yt-dlp** with Chrome browser cookies.  
Target platform: **Windows only**.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.10+** | [python.org/downloads](https://www.python.org/downloads/) — add to PATH during install |
| **ffmpeg** | Required by yt-dlp for audio post-processing |
| **Google Chrome** | Required for authenticated downloads via Chrome cookie store |

### Install ffmpeg via winget

```powershell
winget install --id Gyan.FFmpeg -e
```

Restart your terminal after installation so that `ffmpeg` is available on `PATH`.

### Chrome login (authenticated downloads only)

For videos that require a YouTube account (members-only, age-gated, etc.) you must be **signed in to YouTube inside Chrome** before running the script.  The script reads Chrome's encrypted cookie store automatically — no manual cookie export needed.  Public videos work without being signed in.

---

## One-time setup

Run these commands once from the `downloader/` directory.

```powershell
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate it (Windows)
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running the script

With the virtual environment active:

```powershell
python download.py --url <youtube-url>
```

The audio file is saved to `downloads/` (created automatically).  
Re-running with the same URL is safe — the script skips the download when the file already exists.

---

## Manual test procedure

Use the first-ever YouTube video ("Me at the zoo", 18 seconds, public, no auth required) to verify the happy path end-to-end.

```powershell
# Activate the venv if not already active
.venv\Scripts\activate

# Download a known short public video
python download.py --url "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

**Expected output:**

```
Downloaded: downloads\Me_at_the_zoo.opus
```

**Verify the file was created:**

```powershell
Get-ChildItem downloads\
```

You should see a file named `Me_at_the_zoo.opus` (or similar Windows-safe variant) with a non-zero size.

**Re-run to verify idempotency:**

```powershell
python download.py --url "https://www.youtube.com/watch?v=jNQXAC9IVRw"
```

Expected output:

```
Already exists, skipping download: downloads\Me_at_the_zoo.opus
Downloaded: downloads\Me_at_the_zoo.opus
```

The file is **not** re-downloaded.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `'ffmpeg' is not recognized` | Run `winget install --id Gyan.FFmpeg -e` and restart the terminal |
| `ERROR: Requested format is not available` | yt-dlp version mismatch — run `pip install -U yt-dlp` |
| `ERROR: Sign in to confirm you're not a bot` | Open Chrome, sign into YouTube, then retry |
| Playlist URL downloads only one video | Intended — the script is single-video only (playlist URLs are silently clamped) |
