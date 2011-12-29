# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import View, TemplateView

from qualitio.chart import forms
from qualitio import filter as filterapp
from qualitio.core.utils import json_response, failed, success
from qualitio.chart.models import ChartQuery
from qualitio.chart.types import get_engine
from qualitio.store.models import TestCase
from qualitio.chart import filter as chartfilter


class NewChartView(TemplateView):
    template_name='chart/new.html'

    def get_context_data(self, **kw):
        context = super(NewChartView, self).get_context_data(**kw)
        context.update({
            'form': forms.ChartTypeChoiceForm(),
        })
        return context


class FilterView(filterapp.FilterView):
    """
    Base FilterView. Gives ability to customize ModelFilter classes.
    """
    modelfilters = {
        TestCase: chartfilter.TestCaseFilter,
    }

    def get_filter_class(self):
        klass = self.modelfilters.get(self.model)
        if klass is None:
            return super(FilterView, self).get_filter_class()
        return klass


class ChartBuilderView(FilterView):
    """
    Base view for all charts views. Gives ability to customize
    source of "model" and "charttype" attributes.
    """
    fields_order = ['id', 'path', 'name']
    table_fields = ["id", "path", "name"]
    configurable_options = [
        "fields_order", "table_fields", "table_exclude",
        "filter_fields", "filter_exclude",
    ]
    js_handler = None

    def get_context_data(self, request, **kwargs):
        context = super(ChartBuilderView, self).get_context_data(request, **kwargs)
        context.update({
            'engine': get_engine(),
            'project': request.project,
            'filterable_axis_model': self.charttype.filterable_axis_model().__name__.lower(),
            'chartid': self.charttype.id(),
            'js_handler': self.js_handler,
            'js_plot_handler': "%sChart" % self.charttype.type,
        })
        return context

    def fetch_charttype(self, request, *args, **kwargs):
        """
        Fetching charttype from the request and params.
        Usage:

        >>> redirect, charttype = self.fetch_charttype(....)
        >>> if redirect:        # there was a problem with charttype
        >>>    return redirect
        >>> # overwhise you can use charttype
        """
        if 'chartid' not in kwargs:
            raise Http404("This action requires 'chartid' params.")

        form = forms.ChartTypeChoiceForm({
            'chart': kwargs.get('chartid'),
        })

        if not form.is_valid():
            return HttpResponseRedirect("/project/%s/chart/" % request.project), None

        return None, form.get_charttype()

    def configure_options(self, charttype):
        for opt in self.configurable_options:
            setattr(self, opt, getattr(charttype, opt, None) or getattr(self, opt, None))
        self.charttype = charttype
        self.model = charttype.filterable_axis_model()

    def before_get(self, request, *args, **kwargs):
        redirect, charttype = self.fetch_charttype(request, *args, **kwargs)
        if redirect:
            return redirect
        self.configure_options(charttype)


class FilterXaxisModelView(ChartBuilderView):
    template = "chart/filter_xaxis.html"
    js_handler = "FilterXAxisView"


class ChartView(ChartBuilderView):
    template = "chart/view.html"
    js_handler = "ChartView"

    def get(self, request, **kwargs):
        return super(ChartView, self).get(request, extra_context={
            'data': json.dumps(request.GET),
            'form': forms.SaveChartQueryForm(),
        })


class BaseSavedChartQueryView(ChartBuilderView):
    def fetch_charttype(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            raise Http404("This actions requires 'id' param")

        self.chart_query = get_object_or_404(ChartQuery, id=kwargs.get('id'))
        return None, self.chart_query.get_type_class()()

    def get_context_data(self, request, **kwargs):
        context = super(BaseSavedChartQueryView, self).get_context_data(request, **kwargs)
        context.update({
            'chart_query_id': self.chart_query.id,
        })
        return context


class SavedChartView(BaseSavedChartQueryView):
    template = "chart/view.html"
    js_handler = "SavedChartView"

    def get(self, request, **kwargs):
        return super(SavedChartView, self).get(request, extra_context={
            'data': json.dumps(request.GET),
            'form': forms.SaveChartQueryForm(instance=self.chart_query),
        })


class SavedChartFilterView(BaseSavedChartQueryView):
    template = "chart/filter_xaxis.html"
    js_handler = "SavedChartFilterView"


class SaveChartView(View):
    @json_response
    def post(self, request, project=None, id=None):
        instance = ChartQuery() if not id else get_object_or_404(ChartQuery, id=id)
        form = forms.SaveChartQueryForm(request.POST, instance=instance, project=request.project)
        if form.is_valid():
            chart_query = form.save()
            return success(
                message="Query saved!",
                data={
                    'id': chart_query.id,
                    'query': chart_query.query,
                })

        return failed(
            message="Validation errors: %s" % form.error_message(),
            data=form.errors_list())


class DeleteChartQueryView(View):
    @json_response
    def post(self, request, project=None, id=None):
        instance = ChartQuery() if not id else get_object_or_404(ChartQuery, id=id)
        instance.delete()
        return success(message="Query deleted!")


class ChartDataView(ChartBuilderView):
    def get_response(self, request, context):
        chartdata = self.charttype(**{
            self.charttype.filterable_axis(): context['page_obj'].object_list
        })
        chart = chartdata.get_chart()
        return HttpResponse(chart.render(), content_type='application/json; charset=UTF-8')
