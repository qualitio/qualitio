# -*- coding: utf-8 -*-
from operator import attrgetter

from django import forms

from qualitio.require.models import Requirement
from qualitio.store.models import TestCase
from qualitio.execute.models import TestCaseRun, Bug
from qualitio.chart.models import charttypes

avaiable_models = (
    ("requirements", "requirements"),
    ("testcases", "testcases"),
    ("testcaseruns", "testcase runs"),
    ("bugs", "bugs"),
    )

models = {
    "requirements": Requirement,
    "testcases": TestCase,
    "testcaseruns": TestCaseRun,
    "bugs": Bug,
    }

class ChartModelChoiceForm(forms.Form):
    xaxis = forms.ChoiceField(choices=avaiable_models)
    yaxis = forms.ChoiceField(choices=avaiable_models)

    def get_models(self):
        cd = self.cleaned_data
        return models[cd['xaxis']], models[cd['yaxis']]


class ChartTypeChoiceForm(forms.Form):
    chart = forms.ChoiceField(choices=map(lambda x: (x.id(), x.title), charttypes.values()))

    def get_models(self):
        chart = self.get_charttype()
        return chart.xaxismodel, chart.yaxismodel

    def get_charttype(self):
        return charttypes[self.cleaned_data['chart']]
