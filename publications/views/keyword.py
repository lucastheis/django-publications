__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication, CustomFile, CustomLink

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
		customlinks = CustomLink.objects.filter(publication__in=publications)
		customfiles = CustomFile.objects.filter(publication__in=publications)

		publications_ = {}
		for publication in publications:
			publication.links = []
			publication.files = []
			publications_[publication.id] = publication

		for link in customlinks:
			publications_[link.publication_id].links.append(link)
		for file in customfiles:
			publications_[file.publication_id].files.append(file)

		return render_to_response('publications/keyword.html', {
				'publications': publications,
				'keyword': keyword.replace('+', ' ')
			}, context_instance=RequestContext(request))
