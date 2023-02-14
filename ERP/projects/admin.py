from django.contrib import admin
from . models import Client
from . models import Project


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'address',
        'email',
        'description',
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'date',
        'status',
        'description',
        'manager',
    )

    def get_manager(self, obj):
        if obj.is_manager:
            return obj