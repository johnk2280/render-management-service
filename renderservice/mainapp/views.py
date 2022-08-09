import random
import time

from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Task
from .models import Status

from .serializers import TaskSerializer
from .serializers import StatusSerializer


class TaskModelViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self._render(serializer.instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _render(self, new_task: Task) -> bool:
        Status(task=new_task, name='rendering').save()
        print('start')
        time.sleep(random.randint(60, 300))
        Status(task=new_task, name='complete').save()
        print('stop')
        return True


class StatusModelViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

#
# class TaskStatusHistoryViewSet(ViewSet):
#     def retrieve(self, request, pk=None):
#         pass
