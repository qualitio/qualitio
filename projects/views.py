from django.views.generic.simple import direct_to_template
from tcstorm_requirements.projects.models import *

def index(request):
    return direct_to_template(request, 'projects/base.html',
                              {})

def teams(request):
    return direct_to_template(request, 'projects/teams.html',
                              {'teams' : Team.objects.all()})

