__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render_to_response
from django.template import RequestContext
from publications.models import Type, Publication
from string import capwords, replace, split

def person(request, name):
	author = capwords(replace(name, '+', ' '))
	author = author.replace(' Von ', ' von ').replace(' Van ', ' van ')
	author = author.replace(' Der ', ' der ')

	# take care of dashes
	off = author.find('-')
	while off > 0:
		off += 1
		if off <= len(author):
			author = author[:off] + author[off].upper() + author[off + 1:]
		off = author.find('-', off)

	# split into forename, middlenames and surname
	names = split(replace(name, ' ', '+'), '+')

	# find publications of this author
	publications = []
	types = Type.objects.all()
	types_dict = {}

	for t in types:
		types_dict[t] = []

	if len(names) > 1:
		for publication in Publication.objects.filter(authors__icontains=names[-1]):
			if names[0][0].lower() + '. ' + names[-1].lower() in publication.authors_list_simple:
				publications.append(publication)
				types_dict[publication.type].append(publication)

	elif len(names) > 0:
		for publication in Publication.objects.filter(authors__icontains=names[-1]):
			if names[-1].lower() in publication.authors_list_simple:
				publications.append(publication)
				types_dict[publication.type].append(publication)

	# remove empty types
	for t in types:
		if not types_dict[t]:
			types = types.exclude(pk=t.pk)

	# attach publications to types
	for t in types:
		t.publications = types_dict[t]

	if 'ascii' in request.GET:
		return render_to_response('publications/publications.txt', {
				'publications': publications
			}, context_instance=RequestContext(request), mimetype='text/plain; charset=UTF-8')

	elif 'bibtex' in request.GET:
		return render_to_response('publications/publications.bib', {
				'publications': publications
			}, context_instance=RequestContext(request), mimetype='text/x-bibtex; charset=UTF-8')

	elif 'rss' in request.GET:
		return render_to_response('publications/publications.rss', {
				'url': 'http://' + request.META['HTTP_HOST'] + request.path,
				'author': author,
				'publications': publications
			}, context_instance=RequestContext(request), mimetype='application/rss+xml; charset=UTF-8')

	else:
		return render_to_response('publications/person.html', {
				'publications': publications,
				'types': types,
				'author': author
			}, context_instance=RequestContext(request))
