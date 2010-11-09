from mptt.forms import MoveNodeForm

from django import forms
from django.forms.models import inlineformset_factory

from equal.store.models import TestCaseDirectory, TestCase, TestCaseStep, Attachment


class TestCaseDirectoryForm(forms.ModelForm):
    class Meta:
        model = TestCaseDirectory


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase


TestCaseStepFormSet = inlineformset_factory(TestCase, TestCaseStep, extra=1)
AttachmentFormSet = inlineformset_factory(TestCase, Attachment, extra=1)

class GlossaryWord(forms.Form):
    search = forms.CharField()
