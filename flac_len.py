#!/usr/bin/python3

import os
import sys
import subprocess

def flac_len(fname):
    p = subprocess.Popen(["metaflac", "--list", fname], stdout=subprocess.PIPE)
    stdout,stderr = p.communicate()
    hz = 44100
    samples = 44100
    for line in stdout.split(b"\n"):
        if line.startswith(b"  sample_rate: "):
            hz = int(line.split()[1])
        elif line.startswith(b"  total samples: "):
            samples = int(line.split()[-1])

    return float(samples)/hz

for f in sys.argv[1:]:
    seconds = flac_len(f)
    bytes = os.stat(f).st_size
    ratio = float(bytes)/seconds

    print("{0} {1}".format(int(ratio), f))

