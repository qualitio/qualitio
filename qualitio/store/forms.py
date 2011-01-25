from mptt.forms import MoveNodeForm
from django import forms
from django.forms.models import inlineformset_factory

from qualitio.core.forms import PathModelForm
from qualitio.store import models

class TestCaseDirectoryForm(PathModelForm):
    class Meta(PathModelForm.Meta):
        model = models.TestCaseDirectory


class TestCaseForm(PathModelForm):
    class Meta(PathModelForm.Meta):
        model = models.TestCase
        # fields = ("parent", "name", "requirement", "description", "precondition")

class TestCaseStepForm(forms.ModelForm):
    sequence = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = models.TestCaseStep

TestCaseStepFormSet = inlineformset_factory(models.TestCase, models.TestCaseStep, 
                                            form=TestCaseStepForm, extra=0, can_delete=True)
TestCaseStepFormSet.empty_form = property(TestCaseStepFormSet._get_empty_form)
AttachmentFormSet = inlineformset_factory(models.TestCase, models.Attachment, 
                                          extra=1, can_delete=True)

class GlossaryWord(forms.Form):
    search = forms.CharField()
