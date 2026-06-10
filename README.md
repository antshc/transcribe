# transcribe
````
sudo apt install -y python3-venv python3-full
sudo apt install python3-pip
python3 -m venv venv # create virtual environment
source ./venv/bin/activate
pip install -U yt-dlp openai-whisper
pip install click httpx
pip install ffmpeg-python

````

````
docker build -t khdevnet/ytt:latest .
docker run --rm khdevnet/ytt:latest --repo antshc/youtube-transcripts --token github_pat_xxxxxx

docker run --rm -v "%cd%/downloads:/app/downloads" khdevnet/ytt:latest --repo antshc/youtube-transcripts --token github_pat_xxxxxx
````

## Ubuntu wsl
````

sudo apt-get update && sudo apt-get install -y --no-install-recommends python3 pip ffmpeg ca-certificates

# Install Python deps
# (openai-whisper pulls torch; can be heavy on CPU images)
# should run in python env
source ./venv/bin/activate
pip install --no-cache-dir -U pip \
 && pip install --no-cache-dir yt-dlp openai-whisper
````
