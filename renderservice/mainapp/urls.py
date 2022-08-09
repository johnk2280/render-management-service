from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import TaskModelViewSet
from .views import StatusModelViewSet

app_name = 'mainapp'

router = DefaultRouter()
router.register('tasks', TaskModelViewSet, basename='tasks')
router.register('statuses', StatusModelViewSet, basename='statuses')

urlpatterns = [
    path('', include(router.urls)),
]
