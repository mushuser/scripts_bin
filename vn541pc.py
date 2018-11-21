#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# sudo systemctl list-units -t mount
#
# /etc/systemd/system/vn541pc.service
#
# [Unit]
# Description=VN541PC Script
# Requires=media-user-VN_541PC.mount
# After=media-user-VN_541PC.mount
# 
# [Service]
# ExecStart=/home/user/bin/vn541pc.py
# 
# [Install]
# WantedBy=media-user-VN_541PC.mount


import os
import re
from datetime import datetime, timedelta
import time
import sys
from shutil import copy2
import subprocess

import urllib2

def internet_on():
    try:
        urllib2.urlopen('https://drive.google.com', timeout=5)
        return True
    except urllib2.URLError as err: 
        return False


def check_files(paths):
    os.chdir(GD_PATH)
    files = []
    
    output = ""
    for path in paths:
        print "Checking %s files" % path
        GD_CMD_LIST_CHECK=[GDRIVE_PATH, "list", path]
        output = output + subprocess.check_output(GD_CMD_LIST_CHECK)

    for filename in os.listdir(DEST_DIR):
        fullf = os.path.join(DEST_DIR, filename)
        if filename.lower().endswith(ext) and (len(filename)==len("20181113_0917_0691.WMA")):
            if (filename not in output):
                files.append(filename)

    for f in files:
        print "pushing: %s" % f

    return files


MEDIA_DIR="/media/user/VN_541PC/RECORDER/"
MEDIA_SUBDIRS=['MEMO', 'TALK', 'MUSIC', 'LP']
DEST_DIR="/home/user/VN541PC/"

while not os.path.exists(MEDIA_DIR):
    time.sleep(1)

ext = ".wma"

FNULL = open(os.devnull, 'w')

# copy to local
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


if not internet_on():
    sys.exit(1)

# push to drive
GDRIVE_PATH="/home/user/gopath/bin/drive"
GD_PATH=DEST_DIR
GD_BACKUP_PATH="錄音/WMA"
GD_CHECK_PATHS=["錄音/WMA_COMPLETED", "錄音/WMA_OVERSIZED", GD_BACKUP_PATH]
GD_CMD_PUSH_FILES=[GDRIVE_PATH, "push", "-no-prompt", "-destination", GD_BACKUP_PATH]

files = check_files(GD_CHECK_PATHS)

if len(files) > 0:
    cmd = GD_CMD_PUSH_FILES + files
    os.chdir(GD_PATH)
    output = subprocess.check_output(cmd)
    print "%d files pushed" % len(files)
else:
    print "no files pushed"
