# -*- coding: utf-8 -*-
# Customized from Django 1.10 on 2017-01-04 
from __future__ import unicode_literals

from django.db import migrations
import publications.fields


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_simplified_meta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='doi',
            field=publications.fields.NullCharField(blank=True, max_length=128, null=True, verbose_name='DOI'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='isbn',
            field=publications.fields.NullCharField(blank=True, help_text='Only for a book.', max_length=32, null=True, verbose_name='ISBN'),
        ),
    ]
