# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 20:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('name', 'user')]),
        ),
    ]