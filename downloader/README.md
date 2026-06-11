# downloader

Standalone CLI tool that downloads audio from a YouTube URL using **yt-dlp** with a `cookies.txt` file for authentication.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.10+** | [python.org/downloads](https://www.python.org/downloads/) — add to PATH during install |
| **Node.js 18+** | Required by yt-dlp to solve YouTube's JS challenge; [nodejs.org](https://nodejs.org/) or `winget install OpenJS.NodeJS` |
| **ffmpeg** | Required by yt-dlp for audio post-processing |
| **cookies.txt** | Required for authenticated downloads (members-only, age-gated videos) |

### Install ffmpeg via winget

```powershell
winget install --id Gyan.FFmpeg -e
```

Restart your terminal after installation so that `ffmpeg` is available on `PATH`.

### Exporting cookies.txt (authenticated downloads only)

For videos that require a YouTube account (members-only, age-gated, etc.) you must export your browser cookies to a `cookies.txt` file:

1. Sign in to YouTube in your browser.
2. Install the [cookies.txt browser extension](https://github.com/kairi003/Get-cookies.txt-LOCALLY) (available for Chrome and Firefox).
3. Navigate to `https://www.youtube.com` and export cookies using the extension.
4. Save the exported file as `cookies.txt` in the `downloader/` directory.

Public videos work without a cookies.txt file, but the argument is always passed to yt-dlp (yt-dlp silently ignores a missing file for public content).

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

To use a cookies.txt file at a non-default location:

```powershell
python download.py --url <youtube-url> --cookies-file path\to\cookies.txt
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
| `WARNING: n challenge solving failed` | Install Node.js (`winget install OpenJS.NodeJS`) and restart the terminal; yt-dlp uses it to solve YouTube's JS challenge |
| `ERROR: Sign in to confirm you're not a bot` | Export a fresh `cookies.txt` from your browser and place it in the `downloader/` directory |
| Playlist URL downloads only one video | Intended — the script is single-video only (playlist URLs are silently clamped) |
