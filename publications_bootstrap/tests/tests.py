# -*- coding: utf-8 -*-
import warnings
from distutils.version import StrictVersion

import django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.template import Template, RequestContext
from django.test import TestCase

from ..models import Publication, Type, PublicationLink, Catalog
from ..templatetags.publication_extras import tex_parse

warnings.simplefilter("always")


class Tests(TestCase):
    fixtures = ['initial_data.json', 'test_data.json']
    urls = 'publications_bootstrap.tests.urls'

    def test_authors(self):
        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'Jörn-Philipp Lies and Ralf M. Häfner and M. Bethge',
            title=u'Slowness and sparseness have diverging effects on complex cell learning',
            year=2014,
            journal=u'PLoS Computational Biology',
            external=0)
        publication.clean()
        publication.save()

        self.assertEqual(len(publication.authors_list), 3)
        self.assertTrue('J.-P. Lies' in publication.authors_list)
        self.assertTrue(('J.-P.', 'Lies') in publication.authors_list_split)

    def test_citekey(self):
        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and B. Common',
            title=u'Title 1',
            year=2014,
            journal=u'Journal',
            external=0)
        publication.clean()
        publication.save()

        self.assertEqual(publication.citekey, 'Unique2014a')

        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and C. Common',
            title=u'Title 2',
            year=2014,
            journal=u'Journal',
            external=0)
        publication.clean()
        publication.save()

        self.assertEqual(publication.citekey, 'Unique2014b')

        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and D. Uncommon',
            title=u'Title 3',
            year=2013,
            journal=u'Journal',
            external=0)
        publication.clean()
        publication.save()

        self.assertEqual(publication.citekey, 'Unique2013a')

        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and D. Uncommon',
            title=u'Title 4',
            year=2013,
            month=Publication.EMonths.MAY,
            journal=u'Journal',
            external=0)
        publication.clean()
        publication.save()

        self.assertEqual(publication.citekey, 'Unique2013b')

        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and D. Uncommon',
            title=u'Title 5',
            year=2013,
            journal=u'Journal',
            external=0)
        publication.clean()
        publication.save()

        self.assertEqual(publication.citekey, 'Unique2013c')

    def test_month(self):
        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and B. Common',
            title=u'Publication with month',
            year=2017,
            month=Publication.EMonths.MAY)
        publication.clean()
        publication.save()

        self.assertEqual(publication.month, Publication.EMonths.MAY)
        self.assertEqual(publication.month_long(), Publication.EMonths.MAY.label)
        self.assertEqual(publication.month_bibtex(), Publication.EMonths.MAY.bibtex)

        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and B. Common',
            title=u'Publication without month',
            year=2017)
        publication.clean()
        publication.save()

        self.assertEqual(publication.month, None)
        self.assertEqual(publication.month_long(), '')
        self.assertEqual(publication.month_bibtex(), '')

    def test_publication_links(self):
        link = PublicationLink.objects.create(publication_id=1, description='Test', url='http://test.com')
        link.save()

        self.assertEqual(self.client.get('/publications/').status_code, 200)
        self.assertEqual(self.client.get('/publications/1/').status_code, 200)

    def test_publications(self):
        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'Jörn-Philipp Lies and Ralf M. Häfner and M. Bethge',
            title=u'Slowness and sparseness have diverging effects on complex cell learning',
            year=2014,
            journal=u'PLoS Computational Biology',
            external=0)
        publication.clean()
        publication.save()

        self.assertEqual(self.client.get('/publications/').status_code, 200)
        self.assertEqual(self.client.get('/publications/?plain').status_code, 200)
        self.assertEqual(self.client.get('/publications/?bibtex').status_code, 200)
        self.assertEqual(self.client.get('/publications/?mods').status_code, 200)
        self.assertEqual(self.client.get('/publications/?ris').status_code, 200)
        self.assertEqual(self.client.get('/publications/?rss').status_code, 200)
        self.assertEqual(self.client.get('/publications/1/').status_code, 200)
        self.assertEqual(self.client.get('/publications/1/?plain').status_code, 200)
        self.assertEqual(self.client.get('/publications/1/?bibtex').status_code, 200)
        self.assertEqual(self.client.get('/publications/1/?mods').status_code, 200)
        self.assertEqual(self.client.get('/publications/1/?ris').status_code, 200)
        self.assertEqual(self.client.get('/publications/100/').status_code, 404)
        response = self.client.get('/publications/j.-p.+lies/')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['publications']), 0)
        self.assertEqual(self.client.get('/publications/j.-p.+lies/?plain').status_code, 200)
        self.assertEqual(self.client.get('/publications/j.-p.+lies/?bibtex').status_code, 200)
        self.assertEqual(self.client.get('/publications/j.-p.+lies/?mods').status_code, 200)
        self.assertEqual(self.client.get('/publications/j.-p.+lies/?ris').status_code, 200)
        self.assertEqual(self.client.get('/publications/j.-p.+lies/?rss').status_code, 200)
        self.assertEqual(self.client.get('/publications/tag/noise+correlations/').status_code, 200)
        self.assertEqual(self.client.get('/publications/tag/noise+correlations/?plain').status_code, 200)
        self.assertEqual(self.client.get('/publications/tag/noise+correlations/?bibtex').status_code, 200)
        self.assertEqual(self.client.get('/publications/tag/noise+correlations/?mods').status_code, 200)
        self.assertEqual(self.client.get('/publications/tag/noise+correlations/?ris').status_code, 200)
        self.assertEqual(self.client.get('/publications/catalog/highlights/').status_code, 200)
        self.assertEqual(self.client.get('/publications/catalog/highlights/?plain').status_code, 200)
        self.assertEqual(self.client.get('/publications/catalog/highlights/?bibtex').status_code, 200)
        self.assertEqual(self.client.get('/publications/catalog/highlights/?mods').status_code, 200)
        self.assertEqual(self.client.get('/publications/catalog/highlights/?ris').status_code, 200)
        self.assertEqual(self.client.get('/publications/catalog/highlights/?rss').status_code, 200)
        self.assertEqual(self.client.get('/publications/catalog/foobar/').status_code, 404)
        self.assertEqual(self.client.get('/publications/year/2011/').status_code, 200)
        self.assertEqual(self.client.get('/publications/year/2011/?plain').status_code, 200)
        self.assertEqual(self.client.get('/publications/year/2011/?bibtex').status_code, 200)

        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and B. Common',
            title=u'Title 3',
            year=2012,
            journal=u'Journal',
            external=0)
        publication.clean()
        publication.save()

        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and C. Common and D. Someone',
            title=u'Title 4',
            year=2011,
            journal=u'Journal',
            external=0)
        publication.clean()
        publication.save()

        link = PublicationLink.objects.create(publication_id=publication.id, description='Test', url='http://test.com')
        link.save()

        response = self.client.get('/publications/c.+common/')

        self.assertTrue('C. Common' in str(response.content))
        self.assertFalse('B. Common' in str(response.content))

    def test_catalogs(self):
        # Ensure backwards compatibility
        publication = Publication.objects.create(
            type=Type.objects.get(pk=1),
            authors=u'A. Unique and C. Common and D. Someone',
            title=u'Title 4',
            year=2011,
            journal=u'Journal',
            external=0)
        publication.clean()
        publication.save()

        catalog = Catalog.objects.get(pk=1)
        catalog.publications.add(publication)

        self.assertEqual(list(publication.catalogs), [catalog])

    def test_unapi(self):
        self.assertEqual(self.client.get('/publications/unapi/').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=1').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=1&format=mods').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=1&format=bibtex').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=1&format=ris').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=99999&format=bibtex').status_code, 404)
        self.assertEqual(self.client.get('/publications/unapi/?id=1&format=foobar').status_code, 406)


