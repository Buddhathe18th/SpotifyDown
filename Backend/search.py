import yt_dlp
import Backend.logger as logger

FFMPEG_DIR = '.\\ffmpeg-8.0-essentials_build\\bin\\ffmpeg.exe'

def find_best_song(isrc, title):
    option_length=0
    option_title=""
    
    query = f"ytsearch:{isrc}]"

    with yt_dlp.YoutubeDL({
        # 'quiet': True,
        "ffmpeg_location": FFMPEG_DIR
        , "logger": logger.YTDLPPyLogger()
        ,"verbose": True
        ,'flat_playlist': True
        ,"skip_download": True
        }) as ydl:
        info = ydl.extract_info(query, download=False)

    for entry in info["entries"]:
        
        option_title=entry["title"]
        option_length=entry["duration"]
        if "Official Video" not in option_title and "Official Music Video" not in option_title:
            print("Found song for "+title)
            print(info["entries"][0]["webpage_url"])
            return info["entries"][0]["webpage_url"]
        else:
            next
            
            
    print("Did not find song for "+title)
    return None