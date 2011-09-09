import operator

from mptt.models import MPTTModel
from reversion.models import Version

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.loading import get_model
from django.views.generic.simple import direct_to_template

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
def get_children(request, directory, *args, **kwargs):
    data = []

    try:
        node_id = int(request.GET.get('id', 0))
        node = directory.objects.get(pk=node_id)
        directories = node.children.order_by('name')
        data = map(lambda x: to_tree_element(x, x._meta.module_name), directories)
        try:
            subchildren = getattr(node, "subchildren", None)
            subchildren = getattr(subchildren, "order_by", lambda *a, **k: None)('name')

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
def get_ancestors(request, app, *args, **kwargs):

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


def history(request, object_id, Model, *args, **kwargs):
    object = Model.objects.get(pk=object_id)
    versions = Version.objects.get_for_object(object)
    return direct_to_template(request, 'core/history.html',
                              {'object': object,
                               'name' : object._meta.object_name,
                               'versions' : versions})


def permission_required(request, *args, **kwargs):
    return direct_to_template(request, 'core/permission_required.html')


registry = {}
def menu_view(_object,  view_name, perm="", index=-1, *args, **kwargs):
    if index < 0:
        index = len(registry)-index+1 # this is only append

    if registry.has_key(_object):
        registry[_object].insert(index, dict(name=view_name, perm=perm))
    else:
        registry[_object] = [dict(name=view_name, perm=perm)]

    def _menu_view(function):
        def __menu_view(*args, **kw):
            return function(*args, **kw)
        return __menu_view
    return _menu_view


# jQuery DataTable's ajax params helper #################
class DataTableColumn(object):
    """
    Column that represents jQuery DataTable column.
    The main responsibility is to create criteria (django ``Q`` objects)
    for each client-side table column.

    Params:
       - ``name``
         name of models *attribute* (not the column label or name); if column have
         information from ForeignKey field then use normal django-orm-like queries strings,
         eg. for store.TestCase.requirement attribute the column name should be:
         ``requirement__name``.

       - ``is_searchable``
         think it's self-descibing

       - ``search``
         the search query, should contains query specified by a user; if query is NOT defined
         for specific column, the search query from DataTables search field is used.

       - ``search_is_regex``
         tells column object should tread serach query as regex pattern

    Used internally by DataTable class.
    """
    def __init__(self, name=None, is_searchable=False, search=None, search_is_regex=None):
        self.name = name
        self.is_searchable = is_searchable
        self.search = search
        self.search_is_regex = search_is_regex

    def search_key(self):
        if self.search_is_regex:
            return '%s__regex' % self.name
        return '%s__icontains' % self.name

    def construct_Q(self):
        if not self.is_searchable:
            return Q()

        if not self.search:
            return Q()

        return Q(**{self.search_key():self.search})


class DataTableOptions(object):
    """
    Represents jQuery DataTable options send by the plugin
    via ajax request.
    Usage:

    def myview(request, ...):
        options = DataTableOptions(request.GET)
        # do something with options

    """

    def getitem(self, itemable, key, *args):
        """
        Work's pretty much the same as ``getattr`` function
        but for objects that have ``__getitem__`` method.
        """
        try:
            return itemable[key]
        except (IndexError, KeyError):
            if args:
                return args[0]
            raise

    def _get_name(self, column_names, column_index):
        return self.getitem(column_names, column_index, None)  # default name is None

    def _get_searchable(self, opts_dict, column_index):
        return opts_dict.get('bSearchable_%s' % column_index, 'false') == 'true'

    def _get_search_query(self, opts_dict, column_index):
        return opts_dict.get('sSearch_%s' % column_index, self.search) or self.search

    def _get_search_is_regex(self, opts_dict, column_index):
        return opts_dict.get('bRegex_%s' % column_index, 'false') == 'true' or self.search_is_regex

    def _get_columns(self, columns_names, params):
        columns = []
        for i in xrange(len(columns_names)):
            columns.append(DataTableColumn(**{
                        'name': self._get_name(columns_names, i),
                        'is_searchable': self._get_searchable(params, i),
                        'search': self._get_search_query(params, i),
                        'search_is_regex': self._get_search_is_regex(params, i),
                        }))
        return columns

    def _get_ordering(self, columns, params):
        ordering = None
        sorting_column_index = int(params.get('iSortingCols', None))
        sorting_column_dir = params.get('sSortDir_0', 'asc')

        if sorting_column_index:
            ordering = columns[sorting_column_index].name
            if sorting_column_dir == 'desc':
                ordering = '-%s' % ordering

        return ordering

    def __init__(self, model, column_names, params):
        self.search = params.get('sSearch', '')
        self.search_is_regex = params.get('bRegex', 'false') == 'true'
        self.columns = self._get_columns(column_names, params)
        self.model = model
        self.limit = int(params.get('iDisplayLength', 100))
        self.start_record = int(params.get('iDisplayStart', 0))
        self.end_record = self.start_record + self.limit
        self.echo = int(params.get('sEcho', 1))
        self.ordering = self._get_ordering(self.columns, params)


class DataTable(object):
    model = None

    def __init__(self, columns=None, params=None, model=None, queryset=None):
        self._count = None  # cache count field
        self._meta = DataTableOptions(model or self.__class__.model or queryset.model, columns, params)
        if queryset is not None:
            self._queryset = queryset
        else:
            self._queryset = self._meta.model.objects

    def construct_Q(self):
        return reduce(operator.or_, [col.construct_Q() for col in self._meta.columns])

    def queryset(self):
        qs = self._queryset.filter(self.construct_Q())
        if self._meta.ordering:
            return qs.order_by(self._meta.ordering)
        return qs

    def count(self):
        if self._count is None:
            self._count = self.queryset().count()
        return self._count

    def slice_queryset(self):
        return self.queryset()[self._meta.start_record:self._meta.end_record]

    def map(self, function):
        return map(function, self.slice_queryset())

    def response_dict(self, mapitem=lambda x: x):
        return {
            'iTotalRecords': self.count(),
            'iTotalDisplayRecords': self.count(),
            'sEcho': self._meta.echo,
            'aaData': self.map(mapitem),
            }
#########################################################
