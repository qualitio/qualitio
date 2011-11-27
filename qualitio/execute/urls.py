from django.conf.urls.defaults import *

from qualitio import core
from qualitio import report
from qualitio.execute.views import *
from qualitio.execute.models import TestRunDirectory, TestRun

from qualitio.filter import FilterView


class ExecuteFilterView(FilterView):
    model = TestRun
    fields_order = ['id', 'path', 'name']
    exclude = ['lft', 'rght', 'tree_id', 'level', 'notes',
               'parent', 'project', 'translation']


urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^filter/', ExecuteFilterView()),

                       url(r'^ajax/get_children$', core.get_children,
                           {'directory': TestRunDirectory}),
                       url(r'^ajax/get_antecedents$',
                           core.get_ancestors, {'app': 'execute'}),

                       url(r'^ajax/testrun/(?P<object_id>\d+)/(?P<report_id>\d+)/$',
                           report.report_bound, {'Model': TestRun}),

                       # Test run directory directory urls
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/details/?$',
                           directory_details),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/new/?$',
                           directory_new),
                       url(r'^ajax/testrundirectory/new/valid/?$',
                           directory_valid),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/edit/?$',
                           directory_edit),
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/edit/valid/?$',
                           directory_valid),
                       url(r'^ajax/testrundirectory/(?P<object_id>\d+)/history/$',
                           core.menu_view(TestRunDirectory, "history")(core.history),
                           {'Model' : TestRunDirectory}),

                       # Test run urls
                       url(r'^ajax/testrundirectory/(?P<directory_id>\d+)/newtestrun/?$',
                           testrun_new),
                       url(r'^ajax/testrundirectory/newtestrun/valid/?$',
                           testrun_valid),

                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/details/?$',
                           testrun_details),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/edit/?$',
                           testrun_edit),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/edit/valid/?$',
                           testrun_valid),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/copy/?$',
                           testrun_copy),

                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/execute/?$',
                           testrun_execute),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/notes/?$',
                           testrun_notes),
                       url(r'^ajax/testrun/(?P<testrun_id>\d+)/notes/valid/?$',
                           testrun_notes_valid),

                       url(r'^ajax/testrun/(?P<object_id>\d+)/history/?$',
                           core.menu_view(TestRun, "history")(core.history),
                           {'Model' : TestRun}),

                       # Test run execute helpers
                       url(r'^ajax/testcaserun/(?P<testcaserun_id>\d+)/?$',
                           testcaserun),
                       url(r'^ajax/testcaserun/(?P<testcaserun_id>\d+)/setstatus/?$',
                           testcaserun_setstatus),
                       url(r'^ajax/testcaserun/(?P<testcaserun_id>\d+)/addbug/?$',
                           testcaserun_addbug),
                       url(r'^ajax/testcaserun/(?P<testcaserun_id>\d+)/removebug/?$',
                           testcaserun_removebug),
                       url(r'^ajax/testcaserun/(?P<testcaserun_id>\d+)/bugs/?$',
                           testcaserun_bugs),
                       )
