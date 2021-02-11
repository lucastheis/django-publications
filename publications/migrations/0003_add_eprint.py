# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.core import management

class Migration(migrations.Migration):
	dependencies = [
		('publications', '0002_initial_data'),
	]

	operations = [
        migrations.AddField(
            model_name='publication',
            name='eprint',
            field=models.CharField(max_length=256, verbose_name='eprint', blank=True,
				help_text='Link to electronic (preprint) or eprint identifier'),
        ),
        migrations.AddField(
            model_name='publication',
            name='primaryclass',
            field=models.CharField(max_length=128, verbose_name='eprint class',
				blank=True, help_text='Preprint classification'),
        ),
        migrations.AddField(
            model_name='publication',
            name='archiveprefix',
            field=models.CharField(max_length=128, verbose_name='eprint type',
				blank=True, help_text='Name of preprint archive'),
        ),
	]
