from rest_framework import serializers
from . models import Project


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор для исполнителя"""
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'client',
            'date',
            'status',
            'description',
            'manager',
        )
        read_only_fields = (
            'id',
            'name',
            'client',
            'date',
            'status',
            'description',
            'manager',
        )


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для менеджера"""
    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'client',
            'date',
            'status',
            'description',
            'manager',
        )
