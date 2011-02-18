from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory

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


class AddBugForm(core.BaseForm):
    bugs = forms.CharField()

    def clean_bugs(self):
        return map(lambda x: x.strip(",").strip("#"),
                   self.cleaned_data['bugs'].split())


class BugForm(core.BaseModelForm):
    class Meta:
        model = models.Bug
        widgets = {'alias': forms.HiddenInput()}

    def __init__(self, *args,**kwargs):
        super(BugForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget = forms.HiddenInput()

BugFormSet = inlineformset_factory(models.TestCaseRun,
                                   models.Bug,
                                   extra=0,
                                   formset=core.BaseInlineFormSet,
                                   form=BugForm)


class BaseAvailableTestCases(core.BaseModelFormSet):
    def add_fields(self, form, index):
        super(BaseAvailableTestCases, self).add_fields(form, index)
        form.fields["action"] = forms.BooleanField(required=False)


AvailableTestCases = modelformset_factory(store.TestCase,
                                          formset=BaseAvailableTestCases,
                                          fields=("id", "action"),
                                          extra=0)


ConnectedTestCases = inlineformset_factory(models.TestRun,
                                           models.TestCaseRun,
                                           formset=core.BaseInlineFormSet,
                                           fields=("id",),
                                           extra=0)
