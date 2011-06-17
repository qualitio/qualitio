#!/usr/bin/env python
import os
import sys


import_error_message = """
Error: Can't find the file 'settings.py' in the directory containing %r.
It appears you've customized things.\n
You'll have to run django-admin.py, passing it your settings module.\n
(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__
"""


def manage_local():

    try:
        os.environ["VIRTUAL_ENV"]
    except KeyError:
        developemnt_virtualenv = os.path.join(os.path.dirname(__file__),
                                              "../.virtualenv/bin/activate_this.py")
        execfile(developemnt_virtualenv, dict(__file__=developemnt_virtualenv))

    tests_path = os.path.join(os.path.dirname(__file__), "../tests")
    sys.path.append(tests_path)

    try:
        import settings
    except ImportError:
        sys.stderr.write(import_error_message)

    from django.core.management import execute_manager
    execute_manager(settings)


def manage_global():
    try:
        from qualitio import settings
    except:
        sys.stderr.write(import_error_message)

    from django.core.management import execute_manager
    execute_manager(settings)


if __name__ == "__main__":
    manage_local()
