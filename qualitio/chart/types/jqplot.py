# -*- coding: utf-8 -*-
from operator import attrgetter, methodcaller

from django.utils import simplejson as json

from qualitio.chart.utils import comp
from qualitio.chart.types import base
from qualitio.store.models import TestCase
from qualitio.execute.models import Bug


def get_js_include_template():
    return "chart/types/jqplot_js.html"


def get_css_include_template():
    return "chart/types/jqplot_css.html"


charttypes = base.ChartTypes()


class Chart(object):
    def __init__(self, data=None, options=None):
        self.data = data or {}
        self.options = options or {}

    def render(self):
        return json.dumps({
            'data': self.data,
            'options': self.options,
        })


class JQPlotBase(base.ChartData):
    def format_xaxis_label(self, obj):
        return obj.name[:37] + "..." if len(obj.name) > 40 else obj.name


class number_of_testcaseruns_related_to_testcase_chartdata(
        JQPlotBase,
        base.number_of_testcaseruns_related_to_testcase_chartdata):

    def get_chart(self):
        series = self.groups()
        statuses = sorted(self.statuses, key=attrgetter('name'))
        colours = map(attrgetter('color'), statuses)

        names, values_groups = series.regroup(
            groupkeys=map(attrgetter('name'), statuses),
            groupby=attrgetter('status.name'),
            group_transform=len)

        return Chart(
            data=zip(*values_groups),
            options={
                'title': self.title,
                'stackBar': True,
                'xaxisNames': map(self.format_xaxis_label, series.xaxis()),
                'yaxismax': comp(max, map)(sum, values_groups) + 2,
                'legendLabels': map(attrgetter('name'), statuses),
            })
charttypes.add(number_of_testcaseruns_related_to_testcase_chartdata)


class number_of_bugs_related_to_testcases_chartdata(
        JQPlotBase,
        base.number_of_bugs_related_to_testcases_chartdata):

    def get_chart(self):
        series = self.groups()
        get_values = comp(len, methodcaller('values'), dict, map)
        values = [
             get_values(lambda bug: (bug.alias, bug), col)
             for col in series.yaxis_columns()
        ]
        return Chart(
            data=[values],
            options={
                'title': self.title,
                'stackBar': False,
                'xaxisNames': map(self.format_xaxis_label, series.xaxis()),
                'yaxismax': max(values) + 2,
                'legendLabels': ['Number of bugs'],
            })
charttypes.add(number_of_bugs_related_to_testcases_chartdata)



class number_of_requirements_afected_by_bug_chartdata(
        JQPlotBase,
        base.number_of_requirements_afected_by_bug_chartdata):

    def get_chart(self):
        series = self.groups()
        values = map(len, series.yaxis_columns())
        return Chart(
            data=[values],
            options={
                'title': self.title,
                'stackBar': False,
                'xaxisNames': map(self.format_xaxis_label, series.xaxis()),
                'yaxismax': max(values) + 2,
                'legendLabels': ['Number of requirements'],
            })
charttypes.add(number_of_requirements_afected_by_bug_chartdata)



class coverage_of_requirements_by_testcases_chartdata(
        JQPlotBase,
        base.coverage_of_requirements_by_testcases_chartdata):

    def get_chart(self):
        series = self.groups()
        values = map(len, series.yaxis_columns())
        return Chart(
            data=[values],
            options={
                'title': self.title,
                'stackBar': False,
                'xaxisNames': map(self.format_xaxis_label, series.xaxis()),
                'yaxismax': max(values) + 2,
                'legendLabels': ['Number of testcases'],
            })
charttypes.add(coverage_of_requirements_by_testcases_chartdata)



class testcaserun_passrate_chartdata(
        JQPlotBase,
        base.testcaserun_passrate_chartdata):

    def get_chart(self):
        series = self.groups()
        values = map(len, series.yaxis_columns())
        return Chart(
            data=[values],
            options={
                'title': self.title,
                'stackBar': False,
                'xaxisNames': map(self.format_xaxis_label, series.xaxis()),
                'yaxismax': max(values) + 2,
                'legendLabels': ['Number of testcaseruns'],
            })
charttypes.add(testcaserun_passrate_chartdata)
