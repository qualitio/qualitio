import datetime

from django import forms

from qualitio.store.models import TestCase
from qualitio.require.models import Requirement
from qualitio.core.utils import success, failed
from qualitio.filter import actions


class ChangeParent(actions.ChangeParent):
    model = TestCase


class RequirementChooseForm(actions.ActionForm):
    requirement = forms.ModelChoiceField(queryset=Requirement.objects.all())


class SetRequirement(actions.Action):
    label = 'Set requirement'
    model = TestCase
    form_class = RequirementChooseForm

    def run_action(self, data, queryset, form=None):
        from django.db import transaction

        try:
            with transaction.commit_on_success():
                for obj in queryset.all():
                    obj.requirement = form.cleaned_data.get('requirement')
                    obj.modified_time = datetime.datetime.now()
                    obj.save()
        except Exception, error:
            return failed(message='"%s" fail: %s' % (obj.name, error.message))

        return self.success(message='Action complete!')
