# -*- coding: utf-8 -*-

from django.shortcuts import render

from ..models import Publication
from ..utils import populate


def by_year(request, year=None):
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
        return render(request, 'publications_bootstrap/export/publications.txt',
                      {'publications': sum([y[1] for y in years], [])},
                      content_type='text/plain; charset=UTF-8')

    if 'bibtex' in request.GET:
        return render(request, 'publications_bootstrap/export/publications.bib',
                      {'publications': sum([y[1] for y in years], [])},
                      content_type='text/x-bibtex; charset=UTF-8')

    if 'mods' in request.GET:
        return render(request, 'publications_bootstrap/export/publications.mods',
                      {'publications': sum([y[1] for y in years], [])},
                      content_type='application/xml; charset=UTF-8')

    if 'ris' in request.GET:
        return render(request, 'publications_bootstrap/export/publications.ris',
                      {'publications': sum([y[1] for y in years], [])},
                      content_type='application/x-research-info-systems; charset=UTF-8')

    if 'rss' in request.GET:
        return render(request, 'publications_bootstrap/export/publications.rss',
                      {'url': 'http://' + request.get_host() + request.path,
                       'publications': sum([y[1] for y in years], [])},
                      content_type='application/rss+xml; charset=UTF-8')

    # load custom links and files
    populate(publications)

    return render(request, 'publications_bootstrap/pages/years.html', {'publications': publications,
                                                                       'years': years})
