# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.forms import widgets


class PagesWidget(widgets.MultiWidget):
    def __init__(self, *args, **kwargs):
        attrs = {'style': 'width: 40px; text-align: center;'}
        forms.widgets.MultiWidget.__init__(self, [widgets.TextInput(attrs), widgets.TextInput(attrs)], *args, **kwargs)

    def format_output(self, rendered_widgets):
        to = ' <span style="vertical-align: middle;">to</span> '
        return rendered_widgets[0] + to + rendered_widgets[1]

    def decompress(self, value):
        if value:
            values = value.split('-')
            if len(values) > 1:
                return values
            if len(values) > 0:
                return [values[0], values[0]]
        return [None, None]


class PagesForm(forms.MultiValueField):
    widget = PagesWidget

    def __init__(self, *args, **kwargs):
        forms.MultiValueField.__init__(self, [forms.CharField(), forms.CharField()], *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[0] and data_list[1]:
                if data_list[0] == data_list[1]:
                    return str(data_list[0])
                return str(data_list[0]) + '-' + str(data_list[1])
            if data_list[0]:
                return str(data_list[0])
            if data_list[1]:
                return str(data_list[1])
        return ''


class PagesField(models.Field):
    def formfield(self, **kwargs):
        kwargs['form_class'] = PagesForm
        return models.Field.formfield(self, **kwargs)

    def get_internal_type(self):
        return 'CharField'


try:
    from south.modelsinspector import add_introspection_rules

    add_introspection_rules([], ["^publications_bootstrap\.fields\.PagesField"])
except:
    pass


class NullCharField(models.CharField):
    """
    Allows to apply the unique condition even if no value is set.
    Adapted from U{http://stackoverflow.com/a/33525694}
    U{Issue #4136<https://code.djangoproject.com/ticket/4136>} fixed in U{PR #6624<
    https://github.com/django/django/pull/6624>}
    Fixed in U{Django 1.11<https://docs.djangoproject.com/en/dev/releases/1.11/#miscellaneous>}
    """
    description = "CharField that stores NULL instead of empty strings"

    def get_db_prep_value(self, value, connection=None, prepared=False):
        value = super(NullCharField, self).get_db_prep_value(value, connection, prepared)
        if value == "":
            return None
        else:
            return value
