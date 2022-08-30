import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import csv
import numpy as np
import re

from get_credentials import get_credentials
from extract_playlist import extract_playlist
from artistsgenres_dummies import artistsgenres_dummies

from sklearn import preprocessing

def unl_data():

    cid,secret = get_credentials()

    # Adding the Playlist link and URI.
    # Liked Songs - 4000 songs
    # songs_to_add_link = "https://open.spotify.com/playlist/5F5yHyXHt6vp2taA7DrEhJ?si=b4f82e9651444f28"
    # # Gym - 500 songs
    # playlist_link = "https://open.spotify.com/playlist/5CYdyJ0w4OVc1oitZWQvj3?si=76db4826bb254432"

    # Liked Songs mask - 80 songs
    songs_to_add_link = "https://open.spotify.com/playlist/3ZqPfj9NrumTSN8mANanIK?si=bbded8c33a274d55"
    # Gym mask - 20 songs
    playlist_link = "https://open.spotify.com/playlist/5dFBFbT5ZmJruYvK8IVd6c?si=80cad7f1d80b49cd"

    # # Spotify Playlist Generator - 16 songs
    # playlist_link = "https://open.spotify.com/playlist/7LaicnuGlBjUoHZ5Rd4tjm?si=e9f47ebd992b4d08"

    # # NN Test
    # # Gym mask - 20 songs
    # songs_to_add_link = "https://open.spotify.com/playlist/5dFBFbT5ZmJruYvK8IVd6c?si=80cad7f1d80b49cd"

    df_p = extract_playlist(playlist_link,cid,secret)
    df_p.to_csv('Playlist_p.csv', encoding='utf-8', index = False)
    print(df_p.shape)
    df_sta = extract_playlist(songs_to_add_link,cid,secret)
    print(df_sta.shape)
    df_sta = df_sta.reset_index(drop=True)
    df_p = df_p.reset_index(drop=True)
    df_sta.to_csv('Playlist_sta.csv', encoding='utf-8', index = False)
    df_p.to_csv('Playlist_p.csv', encoding='utf-8', index = False)
    df_sta['in playlist'] = -2
    df_p['in playlist'] = 1
    ip = []

    # # df_unlabelled = df_sta_ag.loc[~((df_sta_ag.song_fil.isin(df_p['song_fil']))&(df_sta_ag.artists_fil.isin(df_p['artists_fil']))),:]
    for index, row in df_sta.iterrows():
        for index2, row2 in df_p.iterrows():
            if row['song_fil'] == row2['song_fil'] and row['artists_fil'] == row2['artists_fil']:
                print(row['song_fil'], row['artists_fil'])
                in_playlist = index
                ip.append(in_playlist)
    print(len(ip))
    print(ip)

    df_u = df_sta.copy()
    df_l = df_p.copy()

    df_u = df_u.drop(df_u.index[ip])

    df1 = df_u
    df2 = df_l

    df1['in playlist'] = -2
    df2['in playlist'] = 1

    df = pd.concat([df1, df2])
    df = df.reset_index(drop=True)
    df.to_csv('Playlist_df.csv', encoding='utf-8', index = False)
    df.drop(['local','song_fil','artists_fil','album_fil'], 1)
    df_ag, df_num_artists, df_num_genres = artistsgenres_dummies(df)

    df_ag.to_csv('Playlist_df_ag.csv', encoding='utf-8', index = False)

    tot1 = df_ag.shape[0]
    df_ag = df_ag.drop(df_ag[df_ag['date'] == ''].index)
    tot2 = df_ag.shape[0]
    tot = tot1-tot2
    print("There were %i local songs within both playlists. All are removed as they don't have any song parameters." %tot)
    df_ag = df_ag.reset_index(drop=True)

    df_trackparams = df_ag.iloc[:,7:21]
    df_trackgenres = df_ag.iloc[:,-(df_num_genres):]
    X = pd.concat([df_trackparams,df_trackgenres], axis = 1)
    X = X.drop(['local'], 1)

    X.to_csv('Playlist_X.csv', encoding='utf-8', index = False)

    X['date'] = X['date'].apply(lambda x: str(x))
    X['date'] = X['date'].apply(lambda x: re.split('-',x)[0])
    X['date'] = X['date'].apply(lambda x: int(x))

    X.iloc[:,:6] = preprocessing.StandardScaler().fit(X.iloc[:,:6]).transform(X.iloc[:,:6].astype(float))
    X.iloc[:,7:13] = preprocessing.StandardScaler().fit(X.iloc[:,7:13]).transform(X.iloc[:,7:13].astype(float))

    j = df_ag.columns.get_loc("in playlist")
    y = df_ag.iloc[:,j:j+1]

    y_pos = y[y['in playlist'] == 1]
    y_unl = y[y['in playlist'] == -2]

    X_pos = X.loc[y_pos.index]
    X_unl = X.loc[y_unl.index]

    pos_index = y_pos.index
    unl_index = y_unl.index

    pos = pd.concat((y_pos,X_pos),axis=1)
    unl = pd.concat((y_unl,X_unl),axis=1)

    num_pos = len(y_pos)
    num_unl = len(y_unl)

    print("There are %i songs in the current playlist." %num_pos)
    print("There are %i songs in your music library." %num_unl)

    return unl,pos,X