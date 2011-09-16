from social_auth.backends import OpenIdAuth
from social_auth.backends.google import GoogleBackend

from qualitio import THREAD


class GoogleAuth(OpenIdAuth):
    """Google OpenID authentication"""
    AUTH_BACKEND = GoogleBackend

    def openid_url(self):
        """Return Google OpenID service url"""
        return 'https://www.google.com/accounts/o8/site-xrds?hd=%s' % THREAD.organization.googleapps_domain


BACKENDS = {
    'google': GoogleAuth,
}
