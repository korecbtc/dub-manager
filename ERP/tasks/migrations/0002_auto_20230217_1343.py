# Generated by Django 2.2.19 on 2023-02-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='comments',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='Комментарий исполнителя'),
        ),
    ]
