from __future__ import with_statement

import os
from fabric.api import *

from fabric.contrib.project import rsync_project
from fabric.colors import green


def setup_development():
    "Create development envirotment"
    
    with hide('running', 'stdout'):
        print("Creating development evnirotment: ... ")
        print("  1. Installing python libraries: python-setuptools, python-dev")
        local('sudo apt-get install -y python-setuptools python-dev', capture=False)
        print("  2. Installing pip")
        local('sudo easy_install pip', capture=False)
        print("  3. Installing virtualenv")
        local('sudo pip install virtualenv', capture=False)
    
        try:
            workon = os.environ["WORKON_HOME"]
            print("  4. Creating virtualenv environment")
            local('virtualenv %s/qualitio-dev' % workon)
            print("  5. Downloading required development packages")
            local('pip -E %s/qualitio-dev install -r requirements.txt' % workon)
            print("\nDevelopment evnirotment for qualitio project created!" + 
                  "\nType " + green("workon qualitio-dev") + " to start workoing!")

        except KeyError:
            print("  4. Creating virtualenv environment")
            local('virtualenv .virtualenv')
            print("  5. Downloading required development packages")
            local('pip -E .virtualenv install -r requirements.txt')
            
            print("\nDevelopment evnirotment for qualitio project created in " + 
                  green("%s/.virtualenv" % os.getcwd()) + " directory")
        

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
