# CUDA optional; this is CPU-only and works everywhere
FROM python:3.11-slim

# System deps: ffmpeg for whisper audio decoding + ca-certs
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
# (openai-whisper pulls torch; can be heavy on CPU images)
RUN pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir yt-dlp openai-whisper

# Copy your app
COPY app.py /app/app.py

# Downloads will go to /app/downloads inside the container
RUN mkdir -p /app/downloads

# Default command
CMD ["python", "app.py"]
