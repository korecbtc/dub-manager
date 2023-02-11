from django.db import models
from projects.models import Project
from users.models import User


class Task(models.Model):
    CHOICES_URGENCY = (
        ('week', 'В течении недели'),
        ('day', 'В течении дня'),
        ('hour', 'В течении часа'),
        ('now', 'Срочно'),
        ('yesterday', 'Бросать все, делать это')
    )
    CHOICES_STATUS = (
        ('in_progress', 'В работе'),
        ('finished', 'Завершено'),
        ('not_viewed', 'Не просмотрено')
    )
    CHOICES_TYPE = (
        ('send', 'Отправка материалов'),
        ('receive', 'Получение материалов'),
        ('transport', 'Перемещение материалов внутри студии'),
        ('patch', 'Переделать/Изменить материалы'),
        ('other', 'Другое')
    )
    what_needed = models.CharField(
        max_length=100, verbose_name='Что нужно сделать (кратко)',
        unique=True
        )
    type = models.CharField(
        max_length=150, choices=CHOICES_TYPE, default='receive'
        )
    urgency = models.CharField(
        max_length=150, choices=CHOICES_URGENCY, default='day'
        )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Проект',
        )
    description = models.CharField(
        max_length=350, verbose_name='Что нужно сделать (подробно)'
        )
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managers_tasks',
        verbose_name='Менеджер',
    )
    status = models.CharField(
        max_length=150,
        choices=CHOICES_STATUS, default='not_viewed',
        verbose_name='Статус'
        )

    def __str__(self):
        return self.what_needed
