from spotipyMain import *
from youtube import *
from search import *
from metadata import *
# from website2 import progress_messages
import time

def main(id):
    # progress_messages.append("AAAAAAAAAAA")
    pre_auth = time.perf_counter()
    authentication()
    post_auth = time.perf_counter()

    playlist=store_playlist(id)

    post_spotify=time.perf_counter()

    for song in playlist:
        print(song["name"])
        # progress_messages.append("test")
        song["url"]=find_best_song(song["name"],song["artists"],song["duration"])
        
        if song["url"]==None:
            with open("skipped.txt", "a", encoding="utf-8") as f:
                f.write(str(song)+"\n")
        else:
            print("Found best song for:"+str(song["name"]))
            download(song)
            print("Finish downloading:"+str(song["name"]))

    post_download=time.perf_counter()

    for song in playlist:
        tag_music(song)

    post_tag=time.perf_counter()
    print(f"\n\n\nTime elapsed for authentication: {post_auth-pre_auth:.6f} seconds\nTime elapsed for Spotify info: {post_spotify-post_auth:.6f} seconds\nTime elapsed for downloading: {post_download-post_spotify:.6f} seconds\nTime elapsed for tagging: {post_tag-post_download:.6f} seconds\n\n\nAverage time per song: {(post_tag-pre_auth)/len(playlist):.6f} seconds")



# def test(str):
    # progress_messages.append["idk does this work"]

# main("61if3C421hODLXUxadAdpA") #1
# main("36TvZ8Isaxokapj7WmXEX7") #2
# main("3sNhBMZ7zUVLXi7TdxjOLL") #3
# main("7FOngrOmbtHjHP6B3JeGJP") #4
# main("5hW8N4VRaFfO315O07gkD9") #5

# main("4VQ6hHW1uqvzqS2MvY5L5s") # Country1
# main("2blZ0NmGk2Ck9yGNOdpsf4") # Country2

main("1mFPviVFIXGIvDRvh4GIOq")
# start=time.perf_counter()
# find_best_song("Dusk Till Dawn",["ZAYN","Sia"],239)
# end=time.perf_counter()
# print(end-start)
