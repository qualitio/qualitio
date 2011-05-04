from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms

import django_tables

from qualitio import filter as filterapp


def filter(request, model=None, exclude=('lft', 'rght', 'tree_id', 'level')):
    Model = model
    fields_to_exclude = exclude

    class ModelTable(django_tables.ModelTable):
        class Meta:
            model = Model
            exclude = fields_to_exclude

    class ModelFilter(filterapp.ModelFilter):
        class Meta:
            model = Model
            exclude = fields_to_exclude
            related_objects = False

    generic_filter = ModelFilter(request.GET)
    has_control_params, params = generic_filter.build_from_params()
    if has_control_params:
        return HttpResponseRedirect('%s?%s' % (request.path, params.urlencode()))

    table = ModelTable(generic_filter.qs)
    return render_to_response('filter/filter.html',
                              {'table': table,
                               'app_label': Model._meta.app_label,
                               'filter': generic_filter,
                               },
                              context_instance=RequestContext(request))