class AdminTests(TestCase):
    fixtures = ['initial_data.json', 'test_data.json']

    def setUp(self):
        User.objects.create_superuser('admin', 'admin@test.de', 'admin')
        self.client.login(username='admin', password='admin')

    def test_basics(self):
        self.assertEqual(self.client.get('/publications/').status_code, 200)
        self.assertEqual(self.client.get('/admin/publications_bootstrap/').status_code, 200)

    def test_type_list(self):
        self.assertEqual(self.client.get('/admin/publications_bootstrap/type/').status_code, 200)
        self.assertEqual(self.client.get('/admin/publications_bootstrap/type/6/move-up/', follow=True).status_code, 200)
        self.assertEqual(self.client.get('/admin/publications_bootstrap/type/6/move-down/', follow=True).status_code,
                         200)

    def test_type_change(self):
        self.assertEqual(self.client.get('/admin/publications_bootstrap/type/1/change/').status_code, 200)
        # TODO: assert content

    def test_catalog_list(self):
        res = self.client.get('/admin/publications_bootstrap/catalog/')
        self.assertEqual(res.status_code, 200)
        self.assertInHTML("""<th scope="col"  class="column-publications_count">
    <div class="text"><span>Publications</span></div><div class="clear"></div></th>""", res.rendered_content)
        self.assertInHTML(
            """<tr class="row1">
    <td class="action-checkbox"><input type="checkbox" name="_selected_action" value="1" class="action-select" /></td>
    <th class="field-title"><a href="/admin/publications_bootstrap/catalog/1/change/">Highlights</a></th>
    <td class="field-description">Highlights</td><td class="field-publications_count">0 publications</td></tr>""",
            res.rendered_content)

    def test_catalog_change(self):
        res = self.client.get('/admin/publications_bootstrap/catalog/1/change/')
        self.assertEqual(res.status_code, 200)
        # TODO: assert content

    def test_publications_list(self):
        self.assertEqual(self.client.get('/admin/publications_bootstrap/publication/').status_code, 200)
        # Test admin actions
        from django.contrib.admin import ACTION_CHECKBOX_NAME
        change_url = reverse('admin:publications_bootstrap_publication_changelist')
        for action, db_value in [('set_status_draft', Publication.EStatuses.DRAFT),
                                 ('set_status_submitted', Publication.EStatuses.SUBMITTED),
                                 ('set_status_accepted', Publication.EStatuses.ACCEPTED),
                                 ('set_status_published', Publication.EStatuses.PUBLISHED), ]:
            data = {'action': action,
                    ACTION_CHECKBOX_NAME: Publication.objects.all().values_list('pk', flat=True)}
            response = self.client.post(change_url, data, follow=True)

            # Test effective change in DB
            measured = Publication.objects.filter(status=db_value, pk__in=data[ACTION_CHECKBOX_NAME]).count()
            expected = Publication.objects.count()
            self.assertEqual(measured, expected, "AssertionError in {}: {} != {}".format(action, measured, expected, ))
            # Test UI
            # For some reason, the <ul class="messagelist"> is not shown on D1.10
            if StrictVersion(django.get_version()) < StrictVersion('1.10.0'):
                self.assertContains(response, '{} publications were successfully marked as '
                                              ''.format(expected),
                                    msg_prefix="AssertionError in {}: ".format(action))
                # Test on a single object
                # Django<1.6 does not support QuerySet.first()
                data[ACTION_CHECKBOX_NAME] = [Publication.objects.all()[0].pk]
                response = self.client.post(change_url, data, follow=True)
                self.assertContains(response, '1 publication was successfully marked as ',
                                    msg_prefix="AssertionError in {}: ".format(action))

    def test_publication_change(self):
        res = self.client.get('/admin/publications_bootstrap/publication/1/change/')
        self.assertEqual(res.status_code, 200)
        self.assertInHTML("""<select name="Catalog_publications-0-catalog" id="id_Catalog_publications-0-catalog">
    <option value="" selected>---------</option><option value="1">Highlights</option></select>""",
                          res.rendered_content)
        # TODO: assert more content

    def test_bibtex_import(self):
        self.client.login(username='admin', password='admin')

        count = Publication.objects.count()
        self.client.post('/admin/publications_bootstrap/publication/import_bibtex/',
                         {'bibliography': TEST_BIBLIOGRAPHY}, follow=False)

        self.assertEqual(Publication.objects.count() - count, TEST_BIBLIOGRAPHY_COUNT)

        publications = Publication.objects.filter(citekey='test:2009')

        self.assertEqual(len(publications), 1)
        self.assertTrue('F. Last-Name' in publications[0].authors_list)
        self.assertTrue('P. van der Markt III' in publications[0].authors_list)
        self.assertTrue('Test' in publications[0].authors_list)
        self.assertTrue('C. F. Gauss II' in publications[0].authors_list)

        publications = Publication.objects.filter(citekey='kay2015good')

        self.assertEqual(len(publications), 1)
        self.assertTrue(publications[0].title.startswith('How Good is 85%?'))


