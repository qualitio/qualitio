from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, RedirectView
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from qualitio.organizations.models import Organization

from .paypal import PayPal, PayPalException
from .models import Strategy, Profile
from .forms import PaymentForm

@csrf_exempt
def paypal_ipn(request, *args, **kwargs):
    if not request.method == "POST":
        raise Http404 

    organization_name, strategy_name = request.POST.get('product_name').split(":")

    profile = Profile.objects.get(organization__name=organization_name)
    
    if request.POST.get('txn_type') == 'recurring_payment' and \
       request.POST.get('payment_status') == u'Completed':
        profile.status = Profile.ACTIVE
        
    elif request.POST.get('txn_type') == 'recurring_payment_profile_created':
        profile.status = Profile.PENDING

    profile.save()

    return HttpResponse()


class Billing(TemplateView):
    template_name = "payments/billing.html"

    def get_context_data(self, **kwargs):
        try:
            self.request.organization.payment
        except Profile.DoesNotExist:
            raise Http404
            
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
            payment_strategy = Strategy.objects.get(
                name=payment_form.cleaned_data['plan']
            )
            payment = self.request.organization.payment
            
            paypal_data = dict(payment_form.cleaned_data, **{
                "CURRENCYCODE": "USD",
                "PROFILESTARTDATE": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "DESC": "%s:%s" % (self.request.organization.name, payment_strategy.name),
                "BILLINGPERIOD": "Month",
                "BILLINGFREQUENCY": "1",
                "AMT": payment_strategy.price,
                "PAYERSTATUS": "verified",
            })
            paypal_data['FIRSTNAME'] = "%s : %s" % (
                self.request.organization.name,
                paypal_data['FIRSTNAME']
            )
            
            paypal = PayPal()

            try:
                paypal.ManageRecurringPaymentsProfileStatus(
                    PROFILEID=payment.paypal_id,
                    ACTION="Cancel"
                )
            except PayPalException as e:
                if e.message['L_ERRORCODE0'] not in ('11556', '11551'): 
                    raise e

            try:
                paypal_response = paypal.CreateRecurringPaymentsProfile(**paypal_data)
            except PayPalException as e:
                
                if e.message['L_ERRORCODE0'] == '10527':
                    payment_form._errors['ACCT'] = payment_form.error_class(
                        [e.message['L_LONGMESSAGE0']])
                
                return self.render_to_response(
                    self.get_context_data(
                        payment_form=payment_form,
                        payment_error=e.message['L_LONGMESSAGE0']
                    )
                )
                    
            valid_time = datetime.now() + relativedelta(months=+1, days=+1)

            old_strategy = payment.strategy
            
            payment.strategy = payment_strategy
            payment.valid_time = valid_time
            payment.paypal_id = paypal_response['PROFILEID']
            payment.status = Profile.PENDING
            
            payment.save()
            
            send_mail(
                'Qualitio Project, Payment profile updated for %s organization'
                % self.request.organization.name,
                render_to_string('payments/profile_update.mail',
                                 {"organization": self.request.organization,
                                  "old_strategy": old_strategy,
                                  "current_strategy": payment.strategy}),
                'Qualitio Notifications <notifications@qualitio.com>',
                self.request.organization.admins.values_list("email", flat=True))

            return redirect("/settings/billing/")

        return self.render_to_response(
            self.get_context_data(**{"payment_form": payment_form}))


class BillingCancel(RedirectView):
    url = "/settings/billing/"
    permanent = False
    
    def get(self, request, *args, **kwargs):
        payment = self.request.organization.payment
        payment.cancel()

        send_mail(
            'Qualitio Project, Payment profile cancled for %s organization'
            % self.request.organization.name,
            render_to_string('payments/profile_cancel.mail',
                             {"organization": self.request.organization}),
            'Qualitio Notifications <notifications@qualitio.com>',
            self.request.organization.admins.values_list("email", flat=True))

        
        return super(BillingCancel, self).get(request, *args, **kwargs)