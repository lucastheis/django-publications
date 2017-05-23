# -*- coding: utf-8 -*-

from django.db import models

from ..models import Publication


class PublicationLink(models.Model):
    class Meta:
        app_label = 'publications_bootstrap'  # Fix for Django<1.7

    publication = models.ForeignKey(Publication)
    description = models.CharField(max_length=256)
    url = models.URLField(verbose_name='URL')

    def __unicode__(self):
        return self.description

    def __str__(self):
        return self.description
