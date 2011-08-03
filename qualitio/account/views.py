from django.template.response import TemplateResponse
from reversion.models import Revision
from articles.models import Article

from qualitio.core.models import Project

def index(request):
    revisons = Revision.objects.filter(user=request.user).order_by("-date_created")
    articles = Article.objects.filter(status__name="Finished")
    projects = Project.objects.all()
    return TemplateResponse(request, "account/base.html",
                            {"revisons": revisons,
                             "articles": articles,
                             "projects": projects})
