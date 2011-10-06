from social_auth.backends import OpenIdAuth
from social_auth.backends.google import GoogleBackend, GoogleAuth
from social_auth.backends import OpenIDBackend

from qualitio import THREAD


class GoogleAppsBackend(OpenIDBackend):
    """Google OpenID authentication backend"""
    name = 'googleapps'

    def get_user_id(self, details, response):
        """Return user unique id provided by service. For google user email
        is unique enought to flag a single user. Email comes from schema:
        http://axschema.org/contact/email"""
        return details['email']


class GoogleAppsAuth(OpenIdAuth):
    """Google OpenID authentication"""
    AUTH_BACKEND = GoogleAppsBackend

    def openid_url(self):
        """Return Google OpenID service url"""
        return ('https://www.google.com/accounts/o8/site-xrds?hd=%s'
                % THREAD.organization.googleapps_domain)


BACKENDS = {
    'google': GoogleAuth,
    'googleapps': GoogleAppsAuth,
}
