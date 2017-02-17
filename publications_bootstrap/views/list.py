__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.shortcuts import render

from ..models import List
from ..utils import populate


def list(request, title):
    try:
        publication_list = List.objects.get(title__iexact=title)

        publications = publication_list.publication_set.all()
        publications = publications.order_by('-year', '-month', '-id')

        if 'plain' in request.GET:
            return render(request, 'publications-bootstrap/export/publications-bootstrap.txt', {
                'publications-bootstrap': publications
            }, content_type='text/plain; charset=UTF-8')

        if 'bibtex' in request.GET:
            return render(request, 'publications-bootstrap/export/publications-bootstrap.bib', {
                'publications-bootstrap': publications
            }, content_type='text/x-bibtex; charset=UTF-8')

        if 'mods' in request.GET:
            return render(request, 'publications-bootstrap/export/publications-bootstrap.mods', {
                'publications-bootstrap': publications
            }, content_type='application/xml; charset=UTF-8')

        if 'ris' in request.GET:
            return render(request, 'publications-bootstrap/export/publications-bootstrap.ris', {
                'publications-bootstrap': publications
            }, content_type='application/x-research-info-systems; charset=UTF-8')

        if 'rss' in request.GET:
            return render(request, 'publications-bootstrap/export/publications-bootstrap.rss', {
                'url': 'http://' + request.get_host() + request.path,
                'publications-bootstrap': publications
            }, content_type='application/rss+xml; charset=UTF-8')

        # load custom links and files
        populate(publications)

        return render(request, 'publications-bootstrap/pages/list.html', {
            'publications-bootstrap': publications,
            'title': "publications-bootstrap for list {}".format(title)
        })
    except List.DoesNotExist:
        return render(request, 'publications-bootstrap/base.html', {
            'error': True,
            'alert': {
                'message': "There is no publication list with this name: {}".format(title)},
        }, status=404)
