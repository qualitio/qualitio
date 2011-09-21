from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from qualitio.organizations.models import OrganizationMember

import forms


class RegisterUser(CreateView):
    model = User
    template_name = "registration/registration.html"
    form_class = forms.RegistrationForm
    success_url = "/login/"

    def form_valid(self, form):
        user = User.objects.create_user(form.cleaned_data['username'],
                                        form.cleaned_data['email'],
                                        form.cleaned_data['password1'])

        OrganizationMember.objects.create(user=user, organization=self.request.organization)

        return redirect("registration_thanks")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class RegisterUserThanks(TemplateView):
    template_name = "registration/registration_thanks.html"
