# -*- coding: utf-8 -*-
from django import forms

from qualitio import core
from qualitio.filter.models import FilterQuery


class OnPageForm(forms.Form):
    onpage = forms.ChoiceField(choices=(
            (15, '15 on page'),
            (30, '30 on page'),
            (50, '50 on page'),
            (100, '100 on page'),
            ), required=False, label=u'On page')

    def value(self):
        self.is_valid()
        return int(getattr(self, 'cleaned_data', {}).get('onpage') or 15)


class FilterQueryForm(core.BaseModelForm):
    class Meta:
        model = FilterQuery
        fields = ["name", "query"]
        widgets = {
            "query": forms.HiddenInput
            }

    def clean_query(self):
        # sort keys before saving them
        return '&'.join(sorted(self.cleaned_data['query'].split('&')))

    def save_if_valid(self, *args, **kwargs):
        if self.is_valid():
            return self.save(*args, **kwargs) is not None
        return False
