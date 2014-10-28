__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from publications.models import Publication

def unapi(request):
	"""
	This view implements unAPI 1.0 (see http://unapi.info).
	"""

	id = request.GET.get('id')
	format = request.GET.get('format')

	if format is not None:
		try:
			publications = Publication.objects.filter(pk=int(id))
			
			if not publications:
				raise ValueError

		except ValueError:
			# invalid id
			return HttpResponse('\n'.join([
				'<?xml version="1.0" encoding="UTF-8"?>',
				'<error>Invalid ID.</error>']),
				content_type="application/xml",
				status=404)

		if format == 'bibtex':
			# return BibTex encoded publication
			return render_to_response('publications/publication.bib', {
					'publication': publications[0]
				},
				context_instance=RequestContext(request),
				content_type='text/x-bibtex; charset=UTF-8')

		if format == 'mods':
			# return MODS encoded publication
			return render_to_response('publications/publications.mods', {
					'publications': publications
				},
				context_instance=RequestContext(request),
				content_type='application/xml; charset=UTF-8')

		if format == 'ris':
			# return MODS encoded publication
			return render_to_response('publications/publications.ris', {
					'publications': publications
				},
				context_instance=RequestContext(request),
				content_type='application/x-research-info-systems; charset=UTF-8')

		# invalid format
		return HttpResponse('\n'.join([
			'<?xml version="1.0" encoding="UTF-8"?>',
			'<error>Invalid format.</error>']),
			content_type="application/xml",
			status=406)

	if id is not None:
		return HttpResponse('\n'.join([
			'<?xml version="1.0" encoding="UTF-8"?>',
			'<formats id="{0}">'.format(id),
			'<format name="bibtex" type="text/x-bibtex" />',
			'<format name="ris" type="application/x-research-info-systems" />',
			'<format name="mods" type="application/xml" />',
			'</formats>']), content_type="application/xml")

	return HttpResponse('\n'.join([
		'<?xml version="1.0" encoding="UTF-8"?>',
		'<formats>',
		'<format name="bibtex" type="text/x-bibtex" />',
		'<format name="ris" type="application/x-research-info-systems" />',
		'<format name="mods" type="application/xml" />',
		'</formats>']), content_type="application/xml")
