# -*- coding: utf-8 -*-

from time import sleep

from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver

from ..models import Publication
from ..tests import tests


class LiveTests(LiveServerTestCase):
    fixtures = ['initial_data.json', 'test_data.json']
    urls = 'publications_bootstrap.tests.urls'

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.PhantomJS()
        super(LiveTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LiveTests, cls).tearDownClass()

    def setUp(self):
        User.objects.create_superuser('admin', 'admin@test.de', 'admin')

        # give the browser a little time
        sleep(1.)

        # login
        self.selenium.get('{0}{1}'.format(self.live_server_url, '/admin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

    def test_import_bibtex(self):
        count = Publication.objects.count()

        self.selenium.get('{0}{1}'.format(
            self.live_server_url,
            '/admin/publications_bootstrap/publication/import_bibtex/'))
        bibliography_input = self.selenium.find_element_by_name("bibliography")
        bibliography_input.send_keys(tests.TEST_BIBLIOGRAPHY)
        self.selenium.find_element_by_xpath('//input[@value="Import"]').click()

        self.assertEqual(Publication.objects.count() - count, tests.TEST_BIBLIOGRAPHY_COUNT)

    def test_import_bibtex_button(self):
        count = Publication.objects.count()

        self.selenium.get(
            '{0}{1}'.format(self.live_server_url, '/admin/publications_bootstrap/publication/'))
        self.selenium.find_element_by_link_text('Import BibTex').click()
        self.selenium.find_element_by_xpath('//input[@value="Import"]').click()
