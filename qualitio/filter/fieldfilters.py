# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured
from django import forms


from qualitio.filter import utils, fieldforms


class FieldFilter(utils.ObjectCounter):
    """
    Field class that is acctually a factory for field form creation.
    It can generate 'q' form field automatically if 'auto_query_field' option
    on 'form_class' is set to True.
    """
    form_class = fieldforms.FieldFilterForm

    def __init__(self, form_class=None, label=None, name=None, model=None, field=None,
                 field_name=None):
        self.form_class = form_class or self.__class__.form_class
        self.label = label
        self.field_name = field_name

        # those variables below are filled by metaclass:
        self.name = name
        self.model = model
        self.field = field

    def form_class_attrs(self):
        attrs = {
            'field_name': self.field_name or self.name,
            'field_name_label': self.label or utils.pretty_field_name(self.name),
            }

        if getattr(self.form_class, 'auto_query_field', False):
            attrs['q'] = self.field.formfield(required=False)

        return attrs

    def create_form_class(self):
        bases = (self.form_class,)
        attrs = self.form_class_attrs()
        return type(utils.class_field_name(self.name, 'FilterForm'), bases, attrs)


class AutoQueryFieldFilter(FieldFilter):
    form_class = fieldforms.AutoQueryFieldFilterForm


class TextFieldFilter(FieldFilter):
    form_class = fieldforms.TextFieldFilterForm


class DateFieldFilter(FieldFilter):
    form_class = fieldforms.DateFieldFilterForm


class DateTimeFieldFilter(FieldFilter):
    form_class = fieldforms.DateTimeFieldFilterForm


class DateRangeFieldFilter(FieldFilter):
    form_class = fieldforms.DateRangeFieldFilterForm


class DateTimeRangeFieldFilter(FieldFilter):
    form_class = fieldforms.DateTimeRangeFieldFilterForm


FIELD_FORM_FOR_DBFIELD_DEFAULTS = {
    models.CharField: TextFieldFilter,
    models.TextField: TextFieldFilter,
    models.BooleanField: AutoQueryFieldFilter,
    models.DateField: DateFieldFilter,
    models.DateTimeField: DateTimeFieldFilter,
    models.TimeField: AutoQueryFieldFilter,
    models.OneToOneField: AutoQueryFieldFilter,
    models.ForeignKey: AutoQueryFieldFilter,
    models.ManyToManyField: AutoQueryFieldFilter,
    models.DecimalField: AutoQueryFieldFilter,
    models.SmallIntegerField: AutoQueryFieldFilter,
    models.IntegerField: AutoQueryFieldFilter,
    models.PositiveIntegerField: AutoQueryFieldFilter,
    models.PositiveSmallIntegerField: AutoQueryFieldFilter,
    models.FloatField: AutoQueryFieldFilter,
    models.NullBooleanField: AutoQueryFieldFilter,
    models.SlugField: AutoQueryFieldFilter,
    models.EmailField: AutoQueryFieldFilter,
    models.FilePathField: AutoQueryFieldFilter,
    models.URLField: AutoQueryFieldFilter,
    models.XMLField: AutoQueryFieldFilter,
    models.IPAddressField: AutoQueryFieldFilter,
    models.CommaSeparatedIntegerField: AutoQueryFieldFilter,
    }


def fieldfilters_for_model(Model, fields=None, exclude=(), fields_overrides=None):
    fields_map = dict(FIELD_FORM_FOR_DBFIELD_DEFAULTS)
    fields_map.update(fields_overrides or {})

    result = {}
    for f in list(Model._meta.fields):
        if (fields and f.name not in fields) or (exclude and f.name in exclude):
            continue

        fieldfilter_class = fields_map.get(f.__class__)
        if fieldfilter_class:
            result[f.name] = fieldfilter_class(model=Model, name=f.name, field=f)

        # TODO: this is just little hack here, we need to change it somehow
        #       in the future. We'll simply add additional fields for date-type
        #       fields.

        if f.__class__ == models.DateField:
            field_name = '%s_range' % f.name
            result[field_name] = DateRangeFieldFilter(model=Model, field_name=f.name, field=f)

        if f.__class__ == models.DateTimeField:
            field_name = '%s_range' % f.name
            result[field_name] = DateTimeRangeFieldFilter(model=Model, field_name=f.name, field=f)

    return result
