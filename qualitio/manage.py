#!/usr/bin/env python
import os, sys

try: 
    os.environ["VIRTUAL_ENV"]
except KeyError:
    developemnt_virtualenv = os.path.join(os.path.dirname(__file__), "../.virtualenv/bin/activate_this.py")
    execfile(developemnt_virtualenv, dict(__file__=developemnt_virtualenv))

from django.core.management import execute_manager
try:
    import settings # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)

