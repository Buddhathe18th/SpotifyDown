import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()  # loads variables from .env in the repo root

scope = "user-library-read"

auth_manager = SpotifyOAuth(scope=scope, show_dialog=True, open_browser=False)
sp = spotipy.Spotify(auth_manager=auth_manager)

try:
    auth_manager.get_cached_token()
    print("COOKED WOOOO")
except:
    print("I'm cooked")
    
    print("CLICK:")
    print(f"\n{auth_manager.get_authorize_url()}")
    redirect_response = input("\nPaste FULL REDIRECT LINK: ").strip()




def getArtists(artists):
    artist_list=[]
    for artist in artists:
        artist_list.append(artist["name"])
    return artist_list


try:
    results = sp.playlist_items("1WH6WVBwPBz35ZbWsgCpgr")
    good=[]
    for song_details in results["items"]:
        song_raw=song_details["track"]
        song={"image_url":song_raw["album"]["images"][0]["url"],"album":song_raw["album"]["name"],"artists":getArtists(song_raw["artists"]),"duration_ms":song_raw["duration_ms"],"name":song_raw["name"]}
        good.append(song)
    
            
except Exception as e:
    print("I'm shit at programming what did I do")
    print(e)
    # Clear the token if there's an auth error
    if "401" in str(e) or "Unauthorized" in str(e):
        try:
            open('.cache', 'w').close()
        except:
            pass