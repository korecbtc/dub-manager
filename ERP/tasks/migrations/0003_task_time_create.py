# Generated by Django 3.2.18 on 2023-02-25 12:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20230217_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Время создания'),
            preserve_default=False,
        ),
    ]
