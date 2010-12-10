from django import forms
from equal.requirements.models import Requirement

class RequirementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.fields['dependencies'].required = False
        if self.instance:
            self.fields['dependencies'].queryset = Requirement.objects.exclude(pk=self.instance.pk)
        else:
            self.fields['dependencies'].queryset = Requirement.objects.all()

    class Meta:
        model = Requirement
        fields = ("parent", "name", "release_target", "description", "dependencies" )
        widgets = {"release_target": forms.DateInput(attrs={"class":"date-field"})}


class SearchTestcasesForm(forms.Form):
    search = forms.CharField(required=True)
