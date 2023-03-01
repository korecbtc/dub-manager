from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    CHOICES = (
        ('manager', 'Менеджер'),
        ('executer', 'Исполнитель'),
        ('admin', 'Администратор')
    )
    first_name = models.CharField(
        max_length=150, blank=False, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, blank=False, verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    role = models.CharField(
        max_length=150, choices=CHOICES, default='executer'
        )
    username = models.CharField(
        max_length=150,
        null=False,
        unique=True,
        verbose_name='Имя пользователя'
    )
    password = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Пароль'
    )

    @property
    def is_executer(self):
        return self.role == 'executer'

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_admin(self):
        return self.role == 'admin'
