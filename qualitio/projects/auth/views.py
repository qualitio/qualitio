from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.sites.models import get_current_site
from django.views.generic.simple import direct_to_template

from qualitio.projects.models import OrganizationMember
from qualitio.projects.auth.forms import OrganizationAuthForm


@csrf_protect
@never_cache
def login(request):

    if request.method == "POST":

        form = OrganizationAuthForm(data=request.POST)
        if form.is_valid():

            user = form.get_user()
            auth_login(request, user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            organization_member = OrganizationMember.objects.get(user__username=form.cleaned_data['username'],
                                                                 organization__name=form.cleaned_data['organization'])

            return HttpResponseRedirect("http://%s.%s" %
                                        (organization_member.organization.name, request.get_host()))
    else:
        form = OrganizationAuthForm(request,
                                    initial={"organization": request.organization or ""})

    request.session.set_test_cookie()

    return direct_to_template(request, 'registration/login.html',
                              {'form': form})
