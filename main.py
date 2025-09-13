from spotipyMain import *
from youtube import *
from search import *
import time

pre_auth = time.perf_counter()
authentication()
post_auth = time.perf_counter()

playlist=store_playlist("1fyiyQnp1D2OGyT96v9bjm")

post_spotify=time.perf_counter()

links=[]
for song in playlist:
    links.append(find_best_song(song["name"],song["artists"],song["duration"]))

post_search=time.perf_counter()

download(links)

post_download=time.perf_counter()

print(f"\n\n\nTime elapsed for authentication: {post_auth-pre_auth:.6f} seconds")
print(f"Time elapsed for Spotify info: {post_spotify-post_auth:.6f} seconds")
print(f"Time elapsed for searching: {post_search-post_spotify:.6f} seconds")
print(f"Time elapsed for downloading: {post_download-post_search:.6f} seconds")

print(f"\n\nAverage time per song: {post_download-pre_auth:.6f} seconds")


