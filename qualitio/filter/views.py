from django.shortcuts import render_to_response
from django.template import RequestContext

import django_tables

from qualitio.filter.filterset import ModelFilterSet


def filter(request, model=None, exclude=('lft', 'rght', 'tree_id', 'level')):
    Model = model
    fields_to_exclude = exclude


    class ModelFilter(ModelFilterSet):
        class Meta:
            model = Model
            exclude = fields_to_exclude


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
