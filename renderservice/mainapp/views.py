import random
import time

from django.db import models
from rest_framework import status
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView

from .models import Task
from .models import Status

from .serializers import TaskSerializer
from .serializers import StatusSerializer


class TaskModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
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


class StatusModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class TaskHistoryRetrieveAPIView(RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        data = {
            'error': 'ERROR'
        }
        try:
            task = Task.objects.get(id=kwargs['pk'])
            task_statuses = Status.objects.filter(task_id=task.id)
            data = {
                'task': TaskSerializer(task).data,
                'status_history': StatusSerializer(
                    task_statuses,
                    many=True,
                ).data,
            }
            response_status = status.HTTP_200_OK
        except Exception:
            response_status = status.HTTP_400_BAD_REQUEST
        # TODO: переписать try-except
        return Response(data, status=response_status)
