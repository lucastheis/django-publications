__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from publications import views

urlpatterns = [
    url(r'^$', views.year, name='publications.views.year'),
    url(r'^(?P<publication_id>\d+)/$', views.id, name='publications.views.id'),
    url(r'^year/(?P<year>\d+)/$', views.year, name='publications.views.year'),
    url(r'^tag/(?P<keyword>.+)/$', views.keyword, name='publications.views.keyword'),
    url(r'^list/(?P<list>.+)/$', views.list, name='publications.views.list'),
    url(r'^unapi/$', views.unapi, name='publications.views.unapi'),
    url(r'^(?P<name>.+)/$', views.person, name='publications.views.person'),
]
