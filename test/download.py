import yt_dlp

def download_song(isrcs: list, title: str = "Unknown Track", artist: str = "Unknown Artist"):
    if not isrcs:
        print("No ISRCs provided. Skipping.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320', 
        }],
        'outtmpl': f'{artist} - {title}.%(ext)s',
        'quiet': False, # Temporarily set to False so we can see if it works!
        'noplaylist': True,
        
        # --- THE ANTI-403 BYPASS ---
        'extractor_args': {
            'youtube': {
                # Force clients that currently do not heavily enforce SABR JS challenges
                'player_client': ['android', 'tv'] 
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for isrc in isrcs:
            print(f"Searching for ISRC: {isrc}...")
            
            # Use standard ytsearch1: which natively supports ISRC lookups
            search_query = f'ytsearch1:"{isrc}"'
            
            try:
                # download=True triggers the actual download immediately if found
                info = ydl.extract_info(search_query, download=True)
                
                # Check if the search returned zero results
                if 'entries' in info and len(info['entries']) == 0:
                    print(f" -> No results found for {isrc}. Trying next...")
                    continue
                
                print(f"✅ Success! Downloaded '{title}' using ISRC: {isrc}")
                return # Exit the function immediately upon success

            except Exception as e:
                print(f" -> Failed on {isrc}. Trying next...")
                continue
                
    print(f"❌ Exhausted all {len(isrcs)} ISRCs. Could not find the song.")