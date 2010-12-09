from django import forms
from equal.requirements.models import Requirement

class RequirementForm(forms.ModelForm):
    dependencies = forms.ModelMultipleChoiceField(Requirement)

    class Meta:
        model = Requirement
        fields = ("parent", "name", "release_target", "description", "dependencies" )
        widgets = {"release_target": forms.DateInput(attrs={"class":"date-field"})}

    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        if "initial" in kwargs: 
            self.fields["dependencies"].queryset = Requirement.objects.filter(pk=1)
