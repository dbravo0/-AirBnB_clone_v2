#!/usr/bin/python3
# Distributes an archive to web servers

from fabric.api import env
from fabric.api import put
from fabric.api import run
import os
import ntpath


env.hosts = ["34.75.15.77", "35.185.77.201"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """ Funtion do_deploy """
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")

        file = ntpath.basename(archive_path)
        folder = file[:-4]
        run("mkdir -p /data/web_static/releases/" + folder)
        run("tar -xzf /tmp/" + file + " -C /data/web_static/releases/" +
            folder)
        run("rm /tmp/" + file)
        run("rm /data/web_static/current")
        run("ln -sf /data/web_static/releases/" + folder +
            "/web_static/ /data/web_static/current")
        return True
    except Exception:
        return False
