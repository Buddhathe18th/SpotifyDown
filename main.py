import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

auth_manager = SpotifyOAuth(scope=scope, show_dialog=True)
sp = spotipy.Spotify(auth_manager=auth_manager)

try:
    results = sp.playlist("41TSE7Yh4ZYy0xueqVg8cx")
    
    if not results['items']:
        print("Nothing is here")
    else:
        print(f"There are {len(results['items'])} saved tracks:\n")
            
except Exception as e:
    print(e)
