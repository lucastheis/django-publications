# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import publications_bootstrap.fields
import echoices.fields
import publications_bootstrap.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256)),
                ('file', models.FileField(upload_to='publications_bootstrap/')),
            ],
        ),
        migrations.CreateModel(
            name='PublicationLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256)),
                ('url', models.URLField(verbose_name='URL')),
            ],
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citekey', publications_bootstrap.fields.NullCharField(blank=True, help_text='BibTex citation key. Leave blank if unsure.', max_length=512, null=True, unique=True)),
                ('title', models.CharField(max_length=512)),
                ('authors', models.CharField(help_text='List of authors separated by commas or <i>and</i>.', max_length=2048)),
                ('year', models.PositiveIntegerField()),
                ('month', echoices.fields.make_echoicefield(blank=True, echoices=publications_bootstrap.models.Publication.EMonths, null=True),),
                ('journal', models.CharField(blank=True, max_length=256)),
                ('book_title', models.CharField(blank=True, help_text='Title of a book, part of which is being cited. See the LATEX book for how to type titles. For book entries, use the `title` field instead', max_length=256)),
                ('publisher', models.CharField(blank=True, max_length=256)),
                ('editor', models.CharField(blank=True, help_text='Name(s) of editor(s), typed as indicated in the LATEX book. If there is also an `author` field, then the `editor` field gives the editor of the book or collection in which the reference appears.', max_length=256)),
                ('edition', models.CharField(blank=True, help_text='The edition of a book -- for example, "Second". This should be an ordinal, and should have the first letter capitalized.', max_length=256)),
                ('institution', models.CharField(blank=True, max_length=256)),
                ('school', models.CharField(blank=True, help_text='The name of the school where a thesis was written.', max_length=256)),
                ('organization', models.CharField(blank=True, help_text='The organization that sponsors a conference or that publishes a manual.', max_length=256)),
                ('location', models.CharField(blank=True, help_text="Place of publication, location of conference, or publisher's address.", max_length=256)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('series', models.CharField(blank=True, help_text='The name of a series or set of books. When citing an entire book, the `title` field gives its title and an optional `series` field gives the name of a series or multi-volume set in which the book is published.', max_length=256)),
                ('volume', models.CharField(blank=True, max_length=128, null=True)),
                ('number', models.CharField(blank=True, help_text='The number of a journal, magazine, technical report, or of a work in a series. An issue of a journal or magazine is usually identified by its volume and number; the organization that issues a technical report usually gives it a number; and sometimes books are given numbers in a named series.', max_length=128, null=True, verbose_name='Issue number')),
                ('chapter', models.CharField(blank=True, max_length=128, null=True)),
                ('section', models.CharField(blank=True, max_length=128, null=True)),
                ('pages', publications_bootstrap.fields.PagesField(blank=True, max_length=32)),
                ('note', models.CharField(blank=True, help_text='Any additional information that can help the reader. The first word should be capitalized.', max_length=256)),
                ('tags', models.CharField(blank=True, help_text='List of tags separated by commas.', max_length=256)),
                ('url', models.URLField(blank=True, help_text='Link to PDF or journal page.', verbose_name='URL')),
                ('code', models.URLField(blank=True, help_text='Link to page with code.')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='publications_bootstrap/', verbose_name='PDF')),
                ('image', models.ImageField(blank=True, null=True, upload_to='publications_bootstrap/images/')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='publications_bootstrap/thumbnails/')),
                ('external', models.BooleanField(default=False, help_text='If publication was written in another lab, mark as external.')),
                ('abstract', models.TextField(blank=True)),
                ('doi', publications_bootstrap.fields.NullCharField(blank=True, max_length=128, null=True, unique=True, verbose_name='DOI')),
                ('isbn', publications_bootstrap.fields.NullCharField(blank=True, help_text='Only for a book.', max_length=32, null=True, unique=True, verbose_name='ISBN')),
                ('status', echoices.fields.make_echoicefield(default=publications_bootstrap.models.Publication.EStatuses.PUBLISHED, echoices=publications_bootstrap.models.Publication.EStatuses)),
                ('catalogs', models.ManyToManyField(blank=True, to='publications_bootstrap.Catalog')),
            ],
            options={
                'ordering': ['-year', '-month', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('title', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(max_length=128)),
                ('bibtex_types', models.CharField(default='article', help_text='Possible BibTex types, separated by comma.', max_length=256, verbose_name='BibTex types')),
                ('hidden', models.BooleanField(default=False, help_text='Hide publications from main view.')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.AddField(
            model_name='publication',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications_bootstrap.Type'),
        ),
        migrations.AddField(
            model_name='publicationlink',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications_bootstrap.Publication'),
        ),
        migrations.AddField(
            model_name='publicationfile',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publications_bootstrap.Publication'),
        ),
    ]
