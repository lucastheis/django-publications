__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication
from string import replace, split

def keyword(request, keyword):
	keyword = replace(keyword.lower(), ' ', '+')
	candidates = Publication.objects.filter(keywords__icontains=split(keyword, '+')[0], external=False)
	publications = []

	for i, publication in enumerate(candidates):
		if keyword in [k[1] for k in publication.keywords_escaped()]:
			publications.append(publication)

	if 'bibtex' in request.GET:
		return render_to_response('publications/publications.bib', {
				'publications': publications
			}, context_instance=RequestContext(request), mimetype='text/plain; charset=UTF-8')
	else:
		return render_to_response('publications/keyword.html', {
				'publications': publications,
				'keyword': replace(keyword, '+', ' ')
			}, context_instance=RequestContext(request))
