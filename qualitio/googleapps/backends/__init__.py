from social_auth.backends import OpenIdAuth, OpenIDBackend
from social_auth.backends.google import GoogleAuth

from qualitio import THREAD

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
    AUTH_BACKEND = GoogleBackend

    def openid_url(self):
        return ('https://www.google.com/accounts/o8/site-xrds?hd=%s'
                % THREAD.organization.googleapps_domain)


BACKENDS = {
    'google': GoogleAuth,
    'googleapps': GoogleAppsAuth,
}
