# -*- coding: utf-8 -*-
from django import forms

import django_filters


class RelatedObjectFilter(django_filters.BooleanFilter):
    def __init__(self, related_object=None, *args, **kwargs):
        super(RelatedObjectFilter, self).__init__(*args, **kwargs)
        self.related_object = related_object

    def filter(self, qs, value):
        ro = self.related_object

        if value == True:
            other_model_qs = ro.model.objects.filter(**{'%s__isnull' % ro.field.name: False})
            ids_of_current_model = other_model_qs.values_list('%s__id' % ro.field.name, flat=True)
            ids_of_current_model = list(set(ids_of_current_model))
            qs = qs.filter(id__in=ids_of_current_model)
        elif value == False:
            qs = qs.filter(**{'%s__isnull' % ro.var_name: True})

        return qs
