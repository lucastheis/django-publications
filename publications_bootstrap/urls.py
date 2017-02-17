# -*- coding: utf-8 -*-

try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from . import views

app_name = 'publications_bootstrap'
urlpatterns = [
    url(r'^$', views.year, name='index'),
    url(r'^(?P<publication_id>\d+)/$', views.id, name='id'),
    url(r'^year/(?P<year>\d+)/$', views.year, name='year'),
    url(r'^tag/(?P<keyword>.+)/$', views.keyword, name='keyword'),
    url(r'^list/(?P<title>.+)/$', views.list, name='list'),
    url(r'^unapi/$', views.unapi, name='unapi'),
    url(r'^(?P<name>.+)/$', views.author, name='author'),
]
