from django.contrib import admin
from . models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'what_needed',
        'type',
        'urgency',
        'project',
        'description',
        'status',
        'time_create'
    )
