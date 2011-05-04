import re

from django.db import models
from django.db.models import Q
from django import forms
from django.utils.datastructures import SortedDict
from qualitio.filter.options import MetaFilter

class BaseControlForm(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        form_classes = kwargs.pop('form_classes', [])
        self.form_classes = form_classes or self.__class__.form_classes
        super(BaseControlForm, self).__init__(*args, **kwargs)


class SelectControlForm(BaseControlForm):
    control_field_name = None

    def __init__(self, *args, **kwargs):
        self.control_field_name = kwargs.pop('control_field_name', self.__class__.control_field_name)
        field = forms.ChoiceField(choices=kwargs.pop('choices', ()))
        self.base_fields[self.control_field_name] = field
        field.widget.attrs['class'] = 'control-select'
        field.label = ''
        super(SelectControlForm, self).__init__(*args, **kwargs)

    def get_form_class(self):
        if not self.is_valid():
            return None
        index = self.cleaned_data[self.control_field_name]
        return self.form_classes[int(index)]


class AddFieldFilterForm(SelectControlForm):
    control_field_name = 'add_field_filter'


class AddFieldGroupForm(SelectControlForm):
    control_field_name = 'add_group'


class FilterGroup(object):
    form_classes = []

    def __init__(self, group_id, data=None, form_classes=()):
        self.id = group_id
        self.forms = SortedDict()
        self.data = data
        self.form_classes = form_classes or self.__class__.form_classes

    def add_form(self, form_class, initial=None):
        return self.build_form(self.form_classes.index(form_class), self._get_next_id(form_class), initial=initial)

    def build_form(self, form_class_id, form_id, initial=None):
        form_class = self.form_classes[form_class_id]
        form_for_class = self.forms.get(form_class, SortedDict())
        if form_id not in form_for_class:
            form = form_class(data=self.data, initial=initial, prefix=self.get_prefix(form_class, form_id))
            form_for_class[form_id] = form
            self.forms[form_class] = form_for_class
        return self.forms[form_class][form_id]

    def _get_next_id(self, form_class):
        if form_class not in self.forms:
            self.forms[form_class] = SortedDict()
        return len(self.forms[form_class]) + 1

    def get_prefix(self, form_class=None, form_id=None):
        form_id = form_id or self._get_next_id(form_class)
        return '%s-%s-%s' % (self.id, self.form_classes.index(form_class), form_id)

    def get_control_new_criteria(self):
        return '%s-%s-%s' % (self.id, 'control', 'new-criteria')

    def _get_add_field_filter_form_choices(self):
        return [('', 'add new field filter')] + [(i, f.field_name) for i, f in enumerate(self.form_classes)]

    def get_new_criteria_form(self, data=None):
        return AddFieldFilterForm(
            data=data,
            choices=self._get_add_field_filter_form_choices(),
            form_classes=self.form_classes,
            prefix=self.get_control_new_criteria())

    def _iter_forms(self):
        for form_class, form_for_class in self.forms.items():
            for form in form_for_class.values():
                yield form

    def is_valid(self):
        return all(f.is_valid() for f in self._iter_forms())

    def __iter__(self):
        for form in self._iter_forms():
            yield form
        yield self.get_new_criteria_form()

    def construct_Q(self):
        query = Q()
        for form in self._iter_forms():
            query = query & form.construct_Q()
        return query


class Filter(object):
    field_name_ptr = re.compile(r'(?P<group_id>\d+)-(?P<form_class_id>\d+)-(?P<form_id>\d+)-(?P<field_name>\w+)')
    control_form_ptr = re.compile(r'(\d+)-control-new-criteria-(\w+)')
    control_group_ptr = re.compile(r'control-new-group-(\w+)')

    def get_form_classes(self):
        return getattr(self.__class__, 'form_classes', ())

    def __init__(self, data=None, form_classes=()):
        self.data = data
        self.groups = SortedDict()
        self.form_classes = form_classes or self.get_form_classes()
        self.has_control_params = False

    def add_group(self, group_id=None):
        group_id = group_id or (len(self.groups) + 1)
        new_group = FilterGroup(group_id, data=self.data, form_classes=self.form_classes)
        self.groups[group_id] = new_group
        return new_group

    def build_from_params(self):
        copy = self.data.copy()
        data = self.data.copy()

        # first build existing groups...
        for fname in data.keys():
            match = self.field_name_ptr.match(fname)
            if match:
                group_id = int(match.group('group_id'))
                group = self.groups.get(group_id) or self.add_group(group_id)
                group.build_form(int(match.group('form_class_id')), int(match.group('form_id')))
                del data[fname]

        # then create all new field filters in all groups
        for fname in data.keys():
            match = self.control_form_ptr.match(fname)
            if match:
                group = self.groups.get(int(match.group(1))) or self.add_group()
                criteria_form = group.get_new_criteria_form(data=self.data)
                self._process_criteria_form(criteria_form, group, copy, data, fname)

        # in the end try to add new groups
        for fname in data.keys():
            match = self.control_group_ptr.match(fname)
            if match:
                group = self.add_group()
                criteria_form = self.get_new_group_form(data=self.data)
                self._process_criteria_form(criteria_form, group, copy, data, fname)

        self.data = copy
        return self.has_control_params, self.data

    def _add_empty_params(self, form, params):
        for name in form.base_fields:
            params[form.add_prefix(name)] = ''
        return form

    def _process_criteria_form(self, criteria_form, group, params_copy, params_data, fname):
        form_class = criteria_form.get_form_class()
        if form_class:
            self._add_empty_params(group.add_form(form_class, {'q': ''}), params_copy)

        self.has_control_params = True
        del params_copy[fname]
        del params_data[fname]

    def has_groups(self):
        return bool(self.groups)

    def get_control_new_group(self):
        return '%s-%s' % ('control', 'new-group')

    def _get_add_group_form_choices(self):
        return [('', 'add group')] + [(i, f.field_name) for i, f in enumerate(self.form_classes)]

    def get_new_group_form(self, data=None):
        return AddFieldGroupForm(
            data=data,
            choices=self._get_add_group_form_choices(),
            form_classes=self.form_classes,
            prefix=self.get_control_new_group())
    new_group_form = property(get_new_group_form)

    def __iter__(self):
        return iter(self.groups.values())

    def is_valid(self):
        return all(g.is_valid() for g in self)

    def construct_Q(self):
        query = Q()
        for group in self:
            query = query | group.construct_Q()
        return query


class ModelFilter(Filter):
    __metaclass__ = MetaFilter

    def get_form_classes(self):
        return [f.create_form_class() for f in self.base_filters.values()]

    def queryset(self):
        query = Q() if not self.is_valid() else self.construct_Q()
        return self._meta.model.objects.filter(query)

    qs = property(lambda self: self.queryset())


def generate_form_classes(model, fields=None, exclude=(), bases=(ModelFilter,)):
    _model, _fields, _exclude = model, fields, exclude

    class Meta:
        model = _model
        fields = _fields
        exclude = _exclude

    _Filter = type('_Filter', bases, { 'Meta': Meta })
    return [f.create_form_class() for f in _Filter.base_filters.values()]
