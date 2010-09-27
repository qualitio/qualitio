from django.conf.urls.defaults import *

from tcstorm_requirements.requirements.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       
                       url(r'^ajax/get_children/$', get_children),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/details/$', details),
                       url(r'^ajax/valid_requirement_form/(?P<requirement_id>\d+)/?$', 
                           valid_requirement_form),
                       
                       )
