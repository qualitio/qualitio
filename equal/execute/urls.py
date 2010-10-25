from django.conf.urls.defaults import *

from equal.execute.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^testrun/(?P<testrun_id>\d+)/execute/?$',testrun_execute),

                       url(r'^ajax/get_children$', get_children),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/details/?$', directory_details),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/new/?$', directory_new),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/edit/?$', directory_edit),

                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/details/?$', testrun_details),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/notes/?$', testrun_notes),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/edit/?$', testrun_edit),

                       # url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/$', edit),
                       # url(r'^ajax/requirement/(?P<requirement_id>\d+)/menu/$', menu),
                       # url(r'^ajax/requirement/(?P<requirement_id>\d+)/test_cases/$', test_cases),
                       # url(r'^ajax/valid_requirement_form/(?P<requirement_id>\d+)/?$',
                       #     valid_requirement_form),

                       # url(r'filter/?$', filter)
                       )
