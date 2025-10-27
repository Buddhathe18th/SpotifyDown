import yt_dlp
import os
import logger

FFMPEG_DIR = '.\\ffmpeg-8.0-essentials_build\\bin\\ffmpeg.exe'

def download(song): # song dictionary
    ydl_opts = {
        # 'quiet': True,
        "format": "bestaudio/best",
        "outtmpl": ".\\Songs\\"+song["playlist"]+"\\"+str(song["name"])+".%(ext)s",  # save as video title
        "ffmpeg_location": FFMPEG_DIR,   # use repo-local ffmpeg
        "logger": logger.YTDLPPyLogger()
        ,"verbose": True,
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([song["url"]])
    except:
        with open("skipped.txt", "a", encoding="utf-8") as f:
                f.write(str(song)+"\n")