from rest_framework import viewsets
from . models import Task
from . serializers import TaskSerializer, TaskCreateSerializer


class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

