# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core import management
from django.db import migrations


def load_data(apps, schema_editor):
    management.call_command('loaddata', 'initial_data.json')


class Migration(migrations.Migration):
    dependencies = [
        ('publications_bootstrap', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data),
    ]
