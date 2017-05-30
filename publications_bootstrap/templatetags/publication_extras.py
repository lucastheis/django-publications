# -*- coding: utf-8 -*-

from distutils.version import StrictVersion
from re import sub

import django
from django.template import Library, RequestContext
from django.template.loader import get_template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from ..models import Publication, Catalog, Type
from ..utils import populate

register = Library()

GREEK_LETTERS = \
    '[Aa]lpha|[Bb]eta|[Gg]amma|[Dd]elta|[Ee]psilon|[Zz]eta|' + \
    '[Ee]ta|[Tt]heta|[Ll]ambda|[Mm]u|[Nn]u|[Pp]i|[Ss]igma|[Tt]au|' + \
    '[Pp]hi|[Pp]si|[Cc]hi|[Oo]mega|[Rr]ho|[Xx]i|[Kk]appa'


def render_template(template, request, args):
    if StrictVersion(django.get_version()) < StrictVersion('1.8.0'):
        return get_template(template).render(RequestContext(request, args))
    return get_template(template).render(args, request)


@register.simple_tag(takes_context=True)
def get_publications(context, template='publications_bootstrap/components/publications.html'):
    """
    Get all publications.
    """

    types = Type.objects.filter(hidden=False)
    publications = Publication.objects.select_related()
    publications = publications.filter(external=False, type__in=types)
    publications = publications.order_by('-year', '-month', '-id')

    if not publications:
        return render_template('publications_bootstrap/components/empty.html', context['request'], {})

    # load custom links and files
    populate(publications)

    return render_template(template, context['request'], {'publications': publications})


@register.simple_tag(takes_context=True)
def get_publication(context, p_id):
    """
    Get a single publication.
    """
    try:
        pbl = Publication.objects.get(pk=int(p_id))

        pbl.links = pbl.publicationlink_set.all()
        pbl.files = pbl.publicationfile_set.all()

        return render_template('publications_bootstrap/components/publication.html', context['request'],
                               {'publication': pbl})
    except Publication.DoesNotExist:
        return render_template('publications_bootstrap/components/empty.html', context['request'], {})


@register.simple_tag(takes_context=True)
def get_catalog(context, catalog_title, template='publications_bootstrap/components/section.html'):
    """
    Get a publication catalog.
    """
    try:
        publications_catalog = Catalog.objects.get(title__iexact=catalog_title)

        publications = publications_catalog.publication_set.all()
        if not publications:
            raise Publication.DoesNotExist
        publications = publications.order_by('-year', '-month', '-id')

        # load custom links and files
        populate(publications)

        return render_template(template, context['request'], {'title': catalog_title, 'publications': publications})
    except Catalog.DoesNotExist:
        return render_template('publications_bootstrap/components/empty.html', context['request'],
                               {'error': True, 'alert':
                                   {'heading': 'Zut!',
                                    'message': 'There is no such catalog named "%"'.format(catalog_title)}})
    except Publication.DoesNotExist:
        return render_template('publications_bootstrap/components/empty.html', context['request'], {})


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
