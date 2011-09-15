from django.views.generic.simple import direct_to_template

from qualitio.core.utils import json_response, success, failed
from qualitio.organizations import permission_required
from qualitio import core
from qualitio import store
from qualitio.require.models import Requirement
from qualitio.require.forms import RequirementForm

from qualitio import history


def index(request, **kwargs):
    return direct_to_template(request, 'require/base.html')


@permission_required('USER_READONLY')
@core.menu_view(Requirement, "details")
def details(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)
    testcases = requirement.testcase_set.all()
    return direct_to_template(request, 'require/details.html',
                              {'requirement': requirement ,
                               'testcases': testcases })

@permission_required('USER')
@core.menu_view(Requirement, "edit", perm='require.change_requirement')
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
@core.menu_view(Requirement, "testcases", perm='store.change_testcase')
def testcases(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)
    url = '/project/%(slug)s/require/ajax/requirement/%(id)s/' % {
        'slug': request.project.slug,
        'id': requirement_id,
        }
    return direct_to_template(request, 'require/test_cases.html',
                              {'requirement': requirement,
                               'connected_testcases_url': url + 'connected_testcases/',
                               'available_testcases_url': url + 'available_testcases/',
                               'connect_testcases_url': url + 'testcases/connect/',
                               'disconnect_testcases_url': url + 'testcases/disconnect/',
                               })


@permission_required('USER')
@json_response
def connected_testcases(request, requirement_id, **kwargs):
    datatable = core.DataTable(
        columns=["checkbox", "id", "path", "name", "modified_time", "created_time"],
        params=request.GET,
        queryset=store.TestCase.objects.filter(requirement__id=requirement_id))
    return datatable.response_dict(mapitem=lambda item: [
            '<input type="checkbox" id="testcase-%s" name="connected_testcase" />' % item.id,
            item.id,
            item.path,
            item.name,
            item.modified_time.strftime("%d-%m-%Y"),
            item.created_time.strftime("%d-%m-%Y"),
            ])


@json_response
def available_testcases(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)
    datatable = core.DataTable(
        columns=["checkbox", "id", "path", "name", "modified_time", "created_time"],
        params=request.GET,
        queryset=store.TestCase.objects.get_query_set(select_related_fields=[]).exclude(
            id__in=requirement.testcase_set.values_list('id', flat=True)))
    return datatable.response_dict(mapitem=lambda item: [
            '<input type="checkbox" id="testcase-%s" name="available_testcase" />' % item.id,
            item.id,
            item.path,
            item.name,
            item.modified_time.strftime("%d-%m-%Y"),
            item.created_time.strftime("%d-%m-%Y"),
            ])


@json_response
def testcases_connect(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)
    testcases = store.TestCase.objects.filter(pk__in=request.POST.getlist("testcases[]"))
    testcases.update(requirement=requirement)

    log = history.History(request.user, requirement)
    log.add_objects(created=testcases)
    message = log.save()

    return success(message=message)


@json_response
def testcases_disconnect(request, requirement_id, **kwargs):
    requirement = Requirement.objects.get(pk=requirement_id)
    testcases = store.TestCase.objects.filter(pk__in=request.POST.getlist("testcases[]"))
    testcases.update(requirement=None)

    log = history.History(request.user, requirement)
    log.add_objects(deleted=testcases)
    message = log.save()

    return success(message=message)
