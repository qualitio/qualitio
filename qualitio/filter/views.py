from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured

from qualitio import filter as filterapp
from qualitio.filter import actions, tables


def filter(request, model=None, exclude=('lft', 'rght', 'tree_id', 'level'),
           model_filter_class=None):

    if not model and not model_filter_class:
        raise ImproperlyConfigured('"filter" view requires model or model_filter_class to be defined.')
    model = model or model_filter_class._meta.model

    ModelTable = tables.generate_model_table(model, exclude=exclude)

    if not model_filter_class:
        model_filter_class = filterapp.generate_model_filter(model=Model, exclude=exclude)

    generic_filter = model_filter_class(request.GET)
    has_control_params, params = generic_filter.build_from_params()
    if has_control_params:
        return HttpResponseRedirect('%s?%s' % (request.path, params.urlencode()))

    table = ModelTable(generic_filter.qs, query_dict=request.GET)
    return render_to_response('filter/filter.html', {
            'table': table,
            'app_label': model._meta.app_label,
            'filter': generic_filter,
            'actions': []
            }, context_instance=RequestContext(request))
