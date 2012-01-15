__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.db import models
from django.utils.http import urlquote_plus
from string import split, strip, join, replace, ascii_uppercase
from publications.fields import PagesField
from publications.models import Type

class Publication(models.Model):
	class Meta:
		app_label = 'publications'
		ordering = ['-year', '-month', '-id']

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

	type = models.ForeignKey(Type)
	title = models.CharField(max_length=512)
	authors = models.CharField(max_length=2048,
		help_text='List of authors separated by commas or <i>and</i>.')
	year = models.PositiveIntegerField(max_length=4)
	month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
	journal = models.CharField(max_length=256, blank=True)
	book_title = models.CharField(max_length=256, blank=True)
	publisher = models.CharField(max_length=256, blank=True)
	volume = models.IntegerField(blank=True, null=True)
	number = models.IntegerField(blank=True, null=True, verbose_name='Issue number')
	pages = PagesField(max_length=32, blank=True)
	note = models.CharField(max_length=256, blank=True)
	keywords = models.CharField(max_length=256, blank=True,
		help_text='List of keywords separated by commas.')
	url = models.URLField(blank=True, verify_exists=False, verbose_name='URL',
		help_text='Link to PDF or journal page.')
	code = models.URLField(blank=True, verify_exists=False,
		help_text='Link to page with code.')
	pdf = models.FileField(upload_to='publications/', verbose_name='PDF', blank=True, null=True)
	doi = models.CharField(max_length=128, verbose_name='DOI', blank=True)
	external = models.BooleanField(
		help_text='If publication was written in another lab, mark as external.')
	abstract = models.TextField(blank=True)

	def __init__(self, *args, **kwargs):
		models.Model.__init__(self, *args, **kwargs)

		# post-process keywords
		self.keywords = replace(self.keywords, ';', ',')
		self.keywords = replace(self.keywords, ', and ', ', ')
		self.keywords = replace(self.keywords, ',and ', ', ')
		self.keywords = replace(self.keywords, ' and ', ', ')
		self.keywords = [strip(s).lower() for s in split(self.keywords, ',')]
		self.keywords = join(self.keywords, ', ').lower()

		# post-process author names
		self.authors = replace(self.authors, ', and ', ', ')
		self.authors = replace(self.authors, ',and ', ', ')
		self.authors = replace(self.authors, ' and ', ', ')
		self.authors = replace(self.authors, ';', ',')

		# list of authors
		self.authors_list = [strip(author) for author in split(self.authors, ',')]

		# simplified representation of author names
		self.authors_list_simple = []

		# tests if title already ends with a punctuation mark
		self.title_ends_with_punct = self.title[-1] in ['.', '!', '?'] \
			if len(self.title) > 0 else False

		# further post-process author names
		for i, author in enumerate(self.authors_list):
			names = split(author, ' ')

			# check if last string contains initials
			if (len(names[-1]) <= 3) and all(c in ascii_uppercase for c in names[-1]):
				names = [c + '.' for c in names[-1]] + names[:-1]

			# abbreviate names
			for j, name in enumerate(names[:-1]):
				if (j > 0) and name in ['van', 'von', 'der']:
					continue

				if (len(name) > 2) or (len(name) and (name[-1] != '.')):
					k = name.find('-')
					if 0 < k + 1 < len(name):
						# take care of dash
						names[j] = name[0] + '.-' + name[k + 1] + '.'
					else:
						names[j] = name[0] + '.'

			if len(names):
				self.authors_list[i] = join(names, ' ')

				# create simplified representation of author name
				if len(names) > 1:
					for name in names[0].split('-'):
						self.authors_list_simple.append(join(
							[name.lower(), names[-1].lower()], ' '))
				else:
					self.authors_list_simple.append(names[0].lower())

		# list of authors in BibTex format
		self.authors_bibtex = join(self.authors_list, ' and ')

		# overwrite authors string
		if len(self.authors_list) > 2:
			self.authors = join([
				join(self.authors_list[:-1], ', '),
				self.authors_list[-1]], ', and ')
		elif len(self.authors_list) > 1:
			self.authors = join(self.authors_list, ' and ')
		else:
			self.authors = self.authors_list[0]


	def __unicode__(self):
		if len(self.title) < 64:
			return self.title
		else:
			index = self.title.rfind(' ', 40, 62)

			if index < 0:
				return self.title[:61] + '...'
			else:
				return self.title[:index] + '...'


	def keywords_escaped(self):
		return [(strip(keyword), urlquote_plus(strip(keyword)))
			for keyword in split(self.keywords, ',')]


	def authors_escaped(self):
		return [(author, replace(author.lower(), ' ', '+'))
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
