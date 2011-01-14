import os
import sys

# TODO: check apache server performance
virtualenv = os.path.join(os.path.dirname(__file__), ".virtualenv/bin/activate_this.py")
execfile(virtualenv, dict(__file__=virtualenv))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

os.environ["DJANGO_SETTINGS_MODULE"] = "qualitio.settings"
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
