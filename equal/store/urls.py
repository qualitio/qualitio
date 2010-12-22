from django.conf.urls.defaults import *

from equal.store.views import *

urlpatterns = patterns('',
                       url(r'^$', index),

                       url(r'^ajax/get_children$', get_children),
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/details/?$', directory_details),
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/edit/?$', directory_edit),
                                              

                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/details/?$', testcase_details),
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/edit/?$', testcase_edit),
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/attachments/?$', testcase_attachments),
                       
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/edit/valid/$', testcase_valid),
                       )
