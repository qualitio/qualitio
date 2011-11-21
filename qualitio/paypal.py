import urllib
import urlparse
import pprint
import functools

from restkit import Resource


class PayPalException(Exception):
    pass


class PayPal(Resource):

    def __init__(self):
        self.payload = {
            "USER": PAYPAL_USER,
            "PWD": PAYPAL_PASSWORD,
            "SIGNATURE": PAYPAL_SIGNATURE,
            "VERSION": "82%2E0"
        }

        super(PayPal, self).__init__(PAYPAL_HOST, follow_redirect=True,
                                     max_follow_redirect=10)

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


paypal = PayPal()
<<<<<<< HEAD
pprint.pprint(paypal.GetTransactionDetails(TRANSACTIONID="62F98038A3404964N"))
=======
# pprint.pprint(paypal.GetTransactionDetails(TRANSACTIONID="62F98038A3404964N"))
# pprint.pprint(paypal.GetTransactionDetails(TRANSACTIONID="2YS68286B0644402R"))
pprint.pprint(paypal.RefundTransaction(TRANSACTIONID="2YS68286B0644402R"))
>>>>>>> 87cc20952810844fab1d02c840be234509d49a56
