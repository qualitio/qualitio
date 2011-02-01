from django import forms

from qualitio import core
from qualitio.execute import models


class TestRunDirectoryForm(core.PathModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestRunDirectory


class TestRunForm(core.PathModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestRun


class TestCaseRunStatus(forms.ModelForm):

    class Meta:
        model = models.TestCaseRun
        fields = ("status",)
        widgets = {
            'status': forms.RadioSelect(renderer=core.RawRadioSelectRenderer)
            }

    def __init__(self, *args, **kwargs):
        super(TestCaseRunStatus, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = None
