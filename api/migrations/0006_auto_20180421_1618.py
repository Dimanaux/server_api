# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-21 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20180418_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(default='Train Rabbits', max_length=16),
        ),
    ]