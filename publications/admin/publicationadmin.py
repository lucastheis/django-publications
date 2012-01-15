__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.contrib import admin

class PublicationAdmin(admin.ModelAdmin):
	list_display = ('type', 'first_author', 'title', 'type', 'year', 'journal_or_book_title')
	list_display_links = ('title',)
	change_list_template = 'admin/publications/change_list.html'
	search_fields = ('title', 'journal', 'authors', 'keywords', 'year')
	fieldsets = (
		(None, {'fields': 
			('type', 'title', 'authors', 'year', 'month')}),
		(None, {'fields': 
			('journal', 'book_title', 'publisher', 'volume', 'number', 'pages')}),
		(None, {'fields': 
			('keywords', 'url', 'code', 'pdf', 'doi', 'note', 'external')}),
		(None, {'fields':
			('abstract',)}),
	)
