# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-06 22:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babynamebook', '0009_auto_20170706_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='middle_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
