from mptt.models import MPTTModel

from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson as json
from django.http import HttpResponse

from equal.execute.models import TestRunDirectory, TestRun
from equal.execute.forms import TestRunDirectoryForm, TestRunForm

def index(request):
    return direct_to_template(request,'execute/base.html',{})

def directory_details(request, directory_id):
    return direct_to_template(request, 'execute/testrundirectory_details.html',
                              {'directory' : TestRunDirectory.objects.get(pk=directory_id)})

def directory_new(request, directory_id):
    return direct_to_template(request, 'execute/testrundirectory_new.html',
                              {'directory' : TestRunDirectory.objects.get(pk=directory_id)})

def directory_edit(request, directory_id):
    directory = TestRunDirectory.objects.get(pk=directory_id)
    return direct_to_template(request, 'execute/testrundirectory_edit.html',
                              {'directory' : directory,
                               'directory_form' : TestRunDirectoryForm(instance=directory)})

def testrun_details(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_details.html',
                              {'testrun' : TestRun.objects.get(pk=testrun_id)})

def testrun_edit(request, testrun_id):
    testrun = TestRun.objects.get(pk=testrun_id)
    testrun_form = TestRunForm(instance=testrun)
    return direct_to_template(request, 'execute/testrun_edit.html',
                              {'testrun' : testrun,
                               'testrun_form' : testrun_form})

def testrun_execute(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_execute.html',
                              {'testrun' : TestRun.objects.get(pk=testrun_id)})

def testrun_notes(request, testrun_id):
    return direct_to_template(request, 'execute/testrun_notes.html',
                              {'testrun' : TestRun.objects.get(pk=testrun_id)})



def to_tree_element(object, type):
    state = "closed" if isinstance(object, MPTTModel) else ""
    return { 'attr' : {'id' : "%s_%s" % (object.pk, type),
                       'rel' : type},
             'data' : object.name,
             'state' : state }

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

        print data
    return HttpResponse(json.dumps(data), mimetype="application/json")
