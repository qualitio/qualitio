# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms.widgets import Media, HiddenInput
from django.db.models import Q



class BaseFieldFilterForm(forms.Form):
    field_name = None

    def construct_Q(self):
        data = self.cleaned_data['q']
        if data:
            return Q(**{self.field_name: data})
        return Q()


class BaseTextFieldFilterForm(BaseFieldFilterForm):
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


class BaseDateRangeFieldFilterForm(BaseFieldFilterForm):
    from_date = forms.DateField(required=False)
    to_date = forms.DateField(required=False)

    def construct_Q(self):
        from_date = self.cleaned_data['from_date']
        to_date = self.cleaned_data['to_date']
        if from_date and to_date:
            return Q(**{'%s__%s' % (self.field_name, 'range'): [from_date, to_date]})
        return Q()


class RelatedObjectFilterForm(BaseFieldFilterForm):
    q = forms.NullBooleanField(required=False)

    related_object = None
    field_name = None
    field_name_label = None

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


# utils ######################################################
def _get_db_field(Model, field_or_field_name_):
    field = field_or_field_name_
    if isinstance(field_or_field_name_, basestring):
        field = Model._meta.get_field(field_or_field_name_)
    return field


def _camel_name(name):
    return ''.join([w.capitalize() for w in name.split('_')])


def _class_field_name(name):
    return '%s%s' % (_camel_name(name), 'FilterForm')


def _pretty_field_name(name):
    return ' '.join(name.split('_')).capitalize()
# end of utils ###############################################


def fieldfilter_factory(Model, field_or_field_name_,
                        bases=(BaseFieldFilterForm,), attrs=None):
    field = _get_db_field(Model, field_or_field_name_)
    if attrs is None:
        attrs = {
            'field_name': field.name,
            'field_name_label': _pretty_field_name(field.name),
            'q': field.formfield(required=False)
            }
    return type(_class_field_name(field.name), bases, attrs)


def text_fieldfilter(Model, field):
    field = _get_db_field(Model, field)
    if field.choices:
        return fieldfilter_factory(Model, field)
    return fieldfilter_factory(Model, field, bases=(BaseTextFieldFilterForm,))


def date_fieldfilter(Model, field):
    field = _get_db_field(Model, field)
    return fieldfilter_factory(Model, field, bases=(BaseDateRangeFieldFilterForm,), attrs={
            'field_name': field.name,
            'field_name_label': _pretty_field_name(field.name),
            })


FIELD_FORM_FOR_DBFIELD_DEFAULTS = {
    models.CharField: text_fieldfilter,
    models.TextField: text_fieldfilter,
    models.BooleanField: fieldfilter_factory,
    models.DateField: date_fieldfilter,
    models.DateTimeField: date_fieldfilter,
    models.TimeField: fieldfilter_factory,
    models.OneToOneField: fieldfilter_factory,
    models.ForeignKey: fieldfilter_factory,
    models.ManyToManyField: fieldfilter_factory,
    models.DecimalField: fieldfilter_factory,
    models.SmallIntegerField: fieldfilter_factory,
    models.IntegerField: fieldfilter_factory,
    models.PositiveIntegerField: fieldfilter_factory,
    models.PositiveSmallIntegerField: fieldfilter_factory,
    models.FloatField: text_fieldfilter,
    models.NullBooleanField: fieldfilter_factory,
    models.SlugField: fieldfilter_factory,
    models.EmailField: fieldfilter_factory,
    models.FilePathField: fieldfilter_factory,
    models.URLField: fieldfilter_factory,
    models.XMLField: fieldfilter_factory,
    models.IPAddressField: fieldfilter_factory,
    models.CommaSeparatedIntegerField: fieldfilter_factory,
    }


def generate_field_forms(Model, fields=None, exclude=(), fields_overrides=None):
    fields_map = dict(FIELD_FORM_FOR_DBFIELD_DEFAULTS)
    fields_map.update(fields_overrides or {})

    result = []
    for f in list(Model._meta.fields):
        if (fields and f.name not in fields) or (exclude and f.name in exclude):
            continue

        field_form = fields_map.get(f.__class__)
        if field_form:
            result.append(field_form(Model, f.name))

    return result
