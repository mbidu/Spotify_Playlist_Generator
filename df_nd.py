import pandas as pd

def df_no_duplicates(lib):

    # Sort Dictionary by popularity
    # lib = {k: v for k, v in sorted(lib.items(), key=lambda item: item[1]['popularity'], reverse = True)}
    lib = dict(sorted(lib.items(), key=lambda item: item[1]['popularity'], reverse = True))

    # for i in range(len(lib)):
    #     print(lib["track{0}". format(i)]['popularity'])

    # Remove Duplicates
    d = []
    lib_nd = {}

    for k, v in lib.items():
        if v["duplicates"]["dup_id"] not in d:
            if v["duplicates"]["dup_id"] != -1:
                d.append(v["duplicates"]["dup_id"])
            lib_nd[k] = v

    # Reset index
    lib_nd = {"track{0}".format(k): v for k, v in enumerate(lib_nd.values())}

    # for i in range(len(lib_nd)):
    #     print(lib_nd["track{0}". format(i)]['song'],lib_nd["track{0}". format(i)]['duplicates']["dup_id"], lib_nd["track{0}". format(i)]['popularity'])

    return lib_nd