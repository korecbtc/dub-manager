# Generated by Django 2.2.19 on 2023-02-14 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Имя клиента')),
                ('address', models.CharField(max_length=256, verbose_name='Адрес')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Адрес электронной почты')),
                ('description', models.CharField(max_length=256, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название проекта')),
                ('date', models.DateField(verbose_name='Дата создания')),
                ('status', models.CharField(choices=[('in_progress', 'В работе'), ('finished', 'Завершен')], default='in_progress', max_length=150)),
                ('description', models.CharField(max_length=256, verbose_name='Описание проекта')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='projects.Client', verbose_name='Клиент')),
            ],
        ),
    ]
