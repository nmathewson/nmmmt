#!/usr/bin/python3

import os
import re

def get_track_num(fn):
    m = re.match(r'(\d+)[^a-zA-Z0-9]', fn)
    if m:
        return int(m.group(1))
    m = re.match(r'd\d+t(\d+)[^a-zA-Z0-9]', fn)
    if m:
        return int(m.group(1))
    return -1

def is_well_numbered(d):
    s = os.listdir(d)
    s.sort()
    for i, n in zip(range(1,len(s)+1), s):
        t = get_track_num(n)
        if t != i:
            print("!", (i, t, n))
            return False
    return True

D = 'flac_rip'

for artist in sorted(os.listdir(D)):
    if not os.path.isdir(os.path.join(D,artist)):
        continue
    for album in sorted(os.listdir(os.path.join(D,artist))):
        if not os.path.isdir(os.path.join(D,artist,album)):
            continue
        if not is_well_numbered(os.path.join(D,artist,album)):
            print(artist,album)
