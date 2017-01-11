__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

try:
	from django.conf.urls import patterns, include, url
except ImportError:
	from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

app_name = 'publications'
urlpatterns = patterns('',
	url(r'^publications/', include('publications.urls')),
	url(r'^admin/', include(admin.site.urls)),
)
