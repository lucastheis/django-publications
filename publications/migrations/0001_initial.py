# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import publications.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=256)),
                ('file', models.FileField(upload_to=b'publications/')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=256)),
                ('url', models.URLField(verbose_name=b'URL')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('list', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('list',),
                'verbose_name_plural': 'Lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('citekey', models.CharField(help_text=b'BibTex citation key. Leave blank if unsure.', max_length=512, null=True, blank=True)),
                ('title', models.CharField(max_length=512)),
                ('authors', models.CharField(help_text=b'List of authors separated by commas or <i>and</i>.', max_length=2048)),
                ('year', models.PositiveIntegerField(max_length=4)),
                ('month', models.IntegerField(blank=True, null=True, choices=[(1, b'January'), (2, b'February'), (3, b'March'), (4, b'April'), (5, b'May'), (6, b'June'), (7, b'July'), (8, b'August'), (9, b'September'), (10, b'October'), (11, b'November'), (12, b'December')])),
                ('journal', models.CharField(max_length=256, blank=True)),
                ('book_title', models.CharField(max_length=256, blank=True)),
                ('publisher', models.CharField(max_length=256, blank=True)),
                ('institution', models.CharField(max_length=256, blank=True)),
                ('volume', models.IntegerField(null=True, blank=True)),
                ('number', models.IntegerField(null=True, verbose_name=b'Issue number', blank=True)),
                ('pages', publications.fields.PagesField(max_length=32, blank=True)),
                ('note', models.CharField(max_length=256, blank=True)),
                ('keywords', models.CharField(help_text=b'List of keywords separated by commas.', max_length=256, blank=True)),
                ('url', models.URLField(help_text=b'Link to PDF or journal page.', verbose_name=b'URL', blank=True)),
                ('code', models.URLField(help_text=b'Link to page with code.', blank=True)),
                ('pdf', models.FileField(upload_to=b'publications/', null=True, verbose_name=b'PDF', blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'publications/images/', blank=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'publications/thumbnails/', blank=True)),
                ('doi', models.CharField(max_length=128, verbose_name=b'DOI', blank=True)),
                ('external', models.BooleanField(default=False, help_text=b'If publication was written in another lab, mark as external.')),
                ('abstract', models.TextField(blank=True)),
                ('isbn', models.CharField(help_text=b'Only for a book.', max_length=32, verbose_name=b'ISBN', blank=True)),
                ('lists', models.ManyToManyField(to='publications.List', blank=True)),
            ],
            options={
                'ordering': ['-year', '-month', '-id'],
                'verbose_name_plural': ' Publications',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('type', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('bibtex_types', models.CharField(default=b'article', help_text=b'Possible BibTex types, separated by comma.', max_length=256, verbose_name=b'BibTex types')),
                ('hidden', models.BooleanField(default=False, help_text=b'Hide publications from main view.')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': '  Types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='publication',
            name='type',
            field=models.ForeignKey(to='publications.Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customlink',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customfile',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
            preserve_default=True,
        ),
    ]
