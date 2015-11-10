# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
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
                ('file', models.FileField(upload_to='publications/')),
            ],
        ),
        migrations.CreateModel(
            name='CustomLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=256)),
                ('url', models.URLField(verbose_name='URL')),
            ],
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
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('citekey', models.CharField(null=True, help_text='BibTex citation key. Leave blank if unsure.', max_length=512, blank=True)),
                ('title', models.CharField(max_length=512)),
                ('authors', models.CharField(help_text='List of authors separated by commas or <i>and</i>.', max_length=2048)),
                ('year', models.PositiveIntegerField()),
                ('month', models.IntegerField(null=True, blank=True, choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('journal', models.CharField(max_length=256, blank=True)),
                ('book_title', models.CharField(max_length=256, blank=True)),
                ('publisher', models.CharField(max_length=256, blank=True)),
                ('institution', models.CharField(max_length=256, blank=True)),
                ('volume', models.IntegerField(null=True, blank=True)),
                ('number', models.IntegerField(null=True, verbose_name='Issue number', blank=True)),
                ('pages', publications.fields.PagesField(max_length=32, blank=True)),
                ('note', models.CharField(max_length=256, blank=True)),
                ('keywords', models.CharField(help_text='List of keywords separated by commas.', max_length=256, blank=True)),
                ('url', models.URLField(verbose_name='URL', help_text='Link to PDF or journal page.', blank=True)),
                ('code', models.URLField(help_text='Link to page with code.', blank=True)),
                ('pdf', models.FileField(null=True, verbose_name='PDF', blank=True, upload_to='publications/')),
                ('image', models.ImageField(null=True, upload_to='publications/images/', blank=True)),
                ('thumbnail', models.ImageField(null=True, upload_to='publications/thumbnails/', blank=True)),
                ('doi', models.CharField(verbose_name='DOI', max_length=128, blank=True)),
                ('external', models.BooleanField(default=False, help_text='If publication was written in another lab, mark as external.')),
                ('abstract', models.TextField(blank=True)),
                ('isbn', models.CharField(verbose_name='ISBN', help_text='Only for a book.', max_length=32, blank=True)),
                ('lists', models.ManyToManyField(blank=True, to='publications.List')),
            ],
            options={
                'ordering': ['-year', '-month', '-id'],
                'verbose_name_plural': ' Publications',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('type', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128)),
                ('bibtex_types', models.CharField(verbose_name='BibTex types', default='article', max_length=256, help_text='Possible BibTex types, separated by comma.')),
                ('hidden', models.BooleanField(default=False, help_text='Hide publications from main view.')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': '  Types',
            },
        ),
        migrations.AddField(
            model_name='publication',
            name='type',
            field=models.ForeignKey(to='publications.Type'),
        ),
        migrations.AddField(
            model_name='customlink',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
        ),
        migrations.AddField(
            model_name='customfile',
            name='publication',
            field=models.ForeignKey(to='publications.Publication'),
        ),
    ]
