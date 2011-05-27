from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^action/execute/(?P<app_label>require|store|execute)/(?P<action_name>\w+)/$',
                        'qualitio.filter.views.actions'),
                       )
