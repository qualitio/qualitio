# -*- coding: utf-8 -*-
import hashlib
from operator import attrgetter, methodcaller
from pprint import pprint

from qualitio.chart.utils import identity, OrderedDict, comp, ImproperlyConfigured
from qualitio.require.models import Requirement
from qualitio.store.models import TestCase
from qualitio.execute.models import Bug, TestCaseRun, TestCaseRunStatus


class BarChartDict(OrderedDict):
    def xaxis(self):
        return self.keys()

    def yaxis_columns(self):
        return self.values()

    def __groupby(self, seq, keys=(), key=identity):
        values = OrderedDict([(g, []) for g in keys])
        for obj in seq:
            values[key(obj)].append(obj)
        return values

    def regroup(self, groupkeys=(), groupby=identity,
                group_name_transform=identity, group_transform=identity):

        names = []
        groups = []
        for alist in self.yaxis_columns():
            values = self.__groupby(alist, keys=groupkeys, key=groupby)
            names.append(map(group_name_transform, values.keys()))
            groups.append(map(group_transform, values.values()))

        return names, groups


class ChartData(object):
    title = None
    xaxismodel = None
    yaxismodel = None

    fields_order = ()

    filter_fields = None
    filter_table_fields = ()

    filter_exclude = ()
    filter_table_exclude = ()
    type = "Bar"  # the default one

    description = " -- no description -- "

    @classmethod
    def id(cls):
        return hashlib.sha1(cls.__name__).hexdigest()[:10]

    def __init__(self, xaxis=None, yaxis=None):
        self.xaxis = xaxis or self.xaxismodel.objects.all()
        self.yaxis = yaxis or self.yaxismodel.objects.all()

    def belongs(self, y, x):
        """
        Should return True or False if ``y`` belongs to ``x``.
        """
        raise NotImplementedError("Subclass should override this method.")

    def groups(self):
        xaxis = list(self.xaxis)
        yaxis = list(self.yaxis)
        result = BarChartDict()
        while xaxis:
            xitem = xaxis.pop(0)
            result[xitem] = []
            counter = 0
            while yaxis and counter < len(yaxis):
                yitem = yaxis[counter]
                if self.belongs(yitem, xitem):
                    yaxis.pop(counter)
                    result[xitem].append(yitem)
                else:
                    counter += 1
        return result

    def get_chart(self):
        raise NotImplementedError()

    @classmethod
    def filterable_axis_model(cls):
        return cls.xaxismodel

    @classmethod
    def filterable_axis(cls):
        if cls.filterable_axis_model() == cls.xaxismodel:
            return "xaxis"
        return "yaxis"


class ChartTypes(dict):
    def add(self, chart_type):
        self[chart_type.id()] = chart_type

    def get_class_path(self, key):
        klass = self.get(key)
        return '.'.join([klass.__module__, klass.__name__])


class number_of_bugs_related_to_testcases_chartdata(ChartData):
    """
    Defines Bug model to TestCaseRun model bar chartdata.
    The chart shows how many bugs are added to particular
    testcase.

    Usage:

    >>> chart = number_of_bugs_related_to_testcases_chartdata(
    >>>     xaxis=TestCase.objects.all(),
    >>>     yaxis=Bug.objects.all())
    >>>
    """
    title = "Number of bugs related to testcases"
    description = ""\
        "The chart shows how many bugs are issued for particular testcase.\n"\
        "Gives ability to filter testcase set.\n"

    xaxismodel = TestCase
    yaxismodel = Bug
    filter_table_fields = ["id", "path", "name"]

    def belongs(self, bug, tc):
        return tc.testcaserun_set.filter(bugs__in=[bug]).exists()


class number_of_testcaseruns_related_to_testcase_chartdata(ChartData):
    """
    Number of testcaseruns related to each testcase.
    Testcaseruns are grouped by "status".

    Usage:

    >>> chart = number_of_testcaseruns_for_testcase_chartdata(
    >>>     xaxis=TestCase.objects.all(),
    >>>     yaxis=Bug.objects.all(),
    >>>     statuses=TestCaseStatus.objects.filter(project__slug="meego"))
    >>> # REMEMBER ABOUT PROJECT IN STATUSES FILTER!
    >>>
    """
    title = "Number of testcaseruns related to testcase"
    xaxismodel = TestCase
    yaxismodel = TestCaseRun

    def __init__(self, *args, **kwargs):
        self.statuses = kwargs.pop('statuses', None) or TestCaseRunStatus.objects.all()
        super(number_of_testcaseruns_related_to_testcase_chartdata, self).__init__(*args, **kwargs)

    def belongs(self, tcr, tc):
        return tcr.origin_id == tc.id


class number_of_requirements_afected_by_bug_chartdata(ChartData):
    """
    """

    title = "Number of requirements related to bugs"
    xaxismodel = Bug
    yaxismodel = Requirement

    fields_order = ["id", "name"]
    filter_table_fields = ["id", "name", "alias"]

    def __init__(self, *args, **kwargs):
        self._testcaseruns = set(TestCaseRun.objects.filter(status__name="FAIL").values_list('id', 'origin__requirement__id'))
        super(number_of_requirements_afected_by_bug_chartdata, self).__init__(*args, **kwargs)

    def belongs(self, req, bug):
        return (bug.testcaserun_id, req.id) in self._testcaseruns


class coverage_of_requirements_by_testcases_chartdata(ChartData):
    title = "Coverage of requirements by testcases"
    xaxismodel = Requirement
    yaxismodel = TestCase

    def belongs(self, tc, req):
        return tc.requirement_id == req.id


class testcaserun_passrate_chartdata(ChartData):
    title = "Test cases passrate"
    xaxismodel = TestCaseRunStatus
    yaxismodel = TestCaseRun
    type = "Pie"

    def belongs(self, tcr, status):
        return tcr.status == status

    @classmethod
    def filterable_axis_model(cls):
        return cls.yaxismodel
