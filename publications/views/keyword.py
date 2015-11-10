__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication, CustomFile, CustomLink
from publications.utils import populate

def keyword(request, keyword):
	publications = Publication.objects.filter(keywords__slug__in=[keyword])

	if 'plain' in request.GET:
		return render_to_response('publications/publications.txt', {
				'publications': publications
			}, context_instance=RequestContext(request), content_type='text/plain; charset=UTF-8')

	if 'bibtex' in request.GET:
		return render_to_response('publications/publications.bib', {
				'publications': publications
			}, context_instance=RequestContext(request), content_type='text/x-bibtex; charset=UTF-8')

	if 'mods' in request.GET:
		return render_to_response('publications/publications.mods', {
				'publications': publications
			}, context_instance=RequestContext(request), content_type='application/xml; charset=UTF-8')

	if 'ris' in request.GET:
		return render_to_response('publications/publications.ris', {
				'publications': publications
			}, context_instance=RequestContext(request), content_type='application/x-research-info-systems; charset=UTF-8')

	# load custom links and files
	populate(publications)

	return render_to_response('publications/keyword.html', {
			'publications': publications,
			'keyword': keyword,
		}, context_instance=RequestContext(request))
