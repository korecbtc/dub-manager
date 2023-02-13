from . models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для исполнителя"""
    project = serializers.StringRelatedField(read_only=True)
    manager = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'what_needed',
            'type',
            'urgency',
            'project',
            'description',
            'manager',
            'status',
            'comments',
        )
        read_only_fields = (
            'what_needed',
            'type',
            'urgency',
            'project',
            'description',
            'manager',
        )
