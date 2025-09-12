from spotipyMain import *
from youtube import *
from search import *

authentication()
playlist=store_playlist("1fyiyQnp1D2OGyT96v9bjm")

links=[]
for song in playlist:
    links.append(find_best_song(song["name"],song["artists"],song["duration"]))

download(links)


