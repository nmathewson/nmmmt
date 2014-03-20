#!/usr/bin/python3

#   This software has been dedicated to the public domain under the CC0
#   public domain dedication.
#
#   To the extent possible under law, the person who associated CC0 with
#   this script has waived all copyright and related or neighboring rights.
#
#   You should have received a copy of the CC0 legalcode along with this
#   work in doc/cc0.txt.  If not, see
#      <http://creativecommons.org/publicdomain/zero/1.0/>.

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
