import urllib
import urlparse
import pprint
import functools

from restkit import Resource

from django.conf import settings

class PayPalException(Exception):
    pass


class PayPal(Resource):

    def __init__(self):
        self.payload = {
            "USER": settings.PAYPAL_USER,
            "PWD": settings.PAYPAL_PASSWORD,
            "SIGNATURE": settings.PAYPAL_SIGNATURE,
            "VERSION": "82%2E0"
        }

        super(PayPal, self).__init__(
            settings.PAYPAL_HOST, follow_redirect=True,
            max_follow_redirect=10
        )

    def post(self, name, **kwargs):
        _payload = self.payload.copy()
        _payload.update(kwargs)
        _payload["METHOD"] = name
        response = dict(urlparse.parse_qsl(
            super(PayPal, self).post(payload=_payload).body_string())
        )

        if response['ACK'] == 'Failure':
            raise PayPalException(response)
        return response

    def __getattr__(self, name):
        return functools.partial(self.post, name)

