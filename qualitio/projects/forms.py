from django import forms
from django.contrib.auth import models as auth

from qualitio.core.middleware import THREAD
from qualitio.core.forms import BaseModelForm
from qualitio.projects.models import Project
from qualitio import core

class ProjectForm(BaseModelForm):

    class Meta(BaseModelForm.Meta):
        model = Project
        fields = ("name", "homepage", "description")


class ProjectUserForm(core.BaseForm):
    username = forms.CharField()

    def clean_username(self):
        data = self.cleaned_data['username']

        try:
            user = auth.User.objects.get(username=data)
        except auth.User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")

        if THREAD.project.owner == user:
            raise forms.ValidationError("You can't add creator of project to users.")

        if THREAD.project.team.filter(username=data).exists():
            raise forms.ValidationError("This users is already added to project.")

        return data
