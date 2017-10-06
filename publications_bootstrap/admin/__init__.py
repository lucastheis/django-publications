# -*- coding: utf-8 -*-

from django.contrib import admin

from .catalogadmin import CatalogAdmin
from .publicationadmin import PublicationAdmin
from .typeadmin import TypeAdmin
from ..models import Type, Catalog, Publication

admin.site.register(Type, TypeAdmin)
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Publication, PublicationAdmin)
