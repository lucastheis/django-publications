# -*- coding: utf-8 -*-
import warnings
from string import ascii_uppercase

from django.conf import settings
from django.db import models
from django.utils.http import urlquote_plus
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from echoices.enums import EChoice, EOrderedChoice
from echoices.fields import make_echoicefield

from ..fields import NullCharField, PagesField
from ..models import Type

if 'django.contrib.sites' in settings.INSTALLED_APPS:
    from django.contrib.sites.models import Site


class Publication(models.Model):
    """
    Model representing a publication.
    """

    class Meta:
        ordering = ['-year', '-month', '-id']
        app_label = 'publications_bootstrap'  # Fix for Django<1.7

    # names shown in admin area
    class EMonths(EOrderedChoice):
        JAN = (1, _('January'), 'Jan')
        FEB = (2, _('February'), 'Feb')
        MAR = (3, _('March'), 'Mar')
        APR = (4, _('April'), 'Apr')
        MAY = (5, _('May'), 'May')
        JNE = (6, _('June'), 'Jun')
        JLY = (7, _('July'), 'Jul')
        AUG = (8, _('August'), 'Aug')
        SEP = (9, _('September'), 'Sep')
        OCT = (10, _('October'), 'Oct')
        NOV = (11, _('November'), 'Nov')
        DEC = (12, _('December'), 'Dec')

        def __init__(self, v_, l_, bibtex):
            # abbreviations used in BibTex
            self.bibtex = bibtex

    # Status of the publication
    class EStatuses(EChoice):
        DRAFT = ('d', _('draft'))
        SUBMITTED = ('s', _('submitted'))
        ACCEPTED = ('a', _('accepted'))
        PUBLISHED = ('p', _('published'))

    type = models.ForeignKey(Type, db_index=True)
    citekey = NullCharField(max_length=512, blank=True, null=True, unique=True, db_index=True,
                            help_text='BibTex citation key. Leave blank if unsure.')
    title = models.CharField(max_length=512, db_index=True)
    authors = models.CharField(max_length=2048,
                               help_text='List of authors separated by commas or <i>and</i>.')
    year = models.PositiveIntegerField(db_index=True)
    month = make_echoicefield(EMonths, blank=True, null=True, db_index=True)
    journal = models.CharField(max_length=256, blank=True)
    book_title = models.CharField(max_length=256, blank=True,
                                  help_text='Title of a book, part of which is being cited. See '
                                            'the LATEX book for how to type titles. For book '
                                            'entries, use the `title` field instead')
    publisher = models.CharField(max_length=256, blank=True)
    editor = models.CharField(max_length=256, blank=True,
                              help_text='Name(s) of editor(s), typed as indicated in the LATEX '
                                        'book. If there is also an `author` field, then the '
                                        '`editor` field gives the editor of the book or '
                                        'collection in which the reference appears.')
    edition = models.CharField(max_length=256, blank=True,
                               help_text='The edition of a book -- for example, "Second". This '
                                         'should be an ordinal, and should have the first letter '
                                         'capitalized.')
    institution = models.CharField(max_length=256, blank=True)
    school = models.CharField(max_length=256, blank=True,
                              help_text='The name of the school where a thesis was written.')
    organization = models.CharField(max_length=256, blank=True,
                                    help_text='The organization that sponsors a conference or '
                                              'that publishes a manual.')
    location = models.CharField(max_length=256, blank=True,
                                help_text="Place of publication, location of conference, "
                                          "or publisher's address.")
    country = CountryField(blank=True)
    series = models.CharField(blank=True, max_length=256,
                              help_text='The name of a series or set of books. When citing an '
                                        'entire book, the `title` field gives its title and an '
                                        'optional `series` field gives the name of a series or '
                                        'multi-volume set in which the book is published.')
    volume = models.CharField(blank=True, null=True, max_length=128)
    number = models.CharField(blank=True, null=True, max_length=128, verbose_name='Issue number',
                              help_text='The number of a journal, magazine, technical report, or '
                                        'of a work in a series. An issue of a journal or magazine '
                                        'is usually identified by its volume and number; the '
                                        'organization that issues a technical report usually '
                                        'gives it a number; and sometimes books are given numbers '
                                        'in a named series.')
    chapter = models.CharField(blank=True, null=True, max_length=128)
    section = models.CharField(blank=True, null=True, max_length=128)  # Not officially
    # recognized as Bibtex Field Type
    pages = PagesField(max_length=32, blank=True)
    note = models.CharField(max_length=256, blank=True,
                            help_text='Any additional information that can help the reader. The '
                                      'first word should be capitalized.')
    tags = models.CharField(max_length=256, blank=True,
                            help_text='List of tags separated by commas.')
    url = models.URLField(blank=True, verbose_name='URL', help_text='Link to PDF or journal page.')
    code = models.URLField(blank=True, help_text='Link to page with code.')
    pdf = models.FileField(upload_to='publications_bootstrap/', verbose_name='PDF', blank=True, null=True)
    image = models.ImageField(upload_to='publications_bootstrap/images/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='publications_bootstrap/thumbnails/', blank=True, null=True)
    external = models.BooleanField(default=False, db_index=True,
                                   help_text='If publication was written in another lab, mark as external.')
    abstract = models.TextField(blank=True)
    doi = NullCharField(max_length=128, verbose_name='DOI', blank=True, null=True, unique=True)
    isbn = NullCharField(max_length=32, verbose_name='ISBN', blank=True, null=True, unique=True,
                         help_text='Only for a book.')  # A-B-C-D
    status = make_echoicefield(EStatuses, default=EStatuses.PUBLISHED, blank=False)

    def __init__(self, *args, **kwargs):
        models.Model.__init__(self, *args, **kwargs)

        # post-process tags
        self.tags = self.tags.replace(';', ',')
        self.tags = self.tags.replace(', and ', ', ')
        self.tags = self.tags.replace(',and ', ', ')
        self.tags = self.tags.replace(' and ', ', ')
        self.tags = [s.strip().lower() for s in self.tags.split(',')]
        self.tags = ', '.join(self.tags).lower()

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
        self.title_ends_with_punct = self.title[-1] in ['.', '!', '?'] if len(self.title) > 0 else False

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
                self.authors_list_split.append((' '.join(names[:-sp]), ' '.join(names[-sp:])))

        # list of authors in BibTex format
        self.authors_bibtex = ' and '.join(self.authors_list)

        # overwrite authors string
        if len(self.authors_list) > 2:
            self.authors = ', and '.join([', '.join(self.authors_list[:-1]),
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

    def tags_escaped(self):
        warnings.warn("{0}.{1} will be a property in a future release.".format(Publication.__name__,
                                                                               Publication.tags_escaped.__name__, ),
                      FutureWarning)
        return [(tag.strip(), urlquote_plus(tag.strip())) for tag in self.tags.split(',')]

    def authors_escaped(self):
        warnings.warn("{0}.{1} will be a property in a future release.".format(Publication.__name__,
                                                                               Publication.authors_escaped.__name__, ),
                      FutureWarning)
        return [(author, author.lower().replace(' ', '+')) for author in self.authors_list]

    def key(self):
        warnings.warn("Signature of {0}.{1} may change or become a property in a future release.".format(
            Publication.__name__, Publication.key.__name__, ), FutureWarning)
        from django.db.models import Count
        # this publication's first author
        author_lastname = self.authors_list[0].split(' ')[-1]

        # SEE: https://stackoverflow.com/a/5236352/
        publications = Publication.objects.filter(year=self.year, authors__icontains=author_lastname) \
            .annotate(null_citekey=Count('citekey')) \
            .annotate(null_month=Count('month')) \
            .order_by('-null_citekey',  # Ensure publications with citekey are listed first
                      '-null_month',  # Penalize publications without month
                      'month', 'id')

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
        warnings.warn("{0}.{1} will be a property in a future release.".format(Publication.__name__,
                                                                               Publication.title_bibtex.__name__, ),
                      FutureWarning)
        return self.title.replace('%', r'\%')

    def month_bibtex(self):
        warnings.warn("{0}.{1} is deprecated and will be removed in a future release. "
                      "Please use {0}.{2} instead".format(Publication.__name__, Publication.month_bibtex.__name__,
                                                          "month.bibtex"), PendingDeprecationWarning)
        if self.month:
            return self.month.bibtex
        return ''

    def month_long(self):
        warnings.warn("{0}.{1} is deprecated and will be removed in a future release. "
                      "Please use {0}.{2} instead".format(Publication.__name__, Publication.month_long.__name__,
                                                          "month.label"), PendingDeprecationWarning)
        if self.month:
            return self.month.label
        return ''

    def first_author(self):
        warnings.warn("{0}.{1} will be a property in a future release.".format(Publication.__name__,
                                                                               Publication.first_author.__name__, ),
                      FutureWarning)
        return self.authors_list[0]

    def journal_or_book_title(self):
        warnings.warn("{0}.{1} will be a property in a future release.".format(Publication.__name__,
                                                                               Publication.journal_or_book_title.__name__, ),
                      FutureWarning)
        if self.journal:
            return self.journal
        else:
            return self.book_title

    def first_page(self):
        warnings.warn("{0}.{1} will be a property in a future release.".format(Publication.__name__,
                                                                               Publication.first_page.__name__, ),
                      FutureWarning)
        return self.pages.split('-')[0]

    def last_page(self):
        warnings.warn("{0}.{1} will be a property in a future release.".format(Publication.__name__,
                                                                               Publication.last_page.__name__, ),
                      FutureWarning)
        return self.pages.split('-')[-1]

    def z3988(self):
        warnings.warn("Signature of {0}.{1} may change or become a property in a future release.".format(
            Publication.__name__, Publication.z3988.__name__, ), FutureWarning)
        context_obj = ['ctx_ver=Z39.88-2004']

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
            context_obj.append('rft_val_fmt=info:ofi/fmt:kev:mtx:book')
            context_obj.append('rfr_id=info:sid/' + domain + ':' + rfr_id)
            context_obj.append('rft_id=info:doi/' + urlquote_plus(self.doi))

            context_obj.append('rft.btitle=' + urlquote_plus(self.title))

            if self.publisher:
                context_obj.append('rft.pub=' + urlquote_plus(self.publisher))

        else:
            context_obj.append('rft_val_fmt=info:ofi/fmt:kev:mtx:journal')
            context_obj.append('rfr_id=info:sid/' + domain + ':' + rfr_id)
            context_obj.append('rft_id=info:doi/' + urlquote_plus(self.doi))
            context_obj.append('rft.atitle=' + urlquote_plus(self.title))

            if self.journal:
                context_obj.append('rft.jtitle=' + urlquote_plus(self.journal))

            if self.volume:
                context_obj.append('rft.volume={0}'.format(self.volume))

            if self.pages:
                context_obj.append('rft.pages=' + urlquote_plus(self.pages))

            if self.number:
                context_obj.append('rft.issue={0}'.format(self.number))

        if self.month:
            context_obj.append(
                'rft.date={0}-{1}-1'.format(self.year, self.month.value))
        else:
            context_obj.append('rft.date={0}'.format(self.year))

        for author in self.authors_list:
            context_obj.append('rft.au=' + urlquote_plus(author))

        if self.isbn:
            context_obj.append('rft.isbn=' + urlquote_plus(self.isbn))

        return '&'.join(context_obj)

    def clean(self):
        if not self.citekey:
            self._produce_author_lists()
            self.citekey = self.key()

    @property
    def catalogs(self):
        return self.catalog_set.all()

    @staticmethod
    def simplify_name(name):
        name = name.lower()
        name = name.replace(u'ä', u'ae')
        name = name.replace(u'ö', u'oe')
        name = name.replace(u'ü', u'ue')
        name = name.replace(u'ß', u'ss')
        return name
