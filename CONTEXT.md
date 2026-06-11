# Transcribe

A tool that downloads audio from YouTube, transcribes it locally using Whisper, and uploads the resulting subtitle file to a GitHub repository.

## Language

**Video**: A YouTube resource identified by a URL. The unit of work the system processes.
_Avoid_: clip, content, media

**Audio**: The extracted audio track downloaded from a Video. Stored locally as the input to transcription.
_Avoid_: track, file, recording

**Transcript**: A timed subtitle file (`.srt`) produced by running Whisper over an Audio file.
_Avoid_: subtitles, captions, text

**Download**: The act of fetching a Video's Audio from YouTube and saving it to a local output directory.
_Avoid_: fetch, pull, save

**Transcription**: The act of running Whisper over an Audio file to produce a Transcript.
_Avoid_: recognition, conversion

**Screenshot**: A single video frame extracted at a specific timestamp, produced by ffmpeg from a downloaded video file.
_Avoid_: frame, capture, image

**Cookies**: A `cookies.txt` file exported from the browser once and supplied to yt-dlp for authenticated downloads. Used to authenticate yt-dlp requests to YouTube for members-only, age-gated, or rate-limited content.
_Avoid_: session, credentials, auth token, browser profile

**Output directory**: The local directory where Audio files and Transcripts are written. Exposed as a volume mount in Docker deployments.
_Avoid_: downloads folder, destination

## Example dialogue

> **Dev**: So the user points the tool at a YouTube URL and we get an SRT back?
> **Domain expert**: Right. We Download the Audio first, then run Transcription on it. The Transcript is what gets uploaded to GitHub.
> **Dev**: What about the `downloaderv2.py` file — does that replace the original?
> **Domain expert**: Not yet. v2 adds video Download and Screenshot support on top of the audio-only path. The two live side by side until the CLI is unified.
> **Dev**: And Cookies — the user has to supply those?
> **Domain expert**: Yes, if YouTube rate-limits or requires login. The user exports their browser Cookies to a `cookies.txt` file once and mounts it into the container.
