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

def menu(request, requirement_id):
    return render_to_response('requirements/menu.html',
                              { 'requirement' : Requirement.objects.get(pk=requirement_id) },
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

def valid_requirement_form(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    requirement_form = RequirementForm(request.POST, instance=requirement)

    if requirement_form.is_valid():
        requirement_form.save()
        return HttpResponse('OK')

    return HttpResponse(requirement_form.errors.as_ul())


def details(request, requirement_id):
    return render_to_response('requirements/details.html',
                              { 'requirement' : Requirement.objects.get(pk=requirement_id) },
                              context_instance=RequestContext(request))

def edit(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    return render_to_response('requirements/edit.html',
                              { 'requirement_form' : RequirementForm(instance=requirement) },
                              context_instance=RequestContext(request))


def test_cases(request, requirement_id):
    return render_to_response('requirements/test_cases.html',
                              { 'requirement' : Requirement.objects.get(pk=requirement_id) },
                              context_instance=RequestContext(request))


from django.views.generic.simple import direct_to_template
from tcstorm_requirements.requirements.tables import RequirementsFilterTable

def filter(request):
    requirements_table = RequirementsFilterTable(Requirement.objects.select_related(depth=1).all(),
                                                 order_by=request.GET.get('sort'))
    return direct_to_template(request, 'requirements/filter.html',
                              {'requirements_table' : requirements_table})
