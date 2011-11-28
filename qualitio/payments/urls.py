from django.conf.urls.defaults import patterns, include, url

from .views import paypal_ipn

urlpatterns = patterns('',
    url(r'^paypal_ipn/$', paypal_ipn, name="paypal_ipn")
)
