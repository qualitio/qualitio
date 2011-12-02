from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, RedirectView
from django.http import HttpResponse
from django.shortcuts import redirect

from qualitio.organizations.models import Organization

from .paypal import PayPal, PayPalException
from .models import Strategy
from .forms import PaymentForm

@csrf_exempt
def paypal_ipn(request, *args, **kwargs):

    if request.POST.get('payment_status') == u'Completed':
        organization_name = request.POST['option_selection1']
        strategy_name = request.POST['option_selection2']
        strategy_price = request.POST['payment_gross']

        organization = Organization.objects.get(name=organization_name)
        organization.payment = Strategy.objects.get(
            name=strategy_name,
            price=strategy_price
        )
        organization.save()

    return HttpResponse()


class Billing(TemplateView):
    template_name = "payments/billing.html"

    def get_context_data(self, **kwargs):
        context = {
            "strategies": Strategy.objects.all(),
            "organization": self.request.organization,
            "payment_form": PaymentForm()
        }
        context.update(kwargs)
        return context

    def post(self, *args, **kwargs):
        payment_form = PaymentForm(self.request.POST)
        if payment_form.is_valid():
            try:
                payment_strategy = Strategy.objects.get(
                    name=payment_form.cleaned_data['plan']
                )
                payment = self.request.organization.payment

                paypal_data = dict(payment_form.cleaned_data, **{
                    "CURRENCYCODE": "USD",
                    "PROFILESTARTDATE": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                    "DESC": payment_strategy.name,
                    "BILLINGPERIOD": "Month",
                    "BILLINGFREQUENCY": "1",
                    "AMT": payment_strategy.price,
                    "PAYERSTATUS": "verified"
                })
                paypal = PayPal()

                if payment.paypal_id:
                    paypal.ManageRecurringPaymentsProfileStatus(
                        PROFILEID=payment.paypal_id,
                        ACTION="Cancel"
                    )

                paypal_response = paypal.CreateRecurringPaymentsProfile(**paypal_data)

                valid_till = datetime.now() + relativedelta(months=+1, days=+1)

                payment.strategy = payment_strategy
                payment.valid_till = valid_till
                payment.paypal_id = paypal_response['PROFILEID']
                payment.status = True
                payment.save()

                return redirect("/settings/billing/")

            except PayPalException as e:
                return self.render_to_response(
                    self.get_context_data(
                        payment_form=payment_form,
                        payment_error=e.message['L_LONGMESSAGE0']
                    )
                )

        return self.render_to_response(
            self.get_context_data(payment_form=payment_form)
        )



class BillingCancel(RedirectView):
    url = "/settings/billing/"
    permanent = False

    def get(self, request, *args, **kwargs):
        payment = self.request.organization.payment

        paypal = PayPal()
        paypal.ManageRecurringPaymentsProfileStatus(
            PROFILEID=payment.paypal_id,
            ACTION="Cancel"
        )


        payment.paypal_id = ""
        payment.status = False
        payment.save()

        return super(BillingCancel, self).get(request, *args, **kwargs)