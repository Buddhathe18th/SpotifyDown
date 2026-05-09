import json
import glob
import os

def getArtists(artists_items: list) -> list:
    """Helper to extract a list of artist names from the GraphQL artist array."""
    artist_list = []
    for artist in artists_items:
        name = artist.get("profile", {}).get("name")
        if name:
            artist_list.append(name)
    return artist_list


def parse_intercepted_playlists(dump_dir: str = "spotify_payloads") -> list:
    """
    Parses intercepted GraphQL payloads by first identifying the playlist name
    from the header payload and applying it to all paginated tracks.
    """
    extracted_tracks = []
    seen_uris = set()
    playlist_name = "Unknown Playlist"
    
    search_pattern = os.path.join(dump_dir, "TRACK_DATA_part_*.json")
    payload_files = glob.glob(search_pattern)
    
    # --- FIRST PASS: Find the Playlist Name ---
    for file_path in payload_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
                # The name is only in the payload where offset is 0
                found_name = payload.get("data", {}).get("playlistV2", {}).get("name")
                if found_name:
                    playlist_name = found_name
                    break # Stop looking once we find it
        except Exception:
            continue

    # --- SECOND PASS: Extract Tracks ---
    for file_path in payload_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
                
                # Navigate to items array
                items = payload.get("data", {}).get("playlistV2", {}).get("content", {}).get("items", [])
                
                for item in items:
                    track_data = item.get("itemV2", {}).get("data", {})
                    if not track_data: continue
                    
                    uri = track_data.get("uri")
                    name = track_data.get("name")
                    
                    if name and uri and uri not in seen_uris:
                        seen_uris.add(uri)
                        
                        album_data = track_data.get("albumOfTrack", {})
                        
                        # Grab image URL from the sources list
                        image_url = None
                        cover_sources = album_data.get("coverArt", {}).get("sources", [])
                        if cover_sources:
                            image_url = cover_sources[0].get("url")
                        
                        song = {
                            "image_url": image_url,
                            "album": album_data.get("name"),
                            "artists": getArtists(track_data.get("artists", {}).get("items", [])),
                            "isrc": None,
                            "name": name,
                            "playlist": playlist_name  # Use the name found in the first pass
                        }
                        extracted_tracks.append(song)
                        
        except Exception as e:
            print(f"Error parsing tracks in {file_path}: {e}")

    return extracted_tracks