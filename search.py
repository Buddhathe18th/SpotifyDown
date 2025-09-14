import yt_dlp

FFMPEG_DIR = '.\\ffmpeg-8.0-essentials_build\\bin\\ffmpeg.exe'

def find_best_song(title, artists, length):
    option_length=0
    while abs(option_length-length)>15:
        query = f"ytsearch:{title}"
        for artist in artists:
            query+=" "+artist
        query+=" audio"

        with yt_dlp.YoutubeDL({"ffmpeg_location": FFMPEG_DIR}) as ydl:
            info = ydl.extract_info(query, download=False)

        for entry in info["entries"]:
            option_length=entry["duration"]
    return info["entries"][0]["webpage_url"]

# song_title = "Baby"
# song_artists = ["Justin Beiber","Ludacris"]
# song_length = 214  # seconds

# print(find_best_song(song_title,song_artists,song_length))


