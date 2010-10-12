from django.conf.urls.defaults import *

from tcstorm_requirements.projects.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'teams/?$', teams)
                       )
