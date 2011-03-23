from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.db.models import Q

from reversion import revision

from qualitio.core.utils import json_response, success, failed
from qualitio import store
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

@revision.create_on_success
@json_response
def valid(request, requirement_id=0):
    if requirement_id:
        requirement = Requirement.objects.get(pk=requirement_id)
        requirement_form = RequirementForm(request.POST, instance=requirement)
    else:
        requirement_form = RequirementForm(request.POST)

    if requirement_form.is_valid():
        revision.comment = requirement_form.changelog()
        revision.user = request.user
        if not revision.comment:
            revision.invalidate()

        requirement = requirement_form.save()
        return success(message='Requirement saved: %s' % revision.comment,
                       data={"parent_id" : getattr(requirement.parent,"id", 0),
                             "current_id" : requirement.id })

    return failed(message="Validation errors %s" % requirement_form.error_message(),
                  data=requirement_form.errors_list())


def testcases(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    return render_to_response('requirements/test_cases.html',
                              {'requirement' : requirement,
                               'connected_testcases' : requirement.testcase_set.all(),
                               'available_testcases' : store.TestCase.objects.all(),
                               'search_testcases_form' : SearchTestcasesForm()},
                              context_instance=RequestContext(request))


@json_response
def testcases_connect(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)

    requirement.testcase_set.clear()

    testcases =\
        store.TestCase.objects.filter(pk__in=request.POST.getlist("connected_test_case"))

    for testcase in testcases:
        requirement.testcase_set.add(testcase)

    return success(message="Test cases connected")


def history(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)

    from reversion.models import Version
    versions = Version.objects.get_for_object(requirement)
    return direct_to_template(request, 'requirements/history.html',
                          {'requirement': requirement,
                           'versions' : versions})


def filter(request):
    requirements_table = RequirementsFilterTable(Requirement.objects.select_related(),
                                                 order_by=request.GET.get('sort'))
    return direct_to_template(request, 'requirements/filter.html',
                              {'requirements_table' : requirements_table})
