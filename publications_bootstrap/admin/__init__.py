# -*- coding: utf-8 -*-

from django.contrib import admin

from .listadmin import ListAdmin
from .orderedmodeladmin import OrderedModelAdmin
from .publicationadmin import PublicationAdmin
from .typeadmin import TypeAdmin
from ..models import Type, List, Publication

admin.site.register(Type, TypeAdmin)
admin.site.register(List, ListAdmin)
admin.site.register(Publication, PublicationAdmin)
