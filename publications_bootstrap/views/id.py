# -*- coding: utf-8 -*-

from django.shortcuts import render

from ..models import Publication


def by_id(request, publication_id):
    try:
        publication = Publication.objects.get(pk=publication_id)

        if 'plain' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.txt', {'publications': [publication]},
                          content_type='text/plain; charset=UTF-8')

        if 'bibtex' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.bib', {'publications': [publication]},
                          content_type='text/x-bibtex; charset=UTF-8')

        if 'mods' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.mods', {'publications': [publication]},
                          content_type='application/xml; charset=UTF-8')

        if 'ris' in request.GET:
            return render(request, 'publications_bootstrap/export/publications.ris', {'publications': [publication]},
                          content_type='application/x-research-info-systems; charset=UTF-8')

        publication.links = publication.publicationlink_set.all()
        publication.files = publication.publicationfile_set.all()

        return render(request, 'publications_bootstrap/pages/id.html', {'publication': publication,
                                                                        'title': publication.type})
    except Publication.DoesNotExist:
        return render(request, 'publications_bootstrap/base.html', {
            'error': True,
            'alert': {'message': "There is no publication with this id: {}".format(publication_id)}},
                      status=404)
