from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from qualitio.report.models import Report, Query, ReportDirectory

class ReportForm(ModelForm):
    class Meta:
        model = Report

QueryFormSet = inlineformset_factory(Report, Query, extra=2)

class ReportDirectoryForm(ModelForm):
    class Meta:
        model = ReportDirectory

