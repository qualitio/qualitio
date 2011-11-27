from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from qualitio.organizations.models import Organization
from .models import PaymentStrategy

@csrf_exempt
def paypal_ipn(request, *args, **kwargs):

    if request.POST.get('payment_status') == u'Completed':
        organization_name = request.POST['option_selection1']
        strategy_name = request.POST['option_selection2']
        strategy_price = request.POST['payment_gross']

        organization = Organization.objects.get(name=organization_name)
        organization.payment = PaymentStrategy.objects.get(
            name=strategy_name,
            price=strategy_price
        )
        organization.save()

    return HttpResponse()
