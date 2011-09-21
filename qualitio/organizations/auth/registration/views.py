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
        user = User.objects.create_user(form.cleaned_data['username'],
                                        form.cleaned_data['email'],
                                        form.cleaned_data['password1'])

        OrganizationMember.objects.create(user=user, organization=self.request.organization)

        send_mail('Welcome in Qualitio Project',
                  render_to_string('registration/registration_thanks.mail',
                                   {"organization": self.request.organization,
                                    "username": form.cleaned_data['username']}),
                  'Qualitio Notifications <notifications@qualitio.com>',
                  [form.cleaned_data['email']])

        organization_admin_emails = \
            User.objects.filter(organization_member__organization=self.request.organization,
                                organization_member__role=OrganizationMember.ADMIN)\
                                .values_list("email", flat=True)

        import ipdb; ipdb.set_trace()
        send_mail('Your organization has new candidate',
                  render_to_string('registration/registration_new_candidate.mail',
                                   {"organization": self.request.organization,
                                    "username": form.cleaned_data['username'],
                                    "email": form.cleaned_data['email']}),
                  'Qualitio Notifications <notifications@qualitio.com>',
                  organization_admin_emails)


        return redirect("registration_thanks")

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class RegisterUserThanks(TemplateView):
    template_name = "registration/registration_thanks.html"
