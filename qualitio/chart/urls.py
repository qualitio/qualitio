# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

from qualitio.chart.models import ChartQuery
from qualitio.chart.views import (FilterXaxisModelView,
    ChartDataView, ChartView, NewChartView, SaveChartView,
    SavedChartView, SavedChartFilterView, DeleteChartQueryView)

urlpatterns = patterns(
    '',
    (r'^$', 'django.views.generic.simple.direct_to_template', {
        'template': 'chart/base.html',
    }),
    (r'^new/$', NewChartView.as_view()),

    (r'^filter/(?P<chartid>\w+)/$', FilterXaxisModelView.as_view()),
    (r'^view/(?P<chartid>\w+)/$', ChartView.as_view()),
    (r'^data/(?P<chartid>\w+)/$', ChartDataView.as_view()),

    (r'^saved/(?P<id>\d+)/$', SavedChartView.as_view()),
    (r'^saved/(?P<id>\d+)/filter/$', SavedChartFilterView.as_view()),

    (r'^ajax/save/((?P<id>\d+)/)?$', SaveChartView.as_view()),
    (r'^ajax/delete/(?P<id>\d+)/$', DeleteChartQueryView.as_view()),
    (r'^ajax/list/$', 'django.views.generic.simple.direct_to_template', {
        'template': 'chart/list.html',
        'extra_context': {
            'chart_list': lambda : ChartQuery.objects.all(),
        }
    }),
)
