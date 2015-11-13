# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.text import slugify


def keywords_to_tags(apps, schema_editor):

    Publication = apps.get_model('publications', 'Publication')
    Tag = apps.get_model('taggit', 'Tag')
    TaggedItem = apps.get_model('taggit', 'TaggedItem')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    ct = ContentType.objects.get_for_model(Publication)

    for publication in Publication.objects.all():
        for keyword in publication.keywords.split(','):
            keyword = keyword.strip()
            try:
                tag = Tag.objects.get(slug=slugify(keyword))
            except Tag.DoesNotExist:
                tag = Tag(
                    name=keyword,
                    slug=slugify(keyword)
                )
                tag.save()

            ti, _ = TaggedItem.objects.get_or_create(
                content_type=ct,
                object_id=publication.id,
                tag=tag
            )


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('publications', '0002_addTaggit'),
    ]

    operations = [
        migrations.RunPython(keywords_to_tags)
    ]
