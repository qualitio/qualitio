from mptt.models import MPTTModel

from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson as json
from django.http import HttpResponse

from qualitio.core.utils import json_response, success, failed
from qualitio.execute.models import TestRunDirectory, TestRun
from qualitio.execute.forms import TestRunDirectoryForm, TestRunForm

def index(request):
    return direct_to_template(request,'execute/base.html',{})

def directory_details(request, directory_id):
    return direct_to_template(request, 'execute/testrundirectory_details.html',
                              {'directory' : TestRunDirectory.objects.get(pk=directory_id)})

def directory_new(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrundirectory_form = TestRunDirectoryForm(initial={'parent': directory })
    print testrundirectory_form
    return direct_to_template(request, 'execute/testrundirectory_edit.html',
                              {'testrundirectory_form' : testrundirectory_form})

def directory_edit(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrundirectory_form = TestRunDirectoryForm(instance=directory)
    return direct_to_template(request, 'execute/testrundirectory_edit.html',
                              {'testrundirectory_form' : testrundirectory_form})

@json_response
def directory_valid(request, directory_id=0):
    if directory_id:
        testrun_directory = TestRunDirectory.objects.get(pk=str(directory_id))
        testrun_directory_form = TestRunDirectoryForm(request.POST, instance=testrun_directory)
    else:
        testrun_directory_form = TestRunDirectoryForm(request.POST)

    if testrun_directory_form.is_valid():
        testrun_directory = testrun_directory_form.save()
        return success(message='testrun directory saved',
                       data={ "parent_id" : getattr(testrun_directory.parent,"id", 0),
                              "current_id" : testrun_directory.id })
    else:
        return failed(message="Validation errors",
                      data=[(k, v[0]) for k, v in testrun_directory_form.errors.items()])

def testrun_details(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_details.html',
                              {'testrun' : TestRun.objects.get(pk=testrun_id)})

def testrun_execute(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_execute.html',
                              {'testrun' : TestRun.objects.get(pk=testrun_id)})

def testrun_notes(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_notes.html',
                              {'testrun' : TestRun.objects.get(pk=testrun_id)})

def testrun_new(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    testrun_form = TestRunForm(initial={'parent': directory})
    return direct_to_template(request, 'execute/testrun_edit.html',
                              { "testrun_form" : testrun_form })

def testrun_edit(request, testrun_id):
    testrun = TestRun.objects.get(pk=testrun_id)
    testrun_form = TestRunForm(instance=testrun)
    return direct_to_template(request, 'execute/testrun_edit.html',
                              {'testrun' : testrun,
                               'testrun_form' : testrun_form})
@json_response
def testrun_valid(request, testrun_id=0):
    if testrun_id:
        testrun = TestRun.objects.get(pk=str(testrun_id))
        testrun_form = TestRunForm(request.POST, instance=testrun)
    else:
        testrun_form = TestRunForm(request.POST)

    if testrun_form.is_valid():
        testrun = testrun_form.save()
        return success(message='testrun directory saved',
                       data={ "parent_id" : getattr(testrun.parent,"id", 0),
                              "current_id" : testrun.id })
    else:
        return failed(message="Validation errors",
                      data=[(k, v[0]) for k, v in testrun_form.errors.items()])


# @json_response
# def available_testcases(request, requirement_id):
#     search_testcases_form = SearchTestcasesForm(request.POST)
#     if search_testcases_form.is_valid():
#         search = request.POST["search"]
#         testcases =  TestCase.objects.filter(Q(name__contains=search) | Q(path__contains=search))
#         if testcases:
#             return success(message="%s testcases found" % testcases.count(),
#                            data=loader.render_to_string("requirements/_available_testcases.html",
#                                                         { "testcases" : testcases }))
#         return success(message="no testcases found")

#     return failed(message="validation errors",
#                   data=[(k, v[0]) for k, v in search_testcases_form.errors.items()])


def to_tree_element(object, type):
    tree_element = { 'attr' : {'id' : "%s_%s" % (object.pk, type),
                               'rel' : type},
                     'data' : object.name }

    if isinstance(object, MPTTModel):
        #TODO: temporary solution, remove TestRun call with something thath will be more generic,
        #      and will aply to all tree objects
        if object.get_children() or TestRun.objects.filter(parent=object):
            tree_element['state'] = "closed"

    return tree_element


def get_children(request):
    data = []

    try:
        node_id = int(request.GET.get('id', 0))
        node = TestRunDirectory.objects.get(pk=node_id)
        directories = node.get_children()
        files = node.testrun_set.all()
        data = map(lambda x: to_tree_element(x, x._meta.module_name), directories)+\
               map(lambda x: to_tree_element(x,x._meta.module_name), files)

    except (ObjectDoesNotExist, ValueError):
        directories = TestRunDirectory.tree.root_nodes()
        data = map(lambda x: to_tree_element(x, x._meta.module_name), directories)

    return HttpResponse(json.dumps(data), mimetype="application/json")
