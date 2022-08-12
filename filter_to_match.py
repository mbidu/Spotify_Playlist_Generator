import re

def filter_to_match(word):
    word = word.lower() # All letter lowercase
    # word = re.sub(r'[^\x00-\x7F]','_', word)
    word = re.sub('(?= \(feat.)(.*?)(?<=\))', '', word)
    word = re.sub('(?= \(with)(.*?)(?<=\))', '', word)
    word = re.sub('(?= \(ft.)(.*?)(?<=\))', '', word)
    return word