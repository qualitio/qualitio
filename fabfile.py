#!/usr/bin/env python
from __future__ import with_statement

import os
import sys
import subprocess

try:
    from fabric.api import *
    from fabric.contrib.project import rsync_project
    from fabric.contrib import files
    from fabric import colors
except ImportError:
    print ("""The 'fabric' package is currently not installed.  You can install it by typing:\n
  - sudo apt-get install fabric or,
  - sudo easy-install fabric or,
  - sudo pip install fabric.
""")
    sys.exit()


def setup_development(virtualenv_name="qualitio"):
    "Creates local development envirotment"

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
            local('virtualenv %s/%s' % (workon, virtualenv_name))
            print("  5. Downloading required development packages, this may take a while")
            local('pip -E %s/%s install -r requirements.txt' % (workon, virtualenv_name))
            print("\nDevelopment evnirotment for qualitio project created!" +
                  "\nType " + green("workon %s" % virtualenv_name) + " to start workoing!")

        except KeyError:
            print("  4. Creating virtualenv environment")
            local('virtualenv .virtualenv')
            print("  5. Downloading required development packages")
            local('pip -E .virtualenv install -r requirements.txt')

            print("\nDevelopment evnirotment for qualitio project created in " +
                  colors.green("%s/.virtualenv" % os.getcwd()) + " directory")



def setup_production(path="/var/www/qualitio", local_settings="", fixtures=False):
    "Creates remote production envirotment"

    #TODO: switch to reall check. This normalization is pretty odd
    env.path = path.rstrip("/")
    env.apache_config = env.path.split("/")[-1]

    sudo('apt-get install -y python-setuptools')
    sudo('easy_install pip')
    sudo('pip install virtualenv')
    sudo('apt-get install -y apache2')
    sudo('apt-get install -y libapache2-mod-wsgi')

    sudo('mkdir -p %(path)s' % env)

    _download_release()
    _install_requirements()
    _configure_webserver()
    _local_settings(local_settings)
    _synchronize_database()
    _migrate_database()
    _restart_webserver()
    if fixtures:
        _load_dumpdata()

    print("Check your site setup at http://%s.%s:8081" % (colors.green(env.apache_config), colors.green(env.host)))


def update_production(path="/var/www/qualitio", local_settings=""):
    """Updates remote production envirotment"""
    env.path = path.rstrip("/")

    if not files.exists(env.path):
        print colors.red("No instance found on path=%s. Breaking update." % env.path)
    else:
        _download_release()
        _install_requirements()
        _local_settings(local_settings)
        _synchronize_database()
        _migrate_database()
        _restart_webserver()

        print("Instsance at %s:%s, updated." % (colors.green(env.host),
                                                colors.green(env.path)))


def _download_release(release="development"):
    require("path")

    env.release = release
    env.release_download_tmp_file = "~/%(release)s.tgz" % env

    sudo("wget http://github.com/qualitio/qualitio/tarball/%(release)s -O %(release_download_tmp_file)s --no-check-certificate" % env)
    sudo("tar xzvf %(release_download_tmp_file)s --strip-components=1 --directory=%(path)s" % env)
    sudo("rm -f %(release_download_tmp_file)s" % env)


def _install_requirements():
    require("path")

    try:
        del(os.environ['PIP_VIRTUALENV_BASE'])
    except KeyError:
        pass
    sudo('pip -E %(path)s/.virtualenv install -r %(path)s/requirements.txt' % env)


def _configure_webserver():
    env.esc_path = env.path.replace('/','\/')
    require("path", "esc_path")

    sudo("sed -i 's/${PATH}/%(esc_path)s/g' %(path)s/deploy/apache.virtualhost" % env)

    # TODO: put here diff check between config versions

    sudo("cp %(path)s/deploy/apache.virtualhost /etc/apache2/sites-available/%(apache_config)s" % env)

    sudo("a2ensite %(apache_config)s" % env)


def _local_settings(local_settings):
    require("path")

    if not local_settings:
        print(colors.yellow("No local settins files provied, using defaults."))
    else:
        try:
            put(local_settings, "%(path)s/qualitio/local_settings.py" % env, use_sudo=True)
        except ValueError:
            print(colors.yellow("Local settings file doesn't exists, using defaults."))


def _synchronize_database():
    require("path")

    sudo("chown :www-data -R %(path)s/qualitio/data && chmod g+rw -R %(path)s/qualitio/data" % env)
    sudo("python %(path)s/qualitio/manage.py syncdb --noinput" % env)


def _migrate_database():
    require("path")
    sudo("python %(path)s/qualitio/manage.py migrate --noinput" % env)


def _load_dumpdata():
    require("path")

    sudo("python %(path)s/qualitio/manage.py loaddata %(path)s/qualitio/example_data.json" % env)


def _restart_webserver():
    "Restart apache"

    sudo("/etc/init.d/apache2 restart")


if __name__ == '__main__':
    subprocess.call(['fab', '-f', __file__] + sys.argv[1:])
