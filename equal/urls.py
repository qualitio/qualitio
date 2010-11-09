from django.conf.urls.defaults import patterns, include
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^require/', include('equal.requirements.urls')),
                       (r'^report/', include('equal.report.urls')),
                       (r'^settings/', include('equal.projects.urls')),
                       (r'^execute/', include('equal.execute.urls')),
                       (r'^store/', include('equal.store.urls')),

                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       )



if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                            )
