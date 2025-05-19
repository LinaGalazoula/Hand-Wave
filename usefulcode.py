import os
from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-playback-state,user-modify-playback-state,user-top-read,user-library-read,user-read-recently-played"
))

# Ensure there's an active device
devices = sp.devices()['devices']
active_device = next((d for d in devices if d['is_active']), None)
if not active_device:
    print("⚠️ No active device. Open Spotify on a device and play something.")
    exit()

device_id = active_device['id']

# Change volume
sp.volume(100, device_id=device_id)
sleep(2)
sp.volume(50, device_id=device_id)
sleep(2)
sp.volume(100, device_id=device_id)

# Start a specific track
sp.start_playback(device_id=device_id, uris=['spotify:track:6gdLoMygLsgktydTQ71b15'])

# Define some seed track IDs (example)
seed_track_ids = ['6gdLoMygLsgktydTQ71b15']

# Get recommendations
recommendations = sp.recommendations(seed_tracks=seed_track_ids[0:5], limit=10, country='US')

# Print recommendations
for i, track in enumerate(recommendations['tracks']):
    print(f"{i+1}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
