from django.conf.urls.defaults import patterns, include, url

from qualitio.organizations.auth.decorators import permission_required
from qualitio.organizations import views


urlpatterns = patterns('',
                       url(r'^$',
                           views.OrganizationDetails.as_view(),
                           name="organization_details"),

                       url(r'^settings/$',
                           permission_required('ADMIN')(views.OrganizationSettings.as_view()),
                           name="organization_settings"),

                       url(r'^settings/profile/$',
                           permission_required('ADMIN')(views.OrganizationSettings.Profile.as_view()),
                           name="organization_settings_profile"),

                       url(r'^settings/users/$',
                           permission_required('ADMIN')(views.OrganizationSettings.Users.as_view()),
                           name="organization_settings_users"),

                       url(r'^settings/users/new/member/$',
                           permission_required('ADMIN')(views.OrganizationSettings.NewMember.as_view()),
                           name="organization_settings_users_new_member"),

                       url(r'^settings/projects/((?P<pk>\d+)/)?$',
                           permission_required('ADMIN')(views.OrganizationSettings.Projects.as_view()),
                           name="organization_settings_projects"),

                       url(r'^project/new/$',
                           permission_required('ADMIN')(views.ProjectNew.as_view()),
                           name="project_new"),

                       url(r'^project/(?P<slug>[\w-]+)/$',
                           permission_required('USER_READONLY')(views.ProjectDetails.as_view()),
                           name="project_details"),
                       )

