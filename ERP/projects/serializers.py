from rest_framework import serializers
from . models import Project, Client


class ClientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения"""
    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'address',
            'email',
            'description',
        )
        read_only_fields = (
            'id',
            'name',
            'address',
            'email',
            'description',
        )


class ClientCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для менеджера"""
    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'address',
            'email',
            'description',
        )


class ProjectSerializer(serializers.ModelSerializer):
    """Сериализатор для исполнителя"""
    client = serializers.StringRelatedField(many=False, read_only=True)
    manager = serializers.StringRelatedField(many=False, read_only=True)

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

    def to_representation(self, value):
        """Отклик на POST запрос обрабатывается другим сериализатором"""
        return ProjectSerializer(
            value,
            context={'request': self.context.get('request')}
        ).data
