# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, TemplateView

from qualitio.chart import forms
from qualitio.filter import FilterView
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


class ChartBuilderView(FilterView):
    fields_order = ['id', 'path', 'name']
    table_fields = ["id", "path", "name"]
    modelfilters = {
        TestCase: chartfilter.TestCaseFilter,
    }

    def get_filter_class(self):
        klass = self.modelfilters.get(self.model)
        if klass is None:
            return super(ChartBuilderView, self).get_filter_class()
        return klass

    def before_get(self, request, *args, **kwargs):
        form = forms.ChartTypeChoiceForm({
            'chart': kwargs.get('chartid'),
        })

        if not form.is_valid():
            return HttpResponseRedirect("/project/%s/chart/" % request.project)

        self.model, _ = form.get_models()
        self.charttype = form.get_charttype()

        self.fields_order = self.charttype.fields_order or self.fields_order
        self.table_fields = self.charttype.filter_table_fields or self.table_fields
        self.table_exclude = self.charttype.filter_table_exclude or self.table_exclude
        self.filter_fields = self.charttype.filter_fields or self.filter_fields
        self.filter_exclude = self.charttype.filter_exclude or self.filter_exclude


class FilterXaxisModelView(ChartBuilderView):
    template = "chart/filter_xaxis.html"
    js_handler = "FilterXAxisView"

    def get(self, request, project=None, chartid=None):
        return super(FilterXaxisModelView, self).get(request, extra_context={
            'project': project,
            'chartid': chartid,
            'previous_step_url': "/project/%s/chart/" % project,
            'xaxismodel': self.model.__name__.lower(),
            'js_handler': self.js_handler,
        })


class ChartView(ChartBuilderView):
    template = "chart/view.html"
    js_handler = "ChartView"

    def get(self, request, project=None, chartid=None):
        return super(ChartView, self).get(request, extra_context={
            'project': project,
            'chartid': chartid,
            'previous_step_url': "/project/%s/chart/" % project,
            'xaxismodel': self.model.__name__.lower(),
            'data': json.dumps(request.GET),
            'form': forms.SaveChartQueryForm(),
            'chart_engine': get_engine(),
            'chart_engine_js_include_template': get_engine().get_js_include_template(),
            'chart_engine_css_include_template': get_engine().get_css_include_template(),
            'js_handler': self.js_handler,
        })


class BaseSavedChartQueryView(FilterView):
    def before_get(self, request, *args, **kwargs):
        self.chart_query = get_object_or_404(ChartQuery, id=kwargs.get('id'))
        self.charttype = self.chart_query.get_type_class()()  # construct the object
        self.model = self.charttype.xaxismodel

        self.fields_order = self.charttype.fields_order or self.fields_order
        self.table_fields = self.charttype.filter_table_fields or self.table_fields
        self.table_exclude = self.charttype.filter_table_exclude or self.table_exclude
        self.filter_fields = self.charttype.filter_fields or self.filter_fields
        self.filter_exclude = self.charttype.filter_exclude or self.filter_exclude


class SavedChartView(BaseSavedChartQueryView):
    template = "chart/view.html"
    js_handler = "SavedChartView"

    def get(self, request, project=None, id=None):
        return super(SavedChartView, self).get(request, extra_context={
            'project': project,
            'data': json.dumps(request.GET),
            'chartid': self.charttype.id(),
            'xaxismodel': self.model.__name__.lower(),
            'form': forms.SaveChartQueryForm(instance=self.chart_query),
            'chart_query_id': id,
            'chart_engine': get_engine(),
            'chart_engine_js_include_template': get_engine().get_js_include_template(),
            'chart_engine_css_include_template': get_engine().get_css_include_template(),
            'saved_chart_view': True,
            'js_handler': self.js_handler,
        })


class SavedChartFilterView(BaseSavedChartQueryView, ChartBuilderView):
    template = "chart/filter_xaxis.html"
    js_handler = "SavedChartFilterView"

    def get(self, request, project=None, id=None):
        return super(SavedChartFilterView, self).get(request, extra_context={
            'project': project,
            'chart_query_id': id,
            'chartid': self.charttype.id(),
            'xaxismodel': self.model.__name__.lower(),
            'js_handler': self.js_handler,
        })


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
    def get(self, request, project=None, chartid=None):
        return super(ChartDataView, self).get(request, extra_context={
            'project': project,
            'chartid': chartid,
            'xaxismodel': self.model.__name__.lower(),
        })

    def get_response(self, request, context):
        chartdata = self.charttype(xaxis=context['page_obj'].object_list)
        chart = chartdata.get_chart()
        return HttpResponse(chart.render(), content_type='application/json; charset=UTF-8')
