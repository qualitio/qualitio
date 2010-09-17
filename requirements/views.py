from django.http import HttpResponse
from django.template import RequestContext
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.conf import settings

from tcstorm_requirements.requirements.models import Requirement
from tcstorm_requirements.requirements.forms import RequirementForm



def index(request):
    return render_to_response('requirements/base.html', 
                              context_instance=RequestContext(request))

def to_tree_element(object):
    return { 'data' : object.name,
             'attr' : {'id' : object.pk},
             'state' : 'closed', 
             'children' : [] }

def get_children(request):
    node_id = int(request.GET['id'])
    if not node_id:
        qs = Requirement.get_root_nodes()
    else:
        qs = Requirement.objects.get(pk=node_id).get_children()
    
    requirements_totreeel = map(lambda x: to_tree_element(x), qs)
    return HttpResponse(json.dumps(requirements_totreeel), mimetype="application/json")
            
def requirement(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    requirement_form = RequirementForm(instance=requirement)
    return render_to_response('requirements/_requirement_preview.html', 
                              {'requirement' : requirement,
                               'requirement_form' : requirement_form },
                              context_instance=RequestContext(request))
    


    
    

def requirement_children_table(request, requirement_id):
    # if not node_id:
    #     qs = Requirement.get_root_nodes()
    # else:
    #     qs = Requirement.objects.get(pk=requirement_id).get_children()
        
    return HttpResponse(json.dumps(requirements_totreeel), mimetype="application/json")
