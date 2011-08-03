from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from qualitio import api
from qualitio import projects


urlpatterns = patterns('',
                       (r'', include('social_auth.urls')),
                       (r'^logout/$', 'django.contrib.auth.views.logout',
                        {'next_page' : '/'}),
                       (r'^login/', 'django.contrib.auth.views.login',
                        {'template_name': "registration/login.html"}),

                       (r'^register/', 'registration.views.register',
                        {'template_name': "registration/registration.html",

                         'backend': 'registration.backends.simple.SimpleBackend',
                         'success_url': 'django.contrib.auth.views.login'}),

                       (r'^permission_required/$', 'qualitio.core.permission_required'),

                       url(r'^$', projects.ProjectList.as_view(), name="dashboard"),
                       url(r'^project/new/$', projects.ProjectNew.as_view(), name="project_new"),
                       url(r'^project/(?P<slug>[\w-]+)/$', projects.ProjectDetails.as_view(), name="project_details"),
                       url(r'^project/(?P<slug>[\w-]+)/edit/$', projects.ProjectEdit.as_view(), name="project_edit"),

                       (r'^project/(?P<project>[\w-]+)/require/',
                        include('qualitio.require.urls', app_name="require")),
                       (r'^project/(?P<project>[\w-]+)/execute/',
                        include('qualitio.execute.urls', app_name="execute")),
                       (r'^project/(?P<project>[\w-]+)/store/',
                        include('qualitio.store.urls', app_name="store")),
                       (r'^project/(?P<project>[\w-]+)/report/',
                        include('qualitio.report.urls', app_name="report")),
                       (r'^project/(?P<project>[\w-]+)/filter/',
                        include('qualitio.filter.urls')),
                       (r'^project/(?P<project>[\w-]+)/glossary/',
                        include('qualitio.glossary.urls')),
                       (r'^account/', include('qualitio.account.urls', app_name="account")),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'', include(api.urls)),
                       )


if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                            )

