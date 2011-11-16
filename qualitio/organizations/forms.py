from django import forms
from django.contrib.auth import models as auth
from django.forms.models import modelformset_factory, inlineformset_factory

from qualitio import store
from qualitio import execute
from qualitio import glossary
from qualitio import core
from qualitio import THREAD

from qualitio.organizations import models


class OrganizationProfileForm(core.BaseModelForm):

    class Meta(core.BaseModelForm.Meta):
        model = models.Organization
        fields = ("name", "slug", "homepage", "description", "googleapps_domain")
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'slug': forms.TextInput(attrs={'readonly': 'readonly'})
        }


class OrganizationGoogleAppsSetupForm(core.BaseModelForm):
    # helper field for handling googleapp additional configuration
    callback = forms.CharField(widget=forms.HiddenInput, required=False)

    slug = forms.RegexField(
        regex="^[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$",
        label="subdomain (part of url address)",
        error_messages={
            'invalid': 'subdomain may only conatin characters from set: 0-9, a-z and - (hypen)'
        })

    class Meta(core.BaseModelForm.Meta):
        model = models.Organization
        fields = ("name", "homepage", "slug", "description", "googleapps_domain")
        widgets = {
            'googleapps_domain': forms.HiddenInput(attrs={'readonly': 'readonly'})
        }


class OrganizationMemberForm(core.BaseModelForm):

    class Meta(core.BaseModelForm.Meta):
        model = models.OrganizationMember
        fields = ("role",)


class NewUserForm(core.BaseModelForm):
    class Meta(core.BaseModelForm.Meta):
        model = auth.User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput,
            }

    email = forms.EmailField(required=True)
    password2 = forms.CharField(label='Retype password', widget=forms.PasswordInput)

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password = self.cleaned_data.get('password')
        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords need to be the same.')
        return password2

    def save(self, *args, **kwargs):
        password2 = self.cleaned_data.pop('password2')
        instance = super(NewUserForm, self).save(*args, **kwargs)
        instance.set_password(password2)
        instance.save()
        return instance

class ProjectForm(core.BaseModelForm):

    class Meta(core.BaseModelForm.Meta):
        model = models.Project
        fields = ("name", "homepage", "description")

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.instance.organization = self.organization

    def clean(self):
        name = self.cleaned_data.get('name')
        qs = models.Project.objects.filter(name=name, organization=self.organization)
        qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Project with name "%s" already exists in "%s" organization.' % (
                    name, self.organization.name))
        return self.cleaned_data


class ProjectUserForm(core.BaseForm):
    username = forms.CharField()

    def clean_username(self):
        data = self.cleaned_data['username']

        try:
            user = auth.User.objects.get(username=data)
        except auth.User.DoesNotExist:
            raise forms.ValidationError("User does not exist.")

        return data


class BaseOrganizationUsersFormSet(core.BaseModelFormSet):
    def get_queryset(self):
        qs = super(BaseOrganizationUsersFormSet, self).get_queryset()
        if THREAD.organization:
            qs = qs.filter(organization=THREAD.organization)
        return qs

    def get_deleted_members_users_ids(self):
        ids = []
        for form in self.deleted_forms:
            ids.append(form.instance.user.id)
        return ids

    def save(self, commit=True, delete_users=False):
        user_ids_to_delete = user_ids_to_delete = self.get_deleted_members_users_ids()
        to_return = super(BaseOrganizationUsersFormSet, self).save(commit=commit)
        if delete_users and commit and user_ids_to_delete:
            auth.User.objects.filter(pk__in=user_ids_to_delete).delete()
        return to_return


OrganizationUsersForm = modelformset_factory(models.OrganizationMember,
                                             form=OrganizationMemberForm,
                                             formset=BaseOrganizationUsersFormSet,
                                             extra=0, can_delete=True)

OrganizationProjectsForm = modelformset_factory(models.Project,
                                                form=ProjectForm,
                                                formset=core.BaseModelFormSet,
                                                extra=0, can_delete=False)

ProjectTestCaseStatusFormSet = inlineformset_factory(models.Project,
                                                     store.TestCaseStatus,
                                                     formset=core.BaseInlineFormSet,
                                                     extra=0)

ProjectTestRunStatusFormSet = inlineformset_factory(models.Project,
                                                    execute.TestRunStatus,
                                                    formset=core.BaseInlineFormSet,
                                                    extra=0)

ProjectTestCaseRunStatusFormSet = inlineformset_factory(models.Project,
                                                        execute.TestCaseRunStatus,
                                                        formset=core.BaseInlineFormSet,
                                                        extra=0)

ProjectGlossaryLanguageFormSet = inlineformset_factory(models.Project,
                                                       glossary.Language,
                                                       formset=core.BaseInlineFormSet,
                                                       extra=0)
