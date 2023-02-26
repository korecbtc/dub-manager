from . models import Task
from projects.serializers import ProjectSerializer
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор для исполнителя"""
    project = ProjectSerializer(many=False, read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'what_needed',
            'type',
            'urgency',
            'project',
            'description',
            'status',
            'comments',
            'time_create',
        )
        read_only_fields = (
            'id',
            'what_needed',
            'type',
            'urgency',
            'project',
            'description',
            'time_create',
        )


class TaskCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для менеджера"""

    class Meta:
        model = Task
        fields = (
            'id',
            'what_needed',
            'type',
            'urgency',
            'project',
            'description',
            'status',
            'comments',
            'time_create',
        )
        read_only_fields = (
            'status',
            'comments',
        )

    def to_representation(self, value):
        """Отклик на POST запрос обрабатывается другим сериализатором"""
        return TaskSerializer(
            value,
            context={'request': self.context.get('request')}
        ).data


class TaskAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для администратора"""

    class Meta:
        model = Task
        fields = (
            'id',
            'what_needed',
            'type',
            'urgency',
            'project',
            'description',
            'status',
            'comments',
            'time_create',
        )

    def to_representation(self, value):
        """Отклик на POST запрос обрабатывается другим сериализатором"""
        return TaskSerializer(
            value,
            context={'request': self.context.get('request')}
        ).data
