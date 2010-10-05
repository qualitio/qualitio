from django import forms

from tcstorm_requirements.requirements.models import Requirement
from treebeard.forms import MoveNodeForm

class RequirementForm(MoveNodeForm):

    class Meta:
        model = Requirement
        fields = ('name','_position')

# class FilterForm(forms.Form):


