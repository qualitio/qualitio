from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from qualitio import actions as actionsapp
from qualitio.filter import forms
from qualitio.filter.filter import generate_model_filter
from qualitio.filter.tables import generate_model_table


class FilterView(object):
    model = None
    model_filter_class = None
    model_table_class = None

    exclude = ()
    fields_order = ()

    template = 'filter/filter.html'

    def __init__(self, **kwargs):
        for fname in ['model', 'model_filter_class', 'exclude',
                      'fields_order', 'template', 'model_table_class']:
            setattr(self, fname, kwargs.pop(fname, None) or getattr(self.__class__, fname))

    def _assere_requirements(self):
        if not self.model and not self.model_filter_class:
            raise ImproperlyConfigured('"filter" view requires model or model_filter_class to be defined.')

    def get_model(self):
        return self.model or self.model_filter_class._meta.model

    def get_app_label(self):
        return self.get_model()._meta.app_label

    def get_filter_class(self):
        return self.model_filter_class or generate_model_filter(
            model=self.get_model(),
            exclude=self.exclude)

    def get_filter(self, *args, **kwargs):
        return self.get_filter_class()(*args, **kwargs)

    def build_filter(self, data):
        return self.get_filter(data, build=True)

    def get_table_class(self):
        return self.model_table_class or generate_model_table(
            self.get_model(),
            exclude=self.exclude,
            fields_order=self.fields_order)

    def get_page_number(self, request):
        # 1) We DO NOT use django-pagination 'request.page' feature since
        #    it doesn't work as expected
        # 2) We DO NOT use 'autopaginate' tag since it can raise 404 on wrong page number
        #    and it causes 500.
        try:
            return int(request.REQUEST['page'])
        except (KeyError, ValueError, TypeError):
            return 1

    def paginate_queryset(self, queryset, page_number, onpage):
        paginator = Paginator(queryset, onpage)
        try:
            return paginator, paginator.page(page_number)
        except (EmptyPage, InvalidPage):
            raise Http404

    def get_context_data(self, request, **kwargs):
        context = {}
        context.update(kwargs)
        return context

    def get_actions(self, request):
        module_name = 'qualitio.%s' % self.get_app_label()
        return actionsapp.create_actions(request, module_name, model=self.get_model())

    def handle_request(self, request, *args, **kwargs):
        self._assere_requirements()  # may raise ImproperlyConfigured

        # create filter and redirect if there are control forms
        filter_object = self.build_filter(request.GET)
        if filter_object.has_control_params:
            return HttpResponseRedirect('%s?%s' % (request.path, filter_object.data.urlencode()))

        # pagination stuff
        onpage_form = forms.OnPageForm(request.GET)
        paginator, page = self.paginate_queryset(
            queryset=filter_object.queryset(),
            page_number=self.get_page_number(request),
            onpage=onpage_form.value())

        actions = self.get_actions(request)
        model_table_class = self.get_table_class()

        context = self.get_context_data(request, **{
                'app_label': self.get_app_label(),
                'filter': filter_object,
                'table': model_table_class(page.object_list, query_dict=request.GET, request=request),
                'paginator': paginator,
                'page_obj': page,
                'onpage_form': onpage_form,
                'action_choice_form': actionsapp.ActionChoiceForm(actions=actions),
                })
        context.update(kwargs)
        return self.get_response(request, context)

    def get_response(self, request, context):
        return render_to_response(self.template, context, context_instance=RequestContext(request))

    def __call__(self, *args, **kwargs):
        return self.handle_request(*args, **kwargs)
