#Has to be applied to DirectoryModelForms
from mptt.forms import MoveNodeForm

from django import forms

class PathModelForm(forms.ModelForm):
    class Meta:
        exclude = ("path",)
