__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication

def id(request, publication_id):
	publications = Publication.objects.filter(pk=publication_id)

	if 'ascii' in request.GET:
		return render_to_response('publications/ascii.txt', {
				'publications': publications
			}, context_instance=RequestContext(request), mimetype='text/plain; charset=UTF-8')
	elif 'bibtex' in request.GET:
		return render_to_response('publications/publications.bib', {
				'publications': publications
			}, context_instance=RequestContext(request), mimetype='text/plain; charset=UTF-8')
	else:
		return render_to_response('publications/id.html', {
				'publications': publications
			}, context_instance=RequestContext(request))
