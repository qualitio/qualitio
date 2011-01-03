from __future__ import with_statement

import os
from fabric.api import *

from fabric.contrib.project import rsync_project

def push():
    "Get new development code to device"

    rsync_project(remote_dir="/home/services/www/",
                  local_dir="qualitio",
                  delete=True,
                  exclude=[".git*",
                           "*.pyc",
                           "*.pyo"])
    run("chown :dev -R /home/services/www/qualitio")
    run("chmod g+rw -R /home/services/www/qualitio/data")


def requirements():
    "Install required packages for application"

    virtualenv = "source /home/services/python-virtualenvs/qualitio/bin/activate && "
    with cd('/home/services/www/qualitio/'):
        put("requirements.txt",
            "/home/services/www/qualitio")

        run(virtualenv+" pip install -r requirements.txt")


def restart():
    "Restart apache"

    sudo("/etc/init.d/apache2 restart")

def deploy():
    "Full deploy: push and start"

    push()
    requirements()
    restart()
