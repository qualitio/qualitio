from django.forms.models import inlineformset_factory
from django import forms

from qualitio import core
from qualitio.report import models
from qualitio.report import validators


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
    """
    ContextElementForm has special behaviour.
    If query string is valid it is evaluated
    and stored in cleaned_data 'evaluated_query' key.
    """
    class Meta(core.BaseModelForm):
        fields = ("name", "query")

    def clean_query(self):
        query = self.cleaned_data['query']
        self.cleaned_data['evaluated_query'] = validators.clean_query_string(query)
        return query


BaseContextElementFormset = inlineformset_factory(models.Report,
                                              models.ContextElement,
                                              extra=2,
                                              formset=core.BaseInlineFormSet,
                                              form=ContextElementForm)


class ContextElementFormset(BaseContextElementFormset):
    def context_queries(self):
        context = {}
        for cd in filter(lambda cd: 'name' in cd and 'evaluated_query' in cd, self.cleaned_data):
            context[cd['name']] = cd['evaluated_query']
        return context
