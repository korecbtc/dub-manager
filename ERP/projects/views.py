from rest_framework import viewsets
from . models import Project, Client
from . serializers import ProjectSerializer, ProjectCreateSerializer
from . serializers import ClientCreateSerializer, ClientSerializer


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer


class ClientViewset(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer
