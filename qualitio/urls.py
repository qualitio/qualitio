from django.conf.urls.defaults import *
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import admin
admin.autodiscover()

from qualitio import api
from qualitio.organizations.auth.registration.views import RegisterUser, RegisterUserThanks
from qualitio.organizations import views as organization_views


def admin_redirect(request, *args, **kwargs):
    if request.organization:
        site_host = ".".join(request.get_host().split('.')[1:])
        protocol = 'https' if request.is_secure() else 'http'
        return redirect("%s://%s/admin/" % (protocol,site_host))

    return admin.site.index(request, *args, **kwargs)


urlpatterns = patterns('',
                       (r'', include('social_auth.urls')),
                       (r'', include('qualitio.organizations.urls')),

                       url(r'^register/$', RegisterUser.as_view(), name="registration"),
                       url(r'^register/thanks/$',
                           RegisterUserThanks.as_view(), name="registration_thanks"),
                       url(r'^inactive/',
                           organization_views.UserInactive.as_view(), name="inactive"),
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {'next_page' : '/'}, name="logout"),
                       url(r'^login/$', 'django.contrib.auth.views.login',
                           {'template_name': "registration/login.html"}, name="login"),

                       (r'^permission_required/$', 'qualitio.core.permission_required'),

                       (r'^project/(?P<project>[\w-]+)/require/',
                        include('qualitio.require.urls', app_name="require")),
                       (r'^project/(?P<project>[\w-]+)/execute/',
                        include('qualitio.execute.urls', app_name="execute")),
                       (r'^project/(?P<project>[\w-]+)/store/',
                        include('qualitio.store.urls', app_name="store")),
                       (r'^project/(?P<project>[\w-]+)/report/',
                        include('qualitio.report.urls', app_name="report")),
                       (r'^project/(?P<project>[\w-]+)/actions/',
                        include('qualitio.actions.urls')),
                       (r'^project/(?P<project>[\w-]+)/glossary/',
                        include('qualitio.glossary.urls', app_name="glossary")),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/$', admin_redirect),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^project/[\w-]+/', include(api.urls)),
                       )


if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                            )

