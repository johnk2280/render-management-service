from rest_framework.viewsets import ModelViewSet

from .models import Task
from .models import Status

from .serializers import TaskSerializer
from .serializers import StatusSerializer


class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class StatusModelViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
