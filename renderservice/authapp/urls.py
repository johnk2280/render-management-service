from django.urls import path
from django.urls import include

# from rest_framework.routers import DefaultRouter
#
# from .views import StatusModelViewSet
# from .views import TaskHistoryRetrieveAPIView
# from .views import TaskModelViewSet
# from .views import UserRegisterAPIView

app_name = 'authapp'

# router = DefaultRouter()
# router.register('tasks', TaskModelViewSet, basename='tasks')
# router.register('statuses', StatusModelViewSet, basename='statuses')
#
# urlpatterns = [
#     path('', include(router.urls)),
#     path('task_history/<int:pk>', TaskHistoryRetrieveAPIView.as_view()),
#     path('registration', UserRegisterAPIView.as_view()),
# ]
