# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-10 09:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0006_blog_read_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogDraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('text', models.TextField()),
                ('category', models.CharField(blank=True, max_length=500, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
