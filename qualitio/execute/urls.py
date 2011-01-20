from django.conf.urls.defaults import *

from qualitio.execute.views import *

urlpatterns = patterns('',
                       url(r'^$', index),

                       url(r'^ajax/get_children$', get_children),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/details/?$', directory_details),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/new/?$', directory_new),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/edit/?$', directory_edit),

                       # valid
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/edit/valid/?$', directory_valid),
                       url(r'^ajax/testrundirectory/new/valid/?$', directory_valid),
                       
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/details/?$', testrun_details),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/notes/?$', testrun_notes),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/edit/?$', testrun_edit),
                       url(r'^ajax/testrun/(?P<directory_id>\d+)/new/?$', testrun_new),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/execute/?$',testrun_execute),

                       # valid
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/edit/valid/?$', testrun_valid),
                       url(r'^ajax/testrun/new/valid/?$', testrun_valid),
                       )
