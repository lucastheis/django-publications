__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.db import models
from publications.models.orderedmodel import OrderedModel

class Type(OrderedModel):
	class Meta:
		ordering = ('order',)
		app_label = 'publications'
		verbose_name_plural = '  Types'

	type = models.CharField(max_length=128)
	description = models.CharField(max_length=128)
	bibtex_types = models.CharField(max_length=256, default='article',
			verbose_name='BibTex types',
			help_text='Possible BibTex types, separated by comma.')
	hidden = models.BooleanField(default=False,
		help_text='Hide publications from main view.')

	def __unicode__(self):
		return self.type


	def __str__(self):
		return self.type


	def __init__(self, *args, **kwargs):
		OrderedModel.__init__(self, *args, **kwargs)

		self.bibtex_types = self.bibtex_types.replace('@', '')
		self.bibtex_types = self.bibtex_types.replace(';', ',')
		self.bibtex_types = self.bibtex_types.replace('and', ',')
		self.bibtex_type_list = [s.strip().lower()
			for s in self.bibtex_types.split(',')]
		self.bibtex_types = ', '.join(self.bibtex_type_list)
		self.bibtex_type = self.bibtex_type_list[0]


	def ris_type(self):
		# convert bibtex type to RIS type
		bibtex2ris = {
				'article': 'JOUR',
				'book': 'BOOK',
				'booklet': 'PAMP',
				'inbook': 'CHAP',
				'conference': 'CHAP',
				'inproceedings': 'CHAP',
				'incollection': 'CHAP',
				'manual': 'BOOK',
				'masterthesis': 'THES',
				'phdthesis': 'THES',
				'misc': 'GEN',
				'proceedings': 'CONF',
				'techreport': 'RPRT',
				'unpublished': 'UNPB',
				'patent': 'PAT',
				'abstract': 'ABST',
			}
		return bibtex2ris.get(self.bibtex_type, 'GEN')



	def mods_genre(self):
		"""
		Guesses an appropriate MODS XML genre type.
		"""

		type2genre = {
				'conference': 'conference publication',
				'book chapter': 'bibliography',
				'unpublished': 'article'
			}
		tp = str(self.type).lower()
		return type2genre.get(tp, tp)
