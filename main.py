from spotipyMain import *
from youtube import *
from search import *
from metadata import *
import time

def main(id):
    pre_auth = time.perf_counter()
    authentication()
    post_auth = time.perf_counter()

    playlist=store_playlist(id)

    post_spotify=time.perf_counter()

    for song in playlist:
        song["url"]=find_best_song(song["name"],song["artists"],song["duration"])
        download(song)

    post_download=time.perf_counter()

    for song in playlist:
        tag_music(song)

    post_tag=time.perf_counter()
    return(f"\n\n\nTime elapsed for authentication: {post_auth-pre_auth:.6f} seconds\nTime elapsed for Spotify info: {post_spotify-post_auth:.6f} seconds\nTime elapsed for downloading: {post_download-post_spotify:.6f} seconds\nTime elapsed for tagging: {post_tag-post_download:.6f} seconds\n\n\nAverage time per song: {(post_tag-pre_auth)/len(playlist):.6f} seconds")


