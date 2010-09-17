from django.conf.urls.defaults import *

from tcstorm_requirements.requirements.views import index, get_children, requirement

urlpatterns = patterns('',
                       url(r'requirements/$', index),
                       
                       url(r'requirements/ajax/get_children/$', get_children),
                       url(r'requirements/ajax/requirement/(?P<requirement_id>\d+)/?$', requirement),
                       )
