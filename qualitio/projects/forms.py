from qualitio.core.forms import BaseModelForm
from qualitio.projects.models import Project


class ProjectForm(BaseModelForm):

    class Meta(BaseModelForm.Meta):
        model = Project
        fields = ("name", "homepage", "description", "team")

