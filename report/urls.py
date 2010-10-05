from django.conf.urls.defaults import *

from tcstorm_requirements.report.views import *

urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^ajax/(?P<node_type>.+)/(?P<node_id>\d+)/(?P<view>.+)/menu/$', menu),

                       url(r'^ajax/report/(?P<report_id>\d+)/details/$', report_details),
                       url(r'^ajax/report/(?P<report_id>\d+)/edit/$', report_edit),

                       url(r'^ajax/reportdirectory/(?P<reportdirectory_id>\d+)/details/$', reportdirectory_details),
                       url(r'^ajax/reportdirectory/(?P<reportdirectory_id>\d+)/edit/$', reportdirectory_edit),

                       url(r'^ajax/get_children/$', get_children),)
