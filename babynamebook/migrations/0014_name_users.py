# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-20 00:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('babynamebook', '0013_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='name',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
