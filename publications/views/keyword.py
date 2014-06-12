__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication

def keyword(request, keyword):
	keyword = keyword.lower().replace(' ', '+')
	candidates = Publication.objects.filter(keywords__icontains=keyword.split('+')[0], external=False)
	publications = []

	for i, publication in enumerate(candidates):
		if keyword in [k[1] for k in publication.keywords_escaped()]:
			publications.append(publication)

	if 'ascii' in request.GET:
		return render_to_response('publications/publications.txt', {
				'publications': publications
			}, context_instance=RequestContext(request), content_type='text/plain; charset=UTF-8')

	elif 'bibtex' in request.GET:
		return render_to_response('publications/publications.bib', {
				'publications': publications
			}, context_instance=RequestContext(request), content_type='text/x-bibtex; charset=UTF-8')

	else:
		for publication in publications:
			publication.links = publication.customlink_set.all()
			publication.files = publication.customfile_set.all()

		return render_to_response('publications/keyword.html', {
				'publications': publications,
				'keyword': keyword.replace('+', ' ')
			}, context_instance=RequestContext(request))
