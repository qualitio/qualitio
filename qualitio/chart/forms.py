# -*- coding: utf-8 -*-
from django import forms

from qualitio.chart.models import charttypes


class ChartTypeChoiceForm(forms.Form):
    chart = forms.ChoiceField(choices=map(lambda x: (x.id(), x.title), charttypes.values()))

    def get_models(self):
        chart = self.get_charttype()
        return chart.xaxismodel, chart.yaxismodel

    def get_charttype(self):
        return charttypes[self.cleaned_data['chart']]
