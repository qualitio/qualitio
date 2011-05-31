from django.contrib.auth.decorators import permission_required
from django.views.generic.simple import direct_to_template
from django.db.models import Count
from django.conf import settings

from qualitio.core.utils import json_response, success, failed
from qualitio import store
from qualitio.execute.models import TestRunDirectory, TestRun, TestCaseRun, TestCaseRunStatus
from qualitio.execute import forms
from qualitio import history


def index(request):
    return direct_to_template(request, 'execute/base.html', {})


def directory_details(request, directory_id):
    return direct_to_template(request, 'execute/testrundirectory_details.html',
                              {'directory': TestRunDirectory.objects.get(pk=directory_id)})


@permission_required('execute.add_testrundirectory', login_url='/permission_required/')
def directory_new(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrundirectory_form = forms.TestRunDirectoryForm(initial={'parent': directory})
    return direct_to_template(request, 'execute/testrundirectory_edit.html',
                              {'testrundirectory_form': testrundirectory_form})


@permission_required('execute.change_testrundirectory', login_url='/permission_required/')
def directory_edit(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrundirectory_form = forms.TestRunDirectoryForm(instance=directory)
    return direct_to_template(request, 'execute/testrundirectory_edit.html',
                              {'testrundirectory_form': testrundirectory_form})


@json_response
def directory_valid(request, directory_id=0):
    # TODO: should we think about permissions for valid views?
    if directory_id:
        testrun_directory = TestRunDirectory.objects.get(pk=str(directory_id))
        testrun_directory_form = forms.TestRunDirectoryForm(request.POST,
                                                            instance=testrun_directory)
    else:
        testrun_directory_form = forms.TestRunDirectoryForm(request.POST)

    if testrun_directory_form.is_valid():
        testrun_directory = testrun_directory_form.save()

        log = history.History(request.user, testrun_directory)
        log.add_form(testrun_directory_form)
        log.save()

        return success(message='testrun directory saved',
                       data={"parent_id": getattr(testrun_directory.parent, "id", 0),
                             "current_id": testrun_directory.id})
    else:
        return failed(message="Validation errors: %s" % testrun_directory_form.error_message(),
                      data=testrun_directory_form.errors_list())


def testrun_details(request, testrun_id):
    testrun = TestRun.objects.get(pk=testrun_id)
    return direct_to_template(request, 'execute/testrun_details.html',
                              {'testrun': testrun})


@permission_required('execute.add_testrun', login_url='/permission_required/')
def testrun_new(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrun_form = forms.TestRunForm(initial={'parent': directory})

    return direct_to_template(request, 'execute/testrun_edit.html',
                              {"testrun_form": testrun_form,
                               'available_test_cases': store.TestCase.objects.all()})


@permission_required('execute.change_testrun', login_url='/permission_required/')
def testrun_edit(request, testrun_id):
    testrun = TestRun.objects.get(pk=testrun_id)
    testrun_form = forms.TestRunForm(instance=testrun, prefix="testrun")

    return direct_to_template(request, 'execute/testrun_edit.html',
                              {'testrun_form': testrun_form,
                               'available_test_cases': store.TestCase.objects.all(),
                               'connected_test_cases' : testrun.testcases.all()})


@permission_required('execute.change_testrun', login_url='/permission_required/')
def testrun_notes(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_notes.html',
                              {'testrun': TestRun.objects.get(pk=testrun_id)})


@json_response
def testrun_valid(request, testrun_id=0):
    if testrun_id:
        testrun = TestRun.objects.get(pk=str(testrun_id))
        testrun_form = forms.TestRunForm(request.POST, instance=testrun, prefix="testrun")

    else:
        testrun_form = forms.TestRunForm(request.POST)

    if testrun_form.is_valid():
        testrun = testrun_form.save()

        testcase_id_list = list(set(request.POST.getlist('connected_test_case')))
        testcases = store.TestCase.objects.filter(pk__in=testcase_id_list)

        created_testcases, deleted_testcases = testrun.testcase_setup(testcases)
        testrun.update_passrate()

        log = history.History(request.user, testrun)
        log.add_form(testrun_form)
        log.add_objects(created=created_testcases, deleted=deleted_testcases)
        log.save()

        return success(message='Test run saved',
                       data={"parent_id": getattr(testrun.parent, "id", 0),
                             "current_id": testrun.id})

    else:
        return failed(message="Validation errors: %s" % testrun_form.error_message(),
                      data=testrun_form.errors_list())


@permission_required('execute.change_testrun', login_url='/permission_required/')
def testrun_execute(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_execute.html',
                              {'testrun': TestRun.objects.get(pk=testrun_id)})


def testcaserun(request, testcaserun_id):
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    testcaserun_status_form = forms.TestCaseRunStatus(instance=testcaserun)


    bugs_formset = forms.BugFormSet(instance=testcaserun)
    return direct_to_template(request, 'execute/_testcaserun.html',
                              {'testcaserun': TestCaseRun.objects.get(pk=testcaserun_id),
                               'testcaserun_status_form': testcaserun_status_form,
                               'bugs_formset': bugs_formset
                               })


def testcaserun_bugs(request, testcaserun_id):
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    if request.method == "POST":
        bugs_formset = forms.BugFormSet(request.POST, instance=testcaserun)
        if bugs_formset.is_valid():
            bugs_formset.save()

    bugs_formset = forms.BugFormSet(instance=testcaserun)
    testcaserun_add_bug_form = forms.AddBugForm()
    return direct_to_template(request, 'execute/_testcaserun_bugs.html',
                              {'bugs_formset': bugs_formset,
                               'testcaserun_add_bug_form': testcaserun_add_bug_form})


@json_response
def testcaserun_setstatus(request, testcaserun_id):
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    testcaserun_status_form = forms.TestCaseRunStatus(request.POST, instance=testcaserun)
    if testcaserun_status_form.is_valid():
        testcaserun = testcaserun_status_form.save()

        log = history.History(request.user, testcaserun.parent)
        log.add_form(testcaserun_status_form, capture=["status"], prefix=True)
        log.save()

        # TODO: move this to testrun? method. Chec also templatetags
        passrate_ratio = []
        testrun = testcaserun.parent
        testcaseruns_count = testrun.testcases.count()
        statuses = TestCaseRunStatus.objects.filter(testcaserun__parent=testrun).annotate(count=Count('testcaserun'))
        for status in statuses:
            passrate_ratio.append({
                "ratio": float(status.count) / float(testcaseruns_count) * 100,
                "name": status.name,
                "color": status.color,
                })

        return success(message=testcaserun.status.name,
                       data=dict(id=testcaserun.pk,
                                 name=testcaserun.status.name,
                                 color=testcaserun.status.color,
                                 passrate=testcaserun.parent.passrate,
                                 passrate_ratio=passrate_ratio))
    else:
        return failed(message=testcaserun.status.name,
                      data=testcaserun_status_form.errors_list())


@json_response
def testcaserun_addbug(request, testcaserun_id):

    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    add_bug_form = forms.AddBugForm(request.POST)

    from django.utils.importlib import import_module

    backend_name = getattr(settings, "ISSUE_BACKEND", None)
    issues = import_module(backend_name)

    if add_bug_form.is_valid():
        bugs = []
        for bug_id in add_bug_form.cleaned_data['bugs']:
            try:
                bugs.append(testcaserun.bugs.get_or_create(**issues.Backend.fetch_bug(bug_id))[0])
            except (issues.IssueError, issues.IssueServerError) as e:
                return failed(message="Issue server error meessage: %s" %e)


        log = history.History(request.user, testcaserun.parent)
        log.add_objects(created=bugs, prefix_object=testcaserun)
        log.save()
        return success(message="Issue(s) created.",
                       data=dict(testcaserun=testcaserun.id,
                                 created_bugs=map(lambda x: { "alias" : x.alias,
                                                              "name": x.name,
                                                              "status" : x.status,
                                                              "resolution": x.resolution },
                                                  bugs),
                                 all_bugs=list(testcaserun.bugs.values_list('alias', flat=True))))

    return failed(message="Validation error",
                  data=add_bug_form.errors_list())


@json_response
def testcaserun_removebug(request, testcaserun_id):
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    bugs_formset = forms.BugFormSet(request.POST, instance=testcaserun)

    if bugs_formset.is_valid():
        bugs_formset.save()

        log = history.History(request.user, testcaserun.parent)
        log.add_formset(bugs_formset, prefix=True)
        log.save()
        return success(message="Issue(s) deleted.",
                       data=dict(id=testcaserun.id,
                                 all=map(lambda x: x.id, testcaserun.bugs.all())))

    return failed(message="Validation error",
                  data=bugs_formset.errors_list())


