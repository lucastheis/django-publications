# -*- coding: utf-8 -*-

__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

import os

from django.db import models
from django.utils.http import urlquote_plus
from django.conf import settings
from publications.fields import PagesField
from publications.models import Type, List
from string import ascii_uppercase

if 'django.contrib.sites' in settings.INSTALLED_APPS:
	from django.contrib.sites.models import Site

class Publication(models.Model):
	"""
	Model representing a publication.
	"""

	class Meta:
		app_label = 'publications'
		ordering = ['-year', '-month', '-id']
		verbose_name_plural = ' Publications'

	# names shown in admin area
	MONTH_CHOICES = (
			(1, 'January'),
			(2, 'February'),
			(3, 'March'),
			(4, 'April'),
			(5, 'May'),
			(6, 'June'),
			(7, 'July'),
			(8, 'August'),
			(9, 'September'),
			(10, 'October'),
			(11, 'November'),
			(12, 'December')
		)

	# abbreviations used in BibTex
	MONTH_BIBTEX = {
			1: 'Jan',
			2: 'Feb',
			3: 'Mar',
			4: 'Apr',
			5: 'May',
			6: 'Jun',
			7: 'Jul',
			8: 'Aug',
			9: 'Sep',
			10: 'Oct',
			11: 'Nov',
			12: 'Dec'
		}

	type = models.ForeignKey(Type, on_delete=models.CASCADE)
	citekey = models.CharField(max_length=512, blank=True, null=True,
		help_text='BibTex citation key. Leave blank if unsure.')
	title = models.CharField(max_length=512)
	authors = models.CharField(max_length=2048,
		help_text='List of authors separated by commas or <i>and</i>.')
	year = models.PositiveIntegerField()
	month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
	journal = models.CharField(max_length=256, blank=True)
	book_title = models.CharField(max_length=256, blank=True)
	publisher = models.CharField(max_length=256, blank=True)
	institution = models.CharField(max_length=256, blank=True)
	volume = models.IntegerField(blank=True, null=True)
	number = models.IntegerField(blank=True, null=True, verbose_name='Issue number')
	pages = PagesField(max_length=32, blank=True)
	note = models.CharField(max_length=256, blank=True)
	keywords = models.CharField(max_length=256, blank=True,
		help_text='List of keywords separated by commas.')
	url = models.URLField(blank=True, verbose_name='URL',
		help_text='Link to PDF or journal page.')
	code = models.URLField(blank=True,
		help_text='Link to page with code.')
	pdf = models.FileField(upload_to='publications/', verbose_name='PDF', blank=True, null=True)
	image = models.ImageField(upload_to='publications/images/', blank=True, null=True)
	thumbnail = models.ImageField(upload_to='publications/thumbnails/', blank=True, null=True)
	doi = models.CharField(max_length=128, verbose_name='DOI', blank=True)
	external = models.BooleanField(default=False,
		help_text='If publication was written in another lab, mark as external.')
	abstract = models.TextField(blank=True)
	isbn = models.CharField(max_length=32, verbose_name="ISBN", blank=True,
		help_text='Only for a book.') # A-B-C-D
	lists = models.ManyToManyField(List, blank=True)

	def __init__(self, *args, **kwargs):
		models.Model.__init__(self, *args, **kwargs)

		# post-process keywords
		self.keywords = self.keywords.replace(';', ',')
		self.keywords = self.keywords.replace(', and ', ', ')
		self.keywords = self.keywords.replace(',and ', ', ')
		self.keywords = self.keywords.replace(' and ', ', ')
		self.keywords = [s.strip().lower() for s in self.keywords.split(',')]
		self.keywords = ', '.join(self.keywords).lower()

		self._produce_author_lists()


	def _produce_author_lists(self):
		"""
		Parse authors string to create lists of authors.
		"""

		# post-process author names
		self.authors = self.authors.replace(', and ', ', ')
		self.authors = self.authors.replace(',and ', ', ')
		self.authors = self.authors.replace(' and ', ', ')
		self.authors = self.authors.replace(';', ',')

		# list of authors
		self.authors_list = [author.strip() for author in self.authors.split(',')]

		# simplified representation of author names
		self.authors_list_simple = []

		# author names represented as a tuple of given and family name
		self.authors_list_split = []

		# tests if title already ends with a punctuation mark
		self.title_ends_with_punct = self.title[-1] in ['.', '!', '?'] \
			if len(self.title) > 0 else False

		suffixes = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', "Jr.", "Sr."]
		prefixes = ['Dr.']
		prepositions = ['van', 'von', 'der', 'de', 'den']

		# further post-process author names
		for i, author in enumerate(self.authors_list):
			if author == '':
				continue

			names = author.split(' ')

			# check if last string contains initials
			if (len(names[-1]) <= 3) \
				and names[-1] not in suffixes \
				and all(c in ascii_uppercase for c in names[-1]):
				# turn "Gauss CF" into "C. F. Gauss"
				names = [c + '.' for c in names[-1]] + names[:-1]

			# number of suffixes
			num_suffixes = 0
			for name in names[::-1]:
				if name in suffixes:
					num_suffixes += 1
				else:
					break

			# abbreviate names
			for j, name in enumerate(names[:-1 - num_suffixes]):
				# don't try to abbreviate these
				if j == 0 and name in prefixes:
					continue
				if j > 0 and name in prepositions:
					continue

				if (len(name) > 2) or (len(name) and (name[-1] != '.')):
					k = name.find('-')
					if 0 < k + 1 < len(name):
						# take care of dash
						names[j] = name[0] + '.-' + name[k + 1] + '.'
					else:
						names[j] = name[0] + '.'

			if len(names):
				self.authors_list[i] = ' '.join(names)

				# create simplified/normalized representation of author name
				if len(names) > 1:
					for name in names[0].split('-'):
						name_simple = self.simplify_name(' '.join([name, names[-1]]))
						self.authors_list_simple.append(name_simple)
				else:
					self.authors_list_simple.append(self.simplify_name(names[0]))

				# number of prepositions
				num_prepositions = 0
				for name in names:
					if name in prepositions:
						num_prepositions += 1

				# splitting point
				sp = 1 + num_suffixes + num_prepositions
				self.authors_list_split.append(
					(' '.join(names[:-sp]), ' '.join(names[-sp:])))

		# list of authors in BibTex format
		self.authors_bibtex = ' and '.join(self.authors_list)

		# overwrite authors string
		if len(self.authors_list) > 2:
			self.authors = ', and '.join([
				', '.join(self.authors_list[:-1]),
				self.authors_list[-1]])
		elif len(self.authors_list) > 1:
			self.authors = ' and '.join(self.authors_list)
		else:
			self.authors = self.authors_list[0]


	def __unicode__(self):
		return self.__str__()


	def __str__(self):
		if len(self.title) < 64:
			return self.title
		else:
			index = self.title.rfind(' ', 40, 62)

			if index < 0:
				return self.title[:61] + '...'
			else:
				return self.title[:index] + '...'


	def keywords_escaped(self):
		return [(keyword.strip(), urlquote_plus(keyword.strip()))
			for keyword in self.keywords.split(',')]


	def authors_escaped(self):
		return [(author, author.lower().replace(' ', '+'))
			for author in self.authors_list]


	def key(self):
		# this publication's first author
		author_lastname = self.authors_list[0].split(' ')[-1]

		publications = Publication.objects.filter(
			year=self.year,
			authors__icontains=author_lastname).order_by('month', 'id')

		# character to append to BibTex key
		char = ord('a')

		# augment character for every publication 'before' this publication
		for publication in publications:
			if publication == self:
				break
			if publication.authors_list[0].split(' ')[-1] == author_lastname:
				char += 1

		return self.authors_list[0].split(' ')[-1] + str(self.year) + chr(char)


	def title_bibtex(self):
		return self.title.replace('%', r'\%')


	def month_bibtex(self):
		return self.MONTH_BIBTEX.get(self.month, '')


	def month_long(self):
		for month_int, month_str in self.MONTH_CHOICES:
			if month_int == self.month:
				return month_str
		return ''


	def first_author(self):
		return self.authors_list[0]


	def journal_or_book_title(self):
		if self.journal:
			return self.journal
		else:
			return self.book_title


	def first_page(self):
		return self.pages.split('-')[0]


	def last_page(self):
		return self.pages.split('-')[-1]


	def z3988(self):
		contextObj = ['ctx_ver=Z39.88-2004']

		if 'django.contrib.sites' in settings.INSTALLED_APPS:
			domain = Site.objects.get_current().domain
		else:
			domain = 'example.com'

		rfr_id = domain.split('.')

		if len(rfr_id) > 2:
			rfr_id = rfr_id[-2]
		elif len(rfr_id) > 1:
			rfr_id = rfr_id[0]
		else:
			rfr_id = ''

		if self.book_title and not self.journal:
			contextObj.append('rft_val_fmt=info:ofi/fmt:kev:mtx:book')
			contextObj.append('rfr_id=info:sid/' + domain + ':' + rfr_id)
			contextObj.append('rft_id=info:doi/' + urlquote_plus(self.doi))

			contextObj.append('rft.btitle=' + urlquote_plus(self.title))

			if self.publisher:
				contextObj.append('rft.pub=' + urlquote_plus(self.publisher))

		else:
			contextObj.append('rft_val_fmt=info:ofi/fmt:kev:mtx:journal')
			contextObj.append('rfr_id=info:sid/' + domain + ':' + rfr_id)
			contextObj.append('rft_id=info:doi/' + urlquote_plus(self.doi))
			contextObj.append('rft.atitle=' + urlquote_plus(self.title))

			if self.journal:
				contextObj.append('rft.jtitle=' + urlquote_plus(self.journal))

			if self.volume:
				contextObj.append('rft.volume={0}'.format(self.volume))

			if self.pages:
				contextObj.append('rft.pages=' + urlquote_plus(self.pages))

			if self.number:
				contextObj.append('rft.issue={0}'.format(self.number))

		if self.month:
			contextObj.append('rft.date={0}-{1}-1'.format(self.year, self.month))
		else:
			contextObj.append('rft.date={0}'.format(self.year))

		for author in self.authors_list:
			contextObj.append('rft.au=' + urlquote_plus(author))


		if self.isbn:
			contextObj.append('rft.isbn=' + urlquote_plus(self.isbn))

		return '&'.join(contextObj)


	def clean(self):
		if not self.citekey:
			self._produce_author_lists()
			self.citekey = self.key()

		# remove unnecessary whitespace
		self.title = self.title.strip()
		self.journal = self.journal.strip()
		self.book_title = self.book_title.strip()
		self.publisher = self.publisher.strip()
		self.institution = self.institution.strip()


	@staticmethod
	def simplify_name(name):
		name = name.lower()
		name = name.replace(u'ä', u'ae')
		name = name.replace(u'ö', u'oe')
		name = name.replace(u'ü', u'ue')
		name = name.replace(u'ß', u'ss')
		return name
