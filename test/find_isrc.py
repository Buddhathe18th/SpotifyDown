import musicbrainzngs
import re

def get_canonical_studio_isrc(artist: str, title: str, spotify_duration_ms: int) -> list:
    """
    Searches MusicBrainz for a track and strictly filters for the official studio ISRC
    using duration matching and release status.
    """
    musicbrainzngs.set_useragent("MySpotifyDownloader", "2.0", "your@email.com")
    
    # Clean title to prevent strict Lucene search failures
    clean_title = re.sub(r'\(.*?\)|\[.*?\]', '', title).strip()
    query = f'artist:"{artist}" AND recording:"{clean_title}"'
    
    try:
        print(f"Searching MusicBrainz for: {clean_title} by {artist}...")
        # Fetch top 15 results to ensure we cast a wide enough net
        result = musicbrainzngs.search_recordings(query=query, limit=15)
        
        for rec in result.get('recording-list', []):
            rec_id = rec['id']
            
            # Fetch specific recording details, explicitly asking for ISRCs and Release info
            details = musicbrainzngs.get_recording_by_id(rec_id, includes=["isrcs", "releases"])
            recording = details.get('recording', {})
            
            # Rule 1: Must have an ISRC
            isrc_list = recording.get('isrc-list', [])
            if not isrc_list:
                continue
            print(isrc_list)
                
            # Rule 2: Exclude Video Tracks (We want the studio audio)
            # if recording.get('video') == 'true':
            #     continue
                
            # Rule 3: Duration Match (The ultimate identifier)
            mb_duration = int(recording.get('length', 0))
            # Inside your MusicBrainz loop...
            if spotify_duration_ms > 0 and abs(mb_duration - spotify_duration_ms) <= 3000:
                releases = recording.get('release-list', [])
                for release in releases:
                    if release.get('status') == 'Official':
                        print(f"Match found! Returning {len(isrc_list)} possible ISRCs.")
                        return isrc_list # FIX: Return the whole list, not isrc_list[0]
                        
                return isrc_list # FIX: Return the whole list
                
        print("No exact studio match found within the duration threshold.")
        return None

    except Exception as e:
        print(f"MusicBrainz API Error: {e}")
        return None
    

def new(artist: str, title: str, spotify_duration_ms: int) -> list:
    """
    Searches MusicBrainz for a track and aggregates ALL valid ISRCs across different 
    recordings that match the studio duration.
    """
    musicbrainzngs.set_useragent("MySpotifyDownloader", "2.1", "your@email.com")
    
    # Clean title to prevent strict Lucene search failures
    clean_title = re.sub(r'\(.*?\)|\[.*?\]', '', title).strip()
    query = f'artist:"{artist}" AND recording:"{clean_title}"'
    
    # We use sets to automatically prevent duplicate ISRCs
    strict_isrcs = set()
    fallback_isrcs = set()
    
    try:
        print(f"Searching MusicBrainz for: {clean_title} by {artist}...")
        # Fetch top 15 results to ensure we cast a wide enough net
        result = musicbrainzngs.search_recordings(query=query, limit=15)
        
        for rec in result.get('recording-list', []):
            rec_id = rec['id']
            
            # Fetch specific recording details, explicitly asking for ISRCs and Release info
            details = musicbrainzngs.get_recording_by_id(rec_id, includes=["isrcs", "releases"])
            recording = details.get('recording', {})
            
            # Rule 1: Must have an ISRC
            isrc_list = recording.get('isrc-list', [])
            if not isrc_list:
                continue
                
            # Rule 2: Exclude Video Tracks (We want the studio audio)
            if recording.get('video') == 'true':
                continue
                
            # Safely get the duration, defaulting to 0 if MusicBrainz is missing the data
            length_val = recording.get('length')
            mb_duration = int(length_val) if length_val else 0
            
            # --- AGGREGATION LOGIC (No early returns here!) ---
            
            # Rule 3: Duration Match 
            if mb_duration > 0 and abs(mb_duration - spotify_duration_ms) <= 3000:
                # Add every ISRC in this matched recording to our strict pool
                for isrc in isrc_list:
                    strict_isrcs.add(isrc)
            
            # Fallback: If duration is missing entirely on MusicBrainz, save it just in case
            elif mb_duration == 0:
                for isrc in isrc_list:
                    fallback_isrcs.add(isrc)

        # --- EVALUATE AND RETURN (After the loop finishes processing all 15) ---
        
        if strict_isrcs:
            print(f"Match found! Aggregated {len(strict_isrcs)} possible ISRCs.")
            return list(strict_isrcs)
            
        if fallback_isrcs:
            print(f"No exact duration matches, but found {len(fallback_isrcs)} fallback ISRCs with missing duration data.")
            return list(fallback_isrcs)
            
        print("No exact studio match found within the duration threshold.")
        return []

    except Exception as e:
        print(f"MusicBrainz API Error: {e}")
        return []

# --- Example Usage ---
# isrcs = get_canonical_studio_isrc("Taylor Swift", "The Fate of Ophelia", 226000) 
# print(f"Final ISRC List: {isrcs}")

# --- Example Usage ---
# Using data specifically extracted from your Spotify JSON payloads:
# Title: "Babydoll" | Artist: "Dominic Fike" | Duration: 97960ms
# isrc = new("Taylor Swift", "The Fate of Ophelia", 226000)  # Using the Spotify duration for better matching
# print(f"Final ISRC: {isrc}")