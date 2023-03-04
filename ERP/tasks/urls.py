from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewset

router = DefaultRouter()
router.register('tasks', TaskViewset, basename='tasks')
urlpatterns = [
    path('', include(router.urls)),
]
