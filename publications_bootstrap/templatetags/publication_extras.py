# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from distutils.version import StrictVersion
from re import sub

import django
from django.template import Library, RequestContext
from django.template.loader import get_template, render_to_string
from django.utils.html import escape
from django.utils.safestring import mark_safe

from ..apps import PublicationsBootstrapConfig
from ..models import Publication, Catalog, Type
from ..utils import populate

register = Library()

GREEK_LETTERS = \
    '[Aa]lpha|[Bb]eta|[Gg]amma|[Dd]elta|[Ee]psilon|[Zz]eta|' + \
    '[Ee]ta|[Tt]heta|[Ll]ambda|[Mm]u|[Nn]u|[Pp]i|[Ss]igma|[Tt]au|' + \
    '[Pp]hi|[Pp]si|[Cc]hi|[Oo]mega|[Rr]ho|[Xx]i|[Kk]appa'

DEFAULT_MARKER = '[#1-,'
DEFAULT_CITATION_STYLE = 'chicago'
DEFAULT_BIBLIOGRAPHY_LAYOUT = 'card'
DEFAULT_BIBLIOGRAPHY_TITLE = 'References'
DEFAULT_SORTING = 'referenced'


def render_template(template, request, context={}):
    if StrictVersion(django.get_version()) < StrictVersion('1.8.0'):
        return get_template(template).render(RequestContext(request, context))
    # Use kwargs for Django < 1.10
    return render_to_string(template, context=context, request=request)


class CitationManger:
    import re

    marker_pattern = re.compile(
        r'(?P<sup>^\^?)(?P<open>[<({\[]?)(?P<href>#?)(?P<style>1)(?P<ranging>-?)(?P<separator>[^-]+)')
    closing_brackets = {'[': ']', '(': ')', '{': '}', '<': '>'}
    styles_templates = {'1': 'numbered'}

    def __init__(self, **kwargs):
        marker = kwargs.setdefault('marker', PublicationsBootstrapConfig.defaults.get('marker', DEFAULT_MARKER))
        citation = kwargs.setdefault('citation',
                                     PublicationsBootstrapConfig.defaults.get('citation', DEFAULT_CITATION_STYLE))
        bibliography = kwargs.setdefault('bibliography',
                                         PublicationsBootstrapConfig.defaults.get('bibliography',
                                                                                  DEFAULT_BIBLIOGRAPHY_LAYOUT))

        self.sorting = kwargs.setdefault('sorting',  # FIXME: Not yet supported
                                         PublicationsBootstrapConfig.defaults.get('sorting', DEFAULT_SORTING))

        options = {}
        if os.path.sep not in marker:
            # Assume it's not a path to a custom template
            options.update(self.marker_pattern.match(marker).groupdict())
            if options['open']:
                options['close'] = self.closing_brackets[options['open']]
            marker = 'publications_bootstrap/bibliography/markers/{}.html'.format(
                self.styles_templates[options['style']])
        self.marker = marker
        self.marker_options = options
        self.marker_options['separator'] = self.re.sub(r'\s', '&nbsp;', self.marker_options['separator'])
        if os.path.sep not in citation:
            citation = 'publications_bootstrap/citations/{}.html'.format(citation)
        self.citation = citation
        if os.path.sep not in bibliography:
            bibliography = 'publications_bootstrap/bibliography/{}.html'.format(bibliography)
        self.bibliography = bibliography
        self.cited = OrderedDict()

    def cite(self, context, *puids):
        references = []
        for r, p in self.nocite(*puids):
            if references and references[-1][-1][0] + 1 == r:
                references[-1].append((r, p))
            else:
                references.append([(r, p)])
        return render_template(self.marker, context['request'], dict(references=references, marker=self.marker_options))

    def nocite(self, *puids):
        from operator import itemgetter
        batch = []
        for puid in puids:
            publication = _get_publication(puid)
            # Ref key is numeric
            batch.append(self.cited.setdefault(publication.pk, (len(self.cited.keys()) + 1, publication)))
        batch.sort(key=itemgetter(0))
        return batch

    def thebibliography(self, context, title=DEFAULT_BIBLIOGRAPHY_TITLE, **kwargs):
        sorting = kwargs.get('sorting', self.sorting)  # FIXME: Not yet supported
        if sorting == 'referenced':
            references = self.cited.values()
        else:
            # TODO: by author, by title
            raise NotImplementedError
        marker_options = dict(self.marker_options)
        marker_options.pop('href', None)  # Remove hyperlink on 'self' item
        return render_template(self.bibliography, context['request'],
                               dict(title=title, references=references, marker=self.marker,
                                    marker_options=marker_options, citation=self.citation))

    def clear(self):
        self.cited.clear()


