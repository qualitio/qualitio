from django.contrib.auth.models import User

from qualitio import core
from django import forms


class RegistrationForm(forms.ModelForm):

    username = forms.RegexField(label="Username", regex=r'^\w+$', max_length=30)
    email = forms.EmailField(label="E-mail", max_length=75)
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Password (again)",
                                widget=forms.PasswordInput(render_value=False))

    class Meta(core.BaseModelForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email is already taken.")
        return self.cleaned_data['email']
