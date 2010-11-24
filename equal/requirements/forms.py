from django import forms

from equal.requirements.models import Requirement

class RequirementForm(forms.ModelForm):

    class Meta:
        model = Requirement


