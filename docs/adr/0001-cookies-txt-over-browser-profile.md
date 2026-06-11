# Use --cookies-from-browser chrome for YouTube authentication

The youtube-download script runs as a native Windows Python process (no Docker container). On Windows, yt-dlp can read Chrome's cookie store directly via the Windows DPAPI (`--cookies-from-browser chrome`), requiring no manual cookie export from the user.

We use `--cookies-from-browser chrome` because it is transparent: as long as the user is logged into YouTube in Chrome, authenticated downloads succeed with no additional setup.

## Considered Options

- `--cookies-from-browser chrome` — zero setup for the user on Windows; not viable inside a Linux Docker container (DPAPI is inaccessible from Linux)
- `cookies.txt` mount — portable across host OS types, but requires a one-time manual export via a browser extension; still the correct choice for Docker deployments
