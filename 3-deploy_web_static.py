#!/usr/bin/python3
# Import Modules

from datetime import datetime
from fabric.api import *
from os import path


env.host = ["34.75.15.77", "35.185.77.201"]
env.user = "ubuntu"


def do_pack():
    """
        Pack in tgz Extension
    """
    date_today = datetime.now().strftime('%Y%m%d%H%M%S')
    local("mkdir -p versions/")
    try:
        local("tar -cvzf versions/web_static_{}.tgz web_static"
              .format(date_today))
        return "versions/web_static_{}.tgz".format(date_today)
    except Exception:
        return None


def do_deploy(archive_path):
    """
        Function Deploy
    """
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


def deploy():
    """
        Deploy New Files
    """
    new_file = do_pack()
    if (not new_file):
        return False
    return do_deploy(new_file)
