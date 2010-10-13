from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType

from tcstorm_requirements.report.models import ReportDirectory, Report
from tcstorm_requirements.report.forms import ReportForm, QueryFormSet, ReportDirectoryForm

def index(request):
    return render_to_response('report/base.html',
                              context_instance=RequestContext(request))

def menu(request, node_type, node_id, view):
    object_type = lambda x: ContentType.objects.get(app_label="report", model=x)
    return render_to_response('report/%s_menu.html' % node_type,
                              { 'object' : object_type(node_type).get_object_for_this_type(id=node_id) },
                              context_instance=RequestContext(request))

def report_details(request, report_id):
    return render_to_response('report/report_details.html',
                              {'report' : Report.objects.get(pk=report_id) },
                              context_instance=RequestContext(request))

def report_edit(request, report_id):
    report = Report.objects.get(pk=report_id)
    return render_to_response('report/report_edit.html',
                              {'report_form' : ReportForm(instance=report),
                               'query_formset' : QueryFormSet(instance=report)},
                              context_instance=RequestContext(request))



def reportdirectory_details(request, reportdirectory_id):
    reportdirectory = ReportDirectory.objects.get(pk=reportdirectory_id)

    return render_to_response('report/reportdirectory_details.html',
                              {'reportdirectory' : ReportDirectory.objects.get(pk=reportdirectory_id)},
                              context_instance=RequestContext(request))

def reportdirectory_edit(request, reportdirectory_id):
    reportdirectory = ReportDirectory.objects.get(pk=reportdirectory_id)
    return render_to_response('report/reportdirectory_edit.html',
                              {'reportdirectory_form' : ReportDirectoryForm(instance=reportdirectory)},
                              context_instance=RequestContext(request))


def edit_valid(request, report_id):
    report = Report.objects.get(pk=report_id)
    return render_to_response('report/edit.html',
                              {'report_form' : ReportForm(instance=report) },
                              context_instance=RequestContext(request))


def to_tree_element(object, type):
    return { 'data' : object.name,
             'attr' : {'id' : "%s_%s" % (object.pk, type),
                       'rel' : type},
             'state' : 'closed',
             'children' : []}


def get_children(request):
    data = []

    node_id = int(request.GET['id'])
    node_type = request.GET.get("type") or "reportdirectory"

    if node_type == "reportdirectory":
        node_id = int(request.GET['id'])
        if not node_id:
            directories = ReportDirectory.tree.root_nodes()
            data = map(lambda x: to_tree_element(x, x._meta.module_name), directories)
        else:
            node = ReportDirectory.objects.get(pk=node_id)
            directories = node.get_children()
            reports = node.report_set.all()

            data = map(lambda x: to_tree_element(x, x._meta.module_name), directories) + map(lambda x: to_tree_element(x,x._meta.module_name), reports)

    return HttpResponse(json.dumps(data), mimetype="application/json")
