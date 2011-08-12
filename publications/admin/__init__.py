__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.contrib import admin
from publications.models import Type, Publication
from typeadmin import TypeAdmin
from publicationadmin import PublicationAdmin

admin.site.register(Type, TypeAdmin)
admin.site.register(Publication, PublicationAdmin)
