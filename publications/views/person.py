# -*- coding: utf-8 -*-

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

	# construct a liberal query
	surname = names[-1]
	surname = replace(surname, u'ä', u'%%')
	surname = replace(surname, u'ae', u'%%')
	surname = replace(surname, u'ö', u'%%')
	surname = replace(surname, u'oe', u'%%')
	surname = replace(surname, u'ü', u'%%')
	surname = replace(surname, u'ue', u'%%')
	surname = replace(surname, u'ß', u'%%')
	surname = replace(surname, u'ss', u'%%')
	query_str = u'SELECT * FROM {table} WHERE lower(authors) LIKE lower(\'%%{surname}%%\') ORDER BY year DESC, month DESC, id DESC'
	query = Publication.objects.raw(
		query_str.format(table=Publication._meta.db_table, surname=surname))

	# further filter results
	if len(names) > 1:
		name_simple = Publication.simplify_name(names[0][0] + '. ' + names[-1])
		for publication in query:
			if name_simple in publication.authors_list_simple:
				publications.append(publication)
				types_dict[publication.type].append(publication)

	elif len(names) > 0:
		for publication in query:
			if Publication.simplify_name(names[-1].lower()) in publication.authors_list_simple:
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
		for publication in publications:
			publication.links = publication.customlink_set.all()
			publication.files = publication.customfile_set.all()

		return render_to_response('publications/person.html', {
				'publications': publications,
				'types': types,
				'author': author
			}, context_instance=RequestContext(request))
