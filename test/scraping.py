import os
import json
from playwright.sync_api import sync_playwright

# FIX: Import the new Stealth class
from playwright_stealth import Stealth

def dump_payloads_to_disk(captured_jsons: list, dump_dir: str = "spotify_payloads"):
    """
    Safely writes intercepted JSON payloads to disk, automatically identifying 
    and renaming the specific files that contain track metadata.
    """
    os.makedirs(dump_dir, exist_ok=True)
    
    # Recursive helper to find if the payload contains track metadata
    # Recursive helper to find if the payload contains the GraphQL track structure
    def has_track_data(node):
        if isinstance(node, list):
            return any(has_track_data(i) for i in node)
        elif isinstance(node, dict):
            # Structural Signature Check: 
            # Is this dictionary a Playlist Page or a Track Wrapper?
            if node.get('__typename') in ['PlaylistItemsPage', 'TrackResponseWrapper']:
                return True
            
            # If not, keep digging deeper into the dictionary's values
            return any(has_track_data(v) for v in node.values())
        return False

    track_count = 0
    generic_count = 0

    for payload in captured_jsons:
        # Evaluate the payload in memory to determine its filename
        if has_track_data(payload):
            filename = f"TRACK_DATA_part_{track_count}.json"
            track_count += 1
        else:
            filename = f"payload_{generic_count}.json"
            generic_count += 1
            
        try:
            file_path = os.path.join(dump_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4)
        except Exception as e:
            print(f"Failed to write to {filename}: {e}")

    print(f"Extraction complete: Saved {track_count} track payloads and {generic_count} generic payloads.")

def extract_isrcs_stealth(playlist_url: str):
    captured_jsons = []

    def handle_response(response):
        if response.request.resource_type in ["xhr", "fetch"] and response.status == 200:
            try:
                captured_jsons.append(response.json())
            except:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # FIX: Explicitly create a browser context
        context = browser.new_context()
        
        # FIX: Apply the new Stealth class to the entire context
        stealth = Stealth()
        stealth.apply_stealth_sync(context)
        
        # FIX: Open the page from the armored context
        page = context.new_page()
        
        page.on("response", handle_response)
        
        try:
            page.goto(playlist_url, wait_until="domcontentloaded")
            page.wait_for_selector('[data-testid="tracklist-row"]', state="attached", timeout=15000)
            print("Page loaded successfully, processing network traffic...")

            # FIX: Click the page to ensure focus, then simulate human scrolling
            page.click("body")
            
            print("Scrolling down to fetch remaining tracks...")
            # Loop a few times to ensure we hit the bottom of the 50-song list
            for _ in range(4):
                page.keyboard.press("PageDown")
                page.wait_for_timeout(1000)  # Wait 1 second between scrolls for API to fire
            
            # Final wait to ensure the last network packet finishes downloading
            page.wait_for_timeout(3000)
            
        except Exception as e:
            print(f"Navigation or rendering failed: {e}")
            return None
        finally:
            browser.close()

    dump_payloads_to_disk(captured_jsons)
    print(f"Dumped {len(captured_jsons)} payloads to disk. Please check the folder.")
    return captured_jsons