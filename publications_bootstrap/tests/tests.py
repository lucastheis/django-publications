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

    def setUp(self):
        User.objects.create_superuser('admin', 'admin@test.de', 'admin')

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

    def test_unapi(self):
        self.assertEqual(self.client.get('/publications/unapi/').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=1').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=1&format=mods').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=1&format=bibtex').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=1&format=ris').status_code, 200)
        self.assertEqual(self.client.get('/publications/unapi/?id=99999&format=bibtex').status_code, 404)
        self.assertEqual(self.client.get('/publications/unapi/?id=1&format=foobar').status_code, 406)

    def test_admin(self):
        self.client.login(username='admin', password='admin')

        self.assertEqual(self.client.get('/publications/').status_code, 200)
        self.assertEqual(self.client.get('/admin/publications_bootstrap/type/6/move-up/', follow=True).status_code, 200)
        self.assertEqual(self.client.get('/admin/publications_bootstrap/type/6/move-down/', follow=True).status_code,
                         200)

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

    def test_extras(self):
        link = PublicationLink.objects.create(publication_id=1, description='Test', url='http://test.com')
        link.save()

        publication = Publication.objects.get(pk=1)
        highlights_catalog = Catalog.objects.get(title__iexact='highlights')

        # add publication to catalog
        publication.catalogs.add(highlights_catalog)

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
{% get_publication 100 %}
{% get_publications %}
""")

        self.assertGreater(len(tpl.render(RequestContext(HttpRequest())).strip()), 0)

        # tex_parse is used to replace simple LaTeX code in publication titles
        self.assertEqual(tex_parse(u'$L_p$-spherical'), u'L<sub>p</sub>-spherical')
        self.assertEqual(tex_parse(u'$L^2$-spherical'), u'L<sup>2</sup>-spherical')


TEST_BIBLIOGRAPHY_COUNT = 10
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
"""
