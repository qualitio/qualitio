from django import forms
from django.forms.models import inlineformset_factory, BaseModelFormSet, modelformset_factory

from qualitio import core
from qualitio import store
from qualitio.execute import models


class TestRunDirectoryForm(core.PathModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestRunDirectory


class TestRunForm(core.PathModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestRun


class TestCaseRunStatus(core.BaseModelForm):

    class Meta:
        model = models.TestCaseRun
        fields = ("status",)
        widgets = {
            'status': forms.RadioSelect(renderer=core.RawRadioSelectRenderer)
            }

    def __init__(self, *args, **kwargs):
        super(TestCaseRunStatus, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = None


class AddBugForm(forms.ModelForm):
    class Meta:
        fields = ("id",)
        model = models.Bug




class BaseAvailableTestCases(BaseModelFormSet):
    def add_fields(self, form, index):
        super(BaseAvailableTestCases, self).add_fields(form, index)
        form.fields["action"] = forms.BooleanField(required=False)


AvailableTestCases = modelformset_factory(store.TestCase,
                                          formset=BaseAvailableTestCases,
                                          fields=("id", "action"),
                                          extra=0)

ConnectedTestCases = inlineformset_factory(models.TestRun,
                                           models.TestCaseRun,
                                           fields=("id",),
                                           extra=0)

# BugsFormSet = modelformset_factory(models.Bug)