class TestExtras(TestCase):
    fixtures = ['initial_data.json', 'test_data.json']
    urls = 'publications_bootstrap.tests.urls'

    def test_tex_parse(self):
        # tex_parse is used to replace simple LaTeX code in publication titles
        self.assertEqual(tex_parse(u'$L_p$-spherical'), u'L<sub>p</sub>-spherical')
        self.assertEqual(tex_parse(u'$L^2$-spherical'), u'L<sup>2</sup>-spherical')

    def test_flatten_authors(self):
        # Default values
        tpl = Template("""{% load publication_extras %}{{ publication.authors_escaped|flatten_authors }}""")
        ctx = dict(publication=Publication.objects.get(pk=1))
        res = tpl.render(RequestContext(HttpRequest(), ctx))
        self.assertEqual(res, """<a href="/publications/a.+s.+ecker/">A. S. Ecker</a>,
<a href="/publications/p.+berens/">P. Berens</a>,
<a href="/publications/r.+j.+cotton/">R. J. Cotton</a>,
<a href="/publications/m.+subramaniyan/">M. Subramaniyan</a>,
<a href="/publications/g.+h.+denfield/">G. H. Denfield</a>,
<a href="/publications/c.+r.+cadwell/">C. R. Cadwell</a>,
<a href="/publications/s.+m.+smirnakis/">S. M. Smirnakis</a>,
<a href="/publications/m.+bethge/">M. Bethge</a>,&nbsp;<i>et al.</i>""")
        # Provide limit
        tpl = Template("""{% load publication_extras %}{{ publication.authors_escaped|flatten_authors:"limit=3" }}""")
        ctx = dict(publication=Publication.objects.get(pk=1))
        res = tpl.render(RequestContext(HttpRequest(), ctx))
        self.assertEqual(res, """<a href="/publications/a.+s.+ecker/">A. S. Ecker</a>,
<a href="/publications/p.+berens/">P. Berens</a>,
<a href="/publications/r.+j.+cotton/">R. J. Cotton</a>,&nbsp;<i>et al.</i>""")
        # Ignore provided special last author separator
        tpl = Template(
            """{% load publication_extras %}{{ publication.authors_escaped|flatten_authors:"last=, and" }}""")
        ctx = dict(publication=Publication.objects.get(pk=1))
        res = tpl.render(RequestContext(HttpRequest(), ctx))
        self.assertEqual(res, """<a href="/publications/a.+s.+ecker/">A. S. Ecker</a>,
<a href="/publications/p.+berens/">P. Berens</a>,
<a href="/publications/r.+j.+cotton/">R. J. Cotton</a>,
<a href="/publications/m.+subramaniyan/">M. Subramaniyan</a>,
<a href="/publications/g.+h.+denfield/">G. H. Denfield</a>,
<a href="/publications/c.+r.+cadwell/">C. R. Cadwell</a>,
<a href="/publications/s.+m.+smirnakis/">S. M. Smirnakis</a>,
<a href="/publications/m.+bethge/">M. Bethge</a>,&nbsp;<i>et al.</i>""")
        # Provide special last author separator and corner case limit
        tpl = Template(
            """{% load publication_extras %}{{ publication.authors_escaped|flatten_authors:"limit=6&last=, and" }}""")
        ctx = dict(publication=Publication.objects.get(pk=2))
        res = tpl.render(RequestContext(HttpRequest(), ctx))
        self.assertEqual(res, """<a href="/publications/a.+chagas/">A. Chagas</a>,
<a href="/publications/l.+theis/">L. Theis</a>,
<a href="/publications/b.+sengupta/">B. Sengupta</a>,
<a href="/publications/m.+st%C3%BCttgen/">M. Stüttgen</a>,
<a href="/publications/m.+bethge/">M. Bethge</a>, and
<a href="/publications/c.+schwarz/">C. Schwarz</a>""")
        # Provide separator, limit and et_al
        tpl = Template(
            """{% load publication_extras %}{% with et_al="&nbsp;<b>et al.</b>"|urlencode %}{% with args="limit=4&separator= and&et_al="|add:et_al %}{{ publication.authors_escaped|flatten_authors:args }}{% endwith %}{% endwith %}""")
        ctx = dict(publication=Publication.objects.get(pk=2))
        res = tpl.render(RequestContext(HttpRequest(), ctx))
        self.assertEqual(res, """<a href="/publications/a.+chagas/">A. Chagas</a> and
<a href="/publications/l.+theis/">L. Theis</a> and
<a href="/publications/b.+sengupta/">B. Sengupta</a> and
<a href="/publications/m.+st%C3%BCttgen/">M. Stüttgen</a>&nbsp;<b>et al.</b>""")

    def test__get_publication(self):
        from publications_bootstrap.templatetags import publication_extras
        self.assertEqual(publication_extras._get_publication(2), publication_extras._get_publication('Chagas2013a'))

    def test_get_publication(self):
        tpl = Template("""{% load publication_extras %}{% get_publication 2 %}""")
        res = tpl.render(RequestContext(HttpRequest()))
        self.assertInHTML(
            """<p class="card-text"> <a href="/publications/a.+chagas/">A. Chagas</a>, <a href="/publications/l.+theis/">L. Theis</a>, <a href="/publications/b.+sengupta/">B. Sengupta</a>, <a href="/publications/m.+st%C3%BCttgen/">M. Stüttgen</a>, <a href="/publications/m.+bethge/">M. Bethge</a>, and <a href="/publications/c.+schwarz/">C. Schwarz</a></p>""",
            res)
        self.assertInHTML(
            """<a href="/publications/2/" class="title">Functional analysis of ultra high information rates conveyed by rat vibrissal primary afferents</a>""",
            res)
        tpl = Template("""{% load publication_extras %}{% get_publication 'ThisIsNoCitekey' %}""")
        res = tpl.render(RequestContext(HttpRequest()))
        self.assertInHTML(
            """<div class="alert alert-info" role="alert"><h4 class="alert-heading">Sorry</h4><p>There are no publications.</p></div>""",
            res)

    def test_get_publications(self):
        tpl = Template("""{% load publication_extras %}{% get_publications %}""")
        tpl.render(RequestContext(HttpRequest()))
        # TODO: some assertions

    def test__get_catalog(self):
        from publications_bootstrap.templatetags import publication_extras
        self.assertEqual(publication_extras._get_catalog(1), publication_extras._get_catalog('highlights'))

    def test_get_catalog(self):
        link = PublicationLink.objects.create(publication_id=1, description='Test', url='http://test.com')
        link.save()

        publication = Publication.objects.get(pk=1)
        highlights_catalog = Catalog.objects.get(title__iexact='highlights')

        # add publication to catalog
        highlights_catalog.publications.add(publication)

        # Create empty Catalog
        naughty_catalog = Catalog(title="Naughty")
        naughty_catalog.save()

        # render catalog
        tpl = Template("""
{% load publication_extras %}
{% get_publication 1 %}
{% get_catalog 'highlights' 'publications_bootstrap/components/publications_with_thumbnails.html' %}
{% get_catalog 'naughty' %}
{% get_catalog 'foobar' %}
""")

        self.assertGreater(len(tpl.render(RequestContext(HttpRequest())).strip()), 0)

    def test_get_citation(self):
        tpl = Template("""{% load publication_extras %}{% get_citation 2 %}""")
        citation = tpl.render(RequestContext(HttpRequest()))
        self.assertEqual(citation, """<a href="/publications/a.+chagas/">A. Chagas</a>,
<a href="/publications/l.+theis/">L. Theis</a>,
<a href="/publications/b.+sengupta/">B. Sengupta</a>,
<a href="/publications/m.+st%C3%BCttgen/">M. Stüttgen</a>,
<a href="/publications/m.+bethge/">M. Bethge</a>, and
<a href="/publications/c.+schwarz/">C. Schwarz</a>,
"Functional analysis of ultra high information rates conveyed by rat vibrissal primary afferents" <i>Frontiers in Neural Circuits</i> 7 n°&nbsp;190 (2013)""")
        tpl = Template("""{% load publication_extras %}{% get_citation 2 style='chicago' %}""")
        self.assertEqual(tpl.render(RequestContext(HttpRequest())), citation)  # Default is chicago
        # TODO: test other publication types
        tpl = Template("""{% load publication_extras %}{% get_citation 2 style='vancouver' %}""")
        self.assertEqual(tpl.render(RequestContext(HttpRequest())), """<a href="/publications/a.+chagas/">A. Chagas</a>,
<a href="/publications/l.+theis/">L. Theis</a>,
<a href="/publications/b.+sengupta/">B. Sengupta</a>,
<a href="/publications/m.+st%C3%BCttgen/">M. Stüttgen</a>,
<a href="/publications/m.+bethge/">M. Bethge</a>,
<a href="/publications/c.+schwarz/">C. Schwarz</a>.
Functional analysis of ultra high information rates conveyed by rat vibrissal primary afferents. <i>Frontiers in Neural Circuits</i>. 2013; 7 (190).""")
        tpl = Template("""{% load publication_extras %}{% get_citation 'ThisIsNoCitekey' %}""")
        self.assertRaises(Publication.DoesNotExist, tpl.render, RequestContext(HttpRequest()))
        # TODO: test other publication types

    def test_cite(self):
        tpl = Template("""{% load publication_extras %}{% cite 2 %}""")
        self.assertEqual(tpl.render(RequestContext(HttpRequest())), """[<a href="#Chagas2013a">1</a>]""")
        tpl = Template("""{% load publication_extras %}{% cite 1 2 %}""")
        self.assertEqual(tpl.render(RequestContext(HttpRequest())),
                         """[<a href="#Chagas2013a">1</a>,<a href="#Ecker2014a">2</a>]""")
        tpl = Template("""{% load publication_extras %}{% cite 1 5 2 %}""")
        self.assertEqual(tpl.render(RequestContext(HttpRequest())),
                         """[<a href="#Chagas2013a">1</a>&#8209;<a href="#Gerhard2014a">3</a>]""")
        tpl = Template("""{% load publication_extras %}{% cite 2 5 %}""")
        self.assertEqual(tpl.render(RequestContext(HttpRequest())),
                         """[<a href="#Chagas2013a">1</a>,<a href="#Gerhard2014a">3</a>]""")
        tpl = Template("""{% load publication_extras %}{% cite 'ThisIsNoCitekey' %}""")
        self.assertRaises(Publication.DoesNotExist, tpl.render, RequestContext(HttpRequest()))
        # TODO: test other params: sup, open/close, href

    def test_nocite(self):
        tpl = Template("""{% load publication_extras %}{% nocite 2 %}""")
        self.assertEqual(tpl.render(RequestContext(HttpRequest())), '')
        tpl = Template("""{% load publication_extras %}{% nocite 1 2 3 5 %}""")
        self.assertEqual(tpl.render(RequestContext(HttpRequest())), '')
        tpl = Template("""{% load publication_extras %}{% nocite 'ThisIsNoCitekey' %}""")
        self.assertRaises(Publication.DoesNotExist, tpl.render, RequestContext(HttpRequest()))

    def test_thebibliography(self):
        tpl = Template("""{% load publication_extras %}{% thebibliography %}""")
        res = tpl.render(RequestContext(HttpRequest()))
        self.assertIn("""<div class="card mt-5 bibliography">""", res)
        self.assertInHTML("""<h4 class="card-title">References</h4>""", res)
        self.assertIn("""<li class="list-group-item" id="Chagas2013a">""", res)
        self.assertInHTML("""<div class="d-flex mr-1">[<a>1</a>]</div>""", res)
        self.assertInHTML("""<a href="/publications/a.+chagas/">A. Chagas</a>""", res)
        self.assertIn("""<li class="list-group-item" id="Ecker2014a">""", res)
        self.assertInHTML("""<div class="d-flex mr-1">[<a>2</a>]</div>""", res)
        self.assertInHTML("""<a href="/publications/a.+s.+ecker/">A. S. Ecker</a>""", res)
        self.assertIn("""<li class="list-group-item" id="Gerhard2014a">""", res)
        self.assertInHTML("""<div class="d-flex mr-1">[<a>3</a>]</div>""", res)
        self.assertInHTML("""<a href="/publications/h.+gerhard/">H. Gerhard</a>""", res)
        self.assertIn("""<li class="list-group-item" id="Theis2011a">""", res)
        self.assertInHTML("""<div class="d-flex mr-1">[<a>4</a>]</div>""", res)
        self.assertInHTML("""<a href="/publications/l.+theis/">L. Theis</a>""", res)

        tpl_base = """{{% load publication_extras %}}
{{% setup_citations bibliography='{}' %}}
{{% cite 2 3 4 %}}
{{% thebibliography reset=True %}}"""
        for layout in ['card', 'list']:
            tpl = Template(tpl_base.format(layout))
            res = tpl.render(RequestContext(HttpRequest()))
            if layout == 'card':
                self.assertIn("""<div class="card mt-5 bibliography">""", res)
            elif layout == 'list':
                self.assertIn("""<div class="mt-5 bibliography">""", res)
                self.assertInHTML("""<h4>References</h4>""", res)
                self.assertIn("""<li id="Chagas2013a">""", res)
                self.assertInHTML("""<div class="d-flex mr-1">[<a>1</a>]</div>""", res)
                self.assertIn("""<ul class="list-unstyled">""", res)
                self.assertInHTML("""<a href="/publications/a.+chagas/">A. Chagas</a>""", res)
                self.assertIn("""<li id="Ecker2011a">""", res)
                self.assertInHTML("""<div class="d-flex mr-1">[<a>3</a>]</div>""", res)
                self.assertInHTML("""<a href="/publications/a.+s.+ecker/">A. S. Ecker</a>""", res)

        tpl = Template("""{% load publication_extras %}{% nocite 2 %}{% thebibliography sorting='foobar' %}""")
        self.assertRaises(NotImplementedError, tpl.render, RequestContext(HttpRequest()))

    def test_settings(self):
        # TODO: default values set in django.conf.settings
        pass


