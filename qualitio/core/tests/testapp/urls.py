from django.conf.urls.defaults import *
from qualitio.core.views import get_ancestors


urlpatterns = patterns('',
                       url(r'^ajax/get_ancestors$', get_ancestors, {'app': 'testapp'})
                       )
