from django.views.generic import CreateView, TemplateView
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import send_mail

from qualitio.organizations.models import OrganizationMember

import forms


class RegisterUser(CreateView):
    model = User
    template_name = "registration/registration.html"
    form_class = forms.RegistrationForm
    success_url = "/login/"

    def form_valid(self, form):
        organization = self.request.organization

        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        
        user = User.objects.create_user(email, email, password)

        OrganizationMember.objects.create(user=user,
                                          organization=organization)

        send_mail('Welcome to Qualitio Project',
                  render_to_string('registration/registration_thanks.mail',
                                   {"organization": self.request.organization,
                                    "username": email}),
                  'Qualitio Notifications <notifications@qualitio.com>',
                  [form.cleaned_data['email']])

        organization_admin_emails = organization.admins.values_list("email", flat=True)

        send_mail('Your organization has a new candidate',
                  render_to_string('registration/registration_new_candidate.mail',
                                   {"organization": organization,
                                    "username": user,
                                    "email": email}),
                  'Qualitio Notifications <notifications@qualitio.com>',
                  organization_admin_emails)


        return redirect("registration_thanks")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class RegisterUserThanks(TemplateView):
    template_name = "registration/registration_thanks.html"
