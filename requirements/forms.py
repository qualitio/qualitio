from django.forms import ModelForm

from tcstorm_requirements.requirements.models import Requirement
from treebeard.forms import MoveNodeForm

class RequirementForm(MoveNodeForm):
    
    class Meta:
        model = Requirement
        fields = ('name','_position')
