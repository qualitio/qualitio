from django.shortcuts import render_to_response
from django.template import RequestContext
import django_filters
import django_tables


def filter(request, model=None, exclude=('lft', 'rght', 'tree_id', 'level')):
    Model = model
    fields_to_exclude = exclude


    class ModelFilter(django_filters.FilterSet):
        class Meta:
            model = Model
            exclude = fields_to_exclude

        def __init__(self, *args, **kwargs):
            django_filters.FilterSet.__init__(self, *args, **kwargs)
            for f in self.filters.values():
                if issubclass(f.__class__, (django_filters.CharFilter,)):
                    f.lookup_type = 'icontains'


    class ModelTable(django_tables.ModelTable):
        class Meta:
            model = Model
            exclude = fields_to_exclude


    filterset = ModelFilter(request.GET or None)
    table = ModelTable(filterset.qs)
    return render_to_response('filter/filter.html',
                              {'filterset': filterset,
                               'table': table,
                               'app_label': Model._meta.app_label},
                              context_instance=RequestContext(request))
