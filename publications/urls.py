__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.urls import re_path

from publications import views

app_name = 'publications'
urlpatterns = [
    re_path(r'^$', views.year, name='index'),
    re_path(r'^(?P<publication_id>\d+)/$', views.id, name='id'),
    re_path(r'^year/(?P<year>\d+)/$', views.year, name='year'),
    re_path(r'^tag/(?P<keyword>.+)/$', views.keyword, name='keyword'),
    re_path(r'^list/(?P<list>.+)/$', views.list, name='list'),
    re_path(r'^unapi/$', views.unapi, name='unapi'),
    re_path(r'^(?P<name>.+)/$', views.author, name='author'),
]
