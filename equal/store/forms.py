from mptt.forms import MoveNodeForm

from django import forms
from django.forms.models import inlineformset_factory

from equal.store.models import TestCaseDirectory, TestCase, TestCaseStep, Attachment


class TestCaseDirectoryForm(forms.ModelForm):
    class Meta:
        model = TestCaseDirectory
        fields = ("parent", "name")


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ("parent", "name", "requirement", "description", "precondition")


TestCaseStepFormSet = inlineformset_factory(TestCase, TestCaseStep, extra=0)
AttachmentFormSet = inlineformset_factory(TestCase, Attachment, extra=1, can_delete=True)

class GlossaryWord(forms.Form):
    search = forms.CharField()
