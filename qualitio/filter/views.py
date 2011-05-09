from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django import forms
from django.core.exceptions import ImproperlyConfigured

import django_tables

from qualitio import filter as filterapp


def filter(request, model=None, exclude=('lft', 'rght', 'tree_id', 'level'),
           model_filter_class=None):

    if not model and not model_filter_class:
        raise ImproperlyConfigured('"filter" view requires model or model_filter_class to be defined.')

    Model = model or model_filter_class._meta.model
    fields_to_exclude = exclude

    class ModelTable(django_tables.ModelTable):
        class Meta:
            model = Model
            exclude = fields_to_exclude

    if not model_filter_class:
        model_filter_class = filterapp.generate_model_filter(model=Model, exclude=exclude)

    generic_filter = model_filter_class(request.GET)
    has_control_params, params = generic_filter.build_from_params()
    if has_control_params:
        return HttpResponseRedirect('%s?%s' % (request.path, params.urlencode()))

    table = ModelTable(generic_filter.qs)
    return render_to_response('filter/filter.html', {
            'table': table,
            'app_label': Model._meta.app_label,
            'filter': generic_filter,
            }, context_instance=RequestContext(request))
