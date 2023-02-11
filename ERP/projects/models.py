from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя клиента')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    email = models.EmailField(
        unique=True, verbose_name='Адрес электронной почты'
        )
    description = models.CharField(max_length=256, verbose_name='Описание')

    def __str__(self):
        return self.name


class Project(models.Model):
    CHOICES = (
        ('in_progress', 'В работе'), ('finished', 'Завершен')
    )
    name = models.CharField(max_length=256, verbose_name='Название проекта')
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='projects',
                               verbose_name='Клиент',
                               )
    date = models.DateField(auto_now_add=False, verbose_name='Дата создания')
    status = models.CharField(
        max_length=150, choices=CHOICES, default='in_progress'
        )
    description = models.CharField(
        max_length=256, verbose_name='Описание проекта'
        )

    def __str__(self):
        return self.name
