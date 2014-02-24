#!/usr/bin/python

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
import shutil
import sys
import traceback

EXTS = [".mp3", ".ogg"]

def is_music_file(f):
    return any(f.endswith(e) for e in EXTS)

def music_size(f):
    sz = 0
    for fn in os.listdir(f):
        if is_music_file(fn):
            sz += os.stat(os.path.join(f,fn)).st_size
    return sz

def is_uptodate(oldfile, newfile):
    if not os.path.exists(newfile):
        return False

    if os.stat(newfile).st_size != os.stat(oldfile).st_size:
        return False

    return True

def clean_name(name):
    return name.translate(None, "?!")

def copy_music_dir(d1,d2):
    if not os.path.isdir(d2):
        os.makedirs(d2)

    for fn in os.listdir(d1):
        if is_music_file(fn) and not is_uptodate(os.path.join(d1,fn), os.path.join(d2,fn)):

            try:
                shutil.copy(os.path.join(d1,fn), d2)
            except IOError, e:
                fn2 = clean_name(fn)
                if not is_uptodate(os.path.join(d1,fn), os.path.join(d2,fn2)):
                    try:
                        shutil.copy(os.path.join(d1,fn), os.path.join(d2,fn2))
                    except IOError, e:
                        traceback.print_exc()
def is_music_dir(x):
    if not os.path.isdir(x):
        return False
    for fn in os.listdir(x):
        if is_music_file(fn):
            return True
    return False

def albums_in(d):
    for d1 in os.listdir(d):
        for d2 in os.listdir(os.path.join(d,d1)):
            if is_music_dir(os.path.join(d,d1,d2)):
                yield (d,d1,d2)

def parse_file(f):
    status = {}
    for line in open(f):
        pre,rest = line.split("\t",1)
        if pre:
            status[rest.strip()] = pre.strip()

    return status

DIRS = ["misc_dl", "misc_rip", "ogg_flacdl", "ogg_rip"]

ALBUMS = []

if sys.argv[1] == 'make_list':

    if len(sys.argv) > 2:
        status = parse_file(sys.argv[2])
    else:
        status = {}

    for d in DIRS:
        ALBUMS += [ "%s/%s"%(d1,d2) for _,d1,d2 in albums_in(d) ]

    ALBUMS.sort()
    for line in ALBUMS:
        s = status.get(line, "")
        print "%s\t%s"%(s,line)

elif sys.argv[1] == 'list_size' or sys.argv[1] == 'list_copy':

    name_to_dir = {}

    for d in DIRS:
        for (d0,d1,d2) in albums_in(d):
            name_to_dir["%s/%s"%(d1,d2)] = (d,d1,d2)

    status = parse_file(sys.argv[2])

    missing = False
    for s in status.keys():
        if s not in name_to_dir:
            print "WHERE IS",s
            missing = True
    if missing:
        sys.exit(1)

    if sys.argv[1] == 'list_size':
        sz = 0
        for s in status.keys():
            if len(status[s]):
                sz += music_size(os.path.join(*name_to_dir[s]))

        if sz < 1e9:
            print (sz >> 20), "MB"
        else:
            print "%.02f GB"% (sz / float(1 << 30))

    elif sys.argv[1] == 'list_copy':
        if not os.path.isdir(sys.argv[3]):
            print "NO DESTINATION!"
            sys.exit(1)

        for s in status.keys():
            if len(status[s]):
                d0,d1,d2 = name_to_dir[s]
                print d1,d2
                copy_music_dir(os.path.join(d0,d1,d2),
                               os.path.join(sys.argv[3],d1,d2))


