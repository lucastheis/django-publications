# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_moveToTaggit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='keywords',
        ),
    ]
