from django.http import HttpResponse
from django.template import RequestContext
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template

from equal.requirements.models import Requirement
from equal.requirements.forms import RequirementForm
from equal.requirements.tables import RequirementsFilterTable

def index(request):
    return direct_to_template(request, 'requirements/base.html')

def details(request, requirement_id):
    return direct_to_template(request, 'requirements/details.html',
                              {'requirement' : Requirement.objects.get(pk=requirement_id)})

def edit(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    requirement_form = RequirementForm(instance=requirement)
    return direct_to_template(request, 'requirements/edit.html',
                              {'requirement' : requirement,
                               'requirement_form' : requirement_form})

def json_response(x):
    return HttpResponse(json.dumps(x, sort_keys=True, indent=2),
                        content_type='application/json; charset=UTF-8')


def edit_valid(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    requirement_form = RequirementForm(request.POST, instance=requirement)

    if requirement_form.is_valid():
        requirement_form.save()
        return json_response({ 'success' : True,
                               'meesage' : ['Requirment saved'] })
    
    return json_response({ 'success' : False,
                           'message' : [(k, v[0]) for k, v in requirement_form.errors.items()] })

def test_cases(request, requirement_id):
    return render_to_response('requirements/test_cases.html',
                              { 'requirement' : Requirement.objects.get(pk=requirement_id) },
                              context_instance=RequestContext(request))


def filter(request):
    requirements_table = RequirementsFilterTable(Requirement.objects.select_related(),
                                                 order_by=request.GET.get('sort'))
    return direct_to_template(request, 'requirements/filter.html',
                              {'requirements_table' : requirements_table})



## move to core app, as soon as possible
def to_tree_element(object):
    return { 'data' : object.name,
             'attr' : {'id' : object.pk},
             'state' : 'closed',
             'children' : [] }

def get_children(request):
    node_id = int(request.GET['id'])
    if not node_id:
        qs = Requirement.tree.root_nodes()
    else:
        qs = Requirement.objects.get(pk=node_id).get_children()

    requirements_totreeel = map(lambda x: to_tree_element(x), qs)
    return HttpResponse(json.dumps(requirements_totreeel), mimetype="application/json")
