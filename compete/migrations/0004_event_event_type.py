# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-07 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compete', '0003_fixture_fixture_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]