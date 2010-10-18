from django.conf.urls.defaults import *

from equal.projects.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'teams/?$', teams),
                       url(r'team/(?P<team_id>\d+)?$', team_details)
                       )
