# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-04 08:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockapp', '0004_auto_20160602_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_index_name', models.CharField(max_length=100)),
                ('stock_index_data', models.FileField(upload_to='uploads')),
            ],
        ),
    ]