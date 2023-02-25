from rest_framework import viewsets
from . models import Task
from . serializers import TaskSerializer, TaskCreateSerializer
from . serializers import TaskAdminSerializer
from projects.permissions import ManagerOrReadAndPatchOnly
from django_filters.rest_framework import DjangoFilterBackend


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (ManagerOrReadAndPatchOnly, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'urgency', 'type']

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_manager:
            return TaskCreateSerializer
        elif self.request.user.is_authenticated and self.request.user.is_admin:
            return TaskAdminSerializer
        return TaskSerializer
