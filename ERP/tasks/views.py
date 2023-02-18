from rest_framework import viewsets
from . models import Task
from . serializers import TaskSerializer, TaskCreateSerializer
from projects.permissions import ManagerOrReadAndPatchOnly


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (ManagerOrReadAndPatchOnly, )

    def get_serializer_class(self):
        if self.request.user.is_manager:
            return TaskCreateSerializer
        return TaskSerializer
