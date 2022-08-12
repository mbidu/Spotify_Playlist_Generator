import pandas as pd

def df_duplicates(lib):
    # df = pd.DataFrame(lib)
    df = pd.DataFrame.from_dict(lib, orient='index')
    df2 = df['artists_info'].apply(pd.Series)
    df3 = pd.concat([df.drop(['artists_info'], axis=1), df2], axis=1)

    # Sort Alphabetically by Artist -> Album -> Song
    df3 = df3.sort_values(['artists', 'album', 'song'], ascending = True, key = lambda col: col.str.lower())

    # Track IDs
    sl_tr_id = list(range(1,len(df)+1))
    df3['id'] = sl_tr_id

    return df3