# -*- coding: utf-8 -*-
# Customized from Django 1.10 on 2017-01-04 
from __future__ import unicode_literals

from django.db import migrations


def set_refs_null(apps, schema_editor):
    Publication = apps.get_model('publications', 'Publication')
    for row in Publication.objects.all():
        changed = False
        if row.doi == '':
            row.doi = None
            changed = True
        if row.isbn == '':
            row.isbn = None
            changed = True
        if changed:
            row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0004_set_refs_null'),
    ]

    operations = [
        migrations.RunPython(set_refs_null),
    ]
