import yt_dlp
import os

FFMPEG_DIR = '.\\ffmpeg-8.0-essentials_build\\bin\\ffmpeg.exe'

def download(songs): # As a list of tuples, of the song then the url
    urls=[]
    for song in songs:
        urls.append(song[1])
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": ".\\Songs\\%(title)s.%(ext)s",  # save as video title
        "ffmpeg_location": FFMPEG_DIR,   # use repo-local ffmpeg
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)