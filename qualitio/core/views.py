from mptt.models import MPTTModel
from reversion.models import Version

from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.simple import direct_to_template
from django.db.models.loading import get_model

from qualitio.core.utils import json_response


def to_tree_element(object, type):
    tree_element = {'attr': {'id': "%s_%s" % (object.pk, type),
                             'rel': type},
                    'data': object.name}

    if isinstance(object, MPTTModel):
        try:
            subchildren = getattr(getattr(object, "subchildren", None), "all", None)()
        except TypeError:  # Not really good idea, slow typecheck?
            subchildren = None
        if object.get_children() or subchildren:
            tree_element['state'] = "closed"

    return tree_element


@json_response
def get_children(request, directory):
    data = []

    try:
        node_id = int(request.GET.get('id', 0))
        node = directory.objects.get(pk=node_id)
        directories = node.children.all()
        data = map(lambda x: to_tree_element(x, x._meta.module_name), directories)
        try:
            subchildren = getattr(getattr(node, "subchildren", None), "all", None)()
            data.append(map(lambda x: to_tree_element(x, x._meta.module_name), subchildren))
        except TypeError:  # Not really good idea, slow typecheck?
            pass

    except (ObjectDoesNotExist, ValueError):
        # TODO: maybe the better way is to override method 'root_nodes' on manager
        directories = directory.tree.root_nodes().order_by('name')
        data = map(lambda x: to_tree_element(x, x._meta.module_name),
                   directories)

    return data


@json_response
def get_ancestors(request, app):

    Model = get_model(app, request.GET['type'])
    object = Model.objects.get(pk=request.GET['id'])

    ancestors = []
    if isinstance(object, MPTTModel): # directory?
        ancestors  = object.get_ancestors()
    else:
        if object.parent:
            ancestors = list(object.parent.get_ancestors())
            ancestors.extend([object.parent])
    return {"nodes": map(lambda x: '%s_%s' % (x.pk, x._meta.module_name), ancestors),
            "target": "%s_%s" % (object.pk, object._meta.module_name)}


def history(request, object_id, Model):
    object = Model.objects.get(pk=object_id)
    versions = Version.objects.get_for_object(object)
    return direct_to_template(request, 'core/history.html',
                              {'object': object,
                               'name' : object._meta.object_name,
                               'versions' : versions})
