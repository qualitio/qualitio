from django.forms.models import inlineformset_factory
from django import forms

from qualitio import core
from qualitio.report import models
from qualitio.report.validators import report_query_validator


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

    def clean_query(self):
        query = self.cleaned_data['query']
        report_query_validator.clean(query)
        return query


BaseContextElementFormset = inlineformset_factory(models.Report,
                                              models.ContextElement,
                                              extra=2,
                                              formset=core.BaseInlineFormSet,
                                              form=ContextElementForm)


class ContextElementFormset(BaseContextElementFormset):
    def get_context(self):
        context = {}
        for cd in filter(lambda cd: 'name' in cd and 'query' in cd, self.cleaned_data):
            context[cd['name']] = cd['query']
        return context
