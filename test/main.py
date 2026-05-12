# from Backend.spotipyMain import *
# from Backend.youtube import *
# from Backend.search import *
# from Backend.metadata import *

from scraping import extract_isrcs_stealth
from parse_dump import parse_intercepted_playlists
from find_isrc import new as find_best_song
from download import download_song


import time

def main(id, progress_callback=None):
    # progress_messages.append("AAAAAAAAAAA")
    # Not nessecary
    pre_auth = time.perf_counter()
    # authentication()
    # post_auth = time.perf_counter()


    '''
    1. Scrape spotify for track metadata and ISRCs using the playlist ID.
    2. For each track, use the ISRC to find the best matching YouTube video.
    3. Download the audio from the YouTube video.
    4. Tag the downloaded audio file with the correct metadata.
    '''

    # Scrape data from spotify
    print("Extracting playlist data using stealth scraping...")
    extract_isrcs_stealth("https://open.spotify.com/playlist/"+id)
    print("Finished extracting playlist data. Now parsing the saved JSON files...")
    song_list = parse_intercepted_playlists(dump_dir="spotify_payloads")
    print(f"Found {len(song_list)} songs to process.\n")
    if progress_callback:
        progress_callback(None, 0, len(song_list))
    
    counter=0
    for item in song_list:
        if progress_callback:
            progress_callback(None, 0, len(song_list))

        title = item["name"]
        
        # Grab the primary artist (the first one in the list)
        primary_artist = item["artists"][0] if item["artists"] else "Unknown Artist"
        duration = item.get("duration_ms", 0)

        print(f"--- Processing: {title} by {primary_artist} ---")

        # 3. Ask MusicBrainz for the ISRCs using the duration
        isrc_list = find_best_song(primary_artist, title, duration)

        if not isrc_list:
            print(f"Could not find ISRCs for {title}. Skipping download.\n")
            continue

        # 4. Pass the ISRCs to yt-dlp to download the MP3
        download_song(isrc_list, title, primary_artist)
        if progress_callback:
                progress_callback(song, counter, len(song_list))
        print("\n")
        counter+=1

    post_download=time.perf_counter()

    # for song in playlist:
    #     tag_music(song)

    post_tag=time.perf_counter()
    # print(f"\n\n\nTime elapsed for authentication: {post_auth-pre_auth:.6f} seconds\nTime elapsed for Spotify info: {post_spotify-post_auth:.6f} seconds\nTime elapsed for downloading: {post_download-post_spotify:.6f} seconds\nTime elapsed for tagging: {post_tag-post_download:.6f} seconds\n\n\nAverage time per song: {(post_tag-pre_auth)/len(playlist):.6f} seconds")

    print(f"\n\n\nTime elapsed for Spotify info: {post_download-pre_auth:.6f} seconds\nAverage time per song: {(post_download-pre_auth)/len(song_list):.6f} seconds")

# def test(str):
    # progress_messages.append["idk does this work"]

# main("61if3C421hODLXUxadAdpA") #1
# main("36TvZ8Isaxokapj7WmXEX7") #2
# main("3sNhBMZ7zUVLXi7TdxjOLL") #3
# main("7FOngrOmbtHjHP6B3JeGJP") #4
# main("5hW8N4VRaFfO315O07gkD9") #5

main("1mFPviVFIXGIvDRvh4GIOq") # LOCK IN

# main("4VQ6hHW1uqvzqS2MvY5L5s") # Country1
# main("2blZ0NmGk2Ck9yGNOdpsf4") # Country2

# main("1mFPviVFIXGIvDRvh4GIOq")
# start=time.perf_counter()
# find_best_song("Dusk Till Dawn",["ZAYN","Sia"],239)
# end=time.perf_counter()
# print(end-start)