__citations_manager = None


def _get_publication(uid):
    # TODO: add this to a custom models.Manager
    try:
        pbl = Publication.objects.get(pk=int(uid))
    except ValueError:
        pbl = Publication.objects.get(citekey__iexact=uid)
    return pbl


def _get_catalog(id_or_title):
    # TODO: add this to a custom models.Manager
    try:
        pbl = Catalog.objects.get(pk=int(id_or_title))
    except ValueError:
        pbl = Catalog.objects.get(title__iexact=id_or_title)
    return pbl


@register.simple_tag(takes_context=True)
def get_publication(context, puid, template='publications_bootstrap/components/publication.html'):
    """
    Get a single publication.

    Parameters
    ----------
    puid : int or str
        Publication unique id, either pk or citekey.
    """
    try:
        pbl = _get_publication(puid)
        pbl.links = pbl.publicationlink_set.all()
        pbl.files = pbl.publicationfile_set.all()

        return render_template(template, context['request'], {'publication': pbl})
    except Publication.DoesNotExist:
        return render_template('publications_bootstrap/components/empty.html', context['request'])


@register.simple_tag(takes_context=True)
def get_publications(context, template='publications_bootstrap/components/publications.html'):
    """
    Get all publications.
    """

    types = Type.objects.filter(hidden=False)
    publications = Publication.objects.select_related()
    publications = publications.filter(external=False, type__in=types)

    if not publications:
        return render_template('publications_bootstrap/components/empty.html', context['request'])

    publications = publications.order_by('-year', '-month', '-id')
    populate(publications)  # load custom links and files
    return render_template(template, context['request'], {'publications': publications})


@register.simple_tag(takes_context=True)
def get_catalog(context, id_or_title, template='publications_bootstrap/components/section.html'):
    """
    Get a publication catalog.
    """
    try:
        catalog = _get_catalog(id_or_title)

        publications = catalog.publications.all()
        if not publications:
            raise Publication.DoesNotExist
        publications = publications.order_by('-year', '-month', '-id')

        # load custom links and files
        populate(publications)

        return render_template(template, context['request'], {'title': id_or_title, 'publications': publications})
    except Catalog.DoesNotExist:
        return render_template('publications_bootstrap/components/empty.html', context['request'],
                               {'error': True, 'alert':
                                   {'heading': 'Zut!',
                                    'message': 'There is no such catalog named "%"'.format(id_or_title)}})
    except Publication.DoesNotExist:
        return render_template('publications_bootstrap/components/empty.html', context['request'])


@register.simple_tag(takes_context=True)
def get_citation(context, puid, style=DEFAULT_CITATION_STYLE):
    """
    Get a formatted citation
    
    Parameters
    ----------
    context
    puid : int
        Publication unique id, either pk or citekey.
    style

    Returns
    -------

    """
    pbl = _get_publication(puid)
    if os.path.sep not in style:
        style = 'publications_bootstrap/citations/{}.html'.format(style)
    return render_template(style, context['request'], {'publication': pbl})


