# -*- coding: utf-8 -*-

from .orderedmodeladmin import OrderedModelAdmin


class TypeAdmin(OrderedModelAdmin):
    list_display = ('title', 'description', 'hidden', 'move_up_down_links')
