# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-16 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apuestas', '0003_auto_20180607_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneos',
            name='activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='torneos',
            name='fechas',
            field=models.IntegerField(default=0),
        ),
    ]
