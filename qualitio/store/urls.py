from django.conf.urls.defaults import *

from qualitio.core.views import get_children
from qualitio.store.views import *
from qualitio.store.models import TestCaseDirectory, TestCase
from qualitio.filter.views import filter


urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'filter/?$', filter, {'model': TestCase}),

                       url(r'^ajax/get_children$', get_children, {'directory': TestCaseDirectory}),

                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/details/?$', directory_details),
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/edit/?$', directory_edit),
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/new/?$', directory_new),

                       # valid
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/edit/valid/?$', directory_valid),
                       url(r'^ajax/testcasedirectory/new/valid/?$', directory_valid),

                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/details/?$', testcase_details),
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/edit/?$', testcase_edit),
                       url(r'^ajax/testcase/(?P<directory_id>\d+)/new/?$', testcase_new),
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/attachments/?$', testcase_attachments),

                       # valid
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/edit/valid/?$', testcase_valid),
                       url(r'^ajax/testcase/new/valid/?$', testcase_valid),
                       )
