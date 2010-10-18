from django.views.generic.simple import direct_to_template
from equal.projects.models import *

def index(request):
    return direct_to_template(request, 'projects/base.html',
                              {})

def teams(request):
    return direct_to_template(request, 'projects/teams.html',
                              {'teams' : Team.objects.all()})

def team_details(request,team_id):
    return direct_to_template(request, 'projects/team_details.html',
                              {'teams' : Team.objects.all(),
                               'team' : Team.objects.get(id=team_id)})

def team_edit(request,team_id):
    return direct_to_template(request, 'projects/team_edit.html',
                              {'teams' : Team.objects.all(),
                               'team' : Team.objects.get(id=team_id)})

