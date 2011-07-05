from django.conf.urls.defaults import *

from qualitio import core
from qualitio import report
from qualitio.store.views import *
from qualitio.store.models import TestCaseDirectory, TestCase
from qualitio.filter.views import filter


urlpatterns = patterns('',
                       url(r'^$', index),
                       url(r'^filter/', filter,
                           {'model': TestCase,
                            'fields_order': ['id', 'path', 'name', 'requirement'],
                            'exclude': ['lft', 'rght', 'tree_id', 'level', 'precondition', 'description', 'parent'],
                            'app_menu_items': [{'name': 'glossary', 'url': '/glossary/'}],
                            }),

                       url(r'^ajax/get_children$', core.get_children,
                           {'directory': TestCaseDirectory}),

                       url(r'^ajax/get_antecedents$',
                           core.get_ancestors, {'app': 'store'}),

                       url(r'^ajax/testcase/(?P<object_id>\d+)/(?P<report_id>\d+)/$',
                           report.report_bound, {'Model': TestCase}),

                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/details/?$',
                           directory_details),

                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/edit/?$',
                           directory_edit),
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/edit/valid/$',
                           directory_valid),

                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/new/?$',
                           directory_new),
                       url(r'^ajax/testcasedirectory/new/valid/$',
                           directory_valid),


                       # Test case urls
                       url(r'^ajax/testcasedirectory/(?P<directory_id>\d+)/newtestcase/?$',
                           testcase_new),
                       url(r'^ajax/testcasedirectory/newtestcase/valid/$',
                           testcase_valid),

                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/edit/?$',
                           testcase_edit),
                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/edit/valid/$',
                           testcase_valid),

                       url(r'^ajax/testcase/(?P<testcase_id>\d+)/details/?$',
                           testcase_details),


                       url(r'^ajax/testcase/(?P<object_id>\d+)/history/$',
                           core.menu_view(TestCase, "history")(core.history),
                           {'Model' : TestCase}),

                       url(r'^ajax/testcasedirectory/(?P<object_id>\d+)/history/$',
                           core.menu_view(TestCaseDirectory, "history")(core.history),
                           {'Model' : TestCaseDirectory}),
                       )
