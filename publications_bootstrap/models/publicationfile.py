# -*- coding: utf-8 -*-

from django.db import models

from ..models import Publication


class PublicationFile(models.Model):
    class Meta:
        app_label = 'publications_bootstrap'  # Fix for Django<1.7

    publication = models.ForeignKey(Publication)
    description = models.CharField(max_length=256)
    file = models.FileField(upload_to='publications_bootstrap/')

    def __unicode__(self):
        return self.description

    def __str__(self):
        return self.description
