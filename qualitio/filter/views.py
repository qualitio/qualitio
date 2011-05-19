from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured

from qualitio import filter as filterapp
from qualitio.filter import forms


def filter(request, model=None, exclude=('lft', 'rght', 'tree_id', 'level'),
           model_filter_class=None, model_table_class=None, fields_order=()):

    if not model and not model_filter_class:
        raise ImproperlyConfigured('"filter" view requires model or model_filter_class to be defined.')

    model = model or model_filter_class._meta.model
    model_table_class = model_table_class or filterapp.generate_model_table(model, exclude=exclude)
    model_filter_class = model_filter_class or filterapp.generate_model_filter(model=model, exclude=exclude)

    generic_filter = model_filter_class(request.GET)
    has_control_params, params = generic_filter.build_from_params()
    if has_control_params:
        return HttpResponseRedirect('%s?%s' % (request.path, params.urlencode()))

    onpage_form = forms.OnPageForm(request.GET)
    onpage = onpage_form.value()

    return render_to_response('filter/filter.html', {
            'model_table_class': model_table_class,
            'app_label': model._meta.app_label,
            'filter': generic_filter,
            'data': generic_filter.qs,
            'onpage': onpage,
            'onpage_form': onpage_form,
            }, context_instance=RequestContext(request))
