from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CHOICES = (
        ('manager', 'Менеджер'), ('executer', 'Исполнитель')
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    role = models.CharField(
        max_length=150, choices=CHOICES, default='executer'
        )
    username = models.CharField(
        max_length=150,
        null=True,
        unique=True,
        verbose_name='Имя пользователя'
    )

    @property
    def is_executer(self):
        return self.role == 'executer'

    @property
    def is_manager(self):
        return self.role == 'manager'
