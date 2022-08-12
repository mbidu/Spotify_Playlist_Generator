def get_uniques(Duplicate_Index):
    # Number of [non-duplicate songs, duplicates of song 3, duplicates of song 5,...]
    # num_uniques [#nd, #song3, #song5...]
    num_uniques = []

    # Labeling uniques and duplicates
    # uniques = [-1, 1 , 2...]
    uniques = list(set(Duplicate_Index))
    uniques.sort()

    for i in range (len(uniques)):
        count = Duplicate_Index.count(uniques[i])
        num_uniques.append(count)

    print("duplicate_index\n",Duplicate_Index)
    print("uniques\n",uniques)
    print("Amount per uniques\n",num_uniques)

    return uniques, num_uniques