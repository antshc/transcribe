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