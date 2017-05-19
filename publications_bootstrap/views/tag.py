# -*- coding: utf-8 -*-

from django.shortcuts import render

from ..models import Publication
from ..utils import populate


def by_tag(request, tag):
    tag = tag.lower().replace(' ', '+')
    candidates = Publication.objects.filter(tags__icontains=tag.split('+')[0], external=False)
    publications = []

    for i, publication in enumerate(candidates):
        if tag in [k[1] for k in publication.tags_escaped()]:
            publications.append(publication)

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

    # load custom links and files
    populate(publications)

    return render(request, 'publications_bootstrap/pages/tag.html', {
        'publications': publications,
        'tag': tag.replace('+', ' '),
        'title': "publications for tag {}".format(tag.replace('+', ' '))})
