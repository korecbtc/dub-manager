import datetime

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from projects.permissions import ManagerOrReadAndPatchOnly
from rest_framework import exceptions, viewsets

from .models import Project, Task
from .serializers import (TaskAdminSerializer, TaskCreateSerializer,
                          TaskSerializer)


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-time_create')
    permission_classes = (ManagerOrReadAndPatchOnly, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'urgency', 'type']
    PERIOD_FOR_DELETE = timezone.now() - datetime.timedelta(days=7)

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_manager:
            return TaskCreateSerializer
        elif self.request.user.is_authenticated and self.request.user.is_admin:
            return TaskAdminSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        # Автоматическое удаление старых завершенных задач
        Task.objects.filter(
            time_create__lt=self.PERIOD_FOR_DELETE, status='finished'
            ).delete()
        # Менеджер может создвать задачи только по своим проектам
        if self.request.method == 'POST' and self.request.user.is_manager:
            owners_projects = Project.objects.filter(manager=self.request.user)
            if serializer.validated_data['project'] not in owners_projects:
                raise exceptions.PermissionDenied(
                    detail='You do not have permission to perform this action')
        serializer.save()
