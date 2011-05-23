# -*- coding: utf-8 -*-
from django import forms


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
