# -*- coding: utf-8 -*-

from django.test import TestCase
from publications.models import Publication, Type

class Tests(TestCase):
	fixtures = ['initial_data.json', 'test_data.json']

	def test_authors(self):
		publication = Publication.objects.create(
			type=Type.objects.get(pk=1),
			authors=u'Jörn-Philipp Lies and Ralf M. Häfner and M. Bethge',
			title=u'Slowness and sparseness have diverging effects on complex cell learning',
			year=2014,
			journal=u'PLoS Computational Biology',
			external=0)

		self.assertEqual(len(publication.authors_list), 3)
		self.assertEqual(publication.authors_list[0], 'J.-P. Lies')
