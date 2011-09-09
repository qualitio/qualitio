from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from qualitio.projects.auth.decorators import permission_required
from qualitio.actions.views import actions

urlpatterns = patterns('',
                       url(r'^action/execute/(?P<app_label>require|store|execute)/(?P<action_name>\w+)/$',
                           permission_required('USER')(actions), name="qualitio-actions"),
                       )
