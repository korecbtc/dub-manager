from django.urls import path, include
from . views import ProjectViewset, ClientViewset
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('projects', ProjectViewset, basename='projects')
router.register('clients', ClientViewset, basename='projects')
urlpatterns = [
    path('', include(router.urls)),
]
