from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory

from qualitio import core
from qualitio import store
from qualitio.execute import models


class TestRunDirectoryForm(core.DirectoryModelForm):
    class Meta(core.DirectoryModelForm.Meta):
        model = models.TestRunDirectory


class TestRunForm(core.PathModelForm):
    class Meta(core.PathModelForm.Meta):
        model = models.TestRun
        fields = ("parent", "name")


class TestCaseRunStatus(core.BaseModelForm):

    class Meta:
        model = models.TestCaseRun
        fields = ("status",)
        widgets = {
            'status': forms.RadioSelect(renderer=core.RawRadioSelectRenderer)
            }

    def __init__(self, *args, **kwargs):
        super(TestCaseRunStatus, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = None

    def changelog(self):
        return "%s %s. Status changed: %s" % (self.instance._meta.verbose_name.capitalize(),
                                              self.instance.pk,
                                              self.instance.status)

class AddBugForm(core.BaseForm):
    bugs = forms.CharField()

    def clean_bugs(self):
        return map(lambda x: x.strip(",").strip("#").strip(" "),
                   self.cleaned_data['bugs'].split(","))


class BugForm(core.BaseModelForm):
    class Meta:
        model = models.Bug
        widgets = {'alias': forms.HiddenInput()}

    def __init__(self, *args,**kwargs):
        super(BugForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget = forms.HiddenInput()


BugFormSet = inlineformset_factory(models.TestCaseRun,
                                   models.Bug,
                                   extra=0,
                                   formset=core.BaseInlineFormSet,
                                   form=BugForm)


