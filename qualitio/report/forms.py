
from django.forms.models import inlineformset_factory
from django import forms

from qualitio import core
from qualitio.report import models


class ReportDirectoryForm(core.DirectoryModelForm):
    class Meta(core.DirectoryModelForm.Meta):
        model = models.ReportDirectory


class ReportForm(core.PathModelForm):
    public = forms.BooleanField(required=False)
    class Meta(core.PathModelForm.Meta):
        model = models.Report
        fields = ("parent", "name", "template")
        widgets = { 'template': forms.HiddenInput() }


class ContextElementForm(core.BaseModelForm):
    class Meta(core.BaseModelForm):
        fields = ("name", "query")



ContextElementFormset = inlineformset_factory(models.Report,
                                              models.ContextElement,
                                              extra=1,
                                              formset=core.BaseInlineFormSet,
                                              form=ContextElementForm)
