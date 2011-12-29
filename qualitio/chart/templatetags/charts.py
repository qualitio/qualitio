# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

from qualitio.chart.models import ChartQuery
from qualitio.chart.types import get_engine


register = template.Library()


def chart(context, name):
    chart_query = (ChartQuery.objects.filter(name=name) or [None])[0]

    if not chart_query:
        return {
            'error': 'There\'s not such chart: "%s"' % name,
        }

    charttype = chart_query.get_type_class()
    engine = get_engine()
    template_context = {
        'chart_query': chart_query,
        'charttype': charttype,
        'engine': engine,
        'MEDIA_URL': settings.MEDIA_URL,
        'js_plot_handler': "%sChart" % charttype.type,
    }
    return template_context
register.inclusion_tag('chart/charttag.html', takes_context=True)(chart)
