from qualitio import module_absolute_url

get_absolute_url = module_absolute_url(module_name="chart")
verbose_name = "chart"

from django.template.base import add_to_builtins
add_to_builtins('qualitio.chart.templatetags.charts')
