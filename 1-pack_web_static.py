#!/usr/bin/python3
from datetime import datetime
from fabric.api import *


def do_pack():
    date_today = datetime.now().strftime('%Y%m%d%H%M%S')
    local("mkdir -p versions/")
    try:
        local("tar -cvzf versions/web_static_{}.tgz web_static"
              .format(date_today))
        return "versions/web_static_{}.tgz".format(date_today)
    except Exception:
        return None
