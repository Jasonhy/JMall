# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 06:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20170420_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]