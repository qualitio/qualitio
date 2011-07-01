from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from qualitio.core.utils import json_response, failed
from qualitio import filter as filterapp
from qualitio.filter import forms


def filter(request, model=None, exclude=('lft', 'rght', 'tree_id', 'level'),
           model_filter_class=None, model_table_class=None, fields_order=(),
           app_menu_items=()):

    if not model and not model_filter_class:
        raise ImproperlyConfigured('"filter" view requires model or model_filter_class to be defined.')

    model = model or model_filter_class._meta.model
    model_table_class = model_table_class or filterapp.generate_model_table(
        model, exclude=exclude, fields_order=fields_order)
    model_filter_class = model_filter_class or filterapp.generate_model_filter(model=model, exclude=exclude)

    generic_filter = model_filter_class(request.GET)
    has_control_params, params = generic_filter.build_from_params()
    if has_control_params:
        return HttpResponseRedirect('%s?%s' % (request.path, params.urlencode()))

    onpage_form = forms.OnPageForm(request.GET)
    onpage = onpage_form.value()

    # 1) We DO NOT use django-pagination 'request.page' feature since
    #    it doesn't work as expected
    # 2) We DO NOT use 'autopaginate' tag since it can raise 404 on wrong page number
    #    and it causes 500.
    page = 1
    try:
        page = int(request.REQUEST['page'])
    except (KeyError, ValueError, TypeError):
        pass

    paginator = Paginator(generic_filter.qs, onpage)
    page_obj = None
    try:
        page_obj = paginator.page(page)
    except (EmptyPage, InvalidPage):
        raise Http404

    # actions
    action_classes = filterapp.find_actions('qualitio.%s' % model._meta.app_label, model=model)
    actions = [ActionClass(None) for ActionClass in action_classes]

    return render_to_response('filter/filter.html', {
            'app_label': model._meta.app_label,
            'app_menu_items': app_menu_items,
            'filter': generic_filter,
            'table': model_table_class(page_obj.object_list, query_dict=request.GET),
            'paginator': paginator,
            'page_obj': page_obj,
            'onpage_form': onpage_form,
            'action_choice_form': filterapp.ActionChoiceForm(actions=actions),
            }, context_instance=RequestContext(request))

@json_response
def actions(request, app_label=None, action_name=None):
    allactions = filterapp.find_actions('qualitio.%s' % app_label)
    for action_class in allactions:
        action = action_class(data=request.POST)
        if action.name == action_name:
            return action.execute()
    return failed(message="Wrong request")
