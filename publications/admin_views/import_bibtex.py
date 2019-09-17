__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

import re
import publications.six as six
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from publications.bibtex import parse
from publications.models import Publication, Type

# mapping of months
MONTHS = {
	'jan': 1, 'january': 1,
	'feb': 2, 'february': 2,
	'mar': 3, 'march': 3,
	'apr': 4, 'april': 4,
	'may': 5,
	'jun': 6, 'june': 6,
	'jul': 7, 'july': 7,
	'aug': 8, 'august': 8,
	'sep': 9, 'september': 9,
	'oct': 10, 'october': 10,
	'nov': 11, 'november': 11,
	'dec': 12, 'december': 12}

def import_bibtex(request):
	if request.method == 'POST':
		# try to parse BibTex
		bib = parse(request.POST['bibliography'])

		# container for error messages
		errors = {}

		# publication types
		types = Type.objects.all()

		# check for errors
		if not bib:
			if not request.POST['bibliography']:
				errors['bibliography'] = 'This field is required.'

		if not errors:
			publications = []

			# try adding publications
			for entry in bib:
				if 'title' in entry and \
				   'author' in entry and \
				   'year' in entry:
					# parse authors
					authors = entry['author'].split(' and ')
					for i in range(len(authors)):
						author = authors[i].split(',')
						author = [author[-1]] + author[:-1]
						authors[i] = ' '.join(author)
					authors = ', '.join(authors)

					# add missing keys
					keys = [
						'journal',
						'booktitle',
						'publisher',
						'institution',
						'url',
						'doi',
						'isbn',
						'keywords',
						'pages',
						'note',
						'abstract',
						'month']

					for key in keys:
						if not key in entry:
							entry[key] = ''

					# map integer fields to integers
					entry['month'] = MONTHS.get(entry['month'].lower(), 0)

					entry['volume'] = entry.get('volume', None)
					entry['number'] = entry.get('number', None)

					if isinstance(entry['volume'], six.text_type):
						entry['volume'] = int(re.sub('[^0-9]', '', entry['volume']))
					if isinstance(entry['number'], six.text_type):
						entry['number'] = int(re.sub('[^0-9]', '', entry['number']))

					# remove whitespace characters (likely due to line breaks)
					entry['url'] = re.sub(r'\s', '', entry['url'])

					# determine type
					type_id = None

					for t in types:
						if entry['type'] in t.bibtex_type_list:
							type_id = t.id
							break

					if type_id is None:
						errors['bibliography'] = 'Type "' + entry['type'] + '" unknown.'
						break

					# add publication
					publications.append(Publication(
						type_id=type_id,
						citekey=entry['key'],
						title=entry['title'],
						authors=authors,
						year=entry['year'],
						month=entry['month'],
						journal=entry['journal'],
						book_title=entry['booktitle'],
						publisher=entry['publisher'],
						institution=entry['institution'],
						volume=entry['volume'],
						number=entry['number'],
						pages=entry['pages'],
						note=entry['note'],
						url=entry['url'],
						doi=entry['doi'],
						isbn=entry['isbn'],
						external=False,
						abstract=entry['abstract'],
						keywords=entry['keywords']))
				else:
					errors['bibliography'] = 'Make sure that the keys title, author and year are present.'
					break

		if not errors and not publications:
			errors['bibliography'] = 'No valid BibTex entries found.'

		if errors:
			# some error occurred
			return render(
				request,
				'admin/publications/import_bibtex.html', {
					'errors': errors,
					'title': 'Import BibTex',
					'types': Type.objects.all(),
					'request': request})
		else:
			try:
				# save publications
				for publication in publications:
					publication.save()
			except:
				msg = 'Some error occured during saving of publications.'
			else:
				if len(publications) > 1:
					msg = 'Successfully added ' + str(len(publications)) + ' publications.'
				else:
					msg = 'Successfully added ' + str(len(publications)) + ' publication.'

			# show message
			messages.info(request, msg)

			# redirect to publication listing
			if len(publications) == 1:
				return HttpResponseRedirect('../%s/change/' % publications[0].id)
			else:
				return HttpResponseRedirect('../')
	else:
		return render(
			request,
			'admin/publications/import_bibtex.html', {
				'title': 'Import BibTex',
				'types': Type.objects.all(),
				'request': request})

import_bibtex = staff_member_required(import_bibtex)
