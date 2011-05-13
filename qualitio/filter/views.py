from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ImproperlyConfigured

from qualitio.core.utils import success, failed, json_response
from qualitio import filter as filterapp
from qualitio.filter import tables


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

    actions = [
        filterapp.DeleteAction(app_label=model._meta.app_label),
        ]
    return render_to_response('filter/filter.html', {
            'table': table,
            'app_label': model._meta.app_label,
            'filter': generic_filter,
            'action_choice_form': filterapp.ActionChoiceForm(actions=actions),
            }, context_instance=RequestContext(request))

@json_response
def actions(request, app_label=None, action_name=None):
    allactions = filterapp.find_actions('qualitio.%s' % app_label)
    for action_class in allactions:
        action = action_class(app_label=app_label)
        if action.name == action_name:
            return action.execute(request)
    return failed(message="Wrong request")
