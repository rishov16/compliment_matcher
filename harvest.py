import os
import json
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load API credentials from the .env file
load_dotenv()

# Define the permissions we need (reading your liked songs)
SCOPE = "user-library-read"

def get_spotify_client():
    """Authenticates with Spotify using the explicit loopback IP"""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=SCOPE,
        open_browser=True
    ))

def harvest_liked_songs():
    sp = get_spotify_client()
    print("Connecting to Spotify... Your browser might pop up to ask for permission.")
    
    liked_tracks = []
    offset = 0
    limit = 50  # Spotify's maximum batch size

    while True:
        print(f"Fetching songs {offset} to {offset + limit}...")
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        items = results.get('items', [])
        
        if not items:
            break
            
        for item in items:
            track = item['track']
            # Extract just the useful information
            liked_tracks.append({
                "id": track["id"],
                "title": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                "album": track["album"]["name"]
            })
            
        offset += len(items)
        if len(items) < limit:
            break  # Reached the end of your library

    # Save the harvested data locally to a JSON file
    output_file = "my_liked_songs.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(liked_tracks, f, indent=4, ensure_ascii=False)
        
    print(f"\nSuccess! Saved {len(liked_tracks)} tracks to {output_file}")

if __name__ == "__main__":
    harvest_liked_songs()