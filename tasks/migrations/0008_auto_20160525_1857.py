# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-25 16:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_comment_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task'),
        ),
        migrations.AlterField(
            model_name='timelog',
            name='spend_time',
            field=models.PositiveIntegerField(default=0),
        ),
    ]