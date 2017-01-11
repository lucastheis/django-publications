# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='location',
            field=models.CharField(help_text=b"Place of publication, location of conference, or publisher's address.", max_length=256, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='number',
            field=models.CharField(max_length=128, null=True, verbose_name=b'Issue number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='publication',
            name='volume',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
