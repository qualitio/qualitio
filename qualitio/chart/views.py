# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseRedirect

from qualitio.chart import forms
from qualitio.filter import FilterView


def index(request, project=None):
    return render_to_response('chart/choose_chart_type.html', {
            'form': forms.ChartTypeChoiceForm(),
            }, context_instance=RequestContext(request))


class ChartBuilderView(FilterView):
    fields_order = ['id', 'path', 'name']
    table_fields = ["id", "path", "name"]

    def __call__(self, *args, **kwargs):
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

        return self.handle_request(*args, **kwargs)


class FilterXaxisModelView(ChartBuilderView):
    template = "chart/filter_x_axis.html"

    def handle_request(self, request, project=None, chartid=None):
        return super(FilterXaxisModelView, self).handle_request(
            request, project=project, chartid=chartid,
            previous_step_url="/project/%s/chart/" % project,
            xaxismodel=self.model.__name__.lower())


class ChartView(ChartBuilderView):
    template = "chart/chartview.html"

    def handle_request(self, request, project=None, chartid=None):
        previous_step_url = '/project/%(project)s/chart/%(chartid)s/?%(params)s' % {
            'project': project,
            'params': request.GET.urlencode(),
            'chartid': chartid,
            }
        return super(ChartView, self).handle_request(
            request, project=project, chartid=chartid,
            previous_step_url=previous_step_url,
            data=json.dumps(request.GET),
            xaxismodel=self.model.__name__.lower())


class ChartDataView(ChartBuilderView):
    def handle_request(self, request, project=None, chartid=None):
        return super(ChartDataView, self).handle_request(
            request, project=project, chartid=chartid,
            xaxismodel=self.model.__name__.lower())

    def get_response(self, request, context):
        chartdata = self.charttype(xaxis=context['page_obj'].object_list)
        chart = chartdata.get_chart()
        return HttpResponse(chart.render(), content_type='application/json; charset=UTF-8')
