from django.contrib.auth.models import User

from qualitio import core
from django import forms


class RegistrationForm(forms.ModelForm):

    email = forms.EmailField(label="E-mail", max_length=75)
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(render_value=False))

    class Meta(core.BaseModelForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email is already taken.")
        return self.cleaned_data['email']

    def clean(self):
        cleaned_data = self.cleaned_data
        
        if cleaned_data.get('password1') <> cleaned_data.get('password2'):
            self._errors["password1"] = self.error_class(["Password do not match."])
        
        return cleaned_data
