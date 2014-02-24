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

import re
import os
import subprocess

def find_flacs(d):
   for fn in sorted(os.listdir(d)):
      p = os.path.join(d,fn)
      if os.path.isdir(p):
         yield from find_flacs(p)
      elif p.endswith(".flac"):
         yield p

def oggify(flac, ogg):
   assert flac.endswith(".flac")
   flac_time = os.stat(flac).st_mtime
   try:
      ogg_time = os.stat(ogg).st_mtime
   except OSError:
      ogg_time = 0
   if ogg_time > flac_time:
      return
   parent = os.path.split(ogg)[0]
   if not os.path.exists(parent):
      os.makedirs(parent)
   print("=====>",ogg)
   subprocess.check_call(["oggenc", "-q", "5.3", "-o", ogg, flac])

BOGUS = []

def oggify_dir(d, d2):
   d_pat = "^"+d+"/(.*)\.flac$"

   for flac in find_flacs(d):
      p = re.match(d_pat, flac)
      assert p
      basename = p.group(1)
      ogg = (d2+"/%s.ogg") % basename

      try:
         oggify(flac, ogg)
      except subprocess.CalledProcessError:
         BOGUS.append(flac)


oggify_dir("flac_rip", "ogg_rip")
oggify_dir("flac_dl", "ogg_flacdl")

if BOGUS:
   print("Bogus files:",BOGUS)


