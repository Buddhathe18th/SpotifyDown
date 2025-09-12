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



try:
    print("test")
    # code = auth_manager.parse_response_code(redirect_response)
    # token = auth_manager.get_access_token(code)
    
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.playlist("41TSE7Yh4ZYy0xueqVg8cx")
    
    if not results['items']:
        print("Nothing is here")
    else:
        print(f"There are {len(results['items'])} saved tracks:\n")            
except Exception as e:
    print("broken")




# def getArtists(artists):
#     artist_list=[]
#     for artist in artists:
#         artist_list.append(artist["name"])
#     return artist_list


try:
    results = sp.playlist_items("1WH6WVBwPBz35ZbWsgCpgr")
    good={}
    # for song_details in results["items"]:
    #     song_raw=song_details["track"]
    #     song={"images":[],"artists":getArtists(song_raw["artists"]),"duration_ms":[],"name":""}
    
    
    k=results["items"][0]["track"]
    # print(getArtists(results["items"][13]["track"]["artists"]))
    print(k)
    print(type(k))
    print(k.keys())
    good={"images":[],"artists":[],"duration_ms":[],"name":""}

            
except Exception as e:
    print("I'm shit at programming what did I do")
    print(e)
    # Clear the token if there's an auth error
    if "401" in str(e) or "Unauthorized" in str(e):
        try:
            open('.cache', 'w').close()
        except:
            pass