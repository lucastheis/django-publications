__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.conf.urls import  url

from django.urls import path, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
	url(r'^publications/', include('publications.urls', namespace='publications')),
	path(r'admin/', admin.site.urls),
]
