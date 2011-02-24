from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

import django_tables

from qualitio.filter.fields import *
from qualitio.filter.filter import Filter


def filter(request, model=None, exclude=('lft', 'rght', 'tree_id', 'level')):
    Model = model
    fields_to_exclude = exclude

    class ModelTable(django_tables.ModelTable):
        class Meta:
            model = Model
            exclude = fields_to_exclude

    form_classes = generate_field_forms(Model, exclude=fields_to_exclude)

    generic_filter = Filter(request.GET, form_classes=form_classes)
    has_control_params, params = generic_filter.build_from_params()
    if has_control_params:
        return HttpResponseRedirect('%s?%s' % (request.path, params.urlencode()))

    query = Q() if not generic_filter.is_valid() else generic_filter.construct_Q()
    table = ModelTable(Model.objects.filter(query))

    return render_to_response('filter/filter.html',
                              {'table': table,
                               'app_label': Model._meta.app_label,
                               'filter': generic_filter,
                               },
                              context_instance=RequestContext(request))
