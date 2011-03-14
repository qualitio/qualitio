from reversion import revision

from django.views.generic.simple import direct_to_template
from django.utils.encoding import force_unicode

from qualitio.core.utils import json_response, success, failed
from qualitio import store
from qualitio.execute.models import TestRunDirectory, TestRun, TestCaseRun
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

@revision.create_on_success
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

        comment = testrun_directory_form.changelog()
        if comment:
            revision.comment = comment
            revision.user = request.user
        else:
            revision.invalidate()

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
    available_test_cases_form = forms.AvailableTestCases(prefix="available_test_cases")
    connected_test_cases_form = forms.ConnectedTestCases(request.POST,
                                                         prefix="connected_test_cases")
    return direct_to_template(request, 'execute/testrun_edit.html',
                              {"testrun_form": testrun_form,
                               'available_test_cases_form': available_test_cases_form,
                               'connected_test_cases_form' : connected_test_cases_form})


def testrun_edit(request, testrun_id):
    testrun = TestRun.objects.get(pk=testrun_id)
    testrun_form = forms.TestRunForm(instance=testrun, prefix="testrun")
    connected_test_cases_form = forms.ConnectedTestCases(instance=testrun,
                                                         prefix="connected_test_cases")
    available_test_cases_form = forms.AvailableTestCases(
        prefix="available_test_cases",
        queryset=store.TestCase.objects.exclude(testcaserun__parent=testrun))

    return direct_to_template(request, 'execute/testrun_edit.html',
                              {'testrun_form': testrun_form,
                               'available_test_cases_form': available_test_cases_form,
                               'connected_test_cases_form' : connected_test_cases_form})

@revision.create_on_success
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

        # TODO: slow, create mass run method
        for test_case in to_run:
            TestCaseRun.run(test_case, testrun)

        comment = [testrun_form.changelog(),
                   connected_test_cases_form.changelog(),
                   available_test_cases_form.changelog()]

        if any(comment):
            revision.comment = " ".join(comment)
            revision.user = request.user
        else:
            revision.invalidate()

        return success(message='testrun directory saved',
                       data={"parent_id": getattr(testrun.parent, "id", 0),
                             "current_id": testrun.id})
    else:
        return failed(message="Validation errors",
                      data=testrun_form.errors_list())


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


@revision.create_on_success
@json_response
def testcaserun_setstatus(request, testcaserun_id):
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    testcaserun_status_form = forms.TestCaseRunStatus(request.POST, instance=testcaserun)
    if testcaserun_status_form.is_valid():
        testcaserun = testcaserun_status_form.save()

        revision.comment = testcaserun_status_form.changelog()
        revision.user = request.user

        return success(message=testcaserun.status.name,
                       data=dict(id=testcaserun.pk,
                                 name=testcaserun.status.name,
                                 color=testcaserun.status.color))
    else:
        return failed(message=testcaserun.status.name,
                      data=testcaserun_status_form.errors_list())


@revision.create_on_success
@json_response
def testcaserun_addbug(request, testcaserun_id):

    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    add_bug_form = forms.AddBugForm(request.POST)

    if add_bug_form.is_valid():
        from backends.bugs import Bugzilla, IssueError, IssueServerError
        bugs = []
        for bug_id in add_bug_form.cleaned_data['bugs']:
            try:
                bugs.append(testcaserun.bugs.get_or_create(**Bugzilla.fetch_bug(bug_id))[0])
            except (IssueError, IssueServerError) as e:
                return failed(message="Issue server error meessage: %s" %e)

        revision.add(testcaserun)
        revision.user = request.user
        message = []
        for bug in bugs:
            message.append('Created %(name)s "%(object)s"'
                           % {'name': force_unicode(bug._meta.verbose_name),
                              'object': force_unicode(bug)})

        revision.comment = "%s %s: %s." % (testcaserun._meta.verbose_name.capitalize(),
                                          testcaserun.pk,
                                          ", ".join(message))

        return success(message=revision.comment,
                       data=dict(testcaserun=testcaserun.id,
                                 created_bugs=map(lambda x: { "alias" : x.alias,
                                                              "name": x.name,
                                                              "status" : x.status,
                                                              "resolution": x.resolution },
                                                  bugs),
                                 all_bugs=list(testcaserun.bugs.values_list('alias', flat=True))))

    return failed(message="Validation error",
                  data=add_bug_form.errors_list())


@revision.create_on_success
@json_response
def testcaserun_removebug(request, testcaserun_id):
    testcaserun = TestCaseRun.objects.get(pk=testcaserun_id)
    bugs_formset = forms.BugFormSet(request.POST, instance=testcaserun)

    if bugs_formset.is_valid():
        bugs_formset.save()

        revision.add(testcaserun)
        revision.user = request.user
        revision.comment = "%s %s. %s" % (testcaserun._meta.verbose_name.capitalize(),
                                          testcaserun.pk,
                                          bugs_formset.changelog())

        return success(message="Issue(s) removed",
                   data=dict(id=testcaserun.id,
                             all=map(lambda x: x.id, testcaserun.bugs.all())))

    return failed(message="Validation error",
                  data=bugs_formset.errors_list())

