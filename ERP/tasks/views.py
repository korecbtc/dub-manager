from rest_framework import viewsets
from . models import Task
from . serializers import TaskSerializer, TaskCreateSerializer
from django.core.exceptions import PermissionDenied


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_manager:
            return TaskCreateSerializer
        if (self.request.user.is_executer and
                self.request.method in ('GET', 'PATCH')):
            return TaskSerializer
        raise PermissionDenied()
