from django.conf.urls.defaults import *

from qualitio import core
from qualitio.filter.views import filter
from qualitio.require.models import Requirement

urlpatterns = patterns('qualitio.require.views',
                       url(r'^$', 'index'),

                       url(r'^filter/', filter,
                           {'model': Requirement}),

                       url(r'^ajax/get_children$', core.get_children,
                           {'directory': Requirement}),

                       url(r'^ajax/get_antecedents$',
                           core.get_ancestors, {'app': 'require'}),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/details/$',
                           'details'),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/$',
                           'edit'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/valid/$',
                           'valid'),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/$',
                           'testcases'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/connect/$',
                           'testcases_connect'),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/new/$',
                           'new'),
                       url(r'^ajax/requirement/new/valid/$',
                           'valid'),

                       url(r'^ajax/requirement/(?P<object_id>\d+)/history/$', core.history,
                           {'Model' : Requirement}),
                       )
