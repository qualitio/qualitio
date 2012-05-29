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


class NewMemberForm(core.BaseForm):
    email = forms.EmailField(required=True, label="E-mail address")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if auth.User.objects.filter(
            organization_member__organization=THREAD.organization,
            email=self.cleaned_data.get('email')
        ):
            raise forms.ValidationError("User already in organization.")
        return email


class NewUserForm(core.BaseModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
                                help_text = "Enter the same password as above, for verification.")

    class Meta(core.BaseModelForm.Meta):
        model = auth.User
        fields = ("email",)

    def clean_email(self):

        email = self.cleaned_data.get('email')
        if auth.User.objects.filter(username=email).exists():
            raise forms.ValidationError("email")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

        
class OrganizationNew(core.BaseForm):
    email = forms.EmailField(label="your email")
    choices = (0, "I am a returning user."), (1, "I am a new user.")
    new_user = forms.ChoiceField(
        choices=choices, label="Are you nnew user", widget=forms.RadioSelect, initial=0)
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="password again", required=False, widget=forms.PasswordInput)
    name = forms.CharField(label="organization name")
    
    def clean_name(self):
        name = self.cleaned_data['name']

        if models.Organization.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                'An organization with this name alredy exists.')

        return name

    def clean(self):
        from django.contrib.auth import authenticate
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        new_user = bool(int(self.cleaned_data.get('new_user')))

        if email and password1 and not new_user:
            self.user = authenticate(username=email, password=password1)
            if self.user is None:
                self._errors ['email'] = self.error_class(
                    [u"Please enter a correct username and password. Note that both fields are case-sensitive."])

        if email and password1 and new_user:
            if auth.User.objects.filter(email=email).exists():
                self._errors ['email'] = self.error_class(
                    [u"A user with that email already exists."])
            if password2 != password1:
                self._errors ['password1'] = self.error_class(
                    [u"Repeated password did not match."])

        return self.cleaned_data


class ProjectForm(core.BaseModelForm):

    class Meta(core.BaseModelForm.Meta):
        model = models.Project
        fields = ("name", "homepage")

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.instance.organization = self.organization

    def clean(self):
        name = self.cleaned_data.get('name')
        qs = models.Project.objects.filter(
            name__iexact=name,
            organization=self.organization
        ).exclude(pk=self.instance.pk)
        
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


class OrganizationUsersFormSet(core.BaseInlineFormSet):

    def clean(self):
        super(OrganizationUsersFormSet, self).clean()
        active_members = [member for member in self.cleaned_data\
                          if member['role'] < models.OrganizationMember.INACTIVE]

        if hasattr(self.instance, 'payment'):
            if self.instance.payment.strategy.users < len(active_members):
                raise forms.ValidationError(
                    ("Your current plan is %s and maximum number of users is %s.<br/>" +\
                     "Change your plan to increase the number of users.")
                    % (self.instance.payment, self.instance.payment.strategy.users)
                )


OrganizationUsersForm = inlineformset_factory(models.Organization,
                                              models.OrganizationMember,
                                              form=OrganizationMemberForm,
                                              formset=OrganizationUsersFormSet,
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
