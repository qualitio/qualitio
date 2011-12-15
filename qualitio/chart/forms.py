# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.importlib import import_module

from qualitio.core.forms import BaseModelForm
from qualitio.chart.models import ChartQuery

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


class SaveChartQueryForm(BaseModelForm):
    class Meta:
        model = ChartQuery
        exclude = ('project', 'type_class_name')
        widgets = {
            'query': forms.HiddenInput,
        }

    charttype = forms.CharField(widget=forms.HiddenInput)

    def save(self, *args, **kwargs):
        self.instance.type_class_name = engine.charttypes.get_class_path(
            self.cleaned_data['charttype']
        )
        return super(SaveChartQueryForm, self).save(*args, **kwargs)
