from django.conf.urls.defaults import patterns, include, url

from qualitio.projects import views


urlpatterns = patterns('',
                       url(r'^$',
                           views.OrganizationDetails.as_view(),
                           name="organization_details"),

                       url(r'^settings/$',
                           views.OrganizationSettings.as_view(),
                           name="organization_settings"),

                       url(r'^settings/profile/$',
                           views.OrganizationSettings.Profile.as_view(),
                           name="organization_settings_profile"),

                       url(r'^settings/users/$',
                           views.OrganizationSettings.Users.as_view(),
                           name="organization_settings_users"),

                       url(r'^settings/users/new/member/$',
                           views.OrganizationSettings.NewMember.as_view(),
                           name="organization_settings_users_new_member"),

                       url(r'^settings/projects/((?P<pk>\d+)/)?$',
                           views.OrganizationSettings.Porjects.as_view(),
                           name="organization_settings_projects"),

                       url(r'^project/new/$',
                           views.ProjectNew.as_view(),
                           name="project_new"),

                       url(r'^project/(?P<slug>[\w-]+)/$',
                           views.ProjectDetails.as_view(),
                           name="project_details"),
                       )

