from django.urls import path, include
from . views import TaskViewset
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('tasks', TaskViewset, basename='tasks')
urlpatterns = [
    path('', include(router.urls)),
]
