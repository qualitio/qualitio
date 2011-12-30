# -*- coding: utf-8 -*-
from operator import attrgetter, methodcaller
import pyofc2 as ofc

from qualitio.chart.utils import comp
from qualitio.chart.types import base


def get_js_include_template():
    return "chart/types/open_flash_chart.html"


def get_css_include_template():
    return None


charttypes = base.ChartTypes()


class OFCBase(base.ChartData):
    def get_chart(self):
        series = self.groups()
        chart = ofc.open_flash_chart()
        chart.title = ofc.title(text=self.title)
        chart.x_axis = ofc.x_axis(
            labels=ofc.x_axis_labels(
                labels=map(attrgetter('name'), series.xaxis()),
                rotate="45"))
        return self.build_chart(series, chart)

    def build_chart(self, series, chart):
        raise NotImplementedError()


class number_of_bugs_related_to_testcases_chartdata(
        OFCBase,
        base.number_of_bugs_related_to_testcases_chartdata):

    def build_chart(self, series, chart):
        chart.add_element(ofc.bar(
                values=[comp(len, methodcaller('values'), dict, map)(
                        lambda bug: (bug.alias, bug), col) for col in series.yaxis_columns()],
                colour='#56acde'))
        return chart
charttypes.add(number_of_bugs_related_to_testcases_chartdata)


class number_of_testcaseruns_related_to_testcase_chartdata(
        OFCBase,
        base.number_of_testcaseruns_related_to_testcase_chartdata):

    def build_chart(self, series, chart):
        statuses = sorted(self.statuses, key=attrgetter('name'))
        colours = map(attrgetter('color'), statuses)

        names, values_groups = series.regroup(
            groupkeys=map(attrgetter('name'), statuses),
            groupby=attrgetter('status.name'),
            group_transform=len)

        chart.add_element(ofc.bar_stack(
                values=values_groups,
                colours=colours,
                tip="#x_label#"))
        chart.y_axis = ofc.y_axis(max=comp(max, map)(sum, values_groups) + 2)

        return chart
charttypes.add(number_of_testcaseruns_related_to_testcase_chartdata)


class number_of_requirements_afected_by_bug_chartdata(
        OFCBase,
        base.number_of_requirements_afected_by_bug_chartdata):

    def build_chart(self, series, chart):
        values = map(len, series.yaxis_columns())
        chart.add_element(ofc.bar(
                values=values,
                colour='#56acde',
                tip="#x_label# [#val#]"))
        chart.y_axis = ofc.y_axis(max=max(values) + 2)
        return chart
# TODO: this feature doesn't make sense since every bug bind is separate instance.
# charttypes.add(number_of_requirements_afected_by_bug_chartdata)


class coverage_of_requirements_by_testcases_chartdata(
        OFCBase,
        base.coverage_of_requirements_by_testcases_chartdata):

    def build_chart(self, series, chart):
        values = map(len, series.yaxis_columns())
        chart.add_element(ofc.bar(
                values=values,
                colour='#56acde',
                tip="#x_label# [#val#]"))
        chart.y_axis = ofc.y_axis(max=max(values) + 2)
        return chart
charttypes.add(coverage_of_requirements_by_testcases_chartdata)
