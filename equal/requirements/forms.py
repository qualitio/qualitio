from django import forms
from equal.requirements.models import Requirement

class RequirementForm(forms.ModelForm):
    dependency = forms.ModelMultipleChoiceField(queryset=Requirement.objects.all(), required=False)
    
    class Meta:
        model = Requirement
        fields = ("parent", "name", "release_target", "description", "dependency")
        widgets = {'release_target': forms.DateInput(attrs={'class':'date-field'})}
