from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import permission_required

from qualitio import core
from qualitio.core.utils import json_response, success, failed
from qualitio.store.models import TestCaseDirectory, TestCase
from qualitio.store.forms import TestCaseForm, TestCaseDirectoryForm, TestCaseStepFormSet, GlossaryWord

from qualitio import history


def index(request):
    return direct_to_template(request, 'store/base.html', {})


@core.menu_view(TestCaseDirectory, "details")
def directory_details(request, directory_id):
    return direct_to_template(request, 'store/testcasedirectory_details.html',
                              {'directory': TestCaseDirectory.objects.get(pk=directory_id)})


@core.menu_view(TestCaseDirectory, "edit", 'store.add_testcasedirectory')
@permission_required('store.add_testcasedirectory', login_url='/permission_required/')
def directory_edit(request, directory_id):
    directory = TestCaseDirectory.objects.get(pk=directory_id)
    testcasedirectory_form = TestCaseDirectoryForm(instance=directory)
    return direct_to_template(request, 'store/testcasedirectory_edit.html',
                              {'testcasedirectory_form': testcasedirectory_form})


@permission_required('store.add_testcasedirectory', login_url='/permission_required/')
def directory_new(request, directory_id):
    directory = TestCaseDirectory.objects.get(pk=directory_id)
    testcasedirectory_form = TestCaseDirectoryForm(initial={'parent': directory})
    return direct_to_template(request, 'store/testcasedirectory_edit.html',
                              {'testcasedirectory_form': testcasedirectory_form})


@json_response
def directory_valid(request, directory_id=0):
    if directory_id:
        testcase_directory = TestCaseDirectory.objects.get(pk=directory_id)
        testcase_directory_form = TestCaseDirectoryForm(request.POST, instance=testcase_directory)
    else:
        testcase_directory_form = TestCaseDirectoryForm(request.POST)

    if testcase_directory_form.is_valid():
        testcase_directory = testcase_directory_form.save()

        log = history.History(request.user, testcase_directory)
        log.add_form(testcase_directory_form, is_new=(directory_id == 0))
        log.save()
        return success(message='Directory saved',
                       data={"parent_id": getattr(testcase_directory.parent, "id", 0),
                             "current_id": testcase_directory.id})
    else:
        return failed(message="Validation errors: %s" % testcase_directory_form.error_message(),
                      data=testcase_directory_form.errors_list())


@core.menu_view(TestCase, "details")
def testcase_details(request, testcase_id):
    return direct_to_template(request, 'store/testcase_details.html',
                              {'testcase': TestCase.objects.get(pk=testcase_id)})


@permission_required('store.change_testcase', login_url='/permission_required/')
@core.menu_view(TestCase, "edit", 'store.change_testcase')
def testcase_edit(request, testcase_id):
    testcase = TestCase.objects.get(pk=testcase_id)
    testcase_form = TestCaseForm(instance=testcase)
    testcasesteps_form = TestCaseStepFormSet(instance=testcase)
    glossary_word_search_form = GlossaryWord()
    return direct_to_template(request, 'store/testcase_edit.html',
                              {'testcase_form': testcase_form,
                                'testcasesteps_form': testcasesteps_form,
                                'glossary_word_search_form': glossary_word_search_form})


@permission_required('store.add_testcase', login_url='/permission_required/')
def testcase_new(request, directory_id):
    directory = TestCaseDirectory.objects.get(pk=directory_id)
    testcase_form = TestCaseForm(initial={'parent': directory})
    testcasesteps_form = TestCaseStepFormSet()
    return direct_to_template(request, 'store/testcase_edit.html',
                              {"testcase_form": testcase_form,
                               "testcasesteps_form": testcasesteps_form})


@json_response
def testcase_valid(request, testcase_id=0):
    if testcase_id:
        testcase = TestCase.objects.get(pk=str(testcase_id))
        testcase_form = TestCaseForm(request.POST, instance=testcase)
        testcasesteps_form = TestCaseStepFormSet(request.POST, instance=testcase)
    else:
        testcase_form = TestCaseForm(request.POST)
        testcasesteps_form = TestCaseStepFormSet(request.POST)

    if testcase_form.is_valid() and testcasesteps_form.is_valid():
        testcase = testcase_form.save()
        testcasesteps_form.instance = testcase
        testcasesteps_form.save()

        log = history.History(request.user, testcase)
        log.add_form(testcase_form, is_new=(testcase_id == 0))
        log.add_formset(testcasesteps_form)
        log.save()
        return success(message='TestCase saved',
                       data={"parent_id": getattr(testcase.parent, "id", 0),
                              "current_id": testcase.id})
    else:
        return failed(message="Validation errors: %s" % testcase_form.error_message(),
                      data=testcase_form.errors_list() + testcasesteps_form._errors_list())

