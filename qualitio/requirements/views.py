from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import permission_required

from qualitio.core.utils import json_response, success, failed
from qualitio import store
from qualitio.requirements.models import Requirement
from qualitio.requirements.forms import RequirementForm

from qualitio import history

def index(request):
    return direct_to_template(request, 'requirements/base.html')


def details(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    testcases = requirement.testcase_set.all()
    return direct_to_template(request, 'requirements/details.html',
                              {'requirement': requirement ,
                               'testcases': testcases })

@permission_required('requirements.change_requirement', login_url='/permission_required/')
def edit(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    requirement_form = RequirementForm(instance=requirement)
    return direct_to_template(request, 'requirements/edit.html',
                              {'requirement_form': requirement_form})


@permission_required('requirements.add_requirement', login_url='/permission_required/')
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

        log = history.History(request.user, requirement)
        log.add_form(requirement_form)
        log.save()
        return success(message='Requirement saved',
                       data={"parent_id": getattr(requirement.parent,"id", 0),
                             "current_id": requirement.id })

    return failed(message="Validation errors %s" % requirement_form.error_message(),
                  data=requirement_form.errors_list())


@permission_required('perms.store.change_testcase', login_url='/permission_required/')
def testcases(request, requirement_id):
    requirement = Requirement.objects.get(pk=requirement_id)
    return direct_to_template(request, 'requirements/test_cases.html',
                              {'requirement': requirement,
                               'connected_testcases': requirement.testcase_set.all(),
                               'available_testcases': store.TestCase.objects.all()})


@json_response
def testcases_connect(request, requirement_id):
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
