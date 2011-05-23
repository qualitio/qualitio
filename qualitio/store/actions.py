from django import forms

from qualitio.store.models import TestCase
from qualitio.require.models import Requirement
from qualitio.core.utils import success, failed
from qualitio.filter import actions


class RequirementChooseForm(actions.ActionForm):
    requirement = forms.ModelChoiceField(queryset=Requirement.objects.all())


class SetRequirement(actions.Action):
    label = 'Set requirement'
    model = TestCase
    form_class = RequirementChooseForm

    def run_action(self, data, queryset, form=None):
        queryset.update(requirement=form.cleaned_data.get('requirement'))


class Delete(actions.Action):
    label = 'Delete'
    model = TestCase

    def run_action(self, data, queryset, form=None):
        queryset.delete()
