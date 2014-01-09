__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

import os

from django.template import Library, Node, Context, RequestContext
from django.template.loader import get_template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from publications.models import Publication, List
from re import sub
from string import replace

register = Library()

GREEK_LETTERS = \
	'[Aa]lpha|[Bb]eta|[Gg]amma|[Dd]elta|[Ee]psilon|[Zz]eta|' + \
	'[Ee]ta|[Tt]heta|[Ll]ambda|[Mm]u|[Nn]u|[Pp]i|[Ss]igma|[Tt]au|' + \
	'[Pp]hi|[Pp]si|[Cc]hi|[Oo]mega|[Rr]ho|[Xx]i|[Kk]appa'

def get_publication(context, id):
	pbl = Publication.objects.filter(pk=int(id))

	if len(pbl) < 1:
		return ''

	pbl[0].links = pbl[0].customlink_set.all()
	pbl[0].files = pbl[0].customfile_set.all()

	return get_template('publications/publication.html').render(
		RequestContext(context['request'], {'publication': pbl[0]}))


def get_publication_list(context, list, template='publications/publications.html'):
	list = List.objects.filter(list__iexact=list)

	if not list:
		return ''

	list = list[0]
	publications = list.publication_set.all()
	publications = publications.order_by('-year', '-month', '-id')

	if not publications:
		return ''

	for publication in publications:
		publication.links = publication.customlink_set.all()
		publication.files = publication.customfile_set.all()

	return get_template(template).render(
			RequestContext(context['request'], {'list': list, 'publications': publications}))


def tex_parse(string):
	string = replace(replace(string, '{', ''), '}', '')
	def tex_replace(match):
		return \
			sub(r'\^(\w)', r'<sup>\1</sup>',
			sub(r'\^\{(.*?)\}', r'<sup>\1</sup>',
			sub(r'\_(\w)', r'<sub>\1</sub>',
			sub(r'\_\{(.*?)\}', r'<sub>\1</sub>',
			sub(r'\\(' + GREEK_LETTERS + ')', r'&\1;', match.group(1))))))
	return mark_safe(sub(r'\$([^\$]*)\$', tex_replace, escape(string)))

register.simple_tag(get_publication, takes_context=True)
register.simple_tag(get_publication_list, takes_context=True)
register.filter('tex_parse', tex_parse)
