__license__ = 'MIT License <http://www.opensource.org/licenses/mit-license.php>'
__author__ = 'Lucas Theis <lucas@theis.io>'
__docformat__ = 'epytext'

from django.db import models

class List(models.Model):
	"""
	Model representing a list of publications.
	"""

	class Meta:
		app_label = 'publications'
		ordering = ('list',)
		verbose_name_plural = 'Lists'

	list = models.CharField(max_length=128)
	description = models.CharField(max_length=128)

	def __unicode__(self):
		return self.list

	def __str__(self):
		return self.list
