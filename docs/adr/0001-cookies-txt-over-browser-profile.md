# Use cookies.txt for YouTube authentication

The youtube-download script needs to authenticate with YouTube for members-only, age-gated, and rate-limited content. We use a `cookies.txt` file exported once from the browser and supplied to yt-dlp via `--cookies path/to/cookies.txt`.

`cookies.txt` is portable across host OS types (Windows native, Linux, Docker containers) and requires only a one-time manual export via a browser extension.

## Considered Options

- `cookies.txt` (**chosen**) — portable; works on Windows, Linux, and inside Docker containers; requires a one-time manual export via a browser extension (e.g. "Get cookies.txt LOCALLY")
- `--cookies-from-browser chrome` (**rejected**) — reads Chrome's cookie store directly via Windows DPAPI with no manual export step; unsuitable because DPAPI is inaccessible from Linux and Docker containers, making it non-portable for the deployment target
