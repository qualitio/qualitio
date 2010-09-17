from django.forms import ModelForm

from tcstorm_requirements.requirements.models import Requirement

class RequirementForm(ModelForm):
    
    
    
    class Meta:
        model = Requirement
        fields = ('name',)
