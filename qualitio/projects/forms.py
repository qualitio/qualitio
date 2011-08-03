from qualitio.core import forms
from qualitio.projects.models import Project


class ProjectForm(forms.BaseModelForm):
    class Meta:
        model = Project
        fields = ("name", "homepage", "description")

