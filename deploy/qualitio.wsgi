import os
import sys

# TODO: check apache server performance
virtualenv = os.path.join(os.path.dirname(__file__), ".virtualenv/bin/activate_this.py")
execfile(virtualenv, dict(__file__=virtualenv))

os.environ["DJANGO_SETTINGS_MODULE"] = "qualitio.settings"
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
