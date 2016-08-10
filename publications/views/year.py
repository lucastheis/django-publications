__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render
from publications.models import Publication, CustomLink, CustomFile
from publications.utils import populate

def year(request, year=None):
	years = []
	publications = Publication.objects.select_related()
	if year:
		publications = publications.filter(year=year, external=False)
	else:
		publications = publications.filter(external=False)
	publications = publications.order_by('-year', '-month', '-id')

	for publication in publications:
		if publication.type.hidden:
			continue
		if not years or (years[-1][0] != publication.year):
			years.append((publication.year, []))
		years[-1][1].append(publication)

	if 'plain' in request.GET:
		return render(request, 'publications/publications.txt', {
				'publications': sum([y[1] for y in years], [])
			}, content_type='text/plain; charset=UTF-8')

	if 'bibtex' in request.GET:
		return render(request, 'publications/publications.bib', {
				'publications': sum([y[1] for y in years], [])
			}, content_type='text/x-bibtex; charset=UTF-8')

	if 'mods' in request.GET:
		return render(request, 'publications/publications.mods', {
				'publications': sum([y[1] for y in years], [])
			}, content_type='application/xml; charset=UTF-8')

	if 'ris' in request.GET:
		return render(request, 'publications/publications.ris', {
				'publications': sum([y[1] for y in years], [])
			}, content_type='application/x-research-info-systems; charset=UTF-8')

	if 'rss' in request.GET:
		return render(request, 'publications/publications.rss', {
				'url': 'http://' + request.get_host() + request.path,
				'publications': sum([y[1] for y in years], [])
			}, content_type='application/rss+xml; charset=UTF-8')

	# load custom links and files
	populate(publications)

	return render(request, 'publications/years.html', {
			'years': years
		})
