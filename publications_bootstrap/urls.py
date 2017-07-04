# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

app_name = 'publications_bootstrap'
urlpatterns = [
    url(r'^$', views.by_year, name='index'),
    url(r'^(?P<publication_id>\d+)/$', views.by_id, name='id'),
    url(r'^year/(?P<year>\d+)/$', views.by_year, name='year'),
    url(r'^tag/(?P<tag>.+)/$', views.by_tag, name='tag'),
    url(r'^catalog/(?P<title>.+)/$', views.for_catalog, name='catalog'),
    url(r'^unapi/$', views.by_unapi, name='unapi'),
    url(r'^(?P<name>.+)/$', views.by_author, name='author'),
]
