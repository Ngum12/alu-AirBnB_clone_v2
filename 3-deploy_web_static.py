#!/usr/bin/python3
"""
Write a Fabric script that creates and
distributes an archive to my web servers
"""

from fabric.api import env
from os.path import exists
from fabric.api import local, put, run
from datetime import datetime

env.hosts = ["3.85.84.57", "54.196.167.246"]
env.user = "ubuntu"


def do_pack():
    """Creates a .tgz archive of the web_static directory"""
    try:
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None


def do_deploy(archive_path):
    """do_deploy fxn"""
    if not exists(archive_path):
        return False
    try:
        archive_name = archive_path.split("/")[-1]
        folder_name = "/data/web_static/releases/{}".format(
            archive_name.replace(".tgz", "")
        )
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(archive_name, folder_name))
        run("rm /tmp/{}".format(archive_name))
        run("mv {}/web_static/* {}".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_name))
        return True
    except:
        return False


def deploy():
    """deploy fxn"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
