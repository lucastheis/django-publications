# -*- coding: utf-8 -*-

from django.contrib import admin

from ..models import Publication


class CatalogAdmin(admin.ModelAdmin):
    def publications_count(self, instance):
        count = instance.publications.count()
        if count == 1:
            name = Publication._meta.verbose_name
        else:
            name = Publication._meta.verbose_name_plural
        return "{} {}".format(count, name)

    publications_count.short_description = 'Publications'

    list_display = ('title', 'description', 'publications_count')
