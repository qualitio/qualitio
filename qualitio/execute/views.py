from django.views.generic.simple import direct_to_template

from qualitio.core.utils import json_response, success, failed
from qualitio import store
from qualitio.execute.models import TestRunDirectory, TestRun, TestCaseRun, Bug
from qualitio.execute import forms


def index(request):
    return direct_to_template(request, 'execute/base.html', {})


def directory_details(request, directory_id):
    return direct_to_template(request, 'execute/testrundirectory_details.html',
                              {'directory': TestRunDirectory.objects.get(pk=directory_id)})


def directory_new(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrundirectory_form = forms.TestRunDirectoryForm(initial={'parent': directory})
    return direct_to_template(request, 'execute/testrundirectory_edit.html',
                              {'testrundirectory_form': testrundirectory_form})


def directory_edit(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrundirectory_form = forms.TestRunDirectoryForm(instance=directory)
    return direct_to_template(request, 'execute/testrundirectory_edit.html',
                              {'testrundirectory_form': testrundirectory_form})


@json_response
def directory_valid(request, directory_id=0):
    if directory_id:
        testrun_directory = TestRunDirectory.objects.get(pk=str(directory_id))
        testrun_directory_form = forms.TestRunDirectoryForm(request.POST,
                                                            instance=testrun_directory)
    else:
        testrun_directory_form = forms.TestRunDirectoryForm(request.POST)

    if testrun_directory_form.is_valid():
        testrun_directory = testrun_directory_form.save()
        return success(message='testrun directory saved',
                       data={"parent_id": getattr(testrun_directory.parent, "id", 0),
                             "current_id": testrun_directory.id})
    else:
        return failed(message="Validation errors: %s" % testrun_directory_form.error_message(),
                      data=testrun_directory_form.errors_list())


def testrun_details(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_details.html',
                              {'testrun': TestRun.objects.get(pk=testrun_id)})


def testrun_execute(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_execute.html',
                              {'testrun': TestRun.objects.get(pk=testrun_id)})


def testrun_notes(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_notes.html',
                              {'testrun': TestRun.objects.get(pk=testrun_id)})


def testrun_new(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrun_form = forms.TestRunForm(initial={'parent': directory})
    return direct_to_template(request, 'execute/testrun_edit.html',
                              {"testrun_form": testrun_form})


def testrun_edit(request, testrun_id):
    testrun = TestRun.objects.get(pk=testrun_id)
    testrun_form = forms.TestRunForm(instance=testrun, prefix="testrun")
    connected_test_cases_form = forms.ConnectedTestCases(instance=testrun,
                                                         prefix="connected_test_cases")
    available_test_cases_form = forms.AvailableTestCases(
        prefix="available_test_cases",
        queryset=store.TestCase.objects.exclude(testcaserun__parent=testrun))

    return direct_to_template(request, 'execute/testrun_edit.html',
                              {'testrun': testrun,
                               'testrun_form': testrun_form,
                               'available_test_cases_form': available_test_cases_form,
                               'connected_test_cases_form' : connected_test_cases_form})


@json_response
def testrun_valid(request, testrun_id=0):
    if testrun_id:
        testrun = TestRun.objects.get(pk=str(testrun_id))
        testrun_form = forms.TestRunForm(request.POST, instance=testrun, prefix="testrun")

        connected_test_cases_form = forms.ConnectedTestCases(request.POST, instance=testrun,
                                                             prefix="connected_test_cases")
    else:
        testrun_form = forms.TestRunForm(request.POST)
        connected_test_cases_form = forms.ConnectedTestCases(request.POST,
                                                             prefix="connected_test_cases")

    available_test_cases_form = forms.AvailableTestCases(request.POST,
                                                         prefix="available_test_cases")

    if testrun_form.is_valid() and\
            connected_test_cases_form.is_valid() and\
            available_test_cases_form.is_valid():

        testrun = testrun_form.save()
        connected_test_cases_form.save()

        to_run = filter(lambda x: x['action'], available_test_cases_form.cleaned_data)
        to_run = map(lambda x: x['id'], to_run)

        # TODO: slow, greate mass run method
        for test_case in to_run:
            TestCaseRun.run(test_case, testrun)

        return success(message='testrun directory saved',
                       data={"parent_id": getattr(testrun.parent, "id", 0),
                             "current_id": testrun.id})
    else:
        return failed(message="Validation errors",
                      data=testrun_form.errors_list())


def testcaserun(request, testcaserun_id):
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    testcaserun_status_form = forms.TestCaseRunStatus(instance=testcaserun)

    testcaserun_add_bug_form = forms.AddBugForm()
    return direct_to_template(request, 'execute/_testcaserun.html',
                              {'testcaserun': TestCaseRun.objects.get(pk=testcaserun_id),
                               'testcaserun_status_form': testcaserun_status_form,
                               'testcaserun_add_bug_form': testcaserun_add_bug_form})


@json_response
def testcaserun_setstatus(request, testcaserun_id):
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    testcaserun_status_form = forms.TestCaseRunStatus(request.POST, instance=testcaserun)
    if testcaserun_status_form.is_valid():
        testcaserun = testcaserun_status_form.save()
        return success(message=testcaserun.status.name,
                       data=dict(id=testcaserun.pk,
                                 name=testcaserun.status.name,
                                 color=testcaserun.status.color))
    else:
        return failed(message=testcaserun.status.name,
                      data=testcaserun_status_form.errors_list())


@json_response
def testcaserun_addbug(request, testcaserun_id):
    try:
        new_bug = Bug.objects.get(id=request.POST.get("id", None))
    except Bug.DoesNotExist:
        add_bug_form = forms.AddBugForm(request.POST)

        if not add_bug_form.is_valid():
            return failed(message="Validation error",
                      data=[(k, v[0]) for k, v in add_bug_form.errors.items()])

        new_bug = add_bug_form.save()
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    testcaserun.bugs.add(new_bug)
    return success(message="Issue #%s attached" % new_bug.name,
                   data=dict(id=new_bug.id))

