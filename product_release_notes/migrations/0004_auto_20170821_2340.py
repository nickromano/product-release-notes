# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 23:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_release_notes', '0003_client_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='current_version',
        ),
        migrations.AlterField(
            model_name='releasenote',
            name='version',
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
    ]
