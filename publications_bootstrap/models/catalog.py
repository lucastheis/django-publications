# -*- coding: utf-8 -*-

from django.db import models


class Catalog(models.Model):
    """
    Model representing a list of publications.
    """

    class Meta:
        ordering = ('title',)
        app_label = 'publications_bootstrap'  # Fix for Django<1.7

    title = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=128)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
