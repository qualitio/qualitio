# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django import forms
from django.db.models import Q

from qualitio.filter import utils


class FieldFilterForm(forms.Form):
    """
    Basic field filter interface.
    To use it properly you need to define query
    in 'construct_Q' method. This query will be
    pass to the 'queryset.filter' method.

    It need to have two class variables:
    - ``field_name`` : models field name that the filter will work at,
    - ``field_name_label`` : template label for the field.

    DON'T setup the variables your self! It will
    be setup by FieldFilter subclass that will use
    this field form.
    """
    field_name = None
    field_name_label = None

    def construct_Q(self):
        return Q()


class AutoQueryFieldFilterForm(FieldFilterForm):
    """
    Field filter form that will have query field auto-generated
    by FieldFilter subclass.
    """
    auto_query_field = True

    def construct_Q(self):
        data = self.cleaned_data['q']
        if data:
            return Q(**{self.field_name: data})
        return Q()


class TextFieldFilterForm(AutoQueryFieldFilterForm):
    lookup = forms.ChoiceField(choices=[
            ('contains', 'contains'),
            ('icontains', 'icontains'),
            ('startswith', 'startswith'),
            ('istartswith', 'istartswith'),
            ('exact', 'exact'),
            ('iexact', 'iexact'),
            # ... and so on ...
            ], required=False)

    def construct_Q(self):
        lookup = self.cleaned_data['lookup']
        data = self.cleaned_data['q']
        if lookup and data:
            return Q(**{'%s__%s' % (self.field_name, lookup): data})
        return Q()


def to_datetime(date, hour=0, minute=0, second=0):
    if not date:
        return date
    return datetime(date.year, date.month, date.day, hour, minute, second)


class DateFieldFilterForm(FieldFilterForm):
    date = forms.DateField(required=False)

    def construct_Q(self):
        date = self.cleaned_data['date']
        if date:
            return Q(**{self.field_name: date})
        return Q()


class DateTimeFieldFilterForm(FieldFilterForm):
    date = forms.DateField(required=False)

    def construct_Q(self):
        date = to_datetime(self.cleaned_data['date'])
        to_date = to_datetime(date, 23, 59, 59)
        if date:
            return Q(**{'%s__%s' % (self.field_name, 'range'): [date, to_date]})
        return Q()


class DateRangeFieldFilterForm(FieldFilterForm):
    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)

    def construct_Q(self):
        from_date = self.cleaned_data['from_date']
        to_date = self.cleaned_data['to_date']
        if from_date and to_date:
            return Q(**{'%s__%s' % (self.field_name, 'range'): [from_date, to_date]})
        return Q()


class DateTimeRangeFieldFilterForm(DateRangeFieldFilterForm):
    def construct_Q(self):
        from_date = to_datetime(self.cleaned_data['from_date'])
        to_date = to_datetime(self.cleaned_data['to_date'] or from_date, 23, 59, 59)
        if from_date and to_date:
            return Q(**{'%s__%s' % (self.field_name, 'range'): [from_date, to_date]})
        return Q()
