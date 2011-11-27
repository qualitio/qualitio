from social_auth.backends import OpenIdAuth, OpenIDBackend
from social_auth.backends.google import GoogleAuth

from qualitio import THREAD
from qualitio.organizations.models import OrganizationMember

class GoogleBackend(OpenIDBackend):
    name = 'google'

    def get_user_id(self, details, response):
        return details['email']

    def username(self, details):
        return details['email']


class GoogleAppsBackend(OpenIDBackend):
    name = 'googleapps'

    def get_user_id(self, details, response):
        return details['email']

    def username(self, details):
        return details['email']


class GoogleAppsAuth(OpenIdAuth):
    AUTH_BACKEND = GoogleAppsBackend

    def openid_url(self):
        return ('https://www.google.com/accounts/o8/site-xrds?hd=%s'
                % THREAD.organization.googleapps_domain)

    def auth_complete(self, *args, **kwargs):
        user = super(GoogleAppsAuth, self).auth_complete(*args, **kwargs)

        if self.request.organization not in user.organization_set.all():
            OrganizationMember.objects.get_or_create(
                user=user,
                organization=THREAD.organization,
                role=OrganizationMember.USER
            )
        return user


class NewGoogleAuth(GoogleAuth):
    AUTH_BACKEND = GoogleBackend

    def auth_complete(self, *args, **kwargs):
        user = super(NewGoogleAuth, self).auth_complete(*args, **kwargs)
        OrganizationMember.objects.get_or_create(
            user=user,
            organization=THREAD.organization
        )
        return user



BACKENDS = {
    'google': NewGoogleAuth,
    'googleapps': GoogleAppsAuth,
}
