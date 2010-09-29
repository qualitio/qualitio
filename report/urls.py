from django.conf.urls.defaults import *

from tcstorm_requirements.report.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^ajax/get_children/$', get_children),)
