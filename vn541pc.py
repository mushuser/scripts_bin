#!/usr/bin/env python
# sudo systemctl list-units -t mount

import os
import re
from datetime import datetime, timedelta
import time
import sys
from shutil import copy2

MEDIA_DIR="/media/user/VN_541PC/RECORDER/"
MEDIA_SUBDIRS=['MEMO', 'TALK', 'MUSIC', 'LP']
DEST_DIR="/home/user/VN541PC/"

while not os.path.exists(MEDIA_DIR):
    time.sleep(1)

directory = "./"
ext = ".wma"
FNULL = open(os.devnull, 'w')

for sub in MEDIA_SUBDIRS:
    fulldir = os.path.join(MEDIA_DIR, sub)
    for filename in os.listdir(fulldir):
        if filename.lower().endswith(ext) and (len(filename)==len("180424_0034.WMA")):
            oldf = os.path.join(fulldir, filename)

            mtime = os.stat(oldf).st_mtime
            newtime = datetime.fromtimestamp(mtime) - timedelta(hours=8)
            newmtime = time.mktime(newtime.timetuple())
            seq = re.match(r"\d+_(\d+)", filename).group(1)
            newf = newtime.strftime('%Y%m%d_%H%M') + "_" + seq + ext.upper()
            newfullf = os.path.join(DEST_DIR, newf)
            if not os.path.isfile(newfullf):
                print "copying: %s to %s" % (filename, newf)
                copy2(oldf, newfullf)
                os.utime(newfullf, (newmtime, newmtime))
