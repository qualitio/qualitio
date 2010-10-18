from django.conf.urls.defaults import *

from equal.requirements.views import *

urlpatterns = patterns('',
                       url(r'^$', index),

                       url(r'^ajax/get_children/$', get_children),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/details/$', details),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/$', edit),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/menu/$', menu),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/test_cases/$', test_cases),
                       url(r'^ajax/valid_requirement_form/(?P<requirement_id>\d+)/?$',
                           valid_requirement_form),

                       url(r'filter/?$', filter)
                       )
