from django import forms
from equal.requirements.models import Requirement

class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ("parent", "name", "release_target", "description", "dependencies" )
        widgets = {"release_target": forms.DateInput(attrs={"class":"date-field"})}
