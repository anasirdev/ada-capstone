# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-10 14:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('babynamebook', '0010_person_middle_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]