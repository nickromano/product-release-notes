# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 03:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_release_notes", "0002_releasenote_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="icon",
            field=models.CharField(
                choices=[
                    ("desktop", "Desktop"),
                    ("apple", "Apple"),
                    ("android", "Android"),
                ],
                default="desktop",
                max_length=20,
            ),
        ),
    ]
