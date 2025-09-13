from spotipyMain import *
from youtube import *
from search import *
import time

pre_auth = time.perf_counter()
authentication()
post_auth = time.perf_counter()

playlist=store_playlist("1fyiyQnp1D2OGyT96v9bjm")

post_spotify=time.perf_counter()

for song in playlist:
    song["url"]=find_best_song(song["name"],song["artists"],song["duration"])
    download(song)

post_download=time.perf_counter()

for song in playlist:
    print(song)

print(f"\n\n\nTime elapsed for authentication: {post_auth-pre_auth:.6f} seconds")
print(f"Time elapsed for Spotify info: {post_spotify-post_auth:.6f} seconds")
print(f"Time elapsed for downloading: {post_download-post_spotify:.6f} seconds")

print(f"\n\nAverage time per song: {(post_download-pre_auth)/len(playlist):.6f} seconds")


