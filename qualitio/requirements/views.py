from django.http import HttpResponse
from django.template import RequestContext, loader
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.db.models import Q
from qualitio.core.utils import json_response, success, failed

from qualitio.store.models import TestCase

from qualitio.requirements.models import Requirement
from qualitio.requirements.forms import RequirementForm, SearchTestcasesForm
from qualitio.requirements.tables import RequirementsFilterTable

def index(request):
    return direct_to_template(request, 'requirements/base.html')


def details(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    testcases = requirement.testcase_set.all()
    return direct_to_template(request, 'requirements/details.html',
                              {'requirement' : requirement ,
                               'testcases' : testcases })


def edit(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    requirement_form = RequirementForm(instance=requirement)
    return direct_to_template(request, 'requirements/edit.html',
                              {'requirement_form': requirement_form})


def new(request, requirement_id):
    requirement = Requirement.objects.get(id=requirement_id)
    requirement_form = RequirementForm(initial={'parent': requirement})
    return direct_to_template(request, 'requirements/edit.html',
                              {'requirement_form': requirement_form})

@json_response
def valid(request, requirement_id=0):
    if requirement_id:
        requirement = Requirement.objects.get(pk=requirement_id)
        requirement_form = RequirementForm(request.POST, instance=requirement)
    else:
        requirement_form = RequirementForm(request.POST)

    if requirement_form.is_valid():
        requirement = requirement_form.save()
        return success(message='Requirement saved',
                       data={ "parent_id" : getattr(requirement.parent,"id", 0),
                              "current_id" : requirement.id })

    # TODO: move this functionality to helpers
    return failed(message="Validation errors %s" % " ".join([e for e in requirement_form.non_field_errors()]),
                  data=[(k, v[0]) for k, v in requirement_form.errors.items()])


def test_cases(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    connected_testcases = requirement.testcase_set.all()
    available_testcases = TestCase.objects.all()
    return render_to_response('requirements/test_cases.html',
                              {'requirement' : Requirement.objects.get(pk=requirement_id),
                               'connected_testcases' : connected_testcases,
                               'available_testcases' : available_testcases,
                               'search_testcases_form' : SearchTestcasesForm()},
                              context_instance=RequestContext(request))

@json_response
def available_testcases(request, requirement_id):
    search_testcases_form = SearchTestcasesForm(request.POST)
    if search_testcases_form.is_valid():
        search = request.POST["search"]
        testcases =  TestCase.objects.filter(Q(name__contains=search) | Q(path__contains=search))
        if testcases:
            return success(message="%s testcases found" % testcases.count(),
                           data=loader.render_to_string("requirements/_available_testcases.html",
                                                        { "testcases" : testcases }))
        return success(message="no testcases found")

    return failed(message="validation errors",
                  data=[(k, v[0]) for k, v in search_testcases_form.errors.items()])

@json_response
def connect_testcases(request, requirement_id):
    requirement = Requirement.objects.get(id=requirement_id)
    for testcase in TestCase.objects.filter(id__in=request.POST.getlist("connect")):
        testcase.requirement = requirement
        testcase.save()
    for testcase in TestCase.objects.filter(id__in=request.POST.getlist("disconnect")):
        testcase.requirement = None
        testcase.save()
    return success();


def filter(request):
    requirements_table = RequirementsFilterTable(Requirement.objects.select_related(),
                                                 order_by=request.GET.get('sort'))
    return direct_to_template(request, 'requirements/filter.html',
                              {'requirements_table' : requirements_table})

