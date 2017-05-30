# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core import management
from django.db import migrations

app_label = 'publications_bootstrap'
fixture = 'initial_data'


def load_fixtures(apps, schema_editor):
    management.call_command('loaddata', fixture, app_label=app_label)


class Migration(migrations.Migration):
    dependencies = [
        (app_label, '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixtures),
    ]
