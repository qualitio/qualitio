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


class count(object):
    _counter = 0
    @classmethod
    def inc(cls):
        cls._counter += 1
        return cls._counter

run_it = None
sudo_it = None


def _install_python():
    print("%s. Installing python essentials" % count.inc())

    sudo_it('apt-get install -y python-setuptools python-dev')
    sudo_it('easy_install pip')
    sudo_it('pip install -U setuptools')
    sudo_it('pip install virtualenv')


def _create_virtualenv():
    print("%s. Creating virtualenv environment" % count.inc())
    require("virtualenv_path")

    run_it("virtualenv %s" % env.virtualenv_path)

def _synchronize_database():
    print("%s. Synchronizing database" % count.inc())
    require("virtualenv_path","path")

    run_it("%(virtualenv_path)s/bin/python %(path)s/qualitio/manage.py syncdb --noinput"  % env)

def _migrate_database():
    print("%s. Migrating database" % count.inc())
    require("virtualenv_path","path")

    run_it("%(virtualenv_path)s/bin/python %(path)s/qualitio/manage.py migrate"  % env)

def _load_startdata():
    print("%s. Create essential objects" % count.inc())
    require("virtualenv_path","path")

    for fixture in ["auth.json", "exeute.json", "report.json", "require.json", "store.json"]:
        fixture_load = "%(virtualenv_path)s/bin/python %(path)s/qualitio/manage.py loaddata " % env
        fixture_load+= "%s/qualitio/fixtures/%s"  % (env.path, fixture)
        run_it(fixture_load)

def _install_apache():
    print("%s. Install Apache" % count.inc())

    sudo_it('apt-get install -y apache2')
    sudo_it('apt-get install -y libapache2-mod-wsgi')

def _download_release(release="development"):
    print("%s. Download release %s" % (count.inc(), release))
    require("path")

    release_download = "/tmp/%s.tgz" % release

    run_it("wget http://github.com/qualitio/qualitio/tarball/%s -O %s --no-check-certificate"
         % (release, release_download))

    sudo_it("mkdir %(path)s -p" % env)
    sudo_it("chown www-data:www-data -R %(path)s" % env)

    run_it("tar xzvf %s --strip-components=1 --directory=%s"
            % (release_download, env.path))

    run_it("rm -f %s" % release_download)

def _install_requirements():
    print("%s. Install requirements" % count.inc())
    require("path", "virtualenv_path")

    sudo_it("apt-get install git-core mercurial")

    try:
        del(os.environ['PIP_VIRTUALENV_BASE'])
    except KeyError:
        pass

    run_it('pip -E %(virtualenv_path)s install -r %(path)s/requirements.txt' % env)


def _configure_apache():
    print("%s. Setup apache server" % count.inc())
    require("path", "instance_name")

    run_it('sed -i "s/_PATH/%s/g" %s/deploy/apache.virtualhost'
           % (env.path.replace('/','\/'), env.path))

    # TODO: put here diff check between config versions
    sudo_it("cp %s/deploy/apache.virtualhost /etc/apache2/sites-available/%s"
            % (env.path, env.instance_name))

def _setup_local_settings(local_settings):
    print("%s. Setup local settings" % count.inc())
    require("path")

    if local_settings:
        try:
            put(local_settings, "%(path)s/qualitio/local_settings.py" % env, use_sudo=True)
        except ValueError:
            print(colors.yellow("Local settings file doesn't exists, using defaults."))

def _restart_webserver():
    print("%s. Restart apache" % count.inc())

    sudo_it("/etc/init.d/apache2 restart")

def setup_development(virtualenv_name="qualitio-dev"):
    "Creates local development envirotment"

    global run_it
    global sudo_it

    # TODO: there are aguments ("spaces inside") where split is not so good idea
    # but in most cases in our calls will be good.
    run_it = lambda command : subprocess.call(command.split(" "))
    sudo_it = lambda command : subprocess.call(["sudo"] + command.split(" "))

    env.path = os.path.dirname(__file__)

    try:
        workon = os.environ["WORKON_HOME"]
        if os.environ.has_key('VIRTUAL_ENV'):
            del(os.environ['VIRTUAL_ENV'])

        env.virtualenv_path = "%s/%s" % (workon, virtualenv_name)
    except KeyError:
        env.virtualenv_path = "%s/.virtualenv" % env.path

    if os.path.exists(env.virtualenv_path):
        print("Environment already exists in %s. Stoping configuration."
              % colors.red(env.virtualenv_path))
        print("To create new developemnt environment remove one previously created.")
        sys.exit()

    _install_python()
    _create_virtualenv()
    _synchronize_database()
    _migrate_database()
    _load_startdata()


def setup_production(path="/var/www/qualitio", instance_name=None, local_settings=""):
    "Creates remote production envirotment"

    global run_it
    global sudo_it

    run_it = lambda command: sudo(command, user="www-data")
    sudo_it = sudo

    #TODO: switch to reall check. This normalization is pretty odd
    env.path = path.rstrip("/")

    if files.exists(env.path):
        print("Environment %s already exists. Stoping configuration." % colors.red(env.path))
        print("To create new developemnt environment remove one previously created.")
        sys.exit()

    if not instance_name:
        env.instance_name = env.path.split("/")[-1]
    else:
        env.instance_name = instance_name

    env.virtualenv_path = "%s/.virtualenv" % env.path

    _install_python()

    _download_release()
    _create_virtualenv()
    _install_requirements()
    _setup_local_settings(local_settings)

    _install_apache()
    _configure_apache()

    _synchronize_database()
    _migrate_database()
    _load_startdata()

    print("Instance was successfully deployed in %s"
          % colors.green(env.path))
    print("Adapt your settings for instance in /etc/apache2/sites-available/%s and "
          % (colors.green(env.instance_name)))
    print("start instance using a2ensite %s" % colors.green(("a2ensite %s" % env.instance_name)))


def update_production(path="/var/www/qualitio", local_settings=""):
    """Updates remote production envirotment"""

    global run_it
    global sudo_it

    run_it = lambda command: sudo(command, user="www-data")
    sudo_it = sudo

    env.path = path.rstrip("/")
    env.virtualenv_path = "%s/.virtualenv" % env.path

    if not files.exists(env.path):
        print colors.red("No instance found on path=%s. Breaking update." % env.path)
    else:
        _download_release()
        _install_requirements()
        _synchronize_database()
        _migrate_database()
        _restart_webserver()

        print("Instsance at %s:%s, updated." % (colors.green(env.host),
                                                colors.green(env.path)))

def setup_documetation(path="/var/www/qualitiodocs"):

    global run_it
    global sudo_it

    run_it = lambda command: sudo(command, user="www-data")
    sudo_it = sudo

    env.path = os.path.dirname(__file__)
    print "%s/docs" % env.path

    with lcd("%s/docs" % env.path):
        local("make html")
        put("build/html/*", path, use_sudo=True)


if __name__ == '__main__':
    subprocess.call(['fab', '-f', __file__] + sys.argv[1:])
