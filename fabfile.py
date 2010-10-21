from __future__ import with_statement

import os
from fabric.api import *

from fabric.contrib.project import rsync_project

def push():
    "Get new development code to device"

    rsync_project(remote_dir="/home/services/www/",
                  local_dir="equal",
                  delete=True,
                  exclude=[".git*",
                           "*.pyc",
                           "*.pyo"])
    run("chown :dev -R /home/services/www/equal")
    run("chmod g+rw -R /home/services/www/equal/data")


def requirements():
    "Install required packages for application"

    virtualenv = "source /home/services/python-virtualenvs/equal/bin/activate && "
    with cd('/home/services/www/equal/'):
        put("requirements.txt",
            "/home/services/www/equal")

        run(virtualenv+" pip install -r requirements.txt")


def restart():
    "Restart apache"

    sudo("/etc/init.d/apache2 restart")

def deploy():
    "Full deploy: push and start"

    push()
    requirements()
    restart()
