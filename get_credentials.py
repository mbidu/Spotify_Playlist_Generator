def get_credentials():
    # Reading the Client ID and Client Secret from the .txt file to
    # access my Spotify Developer App.
    with open(r"spotify_app_credentials.txt") as f:
        sac_lines = f.readlines()
        cid = sac_lines[0].split(", ")
        cid = cid[1].split("\n")
        cid = cid[0]
        secret = sac_lines[1].split(", ")
        secret = secret[1]
    return cid,secret