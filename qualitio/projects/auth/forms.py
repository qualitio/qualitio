from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class OrganizationAuthForm(AuthenticationForm):
    organization = forms.CharField()

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        organization = self.cleaned_data.get('organization')

        if username and password and organization:
            self.user_cache = authenticate(username=username,
                                           password=password,
                                           organization=organization)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct username and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        self.check_for_test_cookie()
        return self.cleaned_data

