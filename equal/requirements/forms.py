from django import forms
from equal.requirements.models import Requirement

class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ("name","parent","release_target","description")
        widgets = {'release_target': forms.DateInput(attrs={'class':'date-field'})}
