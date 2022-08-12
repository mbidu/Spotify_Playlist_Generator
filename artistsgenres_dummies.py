import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import pandas as pd

def plot_pie(x,labels):
    # with plt.style.context('dark_background'):
    colors = cm.turbo(np.arange(len(x))/(len(x)))

    # plot
    fig, ax = plt.subplots()
    ax.axis(False)
    ax.pie(x,labels = labels, autopct='%1.0f%%',radius=3, center=(4, 4),textprops={'color':"black"},colors=colors,
            wedgeprops={"linewidth": 1, "edgecolor": "black"}, frame=True)

    ax.set(xlim=(0, 1), xticks=np.arange(1, 8),
            ylim=(0, 1), yticks=np.arange(1, 8))

    plt.show()

def plot_bar(labels,y):
    import matplotlib.pyplot as plt
    import numpy as np

    colors = cm.turbo(np.arange(len(y))/(len(y)))

    # plot
    fig, ax = plt.subplots()

    ax.bar(labels, y, labels = labels, width=1, edgecolor="white", colors = colors,linewidth=0.7)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        ylim=(0, 8), yticks=np.arange(1, 8))

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
    artists_cols.value_counts()

    artists_count = artists_cols.isin([1]).sum(axis=0)

    ac = list(artists_count)
    ac = np.array(ac).reshape((-1, 1))
    l = np.array(artists_cols.columns).reshape((artists_cols.columns.size, 1))

    ac = np.hstack((ac,l))
    ac = ac[ac[:, 0].argsort()]

    # other_count = np.sum(ac[:-10, :1])
    # other = np.array([other_count,'Other']).reshape((1, -1))

    # a = np.vstack((ac[-10:,:],other))
    a = ac[:,:10]

    x = a[:, :1]
    x = np.ndarray.tolist(x.reshape(1,-1)[0])
    y = a[:, 1:]
    y = np.ndarray.tolist(y.reshape(1,-1)[0])
    import re
    y = [re.sub('\$', 'S', item) for item in y]

    print("There are {0} unique artists in the playlist.".format(num_artists))
    plot_bar(x,y)

    ############ Genres Dummies ############

    df_artistsgenres = df_artists.copy()

    for index, row in df_artists.iterrows():
        for genre in row['genres']:
            df_artistsgenres.at[index, genre] = 1
    df_artistsgenres = df_artistsgenres.fillna(0)
    df_artistsgenres = df_artistsgenres.drop(['genres'], 1)
    df_artistsgenres.to_csv('Playlist_artists.csv', encoding='utf-8', index = False)

    num_genres = df_artistsgenres.shape[1] - df_artists.shape[1]
    genres_cols = df_artistsgenres.iloc[:,-num_genres:]
    genres_count = genres_cols.isin([1]).sum(axis=0)

    gc = list(genres_count)
    gc = np.array(gc).reshape((-1, 1))
    l = np.array(genres_cols.columns).reshape((genres_cols.columns.size, 1))
    gc = np.hstack((gc,l))
    gc = gc[gc[:, 0].argsort()]

    # other_count = np.sum(gc[:-10, :1])
    # other = np.array([other_count,'Other']).reshape((1, -1))
    # a = np.vstack((gc[-10:,:],other))
    a = gc

    x = a[:, :1]
    x = np.ndarray.tolist(x.reshape(1,-1)[0])
    y = a[:, 1:]
    y = np.ndarray.tolist(y.reshape(1,-1)[0])

    print("There are {0} unique genres in the playlist.".format(num_genres))
    plot_bar(x,y)

    # df_no_artists = df_artistsgenres.iloc[:,:df.shape[1]]
    # df_trackparams = df_artistsgenres.iloc[:,-num_genres:]
    # df_genres = pd.concat([df_no_artists,df_trackparams], axis = 1)

    return df_artistsgenres, num_artists, num_genres