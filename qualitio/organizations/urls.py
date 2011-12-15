from django.conf.urls.defaults import patterns, include, url

from qualitio.organizations.auth.profile.views import OrganizationMemberProfile
from qualitio.organizations.auth.decorators import permission_required
from qualitio.organizations import views

from qualitio.payments import views as payments

urlpatterns = patterns('',
                       url(r'^none/$',
                           views.OrganizationNone.as_view(),
                           name="organization_none"),

                       url(r'^thanks/$',
                           views.OrganizationRequestThanks.as_view(),
                           name="organization_request_thanks"),

                       url(r'^$',
                           views.OrganizationDetails.as_view(),
                           name="organization_details"),

                       url(r'^account/profile/$', OrganizationMemberProfile.as_view(),
                           name="account_profile"),

                       url(r'^settings/$',
                           permission_required('ADMIN')(views.OrganizationSettings.as_view()),
                           name="organization_settings"),

                       url(r'^settings/profile/$',
                           permission_required('ADMIN')(views.OrganizationSettings.Profile.as_view()),
                           name="organization_settings_profile"),

                       url(r'^settings/users/$',
                           permission_required('ADMIN')(views.OrganizationSettings.Members.as_view()),
                           name="organization_settings_users"),

                       url(r'^settings/users/list/$',
                           permission_required('ADMIN')(
                               views.OrganizationSettings.MembersList.as_view()
                           ),
                           name="organization_settings_members_list"),

                       url(r'^settings/users/new/$',
                           permission_required('ADMIN')(
                               views.OrganizationSettings.MemberNew.as_view()
                           ),
                           name="organization_settings_members_new"),

                       url(r'^settings/projects/((?P<pk>\d+)/)?$',
                           permission_required('ADMIN')(views.OrganizationSettings.Projects.as_view()),
                           name="organization_settings_projects"),

                       url(r'^settings/billing/$',
                           permission_required('ADMIN')(payments.Billing.as_view()),
                           name="organization_settings_billing"),

                       url(r'^settings/billing/cancel/$',
                           permission_required('ADMIN')(payments.BillingCancel.as_view()),
                           name="organization_settings_billing_cancel"),

                       url(r'^project/new/$',
                           permission_required('ADMIN')(views.ProjectNew.as_view()),
                           name="project_new"),

                       url(r'^project/(?P<slug>[\w-]+)/$',
                           permission_required('USER_READONLY')(views.ProjectDetails.as_view()),
                           name="project_details"),

                       url(r'^r/(?P<domain>.*)/googleapps_setup/$',
                           views.GoogleAppsSetupRedirect.as_view(),
                           name="googleapps_setup_redirect"),

                       url(r'^googleapps_setup/$',
                           views.googleapps_domain_setup,
                           name="googleapps_setup"),

                       url(r'^r/(?P<domain>.*)/$',
                           views.GoogleAppsRedirect.as_view(),
                           name="googleapps_redirect"),
                       )

# ?callback=https://www.google.com/a/cpanel/qualitio.com/DomainAppInstall