from mptt.forms import MoveNodeForm

from django import forms
from django.forms.models import inlineformset_factory

from qualitio.store.models import TestCaseDirectory, TestCase, TestCaseStep, Attachment


class TestCaseDirectoryForm(forms.ModelForm):
    class Meta:
        model = TestCaseDirectory
        fields = ("parent", "name")


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ("parent", "name", "requirement", "description", "precondition")

class TestCaseStepForm(forms.ModelForm):
    sequence = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model = TestCaseStep

TestCaseStepFormSet = inlineformset_factory(TestCase, TestCaseStep, form=TestCaseStepForm, extra=0, can_delete=True)
TestCaseStepFormSet.empty_form = property(TestCaseStepFormSet._get_empty_form)
AttachmentFormSet = inlineformset_factory(TestCase, Attachment, extra=1, can_delete=True)

class GlossaryWord(forms.Form):
    search = forms.CharField()
