# -*- coding: utf-8 -*-
import re
import inspect
import datetime
from operator import itemgetter

from django.utils import importlib
from django import forms

from qualitio.core.utils import success, failed
from qualitio.core.forms import BaseForm


class ActionForm(BaseForm):
    pass


class Action(object):
    # regex pattern to recognize QueryDict keys
    # In this way we know the IDs of object we want action run on
    item_id_ptr = re.compile(r'^item-(?P<id>\d+)$')

    # model is required to fetch data from db, Look at 'queryset' method
    model = None

    # non-obligatory option - you add form if the action needs it
    form_class = None

    app_label = None

    # name property it's just the '<class_name>.lower()'.
    # It is generated for you, but you can always change it.
    def _get_name(self):
        if not hasattr(self, '_name'):
            self._name = self.__class__.__name__.lower()
        return self._name

    def _set_name(self, name):
        self._name = name

    name = property(_get_name, _set_name)

    # the label that is displayed
    label = 'Action'

    def __init__(self, data=None, app_label=None):
        self.data = data
        self.app_label = app_label

    def has_form(self):
        return self.form_class

    def form(self):
        return self.form_class(self.data or None) if self.form_class else ''

    def url(self):
        return '/filter/action/execute/%s/%s/' % (self.app_label, self.name)

    def queryset(self):
        result = []
        for key in self.data.keys():
            match = self.item_id_ptr.match(key)
            if match:
                result.append(int(match.group('id')))
        return self.model.objects.filter(id__in=result)

    def execute(self):
        form = None
        if self.has_form():
            if self.data:
                form = self.form_class(self.data)
                if not form.is_valid():
                    return failed(
                        message=form.error_message(),
                        data=form.errors_list())
        return self.run_action(self.data, self.queryset(), form)

    def run_action(self, data, queryset, form=None):
        return success(message='Action complete!')


def find_actions(app_label, module_name='actions'):
    actionmodule = importlib.import_module('%s.%s' % (app_label, module_name))
    without_names = map(itemgetter(1), inspect.getmembers(actionmodule))
    classes = filter(inspect.isclass, without_names)
    return filter(lambda class_: issubclass(class_, Action), classes)


class ActionChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        empty_value = '---------'
        choices = [('', empty_value)]
        self.actions = kwargs.pop('actions', [])

        for a in self.actions:
            choices.append((a.name, a.label))

        self.base_fields['action'] = forms.TypedChoiceField(
            choices=choices, required=False, empty_value=empty_value)

        super(ActionChoiceForm, self).__init__(*args, **kwargs)


# COMMON ACTIONS
class ChangeParent(Action):
    label = 'Change parent'

    def _get_form_class(self):
        if not hasattr(self, '_form_class'):
            self._form_class = self._form_for_model()
        return self._form_class

    def _set_form_class(self, form_class):
        self._form_class = form_class

    form_class = property(_get_form_class, _set_form_class)

    def _form_for_model(self):
        model = self.model._meta.get_field('parent').rel.to
        class ParentForm(ActionForm):
            parent = forms.ModelChoiceField(queryset=model.objects.all())
        return ParentForm

    def run_action(self, data, queryset, form=None):
        for obj in queryset.all():
            obj.parent = form.cleaned_data.get('parent')
            obj.modified_time = datetime.datetime.now()
            obj.save()
        return success(message='Action complete!')
