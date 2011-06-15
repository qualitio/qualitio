from django.conf.urls.defaults import *


urlpatterns = patterns('',
                       url(r'^$',
                           'qualitio.glossary.views.index'),

                       url(r'ajax/word/list/$',
                           'qualitio.glossary.views.list'),

                       url(r'^ajax/word/new/$',
                           'qualitio.glossary.views.new'),

                       url(r'^ajax/word/(?P<word_id>\d+)/edit/?$',
                           'qualitio.glossary.views.edit'),

                       url(r'^ajax/word/new/valid/$',
                           'qualitio.glossary.views.edit_valid'),

                       url(r'^ajax/word/(?P<word_id>\d+)/edit/valid/$',
                           'qualitio.glossary.views.edit_valid'),

                       url(r'^ajax/language_switch/$',
                           'qualitio.glossary.views.language_switch'),

                       url(r'^ajax/language_switch_valid/$',
                           'qualitio.glossary.views.language_switch_valid'),

                       )
