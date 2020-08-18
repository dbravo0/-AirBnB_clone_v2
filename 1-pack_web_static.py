#!/usr/bin/python3
# Generates a .tgz archive

from datetime import datetime
import tarfile
import os


def do_pack():
    filename = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".tgz"

    if not os.path.exists("versions/"):
        os.mkdir("versions/")

    with tarfile.open("versions/" + filename, "w:gz") as tar:
        tar.add("web_static", arcname=os.path.basename("web_static"))

    if os.path.exists("versions/" + filename):
        return "versions/" + filename

    return None
