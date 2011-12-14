# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView

from qualitio.chart import forms
from qualitio.filter import FilterView


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

    def before_get(self, request, *args, **kwargs):
        form = forms.ChartTypeChoiceForm({
            'chart': kwargs.get('chartid'),
        })

        if not form.is_valid():
            return HttpResponseRedirect("/project/%s/chart/" % project)

        self.model, _ = form.get_models()
        self.charttype = form.get_charttype()

        self.fields_order = self.charttype.fields_order or self.fields_order
        self.table_fields = self.charttype.filter_table_fields or self.table_fields
        self.table_exclude = self.charttype.filter_table_exclude or self.table_exclude
        self.filter_fields = self.charttype.filter_fields or self.filter_fields
        self.filter_exclude = self.charttype.filter_exclude or self.filter_exclude


class FilterXaxisModelView(ChartBuilderView):
    template = "chart/filter_xaxis.html"

    def get(self, request, project=None, chartid=None):
        return super(FilterXaxisModelView, self).get(
            request, project=project, chartid=chartid,
            previous_step_url="/project/%s/chart/" % project,
            xaxismodel=self.model.__name__.lower())


class ChartView(ChartBuilderView):
    template = "chart/view.html"

    def get(self, request, project=None, chartid=None):
        return super(ChartView, self).get(
            request, project=project, chartid=chartid,
            data=json.dumps(request.GET),
            xaxismodel=self.model.__name__.lower())


class ChartDataView(ChartBuilderView):
    def get(self, request, project=None, chartid=None):
        return super(ChartDataView, self).get(
            request, project=project, chartid=chartid,
            xaxismodel=self.model.__name__.lower())

    def get_response(self, request, context):
        chartdata = self.charttype(xaxis=context['page_obj'].object_list)
        chart = chartdata.get_chart()
        return HttpResponse(chart.render(), content_type='application/json; charset=UTF-8')
