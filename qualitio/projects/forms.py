from django import forms
from django.contrib.auth import models as auth
from django.forms.models import modelformset_factory

from qualitio.projects import models
from qualitio.core.forms import BaseModelForm, BaseModelFormSet, BaseForm
from qualitio.core.middleware import THREAD


class OrganizationProfileForm(BaseModelForm):

    class Meta(BaseModelForm.Meta):
        model = models.Organization
        fields = ("name", "slug", "homepage", "description", "googleapps_domain")
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'slug': forms.TextInput(attrs={'readonly': 'readonly'})
        }


class OrganizationMemberForm(BaseModelForm):

    class Meta(BaseModelForm.Meta):
        model = models.OrganizationMember
        fields = ("role",)

OrganizationUsersForm = modelformset_factory(models.OrganizationMember,
                                             form=OrganizationMemberForm,
                                             formset=BaseModelFormSet,
                                             extra=0, can_delete=True)

class ProjectForm(BaseModelForm):

    class Meta(BaseModelForm.Meta):
        model = models.Project
        fields = ("name", "homepage", "description")


class ProjectUserForm(BaseForm):
    username = forms.CharField()

    def clean_username(self):
        data = self.cleaned_data['username']

        try:
            user = auth.User.objects.get(username=data)
        except auth.User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")

        # if THREAD.project.owner == user:
        #     raise forms.ValidationError("You can't add creator of project to users.")

        if THREAD.project.team.filter(username=data).exists():
            raise forms.ValidationError("This users is already added to project.")

        return data
