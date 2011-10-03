from django.views.generic import UpdateView

from qualitio.organizations.auth.profile.forms import OrganizationMemberProfileForm
from qualitio.core.utils import json_response, success, failed


class OrganizationMemberProfile(UpdateView):
    template_name = 'organizations/organization_member_profile.html'
    form_class = OrganizationMemberProfileForm
    success_url = '/account/profile/'

    def get_object(self):
        return self.request.user

    @json_response
    def form_valid(self, form):
        self.object = form.save()
        return success(message="Account profile successfully updated.")

    @json_response
    def form_invalid(self, form):
        return failed(message=form.error_message(),
                      data=form.errors_list())
