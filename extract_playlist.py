import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

from create_lib import create_lib
def extract_playlist(playlist_link,cid,secret):
    # Passing the credentials through the Spotify API
    # # Authentication - without user
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    # Adding the Playlist link and URI.
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    # Spotify API only allows you to take 100 songs at a time.
    # This allows you to continue to take 100 songs as many times
    # as you can from the given playlist.
    results = sp.playlist_tracks(playlist_URI)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Create dictionary of songs and uplicate index for identifying duplicate and unique songs.
    lib = create_lib(tracks)
    lib = dict(sorted(lib.items(), key=lambda item: item[1]['popularity'], reverse = True))
    df = pd.DataFrame.from_dict(lib, orient='index')
    df = df.drop_duplicates(['song_fil','artists_fil'])

    return df