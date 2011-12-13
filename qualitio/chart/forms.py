# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.importlib import import_module


engine = import_module(getattr(settings, 'CHART_TYPES_ENGINE'))


class ChartTypeChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.charttypes = engine.charttypes
        self.base_fields['chart'] = forms.ChoiceField(
            choices=map(lambda x: (x.id(), x.title), self.charttypes.values()))
        super(ChartTypeChoiceForm, self).__init__(*args, **kwargs)

    def get_models(self):
        chart = self.get_charttype()
        return chart.xaxismodel, chart.yaxismodel

    def get_charttype(self):
        return self.charttypes[self.cleaned_data['chart']]
