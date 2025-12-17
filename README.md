# youtube-transcript
````
sudo apt install python3
sudo apt install python3-pip
pip install -U yt-dlp openai-whisper

````

````
docker build -t youtube-whisper .
docker run --rm -v "%cd%/downloads:/app/downloads" youtube-whisper

````

## Ubuntu wsl
````
sudo apt-get update && sudo apt-get install -y --no-install-recommends python3 pip ffmpeg ca-certificates

# Install Python deps
# (openai-whisper pulls torch; can be heavy on CPU images)
sudo pip install --no-cache-dir -U pip \
 && sudo pip install --no-cache-dir yt-dlp openai-whisper
````