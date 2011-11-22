from django.conf.urls.defaults import *

from qualitio import core
from qualitio.report.views import *
from qualitio.report.models import ReportDirectory

urlpatterns = patterns('',
                       url(r'^$', index),

                       url(r'^ajax/get_children/?$', core.get_children,
                           {'directory': ReportDirectory}),

                       url(r'^ajax/get_antecedents$',
                           core.get_ancestors, {'app': 'report'}),

                       url(r'^ajax/reportdirectory/(?P<directory_id>\d+)/details/?$',
                           directory_details),
                       url(r'^ajax/reportdirectory/(?P<directory_id>\d+)/new/?$',
                           directory_new),
                       url(r'^ajax/reportdirectory/new/valid/?$',
                           directory_valid),
                       url(r'^ajax/reportdirectory/(?P<directory_id>\d+)/edit/?$',
                           directory_edit),
                       url(r'^ajax/reportdirectory/(?P<directory_id>\d+)/edit/valid/?$',
                           directory_valid),

                       # url(r'^ajax/reportdirectory/(?P<object_id>\d+)/history/$',
                       #     core.history, {'Model' : ReportDirectory}),

                       url(r'^ajax/report/(?P<report_id>\d+)/details/?$',
                           report_details),

                       url(r'^ajax/reportdirectory/(?P<directory_id>\d+)/newreport/?$',
                           report_new),
                       url(r'^ajax/newreport/valid/?$',
                           report_valid),

                       url(r'^ajax/report/(?P<report_id>\d+)/edit/?$',
                           report_edit),
                       url(r'^ajax/report/(?P<report_id>\d+)/edit/valid/?$',
                           report_valid),

                       url(r'^external/(?P<report_id>\d+)/(?P<object_type_id>\d+)/(?P<object_id>\d+)/.*',
                           report_external),

                       url(r'^external/(?P<report_id>\d+)/.*',
                           report_external)
                       )

