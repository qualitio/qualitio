from mptt.models import MPTTModel
from django.core.exceptions import ObjectDoesNotExist
from qualitio.core.utils import json_response


def to_tree_element(object, type):
    tree_element = {'attr': {'id': "%s_%s" % (object.pk, type),
                             'rel': type},
                    'data': object.name}

    if isinstance(object, MPTTModel):
        if object.get_children() or object.subchildren.all():
            tree_element['state'] = "closed"

    return tree_element


@json_response
def get_children(request, directory):
    data = []

    try:
        node_id = int(request.GET.get('id', 0))
        node = directory.objects.get(pk=node_id)
        directories = node.get_children()
        files = node.subchildren.all()
        data = map(lambda x: to_tree_element(x, x._meta.module_name),
                   directories) + \
               map(lambda x: to_tree_element(x, x._meta.module_name), files)

    except (ObjectDoesNotExist, ValueError):
        directories = directory.tree.root_nodes()
        data = map(lambda x: to_tree_element(x, x._meta.module_name),
                   directories)

    return data
