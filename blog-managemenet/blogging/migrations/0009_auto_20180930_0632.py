# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-30 06:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0008_auto_20180930_0531'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='data_added',
            new_name='date_added',
        ),
    ]
