# -*- coding: utf-8 -*-

from django.shortcuts import render

from ..models import Catalog
from ..utils import populate


def for_catalog(request, title):
    try:
        catalog = Catalog.objects.get(title__iexact=title)

        publications = catalog.publications.all()
        publications = publications.order_by('-year', '-month', '-id')

        if 'plain' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.txt', {'publications': publications},
                          content_type='text/plain; charset=UTF-8')

        if 'bibtex' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.bib', {'publications': publications},
                          content_type='text/x-bibtex; charset=UTF-8')

        if 'mods' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.mods', {'publications': publications},
                          content_type='application/xml; charset=UTF-8')

        if 'ris' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.ris', {'publications': publications},
                          content_type='application/x-research-info-systems; charset=UTF-8')

        if 'rss' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.rss', {
                'url': 'http://' + request.get_host() + request.path,
                'publications': publications
            }, content_type='application/rss+xml; charset=UTF-8')

        # load custom links and files
        populate(publications)

        return render(request, 'publications_bootstrap/pages/catalog.html', {
            'publications': publications,
            'title': "publications for catalog {}".format(title)})

    except Catalog.DoesNotExist:
        return render(request, 'publications_bootstrap/base.html', {
            'error': True,
            'alert': {'message': "There is no publication catalog with this name: {}".format(title)}},
                      status=404)
