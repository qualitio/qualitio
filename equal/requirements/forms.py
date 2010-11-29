from django import forms
from equal.requirements.models import Requirement

class RequirementForm(forms.ModelForm):
    dependency = forms.ModelMultipleChoiceField(queryset=Requirement.objects.all())
    
    class Meta:
        model = Requirement
        fields = ("name", "parent", "release_target", "dependency", "description")
        widgets = {'release_target': forms.DateInput(attrs={'class':'date-field'})}
