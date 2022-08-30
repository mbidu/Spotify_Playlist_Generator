import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import pandas as pd
import re

def plot_pie(x,y):
    # with plt.style.context('dark_background'):
    colors = cm.turbo(np.arange(len(x))/(len(x)))

    # plot
    fig, ax = plt.subplots()
    ax.axis(False)
    ax.pie(x,labels = y, autopct='%0.1f%%',textprops={'color':"black"},colors=colors,
            wedgeprops={"linewidth": 1, "edgecolor": "black"}, frame=True, startangle=90, pctdistance = 0.85)

    plt.tight_layout()
    plt.show()

def addlabels(x,y,colors):
    for i in range(len(x)):
        plt.text(i,y[i]+0.01,y[i],color = colors[i])

def plot_bar(x,y):
    colors = cm.turbo(np.arange(len(y)+1)/(len(y)+1))
    # plot
    plt.bar(x, y, color = colors, edgecolor='black')
    # calling the function to add value labels
    addlabels(x, y, colors)
    # giving title to the plot
    plt.title("Top 10")
    # giving X and Y labels
    plt.ylabel("Song Appearances")
    plt.xticks(range(len(x)), x, rotation=90)
    plt.show()

def artistsgenres_dummies(df):
    ############ Artists Dummies ############
    df_artists = df.copy()

    for index, row in df.iterrows():
        i = 0
        try:
            while row['artists_info']['ar_name{0}'.format(i)]:
                df_artists.at[index, row['artists_info']['ar_name{0}'.format(i)]] = 1
                i += 1
        except KeyError:
            pass
    df_artists = df_artists.fillna(0)
    df_artists = df_artists.drop(['artists_info'], 1)
    df_artists.to_csv('Playlist_artists.csv', encoding='utf-8', index = False)

    num_artists = df_artists.shape[1] - df.shape[1]
    artists_cols = df_artists.iloc[:,-num_artists:]

    artists_count = artists_cols.isin([1]).sum(axis=0)

    ac = list(artists_count)
    ac = np.array(ac).reshape((-1, 1))
    l = np.array(artists_cols.columns).reshape((artists_cols.columns.size, 1))

    ac = np.hstack((ac,l))
    ac = ac[ac[:, 0].argsort()]
    a = ac[-10:,:]

    x = a[:, :1]
    x = np.ndarray.tolist(x.reshape(1,-1)[0])
    y = a[:, 1:]
    y = np.ndarray.tolist(y.reshape(1,-1)[0])
    y = [re.sub('\$', 'S', item) for item in y]

    print("There are {0} unique artists in the playlist.".format(num_artists))
    plot_bar(y,x)

    other_count = np.sum(ac[:-10, :1])
    other = np.array([other_count,'Other']).reshape((1, -1))
    a = np.vstack((ac[-10:,:],other))

    x = a[:, :1]
    x = np.ndarray.tolist(x.reshape(1,-1)[0])
    y = a[:, 1:]
    y = np.ndarray.tolist(y.reshape(1,-1)[0])
    y = [re.sub('\$', 'S', item) for item in y]

    plot_pie(x,y)

    # ############ Genres Dummies ############

    df_artistsgenres = df_artists.copy()

    for index, row in df_artists.iterrows():
        for genre in row['genres']:
            df_artistsgenres.at[index, genre] = 1
    df_artistsgenres = df_artistsgenres.fillna(0)
    df_artistsgenres = df_artistsgenres.drop(['genres'], 1)
    df_artistsgenres.to_csv('Playlist_artistsgenres.csv', encoding='utf-8', index = False)

    num_genres = df_artistsgenres.shape[1] - df_artists.shape[1]
    genres_cols = df_artistsgenres.iloc[:,-num_genres:]

    genres_count = genres_cols.isin([1]).sum(axis=0)

    gc = list(genres_count)
    gc = np.array(gc).reshape((-1, 1))
    l = np.array(genres_cols.columns).reshape((genres_cols.columns.size, 1))

    gc = np.hstack((gc,l))
    gc = gc[gc[:, 0].argsort()]
    a = gc[-10:,:]
    x = a[:, :1]
    x = np.ndarray.tolist(x.reshape(1,-1)[0])
    y = a[:, 1:]
    y = np.ndarray.tolist(y.reshape(1,-1)[0])

    print("There are {0} unique genres in the playlist.".format(num_genres))

    plot_bar(y,x)

    other_count = np.sum(gc[:-10, :1])
    other = np.array([other_count,'Other']).reshape((1, -1))
    a = np.vstack((gc[-10:,:],other))
    x = a[:, :1]
    x = np.ndarray.tolist(x.reshape(1,-1)[0])
    y = a[:, 1:]
    y = np.ndarray.tolist(y.reshape(1,-1)[0])

    plot_pie(x,y)

    # df_no_artists = df_artistsgenres.iloc[:,:df.shape[1]]
    # df_trackparams = df_artistsgenres.iloc[:,-num_genres:]
    # df_genres = pd.concat([df_no_artists,df_trackparams], axis = 1)

    return df_artistsgenres, num_artists, num_genres