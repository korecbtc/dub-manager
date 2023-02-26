from rest_framework import viewsets
from . models import Task
from . serializers import TaskSerializer, TaskCreateSerializer
from . serializers import TaskAdminSerializer
from projects.permissions import ManagerOrReadAndPatchOnly
from django_filters.rest_framework import DjangoFilterBackend
import datetime
from django.utils import timezone


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
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
        '''Автоматическое удаление старых завершенных задач'''
        Task.objects.filter(
            time_create__lt=self.PERIOD_FOR_DELETE, status='finished'
            ).delete()
        return super().perform_create(serializer)
