# Generated by Django 3.2.4 on 2022-02-25 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_release_notes", "0006_auto_20170905_2248"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="releasenote",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="releasenoteedit",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]