@register.simple_tag(takes_context=False)
def setup_citations(**kwargs):
    """
    Define parameters for the layout of the citation marker and style and the bibliography.
    Will remain until it is redefined with `setup_citations` or reset with `thebibliography(reset=True)`.

    Parameters
    ----------
    kwargs
        marker : str
            Marker specifications or path to custom template. Specifications are a mini-language:
            TODO: specifications
            For example: '^[#1-,' will
            * use superscript notation (^; optional),
            * square brackets ([; can also be '(', '{'or '<'),
            * provide a hyperlink to the entry in the bibliography (#; optional),
            * use a numbered citation (1; mandatory),
            * show range with a dash instead of listing all the individual publications in that range (-; optional),
            * and separate the citations with a comma without trailing space (,; must be at least one char different
              from '-').
        citation : str
            Template name in default location or path to custom template
        bibliography : str
            Template name in default location or path to custom template

    Returns
    -------
    str
        Empty string

    """
    global __citations_manager
    __citations_manager = CitationManger(**kwargs)
    return ''


@register.simple_tag(takes_context=True)
def cite(context, *puids, **kwargs):
    """
    Like \cite{} in LaTeX, add the publication(s) to the bibliography and generate a marker.

    Parameters
    ----------
    context
    puids
        Publication(s) unique id, either pk or citekey.
    kwargs
        Same as `setup_citations`, is actuall just a shortcut. Only the very first call will be effective. After that,
        requires to call directly `setup_citations` to force the reset.

    Returns
    -------

    """
    if __citations_manager is None:
        # Assume new page
        setup_citations(**kwargs)
    return __citations_manager.cite(context, *puids)


@register.simple_tag(takes_context=False)
def nocite(*puids, **kwargs):
    """
    Like \nocite{} in LaTeX, add the publication(s) to the bibliography but generate no marker.

    Parameters
    ----------
    puids
        Publication unique id, either pk or citekey.

    Returns
    -------
    str
        Empty string

    """
    if __citations_manager is None:
        # Assume new page
        setup_citations(**kwargs)
    __citations_manager.nocite(*puids)
    return ''


@register.simple_tag(takes_context=True)
def thebibliography(context, clear=True, reset=False, **kwargs):
    """
    Like \thebibliography{} in LaTeX, generate a list of references.

    Parameters
    ----------
    context
    clear : bool
        Clear the references of cited publications. Else, the next bibliography will also contain the publications
        listed here, as the references persist through the templates.
    reset : bool
        The next bibliography will be generated using new settings. Otherwise, the next bibliographies will all use the
        same parameters as this one, unless `setup_citations` is used.
    kwargs
        Not yet supported, for future features

    Returns
    -------

    """
    global __citations_manager
    bibliography = __citations_manager.thebibliography(context, **kwargs)
    if clear:
        __citations_manager.clear()
    if reset:
        __citations_manager = None
    return bibliography


@register.filter()
def tex_parse(string):
    """
    Renders some basic TeX math to HTML.
    """
    string = string.replace('{', '').replace('}', '')

    def tex_replace(match):
        return \
            sub(r'\^(\w)', r'<sup>\1</sup>',
                sub(r'\^\{(.*?)\}', r'<sup>\1</sup>',
                    sub(r'\_(\w)', r'<sub>\1</sub>',
                        sub(r'\_\{(.*?)\}', r'<sub>\1</sub>',
                            sub(r'\\(' + GREEK_LETTERS + ')', r'&\1;', match.group(1))))))

    return mark_safe(sub(r'\$([^\$]*)\$', tex_replace, escape(string)))


@register.filter(is_safe=False)
def as_list(o):
    return [o]


@register.filter()
def flatten_authors(authors, args=None):
    from django.http import QueryDict
    qs = QueryDict(args)
    separator = qs.get('separator', ',')
    limit = max(int(qs.get('limit', 8)), 0)
    # 'last' is ignored if it can not be applied (limit < #authors)
    last = qs.get('last', separator) if not limit or limit >= len(authors) else separator
    limit = limit if limit > 0 else ''
    et_al = qs.get('et_al', ',&nbsp;<i>et al.</i>')
    template = qs.get('template', 'publications_bootstrap/filters/authors.html')
    return render_to_string(template,
                            dict(authors=authors, limit=str(limit), separator=separator, last=last, et_al=et_al))
