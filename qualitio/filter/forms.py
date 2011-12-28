# -*- coding: utf-8 -*-
from django import forms


class OnPageForm(forms.Form):
    DEFAULT = 15
    onpage = forms.ChoiceField(choices=(
            (15, '15 on page'),
            (30, '30 on page'),
            (50, '50 on page'),
            (100, '100 on page'),
            (200, '200 on page'),
            (500, '500 on page'),
            ('all', 'all'),
            ), required=False, label=u'On page')

    def value(self):
        self.is_valid()
        value = getattr(self, 'cleaned_data', {}).get('onpage') or OnPageForm.DEFAULT
        try:
            return int(value)
        except ValueError:
            if value in ('all',):
                return value
            raise
