from django.template.response import TemplateResponse
from reversion.models import Revision

def index(request):
    revisons = Revision.objects.filter(user=request.user).order_by("-date_created")
    return TemplateResponse(request, "account/base.html",
                            {"revisons": revisons})
