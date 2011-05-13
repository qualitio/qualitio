# -*- coding: utf-8 -*-
import re
import inspect
from operator import itemgetter

from django.utils import importlib
from django import forms

from qualitio.core.utils import success, failed
from qualitio.core.forms import BaseForm


class Action(object):
    item_id_ptr = re.compile(r'^item-(?P<id>\d+)$')
    model = None
    form_class = None
    name = 'action'
    label = 'Action'
    app_label = None

    def __init__(self, data=None, app_label=None):
        self.data = data
        self.app_label = app_label

    def has_form(self):
        return self.form_class

    def form(self):
        return self.form_class() if self.form_class else ''

    def url(self):
        return '/filter/action/execute/%s/%s/' % (self.app_label, self.name)

    def queryset(self):
        result = []
        for key in self.data.keys():
            match = self.item_id_ptr.match(key)
            if match:
                result.append(int(match.group('id')))
        return self.model.objects.filter(id__in=result)

    def execute(self, request):
        print "Action!"
        return success(message='Action validation OK')


def find_actions(app_label, module_name='actions'):
    actionmodule = importlib.import_module('%s.%s' % (app_label, module_name))
    without_names = map(itemgetter(1), inspect.getmembers(actionmodule))
    classes = filter(inspect.isclass, without_names)
    return filter(lambda class_: issubclass(class_, Action), classes)


class TestForm(forms.Form):
    name = forms.CharField(required=False)


class DeleteAction(Action):
    name = 'delete'
    label = 'Delete'


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

