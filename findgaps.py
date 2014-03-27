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
import sys

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

def get_album_speed(d):
    files = []
    for f in os.listdir(d):
        st = os.stat(os.path.join(d,f))
        files.append((st.st_mtime, st.st_size))
    files.sort()
    total_time = files[-1][0] - files[0][0]
    total_size = sum(files[i][1] for i in range(1,len(files)))
    if total_time == 0:
        total_time = 1
    return float(total_size) / total_time

gaps=slow=False

if sys.argv[1] == 'gaps':
    gaps = True
else:
    slow = True

D = 'flac_rip'

album_speed = []

for artist in sorted(os.listdir(D)):
    if not os.path.isdir(os.path.join(D,artist)):
        continue
    for album in sorted(os.listdir(os.path.join(D,artist))):
        if not os.path.isdir(os.path.join(D,artist,album)):
            continue
        if gaps and not is_well_numbered(os.path.join(D,artist,album)):
            print(artist,album)
        if slow:
            s = get_album_speed(os.path.join(D,artist,album))
            album_speed.append((s,artist,album))

album_speed.sort()
for s,artist,album in album_speed:
    print(s,artist,album)
