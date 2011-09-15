from django import forms
from django.contrib.auth import models as auth
from django.forms.models import modelformset_factory, inlineformset_factory

from qualitio import store
from qualitio import execute
from qualitio import glossary
from qualitio import core

from qualitio.organizations import models


class OrganizationProfileForm(core.BaseModelForm):

    class Meta(core.BaseModelForm.Meta):
        model = models.Organization
        fields = ("name", "slug", "homepage", "description", "googleapps_domain")
        widgets = {
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'slug': forms.TextInput(attrs={'readonly': 'readonly'})
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
