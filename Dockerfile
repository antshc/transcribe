FROM khdevnet/whisper:latest
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
