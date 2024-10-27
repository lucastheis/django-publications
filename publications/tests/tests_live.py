# -*- coding: utf-8 -*-

from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
from publications.tests import tests
from publications.models import Publication


class LiveTests(LiveServerTestCase):
	fixtures = ['initial_data.json', 'test_data.json']
	urls = 'publications.tests.urls'

	@classmethod
	def setUpClass(cls):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
		options.add_argument('--no-sandbox')

		cls.selenium = webdriver.Chrome(options=options)
		cls.wait = WebDriverWait(cls.selenium, timeout=5)

		super(LiveTests, cls).setUpClass()


	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super(LiveTests, cls).tearDownClass()


	def setUp(self):
		get_user_model().objects.create_superuser('admin', 'admin@test.de', 'admin')

		# login
		self.selenium.get('{0}{1}'.format(self.live_server_url, '/admin/'))
		username_input = self.selenium.find_element(By.NAME, 'username')
		username_input.send_keys('admin')
		password_input = self.selenium.find_element(By.NAME, 'password')
		password_input.send_keys('admin')
		self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()


	def tearDown(self):
		self.selenium.close()


	def test_import_bibtex(self):
		count = Publication.objects.count()

		self.selenium.get(
			'{0}{1}'.format(self.live_server_url, '/admin/publications/publication/import_bibtex/')
		)
		self.wait.until(presence_of_element_located((By.NAME, 'bibliography')))
		bibliography_input = self.selenium.find_element(By.NAME, 'bibliography')
		bibliography_input.send_keys(tests.TEST_BIBLIOGRAPHY)
		self.selenium.find_element(By.XPATH, '//input[@value="Import"]').click()

		self.assertEqual(Publication.objects.count() - count, tests.TEST_BIBLIOGRAPHY_COUNT)


	def test_import_bibtex_button(self):
		count = Publication.objects.count()

		self.selenium.get('{0}{1}'.format(self.live_server_url, '/admin/publications/publication/'))
		self.wait.until(presence_of_element_located((By.LINK_TEXT, 'Import BibTex')))
		self.selenium.find_element(By.LINK_TEXT, 'Import BibTex').click()
		self.selenium.find_element(By.XPATH, '//input[@value="Import"]').click()
