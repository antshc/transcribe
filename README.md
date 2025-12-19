# youtube-transcript
````
sudo apt install -y python3-venv python3-full
sudo apt install python3-pip
python3 -m venv venv # create virtual environment
pip install -U yt-dlp openai-whisper
pip install click httpx

````

````
docker build -t youtube-whisper .
docker run --rm -v "%cd%/downloads:/app/downloads" youtube-whisper
docker run --rm -v "%cd%/downloads:/app/downloads" youtube-whisper --repo antshc/youtube-transcripts --token github_pat_xxxxxx
````

## Ubuntu wsl
````
sudo apt-get update && sudo apt-get install -y --no-install-recommends python3 pip ffmpeg ca-certificates

# Install Python deps
# (openai-whisper pulls torch; can be heavy on CPU images)
sudo pip install --no-cache-dir -U pip \
 && sudo pip install --no-cache-dir yt-dlp openai-whisper
````