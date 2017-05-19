# -*- coding: utf-8 -*-

from django.contrib import admin

from .listadmin import ListAdmin
from .publicationadmin import PublicationAdmin
from .typeadmin import TypeAdmin
from ..models import Type, Catalog, Publication

admin.site.register(Type, TypeAdmin)
admin.site.register(Catalog, ListAdmin)
admin.site.register(Publication, PublicationAdmin)
