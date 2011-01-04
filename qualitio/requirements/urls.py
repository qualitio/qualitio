from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('qualitio.requirements.views',
                       url(r'^$', 'index'),
                       url(r'filter/?$', filter),
                       
                       url(r'^ajax/get_children/$', 'get_children'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/details/$', 'details'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/$', 'edit'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/$', 'test_cases'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/new/$', 'new'),
                       
                       #helpers view, subviews
                       url(r'^ajax/requirement/new/valid/$', 'valid'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/edit/valid/$', 'valid'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/list/$', 'available_testcases'),
                       url(r'^ajax/requirement/(?P<requirement_id>\d+)/testcases/connect/$', 'connect_testcases'),
                       )
