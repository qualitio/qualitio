# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

from qualitio.chart.views import FilterXaxisModelView, ChartDataView, ChartView

urlpatterns = patterns(
    'chart.views',
    (r'^$', 'index'),
    (r'^(?P<chartid>\w+)/$', FilterXaxisModelView()),
    (r'^(?P<chartid>\w+)/chartview/$', ChartView()),
    (r'^(?P<chartid>\w+)/chartdata/$', ChartDataView()),
    )
