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


_ContextElementFormset = inlineformset_factory(models.Report,
                                              models.ContextElement,
                                              extra=2,
                                              formset=core.BaseInlineFormSet,
                                              form=ContextElementForm)


class ContextElementFormset(_ContextElementFormset):
    def get_context(self):
        context = {}
        for cd in filter(lambda cd: 'name' in cd and 'query' in cd, self.cleaned_data):
            context[cd['name']] = cd['query']
        return context

    def save(self, *args, **kwargs):
        queries = kwargs.pop('queries', {})

        # Before proccesing, make sure it won't commit changes unless
        # we add query result (commit=False ensures that model's save method
        # won't be called)
        kwargs.update(commit=False)

        instances = super(ContextElementFormset, self).save(*args, **kwargs)
        for instance in instances:
            instance.save(query_result=queries.get(instance.name))
        return instances
