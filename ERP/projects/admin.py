from django.contrib import admin

from .models import Client, Project


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'email',
        'description',
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'date',
        'status',
        'description',
        'manager',
    )

    def get_manager(self, obj):
        if obj.is_manager:
            return obj