from django.conf.urls.defaults import patterns, include, url

from qualitio.projects import views


urlpatterns = patterns('',
                       url(r'^$',
                           views.ProjectList.as_view(), name="dashboard"),
                       url(r'^project/new/$',
                           views.ProjectNew.as_view(), name="project_new"),
                       url(r'^project/(?P<slug>[\w-]+)/$',
                           views.ProjectDetails.as_view(), name="project_details"),
                       url(r'^project/(?P<slug>[\w-]+)/edit/$',
                           views.ProjectEdit.as_view(), name="project_edit"),
                       url(r'^project/(?P<slug>[\w-]+)/settings/$',
                           views.ProjectSettingsEdit.as_view(), name="project_settings"),
                       )
