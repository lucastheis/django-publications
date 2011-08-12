__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication

def year(request, year=None):
	years = []
	if year:
		publications = Publication.objects.filter(year=year, external=False)
	else:
		publications = Publication.objects.filter(external=False)
	publications = publications.order_by('-year', '-month', '-id')

	for publication in publications:
		if publication.type.hidden:
			continue
		if not years or (years[-1][0] != publication.year):
			years.append((publication.year, []))
		years[-1][1].append(publication)

	if 'bibtex' in request.GET:
		return render_to_response('publications/publications.bib', {
				'publications': sum([y[1] for y in years], [])
			}, context_instance=RequestContext(request), mimetype='text/plain; charset=UTF-8')
	else:
		return render_to_response('publications/years.html', {
				'years': years
			}, context_instance=RequestContext(request))
