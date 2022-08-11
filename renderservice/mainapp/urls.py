from django.urls import path
from django.urls import include

from rest_framework.routers import DefaultRouter

from .views import StatusModelViewSet
from .views import TaskCreateModelViewSet
from .views import TaskHistoryRetrieveAPIView
from .views import TaskModelViewSet

app_name = 'mainapp'

router = DefaultRouter()
router.register('tasks', TaskModelViewSet, basename='tasks')
router.register('task_create', TaskCreateModelViewSet, basename='task_create')
router.register('statuses', StatusModelViewSet, basename='statuses')

urlpatterns = [
    path('', include(router.urls)),
    path('task_history/<int:pk>', TaskHistoryRetrieveAPIView.as_view()),
]
