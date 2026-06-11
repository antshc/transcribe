# ytt — YouTube Transcription Tool

Downloads audio from a YouTube URL, transcribes it to SRT via Whisper, and uploads the result to a GitHub repository.

---

## How it works

1. Downloads audio using **yt-dlp** (cookies.txt auth, Node.js n-challenge solver)
2. Transcribes audio to SRT using **OpenAI Whisper** (`base` model)
3. Uploads the SRT file to the specified GitHub repository via the Contents API

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Docker** | [docs.docker.com](https://docs.docker.com/get-docker/) |
| **cookies.txt** | Required for authenticated downloads (members-only, age-gated videos) |
| **GitHub PAT** | Personal Access Token with `repo` scope for uploading the SRT |

### Exporting cookies.txt

For videos that require a YouTube account (members-only, age-gated, etc.):

1. Sign in to YouTube in your browser.
2. Install the [cookies.txt browser extension](https://github.com/kairi003/Get-cookies.txt-LOCALLY).
3. Navigate to `https://www.youtube.com` and export cookies using the extension.
4. Save the file as `cookies.txt` next to your `docker run` command.

> ⚠️ `cookies.txt` contains your YouTube session credentials — never commit it.

Public videos work without cookies.txt (yt-dlp silently ignores a missing file).

---

## Building the image

```bash
docker build ytt/ --file ytt/Dockerfile --tag khdevnet/ytt:latest
```

Or from inside the `ytt/` directory:

```bash
docker build . --file Dockerfile --tag khdevnet/ytt:latest
```

---

## Running

### Minimal (public video, no cookies)

```bash
docker run --rm \
  -v "$(pwd)/downloads:/app/downloads" \
  khdevnet/ytt:latest \
  --url "https://www.youtube.com/watch?v=jNQXAC9IVRw" \
  --repo owner/repo-name \
  --token YOUR_GITHUB_PAT
```

### With cookies.txt (authenticated / members-only)

Mount both the cookies file and the downloads folder:

```bash
docker run --rm \
  -v "$(pwd)/downloads:/app/downloads" \
  -v "$(pwd)/cookies.txt:/app/cookies.txt:ro" \
  khdevnet/ytt:latest \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --repo owner/repo-name \
  --token YOUR_GITHUB_PAT \
  --cookies-file /app/cookies.txt
```

### With language hint

```bash
docker run --rm \
  -v "$(pwd)/downloads:/app/downloads" \
  khdevnet/ytt:latest \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --repo owner/repo-name \
  --token YOUR_GITHUB_PAT \
  --lang en
```

---

## CLI reference

| Option | Required | Default | Description |
|---|---|---|---|
| `--url` | ✅ | — | YouTube video URL |
| `--repo` | ✅ | — | Target GitHub repo (`owner/repo` or `owner/repo/folder`) |
| `--token` | ✅ | — | GitHub Personal Access Token (`repo` scope) |
| `--lang` | ❌ | auto-detect | Language code for Whisper transcription (e.g. `en`, `uk`) |
| `--cookies-file` | ❌ | `cookies.txt` | Path to Netscape cookies.txt for yt-dlp authentication |

---

## GitHub Actions

| Workflow | Trigger | Description |
|---|---|---|
| `build-docker-image.yml` | Push to `main` | Builds and pushes `khdevnet/ytt:latest` to Docker Hub |
| `transcript.yml` | Manual dispatch | Runs the transcription pipeline using the published image |

### Required secrets

| Secret | Used by |
|---|---|
| `DOCKER_HUB_USERNAME` | `build-docker-image.yml` |
| `DOCKER_HUB_PASSWORD` | `build-docker-image.yml` |
| `GIT_HUB_PAT` | `transcript.yml` |

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `WARNING: n challenge solving failed` | Ensure Node.js 22 is present in the image (installed by the Dockerfile) |
| `ERROR: Sign in to confirm you're not a bot` | Export a fresh `cookies.txt` and mount it with `-v` |
| `ERROR: Requested format is not available` | Run `docker pull khdevnet/ytt:latest` to get the latest yt-dlp |
| SRT already exists in target repo | The tool skips re-upload when content is identical (idempotent) |
