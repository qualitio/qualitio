from django.conf.urls.defaults import patterns, url
from qualitio import core
from qualitio.requirements.models import Requirement
from qualitio.filter.views import filter

urlpatterns = patterns('qualitio.requirements.views',
                       url(r'^$', 'index'),
                       url(r'filter/?$', filter, {'model': Requirement}),

                       url(r'^ajax/get_children$', core.get_children, {'directory': Requirement}),

                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/details/$', 'details'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/$', 'edit'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/$', 'test_cases'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/new/$', 'new'),
                       url(r'^ajax/requirement/(?P<object_id>\d+)/history/$', core.history, {'Model' : Requirement}),

                       #helpers view, subviews
                       url(r'^ajax/requirement/new/valid/$', 'valid'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/valid/$', 'valid'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/list/$', 'available_testcases'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/connect/$', 'connect_testcases'),
                       )
