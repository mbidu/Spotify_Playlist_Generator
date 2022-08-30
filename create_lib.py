# Spotify Modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Time Modules
from datetime import datetime
import time

# Printing in Multiprocessing
import sys
# Multiprocessing
import multiprocessing

# Import Scripts
from filter_to_match import filter_to_match
from get_credentials import get_credentials

def lib_dics(x):

    track = x[0]
    l = x[1]

    # sys.stdout.write(str(l))
    # time.sleep(1)

    cid,secret = get_credentials()
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    lib = {}

    lib[l] = {}

    # Track ID
    lib[l]["id"] = l

    # Track Name and URI
    track_uri = track["track"]["uri"]
    track_name = track["track"]["name"]
    track_name_fil = filter_to_match(track_name)

    lib[l]["song"] = track_name
    lib[l]["song_fil"] = track_name_fil


    # Artists Name and uri
    track_artists_name = []
    track_artists_name_fil = []
    track_artists_uri = []

    lib[l]["artists_info"] = {}
    i = 0
    while i >= 0:
        an = track["track"]["artists"][i]["name"]
        an_fil = filter_to_match(an)
        au = track["track"]["artists"][i]["uri"]

        lib[l]["artists_info"]["ar_name{0}". format(i)] = an
        lib[l]["artists_info"]["ar_name{0}_fil". format(i)] = an_fil
        lib[l]["artists_info"]["ar_uri{0}". format(i)] = au

        track_artists_name.append(an)
        track_artists_name_fil.append(an_fil)
        track_artists_uri.append(au)

        i = i + 1
        try: track["track"]["artists"][i]["name"]
        except IndexError:

            space = ", "
            str_artists = space.join(track_artists_name)
            str_artists_fil = space.join(track_artists_name_fil)

            lib[l]["artists"] = str_artists
            lib[l]["artists_fil"] = str_artists_fil
            break

    # Track Album
    alb = track["track"]["album"]["name"]
    lib[l]["album"] = alb
    lib[l]["album_fil"] = filter_to_match(alb)

    genres = []

    # Local Tracks
    if track['is_local'] == True:
        # 1. Album/Track Release Date
        lib[l]["date"] = ''
        # 2. Local/Spotify
        lib[l]["local"] = 'Yes'
        # 4. Track Audio Features
        lib[l]["time"] = track["track"]["duration_ms"]
    # Spotify Tracks
    else:
        # 1. Album/Track Release Date
        track_release_date = sp.track(track_uri)["album"]["release_date"]
        if sp.track(track_uri)["album"]["release_date_precision"] == 'day':
            track_release_date = str(datetime.strptime(track_release_date, "%Y-%m-%d").date())
        elif sp.track(track_uri)["album"]["release_date_precision"] == 'month':
            track_release_date = datetime.strptime(track_release_date, "%Y-%m").date()
        elif sp.track(track_uri)["album"]["release_date_precision"] == 'year':
            track_release_date = str(datetime.strptime(track_release_date, "%Y").date())
        lib[l]["date"] = track_release_date
        # 2. Local/Spotify
        lib[l]["local"] = 'No'
        # 3. Artist/Track Genres
        for i in range (len(track["track"]["artists"])):
            artist_genres = sp.artist(track["track"]["artists"][i]["id"])["genres"]
            genres = genres + artist_genres
        # 4. Track Audio Features
        feature_aud = sp.audio_features(track_uri)[0]
        lib[l]["time"] = feature_aud["duration_ms"]
        lib[l]["danceability"] = feature_aud["danceability"]
        lib[l]["energy"] = feature_aud["energy"]
        lib[l]["key"] = feature_aud["key"]
        lib[l]["loudness"] = feature_aud["loudness"]
        lib[l]["mode"] = feature_aud["mode"]
        lib[l]["speechiness"] = feature_aud["speechiness"]
        lib[l]["acousticness"] = feature_aud["acousticness"]
        lib[l]["instrumentalness"] = feature_aud["instrumentalness"]
        lib[l]["liveness"] = feature_aud["liveness"]
        lib[l]["valence"] = feature_aud["valence"]
        lib[l]["tempo"] = feature_aud["tempo"]

    lib[l]["genres"] = genres

    # Track Popularity
    lib[l]["popularity"] = track["track"]["popularity"]

    lib[l]["uri"] = track_uri

    return lib

def create_lib(tracks):

    l = list(range(len(tracks)))

    cpu_count = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cpu_count)

    lib = {}
    ldic = pool.map(lib_dics, zip(tracks,l))

    pool.close()
    pool.join()

    for item in ldic:
        lib |= item
    # for i in range(len(tracks)):
    #     lib = lib_dics(tracks[i],l[i])

    return lib