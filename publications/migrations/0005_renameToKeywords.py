# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0004_remove_publication_keywords'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publication',
            old_name='tags',
            new_name='keywords',
        ),
    ]
