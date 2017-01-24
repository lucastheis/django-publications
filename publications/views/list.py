__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render

from publications.models import List
from publications.utils import populate


def list(request, title):
    try:
        publication_list = List.objects.get(title__iexact=title)

        publications = publication_list.publication_set.all()
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
            'publications': publications,
            'title': "publications for list {}".format(title)
        })
    except List.DoesNotExist:
        return render(request, 'publications/pages/base.html', {
            'error': True,
            'alert': {
                'message': "There is no publication list with this name: {}".format(title)},
        })
