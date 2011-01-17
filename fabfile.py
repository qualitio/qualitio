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
        

def setup_production(path="/var/www/qualitio"):
    #TODO: switch to reall check. This normalization is pretty odd
    env.path = path.rstrip("/")

    sudo('apt-get install -y python-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('apt-get install -y apache2')
    sudo('apt-get install -y libapache2-mod-wsgi')
    
    sudo('mkdir -p %(path)s' % env)
    
    download_release()
    install_requirements()
    configure_webserver()
    synchronize_database()
    restart_webserver()
    load_dumpdata()
    print(green("\nDone.\n") + 
          "Check your site setup at http://%(host)s:8081" % env)
    
def download_release(release="development"):
    require("path")
    
    env.release = release
    env.release_download_tmp_file = "/tmp/%(release)s.tgz" % env
    
    sudo("wget http://github.com/qualitio/qualitio/tarball/%(release)s -O %(release_download_tmp_file)s --no-check-certificate" % env)
    sudo("tar xzvf %(release_download_tmp_file)s --strip-components=1 --directory=%(path)s" % env)
    sudo("rm -f %(release_download_tmp_file)s" % env)

def install_requirements():
    require("path")

    try:
        del(os.environ['PIP_VIRTUALENV_BASE'])
    except KeyError:
        pass
    sudo('pip -E %(path)s/.virtualenv install -r %(path)s/requirements.txt' % env)

def configure_webserver():
    env.esc_path = env.path.replace('/','\/')
    require("path", "esc_path")

    sudo("sed -i 's/${PATH}/%(esc_path)s/g' %(path)s/deploy/apache.virtualhost" % env)
    
    # TODO: put here diff check between config versions
    sudo("cp %(path)s/deploy/apache.virtualhost /etc/apache2/sites-available/qualitio" % env)

    sudo("a2ensite qualitio")

def synchronize_database():
    require("path")
    
    sudo("chown :www-data -R %(path)s/qualitio/data && chmod g+rw -R %(path)s/qualitio/data" % env)
    sudo("python %(path)s/qualitio/manage.py syncdb --noinput" % env, user="www-data")

def load_dumpdata():
    require("path")
    
    sudo("python %(path)s/qualitio/manage.py loaddata %(path)s/qualitio/initial_data.json" % env, user="www-data")
    
def restart_webserver():
    "Restart apache"

    sudo("/etc/init.d/apache2 restart")

