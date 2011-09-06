from django.views.generic.simple import direct_to_template
# from django.contrib.auth.decorators import permission_required

from qualitio.core.utils import json_response, success, failed
from qualitio.projects.auth.decorators import permission_required
from qualitio import core
from qualitio import store
from qualitio.require.models import Requirement
from qualitio.require.forms import RequirementForm

from qualitio import history


def index(request, **kwargs):
    return direct_to_template(request, 'require/base.html')


@permission_required('USER_READONLY')
@core.menu_view(Requirement, "details", role='USER_READONLY')
def details(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)
    testcases = requirement.testcase_set.all()
    return direct_to_template(request, 'require/details.html',
                              {'requirement': requirement ,
                               'testcases': testcases })

@permission_required('USER')
@core.menu_view(Requirement, "edit", role='USER')
def edit(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)
    requirement_form = RequirementForm(instance=requirement)
    return direct_to_template(request, 'require/edit.html',
                              {'requirement_form': requirement_form})


@permission_required('USER')
def new(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(id=requirement_id)
    requirement_form = RequirementForm(initial={'parent': requirement})
    return direct_to_template(request, 'require/edit.html',
                              {'requirement_form': requirement_form})


@permission_required('USER')
@json_response
def valid(request, requirement_id=0, **kwargs):
    if requirement_id:
        requirement = Requirement.objects.get(pk=requirement_id)
        requirement_form = RequirementForm(request.POST, instance=requirement)
    else:
        requirement_form = RequirementForm(request.POST)

    if requirement_form.is_valid():
        requirement = requirement_form.save()

        log = history.History(request.user, requirement)
        log.add_form(requirement_form, is_new=(requirement_id == 0))
        log.save()
        return success(message='Requirement saved',
                       data={"parent_id": getattr(requirement.parent,"id", 0),
                             "current_id": requirement.id })

    return failed(message="Validation errors %s" % requirement_form.error_message(),
                  data=requirement_form.errors_list())


@permission_required('USER')
@core.menu_view(Requirement, "testcases", role='USER')
def testcases(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)
    return direct_to_template(request, 'require/test_cases.html',
                              {'requirement': requirement,
                               'connected_testcases': requirement.testcase_set.all(),
                               'available_testcases': store.TestCase.objects.all()})


@permission_required('USER')
@json_response
def testcases_connect(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)

    previously_connected = set(requirement.testcase_set.all()) # freeze

    requirement.testcase_set.clear()

    testcases =\
        store.TestCase.objects.filter(pk__in=request.POST.getlist("connected_test_case"))

    for testcase in testcases:
        requirement.testcase_set.add(testcase)

    currently_connected = set(requirement.testcase_set.all()) # freeze

    created = list(currently_connected - previously_connected)
    deleted = list(previously_connected - currently_connected)

    log = history.History(request.user, requirement)
    log.add_objects(created=created, deleted=deleted)
    message = log.save()
    return success(message=message)
