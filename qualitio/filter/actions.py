# -*- coding: utf-8 -*-
import re
import inspect
import datetime
from operator import itemgetter

from django.utils import importlib
from django import forms

from mptt.models import MPTTModel

from qualitio.core.utils import success, failed
from qualitio.core.forms import BaseForm
from qualitio.filter.utils import Property
from qualitio import history


class ActionForm(BaseForm):
    pass


class Action(object):
    """
    Base Action class. Provides the action flow.
    Action execution basically works this way:

    * the execute() method is invoked:
       1) it checks if there is something in queryset
          (queryset with items that user selected)
       2) it checks if form is valid (if your action has a form)
       3) invokes run_action() method

    * run_action() method should use core util responses:
      success() and failed() methods are included to
      do it really easy. Both accepts 'message' and 'data' kwargs.
      eg:
         # ...
         return self.succes(message='Somethings went wrong', data={
             'error1': 'error message'
         })
    """

    # regex pattern to recognize QueryDict keys
    # In this way we know the IDs of object we want action run on
    item_id_ptr = re.compile(r'^item-(?P<id>\d+)$')

    app_label = Property(target='_app_label', default=lambda self: self.model._meta.app_label)
    name = Property(target='_name', default=lambda self: self.__class__.__name__.lower())

    # the label that is displayed
    label = 'Action'

    # model is required to fetch data from db, Look at 'queryset' method
    model = None

    # non-obligatory option - you add form if the action needs it
    form_class = None

    def __init__(self, data=None, request=None):
        self.data = data
        self.request = request

    def has_form(self):
        return self.form_class

    def form(self):
        return self.form_class(self.data or None) if self.form_class else ''

    def url(self):
        return '/filter/action/execute/%s/%s/' % (self.app_label, self.name)

    def success(self, *args, **kwargs):
        return success(*args, **kwargs)

    def failed(self, *args, **kwargs):
        return failed(*args, **kwargs)

    def queryset(self):
        result = []
        for key in self.data.keys():
            match = self.item_id_ptr.match(key)
            if match:
                result.append(int(match.group('id')))
        return self.model.objects.filter(id__in=result)

    def validate_form(self):
        form = None
        if self.has_form() and self.data is not None:
            form = self.form_class(self.data)
            if not form.is_valid():
                return False, form
        return True, form

    def validate_queryset(self):
        queryset = self.queryset()
        if not queryset.exists():
            return False, queryset
        return True, queryset

    def run_action(self, data, queryset, form=None):
        return self.success(message='Action complete!')

    def execute(self):
        queryset_is_valid, queryset = self.validate_queryset()
        if not queryset_is_valid:
            return failed(message='Check items you want run throught the action')

        form_is_valid, form = self.validate_form()
        if not form_is_valid:
            return failed(message=form.error_message(), data=form.errors_list())

        return self.run_action(self.data, queryset, form)


def find_actions(app_label, module_name='actions', model=None):
    actionmodule = importlib.import_module('%s.%s' % (app_label, module_name))
    without_names = map(itemgetter(1), inspect.getmembers(actionmodule))
    classes = filter(inspect.isclass, without_names)
    classes = filter(lambda class_: issubclass(class_, Action), classes)
    if model is not None:
        classes = filter(lambda class_: hasattr(class_, 'model') and class_.model == model, classes)
    return classes


class ActionChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        empty_value = ' -- Choose action -- '
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

    def _form_for_model(self):
        model = self.model._meta.get_field('parent').rel.to
        class ParentForm(ActionForm):
            parent = forms.ModelChoiceField(queryset=model.objects.all())
        return ParentForm

    form_class = Property(target='_form_class', default=_form_for_model)

    def run_action(self, data, queryset, form=None):
        from django.db import transaction

        try:
            with transaction.commit_on_success():
                for obj in queryset.all():
                    # NOTE: chaging parent require some extra work by mptt lib so
                    #       we can not just set: obj.parent = form.cleaned_data.get('parent').
                    #       But ofcourse not every model derives from MPTTModel.
                    if issubclass(obj.__class__, MPTTModel):
                        obj.move_to(form.cleaned_data.get('parent'))
                    else:
                        obj.parent = form.cleaned_data.get('parent')

                    obj.modified_time = datetime.datetime.now()
                    obj.save()

                    log = history.History(self.request.user, obj)
                    log.add_message(u"Changed parent")
                    log.save()

        except Exception, error:
            reason = u'; '.join(map(unicode, getattr(error, 'messages', [])))
            if not reason:
                reason = u'%s' % unicode(error)
            return self.failed(message='"%s" fail: %s' % (obj.name, reason))

        return self.success(message='Action complete!')
