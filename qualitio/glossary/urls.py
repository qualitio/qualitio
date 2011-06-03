from django.conf.urls.defaults import *


urlpatterns = patterns('',
                       url(r'^$',
                           'glossary.views.index'),

                       url(r'ajax/word/list/$',
                           'glossary.views.list'),

                       url(r'^ajax/word/new/$',
                           'glossary.views.new'),

                       url(r'^ajax/word/(?P<word_id>\d+)/edit/?$',
                           'glossary.views.edit'),

                       url(r'^ajax/word/new/valid/$',
                           'glossary.views.edit_valid'),

                       url(r'^ajax/word/(?P<word_id>\d+)/edit/valid/$',
                           'glossary.views.edit_valid'),

                       url(r'^ajax/language_switch/$',
                           'glossary.views.language_switch'),

                       url(r'^ajax/language_switch_valid/$',
                           'glossary.views.language_switch_valid'),

                       )
