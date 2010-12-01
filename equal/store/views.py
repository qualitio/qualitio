from mptt.models import MPTTModel

from django.views.generic.simple import direct_to_template
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson as json
from django.http import HttpResponse

from equal.store.models import TestCaseDirectory, TestCase
from equal.store import forms   

def index(request):
    return direct_to_template(request, 'store/base.html', {})

def directory_details(request, directory_id): 
    return direct_to_template(request, 'store/testcasedirectory_details.html',
                              {'directory' : TestCaseDirectory.objects.get(pk=directory_id)})

def directory_edit(request, directory_id):
    directory = TestCaseDirectory.objects.get(pk=directory_id)
    testcasedirectory_form = forms.TestCaseDirectoryForm(instance=directory)
    return direct_to_template(request, 'store/testcasedirectory_edit.html',
                              {'directory' : directory, 
                               'testcasedirectory_form' : testcasedirectory_form })

def testcase_details(request, testcase_id):
    return direct_to_template(request, 'store/testcase_details.html',
                              {'testcase' : TestCase.objects.get(pk=testcase_id)})

def testcase_edit(request, testcase_id):
    testcase = TestCase.objects.get(pk=testcase_id)
    testcase_form = forms.TestCaseForm(instance=testcase)
    testcasesteps_form = forms.TestCaseStepFormSet(instance=testcase)
    glossary_word_search_form = forms.GlossaryWord()
    return direct_to_template(
        request, 'store/testcase_edit.html',
        {'testcase' : testcase,
         'testcase_form' : testcase_form,
         'testcasesteps_form' : testcasesteps_form,
         'glossary_word_search_form' : glossary_word_search_form, 
         })

def testcase_attachments(request, testcase_id):
    testcase = TestCase.objects.get(pk=testcase_id)
    attachments_form = forms.AttachmentFormSet(instance=testcase)
    return direct_to_template(request, 'store/testcase_attachments.html',
                              {'testcase' : testcase,
                               'attachments_form' : attachments_form})

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
        node = TestCaseDirectory.objects.get(pk=node_id)
        directories = node.get_children()
        files = node.testcase_set.all()

    except (ObjectDoesNotExist, ValueError):
        directories = TestCaseDirectory.tree.root_nodes()
        files = TestCase.objects.filter(parent=None)
    
    data = map(lambda x: to_tree_element(x, x._meta.module_name), directories)+\
        map(lambda x: to_tree_element(x,x._meta.module_name), files)

    return HttpResponse(json.dumps(data), mimetype="application/json")
