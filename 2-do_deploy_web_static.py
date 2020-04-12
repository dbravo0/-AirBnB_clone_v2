#!/usr/bin/python3
from datetime import datetime
from fabric.api import *
from os import path

env.host = ['35.227.85.236', '3.80.76.254']


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
    """ Distributes an archive to the web servers """
    if not path.exists(archive_path):
        return False
    # split the path and get the second element in the list
    file_path = archive_path.split("/")[1]
    serv_folder = "/data/web_static/releases/" + file_path

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p " + serv_folder)
        run("sudo tar -xzf /tmp/" + file_path + " -C " + serv_folder + "/")
        run("sudo rm /tmp/" + file_path)
        run("sudo mv " + serv_folder + "/web_static/* " + serv_folder)
        run("sudo rm -rf " + serv_folder + "/web_static")
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s " + serv_folder + " /data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
