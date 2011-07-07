from django.conf.urls.defaults import *

from qualitio import core
from qualitio import report
from qualitio.filter.views import filter

from qualitio.require.models import Requirement
from qualitio.require.filter import RequirementFilter
from qualitio.require.views import *

urlpatterns = patterns('',
                       url(r'^$', index),

                       url(r'^filter/', filter,
                           {'model_filter_class': RequirementFilter,
                            'fields_order': ['id', 'path', 'name', 'release_target'],
                            'exclude': ['lft', 'rght', 'tree_id', 'level', 'dependencies', 'description', 'parent', 'alias'],
                            }),

                       url(r'^ajax/get_children$', core.get_children,
                           {'directory': Requirement}),

                       url(r'^ajax/get_antecedents$',
                           core.get_ancestors, {'app': 'require'}),

                       url(r'^ajax/requirement/(?P<object_id>\d+)/(?P<report_id>\d+)/$',
                           report.report_bound, {'Model': Requirement}),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/details/$',
                           details),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/$',
                           edit),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/valid/$',
                           valid),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/$',
                           testcases),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/connect/$',
                           testcases_connect),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/new/$',
                           new),
                       url(r'^ajax/requirement/new/valid/$',
                           valid),

                       url(r'^ajax/requirement/(?P<object_id>\d+)/history/$',
                           core.menu_view(Requirement, "history")(core.history),
                           {'Model' : Requirement}),
                       )

