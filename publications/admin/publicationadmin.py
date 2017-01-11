__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__authors__ = ['Lucas Theis <lucas@theis.io>', 'Marc Bourqui']
__docformat__ = 'epytext'

import django
from distutils.version import StrictVersion
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from .. import admin_views
from ..models import Publication, CustomLink, CustomFile


class CustomLinkInline(admin.StackedInline):
    model = CustomLink
    extra = 1
    max_num = 5


class CustomFileInline(admin.StackedInline):
    model = CustomFile
    extra = 1
    max_num = 5


class PublicationAdminForm(forms.ModelForm):
    class Meta:
        model = Publication
        if StrictVersion(django.get_version()) >= StrictVersion('1.7.0'):
            # Fix for Django<1.7
            fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PublicationAdminForm, self).__init__(*args, **kwargs)

        # give (usually) numeric fields appearance of IntegerField
        for field in ['volume', 'number', 'chapter', 'section']:
            self.fields[field].widget.attrs['class'] = 'vIntegerField'


class PublicationAdmin(admin.ModelAdmin):
    form = PublicationAdminForm
    list_display = ('type', 'first_author', 'title', 'type', 'year', 'journal_or_book_title')
    list_display_links = ('title',)
    list_filter = ('year', 'journal', 'status', 'lists',)
    change_list_template = 'admin/publications/publication_change_list.html'
    search_fields = ('title', 'journal', 'book_title', 'authors', 'keywords', 'year',
                     'institution', 'school', 'organization',)
    actions = ['set_status_draft', 'set_status_submitted', 'set_status_accepted',
               'set_status_published', ]
    fieldsets = (
        (None, {
            'fields': (
                'type', 'title', 'authors', 'year', 'month', 'external',)}),
        ('Publishing', {
            'fields': (
                'journal', 'book_title', 'publisher', 'editor', 'edition', 'institution',
                'school', 'organization', 'location', 'country', 'volume', 'number',
                'chapter', 'section', 'pages', 'url', 'doi', 'isbn', 'status',)}),
        ('References', {
            'fields': (
                'citekey', 'keywords', 'code',)}),
        (None, {
            'fields': (
                'abstract', 'note',)}),
        ('Media', {
            'classes': ('collapse',),
            'fields': (
                'pdf', 'image', 'thumbnail')}),
        (None, {
            'fields': (
                'lists',)}),
    )
    inlines = [CustomLinkInline, CustomFileInline]

    def get_urls(self):
        return [
                   url(r'^import_bibtex/$', admin_views.import_bibtex,
                       name='publications_publication_import_bibtex'),
               ] + super(PublicationAdmin, self).get_urls()

    def set_status_draft(self, request, queryset):
        rows_updated = queryset.update(status=Publication.DRAFT)
        if rows_updated == 1:
            message_bit = "1 publication was"
        else:
            message_bit = "%s publications were" % rows_updated
        self.message_user(request, "%s successfully marked as draft." % message_bit)

    set_status_draft.short_description = _("Mark selected %(verbose_name_plural)s as drafts")

    def set_status_submitted(self, request, queryset):
        rows_updated = queryset.update(status=Publication.SUBMITTED)
        if rows_updated == 1:
            message_bit = "1 publication was"
        else:
            message_bit = "%s publications were" % rows_updated
        self.message_user(request, "%s successfully marked as submitted." % message_bit)

    set_status_submitted.short_description = _("Mark selected %(verbose_name_plural)s as "
                                               "submitted")

    def set_status_accepted(self, request, queryset):
        rows_updated = queryset.update(status=Publication.ACCEPTED)
        if rows_updated == 1:
            message_bit = "1 publication was"
        else:
            message_bit = "%s publications were" % rows_updated
        self.message_user(request, "%s successfully marked as accepted." % message_bit)

    set_status_accepted.short_description = _("Mark selected %(verbose_name_plural)s as accepted")

    def set_status_published(self, request, queryset):
        rows_updated = queryset.update(status=Publication.DRAFT)
        if rows_updated == 1:
            message_bit = "1 publication was"
        else:
            message_bit = "%s publications were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)

    set_status_published.short_description = _("Mark selected %(verbose_name_plural)s as "
                                               "published")
