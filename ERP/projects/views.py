from rest_framework import viewsets
from . models import Project, Client
from . serializers import ProjectSerializer, ProjectCreateSerializer
from . serializers import ClientCreateSerializer, ClientSerializer
from . permissions import ManagerOrReadOnly, ManagerOnly
from django_filters.rest_framework import DjangoFilterBackend


class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = (ManagerOrReadOnly, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'client', 'manager']

    def get_serializer_class(self):
        if self.request.user.is_manager or self.request.user.is_admin:
            return ProjectCreateSerializer
        return ProjectSerializer


class ClientViewset(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientCreateSerializer
    permission_classes = (ManagerOnly, )
