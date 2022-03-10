__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.urls import path, include, re_path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
	re_path(r'^publications/', include('publications.urls', namespace='publications')),
	path(r'admin/', admin.site.urls),
]
