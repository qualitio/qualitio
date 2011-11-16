from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _
from django import forms

from qualitio import core


class OrganizationMemberProfileForm(core.BaseModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput, required=False)
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.get('instance')
        super(OrganizationMemberProfileForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        new_password = self.cleaned_data.get('new_password1')

        if new_password:
            self.user.set_password(new_password)

        if commit:
            self.user.save()

        return self.user

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if old_password and not self.user.check_password(old_password):
            raise forms.ValidationError(_("Your old password was entered incorrectly. Please enter it again."))
        return old_password


OrganizationMemberProfileForm.base_fields.keyOrder = [
    'first_name', 'last_name', 'email',
    'old_password', 'new_password1', 'new_password2']
