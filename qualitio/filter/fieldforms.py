# -*- coding: utf-8 -*-
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


class DateRangeFieldFilterForm(FieldFilterForm):
    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)

    def construct_Q(self):
        from_date = self.cleaned_data['from_date']
        to_date = self.cleaned_data['to_date']
        if from_date and to_date:
            return Q(**{'%s__%s' % (self.field_name, 'range'): [from_date, to_date]})
        return Q()


class RelatedObjectFilterForm(FieldFilterForm):
    q = forms.NullBooleanField(required=False)

    # need to be set up by subclass of FieldFilter
    related_object = None

    def construct_Q(self):
        ro = self.related_object
        value = self.cleaned_data['q']
        qs = Q()

        if value == True:
            other_model_qs = ro.model.objects.filter(**{'%s__isnull' % ro.field.name: False})
            ids_of_current_model = other_model_qs.values_list('%s__id' % ro.field.name, flat=True)
            ids_of_current_model = list(set(ids_of_current_model))
            qs = Q(id__in=ids_of_current_model)
        elif value == False:
            qs = Q(**{'%s__isnull' % ro.var_name: True})

        return qs
