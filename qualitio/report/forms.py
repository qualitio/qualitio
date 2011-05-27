
from django.forms.models import inlineformset_factory

from django import forms

from qualitio import core
from qualitio.report import models


class ReportDirectoryForm(core.DirectoryModelForm):
    class Meta(core.DirectoryModelForm.Meta):
        model = models.ReportDirectory


class ReportForm(core.PathModelForm):

    class Meta(core.PathModelForm.Meta):
        model = models.Report
        fields = ("parent", "name", "template", "public", "link", "mime")
        widgets = { "template": forms.HiddenInput(),
                    "link": forms.TextInput(attrs={"readonly":"readonly"})}


class ContextElementForm(core.BaseModelForm):
    class Meta(core.BaseModelForm):
        fields = ("name", "query")


ContextElementFormset = inlineformset_factory(models.Report,
                                              models.ContextElement,
                                              extra=2,
                                              formset=core.BaseInlineFormSet,
                                              form=ContextElementForm)
