# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-30 19:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0002_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='stock_data',
            field=models.FileField(default=0, upload_to='uploads/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stock',
            name='stock_name',
            field=models.CharField(max_length=100),
        ),
    ]
