# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import echoices.fields
import publications_bootstrap.models


class Migration(migrations.Migration):

    dependencies = [
        ('publications_bootstrap', '0002_initial_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='month',
            field=echoices.fields.make_echoicefield(blank=True, echoices=publications_bootstrap.models.Publication.EMonths, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='status',
            field=echoices.fields.make_echoicefield(default=publications_bootstrap.models.Publication.EStatuses.PUBLISHED, echoices=publications_bootstrap.models.Publication.EStatuses),
        ),
    ]
