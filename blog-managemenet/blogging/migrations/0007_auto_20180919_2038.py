# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-19 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0006_auto_20180919_0633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followed',
            field=models.ManyToManyField(to='blogging.Profile'),
        ),
    ]