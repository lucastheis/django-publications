# -*- coding: utf-8 -*-

from .models import PublicationLink, PublicationFile


def populate(publications):
    """
    Load publication links and files from database and attach to publications
    """

    publication_links = PublicationLink.objects.filter(publication__in=publications)
    publication_files = PublicationFile.objects.filter(publication__in=publications)

    publications_ = {}
    for publication in publications:
        publication.links = []
        publication.files = []
        publications_[publication.id] = publication

    for link in publication_links:
        publications_[link.publication_id].links.append(link)
    for file in publication_files:
        publications_[file.publication_id].files.append(file)
