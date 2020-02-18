# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-02-17 19:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0008_auto_20200217_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.CharField(choices=[('Bug', 'Bug'), ('Feature', 'Feature')], max_length=10),
        ),
    ]
