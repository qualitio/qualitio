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
            del(os.environ['VIRTUAL_ENV'])
            print("  4. Creating virtualenv environment")
            local('virtualenv %s/qualitio-dev' % workon)
            print("  5. Downloading required development packages, this may take a while")
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
        

def setup_production():
    sudo('apt-get install -y python-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('apt-get install -y apache2')
    sudo('apt-get install -y libapache2-mod-wsgi')
    
    env.path = "/var/www/qualtio"
    sudo('mkdir -p %(path)s' % env)

def download_release():
    env.release = "development"
    env.release_download_tmp_file = "/tmp/%(release)s.tgz" % env
    env.path = "/var/www/qualtio"
    
    sudo("wget http://github.com/qualitio/qualitio/tarball/%(release)s -O %(release_download_tmp_file)s --no-check-certificate" % env)
    sudo("tar xzvf %(release_download_tmp_file)s --strip-components=1 --directory=%(path)s" % env)
    sudo("rm -f %(release_download_tmp_file)s" % env)

def configure_webserver():
    env.path = "/var/www/qualtio" 
    
    sudo("mv %(path)s/deploy/apache.virtualhost /etc/apache2/sites-available/qualitio" % env)
    sudo("a2ensite qualitio")
    
def install_requirements():
    env.path = "/var/www/qualtio"

    try:
        del(os.environ['PIP_VIRTUALENV_BASE'])
    except KeyError:
        pass
    sudo('pip -E %(path)s/deploy/.virtualenv install -r %(path)s/requirements.txt' % env)

def restart_webserver():
    "Restart apache"

    sudo("/etc/init.d/apache2 restart")

