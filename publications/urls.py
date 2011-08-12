__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'publications.views.year'),
	(r'^(?P<publication_id>\d+)/$', 'publications.views.id'),
	(r'^year/(?P<year>\d+)/$', 'publications.views.year'),
	(r'^tag/(?P<keyword>.+)/$', 'publications.views.keyword'),
	(r'^(?P<name>.+)/$', 'publications.views.person'),
)
