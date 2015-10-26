# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
                ('hacker_news_url', models.URLField(unique=True, max_length=255)),
                ('posted_on', models.DateTimeField()),
                ('upvotes', models.IntegerField()),
                ('comments', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('user_deleted', models.ManyToManyField(related_name='deleted_items', to=settings.AUTH_USER_MODEL)),
                ('user_read', models.ManyToManyField(related_name='read_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
