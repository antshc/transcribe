FROM khdevnet/whisper:latest
# Base image (antshc/whisper) already provides:
#   OS:     python:3.11-slim (Debian-based)
#   System: ffmpeg, ca-certificates
#   Python: openai-whisper (includes torch)

# Install Node.js 22 LTS (required by yt-dlp to solve YouTube's n-parameter JS challenge)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --no-cache-dir yt-dlp click httpx

WORKDIR /app

# Copy your app
COPY . /app/.

# Downloads will go to /app/downloads inside the container
RUN mkdir -p /app/downloads

# Default command
ENTRYPOINT ["python", "main.py"]
CMD []
