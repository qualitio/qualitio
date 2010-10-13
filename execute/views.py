from django.views.generic.simple import direct_to_template

def index(request):
    return direct_to_template(request,'execute/base.html',{})


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
