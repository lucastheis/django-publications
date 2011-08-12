__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.template import Library, Node, Context
from django.template.loader import get_template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from publications.models import Publication
from re import sub

register = Library()

GREEK_LETTERS = \
	'[Aa]lpha|[Bb]eta|[Gg]amma|[Dd]elta|[Ee]psilon|[Zz]eta|' + \
	'[Ee]ta|[Tt]heta|[Ll]ambda|[Mm]u|[Nn]u|[Pp]i|[Ss]igma|[Tt]au|' + \
	'[Pp]hi|[Pp]si|[Cc]hi|[Oo]mega|[Rr]ho|[Xx]i|[Kk]appa'

def get_publication(id):
	pbl = Publication.objects.filter(pk=int(id))

	if len(pbl) < 1:
		return ''
	return get_template('publications/publication.html').render(
		Context({'publication': pbl[0]}))

def tex_parse(string):
	def tex_replace(match):
		return \
			sub(r'\^(\w)', r'<sup>\1</sup>',
			sub(r'\^\{(.*?)\}', r'<sup>\1</sup>',
			sub(r'\_(\w)', r'<sub>\1</sub>',
			sub(r'\_\{(.*?)\}', r'<sub>\1</sub>',
			sub(r'\\(' + GREEK_LETTERS + ')', r'&\1;', match.group(1))))))
	return mark_safe(sub(r'\$([^\$]*)\$', tex_replace, escape(string)))

register.simple_tag(get_publication)
register.filter('tex_parse', tex_parse)
