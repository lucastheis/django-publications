__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

try:
	from django.conf.urls import include, url
except ImportError:
	from django.conf.urls.defaults import include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
	url(r'^publications/', include('publications.urls', namespace='publications')),
	url(r'^admin/', include(admin.site.urls)),
]
