from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory

from qualitio import core
from qualitio.store import models


class TestCaseDirectoryForm(core.DirectoryModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestCaseDirectory


class TestCaseForm(core.PathModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestCase


class TestCaseStepForm(core.BaseModelForm):
    sequence = forms.IntegerField(widget=forms.HiddenInput)

    class Meta(core.BaseModelForm.Meta):
        model = models.TestCaseStep


TestCaseStepFormSet = inlineformset_factory(models.TestCase, models.TestCaseStep,
                                            formset=core.BaseInlineFormSet,
                                            form=TestCaseStepForm, extra=0, can_delete=True)
TestCaseStepFormSet.empty_form = property(TestCaseStepFormSet._get_empty_form)


# AttachmentFormSet = inlineformset_factory(models.TestCase, models.Attachment,
#                                           extra=1, can_delete=True)


TestCaseStatusFormSet = modelformset_factory(models.TestCaseStatus,
                                             formset=core.BaseModelFormSet,
                                             form=core.BaseModelForm,
                                             extra=1,
                                             can_delete=True)


class GlossaryWord(forms.Form):
    search = forms.CharField()