TEST_BIBLIOGRAPHY_COUNT = 11
TEST_BIBLIOGRAPHY = r"""
@article{Bethge2002c,
  author = "M. Bethge and D. Rotermund and K. Pawelzik",
  title = "Optimal short-term population coding: when Fisher information fails",
  year = 2002,
  journal = "Neural Computation",
  month = "Oct",
  keywords = "population coding, fisher information",
  doi = "10.1162/08997660260293247",
  url = "http://www.mitpressjournals.org/doi/abs/10.1162/08997660260293247"
}

@article{Simovski2011,
  author =        {Simovski, Constantin R.},
  journal =       {J. Opt.},
  month =         jan,
  number =        {1},
  pages =         {013001},
  title =         {{On electromagnetic characterization and
                   homogenization of nanostructured metamaterials}},
  volume =        {13},
  year =          {2011},
  doi =           {10.1088/2040-8978/13/1/013001},
  issn =          {2040-8978},
  url =           {http://stacks.iop.org/2040-8986/13/i=1/
                  a=013001?key=crossref.7321766a6630b917c6f066f2abc1e2cc},
}

@inproceedings{gerwinn2008bayesian,
  title={Bayesian inference for spiking neuron models with a sparsity prior},
  author={Gerwinn, Sebastian and Macke, Jakob and Seeger, Matthias and Bethge, Matthias},
  booktitle={Proceedings of the 21st Annual Conference on Neural Information Processing Systems},
  number={EPFL-CONF-161311},
  pages={529--536},
  year={2008},
  country={CH}
}

@article{hafner2000dynamical,
  title={A dynamical model of the inner Galaxy},
  author={H{\"a}fner, Ralf and Evans, N Wyn and Dehnen, Walter and Binney, James},
  journal={Monthly Notices of the Royal Astronomical Society},
  volume={314},
  number={3},
  pages={433--452},
  year={2000},
  publisher={Oxford University Press}
}

@misc{test:2009,
    title = "Test",
    author = {Last-Name, First and Peter van der Markt III and Test and Gauss II CF},
    year = 2009,
    country = {Wallis and Futuna},
    pages = {1-2}
}

@article{DBLP:journals/corr/KummererWB14,
 author    = {Matthias K{\"{u}}mmerer and
              Thomas Wallis and
              Matthias Bethge},
 title     = {How close are we to understanding image-based saliency?},
 journal   = {CoRR},
 year      = {2014},
 volume    = {abs/1409.7686},
 url       = {http://arxiv.org/abs/1409.7686},
 timestamp = {Mon, 27 Oct 2014 13:50:21 +0100},
 biburl    = {http://dblp.uni-trier.de/rec/bib/journals/corr/KummererWB14},
 bibsource = {dblp computer science bibliography, http://dblp.org}
}

@ARTICLE{2014arXiv1411.1045K,
   author = {{K{\"u}mmerer}, M. and {Theis}, L. and {Bethge}, M.},
    title = "{Deep Gaze I: Boosting Saliency Prediction with Feature Maps Trained on ImageNet}",
  journal = {ArXiv e-prints},
archivePrefix = "arXiv",
   eprint = {1411.1045},
 primaryClass = "cs.CV",
 keywords = {Computer Science - Computer Vision and Pattern Recognition, Quantitative Biology - Neurons and Cognition, Statistics - Applications},
     year = 2014,
    month = nov,
   adsurl = {http://adsabs.harvard.edu/abs/2014arXiv1411.1045K},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
@incollection{dougan2014objective,
  title={Objective Functions},
  author={Do{\u{g}}an, Haluk and Otu, Hasan H},
  booktitle={Multiple Sequence Alignment Methods},
  pages={45--58},
  year={2014},
  publisher={Springer}
}

@inproceedings{DBLP:conf/patmos/ShahWSB14,
  author    = {Syed Abbas Ali Shah and
               Jan Wagner and
               Thomas Schuster and
               Mladen Berekovic},
  title     = {A lightweight-system-level power and area estimation methodology for
               application specific instruction set processors},
  booktitle = {24th International Workshop on Power and Timing Modeling, Optimization
               and Simulation, PATMOS), Palma de Mallorca, Spain, September 29 -
               Oct. 1, 2014},
  pages     = {1--5},
  publisher = {{IEEE}},
  year      = {2014},
  url       = {http://dx.doi.org/10.1109/PATMOS.2014.6951886},
  doi       = {10.1109/PATMOS.2014.6951886},
  timestamp = {Tue, 18 Nov 2014 12:34:31 +0100},
  biburl    = {http://dblp.uni-trier.de/rec/bib/conf/patmos/ShahWSB14},
  bibsource = {dblp computer science bibliography, http://dblp.org},
  isbn      = {978-1-4799-5412-4}
}


@inproceedings{kay2015good,
  title={How Good is 85\%? A Survey Tool to Connect Classifier Evaluation to Acceptability of Accuracy},
  author={Kay, Matthew and Patel, Shwetak N and Kientz, Julie A},
  booktitle={Proceedings of the 33rd Annual ACM Conference on Human Factors in Computing Systems},
  pages={347--356},
  year={2015},
  organization={ACM},
  address = {New York, NY},
  country = {USA}
}

@article{doi:10.1080/00913367.1990.10673180,
  author = { Thomas E.   Barry },
  title = {Publication Productivity in the Three Leading U.S. Advertising Journals: Inaugural Issues through 1988},
  journal = {Journal of Advertising},
  volume = {19},
  number = {1},
  pages = {52-60},
  year = {1990},
  doi = {10.1080/00913367.1990.10673180},
  URL = {http://dx.doi.org/10.1080/00913367.1990.10673180},
  eprint = {http://dx.doi.org/10.1080/00913367.1990.10673180}
}
"""
