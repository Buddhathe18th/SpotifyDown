import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()  # loads variables from .env in the repo root

scope = "user-library-read"

auth_manager = SpotifyOAuth(scope=scope, show_dialog=True, open_browser=False)
sp = spotipy.Spotify(auth_manager=auth_manager)

print("CLICK:")
print(f"\n{auth_manager.get_authorize_url()}")
redirect_response = input("\nPaste FULL REDIRECT LINK: ").strip()


try:
    print("test")
    code = auth_manager.parse_response_code(redirect_response)
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


# # Get and display saved tracks
# try:
#     results = sp.playlist_items("1WH6WVBwPBz35ZbWsgCpgr")
#     good={}
#     for song_details in results["items"]:
#         song_raw=song_details["track"]
#         song={"images":[],"artists":getArtists(song_raw["artists"]),"duration_ms":[],"name":""}
    
    
#     # k=results["items"][0]["track"]
#     # print(getArtists(results["items"][13]["track"]["artists"]))
#     # print(k)
#     # print(type(k))
#     # print(k.keys())
#     # good={"images":[],"artists":[],"duration_ms":[],"name":""}

    
#     # if not results or not results.get('items'):
#     #     print("\n📭 No saved tracks found in your library!")
#     #     print("💡 Try saving some songs in Spotify and run this again.")
#     # else:
#     #     print(results)
#     #     tracks = results['items']
#     #     print(f"\n🎵 Found {len(tracks)} saved tracks:")
#     #     print("=" * 40)
#     #     for idx, item in enumerate(tracks):
#     #         if item and item.get('track'):
#     #             track = item['track']
#     #             if track.get('artists') and track.get('name'):
#     #                 artist = track['artists'][0]['name']
#     #                 name = track['name']
#     #                 print(f"{idx + 1:2}. {artist} – {name}")
#     #             else:
#     #                 print(f"{idx + 1:2}. [Track info unavailable]")
            
# except Exception as e:
#     print(f"\n❌ Error accessing Spotify data: {e}")
#     # Clear the token if there's an auth error
#     if "401" in str(e) or "Unauthorized" in str(e):
#         try:
#             del db["spotify_token"]
#             print("🔄 Cleared saved token. Please run the app again to reauthorize.")
#         except:
#             pass