import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"

auth_manager = SpotifyOAuth(scope=scope, show_dialog=True, open_browser=False)
sp = spotipy.Spotify(auth_manager=auth_manager)

print("CLICK:")
print(f"\n{auth_manager.get_authorize_url()}")
redirect_response = input("\nPaste FULL REDIRECT LINK: ").strip()


try:
    code = auth_manager.parse_response_code(redirect_response)
    token = auth_manager.get_access_token(code)
    
    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.playlist("41TSE7Yh4ZYy0xueqVg8cx")
    
    if not results['items']:
        print("Nothing is here")
    else:
        print(f"There are {len(results['items'])} saved tracks:\n")
            
except Exception as e:
    print(e)
