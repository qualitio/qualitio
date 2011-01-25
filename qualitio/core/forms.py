from django import forms

class PathModelForm(forms.ModelForm):
    class Meta:
        exclude = ("path",)
