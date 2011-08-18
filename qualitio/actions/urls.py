from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^action/execute/(?P<app_label>require|store|execute)/(?P<action_name>\w+)/$',
                           'qualitio.actions.views.actions', name="qualitio-actions"),
                       )
