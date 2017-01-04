# -*- coding: utf-8 -*-

__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__authors__ = ['Lucas Theis <lucas@theis.io>', 'Marc Bourqui']
__docformat__ = 'epytext'

from django.http import Http404
from django.shortcuts import render

from publications.models import List
from publications.utils import populate


def list(request, list):
    list = List.objects.filter(list__iexact=list)

    if not list:
        raise Http404

    list = list[0]
    publications = list.publication_set.all()
    publications = publications.order_by('-year', '-month', '-id')

    if 'plain' in request.GET:
        return render(request, 'publications/export/publications.txt', {
            'publications': publications
        }, content_type='text/plain; charset=UTF-8')

    if 'bibtex' in request.GET:
        return render(request, 'publications/export/publications.bib', {
            'publications': publications
        }, content_type='text/x-bibtex; charset=UTF-8')

    if 'mods' in request.GET:
        return render(request, 'publications/export/publications.mods', {
            'publications': publications
        }, content_type='application/xml; charset=UTF-8')

    if 'ris' in request.GET:
        return render(request, 'publications/export/publications.ris', {
            'publications': publications
        }, content_type='application/x-research-info-systems; charset=UTF-8')

    if 'rss' in request.GET:
        return render(request, 'publications/export/publications.rss', {
            'url': 'http://' + request.get_host() + request.path,
            'publications': publications
        }, content_type='application/rss+xml; charset=UTF-8')

    # load custom links and files
    populate(publications)

    return render(request, 'publications/pages/list.html', {
        'list': list,
        'publications': publications,
        'title': "publications for list {}".format(list)
    })
