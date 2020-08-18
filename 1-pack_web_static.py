#!/usr/bin/python3
# Generates a .tgz archive

from datetime import datetime
import tarfile
import os


def do_pack():
    pathdir = "versions/"
    namefile = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".tgz"
    if not os.path.exists(pathdir):
        os.mkdir(pathdir)
    with tarfile.open(pathdir + namefile, "w:gz") as tar:
        tar.add("web_static", arcname=os.path.basename("web_static"))
    if os.path.exists(pathdir + namefile):
        return pathdir + namefile
    else:
        return None
