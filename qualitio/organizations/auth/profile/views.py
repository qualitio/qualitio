from django.views.generic import UpdateView
from qualitio.organizations.auth.profile.forms import OrganizationMemberProfileForm

class OrganizationMemberProfile(UpdateView):
    template_name = 'organizations/organization_member_profile.html'
    form_class = OrganizationMemberProfileForm
    success_url = '/account/profile/'

    def get_object(self):
        return self.request.user
