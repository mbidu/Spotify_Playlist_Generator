import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def extract_playlist(playlist_link):
    # Reading the Client ID and Client Secret from the .txt file to
    # access my Spotify Developer App.
    with open(r"C:\Users\mackt\Python\Music Library\spotify_app_credentials.txt") as f:
        sac_lines = f.readlines()
        cid = sac_lines[0].split(", ")
        cid = cid[1].split("\n")
        cid = cid[0]
        secret = sac_lines[1].split(", ")
        secret = secret[1]

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

    return sp,tracks