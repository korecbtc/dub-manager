from django.db import models
from projects.models import Project
from users.models import User


class Task(models.Model):
    CHOICES = (
        ('week', 'В течении недели'),
        ('day', 'В течении дня'),
        ('hour', 'В течении часа'),
        ('now', 'Срочно'),
        ('yesterday', 'Бросать все, делать это')
    )
    what_needed = models.CharField(
        max_length=100, verbose_name='Что нужно сделать (кратко)'
        )
    urgency = models.CharField(
        max_length=150, choices=CHOICES, default='day'
        )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='Клиент',
        )
    description = models.CharField(
        max_length=350, verbose_name='Что нужно сделать (подробно)'
        )
    manager = models.ForeignKey(
        User,
        on_delete=models.set_NULL,
        related_name='managers_tasks',
        verbose_name='Менеджер',
    )
