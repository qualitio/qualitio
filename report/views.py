from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson as json
from django.shortcuts import render_to_response

from tcstorm_requirements.report.models import ReportDirectory, Report


def index(request):
    return render_to_response('report/base.html', 
                              context_instance=RequestContext(request))

def details(request, report_id):
    return render_to_response('report/details.html',
                              {'report' : Report.objects.get(pk=requirement_id) },
                              context_instance=RequestContext(request))

def edit(request, report_id):
    report = Report.objects.get(pk=report_id)
    return render_to_response('report/edit.html',
                              {'report_form' : ReportForm(instance=report) },
                              context_instance=RequestContext(request))

def edit_valid(request, report_id):
    report = Report.objects.get(pk=report_id)
    return render_to_response('report/edit.html',
                              {'report_form' : ReportForm(instance=report) },
                              context_instance=RequestContext(request))


def to_tree_element(object, type):
    return { 'data' : object.name,
             'attr' : {'id' : object.pk,  'rel' : type},
             'state' : 'closed', 
             'children' : [] }


def get_children(request):
    data = []
    
    node_id = int(request.GET['id'])
    node_type = request.GET.get("type") or "directory"

    if node_type == "directory":
        node_id = int(request.GET['id'])
        if not node_id:
            directories = ReportDirectory.tree.root_nodes()
            data = map(lambda x: to_tree_element(x,"directory"), directories)
        else:
            node = ReportDirectory.objects.get(pk=node_id)
            directories = node.get_children()
            reports = node.report_set.all()
            
            data = map(lambda x: to_tree_element(x,"directory"), directories) + map(lambda x: to_tree_element(x,"file"), reports)

    return HttpResponse(json.dumps(data), mimetype="application/json")
