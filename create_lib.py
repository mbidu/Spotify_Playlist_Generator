# Spotify Modules
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Time Modules
from datetime import datetime

# Import Scripts
from filter_to_match import filter_to_match

def create_lib(sp, tracks):

    lib = {}

    sl_tr_name = [] # Track names
    sl_tr_name_fil = [] # Filtered track names

    sl_tr_uri = [] # All song uris for each song

    sl_ar_uri = [] # All artists uris for each song

    Duplicate_Index = []

    l = 0

    for track in tracks:
        lib["track{0}". format(l)] = {}

        # Track ID
        lib["track{0}". format(l)]["id"] = l

        # Track Name and URI
        track_uri = track["track"]["uri"]
        track_name = track["track"]["name"]
        track_name_fil = filter_to_match(track_name)

        lib["track{0}". format(l)]["song"] = track_name
        lib["track{0}". format(l)]["song_fil"] = track_name_fil

        sl_tr_name.append(track_name)
        sl_tr_name_fil.append(track_name_fil)
        sl_tr_uri.append(track_uri)

        # Artists Name and uri
        track_artists_name = []
        track_artists_name_fil = []
        track_artists_uri = []

        lib["track{0}". format(l)]["artists_info"] = {}
        i = 0
        while i >= 0:
            an = track["track"]["artists"][i]["name"]
            an_fil = filter_to_match(an)
            au = track["track"]["artists"][i]["uri"]

            lib["track{0}". format(l)]["artists_info"]["ar_name{0}". format(i)] = an
            lib["track{0}". format(l)]["artists_info"]["ar_name{0}_fil". format(i)] = an_fil
            lib["track{0}". format(l)]["artists_info"]["ar_uri{0}". format(i)] = au

            track_artists_name.append(an)
            track_artists_name_fil.append(an_fil)
            track_artists_uri.append(au)

            i = i + 1
            try: track["track"]["artists"][i]["name"]
            except IndexError:
                sl_ar_uri.append(track_artists_uri)

                space = ", "
                str_artists = space.join(track_artists_name)
                str_artists_fil = space.join(track_artists_name_fil)

                lib["track{0}". format(l)]["artists"] = str_artists
                lib["track{0}". format(l)]["artists_fil"] = str_artists_fil
                break

        # Track Album
        alb = track["track"]["album"]["name"]
        lib["track{0}". format(l)]["album"] = alb
        lib["track{0}". format(l)]["album_fil"] = filter_to_match(alb)

        # Track Release Date + Local
        # Local Tracks
        if track['is_local'] == True:
            lib["track{0}". format(l)]["date"] = ''
            lib["track{0}". format(l)]["local"] = 'Yes'
        # Spotify Tracks
        else:
            track_release_date = sp.track(track_uri)["album"]["release_date"]
            if sp.track(track_uri)["album"]["release_date_precision"] == 'day':
                track_release_date = str(datetime.strptime(track_release_date, "%Y-%m-%d").date())
            elif sp.track(track_uri)["album"]["release_date_precision"] == 'month':
                track_release_date = datetime.strptime(track_release_date, "%Y-%m").date()
            elif sp.track(track_uri)["album"]["release_date_precision"] == 'year':
                track_release_date = str(datetime.strptime(track_release_date, "%Y").date())
            lib["track{0}". format(l)]["date"] = track_release_date
            lib["track{0}". format(l)]["local"] = 'No'

        # Track Genre
        print(track_name)
        genres = []
        if track['is_local'] == False:
            for i in range (len(track["track"]["artists"])):
                artist_genres = sp.artist(track["track"]["artists"][i]["id"])["genres"]
                genres = genres + artist_genres
        lib["track{0}". format(l)]["genres"] = genres

        # Track Duration
        feature_aud = sp.audio_features(track_uri)[0]

        if track['is_local'] == True:
            lib["track{0}". format(l)]["time"] = track["track"]["duration_ms"]
        else:
            lib["track{0}". format(l)]["time"] = feature_aud["duration_ms"]

        # Track Popularity
        lib["track{0}". format(l)]["popularity"] = track["track"]["popularity"]

        # Track Audio Features
        # Locals
        if track['is_local'] == False:
            lib["track{0}". format(l)]["danceability"] = feature_aud["danceability"]
            lib["track{0}". format(l)]["energy"] = feature_aud["energy"]
            lib["track{0}". format(l)]["key"] = feature_aud["key"]
            lib["track{0}". format(l)]["loudness"] = feature_aud["loudness"]
            lib["track{0}". format(l)]["mode"] = feature_aud["mode"]
            lib["track{0}". format(l)]["speechiness"] = feature_aud["speechiness"]
            lib["track{0}". format(l)]["acousticness"] = feature_aud["acousticness"]
            lib["track{0}". format(l)]["instrumentalness"] = feature_aud["instrumentalness"]
            lib["track{0}". format(l)]["liveness"] = feature_aud["liveness"]
            lib["track{0}". format(l)]["valence"] = feature_aud["valence"]
            lib["track{0}". format(l)]["tempo"] = feature_aud["tempo"]

        lib["track{0}". format(l)]["uri"] = track_uri

        # Duplicate Songs
        lib["track{0}". format(l)]["duplicates"] = {}
        lib["track{0}". format(l)]["duplicates"]["dup_id"] = -1
        lib["track{0}". format(l)]["duplicates"]["num_dup"] = 0

        same_tr_names = sl_tr_name_fil.count(track_name_fil)-1
        dup = 0
        if same_tr_names != 0:
            last_ind = 0
            # print(same_tr_names, "same name")
            for i in range(same_tr_names):
                index = sl_tr_name_fil.index(track_name_fil, last_ind)
                if sl_ar_uri[index] == track_artists_uri:
                    if dup == 0:
                        dup = 1
                        dup_id = index
                        Duplicate_Index.append(dup_id)
                        Duplicate_Index[index] = dup_id

                        lib["track{0}". format(l)]["duplicates"]["num_dup"] = dup
                        lib["track{0}". format(index)]["duplicates"]["num_dup"] = dup

                        lib["track{0}". format(l)]["duplicates"]["dup_id"] = dup_id
                        lib["track{0}". format(index)]["duplicates"]["dup_id"] = dup_id

                        lib["track{0}". format(index)]["duplicates"]["dup_loc{0}".format(dup-1)] = index

                    else:
                        lib["track{0}". format(l)]["duplicates"]["num_dup"] = dup

                    lib["track{0}". format(l)]["duplicates"]["dup_loc{0}".format(dup-1)] = index
                    lib["track{0}". format(l)]["duplicates"]["dup_loc{0}".format(dup)] = l

                    dup = dup + 1
                    # print(index, "+")
                elif i == same_tr_names-1 and dup == 0:
                    Duplicate_Index.append(-1)
                    # print(index, "-")

                last_ind = index+1

        else:
            Duplicate_Index.append(-1)

        dup = dup - 1
        iter = dup
        for x in range(dup):
            prev_tr = lib["track{0}". format(l)]["duplicates"]["dup_loc{0}".format(x)]
            lib["track{0}". format(prev_tr)]["duplicates"]["num_dup"] = dup
            iter = iter - x

            for y in range (iter):
                a = lib["track{0}". format(l)]["duplicates"]["dup_loc{0}".format(x+y+1)]
                lib["track{0}". format(prev_tr)]["duplicates"]["dup_loc{0}".format(x+y+1)] = a
        # print(Duplicate_Index)

        dup = lib["track{0}". format(l)]["duplicates"]["num_dup"]

        if dup >= 1:
            for i in range(dup+1):
                loc = lib["track{0}". format(l)]["duplicates"]["dup_loc{0}".format(i)]
                track_uri = lib["track{0}". format(loc)]["uri"]
                lib["track{0}". format(l)]["uri{0}".format(i)] = track_uri
        else:
            lib["track{0}". format(l)]["uri0"] = track_uri

        l = l+1

    # print(lib["track0"]["duplicates"])
    # print(lib["track1"]["duplicates"])
    # print(lib["track2"]["duplicates"])
    # print(lib["track3"]["duplicates"])
    # print(lib["track4"]["duplicates"])
    # print(lib["track5"]["duplicates"])
    # print(lib["track6"]["duplicates"])
    # print(lib["track7"]["duplicates"])
    # print(lib["track8"]["duplicates"])
    # print(lib["track9"]["duplicates"])
    # print(lib["track10"]["duplicates"])

    return lib, Duplicate_Index