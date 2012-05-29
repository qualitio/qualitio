# -*- coding: utf-8 -*-
from django import forms

from qualitio.core.forms import BaseModelForm
from qualitio.chart.models import ChartQuery
from qualitio.chart.types import get_engine


class ChartTypeChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.charttypes = get_engine().charttypes
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

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super(SaveChartQueryForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        queryset = ChartQuery.objects.filter(project=self.project, name=name)
        if self.instance.id:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise forms.ValidationError("There's already \"%s\" query in this project." % name)
        return name

    def save(self, *args, **kwargs):
        self.instance.type_class_name = get_engine().charttypes.get_class_path(
            self.cleaned_data['charttype']
        )
        return super(SaveChartQueryForm, self).save(*args, **kwargs)
