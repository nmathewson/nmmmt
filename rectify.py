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
import hashlib

H = hashlib.sha256

def find_dirs_with(d, ftype):
    for fn in sorted(os.listdir(d)):
        path = os.path.join(d,fn)
        if os.path.isdir(path):
            yield from find_dirs_with(path, ftype)
        elif fn.endswith(ftype):
            yield d
            break

def dir_contents(d, ftype):
    return tuple([ fn[:-len(ftype)] for fn in sorted(os.listdir(d))
                                     if fn.endswith(ftype) ])

def rename_dir(a,b):
    parent = os.path.split(b)[0]
    if not os.path.exists(parent):
        os.makedirs(parent)
    os.rename(a,b)

    a = os.path.split(a)[0]
    while a:
        try:
            os.rmdir(a)
            print("removed",a)
        except OSError:
            return
        aprime = os.path.split(a)[0]
        if aprime == a:
            # oh dear
            return
        a = aprime


def rectify(flactop, oggtop):

    # find all directories with flacs
    flacdirs = list(find_dirs_with(flactop, ".flac"))

    # find all diretories with oggs
    oggdirs = list(find_dirs_with(oggtop, ".ogg"))

    flacdir_by_contents = { dir_contents(d,".flac"):d for d in flacdirs }
    for flacdir in flacdirs:
        other = flacdir_by_contents[dir_contents(flacdir, ".flac")]
        if other != flacdir:
            print("Why do you have duplicate", flacdir, "and", other)

    oggdir_by_contents = { dir_contents(d,".ogg"):d for d in oggdirs }

    for oggdir in oggdirs:
        c = dir_contents(oggdir, ".ogg")
        if c not in flacdir_by_contents:
            print("Where did", oggdir, "come from?")
            continue

        if oggdir_by_contents[c] != oggdir:
            print("Why do you have duplicate",oggdir,"and",oggdir_by_contents[c])
            continue

        flacdir = flacdir_by_contents[c]

        assert flacdir.startswith(flactop)
        assert oggdir.startswith(oggtop)

        flacrest = flacdir[len(flactop):]

        if flacrest != oggdir[len(oggtop):]:
            print("Renaming",oggdir,"to",oggtop+flacrest)
            rename_dir(oggdir, oggtop+flacrest)


rectify("flac_rip", "ogg_rip")
rectify("flac_dl", "ogg_flacdl")
