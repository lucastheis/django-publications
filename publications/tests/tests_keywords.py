# -*- coding: utf-8 -*-

from django.test import TestCase
from publications.models import Publication, Type


class KeywordsTestCase(TestCase):
    fixtures = ['initial_data.json', 'test_data.json']
    urls = 'publications.tests.urls'

    def test_keywords_as_args(self):
        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'Jörn-Philipp Lies and Ralf M. Häfner and M. Bethge',
            title=u'Slowness and sparseness have diverging effects on complex cell learning',
            year=2014,
            journal=u'PLoS Computational Biology',
            external=0,
            keywords='foo, bar, baz bins, other'
        )
        publication.clean()
        publication.save()
        self.assertEqual(publication.keywords.count(), 4)

    def test_keywords_nullable(self):
        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'Jörn-Philipp Lies and Ralf M. Häfner and M. Bethge',
            title=u'Slowness and sparseness have diverging effects on complex cell learning',
            year=2014,
            journal=u'PLoS Computational Biology',
            external=0,
        )
        publication.clean()
        publication.save()
        self.assertEqual(publication.keywords.count(), 0)
