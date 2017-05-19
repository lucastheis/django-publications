# -*- coding: utf-8 -*-

from django.contrib import admin


class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
