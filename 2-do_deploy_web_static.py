#!/usr/bin/python3
from datetime import datetime
from fabric.api import *
from os import path

env.host = ["35.243.184.34", "107.21.164.251"]


def do_pack():
    date_today = datetime.now().strftime('%Y%m%d%H%M%S')
    local("mkdir -p versions/")
    try:
        local("tar -cvzf versions/web_static_{}.tgz web_static"
              .format(date_today))
        return "versions/web_static_{}.tgz".format(date_today)
    except Exception:
        return None


def do_deploy(archive_path):
    if (not path.exists(archive_path)):
        return False
    file_path = archive_path.split("/")[1]
    server_path = "/data/web_static/releases/" + file_path
    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p " + server_path)
        run("sudo tar -xzf /tmp/" + file_path + " -C " + server_path + "/")
        run("sudo rm /tmp/" + file_path)
        run("sudo mv " + server_path + "/web_static/* " + server_path)
        run("sudo rm -rf " + server_path + "/web_static")
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s " + server_path + " /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
