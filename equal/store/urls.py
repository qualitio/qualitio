from django.conf.urls.defaults import *

from equal.store.views import *

urlpatterns = patterns('',
                       url(r'^$', index),

                       url(r'^ajax/get_children$', get_children),
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/details/?$', directory_details),
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/edit/?$', directory_edit),
                       #url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/new/?$', directory_new),
                       

                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/details/?$', testcase_details),
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/edit/?$', testcase_edit),
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/attachments/?$', testcase_attachments),
                       # url(r'^ajax/testcase/(?P<testcase_id>\d+)/notes/?$', testcase_notes),
                       # url(r'^ajax/testcase/(?P<testcase_id>\d+)/execute/?$',testcase_execute),

                       # url(r'filter/?$', filter)
                       )
