from django import forms

from equal.requirements.models import Requirement
from treebeard.forms import MoveNodeForm

class RequirementForm(MoveNodeForm):

    class Meta:
        model = Requirement
        fields = ('name','_position')

# class FilterForm(forms.Form):


